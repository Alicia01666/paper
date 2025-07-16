import os


def get_filename(filepath: str):
    filename_without_extension = os.path.splitext(os.path.basename(filepath))[0]

    return filename_without_extension


def find_best_match(target, paths):
    # 提取模块路径（去掉方法名部分）
    module_parts = target.rsplit('.', 1)[0].split('.')  # ['tools', 'game']

    best_path = None
    best_score = -1

    for path in paths:
        path_parts = path.lstrip('.').split('.')
        module_index = len(module_parts) - 1
        path_index = len(path_parts) - 1
        score = 0

        while module_index >= 0 and path_index >= 0:
            if module_parts[module_index] == path_parts[path_index]:
                score += 1
                module_index -= 1
            path_index -= 1

        # 完全匹配 module_parts 的分数更高
        if score > best_score or (score == best_score and path.endswith('.py')):
            best_score = score
            best_path = path

    return best_path


def filter_by_function_definition(target_file_paths, func_name):
    path_list = []
    for path in target_file_paths:
        contains_func = False
        with open(path, "r") as file:
            lines = file.readlines()
            for line in lines:
                if line.__contains__('def') and line.__contains__(func_name):
                    contains_func = True
        if contains_func:
            path_list.append(path)

    return path_list


def find_file_path(node, file_paths, target_file, func_name):
    """
    从文件路径列表中匹配出指定文件的路径。

    :param file_paths: 文件路径列表，例如 ["/path/to/file1.txt", "/path/to/file2.txt"]
    :param target_file: 目标文件名，例如 "file1.txt"
    :return: 匹配到的文件路径，如果未找到则返回 None
    """
    target_file_paths = []
    for file_path in file_paths:
        # 获取路径中的文件名
        file_name = os.path.basename(file_path)
        if file_name == target_file:
            target_file_paths.append(file_path)

    target_file_paths = filter_by_function_definition(target_file_paths, func_name)
    if len(target_file_paths) == 0:
        return None

    final_path = find_best_match(node, target_file_paths)

    return final_path


def get_all_py_files(directory):
    """获取指定目录下所有的Python文件路径"""
    py_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                full_path = os.path.join(root, file)
                py_files.append(full_path)
    return py_files
