from statement_renamer.extractors.ssa import SocialSecurityDateExtractor
from statement_renamer.extractors.factory import ExtractorFactory
from datetime import datetime

TESTDATA = (
    'Follow the Social Security Administration at these social media sites.     '
    'Your payment would be about$1,234 a monthat full retirement age'
    'George J. Foreman IIIApril 30, 2018Your Social Security Statement Your Social '
    'Security Statement tells you about how much you or your family would receive in disability,'
    ' survivor, or retirement benefits. It also includes our record of your lifetime earnings. '
    'Your estimated taxable earnings per year after 2018')

def test_ssa_yearly_statement():

    extractor = SocialSecurityDateExtractor()
    data = extractor.extract(TESTDATA)
    new_name = extractor.rename(data)

    assert data.get_start_date() == datetime(2018, 1, 1)
    assert data.get_end_date() == datetime(2018, 12, 31)
    assert new_name == '2018 Yearly Statement.pdf'


def test_factory():

    extractor = ExtractorFactory.get_matching_extractor(TESTDATA)

    assert type(extractor) is SocialSecurityDateExtractor
