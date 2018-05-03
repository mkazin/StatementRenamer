from statement_renamer.extractors.rcn import RcnDateExtractor
from statement_renamer.extractors.factory import ExtractorFactory
from datetime import datetime


def disabled_test_rcn_statement():
    TESTDATA = (
        '1-800-RING-RCN (1-800-746-4726)Website:'
        'Statement Date:Account Number:Payment Due Date:11'
        'Statement Date:Account Number:Payment Due Date:01/31/20172301-'
    )

    extractor = RcnDateExtractor()
    data = extractor.extract(TESTDATA)
    new_name = extractor.rename(data)

    assert data.get_start_date() == datetime(2017, 1, 1)
    assert data.get_end_date() == datetime(2017, 1, 31)
    assert new_name == '2017-01-RCN.pdf'


def disabled_test_start_of_month_statement():
    TESTDATA = (
        '1-800-RING-RCN (1-800-746-4726)Website:'
        'Bill Date04/01/2016Due Date'
        'QtyDescriptionDateAmount0.0005/01 - 05/31Customer Owned Modem'
    )

    extractor = RcnDateExtractor()
    data = extractor.extract(TESTDATA)
    new_name = extractor.rename(data)

    # TODO: this fails because we're parsing the statement date,
    # rather than the statement period. Problem is the statement
    # period doesn't include a year, which means we need to grab
    # it from the statement date (and handle edge cases- ick)
    # Let's try checking the PDF/data again (for various versions
    # of this statement format) to see if there's some kind of
    # halfway elegant solution to this extractor.
    assert data.get_start_date() == datetime(2016, 5, 1)
    assert data.get_end_date() == datetime(2016, 5, 31)
    assert new_name == '2016-04-RCN.pdf'


def disabled_test_start_of_year_statement():
    TESTDATA = (
        '1-800-RING-RCN (1-800-746-4726)Website:'
        'Bill Date12/29/2016Due Date'
        'QtyDescriptionDateAmount0.0001/05 - 02/04Customer Owned Modem'
    )

    extractor = RcnDateExtractor()
    data = extractor.extract(TESTDATA)
    new_name = extractor.rename(data)

    # TODO: this fails because we're parsing the statement date,
    # rather than the statement period. Problem is the statement
    # period doesn't include a year, which means we need to grab
    # it from the statement date (and handle edge cases- ick)
    # Let's try checking the PDF/data again (for various versions
    # of this statement format) to see if there's some kind of
    # halfway elegant solution to this extractor.
    assert data.get_start_date() == datetime(2017, 1, 5)
    assert data.get_end_date() == datetime(2017, 2, 4)
    assert new_name == '2017-01-RCN.pdf'


def disabled_test_old_rcn_statement():
    TESTDATA = (
        '1-800-RING-RCN (1-800-746-4726)Website:'
        'Bill Date04/29/2016Due Date'
    )

    extractor = RcnDateExtractor()
    data = extractor.extract(TESTDATA)
    new_name = extractor.rename(data)

    assert data.get_start_date() == datetime(2016, 4, 1)
    assert data.get_end_date() == datetime(2016, 4, 29)
    assert new_name == '2016-04-RCN.pdf'


def disabled_test_factory():
    TESTDATA = (
        '1-800-RING-RCN (1-800-746-4726)Website:'
        'Statement Date:Account Number:Payment Due Date:1'
        'Statement Date:Account Number:Payment Due Date:01/31/20172301-'
    )

    extractor = ExtractorFactory.get_matching_extractor(TESTDATA)

    assert type(extractor) is RcnDateExtractor
