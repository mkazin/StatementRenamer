from datetime import datetime
from statement_renamer.extractors.fidelity_cc import FidelityCreditCardDateExtractor as EXTRACTOR_UNDER_TEST
from statement_renamer.extractors.factory import ExtractorFactory

TESTDATA = (
    'Open Date:07/29/2020Closing Date:08/27/2020Account: '
    'fidelityrewards.com/login'
)


def test_fidelity_cc_date_extractor():

    extractor = EXTRACTOR_UNDER_TEST()
    data = extractor.extract(TESTDATA)
    new_name = extractor.rename(data)

    assert data.get_start_date() == datetime(2020, 7, 29)
    assert data.get_end_date() == datetime(2020, 8, 27)
    assert new_name == '2020-08 - Fidelity CC Statement.pdf'


def test_factory():

    extractor = ExtractorFactory.get_matching_extractor(TESTDATA)

    assert isinstance(extractor, EXTRACTOR_UNDER_TEST)
