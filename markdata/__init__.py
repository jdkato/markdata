import ast
import os
import re

import frontmatter

from frontmatter.default_handlers import YAMLHandler, TOMLHandler, JSONHandler
from .directives import DIRECTIVES

# Block definitions adhere to the following structure:
#
#    `directive{<arguments>}`
#
# OR
#
#    ```directive{<arguments>}
#    <content>
#    ```
#
# Where 'directive' is a Python function.
DEFINITIONS = re.compile(
    r"(?:``)?`(?P<directive>[\w_]+)(?P<arguments>\{.*?\})"
    + r"(?:\n(?P<content>.+?)\n``)?`",
    re.DOTALL | re.VERBOSE,
)

HANDLERS = {"YAML": YAMLHandler, "TOML": TOMLHandler, "JSON": JSONHandler}


def read_data(file_or_str, fm_format):
    """Read the given buffer (`file_or_str`).
    """
    data = {}
    if hasattr(file_or_str, "read"):
        text = file_or_str.read()
    elif hasattr(file_or_str, "read_text"):
        text = file_or_str.read_text()
    else:
        text = file_or_str

    fmt_handler = HANDLERS.get(fm_format)
    if fmt_handler:
        data, _ = frontmatter.parse(text)

    return text, data


def markdata(file_or_str, directives={}, fm_format=None, root=None):
    """Find and compile all block definitions in `file_or_str`.
    """
    DIRECTIVES.update(directives)
    called_from = os.getcwd()

    # NOTE: Since we accept relative file paths in our directives, we need to
    # operate from within the working director of the Markdown file itself --
    # i.e., its parent directory.
    if isinstance(root, str):
        os.chdir(root)
    elif hasattr(file_or_str, "name") and file_or_str.name != "<stdin>":
        os.chdir(os.path.dirname(os.path.abspath(file_or_str.name)))

    text, data = read_data(file_or_str, fm_format)
    for m in DEFINITIONS.finditer(text):
        groups = m.groups()

        directive = groups[0]
        if directive in DIRECTIVES:
            args = ast.literal_eval(groups[1])
            conv = DIRECTIVES[directive]
            if groups[2] is None:
                # Inline directive:
                value = conv(data, **args)
            else:
                # Block directive:
                value = conv(data, groups[2], **args)
            text = text.replace(m.string[m.start() : m.end()], value, 1)

    # Restore our working directory.
    os.chdir(called_from)
    return text
