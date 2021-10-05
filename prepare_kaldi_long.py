import sys
import os
import time
import logging
import argparse
from libs.misc_utils import (find_files, read_file,
                             write_file, get_interview_name)


def batch_run(wavs_dir):
    logging.info('Starting long files Kaldi preparation')

    wav_files = find_files(wavs_dir, '.wav', 'segs')

    long_list = []
    for wav_file in wav_files:
        print(wav_file)
        interview = get_interview_name(wav_file)
        dia_status_file_name = 'dia_status.run'
        logging.info('Starting long files Kaldi preparation on "%s"',
                     interview)
        tic = time.time()
        wav_folder = os.path.dirname(wav_file)
        dia_status_file = f'{wav_folder}/{dia_status_file_name}'
        rttm_file = os.path.splitext(wav_file)[0] + ".rttm"
        rttm_list = read_file(rttm_file)
        wav_id = os.path.splitext(os.path.basename(wav_file))[0]
        for line in rttm_list:
            st, dur, spk = line.split(' ')
            st = float(st)
            dur = float(dur)
            end = round(st + dur, 3)
            spk = ''.join(set([str(ii) for ii in spk]))
            utt_id = f'{wav_id}_{st}_{end}_{spk}'
            long_list.append({'wav_id': wav_id, 'wav_file': wav_file,
                              'utt_id': utt_id, 'st': st, 'end': end})
        write_file(['Completed'], dia_status_file)
        toc = time.time()
        logging.time_info(f'Kaldi preparation of "{interview}" processed in'
                          f' {(toc - tic):.3f} seconds.')

    long_list.sort(key=lambda line: line['st'])
    write_file(set([f'{line["wav_id"]} {line["wav_file"]}'
               for line in long_list]), f'{wavs_dir}/wav.scp')
    write_file([f'{line["utt_id"]} {line["utt_id"]}'
               for line in long_list], f'{wavs_dir}/utt2spk')
    write_file([f'{line["utt_id"]} {line["wav_id"]} {line["st"]} {line["end"]}'
               for line in long_list], f'{wavs_dir}/segments')

    logging.info('Finished long files Kaldi preparation')


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Prepares Kaldi data files for long video files.')
    parser.add_argument('wavs_dir', metavar='folder', nargs='?', default='/mnt/video/audio', help='Set the folder from where to retrieve the audio files. Default: /mnt/video/audio')
    parser.add_argument('-l', '--log-level', dest='log_level', default='ERROR', type=str, help='Set the log level of this program. Default: ERROR')
    args = parser.parse_args()

    loglevel = args.log_level
    FORMAT = '%(asctime)s %(levelname)s: %(message)s'
    formatter = logging.Formatter(FORMAT)
    logging.basicConfig(filename='/opt/gen_rttm.log', format=FORMAT,
                        level=loglevel.upper())

    def time_info(msg, *args, **kwargs):
        if logging.getLogger().isEnabledFor(60):
            logging.log(60, msg)

    logging.addLevelName(60, "TIME_INFO")
    logging.time_info = time_info
    logging.Logger.time_info = time_info

    console = logging.StreamHandler()
    console.setLevel(loglevel.upper())
    console.setFormatter(formatter)
    logging.getLogger().addHandler(console)

    if os.path.isdir(args.wavs_dir):
        batch_run(args.wavs_dir)
    else:
        print(f'Error: Folder {args.wavs_dir} does not exist')
        sys.exit(1)
