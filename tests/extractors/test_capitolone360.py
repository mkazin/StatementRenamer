from statement_renamer.extractors.capitolone360 import CapitolOne360DateExtractor
from statement_renamer.extractors.factory import ExtractorFactory
from datetime import datetime


def test_capitolone360_date_extractor():
    # TESTDATA_A = '''Customer Number XXXXXXX555 Your Savings Summary as of 02/29/2016      Account TypeNicknameAccount NumberAccount BalanceJoint Name360 CheckingElectric Checking5551212$1,234,567.89'''
    TESTDATA = (
        'Your 360 Savings Activity Account: DJT ' +
        'Annual Percentage Yield Earned: 0.75% ' +
        'ActivityDateAmountBalance' +
        'Opening Balance02/01/2016$13,213.32'
        'Deposit from VPUTIN02/16/2016$350,000,000.00$350,013,213.32'
        'Withdrawal to Electric Checking XXXX259476 / 27 / 2016'
        '$(130, 000, 000.00)''$220, 013, 213.32'
        'Closing Balance02 / 29 / 2016$220, 013, 213.32'
        'See below for important information.')

    extractor = CapitolOne360DateExtractor()
    data = extractor.extract(TESTDATA)
    new_name = extractor.rename(data)

    assert data.get_start_date() == datetime(2016, 2, 1)
    assert data.get_end_date() == datetime(2016, 2, 29)
    assert new_name == '2016-02-CapitalOne360.pdf'


def test_factory():
    TESTDATA = (
        'Your 360 Savings Activity Account: DJT '
        'Annual Percentage Yield Earned: 0.75% '
        'ActivityDateAmountBalance'
        'Opening Balance02/01/2016$13,213.32'
        'My Info section.capitalone360.comInteractive'
        'Deposit from VPUTIN02/16/2016$350,000,000.00$350,013,213.32'
        'Withdrawal to Electric Checking XXXX259476 / 27 / 2016'
        '$(130, 000, 000.00)$220, 013, 213.32'
        'Closing Balance02 / 29 / 2016$220, 013, 213.32'
        'See below for important information.')

    extractor = ExtractorFactory.get_matching_extractor(TESTDATA)

    assert type(extractor) is CapitolOne360DateExtractor
