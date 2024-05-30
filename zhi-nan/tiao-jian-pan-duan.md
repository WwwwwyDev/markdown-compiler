---
description: 可以使用if指令进行条件判断
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

# 条件判断

### 定义条件变量

在json文件中定义条件变量，条件变量应为bool类型

{% code title="main.json" %}
```json
{
    "variable1": "hello",
    "variable2": "world",
    "is_show": true,
    "is_show2": false
}
```
{% endcode %}

### 使用条件判断

在markdown文件中使用条件判断，需要以 "if-" 指令开头，并且以\<!--{end}-->结尾

{% code title="main.md" %}
```markdown
<!--{if-is_show}-->
# variable
<!--{v-variable1}--><!--{if-is_show2}--> : <!--{v-variable2}--><!--{end}-->
<!--{end}-->
```
{% endcode %}

### 编译结果

{% code title="dist/build.md" %}
```markdown
# variable
hello
```
{% endcode %}
