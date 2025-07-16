import os
import ast


def extract_functions_from_file(file_path):
    functions = {}
    try:
        with open(file_path, 'r') as file:
            file_content = file.read()
        tree = ast.parse(file_content, filename=file_path)
        for node in ast.walk(tree):
            if (isinstance(node, ast.FunctionDef) or isinstance(node, ast.AsyncFunctionDef)) :
                functions[node.name] = ast.get_source_segment(file_content, node)
        return functions
    except Exception as e:
        return functions

def extract_functions_from_repo(repo_path):
    all_functions = {}
    for root, dirs, files in os.walk(repo_path):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                functions = extract_functions_from_file(file_path)
                all_functions.update(functions)
    return all_functions
