import glob
from translate_md import TranslateMd

path = '/Users/YOSHIKI/github/PyLIS'
exclude_dir = ['venv', 'hsr_meshes']

def main():
    search = []

    files = glob.glob(path + '/**/*.md', recursive=True)

    expath = tuple([path + '/' + dir for dir in exclude_dir])

    for file in files:
        if (not file.startswith(expath)):
            search.append(file)

    print(search)

    for file in search:
        transmd = TranslateMd(file)
        transmd.start()
        del transmd

if __name__ == "__main__":
    main()

