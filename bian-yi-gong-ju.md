---
description: mkdc命令可以帮助你创建项目以及编译项目
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

# 编译工具

### mkdc

```shell
# 使用-h查看帮助文档
mkdc -h 
# 使用-v查看当前版本号
mkdc -v
```

### init子命令

```sh
# 使用-h查看帮助文档
mkdc init -h
# 使用init初始化项目，内含一个初始化模版
mkdc init your_project_path
```

### build子命令

```sh
# 使用-h查看帮助文档
mkdc build -h
# 使用build编译你的项目，以项目目录下的main.md作为入口，会在项目目录下的dist文件夹中，生成一个编译后的build.md文件
mkdc build your_project_path
# -n可以指定，编译后的markdown文件名字
mkdc build your_project_path -n your_markdown_name
# 使用build编译你的markdown文件，会将该文件的父级目录作为项目根目录
mkdc build your_markdown_file.md
```
