from statement_renamer.extractors.amazonprime import AmazonPrimeDateExtractor
from statement_renamer.extractors.factory import ExtractorFactory
from datetime import datetime

TESTDATA = (
    """
    Download theChase Mobileapp today® ACCOUNT SUMMARY
    Get updates on the goLogon tochase.com/alertsP.O. BOX 15123   WILMINGTON, DE 19850-5123For Undeliverable Mail Only$
    This Statement is a Facsimile - Not an originalPayment Due Date:04/28/19New BalanceCredit Card Statement
    www.chase.com/amazon1-888-247-4080Download theChase Mobileapp 
    todayMake/Mail to Chase Card Services at the address below:Late Payment Warning:  
	Opening/Closing Date03/06/19 - 04/03/19Credit Access Line
    TRANSFERS28 Days in Billing PeriodPage2 of 2Statement Date:04/03/19JOHN A DOEDate ofTransactionMerchant
    """
)


def test_monthly_statement():

    extractor = AmazonPrimeDateExtractor()
    data = extractor.extract(TESTDATA)
    new_name = extractor.rename(data)

    assert data.get_start_date() == datetime(2019, 3, 6)
    assert data.get_end_date() == datetime(2019, 4, 3)
    assert new_name == '2019-04 AmazonPrime Statement.pdf'


def test_factory():

    extractor = ExtractorFactory.get_matching_extractor(TESTDATA)

    assert type(extractor) is AmazonPrimeDateExtractor
