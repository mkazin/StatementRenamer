from statement_renamer.extractors.hanscom import HanscomDateExtractor
from statement_renamer.extractors.factory import ExtractorFactory
from datetime import datetime

TESTDATA = ('DATETRANSACTION DESCRIPTIONAMOUNTFINANCECHARGEBALANCEMEMBER NO.ENDING DATEBRANCH'
            'PAGENOTICE:  PLEASE SEE REVERSE SIDE FOR IMPORTANT INFORMATION***'
            '1234567*9876/1234ACCOUNT HOLDER123 Main StSmallville IA 56789'
            '                                                          1234567890'  # Account number
            '   01-31-16     51        1   MA021270000  71234 P                  '
            '          SAVINGS - MBRPTS 3456          '
            'ACCT#  1                01-01-16 THRU 01-31-16    '
            'PREVIOUS BALANCE             2.50   JAN31  DIVIDEND                 '
            )


def test_hanscom_date_extractor():

    extractor = HanscomDateExtractor()
    data = extractor.extract(TESTDATA)
    new_name = extractor.rename(data)

    assert data.get_start_date() == datetime(2016, 1, 1)
    assert data.get_end_date() == datetime(2016, 1, 31)
    assert new_name == '2016-01-Hanscom.pdf'


def test_factory():

    extractor = ExtractorFactory.get_matching_extractor(TESTDATA)

    assert type(extractor) is HanscomDateExtractor
