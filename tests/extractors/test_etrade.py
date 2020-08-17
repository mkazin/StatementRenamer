from datetime import datetime

from statement_renamer.extractors.etrade import ETradeDateExtractor as EXTRACTOR_UNDER_TEST
from statement_renamer.extractors.factory import ExtractorFactory

TESTDATA = (
    """
    PAGE 1 OF  6 February 1, 2019 - March 31, 2019AccountNumber:####-####AccountType:ROTH IRA
    PAGE 5 OF  6Account Number:  ####-####Statement Period :  February 1, 2019 - March 31, 2019Account Type
    TolearnmoreabouttheRSDAProgram,pleasereviewyourRSDAProgramCustomerAgreement,visitwww.etrade.com,orcallusat1-800-387-2331
    """
)


def test_monthly_statement():

    extractor = EXTRACTOR_UNDER_TEST()
    data = extractor.extract(TESTDATA)
    new_name = extractor.rename(data)

    assert data.get_start_date() == datetime(2019, 2, 1)
    assert data.get_end_date() == datetime(2019, 3, 31)
    assert new_name == '2019-03 E-Trade Statement.pdf'


def test_factory():

    extractor = ExtractorFactory.get_matching_extractor(TESTDATA)

    assert isinstance(extractor, EXTRACTOR_UNDER_TEST)
