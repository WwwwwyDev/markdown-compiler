---
description: You can use the "for" command to loop
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

# Loop

### define loop variables

Define a loop variable in the JSON file, which should be of type array\[JSON]

{% code title="main.json" %}
```json
{
    "variable": "hello world",
    "loop": [{"name": "content1", "is_show":true},{"name": "content2","is_show": false},{"name": "content3", "is_show": true}]
}
```
{% endcode %}

### 使用循环

To use loops in a markdown file, it is necessary to start with the "for -" or "for n -" directive and start with \<-- {end}-- >End.

Instructions in the loop can all parse local parameters in the for variable.

Note: "forn-" followed by an integer represents the number of cycles

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

### compiler results

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
