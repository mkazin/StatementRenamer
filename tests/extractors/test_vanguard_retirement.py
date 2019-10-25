from statement_renamer.extractors.vanguard_retirement import VanguardRetirementDateExtractor as EXPECTED_EXTRACTOR
from statement_renamer.extractors.factory import ExtractorFactory
from datetime import datetime

TESTDATA = (
    """
    ACCOUNT SUMMARY: 07/01/2018 - 09/30/2018AMAZON.COM 401(K) PLAN
    RETIREMENT PLAN STATEMENTAccount BalanceYour Account ProgressYour Retirement Income Outlook
    Retirement Income*Connect with Vanguard®Total Account Balance:
    >800-523-1188  >vanguard.com*
    """
)


def test_monthly_statement():

    extractor = EXPECTED_EXTRACTOR()
    data = extractor.extract(TESTDATA)
    new_name = extractor.rename(data)

    assert data.get_start_date() == datetime(2018, 7, 1)
    assert data.get_end_date() == datetime(2018, 9, 30)
    assert new_name == '2018-Q3 Vanguard Retirement Statement.pdf'


def test_factory():

    extractor = ExtractorFactory.get_matching_extractor(TESTDATA)

    assert type(extractor) is EXPECTED_EXTRACTOR
