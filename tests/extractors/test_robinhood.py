from statement_renamer.extractors.robinhood import RobinhoodDateExtractor
from statement_renamer.extractors.factory import ExtractorFactory
from datetime import datetime

TESTDATA = (
    'Page 1 of 6 Robinhood85 Willow Rd, Menlo Park, CA 94025support@robinhood.com02/01/2019 to 02/28/2019Montgomery Burns Account #:12345678900 '
    'Evergreen Terrace Springfield IA 01234PTIONSEQUITIESCASHAccount SummaryOPENINGBALANCECLOSINGBALANCENet Account Balance$12345678.90$1234.56'
    'Total Securities$12345.67$6543.21Portfolio Value$246.80$98765.43Income and ExpenseSummaryTHIS PERIODYEAR TO DATEDividends$0.00$0.00'
    'Capital Gains$0.00$0.00Interest$0.00$0.00Portfolio AllocationCASH0.34\%EQUITIES99.66%OPTIONS0.00%This statement shall be conclusive '
    'if not objected to in writing within ten days. Errors and omissions exempted. Please address all communications to the ﬁrm and not '
    'to the individuals. Address changes orother material changes on your account should be directed to the oﬃce servicing your account. '
    'Kindly mention your account number. This statement should be retained for income tax purposes.'
)


def test_robinhood_monthly_statement():

    extractor = RobinhoodDateExtractor()
    data = extractor.extract(TESTDATA)
    new_name = extractor.rename(data)

    assert data.get_start_date() == datetime(2019, 2, 1)
    assert data.get_end_date() == datetime(2019, 2, 28)
    assert new_name == '2019-02 Robinhood Statement.pdf'


def test_factory():

    extractor = ExtractorFactory.get_matching_extractor(TESTDATA)

    assert type(extractor) is RobinhoodDateExtractor
