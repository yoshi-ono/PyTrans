import glob
import re
import time
from translate_md import TranslateMd

path = '/Users/yoshiki/GitHub/WM_Hackathon.wiki'
exclude_dir = ['venv', 'hsr_meshes']

def main():
    search = []

    files = glob.glob(path + '/**/*.md', recursive=True)

    expath = tuple([path + '/' + dir for dir in exclude_dir])

    for file in files:
        if (not file.startswith(expath)
        and None == re.search(r'-translated-[a-z][a-z].md$', file)):
            search.append(file)

    print("")
    print(search)

    count = 0
    for file in search:
        transmd = TranslateMd(file, count)
        count += 1
        transmd.start()
        time.sleep(1)

if __name__ == "__main__":
    main()

