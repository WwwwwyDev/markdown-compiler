---
description: The `mkdc` command can help you create a project and compile it.
layout:
  title:
    visible: true
  description:
    visible: true
  tableOfContents:
    visible: true
  outline:
    visible: true
  pagination:
    visible: true
---

# Command line tools

### mkdc

```shell
# Use `-h` to view the help documentation.
mkdc -h 
# Use `-v` to view the current version number.
mkdc -v
```

### init子命令

```sh
# Use -h to see the help document.
mkdc init -h
# Use `init` to initialize the project, which includes an initialization template.
mkdc init your_project_path
```

### build子命令

```sh
# Use `-h` to view the help document.
mkdc build -h
# Use `build` to compile your project, using `main.md` as the entry point in the project directory, and it will generate a compiled `build.md` file in the `dist` folder of the project directory.d文件
mkdc build your_project_path
# Use `-n` can be specified to specify the name of the compiled markdown file.
mkdc build your_project_path -n your_markdown_name
# Using `build` to compile your markdown file will set the parent directory of that file as the project root directory.
mkdc build your_markdown_file.md
```
