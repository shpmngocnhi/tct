import tarfile
import re
from glob import glob
import os

def convert_qkview_to_conf(qkview_file):
    folder_path = qkview_file.replace('.qkview', '').replace('qkview/', '')
    print(folder_path)
    os.makedirs(folder_path, exist_ok=True)

    path = f'{folder_path}.conf'
    with open(path, 'w', encoding='utf-8') as f:
        f.write('')

    with tarfile.open(qkview_file, "r:*") as tar:
        for member in tar.getmembers():
            if re.search(r'bigip\.conf$', member.name):
                f = tar.extractfile(member)
                if f:
                    config_data = f.read().decode('utf-8')
                    with open(path, encoding='utf-8') as f:
                        data_conf = f.read()

                        if config_data not in data_conf:
                            with open(path, 'a', encoding='utf-8') as f:
                                f.write(config_data)

    return path

if __name__ == "__main__":
    qkview_paths = glob('qkview/*.qkview')
    for qkview_file in qkview_paths:
        print(f'Extracting {qkview_file}')
        convert_qkview_to_conf(qkview_file)

