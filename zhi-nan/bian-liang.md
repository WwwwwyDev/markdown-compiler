---
description: You can use the "v" command to use variables.
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

# Variable

### define variables

Define variables in the JSON file

{% code title="main.json" %}
```json
{
    "variable1": "hello",
    "variable2": "world"
}
```
{% endcode %}

### use variables

To use variables in a markdown file, it is necessary to start with the "v -" directive

{% code title="main.md" %}
```markdown
# variable
<!--{v-variable1}--> : <!--{v-variable2}-->
```
{% endcode %}

### compiler results

{% code title="dist/build.md" %}
```markdown
# variable
hello : world
```
{% endcode %}
