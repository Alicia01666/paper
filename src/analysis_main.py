import json

from entity import FunctionNode
from analysis_agents import analyse_function_node


def load_from_json():
    repo = 'superSTR-main_call_chain.json'

    with open(repo, 'r') as f:
        serialized_data = json.load(f)
    return [[FunctionNode.from_dict(node) for node in inner_list] for inner_list in serialized_data]


def analysis(chain_list, vul_trigger_condition):
    chain_index = 0
    for chain in chain_list:
        report_lines = []
        chain_index = chain_index + 1
        direct_func_node = chain[0]
        param_conditions = analyse_function_node(direct_func_node, vul_trigger_condition)
        report_lines.append(param_conditions + '\n\n')
        report_lines.append(direct_func_node.function_name + '_function_end_' * 10)
        direct_func_node.add_parameter_condition(param_conditions)

        for i in range(1, len(chain)):
            func_node = chain[i]
            called_func_node = chain[i - 1]
            param_conditions = analyse_function_node(func_node, called_func_node.parameter_conditions)
            report_lines.append(param_conditions + '\n\n')
            report_lines.append(func_node.function_name + '_function_end_' * 10)
            func_node.add_parameter_condition(param_conditions)

        with open('chain_index__' + str(chain_index) + '_analysis_output.txt', 'w', encoding='utf-8') as file:
            for line in report_lines:
                file.write(line)
        print(str(chain_index) + '/' + str(len(chain_list)) + ' done.')


if __name__ == '__main__':
    chain_list = load_from_json()

    vul_trigger_condition = """
    """

    analysis(chain_list, vul_trigger_condition)
