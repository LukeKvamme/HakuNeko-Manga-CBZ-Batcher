from glob import glob
from pathlib import Path
import os

# manga_dir_of_cbz_files = os.path.expanduser('~') + "\\OneDrive\\Documents\\Mangas\\"+ input("Input Manga Name:  ") + '\\'
# manga_dir_of_cbz_files += '*.cbz'
# cbz_list = glob(manga_dir_of_cbz_files)
# cbz_list.sort(key=lambda x: int(x.split('\\')[-1].split('.')[0].split(' ')[-1]))

p = "C:\\Users\\lukek\\OneDrive\\Documents\\Mangas\\+99 Reinforced Wooden Stick\\Chapter 55.cbz"
print(os.path.basename(p)[:-4])

