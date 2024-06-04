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
    "loop": [{"name": "content1", "is_show":true},{"name": "content2","is_show": false},{"name": "content3", "is_show": true}],
}
```
{% endcode %}

### 使用循环

在markdown文件中使用条件判断，需要以 "for-" 指令开头，并且以\<!--{end}-->结尾

通过\<!--\{v-your\_prop\}-->或者\<!--\{if-your\_prop\}-->或者\<!--\{for-your\_prop\}-->可以解析循环中的局部变量

{% code title="main.md" %}
```markdown
<!--{for-loop}-->
# <!--{v-name}-->
<!--{if-is_show}-->
hello world
<!--{end}-->
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
```
{% endcode %}
