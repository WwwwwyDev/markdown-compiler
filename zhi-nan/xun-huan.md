---
description: 可以使用for指令进行循环
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

# 循环

### 定义循环变量

在json文件中定义循环变量，循环变量应为array\[json]类型

{% code title="main.json" %}
```json
{
    "variable": "hello world",
    "loop": [{"name": "content1", "is_show":true},{"name": "content2","is_show": false},{"name": "content3", "is_show": true}]
}
```
{% endcode %}

### 使用循环

在markdown文件中使用循环，需要以 "for-" 或者"forn-"指令开头，并且以\<!--{end}-->结尾

循环中的指令均可解析for变量中的局部参数

注："forn-"后接一个整数，表示循环次数

{% code title="main.md" %}
```markdown
<!--{for-loop}-->
# <!--{v-name}-->
<!--{if-is_show}-->
hello world
<!--{end}-->
<!--{end}-->

<!--{forn-6}-->
hello world
<!--{end}-->
```
{% endcode %}

### 编译结果

{% code title="dist/build.md" %}
```markdown
# content1
hello world
# content2

# content3
hello world

hello world
hello world
hello world
hello world
hello world
hello world
```
{% endcode %}
