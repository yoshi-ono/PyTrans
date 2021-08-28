import glob
import re
from translate_md import TranslateMd

path = '/Users/yoshiki/GitHub/PyLIS.wiki'
#path = '/Users/yoshiki/GitHub/PyTrans'
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

    for file in search:
        transmd = TranslateMd(file)

        if (transmd.translated()):
            print(file, "translated!")
        else:
            transmd.start()
        
        del transmd

if __name__ == "__main__":
    main()

