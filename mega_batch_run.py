import manga_batcherv2, os, re
from pathlib import Path
from tqdm import tqdm
from glob import glob

def verify():
    manga_list = []
    path = Path(os.path.expanduser('~') + "\\OneDrive\\Documents\\Mangas")
    for manga_name in path.iterdir():
        if manga_name.is_dir():
            manga_list.append(os.path.basename(manga_name))

    for manga in tqdm(manga_list, desc= "Checking .cbz file names to make sure they are correctly labelled. "):
        manga_path = os.path.expanduser('~') + '\\OneDrive\\Documents\\Mangas\\' + manga + '\\'
        cbz_files = glob(manga_path + '*.cbz')
        duplicate_naming_incementor = 1

        for chapter_file in cbz_files:
            chapter_rename = ""
            chapter_name = os.path.basename(chapter_file)[:-4].split(" ")
            if len(chapter_name) == 2:
                continue
            else:
                for i in range(len(chapter_name)-1):
                    if chapter_name[i].lower() == "chapter":
                        chapter_rename = chapter_name[i] + " " + chapter_name[i+1]
                
                try:
                    os.rename(chapter_file, f"{manga_path}{chapter_rename}.cbz")
                except FileExistsError:
                    print(f"Duplicate file name: {os.path.basename(chapter_file)} and {chapter_rename}. Adding decimal to chapter number.")
                    os.rename(chapter_file, f"{manga_path}{chapter_rename}.{duplicate_naming_incementor}.cbz")
                    duplicate_naming_incementor += 1
                #print(f"Old Name: {chapter_file}\nNew Name: {new_name}\n") # for testing purposes
        print(f"{manga} checked.")

    print("\n\t\t+~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+")
    print("\t\t  File naming verified and complete! Now beginning main batching procedure")
    print("\t\t+~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+")

def run():
    manga_list = []
    path = Path(os.path.expanduser('~') + "\\OneDrive\\Documents\\Mangas")
    for manga_name in path.iterdir():
        if manga_name.is_dir():
            manga_list.append(os.path.basename(manga_name))
    
    print("\n+-----------------------------------------------------------------------------------------------------------------------------+\n")
    for manga in tqdm(manga_list, desc= ">> Running through all Manga in Documents\Manga folder"):
        manga_batcherv2.main(manga)

if __name__ == '__main__':
    verify()
    run()