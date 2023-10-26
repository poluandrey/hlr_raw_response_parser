import pytest

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


def test__get_msisdn_info__for_tmt_hlr_parser_return_correct_msisdn(tmt_hlr_parser, make_tmt_hlr_response):
    raw_response = make_tmt_hlr_response(msisdn='79216503431')

    msisdn_info = tmt_hlr_parser.get_msisdn_info(raw_response)

    assert msisdn_info.msisdn == '79216503431'


def test__get_msisdn_info__for_tmt_hlr_parser_return_correct_mccmnc(tmt_hlr_parser, make_tmt_hlr_response):
    raw_response = make_tmt_hlr_response(mcc='250', mnc='01')

    msisdn_info = tmt_hlr_parser.get_msisdn_info(raw_response)

    assert msisdn_info.mccmnc == '250001'


@pytest.mark.parametrize('hlr_present_resp, present', [('yes', True), ('no', False), ('na', None)])
def test__get_msisdn_info__for_tmt_hlr_parser_return_correct_present(tmt_hlr_parser,
                                                                     make_tmt_hlr_response,
                                                                     hlr_present_resp, present
                                                                     ):
    raw_response = make_tmt_hlr_response(presents=hlr_present_resp)

    msisdn_info = tmt_hlr_parser.get_msisdn_info(raw_response)

    assert msisdn_info.presents == present


@pytest.mark.parametrize('hlr_ported_resp, ported', [('true', True), ('false', False)])
def test__get_msisdn_info__for_tmt_hlr_parser_return_correct_ported(tmt_hlr_parser,
                                                                    make_tmt_hlr_response,
                                                                    hlr_ported_resp, ported
                                                                    ):
    raw_response = make_tmt_hlr_response(ported=hlr_ported_resp)

    msisdn_info = tmt_hlr_parser.get_msisdn_info(raw_response)

    assert msisdn_info.ported == ported


def test__get_msisdn_info__for_infobip_parser_return_correct_msisdn(infobip_hrl_parser,
                                                                    make_infobip_hlr_response
                                                                    ):
    raw_response = make_infobip_hlr_response(msisdn='79216503431')

    msisdn_info = infobip_hrl_parser.get_msisdn_info(raw_response)

    assert msisdn_info.msisdn == '79216503431'


@pytest.mark.parametrize('hlr_ported_resp, ported', [('true', 1), ('false', 0)])
def test__get_msisdn_info__for_infobip_parser_return_correct_ported(
        infobip_hrl_parser,
        make_infobip_hlr_response,
        hlr_ported_resp,
        ported,
):
    raw_response = make_infobip_hlr_response(ported=hlr_ported_resp)

    msisdn_info = infobip_hrl_parser.get_msisdn_info(raw_response)

    assert msisdn_info.ported == ported


def test__get_msisdn_info__for_infobip_parser_return_correct_mccmnc(infobip_hrl_parser, make_infobip_hlr_response):
    raw_response = make_infobip_hlr_response(mccmnc='25001')

    msisdn_info = infobip_hrl_parser.get_msisdn_info(raw_response)

    assert msisdn_info.mccmnc == '250001'


def test__get_msisdn_info__for_xconnect_hlr_return_correct_msisdn(xconnect_hlr_parser, make_xconnect_hlr_response):
    raw_response = make_xconnect_hlr_response(msisdn='79216503431')

    msisdn_info = xconnect_hlr_parser.get_msisdn_info(raw_response)

    assert msisdn_info.msisdn == '79216503431'


def test__get_msisdn__for_xconnect_hlr_return_correct_mccmnc(xconnect_hlr_parser, make_xconnect_hlr_response):
    raw_response = make_xconnect_hlr_response(mcc='250', mnc='01')

    msisdn_info = xconnect_hlr_parser.get_msisdn_info(raw_response)

    assert msisdn_info.mccmnc == '250001'


@pytest.mark.parametrize('hlr_ported_resp, ported', [('false', 0), ('true', 1)])
def test__get_msisdn_info__for_xconnect_hlr_return_correct_ported(xconnect_hlr_parser,
                                                                  make_xconnect_hlr_response,
                                                                  hlr_ported_resp, ported):
    raw_response = make_xconnect_hlr_response(ported=hlr_ported_resp)

    msisdn_info = xconnect_hlr_parser.get_msisdn_info(raw_response)

    assert msisdn_info.ported == ported


@pytest.mark.parametrize('hlr_present_resp,presents', [
    ('000', True),
    ('001', False),
    ('002', False),
    ('003', False),
    ('004', None),

])
def test__get_msisdn_info__for_xconnect_hlr_return_correct_present(
        xconnect_hlr_parser,
        make_xconnect_hlr_response,
        hlr_present_resp,
        presents):
    raw_response = make_xconnect_hlr_response(presents=hlr_present_resp)

    msisdn_info = xconnect_hlr_parser.get_msisdn_info(raw_response)

    assert msisdn_info.presents == presents


def test__get_msisdn_info__for_xconnect_mnp_return_correct_msisdn(xconnect_mnp_parser, make_xconnect_mnp_response):
    raw_response = make_xconnect_mnp_response(msisdn='79216503431')

    msisdn_info = xconnect_mnp_parser.get_msisdn_info(raw_response)

    assert msisdn_info.msisdn == '79216503431'


def test__get_msisdn_info__for_xconnect_mnp_return_correct_mccmnc(xconnect_mnp_parser, make_xconnect_mnp_response):
    raw_response = make_xconnect_mnp_response(mcc='240', mnc='01')

    msisdn_info = xconnect_mnp_parser.get_msisdn_info(raw_response)

    assert msisdn_info.mccmnc == '240001'


@pytest.mark.parametrize('hlr_ported_resp, ported', [
    ('true', True),
    ('false', False),
])
def test__get_msisdn_info__fir_xconnect_mnp_return_correct_ported(
        xconnect_mnp_parser,
        make_xconnect_mnp_response,
        hlr_ported_resp,
        ported):
    raw_response = make_xconnect_mnp_response(ported=hlr_ported_resp)

    msisdn_info = xconnect_mnp_parser.get_msisdn_info(raw_response)

    assert msisdn_info.ported == ported
