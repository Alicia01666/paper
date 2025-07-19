#### PyReach: A Multi-Agent Framework for Vulnerability Reachability Analysis in Python Projects

##### Introduction of our work：

Modern Python applications heavily rely on third-party libraries (TPLs), which can introduce security risks when vulnerabilities in these libraries silently propagate into client code.
Determining whether a known vulnerability in a third-party library (TPL) can potentially be triggered in a specific downstream application is a key aspect of vulnerability reachability analysis, a research area that remains a manual, error-prone task due to the dynamic nature of the Python language and its implicit coding patterns.
We present PyReach, a multi-agent collaborative framework that automates vulnerability reachability analysis for Python programs. Instead of statically resolving all dynamic behavior, PyReach decomposes the reasoning process into three semantically guided agents: 1) Context Modeling Agent that extracts auxiliary semantic context by analyzing and summarizing the semantic context of external dependencies for each function in a call chain; 2) Reachability Analysis Agent that determines whether a function in a call chain alters a vulnerability's triggering conditions by analyzing its inside semantics; 3) Reachability Verification Agent that determines if execution paths from user-facing entry points can reach the vulnerable code under the right conditions.
We evaluate PyReach on a custom-built dataset, the largest of its kind for Python vulnerability reachability analysis, consisting of 15 real-world Python CVEs and 45 corresponding client projects. Experimental results show that PyReach achieves 90\% precision and 83.3\% specificity, significantly outperforming a call-graph-based baseline, Jarvis.
PyReach effectively distinguishes between truly affected and unaffected clients by reasoning over code semantics and trigger profiles. 
Our results highlight the value of combining modular semantic reasoning with constraint propagation for accurate and scalable vulnerability analysis in dynamic languages.

![overview]([https://anonymous.4open.science/r/paper-EB98/overview.png](https://github.com/Alicia01666/paper/blob/main/overview.png))

##### Usage：

```bash
# install all the libraries required for PyReach
pip install -r requirements.txt
# generate call chain
python3 src/call_chain_main.py repo_path vul_code_keys
# determine the reachability of the project
python3 src/analysis_main.py vul_conditions
```

