import json

from src.util.fileutil import get_filename, find_file_path
from src.context.fetch_repo_functions import extract_functions_from_repo
from src.context.match_client_functions import find_direct_functions, get_function_lineno, get_call_line, \
    find_function_calls_in_file
from src.context.generate_function_call_graph import generate_call_graph
from src.entity import FunctionNode


def parse_call_graph(repo_name, package_path, module_path_list):
    chain_json_file = generate_call_graph(repo_name, package_path, module_path_list)

    with open(chain_json_file, 'r') as file:
        repo_call_graph = json.load(file)

    return repo_call_graph


# megatron.training.optimizer_param_scheduler.OptimizerParamScheduler.load_state_dict
def get_file_func_name(node, module_path_list):
    file_name = ''
    func_name = ''
    sep = node.split('.')
    dot_count = node.count('.')
    if dot_count == 0:
        return file_name, func_name
    if dot_count == 1:
        file_name: str = sep[0]
        func_name = sep[1]

        return file_name, func_name

    py_filenames = []
    for fp in module_path_list:
        py_filenames.append(get_filename(fp))

    intersection = set(py_filenames) & set(sep)
    if intersection:
        file_name = list(intersection)[0]
        func_name = sep[-1]

    return file_name, func_name


def find_chains(graph, start):

    direct_start = start.split('.')
    direct_file_name = direct_start[0]
    direct_function_name = direct_start[1]
    for parent, children in graph.items():
        for child in children:
            child_split = child.split('.')
            if direct_file_name in child_split and direct_function_name in child_split:
                start = child



    def dfs(node, path, chains, visited=None):
        if visited is None:
            visited = set()


        if node in visited:
            return
        visited.add(node)


        path.append(node)


        found_parent = False
        for parent, children in graph.items():
            if node in children:
                dfs(parent, path.copy(), chains, visited.copy())
                found_parent = True


        if not found_parent:
            chains.append(list(path))

    chains = []
    dfs(start, [], chains)

    return chains


def fill_call_info(vul_function, function_call_chain_list):
    function_call_chains = []


    for function_call_chain in function_call_chain_list:
        function_call_chain[0].add_focused_call(vul_function)

        for i in range(1, len(function_call_chain)):
            caller_node = function_call_chain[i]
            called_node = function_call_chain[i - 1]


            # call_line = get_call_line(caller_node.source_code, called_node.function_name)
            caller_node.add_focused_call(called_node.function_name)
    print("function_call_chain_list: ", function_call_chain_list)
    return function_call_chain_list


def build_function_call_chain(repo_name, package_path, module_path_list, vul_code_keys):
    direct_functions_dict = {}
    for py_path in module_path_list:
        direct_functions = find_direct_functions(py_path, vul_code_keys)
        if len(direct_functions) > 0:
            for function in direct_functions:
                direct_functions_dict[py_path] = function

    if len(direct_functions_dict) == 0:
        return []

    functions_dict = extract_functions_from_repo(package_path)
    repo_call_graph = parse_call_graph(repo_name, package_path, module_path_list)

    function_call_chain_list = []
    for direct_function_fp in direct_functions_dict:
        direct_func = direct_functions_dict[direct_function_fp]
        direct_func_key = get_filename(direct_function_fp) + "." + direct_func[0]
        # print("direct_func_key: ", direct_func_key)

        chains = find_chains(repo_call_graph, direct_func_key)

        for chain in chains:
            call_chain = []
            for node in chain:
                py_file_name, func_name = get_file_func_name(node, module_path_list)
                py_file_path = find_file_path(node, module_path_list, py_file_name + ".py", func_name)

                if not py_file_path or py_file_path == '':
                    continue

                func_line_no = get_function_lineno(py_file_path, func_name)
                func_node = FunctionNode(func_name, py_file_path, func_line_no)

                called_functions = find_function_calls_in_file(py_file_path, func_name)
                called_functions = list(set(called_functions))

                for called_function in called_functions:
                    if functions_dict.keys().__contains__(called_function):
                        func_node.add_extend_calls(functions_dict[called_function])

                call_chain.append(func_node)

            function_call_chain_list.append(call_chain)

    function_call_chain_list = fill_call_info(vul_code_keys[0], function_call_chain_list)

    return function_call_chain_list
