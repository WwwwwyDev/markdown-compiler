from pathlib import Path
from util import *
import os


class SyntaxCheckError(Exception):

    def __init__(self, file_path, line, command, message):
        file_path = os.path.realpath(filter_path(file_path))
        self.message = f"[SyntaxCheckError] \nposition: from \"{file_path}.md\" line:{line} command:{command} \nmsg: " + message

    def __str__(self):
        return repr(self.message)


def syntax_check(markdown, variable, root, file_path, max_depth=0):
    match_list = [*re.finditer(identifier_pattern, markdown)]
    match_line = []
    for match in match_list:
        start_pos, end_pos = match.span()
        line_number = markdown[:start_pos].count('\n') + 1
        match_line.append(line_number)
    end_stk = []
    for i, match in enumerate(match_list):
        command = get_command(match)
        if command.count("-") > 1:
            raise SyntaxCheckError(file_path, match_line[i], command,
                                   f"the number of \"-\" is over 1")
        if command.startswith("v-"):
            variable_key = get_command_value(command)
            if variable_key not in variable:
                raise SyntaxCheckError(file_path, match_line[i], command,
                                       f"variable \"{variable_key}\" is not defined in corresponding json")
        elif command.startswith("import-"):
            if max_depth > 128:
                raise SyntaxCheckError(file_path, match_line[i], command,
                                       "maximum recursion depth exceeded")
            start_pos, end_pos = match.span()
            if (start_pos > 0 and markdown[start_pos - 1] != "\n") or (
                    end_pos <= len(markdown) - 1 and markdown[end_pos] != "\n"):
                raise SyntaxCheckError(file_path, match_line[i], command,
                                       f"import must be exclusive to one line")
            relative_path = filter_path(get_command_value(command))
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
            if import_path.count("../") >= 128:
                raise SyntaxCheckError(file_path, match_line[i], command,
                                       "maximum recursion depth exceeded")
            try:
                _markdown = load_markdown(import_path)
                variable.update(load_variable(import_path))
                syntax_check(_markdown, variable, root, import_path, max_depth + 1)
            except RecursionError:
                raise SyntaxCheckError(file_path, match_line[i], command,
                                       "maximum recursion depth exceeded")
        elif command.startswith("if-"):
            variable_key = get_command_value(command)
            if variable_key not in variable:
                raise SyntaxCheckError(file_path, match_line[i], command,
                                       f"if-variable \"{variable_key}\" is not defined in corresponding json")
            end_stk.append({"command": command, "i": i})
        elif command.startswith("for-"):
            variable_key = get_command_value(command)
            if variable_key not in variable:
                raise SyntaxCheckError(file_path, match_line[i], command,
                                       f"for-variable \"{variable_key}\" is not defined in corresponding json")
            if not isinstance(variable[variable_key], list):
                raise SyntaxCheckError(file_path, match_line[i], command,
                                       f"for-variable \"{variable_key}\" must be a array[json] in corresponding json")
            flag = False
            keys = set()
            for for_element in variable[variable_key]:
                if not isinstance(for_element, dict):
                    raise SyntaxCheckError(file_path, match_line[i], command,
                                           f"for-variable \"{variable_key}\" must be a array[json] in corresponding json")
                if not flag:
                    for k in for_element.keys():
                        keys.add(k)
                    flag = True
                for k in for_element.keys():
                    if k not in keys:
                        raise SyntaxCheckError(file_path, match_line[i], command,
                                               f"the key of json in for-variable \"{variable_key}\" must be same")
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
        if "{{" in match.group() and "}}" in match.group():
            continue
        if not end_stk and command.startswith("v-"):
            variable_key = get_command_value(command)
            v = variable[variable_key]
            up_content = str(v)
            start_pos, end_pos = match.span()
            markdown = markdown[:start_pos + offset] + up_content + markdown[end_pos + offset:]
            offset += len(up_content) - len(match.group())
        elif not end_stk and command.startswith("import-"):
            relative_path = filter_path(get_command_value(command))
            _root = root
            if not relative_path.startswith("$root/"):
                _root = str(Path(file_path).parent)
            else:
                relative_path = relative_path[6:]
            if relative_path.startswith("/"):
                import_path = relative_path
            else:
                import_path = _root + "/" + relative_path
            _markdown = load_markdown(import_path)
            variable.update(load_variable(import_path))
            up_content = compile_markdown(_markdown, variable, root, import_path)
            start_pos, end_pos = match.span()
            markdown = markdown[:start_pos + offset] + up_content + markdown[end_pos + offset:]
            offset += len(up_content) - len(match.group())
        elif command.startswith("if-"):
            variable_key = get_command_value(command)
            v = variable[variable_key]
            end_stk.append({
                "if": v,
                "match": match
            })
        elif command.startswith("for-"):
            variable_key = get_command_value(command)
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
                                                                                      or markdown[
                                                                                          end_pos + offset] == "\n")) else 0
                    old_content_len = len(markdown[if_match.span()[1] + offset:start_pos + offset])
                    if condition["if"]:
                        up_content = markdown[
                                     if_match.span()[1] + offset + is_start_line:start_pos + offset - is_end_line]
                        up_content = compile_markdown(up_content, variable, root, file_path)
                        start_pos = if_match.span()[0]
                        end_pos = end_pos
                    else:
                        up_content = ""
                        start_pos = if_match.span()[0] - is_start_line
                        end_pos = end_pos + is_end_line
                    markdown = markdown[:start_pos + offset] + up_content + markdown[end_pos + offset:]
                    offset += len(up_content) - old_content_len - len(match.group()) - len(if_match.group())
                elif "for" in condition.keys():
                    for_match = condition["match"]
                    for_variable = condition["for"]
                    is_start_line = 1 if markdown[for_match.span()[1] + offset] == "\n" and markdown[
                        for_match.span()[0] + offset - 1] == "\n" else 0
                    is_end_line = 1 if (markdown[start_pos + offset - 1] == "\n" and (end_pos + offset >= len(markdown)
                                                                                      or markdown[
                                                                                          end_pos + offset] == "\n")) else 0
                    total_up_content = ""
                    old_content_len = len(markdown[for_match.span()[1] + offset:start_pos + offset])
                    for i, for_element in enumerate(for_variable):
                        up_content = markdown[
                                     for_match.span()[1] + offset + is_start_line:start_pos + offset - is_end_line]
                        up_content = compile_markdown(up_content, variable, root, file_path)
                        temp_for_offset = 0
                        for temp_for_match in re.finditer(for_variable_pattern, up_content):
                            temp_for_variable_key = temp_for_match.group()[6:-5].strip()
                            if temp_for_variable_key in for_element:
                                temp_for_up_content = str(for_element[temp_for_variable_key])
                                temp_for_start_pos, temp_for_end_pos = temp_for_match.span()
                                up_content = up_content[
                                             :temp_for_start_pos + temp_for_offset] + temp_for_up_content + up_content[
                                                                                                            temp_for_end_pos + temp_for_offset:]
                                temp_for_offset += len(temp_for_up_content) - len(temp_for_match.group())
                        total_up_content += up_content

                        if is_end_line and i != len(for_variable) - 1:
                            total_up_content += "\n"
                    start_pos = for_match.span()[0]
                    end_pos = end_pos
                    markdown = markdown[:start_pos + offset] + total_up_content + markdown[end_pos + offset:]
                    offset += len(total_up_content) - old_content_len - len(match.group()) - len(for_match.group())
            end_stk.pop(-1)
    return markdown


def compile_file_or_dir(path, name="build.md"):
    try:
        path = Path(path)
        if path.is_dir():
            path = path.joinpath("main.md")
        if not path.exists():
            log("cannot find the file {}".format(str(path)))
            return
        file_path = filter_path(str(path))
        markdown = load_markdown(file_path)
        variable = load_variable(file_path)
        root = str(path.parent)
        syntax_check(markdown, variable, root, file_path)
        res = compile_markdown(markdown, variable, root, file_path)
        build_dir = path.parent.joinpath("dist")
        if not build_dir.exists():
            build_dir.mkdir()
        with open(build_dir.joinpath(name), "w") as f:
            f.write(res)
    except SyntaxCheckError as e:
        log(e.message)
        return
    except FileNotFoundError as e:
        log(str(e))
        return


