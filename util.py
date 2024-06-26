import re
import json
import os


def load_markdown(name):
    if not name.endswith('.md'):
        name += '.md'
    with open(name, 'r') as f:
        markdown = f.read()
    return markdown


def load_variable(name):
    if not name.endswith('.json'):
        name += '.json'
    if not os.path.exists(name):
        return {}
    with open(name, 'r') as f:
        json_ = f.read()
    if not json_:
        return {}
    return json.loads(json_)


identifier_pattern = re.compile(r"<!--{.*?}-->")
for_variable_pattern = re.compile(r"<!--{{.*?}}-->")


def get_command(match):
    return match.group()[5:-4].strip()


def get_command_value(command):
    return command.split("-")[-1].strip()


def filter_path(file_path):
    if file_path.endswith('.md'):
        file_path = file_path[:-3]
    elif file_path.endswith('.json'):
        file_path = file_path[:-5]
    return file_path


def log(text):
    print('\033[31m' + text + '\033[0m')
