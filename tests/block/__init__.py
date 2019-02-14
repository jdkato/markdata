def callout(fm, content, title="", classes=[]):
    """Example directive for generating admonitions.
    """
    return (
        '<div class="admonition {0}">\n'.format(" ".join(classes))
        + '    <p class="admonition-title">{0}</p>\n'.format(title)
        + "    <p>{0}</p>\n".format(content)
        + "</div>"
    )
