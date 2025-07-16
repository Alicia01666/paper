#### PyReach: Automated Vulnerability Reachability Analysis Framework for Python Programs

PyReach is a multi-agent collaborative framework that automates vulnerability reachability analysis for Python programs, addressing the security risks introduced by third-party library (TPL) dependencies. 

![overview](D:\codes\final\paper_to_submit\myrepo\overview.png)

```bash
# install all the libraries required for PyReach
pip install -r requirements.txt
# generate call chain
python3 src/call_chain_main.py repo_path vul_code_keys
# determine the reachability of the project
python3 src/analysis_main.py vul_conditions
```

