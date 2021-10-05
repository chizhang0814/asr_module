
import sys,csv,os,shutil

def split_ali_file_to_files(final_ali_txt, ali_dir):

    ff = open(final_ali_txt, 'r')
    all_ali_list = ff.readlines()
    ff.close()
    print("    len(all_ali_list) = ", len(all_ali_list)) 
    all_ali_list = sorted(all_ali_list[1:])  ##remove header
    #print("  all_ali_list = \n", all_ali_list)
    name = all_ali_list[0].split()[1]
    print("   first file name = ", name)

    ''' 
    file_name_list = []
    for line in all_ali_list:
        file_name = line.split()[1]
        #print("file_name = ", file_name)
        file_name_list.append(file_name)
    unique_file_name_list = list(set(file_name_list))
    n_of_files = len(unique_file_name_list)
    print("    n_of_files = ", n_of_files)
    '''

    # name = name of first text file in final_ali.txt
    # name_fin = name of final text file in final_ali.txt
    # name = "MMGCS200700176_s_A_VWI_s_ABBIE_s_KENT_s_30_IRSF46_134;_s_17.12.19_24_07_2020_16_50_24_converted"
    # name = "MMGCS200800160_MMGCS200800160"
    # name_fin = "F_25_172602_inLine_99i"

    ## Create the output directory, if it's already exist, then delete the directory.
    dir_name = ali_dir+'/file_align'
    if not os.path.exists(dir_name):
        print("    create a new directory: ", dir_name)
        os.makedirs(dir_name)
    else:
        print("    delete a existing direcry: ", dir_name)
        shutil.rmtree(dir_name)
        print("    create a new directory: ", dir_name)
        os.makedirs(dir_name)

    ## Generate alignment files in the directory
    results = []
    ii = 1
    try:
        '''
        with open(final_ali_txt) as f:
            next(f)  # skip header
            # jj = 1
            for line in f:
                # print("   jj = ", jj)
                columns = line.split("\t")
                name_prev = name
                name = columns[1]
                if (name_prev != name):
                    try:
                        with open(dir_name + '/' + str(ii) + '_' + (name_prev) + ".txt", 'w') as fwrite:
                            print("-----------ii = ", ii, "   ", name_prev)
                            ii += 1
                            writer = csv.writer(fwrite)
                            fwrite.write("\n".join(results))
                            fwrite.write("\n")
                            fwrite.close()
                            # print("    The ", ii, " file write is done.!")
                    # print name
                    except Exception as e:
                        print("Failed to write file", e)
                        sys.exit(2)
                    del results[:]
                    results.append(line[0:-1])
                    # jj = jj+1
                else:
                    results.append(line[0:-1])
                    # jj = jj+1
        '''
        for line in all_ali_list:
            columns = line.split("\t")
            name_prev = name
            name = columns[1]
            if (name_prev != name):
                try:
                    ## sort according to the second last column
                    #print("  results = ", results)
                    results= sorted(results, key=lambda k: float(k.split('\t')[-2]))
                    with open(dir_name + '/' + (name_prev) + ".txt", 'w') as fwrite:
                        print("-----------ii = ", ii, "   ", name_prev)
                        ii += 1
                        writer = csv.writer(fwrite)
                        fwrite.write("\n".join(results))
                        fwrite.write("\n")
                        fwrite.close()
                        #print("    The ", ii, " file write is done.!")
                except Exception as e:
                    print("Failed to write file", e)
                    sys.exit(2)
                del results[:]
                results.append(line[0:-1])
		# jj = jj+1
            else:
                results.append(line[0:-1])
		# jj = jj+1
    except Exception as e:
        print("Failed to read file",e)
        sys.exit(1)
    

    # this prints out the last textfile (nothing following it to compare with)
    try:
        ## sort according to the second last column
        results= sorted(results, key=lambda k: float(k.split('\t')[-2]))
        with open(dir_name + '/' + (name_prev) + ".txt",'w') as fwrite:
            print("-----------ii = ", ii, "   ", name_prev)
            ii += 1
            writer = csv.writer(fwrite)
            fwrite.write("\n".join(results))
            fwrite.write("\n")
            fwrite.close()
            #print("    The ", ii, " file write is done.!")
    except Exception as e:
        print("Failed to write file",e)
        sys.exit(2)


if __name__ == "__main__":
    if (len(sys.argv) != 3):
        print("\n    Usage : " + sys.argv[0] + " final_ali.txt (the alignment file)  <ali_dir>\n")
        sys.exit(0)
    script_name = sys.argv[0]
    final_ali_txt = sys.argv[1]
    ali_dir = sys.argv[2]
    print("\n")
    print("    script_name = ", script_name)
    print("    final_ali_txt = ", final_ali_txt)
    split_ali_file_to_files(final_ali_txt, ali_dir)
