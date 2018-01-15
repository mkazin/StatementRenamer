from statement_renamer.readers.filename_reader import FilenameReader


def test_pdf_reader():
    TEST_FILE = 'tests/readers/made-with-cc-p4.pdf'
    reader = FilenameReader()
    content = reader.parse(TEST_FILE)
    assert content == TEST_FILE
