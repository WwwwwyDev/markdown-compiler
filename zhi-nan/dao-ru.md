---
description: You can use the "import" command to import the content of another file.
---

# Import

### import file

To import another file in the markdown file, it needs to start with the "import-" directive. The import directive must be on a separate line.

$root is the root directory of the project, and you can also use relative or absolute path notation.

{% tabs %}
{% tab title="main.md" %}
{% code title="main.md" %}
```markdown
# <!--{v-name}--> content
<!--{v-name}--> content

<!--{import-$root/hello}-->
```
{% endcode %}
{% endtab %}

{% tab title="main.json" %}
{% code title="main.json" %}
```json
{
    "name": "main"
}
```
{% endcode %}
{% endtab %}

{% tab title="hello.md" %}
{% code title="hello.md" %}
```markdown
# <!--{v-name}--> content
<!--{v-name}--> content
```
{% endcode %}
{% endtab %}

{% tab title="hello.json" %}
{% code title="hello.json" %}
```json
{
    "name": "hello"
}
```
{% endcode %}
{% endtab %}
{% endtabs %}

### compiler results

{% code title="dist/build.md" %}
```markdown
# main content
main content

# hello content
hello content
```
{% endcode %}
