from ryon.parser import RyonParser


def test_parser_initialization():
    RyonParser()


def test_parser_parse(parser, tests_data_dir):
    content = open(tests_data_dir / "foo.ry").read()
    parser.parse(content)
