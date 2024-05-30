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
    "variable1": "hello",
    "variable2": "world",
    "is_show": true,
    "is_show2": false,
    "loop": [{"name": "content1"},{"name": "content2"},{"name": "content3"}]
}
```
{% endcode %}

### 使用循环

在markdown文件中使用条件判断，需要以 "for-" 指令开头，并且以\<!--{end}-->结尾

通过\<!--\{{your\_prop\}}-->，可以解析循环中的局部变量

{% code title="main.md" %}
```markdown
<!--{for-loop}-->
<!--{if-is_show}-->
# <!--{{name}}-->
<!--{v-variable1}--><!--{if-is_show2}--> : <!--{v-variable2}--><!--{end}-->
<!--{end}-->
<!--{end}-->
```
{% endcode %}

### 编译结果

{% code title="dist/build.md" %}
```markdown
# content1
hello
# content2
hello
# content3
hello
```
{% endcode %}
