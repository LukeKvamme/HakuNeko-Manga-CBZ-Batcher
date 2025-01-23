import math
from zipfile import ZipFile, ZIP_DEFLATED
from tqdm import tqdm
from glob import glob
from pathlib import Path
import os, sys, shutil

def main(user_input_filepath):

##################################
# Set up directories and filepaths
##################################
    successful = False
    while True:
        manga_name = user_input_filepath

        if manga_name.lower() == 'q':
            print("Exiting...")
            return False

        try:
            os.chdir(os.path.expanduser('~') + "\\OneDrive\\Documents\\Mangas\\" + manga_name)
            print("\n+-----------------------------------------------------------------------------------------------------------------------------+")
            print(f"Current working directory:\t{os.getcwd()}")
            successful = True
        except FileNotFoundError:
            print(f"Manga directory not found in Documents folder: \"{manga_name}\", input a Manga that exists")
        except PermissionError:
            print(f"Permission denied: {manga_name}")
        except NotADirectoryError:
            print(f"Not a directory: {manga_name}")
        except Exception as e:
            print(f"An error occurred: {e}")
        if successful:
            break

    manga_dir_of_cbz_files = os.path.expanduser('~') + "\\OneDrive\\Documents\\Mangas\\"+ manga_name + '\\'
    batched_file_dir = manga_dir_of_cbz_files + 'batched-cbz-file'
    tmp_dir = manga_dir_of_cbz_files + 'temp'

    if os.path.exists(batched_file_dir):
        files = glob(batched_file_dir + '\\*')
        for file in files:
            os.remove(file)
    else:
        os.mkdir(batched_file_dir)

    if os.path.exists(tmp_dir):
        files = glob(tmp_dir + '\\*')
        for file in files:
            os.remove(file)
    else:
        os.mkdir(tmp_dir)

    

    manga_dir_of_cbz_files += '*.cbz'
    extenstion_list = ['.jpg', '.png', '.webp']
    cbz_list = glob(manga_dir_of_cbz_files)
    try:
        cbz_list.sort(key=lambda x: float(x.split('\\')[-1].split('.')[0].split(' ')[-1])) # natural sorts the list instead of lexicographic sorting
    except ValueError:
        print("#############################################################################################################################################################")
        print(f"{ValueError} popped up when trying to sort the .cbz files in {manga_name}. Was not caught due to obscure naming, please change the file name and try again.")
        print("#############################################################################################################################################################")
    cbz_list_length = len(cbz_list)
    chapters_per_batch = 30
    current_chapter_count = 0
    current_chapter = 0
    batched_file_output_count = math.ceil(len(cbz_list) / chapters_per_batch)

    for output_file_num in range(batched_file_output_count): # for # batched.cbz files

        #-----------------------------------------#
        # Clean tmp folder for next chapter batch #
        #-----------------------------------------#
        files = glob(tmp_dir + '\\*')
        for file in files:
            os.remove(file)
        tqdm_chapter_update_start = (output_file_num * chapters_per_batch) + 1
        if output_file_num+1 == batched_file_output_count:
            tqdm_chapter_update_end = tqdm_chapter_update_start + (cbz_list_length-tqdm_chapter_update_start)
            chapters_per_batch = cbz_list_length-(tqdm_chapter_update_start-1)
        else:
            tqdm_chapter_update_end = (output_file_num + 1) * chapters_per_batch

        #-------------------------------------------------------------------------#
        # Loop through files of current chapter batch, unzip them into tmp folder #
        #-------------------------------------------------------------------------#
        for cbz_index in tqdm(range(chapters_per_batch), desc= f"Unzipping Chapters {tqdm_chapter_update_start} to {tqdm_chapter_update_end}"): # for # chapters inside each batched.cbz file
            if current_chapter_count == cbz_list_length:
                break
            cbz_file = cbz_list[current_chapter_count] # cbz file is the file inside the index
            current_chapter = float(cbz_file.split('\\')[-1].split('.cbz')[0].split(' ')[-1])
            if current_chapter % 1 == 0:
                current_chapter = int(current_chapter)

            #---------------------------#
            # Unzip into the Tmp Folder #
            #---------------------------#
            with ZipFile(cbz_file, 'r') as zObject:
                zObject.extractall(path= batched_file_dir)
            unzipped_list = glob(batched_file_dir + '\\*')
            for image in unzipped_list:
                for extension in extenstion_list:
                    if extension in image:
                        try:
                            os.rename(image, tmp_dir +'\\' + f'chapter{current_chapter}_' + os.path.basename(image))
                        except FileExistsError:
                            print(f"Chapter {current_chapter} has an alternate version (FileExistsError in os.rename() function). May need to re-implement the alternate chapter version incrementor")
                        except Exception as e:
                            print(f"An error occurred: {e}")

            current_chapter_count += 1



        #---------------------------------#
        # Zip files inside Batched Folder #
        #---------------------------------#
        manga_zip = manga_name + '.zip'
        

        with ZipFile(manga_zip, 'w', ZIP_DEFLATED) as zipf:
            for file in tqdm(glob(f'{tmp_dir}\\*'), desc= f"Zipping Chapters {tqdm_chapter_update_start} to {tqdm_chapter_update_end}"):
                for extension in extenstion_list:
                    if extension in file:
                        zipf.write(file, os.path.basename(file))

        os.rename(manga_zip, f'{batched_file_dir}\\{manga_name}_Chap{tqdm_chapter_update_start}-{tqdm_chapter_update_end}.cbz')


    ####################
    # Delete Temp Folder
    ####################

    if os.path.exists(tmp_dir):
        files = glob(tmp_dir + '\\*')
        for file in files:
            os.remove(file)
        os.rmdir(tmp_dir)

    print(f"\n\n\t\t\t=====================>> {manga_name} .cbz batch file completed. <<=====================\n")


if __name__ == '__main__':
    main(sys.argv[1]) #argv[0] is the script name, argv[1] is the actual argument