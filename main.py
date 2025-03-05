from convert_qkview_to_conf import convert_qkview_to_conf
from f5_conf_to_csv import convert_f5_conf_to_csv
from irule import run_extract_irules
from glob import glob



if __name__ == "__main__":
    qkview_paths = glob('qkview/*.qkview')
    for qkview_file in qkview_paths:
        print(f'Extracting {qkview_file}')
        path_conf = convert_qkview_to_conf(qkview_file)
        convert_f5_conf_to_csv(path_conf)
        run_extract_irules(path_conf)

