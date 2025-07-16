import ast


def get_call_line(source_code, called_function_name) -> str:
    if not source_code:
        # print("source code is null")
        return ""


    try:
        tree = ast.parse(source_code)
    except Exception as e:
        return ""


    for node in ast.walk(tree):

        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            if node.func.id == called_function_name:

                call_line_number = node.lineno

                lines = source_code.splitlines()
                if 0 <= call_line_number - 1 < len(lines):
                    return lines[call_line_number - 1].strip()
    return None



def get_function_lineno(file_path, function_name) -> int:

    with open(file_path, "r") as file:
        file_content = file.read()


    try:
        tree = ast.parse(file_content)
    except Exception as e:
        print(e)
        return -1


    for node in ast.walk(tree):

        if (isinstance(node, ast.FunctionDef) or isinstance(node, ast.AsyncFunctionDef)) \
                and node.name == function_name:

            return node.lineno

    return -1


def find_direct_functions(filepath, vul_code_keys: list) -> list:
    with open(filepath, 'r') as file:
        file_content = file.read()

    try:
        tree = ast.parse(file_content)
    except Exception as e:
        print(filepath)
        print(f"ast.parse Error: {e}")
        return []


    target_function_name = vul_code_keys[0]
    required_keys = vul_code_keys[1:]

    functions_with_string = []

    for node in ast.walk(tree):
        if (isinstance(node, ast.FunctionDef) or isinstance(node, ast.AsyncFunctionDef)) :

            function_body = ast.get_source_segment(file_content, node)


            match_keys = all(key in function_body for key in required_keys)


            match_function_call = False
            for body_node in ast.walk(node):
                if isinstance(body_node, ast.Call) and isinstance(body_node.func, ast.Attribute):

                    if body_node.func.attr == target_function_name:
                        match_function_call = True
                        break
                elif isinstance(body_node, ast.Call) and isinstance(body_node.func, ast.Name):

                    if body_node.func.id == target_function_name:
                        match_function_call = True
                        break


            if match_keys and match_function_call:
                functions_with_string.append((node.name, node.lineno))

    return functions_with_string


def find_function_calls_in_file(file_path, function_name):
    with open(file_path, 'r', encoding='utf-8') as file:
        file_content = file.read()


    tree = ast.parse(file_content, filename=file_path)


    called_functions = []


    for node in ast.walk(tree):
        if (isinstance(node, ast.FunctionDef) or isinstance(node, ast.AsyncFunctionDef)) and node.name == function_name:

            for sub_node in ast.walk(node):
                if isinstance(sub_node, ast.Call):

                    if isinstance(sub_node.func, ast.Name):
                        called_functions.append(sub_node.func.id)
                    elif isinstance(sub_node.func, ast.Attribute):

                        called_functions.append(sub_node.func.attr)
                    elif isinstance(sub_node.func, ast.Call):

                        called_functions.append("nested_call")
            break

    return called_functions



if __name__ == '__main__':
    file_path = '/PycharmProjects/PyVul/src/context/dataset/test_data/CVE-2019-7548/dices-master/dices/tools/game.py'
    #
    function_name  = 'get_state'
    index = get_function_lineno(file_path, function_name)
    print(index)

