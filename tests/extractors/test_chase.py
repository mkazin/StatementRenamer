from statement_renamer.extractors.chase import ChaseDateExtractor as EXPECTED_EXTRACTOR
from statement_renamer.extractors.factory import ExtractorFactory
from datetime import datetime

TESTDATA = (
    """
	www.chase.com/creditcardsDownload theChase Mobileapp today® 
	PAYMENT INFORMATIONACCOUNT SUMMARYYOUR ACCOUNT MESSAGESACCOUNT 
	ACTIVITYYear-to-date totals do not reflect any fee or interest refundsyou may have received.
	INTEREST CHARGESGet updates on the goLogon tochase.com/alertsP.O. BOX 15123WILMINGTON, DE19850-5123$
	This Statement is a Facsimile - Not an originalPayment Due Date:08/10/17New Balance:$0.00
	1-800-945-2000Make your check payable to:  Chase Card ServicesLate Payment Warning:  
	Amount EnclosedNew Balance$0.00Payment Due Date08/10/17Minimum Payment Due$0.00
	If we do not receive your minimum paymentby the date listed above, you may have to pay a late fee of up to $35.00.
	Fees Charged$0.00Interest Charged$0.00New Balance$0.00Opening/Closing Date06/14/17 - 07/13/17Credit Limit$1,234,567
   """
)


def test_monthly_statement():

    extractor = EXPECTED_EXTRACTOR()
    data = extractor.extract(TESTDATA)
    new_name = extractor.rename(data)

    assert data.get_start_date() == datetime(2017, 6, 14)
    assert data.get_end_date() == datetime(2017, 7, 13)
    assert new_name == '2017-06 Chase Slate Statement.pdf'


def test_factory():

    extractor = ExtractorFactory.get_matching_extractor(TESTDATA)

    assert type(extractor) is EXPECTED_EXTRACTOR
