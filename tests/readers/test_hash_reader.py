from statement_renamer.readers.hash_reader import HashReader

def test_hesh_reader():
    TEST_FILE = 'tests/readers/made-with-cc-p4.pdf'

    reader = HashReader()
    contents = reader.parse(TEST_FILE)

    assert contents == '2c9f57f8f0e291e84aebc0c3337ea6a1fb07ddc8c134f67ff9d6420ed472d99e'
