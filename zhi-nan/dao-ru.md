---
description: 可以使用import指令导入另一个文件的内容
---

# 导入

### 导入文件

在markdown文件中导入另一个文件，需要以 "import-" 指令开头。import指令必须单独一行

$root为项目根目录，你也可以使用相对路径或者绝对路径的写法



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

### 编译结果

{% code title="dist/build.md" %}
```markdown
# main content
main content

# hello content
hello content
```
{% endcode %}
