from datetime import datetime
from statement_renamer.extractors.fidelity import FidelityDateExtractor as EXTRACTOR_UNDER_TEST
from statement_renamer.extractors.factory import ExtractorFactory

SHARED_TESTDATA = (
    'Brokerage accounts carried by National Financial Services LLC (NFS), Member NYSE, SIPC.M04775210920200731'
    'Brokerage services provided by Fidelity Brokerage Services LLC (FBS), Member NYSE, SIPC (800) 544-6666'
    'Contact InformationOnlineFidelity.comFASTSM-Automated Telephone(800) 544-5555Customer Service(800) 544-6666'
    'Stock Plan Services(800) 544-9354Sun 5pm - Sat 12am ETU.Fund College Investing Plan(800) 544-27762'
)

MONTHLY_TESTDATA = 'INVESTMENT REPORTJuly 1, 2020 - July 31, 2020Envelope # ABCDEFGHIJKLMN' + SHARED_TESTDATA
BIMONTHLY_TESTDATA = 'INVESTMENT REPORTJuly 1, 2020 - August 31, 2020Envelope # ABCDEFGHIJKLMN' + SHARED_TESTDATA
QUARTERLY_TESTDATA = 'INVESTMENT REPORTJanuary 1, 2020 - March 31, 2020Envelope # ABCDEFGHIJKLMN' + SHARED_TESTDATA
YEAR_END_TESTDATA = '2019 YEAR-END INVESTMENT REPORTJanuary 1, 2019 - December 31, 2019Envelope # ABCDEFGHIJKLMN' + SHARED_TESTDATA

def test_monthly_statement():

    extractor = EXTRACTOR_UNDER_TEST()
    data = extractor.extract(MONTHLY_TESTDATA)
    new_name = extractor.rename(data)

    assert data.get_start_date() == datetime(2020, 7, 1)
    assert data.get_end_date() == datetime(2020, 7, 31)
    assert new_name == '2020-07 - Fidelity Statement.pdf'


def test_bimonthly_statement():

    extractor = EXTRACTOR_UNDER_TEST()
    data = extractor.extract(BIMONTHLY_TESTDATA)
    new_name = extractor.rename(data)

    assert data.get_start_date() == datetime(2020, 7, 1)
    assert data.get_end_date() == datetime(2020, 8, 31)
    assert new_name == '2020-07-08 - Fidelity Statement.pdf'


def test_quarterly_statement():

    extractor = EXTRACTOR_UNDER_TEST()
    data = extractor.extract(QUARTERLY_TESTDATA)
    new_name = extractor.rename(data)

    assert data.get_start_date() == datetime(2020, 1, 1)
    assert data.get_end_date() == datetime(2020, 3, 31)
    assert new_name == '2020-Q1 - Fidelity Quarterly Statement.pdf'

def test_year_end_statement():

    extractor = EXTRACTOR_UNDER_TEST()
    data = extractor.extract(YEAR_END_TESTDATA)
    new_name = extractor.rename(data)

    assert data.get_start_date() == datetime(2019, 1, 1)
    assert data.get_end_date() == datetime(2019, 12, 31)
    assert new_name == '2019 - Fidelity Year-End Statement.pdf'


def test_factory():

    extractor = ExtractorFactory.get_matching_extractor(MONTHLY_TESTDATA)

    assert isinstance(extractor, EXTRACTOR_UNDER_TEST)
