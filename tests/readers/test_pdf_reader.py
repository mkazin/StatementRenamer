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


def test_replace_cids_():
    source = '(cid:67)(cid:65)(cid:83)(cid:72)(cid:32)(cid:38)(cid:32)(cid:67)(cid:65)(cid:83)(cid:72)(cid:32)(cid:69)(cid:81)(cid:85)(cid:73)(cid:86)(cid:65)(cid:76)(cid:69)(cid:78)(cid:84)(cid:83)'

    reader = PdfReader()

    result = PdfReader._replace_cids_(source)

    assert result in 'CASH & CASH EQUIVALENTS'
