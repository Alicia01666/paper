import json
import os

from context.parse_function_node import build_function_call_chain
from util.fileutil import get_all_py_files


def save_to_json(data, filename):

    serialized_data = [[node.to_dict() for node in inner_list] for inner_list in data]
    with open(filename, 'w') as f:
        json.dump(serialized_data, f, indent=4)


if __name__ == '__main__':
    repo_name = "superSTR-main"
    package_path = os.path.join(os.getcwd(), 'context/dataset/test_data/CVE-2021-29063', repo_name)
    print(package_path)
    module_path_list = get_all_py_files(package_path)
    print("len(module_path_list): ", len(module_path_list))


    vul_code_keys = ['mpmathify']

    chain_list = build_function_call_chain(repo_name,
                                           package_path,
                                           module_path_list,
                                           vul_code_keys)

    print("len(chain_list): ", len(chain_list))

    filename = repo_name + '_call_chain.json'
    save_to_json(chain_list, filename)
