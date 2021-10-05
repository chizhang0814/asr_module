import sys, re, glob
import os, shutil


def generate_phone_alignment(files, dir_name):
    pron = []

    # process each file
    ii = 1
    for filei in files:
        #print("  filei =" + filei)
        file_name = os.path.basename(filei)
        f = open(filei, 'r')
        header = False
        fout = open(dir_name + '/' + file_name, 'w')
        print("----", ii, "dir-file: ", dir_name + '/' + file_name)
        jj = 1
        for line in f:
            #print("  ------------jj = ", jj)
            if header:
                header = False
                continue
            line = line.split("\t")
            #print("line = ", line)
            seg_id = line[0]
            file = line[1]
            file = file.strip()
            phon_pos = line[6]
            # print phon_pos
            if phon_pos == "SIL":
                phon_pos = "SIL_S"
            phon_pos = phon_pos.split("_")
            #print("  phon_pos = ", phon_pos)
            phon = phon_pos[0]
            pos = phon_pos[1]
            # print pos
            if pos == "B":
                start = line[9]
                #print("  pos-B   start = ", start)
                pron.append(phon)
            if pos == "S":
                start = line[9]
                end = line[10] 
                #print("  pos-S   start = ", start)
                #print("  pos-S   end = ", end)
                pron.append(phon)
                #print("  --write: " + seg_id + '\t' + ' '.join(pron) + '\t' + str(start) + '\t' + str(end))
                fout.write(seg_id + '\t' + ' '.join(pron) + '\t' + str(start) + '\t' + str(end))
                pron = []
            if pos == "E":
                end = line[10]
                #print("  pos-E   end = ", end)
                pron.append(phon)
                #print("  --write: " + seg_id + '\t' + ' '.join(pron) + '\t' + str(start) + '\t' + str(end))
                fout.write(seg_id + '\t' + ' '.join(pron) + '\t' + str(start) + '\t' + str(end))
                pron = []
            if pos == "I":
                pron.append(phon)
            #print("  pron = ", pron)
            jj += 1
        fout.close()
        ii += 1


if __name__ == "__main__":
    print("\n    Usage : " + sys.argv[0])
    print("\n")
    script_name = sys.argv[0]
    ali_dir = sys.argv[1]
    print("    script_name = ", script_name)
    print("    ali_dir = ", ali_dir)

    ## Specify the input directory
    # files = glob.glob('file_align/MMGCS200800160_MMGCS200800160.txt')
    try:
        #files = glob.glob(ali_dir+'/file_align/*MMGCS*.txt')
        files = glob.glob(ali_dir+'/file_align/*.txt')
        files.sort()
        # print("files = ", files)
    except:
        print("The directory file_align doesn't exist or file_align has no files.")
        sys.exit(2)

    ## Create the output directory, if it's already exist, then delete the directory.
    dir_name = ali_dir+'/pron_align'
    if not os.path.exists(dir_name):
        print("    create a new directory: ", dir_name)
        os.makedirs(dir_name)
    else:
        print("    delete a existing direcry: ", dir_name)
        shutil.rmtree(dir_name)
        print("    create a new directory: ", dir_name)
        os.makedirs(dir_name)

    ## Generate phone alignment
    generate_phone_alignment(files, dir_name)
