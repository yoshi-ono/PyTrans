import glob

path = '/Users/YOSHIKI/github/PyLIS'
exclude_dir = ['venv', 'hsr_meshes']

search = []

files = glob.glob(path + '/**/*.md', recursive=True)

expath = tuple([path + '/' + dir for dir in exclude_dir])

for file in files:
    if (not file.startswith(expath)):
        search.append(file)

print(search)
