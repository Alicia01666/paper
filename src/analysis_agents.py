import json
import os
from openai import OpenAI
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

from src.entity import FunctionNode

llm_model = ChatOpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    # model="deepseek-r1-distill-llama-70b"
    # model="qwen-plus"
    model="deepseek-r1",
    # model="llama3.3-70B",
)

system_role = """
    You are a python expert. 
"""

# Based on the provided context information, you are required to complete the following code analysis task.
# Use a Chain-of-Thought approach to break down the problem step by step and provide a clear conclusion.


def build_prompt_param_analysis(function_code, specific_code_lines):
    prompt_template = """
    Conduct a strict analysis of the following Python function code and extract parameter propagation paths and control flow information:
    
    Function Source Code:
    {function_code}
    
    Relevant Code Lines (Vulnerability-Related Calls):
    {specific_code_lines}
    
    Analysis Rules:
    
    1.Parameter Propagation Paths:
        - Describe the path of each parameter from entry to the vulnerability function, formatted as parameter_name -> processing_function/operation -> ... -> vulnerability_function.
        - If the parameter is passed directly without processing, simplify the path to parameter_name -> vulnerability_function.
    2.Control Flow Analysis:
        - List all conditional branches that may prevent parameters from reaching the vulnerability function (e.g., if len(data) < 16).
        - List all loops that may affect the value of parameters (e.g., for i in range(n): data += input[i]).
    3.Dynamic Feature Identification:
        - Identify high-risk operations such as eval, exec, __import__, getattr, and extract the code snippets.
    
    Please strictly output the analysis results in the given JSON structure, with no additional output.
    {{
      "parameters": {{
        "parameter_name": {{
          "propagation_path": ["propagation_path"]
        }}
      }},
      "control_flow": {{
        "branches": ["conditional_branches"],
        "loops": ["loops"]
      }},
      "dynamic_features": ["dynamic_feature_code_snippets"]
    }}
    """

    template = PromptTemplate(
        input_variables=["system_role", "function_code", "specific_code_lines"],
        template=prompt_template
    )

    final_prompt = template.format(
        system_role=system_role,
        function_code=function_code,
        specific_code_lines=specific_code_lines
    )

    return final_prompt


def build_prompt_extend_function(extend_function):
    prompt_template = """
    As a senior code analyst, please conduct a comprehensive analysis of the following Python function.
    
    # Analysis Requirements
    Feature description should differentiate between core functionality and secondary functionality.
    
    # Target Function
    {extend_function}
    
    Please strictly output the analysis results in the given JSON structure, with no additional output.
    ```json
    {{
      "function_name": "function name",
      "description": {{
        "overview": "Core function description (1-2 sentences)"
      }},
    }}
    ```
    """

    template = PromptTemplate(
        input_variables=["extend_function"],
        template=prompt_template
    )

    final_prompt = template.format(
        extend_function=extend_function
    )

    return final_prompt


def build_prompt_path_analysis(function_code, specific_code_lines, trigger_condition,
                               step1_output, extend_context):
    prompt_template = """
    Conduct a strict vulnerability trigger condition analysis based on the following information. 
    Pay special attention to the **extended context** provided, as it contains semantic functions (e.g., the `pad` function) that may alter the conditions for triggering the vulnerability. 
    Ensure that the semantic functions in the extended context are fully considered in the parameter analysis and vulnerability assessment.

    Function Source Code:
    {function_code}  
    
    Conditions the Parameter Must Meet at the Specified Code Line:
    {specific_code_lines}  
    
    Trigger Condition:
    {trigger_condition}
    
    Step1 Output (Parameter Propagation Paths and Control Flow):
    {step1_output}  
    
    Extended Context:
    {extend_context}  
    
    Analysis Rules:
    1. Parameter Analysis:
       - For each parameter, determine whether operations in its propagation path (e.g., filtering, transformation) could lead to the parameter value meeting the vulnerability trigger conditions.  
       - If the parameter is modified, state whether the modified value could meet the vulnerability conditions.  
       - If the parameter is not modified, state whether the original input could meet the vulnerability conditions.  
    2. Control Flow Impact: 
       - Could conditional branches block the parameter from reaching the vulnerability function?  
    3. Output Requirements: 
       - The `conditions` field for each parameter should directly state whether the parameter could meet the vulnerability trigger conditions, rather than describing general constraints on the parameter.  
       - Example:  
         ```json
         "data": {{
           "conditions": ["Likely meets: Parameter is not padded, original length could be <16"]
         }}
         ```  
    4. If a function（excluding the main function entry point）has no input parameters, or if every function_parameter's evaluation condition is 'no', then the overall is_affected judgment should be 'false'.
    5. If the data comes from network requests, databases, or other data sources that are not controllable by the user, then the overall is_affected judgment should be 'false'.

    **Instruction**
    1. Understand the vulnerability reachability analysis task and its objectives
    2. Analyze the given function source code and intermediate analysis results (Parameter Propagation Paths and Control Flow)
    3. Identify suspicious parameters by tracing their data sources (user input/database/configuration files/API responses, etc.) according to the analysis rules
    4. Generate final analysis results by combining the analysis rules with contextual information
    

    Please strictly output the analysis results in the given JSON structure, with no additional output.
    ```json
    {{
      "parameters": {{
        // Automatically generate a field for each parameter of the function
            "function_parameter_name_1": {{
                "conditions": ["Whether the parameter could meet the vulnerability trigger conditions (Yes/No) and reasons"]
            }},
            "function_parameter_name_2": {{
                "conditions": ["Whether the parameter could meet the vulnerability trigger conditions (Yes/No) and reasons"]
            }},
            // Add more fields as needed based on the function's parameters
      }},
      "is_affected": "Overall whether the vulnerability is exploitable (true/false)"
    }}
    ```
    """

    template = PromptTemplate(
        input_variables=["system_role", "function_code", "specific_code_lines",
                         "trigger_condition",  "step1_output",
                         "extend_context"],
        template=prompt_template
    )

    final_prompt = template.format(
        system_role=system_role,
        function_code=function_code,
        specific_code_lines=specific_code_lines,
        trigger_condition=trigger_condition,
        step1_output=step1_output,
        extend_context=extend_context
    )

    return final_prompt


def get_ext_func_summaries(function_node):
    ext_func_summaries = []
    for ext_func in function_node.extend_calls:
        ext_func_prompt = build_prompt_extend_function(ext_func)
        ext_func_summary = llm_model.invoke(ext_func_prompt).content
        ext_func_summaries.append(ext_func_summary)

    extend_context = "\n".join(ext_func_summaries)

    return extend_context


# ast
def analyse_function_node(function_node: FunctionNode, trigger_condition):
    function_code = function_node.source_code
    specific_code_lines = function_node.focused_calls
    specific_conditions = function_node.conditions_for_focused_calls

    param_analysis_prompt = build_prompt_param_analysis(function_code, specific_code_lines)
    param_analysis_result = llm_model.invoke(param_analysis_prompt).content
    extend_context = get_ext_func_summaries(function_node)

    path_analysis_prompt = build_prompt_path_analysis(function_code, specific_code_lines, trigger_condition,
                                                      param_analysis_result, extend_context)

    path_analysis_result = llm_model.invoke(path_analysis_prompt).content

    return path_analysis_result
