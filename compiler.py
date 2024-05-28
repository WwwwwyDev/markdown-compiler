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
        file_path = os.path.realpath(filter_path(file_path))
        self.message = f"[SyntaxCheckError] \nposition: from \"{file_path}.md\" line:{line} command:{command} \nmsg: " + message

    def __str__(self):
        return repr(self.message)


def syntax_check(markdown, variable, root, file_path):
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
                raise SyntaxCheckError(file_path, match_line[i], command,
                                       f"variable \"{variable_key}\" is not defined in json")
        elif command.startswith("import-"):
            relative_path = filter_path(command[7:])
            _root = root
            if not relative_path.startswith("$root/"):
                _root = str(Path(file_path).parent)
            else:
                relative_path = relative_path[6:]
            if relative_path.startswith("/"):
                import_path = relative_path
            else:
                import_path = _root + "/" + relative_path
            if import_path == file_path:
                raise SyntaxCheckError(file_path, match_line[i], command, f"cannot import self file")
            if not os.path.exists(import_path + ".md"):
                raise SyntaxCheckError(file_path, match_line[i], command,
                                       f"file \"{os.path.realpath(import_path)}.md\" does not exist")
            if not os.path.exists(import_path + ".json"):
                raise SyntaxCheckError(file_path, match_line[i], command,
                                       f"file \"{relative_path}.json\" does not exist")
            if import_path.count("../") >= 15:
                raise SyntaxCheckError(file_path, match_line[i], command,
                                       "maximum recursion depth exceeded")
            try:
                _markdown = load_markdown(import_path)
                _variable = load_variable(import_path)
                syntax_check(_markdown, _variable, root, import_path)
            except RecursionError:
                raise SyntaxCheckError(file_path, match_line[i], command,
                                       "maximum recursion depth exceeded")
        elif command.startswith("if-"):
            variable_key = command[3:]
            if variable_key not in variable:
                raise SyntaxCheckError(file_path, match_line[i], command,
                                       f"if-variable \"{variable_key}\" is not defined in json")
            end_stk.append({"command": command, "i": i})
        elif command.startswith("for-"):
            variable_key = command[4:]
            if variable_key not in variable:
                raise SyntaxCheckError(file_path, match_line[i], command,
                                       f"for-variable \"{variable_key}\" is not defined in json")
            if not isinstance(variable[variable_key], list):
                raise SyntaxCheckError(file_path, match_line[i], command,
                                       f"for-variable \"{variable_key}\" must be a list in json")
            end_stk.append({"command": command, "i": i})
        elif command.startswith("end"):
            if len(end_stk) == 0:
                raise SyntaxCheckError(file_path, match_line[i], command,
                                       "\"end\" does not match \"if\" or \"for\"")
            if len(end_stk) > 0:
                end_stk.pop(-1)

    if len(end_stk) != 0:
        command = end_stk[-1]["command"]
        i = end_stk[-1]["i"]
        if command.startswith("if-"):
            raise SyntaxCheckError(file_path, match_line[i], command,
                                   "\"if\" does not match \"end\"")
        if command.startswith("for-"):
            raise SyntaxCheckError(file_path, match_line[i], command,
                                   "\"for\" does not match \"end\"")


def compile_markdown(markdown, variable, root, file_path):
    offset = 0
    end_stk = []
    for match in re.finditer(identifier_pattern, markdown):
        command = get_command(match)
        if command.startswith("v-"):
            variable_key = command[2:]
            v = variable[variable_key]
            up_content = str(v)
            start_pos, end_pos = match.span()
            markdown = markdown[:start_pos + offset] + up_content + markdown[end_pos + offset:]
            offset += len(up_content) - len(match.group())
        elif command.startswith("if-"):
            variable_key = command[3:]
            v = variable[variable_key]
            end_stk.append({
                "if": v,
                "match": match
            })
        elif command.startswith("for-"):
            variable_key = command[4:]
            v = variable[variable_key]
            end_stk.append({
                "for": v,
                "match": match
            })
        elif command.startswith("end"):
            if len(end_stk) == 1:
                condition = end_stk[0]
                start_pos, end_pos = match.span()
                if "if" in condition.keys():
                    if_match = condition["match"]
                    is_start_line = 1 if markdown[if_match.span()[1] + offset] == "\n" and markdown[
                        if_match.span()[0] + offset - 1] == "\n" else 0
                    is_end_line = 1 if (markdown[start_pos + offset - 1] == "\n" and (end_pos + offset >= len(markdown)
                                        or markdown[end_pos + offset] == "\n")) else 0
                    if condition["if"]:
                        up_content = markdown[if_match.span()[1] + offset + is_start_line:start_pos + offset - is_end_line]
                        up_content = compile_markdown(up_content, variable, root, file_path)
                        start_pos = if_match.span()[0]
                        end_pos = end_pos
                    else:
                        up_content = ""
                        start_pos = if_match.span()[0] - is_start_line
                        end_pos = end_pos + is_end_line
                    markdown = markdown[:start_pos + offset] + up_content + markdown[end_pos + offset:]
                    offset += - len(match.group()) - len(if_match.group()) - is_end_line - is_start_line
            end_stk.pop(-1)
    return markdown


if __name__ == "__main__":
    _file_path = "test/main"
    _file_path = filter_path(_file_path)
    _markdown_ = load_markdown(_file_path)
    _variable_ = load_variable(_file_path)
    _root_ = str(Path(_file_path).parent)
    try:
        syntax_check(_markdown_, _variable_, _root_, _file_path)
    except SyntaxCheckError as e:
        print('\033[31m' + e.message + '\033[0m')
        exit(0)
    except FileNotFoundError as e:
        print('\033[0m' + e + '\033[0m')
        exit(0)
    res = compile_markdown(_markdown_, _variable_, _root_, _file_path)
    with open("test.md", "w") as f:
        f.write(res)
