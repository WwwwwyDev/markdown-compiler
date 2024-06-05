---
description: 可以使用v指令使用变量
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

# 变量

### 定义变量

在json文件中定义变量

{% code title="main.json" %}
```json
{
    "variable1": "hello",
    "variable2": "world"
}
```
{% endcode %}

### 使用变量

在markdown文件中使用变量，需要以 "v-" 指令开头

{% code title="main.md" %}
```markdown
# variable
<!--{v-variable1}--> : <!--{v-variable2}-->
```
{% endcode %}

### 编译结果

{% code title="dist/build.md" %}
```markdown
# variable
hello : world
```
{% endcode %}
