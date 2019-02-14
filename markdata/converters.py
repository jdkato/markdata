import tabulate

from functools import partial


def _html_row_with_attrs(celltag, cell_values, colwidths, colaligns):
    alignment = {
        "left": "",
        "right": ' style="text-align: right;"',
        "center": ' style="text-align: center;"',
        "decimal": ' style="text-align: right;"',
    }
    values_with_attrs = [
        "<{0}>{1}</{0}>".format(celltag, c)
        for c, a in zip(cell_values, colaligns)
    ]
    rowhtml = "<tr>" + "".join(values_with_attrs).rstrip() + "</tr>"
    if celltag == "th":  # it's a header row, create a new table header
        rowhtml = "\n".join(["<thead>", rowhtml, "</thead>", "<tbody>"])

    return rowhtml


def to_html_table(rows, caption="", classes=[]):
    """Convert the given rows into an HTML table.

    The first entry in `rows` will be used as the table headers.
    """
    headers = rows.pop(0)

    above = "<table{0}>".format(
        ' class="{0}"'.format(" ".join(classes) if classes else "")
    )
    if caption:
        above += "\n<caption>{0}</caption>\n".format(caption)

    return tabulate.tabulate(
        rows,
        headers,
        stralign=None,
        numalign=None,
        tablefmt=tabulate.TableFormat(
            lineabove=tabulate.Line(above, "", "", ""),
            linebelowheader="",
            linebetweenrows=None,
            linebelow=tabulate.Line("</tbody>\n</table>", "", "", ""),
            headerrow=partial(_html_row_with_attrs, "th"),
            datarow=partial(_html_row_with_attrs, "td"),
            padding=0,
            with_header_hide=None,
        ),
    )
