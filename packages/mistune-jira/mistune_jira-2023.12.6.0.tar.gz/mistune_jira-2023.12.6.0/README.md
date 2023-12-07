# mistune-jira

A Jira Rendering Engine for Mistune. 

[Mistune](https://github.com/lepture/mistune) is awesome. It does an amazing job of parsing
markdown. It has the ability to take those documents and export them in different sytaxes.
This is an attempt to write a parser for 
[Atlassian's Markup Language used in Jira and some other tools](https://jira.atlassian.com/secure/WikiRendererHelpAction.jspa?section=all).

The goal is to be able to have data in markdown and then use that markdown to create a well formatted
ticket in Jira. 

Hopefully Jira will someday fully support markdown and make this project irrelevant.

## Usage

```python
import mistune
import mistune_jira

text = '''
# Lorem Ipsum

This is some sample markdown. [Say hi to google](https://www.google.com) as an example link
to be converted. 

HR line 
---

* a list of cool things
* doggies
    * Little Doggies (Won't yet render correctly)
    * Shaggy Doggies
    * Grumpy Doggies
* spaceships
* $2 bills

'''

rend = mistune_jira.JiraRenderer()

markdown_parser = mistune.Markdown(renderer=rend)

jira_compat = markdown_parser(text)

print(jira_compat)
```