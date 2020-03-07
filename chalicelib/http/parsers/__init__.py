from chalicelib import helper


def request_parser(app):
    logger = helper.get_logger()
    from chalicelib.http.parsers.chalice_request_parser import ChaliceRequestParser
    parser = ChaliceRequestParser(logger)
    request = app.current_request

    parser.set_request(request)
    return parser
