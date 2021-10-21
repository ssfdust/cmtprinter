from cmtprinter import __version__
import textwrap


def test_version():
    assert __version__ == "0.1.0"


def test_wrap_text():
    long_text = "*" * 100
    for i in textwrap.wrap(
        long_text, width=70, initial_indent="- ", subsequent_indent="  "
    ):
        print(i)
