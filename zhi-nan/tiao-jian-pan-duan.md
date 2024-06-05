---
description: Can use the "if" command for conditional judgment.
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

# Condition

### define conditional variables

Define conditional variables in the JSON file, which should be of type bool.

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

### use conditional judgment

To use conditional judgment in a markdown file, it needs to start with the "if -" or "if n -" directive and start with "<--- {end}--->"End.

Note: The "ifn -" instruction will logically invert the corresponding variable.

{% code title="main.md" %}
```markdown
<!--{if-is_show}-->
# variable
<!--{v-variable1}--><!--{ifn-is_show2}--> : <!--{v-variable2}--><!--{end}-->
<!--{end}-->
```
{% endcode %}

### compiler results

{% code title="dist/build.md" %}
```markdown
# variable
hello : world
```
{% endcode %}
