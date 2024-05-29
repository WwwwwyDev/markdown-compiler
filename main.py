import argparse
from gen import generate_project
from compiler import compile_file_or_dir

__VERSION__ = '%(prog)s v0.1-beta'

parser = argparse.ArgumentParser(prog='markdown-compiler',
                                 description='Writing a Markdown like programming',
                                 epilog='github: https://github.com/WwwwwyDev/markdown-compiler')
parser.add_argument('-v', '--version', action='version', version=__VERSION__)
subparsers = parser.add_subparsers(title="command", dest="command", help="Build or init", required=True)
build = subparsers.add_parser("build", prog='build',
                              description='Build the project or markdown file')
build.add_argument('path',
                   help="The path of the project of markdown file. If the path is a project(folder), it will find the main.md in project.")
build.add_argument('--name', '-n',
                   help="The name of the compiled markdown file.", required=False)
init = subparsers.add_parser("init", prog='init',
                             description='Init the project with default template')
init.add_argument('path', help="The path of the project")

args = parser.parse_args()
command = args.command
path = args.path
name = "build.md"
if "name" in args and args.name:
    name = args.name
if command == "init":
    generate_project(path)
elif command == "build":
    compile_file_or_dir(path, name)
