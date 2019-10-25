from statement_renamer.extractors.vanguard import VanguardDateExtractor
from statement_renamer.extractors.factory import ExtractorFactory
from datetime import datetime


def test_vanguard_quarterly_statement():
    TESTDATA = (
        'Client Services: 800-662-2739December 31, 2017, year-to-date statement'
        'DateTransactionAmountSharepriceSharestransactedTotalsharesownedValue'
        'Beginning balance on 12/31/2016$12.34537.672'
        '3214.354Ending balance on 12/31/2017$23,456.78'
        'Client Services: 800-662-2739Page 2 of8')

    extractor = VanguardDateExtractor()
    data = extractor.extract(TESTDATA)
    new_name = extractor.rename(data)

    assert data.get_start_date() == datetime(2016, 12, 31)
    assert data.get_end_date() == datetime(2017, 12, 31)
    assert new_name == '2017-Q4 Vanguard Quarterly Statement.pdf'


def test_factory():
    TESTDATA = (
        'Client Services: 800-662-2739December 31, 2017, year-to-date statement'
        'DateTransactionAmountSharepriceSharestransactedTotalsharesownedValue'
        'Beginning balance on 12/31/2016$12.34537.672'
        '3214.354Ending balance on 12/31/2017$23,456.78'
        'Client Services: 800-662-2739Page 2 of8'
        'Vanguard, P.O. Box 2600Valley Forge, PA 19482-2600')

    extractor = ExtractorFactory.get_matching_extractor(TESTDATA)

    assert type(extractor) is VanguardDateExtractor
