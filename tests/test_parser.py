from pathlib import Path

from specforge.parser import parse_file, parse_text


ROOT = Path(__file__).resolve().parents[1]


def test_parser_parses_all_examples():
    for path in ROOT.glob("examples/*/.specforge/app.appspec"):
        spec = parse_file(path)
        assert spec.app_name
        assert not spec.parse_errors


def test_parser_preserves_line_numbers():
    spec = parse_text("app Demo\n\nmodel Task\n  title text required\n")
    assert spec.models[0].line == 3
    assert spec.models[0].fields[0].line == 4


def test_parser_reports_invalid_indentation():
    spec = parse_text("app Demo\nmodel Task\n title text required\n")
    assert spec.parse_errors
    assert "invalid indentation" in spec.parse_errors[0].message
