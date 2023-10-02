from hlr.parser.context_log_parser import parse_context_log
from hlr.parser.hlr_parser import (HlrParserType, InfobipHlrHlrParser, MsisdnInfo,
                                   TmtHlrHlrParser, XconnectHlrParser,
                                   XconnectMnpParser, create_parser)

import pytest

HLR_PARSERS = [
    (HlrParserType.XCONNECT_HLR, XconnectHlrParser),
    (HlrParserType.XCONNECT_MNP, XconnectMnpParser),
    (HlrParserType.INFOBIP_HLR, InfobipHlrHlrParser),
    (HlrParserType.TMT_HLR, TmtHlrHlrParser),
]


@pytest.mark.parametrize('provider_type,parser', HLR_PARSERS)
def test__create_parser__return_correct_parser_depends_on_passed_provider_type(provider_type, parser):
    assert isinstance(create_parser(provider_type), parser)


def test__get_msisdn_info__for_tmt_parser_return_MsisdnInfo_instance(tmt_context_log):
    raw_response = parse_context_log(tmt_context_log)
    parser = create_parser(HlrParserType.TMT_HLR)

    assert isinstance(parser.get_msisdn_info(raw_response), MsisdnInfo)


def test__get_msisdn_info__for_infobip_parser_return_MsisdnInfo_instance(infobip_context_log):
    raw_response = parse_context_log(infobip_context_log)
    parser = create_parser(HlrParserType.INFOBIP_HLR)

    assert isinstance(parser.get_msisdn_info(raw_response), MsisdnInfo)


def test__get_msisdn_info__for_xconnect_hlr_parser_return_MsisdnInfo_instance(xconnect_hlr_context_log):
    raw_response = parse_context_log(xconnect_hlr_context_log)
    parser = create_parser(HlrParserType.XCONNECT_HLR)

    assert isinstance(parser.get_msisdn_info(raw_response), MsisdnInfo)


def test__get_msisdn_info__for_xconnect_mnp_parser_return_msisdninfo_instance(xconnect_mnp_context_log):
    raw_response = parse_context_log(xconnect_mnp_context_log)
    parser = create_parser(HlrParserType.XCONNECT_MNP)

    assert isinstance(parser.get_msisdn_info(raw_response), MsisdnInfo)
