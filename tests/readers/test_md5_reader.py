from statement_renamer.readers.md5_reader import Md5Reader


def test_pdf_reader():
    TEST_FILE = 'tests/readers/made-with-cc-p4.pdf'

    reader = Md5Reader()
    contents = reader.parse(TEST_FILE)

    assert 'fc25bb5ae5cc65356bfef228903940a1' == contents
