from statement_renamer.extractors import vanguard
from datetime import datetime


def test_vanguard_yearly_statement():
    TESTDATA = (
        'DateTransactionAmountSharepriceSharestransactedTotalsharesownedValue'
        'Beginning balance on 12/31/2016$12.34537.672'
        '3214.354Ending balance on 12/31/2017$23,456.78'
        'Client Services: 800-662-2739Page 2 of8')

    extractor = vanguard.VanguardDateExtractor()
    data = extractor.extract(TESTDATA)
    assert data['start_date'] == datetime(2016, 12, 31)
    assert data['end_date'] == datetime(2017, 12, 31)
