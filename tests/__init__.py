import pathlib
import unittest

import markdata

from .block import callout
from .ditaa import ditaa
from .output import output

CASES = pathlib.Path(__file__).parents[0]


class MarkdataTestCase(unittest.TestCase):
    """Test the read process.
    """

    def test_read(self):
        data = CASES / "data"
        for f in data.glob("**/fm.md"):
            _, data = markdata.read_data(f, "YAML")
            self.assertEqual(
                data,
                {
                    "classes": ["table", "bootstrap"],
                    "layout": "post",
                    "title": "Blogging Like a Hacker",
                },
            )

    def test_convert(self):
        for f in CASES.glob("**/test.md"):
            out = f.parent / "output.md"
            with f.open() as data:
                markdown = markdata.markdata(
                    data,
                    directives={
                        "output": output,
                        "ditaa": ditaa,
                        "callout": callout,
                    },
                )
            self.assertMultiLineEqual(markdown, out.read_text())


if __name__ == "__main__":
    unittest.main()
