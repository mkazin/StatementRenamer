from statement_renamer.extractors.ascensus import AscensusDateExtractor
from statement_renamer.extractors.factory import ExtractorFactory
from datetime import datetime


def test_ascensus_date_extractor():
    TESTDATA_A = (
        'BalanceVested Percent9/30/15 Vested BalanceEMPLOYEE 401(K)$2'
        'Performance SummaryYour Personal Rate of Return for the period'
        ' 7/1/15 through 9/30/15 is -2.61%. ')

    extractor = AscensusDateExtractor()
    data = extractor.extract(TESTDATA_A)
    new_name = extractor.rename(data)

    assert data.get_start_date() == datetime(2015, 7, 1)
    assert data.get_end_date() == datetime(2015, 9, 30)
    assert new_name == '2015-Q3-AcensusQuarterly.pdf'


def test_ascensus_date_extractor_B():
    TESTDATA_B = (
        'period period ABC period 23 BalanceVested Percent'
        '12/31/15 Vested BalanceEMPLOYEE 401(K)$2Performance Summary'
        'Your Personal Rate of Return for the period '
        '10/1/15 through 12/31/15 is -2.61%. ')

    extractor = AscensusDateExtractor()
    data = extractor.extract(TESTDATA_B)
    new_name = extractor.rename(data)

    assert data.get_start_date() == datetime(2015, 10, 1)
    assert data.get_end_date() == datetime(2015, 12, 31)
    assert new_name == '2015-Q4-AcensusQuarterly.pdf'


def test_factory():
    TESTDATA = (
        'BalanceVested Percent9/30/15 Vested BalanceEMPLOYEE 401(K)'
        '$2Performance SummaryYour Personal Rate of '
        'Return for the period 7/1/15 through 9/30/15 is -2.61%. '
        'Visit us at https://www.planservices.com/')

    extractor = ExtractorFactory.get_matching_extractor(TESTDATA)

    assert type(extractor) is AscensusDateExtractor
