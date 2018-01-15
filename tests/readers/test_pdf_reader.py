from statement_renamer.readers.pdf_reader import PdfReader


def test_pdf_reader():
    TEST_FILE = 'tests/readers/made-with-cc-p4.pdf'

    reader = PdfReader()
    contents = reader.parse(TEST_FILE)

    assert 'Made With Creative Commons' in contents
    assert 'Ctrl+Alt+Delete Books' in contents
    assert 'by Paul Stacey & Sarah Hinchliff Pearson' in contents
    assert 'Downloadable e-book available at madewith.cc' in contents
    assert 'Drukarnia POZKAL' in contents
