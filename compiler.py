from pathlib import Path
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
    with open(name, 'r') as f:
        json_ = f.read()
    if not json_:
        return {}
    try:
        return json.loads(json_)
    except:
        return {}


identifier_pattern = re.compile(r"<!--{[A-Za-z0-9-\s\/\.\$\#\[\]]+}-->")


def get_command(match):
    return match.group()[5:-4].strip()


def filter_path(file_path):
    if file_path.endswith('.md'):
        file_path = file_path[:-3]
    elif file_path.endswith('.json'):
        file_path = file_path[:-5]
    return file_path


class SyntaxCheckError(Exception):

    def __init__(self, file_path, line, command, message):
        file_path = filter_path(file_path)
        self.message = f"[from \"{file_path}.md\" line:{line} command:{command}] " + message

    def __str__(self):
        return repr(self.message)


def syntax_check(file_path, root):
    file_path = filter_path(file_path)
    markdown = load_markdown(file_path)
    variable = load_variable(file_path)
    match_list = [*re.finditer(identifier_pattern, markdown)]
    match_line = []
    for match in match_list:
        start_pos, end_pos = match.span()
        line_number = markdown[:start_pos].count('\n') + 1
        match_line.append(line_number)
    end_stk = []
    for i, match in enumerate(match_list):
        command = get_command(match)
        if command.startswith("v-"):
            variable_key = command[2:]
            if variable_key not in variable:
                raise SyntaxCheckError(file_path, match_line[i], command, f"variable \"{variable_key}\" is not defined")
        elif command.startswith("import-"):
            relative_path = filter_path(command[7:])
            _root = root
            if not relative_path.startswith("$root/"):
                _root = str(Path(file_path).parent)
            else:
                relative_path = relative_path[6:]
            import_path = _root + "/" + relative_path
            if ".." in import_path:
                raise SyntaxCheckError(file_path, match_line[i], command, f"does not support \"..\" in import path")
            if import_path == file_path:
                raise SyntaxCheckError(file_path, match_line[i], command, f"cannot import self file")
            if not os.path.exists(import_path + ".md"):
                raise SyntaxCheckError(file_path, match_line[i], command, f"file \"{relative_path}.md\" does not exist")
            if not os.path.exists(import_path + ".json"):
                raise SyntaxCheckError(file_path, match_line[i], command,
                                       f"file \"{relative_path}.json\" does not exist")
            try:
                syntax_check(import_path, root)
            except RecursionError:
                raise SyntaxCheckError(file_path, match_line[i], command,
                                       "maximum recursion depth exceeded")
        elif command.startswith("if-"):
            variable_key = command[3:]
            if variable_key not in variable:
                raise SyntaxCheckError(file_path, match_line[i], command, f"if-variable \"{variable_key}\" is not defined")
            end_stk.append(match)
        elif command.startswith("for-"):
            variable_key = command[4:]
            if variable_key not in variable:
                raise SyntaxCheckError(file_path, match_line[i], command, f"for-variable \"{variable_key}\" is not defined")
            if not isinstance(variable[variable_key], list):
                raise SyntaxCheckError(file_path, match_line[i], command, f"for-variable \"{variable_key}\" must be a list")
            end_stk.append(match)
        elif command.startswith("end"):
            if len(end_stk) == 0:
                raise SyntaxCheckError(file_path, match_line[i], command,
                                       "\"end\" does not match \"if\" or \"for\"")
            if len(end_stk) > 0:
                end_stk.pop(-1)

    if len(end_stk) != 0:
        cnt = len(end_stk)
        while cnt:
            if get_command(match_list[i]).startswith("if-"):
                cnt -= 1
                break
            elif get_command(match_list[i]).startswith("for-"):
                cnt -= 1
                break
            i -= 1
        command = get_command(match_list[i])
        if command.startswith("if-"):
            raise SyntaxCheckError(file_path, match_line[i], command,
                                   "\"if\" does not match \"end\"")
        if command.startswith("for-"):
            raise SyntaxCheckError(file_path, match_line[i], command,
                                   "\"for\" does not match \"end\"")


def compile_file(file_path, is_need_syntax=True):
    root = str(Path(file_path).parent)
    if is_need_syntax:
        try:
            syntax_check(file_path, root)
        except SyntaxCheckError as e:
            print(e.message)


if __name__ == "__main__":
    compile_file("./test/main.json")
