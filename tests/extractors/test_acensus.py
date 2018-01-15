from statement_renamer.extractors import ascensus
from datetime import datetime


def test_ascensus_date_extractor():
    TESTDATA_A = '''BalanceVested Percent9/30/15 Vested BalanceEMPLOYEE 401(K)$2Performance SummaryYour Personal Rate of Return for the period 7/1/15 through 9/30/15 is -2.61%. '''
    extractor = ascensus.AscensusDateExtractor()
    data = extractor.extract(TESTDATA_A)
    assert data['start_date'] == datetime(2015, 7, 1)
    assert data['end_date'] == datetime(2015, 9, 30)


def test_ascensus_date_extractor_B():
    TESTDATA_B = '''period period ABC period 23 BalanceVested Percent9/30/15 Vested BalanceEMPLOYEE 401(K)$2Performance SummaryYour Personal Rate of Return for the period 7/1/15 through 9/30/15 is -2.61%. '''
    extractor = ascensus.AscensusDateExtractor()
    data = extractor.extract(TESTDATA_B)
    assert data['start_date'] == datetime(2015, 7, 1)
    assert data['end_date'] == datetime(2015, 9, 30)
