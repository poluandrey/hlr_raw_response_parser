import pytest

from hlr.parser.context_log_parser import parse_context_log
from hlr.parser.hlr_parser import (HlrParserType, InfobipHlrHlrParser,
                                   TmtHlrHlrParser,
                                   XconnectHlrParser, XconnectMnpParser,
                                   create_parser)

HLR_PARSERS = [
    (HlrParserType.XCONNECT_HLR, XconnectHlrParser),
    (HlrParserType.XCONNECT_MNP, XconnectMnpParser),
    (HlrParserType.INFOBIP_HLR, InfobipHlrHlrParser),
    (HlrParserType.TMT_HLR, TmtHlrHlrParser),
]


@pytest.mark.parametrize('provider_type,parser', HLR_PARSERS)
def test__create_parser__return_correct_parser_depends_on_passed_provider_type(provider_type, parser):
    assert isinstance(create_parser(provider_type), parser)


def test__get_msisdn_info__for_tmt_hlr_parser_return_correct_msisdn(mare_nested_context_log_tmt_hlr):
    raw_response = parse_context_log(mare_nested_context_log_tmt_hlr(msisdn=79216503431))
    parser = create_parser(HlrParserType.TMT_HLR)
    msisdn_info = parser.get_msisdn_info(raw_response)

    assert msisdn_info.msisdn == '79216503431'


def test__get_msisdn_info__for_tmt_hlr_parser_return_correct_mccmnc(mare_nested_context_log_tmt_hlr):
    raw_response = parse_context_log(mare_nested_context_log_tmt_hlr(mcc='250', mnc='01'))
    parser = create_parser(HlrParserType.TMT_HLR)
    msisdn_info = parser.get_msisdn_info(raw_response)

    assert msisdn_info.mccmnc == '250001'


def test__get_msisdn_info__for_tmt_parser_return_correct_present(mare_nested_context_log_tmt_hlr):
    raw_response = parse_context_log(mare_nested_context_log_tmt_hlr(present='yes'))
    parser = create_parser(HlrParserType.TMT_HLR)
    msisdn_info = parser.get_msisdn_info(raw_response)

    assert msisdn_info.presents == 'yes'


def test__get_msisdn_info__for_tmt_parser_return_correct_ported(mare_nested_context_log_tmt_hlr):
    raw_response = parse_context_log(mare_nested_context_log_tmt_hlr(ported='N/A'))
    parser = create_parser(HlrParserType.TMT_HLR)
    msisdn_info = parser.get_msisdn_info(raw_response)

    assert msisdn_info.ported == 'N/A'


def test__get_msisdn_info__for_infobip_parser_return_correct_msisdn(make_nested_context_log_infobip_hlr):
    raw_response = parse_context_log(make_nested_context_log_infobip_hlr(msisdn='79216503431'))
    parser = create_parser(HlrParserType.INFOBIP_HLR)
    msisdn_info = parser.get_msisdn_info(raw_response)

    assert msisdn_info.msisdn == '79216503431'


@pytest.mark.parametrize('hlr_ported_resp, ported', [('true', 1), ('false', 0)])
def test__get_msisdn_info__for_infobip_parser_return_correct_ported(
        make_nested_context_log_infobip_hlr,
        hlr_ported_resp,
        ported,
):
    raw_response = parse_context_log(make_nested_context_log_infobip_hlr(ported=hlr_ported_resp))
    parser = create_parser(HlrParserType.INFOBIP_HLR)
    msisdn_info = parser.get_msisdn_info(raw_response)

    assert msisdn_info.ported == ported


def test__get_msisdn_info__for_infobip_parser_return_correct_mccmnc(make_nested_context_log_infobip_hlr):
    raw_response = parse_context_log(make_nested_context_log_infobip_hlr(mccmnc='25001'))
    parser = create_parser(HlrParserType.INFOBIP_HLR)
    msisdn_info = parser.get_msisdn_info(raw_response)

    assert msisdn_info.mccmnc == '250001'


def test__get_msisdn_info__for_xconnect_hlr_return_correct_msisdn(make_nested_context_log_xconnect_hlr):
    raw_response = parse_context_log(make_nested_context_log_xconnect_hlr(msisdn='79216503431'))
    parser = create_parser(HlrParserType.XCONNECT_HLR)
    msisdn_info = parser.get_msisdn_info(raw_response)

    assert msisdn_info.msisdn == '79216503431'


def test__get_msisdn__for_xconnect_hlr_return_correct_mccmnc(make_nested_context_log_xconnect_hlr):
    raw_response = parse_context_log(make_nested_context_log_xconnect_hlr(mcc='250', mnc='01'))
    parser = create_parser(HlrParserType.XCONNECT_HLR)
    msisdn_info = parser.get_msisdn_info(raw_response)

    assert msisdn_info.mccmnc == '250001'


@pytest.mark.parametrize('hlr_ported_resp, ported', [('false', 0), ('true', 1), ])
def test__get_msisdn_info__for_xconnect_hlr_return_correct_ported(make_nested_context_log_xconnect_hlr, hlr_ported_resp, ported):
    raw_response = parse_context_log(make_nested_context_log_xconnect_hlr(ported=hlr_ported_resp))
    parser = create_parser(HlrParserType.XCONNECT_HLR)
    msisdn_info = parser.get_msisdn_info(raw_response)

    assert msisdn_info.ported == ported


@pytest.mark.parametrize('hlr_present_resp,presents', [
    ('000', 'yes'),
    ('001', 'no'),
    ('002', 'no'),
    ('003', 'no'),
    ('004', 'no answer'),

])
def test__get_msisdn_info__for_xconnect_hlr_return_correct_present(make_nested_context_log_xconnect_hlr,
                                                                   hlr_present_resp,
                                                                   presents):
    context_log = parse_context_log(make_nested_context_log_xconnect_hlr(presents=hlr_present_resp))
    parser = create_parser(HlrParserType.XCONNECT_HLR)
    msisdn_info = parser.get_msisdn_info(context_log)

    assert msisdn_info.presents == presents


def test__get_msisdn_info__for_xconnect_mnp_return_correct_msisdn(make_nested_context_log_xconnect_mnp):
    raw_response = parse_context_log(make_nested_context_log_xconnect_mnp(msisdn='79216503431'))
    parser = create_parser(HlrParserType.XCONNECT_MNP)
    msisdn_info = parser.get_msisdn_info(raw_response)

    assert msisdn_info.msisdn == '79216503431'


def test__get_msisdn_info__for_xconnect_mnp_return_correct_mccmnc(make_nested_context_log_xconnect_mnp):
    raw_response = parse_context_log(make_nested_context_log_xconnect_mnp(mcc='240', mnc='01'))
    parser = create_parser(HlrParserType.XCONNECT_MNP)
    msisdn_info = parser.get_msisdn_info(raw_response)

    assert msisdn_info.mccmnc == '240001'


@pytest.mark.parametrize('hlr_ported_resp, ported', [
    ('true', 'yes'),
    ('false', 'no'),
])
def test__get_msisdn_info__fir_xconnect_mnp_return_correct_ported(make_nested_context_log_xconnect_mnp,
                                                                  hlr_ported_resp,
                                                                  ported):
    raw_response = parse_context_log(make_nested_context_log_xconnect_mnp(ported=hlr_ported_resp))
    parser = create_parser(HlrParserType.XCONNECT_MNP)
    msisdn_info = parser.get_msisdn_info(raw_response)

    assert msisdn_info.ported == ported
