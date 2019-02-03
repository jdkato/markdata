import ast
import os
import re

from .directives import DIRECTIVES

# Block definitions adhere to the following structure:
#
#    `directive{<arguments>}`
#
# Where 'directive' is a Python function.
DEFINITIONS = re.compile(
    r"`(?P<directive>[\w_]+)(?P<arguments>\{.*?\})`", re.DOTALL | re.VERBOSE
)


def markdata(file_or_str, directives={}, root=None):
    """Find and compile all block definitions in the file `f_obj`.
    """
    DIRECTIVES.update(directives)

    # NOTE: Since we accept relative file paths in our directives, we need to
    # operate from within the working director of the Markdown file itself --
    # i.e., its parent directory.
    if isinstance(root, str):
        os.chdir(root)
    elif hasattr(file_or_str, "name") and file_or_str.name != "<stdin>":
        os.chdir(os.path.dirname(os.path.abspath(file_or_str.name)))

    text = file_or_str.read() if hasattr(file_or_str, "read") else file_or_str
    for m in DEFINITIONS.finditer(text):
        groups = m.groups()

        directive = groups[0]
        if directive in DIRECTIVES:
            args = ast.literal_eval(groups[1])
            conv = DIRECTIVES[directive]
            text = text.replace(m.string[m.start() : m.end()], conv(**args), 1)

    return text
