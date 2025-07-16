import os
import time
import subprocess
from src.util.fileutil import get_all_py_files


def generate(module_path, package_path, output_json_file):
    command = [
        "python3",
        "context/callgraph/pythonJaRvis.github.io-master/Jarvis/tool/Jarvis/jarvis_cli.py",
        *module_path,
        "--package",
        package_path,
        # "--decy",
        "-o",
        output_json_file
    ]

    result = subprocess.run(command, capture_output=True, text=True)

    # 检查执行结果
    if result.returncode == 0:
        print("call graph执行成功")
    else:
        print("call graph执行失败")
        print("error:", result.stderr)


def generate_call_graph(repo_name, package_path, module_path_list):
    timestamp = time.time()
    output_json_file = repo_name + "_call_graph_" + str(timestamp) + "_result.json"

    generate(module_path_list, package_path, output_json_file)

    return output_json_file
