from statement_renamer.extractors.aws import AWSDateExtractor
from statement_renamer.extractors.factory import ExtractorFactory
from datetime import datetime

TESTDATA = (
    'AWS, Inc. is a "Registered Foreign Supplier" under Japanese Consumption Tax Law'
    'All charges and prices are in US Dollars'
    'All AWS Services are sold by Amazon Web Services, Inc. '
    'Service Provider:(Not to be used for payment remittance)Amazon Web Services, Inc.410 Terry Ave NorthSeattle , WA   98109-5210 , US1'
    'Account number:************Bill to Address:ATTN: Homer J. Simpsom742 Evergreen TerraceSpringfield , IA , 01234 , US'
    'Amazon Web Services InvoiceEmail or talk to us about your AWS account or bill, visit aws.amazon.com/contact-us/Invoice Summary'
    'Invoice Number:********Invoice Date:August 3 , 2016TOTAL AMOUNT DUE ON August 3 , 2016$0.00'
    'This invoice is for the billing period July 1 - July 31 , 2016Greetings from Amazon Web Services,'
)


def test_aws_yearly_statement():

    extractor = AWSDateExtractor()
    data = extractor.extract(TESTDATA)
    new_name = extractor.rename(data)

    assert data.get_start_date() == datetime(2016, 7, 1)
    assert data.get_end_date() == datetime(2016, 7, 31)
    assert new_name == '2016-07 AWS Invoice.pdf'


def test_factory():

    extractor = ExtractorFactory.get_matching_extractor(TESTDATA)

    assert type(extractor) is AWSDateExtractor
