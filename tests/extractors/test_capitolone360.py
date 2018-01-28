from statement_renamer.extractors import capitolone360
from datetime import datetime


def test_ascensus_date_extractor():
    # TESTDATA_A = '''Customer Number XXXXXXX555 Your Savings Summary as of 02/29/2016      Account TypeNicknameAccount NumberAccount BalanceJoint Name360 CheckingElectric Checking5551212$1,234,567.89'''
    TESTDATA = (
        'Your 360 Savings Activity Account: DJT ' +
        'Annual Percentage Yield Earned: 0.75% ' +
        'ActivityDateAmountBalance' +
        'Opening Balance02/01/2016$13,213.32'
        'Deposit from VPUTIN02/16/2016$350,000,000.00$350,013,213.32'
        'Withdrawal to Electric Checking XXXX259476 / 27 / 2016$(130, 000, 000.00)$220, 013, 213.32'
        'Closing Balance02 / 29 / 2016$220, 013, 213.32See below for important information.')

    extractor = capitolone360.CapitolOne360DateExtractor()
    data = extractor.extract(TESTDATA)
    assert data['start_date'] == datetime(2016, 2, 1)
    assert data['end_date'] == datetime(2016, 2, 29)
