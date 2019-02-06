import pathlib
import unittest

from markdata import markdata

from .block import callout
from .ditaa import ditaa
from .output import output

CASES = pathlib.Path(__file__).parents[0]


class ReadTestCase(unittest.TestCase):
    """Test the read process.
    """

    def test_read(self):
        for f in CASES.glob("**/test.md"):
            out = f.parent / "output.md"
            with f.open() as data:
                markdown = markdata(
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
