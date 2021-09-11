import glob
import re
import time
from translate_ipynb import TranslateIpynb

path = '/Users/yoshiki/GitHub/PyTrans'
exclude_names = ['test']

def main():
    search = []

    files = glob.glob(path + '/**/*.ipynb', recursive=True)

    expath = tuple([path + '/' + name for name in exclude_names])

    for file in files:
        if (not file.startswith(expath)
        and None == re.search(r'-translated-[a-z][a-z].ipynb$', file)):
            search.append(file)

    print("")
    print(search)

    count = 0
    for file in search:
        transmd = TranslateIpynb(file, count)
        count += 1
        transmd.start()
        time.sleep(1)

if __name__ == "__main__":
    main()

