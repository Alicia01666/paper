import os
import json
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

from src.analysis_main import load_from_json
from src.entity import FunctionNode

llm_model = ChatOpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    model="deepseek-r1",
    # model="qwen-plus"
    # model="deepseek-r1-distill-llama-70b"
)


system_role = """
    You are a python testing expert. 
"""


def build_prompt(function_code, analysis_result):
    prompt_template = """
    Given the source code of a function and the conditions that need to be met for the parameter,
    generate the corresponding unit test for the function. 
    
    The purpose is to construct inputs and function calls that can trigger the vulnerability. 
    
    Function Code:
    {function_code}
    
    Analysis Result:
    {analysis_result}
    
    Please provide test code that satisfies vulnerability impact verification. 
    Note that complete tests should be provided, and mocks should not be used.
    """

    template = PromptTemplate(
        input_variables=["system_role", "function_code", "analysis_result"],
        template=prompt_template
    )

    final_prompt = template.format(
        system_role=system_role,
        function_code=function_code,
        analysis_result=analysis_result
    )

    return final_prompt


def generate_test_for_reachable_verify(entry_source_code, analysis_result):
    question = build_prompt(entry_source_code, analysis_result)

    result = llm_model.invoke(question)

    return result.content


def read_analysis_output(file_path):
    decoder = json.JSONDecoder()
    with open(file_path, 'r', encoding='utf-8') as file:
        data = file.read()

    json_objects = []
    idx = 0
    while idx < len(data):
        try:
            obj, idx = decoder.raw_decode(data, idx)
            json_objects.append(obj)
        except json.JSONDecodeError:
            idx += 1

    return json_objects


def read_output_file_paths():
    current_dir = os.getcwd()
    output_files = []
    for root, dirs, files in os.walk(current_dir):
        for file in files:
            if file.endswith('_analysis_output.txt'):
                file_path = os.path.join(root, file)
                output_files.append(file_path)

    return output_files


if __name__ == '__main__':
    output_files = read_output_file_paths()
    test_index = 0
    for file_path in output_files:
        test_index = test_index + 1
        json_data = read_analysis_output(file_path)
        json_string = json.dumps(json_data)
        chain_list = load_from_json()
        print("processing test... ", str(test_index), file_path)

        entry_node: FunctionNode = chain_list[0][0]
        entry_source_code = entry_node.source_code
        print(entry_source_code)

        tests = generate_test_for_reachable_verify(entry_source_code, json_string)
        print(tests)
        with open('chain_index__' + str(test_index) + '_tests_output.txt', 'w', encoding='utf-8') as file:
            file.writelines(tests)

        # for obj in json_data:
        #     print(f"is_affected: {obj['is_affected']}")
        #     for param, details in obj['parameters'].items():
        #         print(f"Parameter: {param}")
        #         for condition in details['conditions']:
        #             print(f"  - {condition}")

        #
