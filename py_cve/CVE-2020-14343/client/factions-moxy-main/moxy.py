import argparse
import re
import json
try:
    import yaml
except ImportError:
    from pip._internal import main as pip
    pip(["install", "--user", "pyyaml"])
from yaml import safe_load

def process(input_file, config_file):
    def textify(list_or_str):
        if type(list_or_str) == list or type(list_or_str) == tuple:
            return "\n".join(list_or_str)
        return list_or_str
    data = None
    with open(input_file, encoding="utf-8") as f:
        data = f.read()
    out = []
    with open(config_file, "r", encoding="utf-8") as config:
        conf = safe_load(config)
        if "motion" not in conf:
            raise Exception(f"The key 'motion' was not found in the configuration file {config_file}!")
        motion_rgx = re.compile(conf["motion"]["regex"], re.DOTALL)
        motions = re.findall(motion_rgx, data)
        groups = None
        try:
            groups = conf["motion"]["groups"]
        except:
            pass
        for motion in motions:
            obj = {}
            if groups:
                if "text" not in groups:
                    raise Exception("Required field 'text' is missing in 'groups'!")
                for k,v in zip(groups, motion):
                    obj[k] = v
            for key in conf["motion"]["keys"]:
                for regex in conf["motion"]["keys"][key]["regex"]:
                    rgx = re.compile(regex, re.DOTALL)   
                    text_ = obj["text"] if "text" in obj else textify(motion)     
                    match = re.search(rgx, text_)
                    if match is not None:
                        if key not in obj:
                            obj[key] = []
                        group = match.group()
                        obj[key].append(group.strip())
                out.append(obj)
    return out

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract motions from a text file and save as JSON.")
    parser.add_argument("input_file", help="Input text file name")
    parser.add_argument("output_file", help="Output JSON file name")
    parser.add_argument("config_file", help="Configuration file")
    args = parser.parse_args()
    result = process(args.input_file, args.config_file)
    with open(args.output_file, 'w', encoding='utf-8') as json_file:
        json.dump(result, json_file, ensure_ascii=False, indent=4)
