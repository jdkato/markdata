# Markdata: Keep your data out of your markup!

[![Build Status](https://img.shields.io/travis/errata-ai/vale/master.svg?logo=travis)](https://travis-ci.org/errata-ai/markdata) [![PyPI](https://img.shields.io/pypi/v/markdata.svg?colorB=blue&style=flat)](https://pypi.org/project/markdata/) [![wheels](https://img.shields.io/badge/wheels-%E2%9C%93-4c1.svg?longCache=true&logo=python&logoColor=white)](https://pypi.org/project/markdata/#files) [![code style](https://img.shields.io/badge/code%20style-black-%23000.svg)](https://black.readthedocs.io/en/stable/)

**Markdata** is a Python library and command-line tool for managing data (e.g., code, diagrams, tables, etc.) in Markdown files. Its goal is to promote one simple rule: prose and non-prose supplements (collectively referred to as "data") should be managed separately whenever possible. The benefits of this philosophy include:

- Adherence to the [DRY principle](https://en.wikipedia.org/wiki/Don%27t_repeat_yourself): multiple files can include data from the same source.

- Higher-quality data: code examples can be tested, tables can be generated directly from serialization formats, diagrams can be built from source, etc.

- Human-friendly markup: less non-prose content means shorter files, which are easier to update and maintain.

See [*Fixing Markdown’s shortcomings with Python*](https://medium.com/@jdkato/fixing-markdowns-shortcomings-with-python-cf1d31450e56) for more information.

## Installation

> :exclamation: Markdata requires Python >= 3.6.0. :exclamation:

```console
$ pip install markdata
```

## Usage

###### As a library

```python
import markdata

def my_directive():
    pass

markdown = markdata.markdata(
    # A string or file-like object.
    file_or_str,
    # A dictionary of custom directives (optional).
    #
    # Format: {'name': my_directive}.
    directives={},
    # The type of front matter to parse (optional).
    fm_format=None,  # 'JSON', 'YAML', or 'TOML'
    # The directory that paths will be resolved relative to (optional).
    root=None
)
```

###### From the command line

```console
$ markdata --help
Usage: markdata [OPTIONS] SOURCE [DESTINATION]

  A flavor-agnostic extension framework for Markdown.

  Reads from <SOURCE> and writes to <DESTINATION>.

  If <SOURCE> is a single file, it will be converted to Markdown and written
  to <DESTINATION> (default: stdout).

  If <SOURCE> is a directory, all child Markdata files will be converted to
  Markdown and written to <DESTINATION> (default: overwrite <SOURCE>).

Options:
  --fm-type [JSON|YAML|TOML]  The type of front matter to parse.
  --root PATH                 The directory that paths will be resolved
                              relative to.
  --directives PATH           The directory containing your custom directives.
  --version                   Show the version and exit.
  --help                      Show this message and exit.
```

## Directives

Markdata's functionality is driven by *directives*, which are Markdown snippets that invoke Python functions. Directives can be defined in two ways:

````markdown
# Example directives

<!-- This is a "block" directive -->

```callout{'title': 'NOTE', 'classes': ['warning']}
This is a callout message.
```

<!-- This is an "inline" directive -->

`table{'path': '../data/table.yml', 'classes': ['table'], 'caption': 'My data'}`
````

The `table` directive creates an HTML table from a YAML, JSON, or CSV file (with an optional caption and classes). After calling `markdata` on this file, the output would be something along the lines of:

```html
<table class="table">
    <caption>My data</caption>
    <thead>
        <!-- headers -->
    </thead>
    <tbody>
        <!-- rows -->
    </tbody>
</table>
```

### Built-in directives

Markdata has a few built-in, general-purpose directives:

```python
def table(path: str, classes: List[str] = [], caption: str = "") -> str:
    """Return an HTML table built from structured data (CSV, JSON, or YAML).

    `path` [required]: A path (relative to the directive-containing file) to a
           CSV, JSON, or YAML file.

    `classes` [optional]: A list of HTML classes to apply to the table.

    `caption` [optional]: A caption for the table.

    Example:

        `table{'path': 'table.yml', 'classes': ['table'], 'caption': '...'}`
    """
```

The `table` directive ([discussed above](#directives)) creates an HTML table from an external data source (CSV, JSON, or YAML). This allows you to avoid having to write and maintain tables in raw Markdown or HTML.

```python
def document(path: str, span: Tuple[int, int] = []) -> str:
    """Return the contents of a document (or part of it).

    `path` [required]: A path (relative to the directive-containing file) to a
           local file.

    `span` [optional]: A tuple ([begin, end]) indicating the beginning and
           ending line of the snippet (defaults to the entire file).

    Example:

        `document{'path': 'my_file.py', 'span': (10, 13)}`
    """
```

The `document` directive includes the content of an external text file (of any type&mdash;Markdown, Python, etc.).

```python
def code(front_matter, path, span=[], lang=None):
    """Return the contents of a document (or part of it) as a code block.

    `path` [required]: A path (relative to the directive-containing file) to a
           local file.

    `span` [optional]: A tuple ([begin, end]) indicating the beginning and
           ending line of the snippet (defaults to the entire file).

    `lang` [optional]: The code block's info string. If not defined, it will be
           inferred from the given file extension.

    Example:
        `code{'path': 'my_file.py', 'span': [10, 13], 'lang': 'python'}`
    """
```

The `code` directive includes the content of an external source code formatted as a [fenced code block](https://spec.commonmark.org/0.29/#fenced-code-blocks). This allows you to, for example, write your code examples in their own files (which can be properly tested and linted).

### Writing your own

> **NOTE**: The first argument passed to custom directives will be a dictionary created from the file's front matter (`{}` by default).

While `table` and `document` attempt to solve the most common needs, the true power of Markdata comes from leveraging Python in *your own* directives.

There are three steps to creating a directive:

1. Design your *directive definition*:  Choose either an inline or block directive and decide what arguments it'll accept.

2. Write a Python function: This function needs to accept the arguments defined in step (1). So, if you were re-implementing the built-in `table` directive, you'd have a directive definition of `table{'path': '../data/table.yml', 'classes': ['table'], 'caption': 'My data'}` and a function definition of `table(fm: Dict, path: str, classes: List[str] = [], caption: str = "") -> str:`. When using block directives, the first argument passed to the backend function is its content (see our [admonition example](https://github.com/errata-ai/markdata/blob/master/tests/block/__init__.py)).

3. Associate your directive with your function:

    - Using the library:
    ```python
    # When using Markdata as a library, you simply pass your function to `markdata`:
    import markdata


    def implementation(path):
        pass

    markdown = markdata.markdata(file_or_str, directives={'directive': implementation})
    ```
    - Using the command-line tool: Markdata will associate all Python modules with their `main` function found in the   directory passed to `--directives='my_dir'`.

Check out [our test cases](https://github.com/errata-ai/Markdata/tree/master/tests) for some examples.

#### Converters

Converters are utilities that you can import and use in your own directives.

```python
# from markdata.converters import to_html_table
def to_html_table(
    rows: List[List[str]], caption: str = "", classes: List[str] = []
) -> str:
    """Convert the given rows into an HTML table.

    The first entry in `rows` will be used as the table headers.
    """
```

## FAQ

> Why only Markdown? What about AsciiDoc and reStructuredText?

AsciiDoc and reStructuredText have more feature-rich syntaxes than Markdown. Many of Markdata's features are available out-of-the-box (in some form) in AsciiDoc and reStructuredText.

That said, Markdown has a much larger ecosystem of parsers (practically every language has a *native* Markdown library), editors (and editor plugins), linters, and static site generators than both AsciiDoc and reStructuredText.

Markdata's goal is to enrich Markdown's syntax without hurting its portability (see the next question).

> What "flavors" of Markdown does Markdata support?

*All of them*.

One of the common complaints about Markdown is that many of its best features are tied to a particular "flavor" (see [Babelmark](https://johnmacfarlane.net/babelmark2/faq.html)) that may not be compatible with other Markdown-related tooling.

Markdata avoids this problem by acting as more of a "preprocessor" (i.e., `Markdata + Markdown <=> Sass + CSS`) than another Markdown implementation. Its users have full control over what it outputs&mdash;meaning that they can choose to output raw HTML (effectively bypassing the problem of flavors altogether) or make use of features limited to their favorite flavor:

<p align="center">
  <img src ="https://user-images.githubusercontent.com/8785025/52157384-8b1b5780-2643-11e9-83de-828d2e541742.png"/>
</p>

> What if I'm already using a static site generator (SSG)?

While many SSGs have built-in support for external data sources (e.g., [Jekyll](https://jekyllrb.com/docs/datafiles/), [Hugo](https://gohugo.io/templates/data-templates/), and [Gatsby](https://www.gatsbyjs.org/tutorial/part-four/)), there are still benefits to using Markdata:

- As dicussed in the previous question, Markdata *doesn't* introduce new Markdown syntax&mdash;meaning Markdata directives can be used with *any* SSG that supports Markdown. This means that you can change SSGs without having to update the syntax (i.e., template language) for accessing your data.

- Markdata's ability to manage data is far more powerful than what most SSGs offer: instead of merely iterating over static resource files, you have full access to Python and its library ecosystem. So, for example, you can
    - fetch data from APIs using the ultra-popular [Requests](http://docs.python-requests.org/en/master/) library;
    - include plots and diagrams created with [seaborn](https://github.com/mwaskom/seaborn); or
    - transform data using [pandas](https://github.com/pandas-dev/pandas).
