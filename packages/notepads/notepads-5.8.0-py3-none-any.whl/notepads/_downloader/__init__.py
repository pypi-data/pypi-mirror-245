import pathlib
import zipfile

def download(module):
    abs = str(pathlib.Path(__file__).parent.absolute()).replace('/_downloader', '')
    path_translate = {
        'color': [f'{abs}/modules/color.zip', f'{abs}/color']
    }
    path = path_translate.get(module)

    if path:
        with zipfile.ZipFile(path[0], 'r') as zipf:
            zipf.extractall(path[1])