from specforge.parser import parse_text
from specforge.validate import validate_spec


def messages(text: str) -> list[str]:
    return [error.message for error in validate_spec(parse_text(text))]


def test_validator_catches_duplicate_models():
    errors = messages("app Demo\nmodel Task\nmodel Task\n")
    assert any("duplicate model" in error for error in errors)


def test_validator_catches_duplicate_fields():
    errors = messages("app Demo\nmodel Task\n  title text required\n  title text optional\n")
    assert any("duplicate field" in error for error in errors)


def test_validator_catches_unknown_field_types():
    errors = messages("app Demo\nmodel Task\n  title string required\n")
    assert any("unknown type" in error for error in errors)


def test_validator_catches_missing_ref_target():
    errors = messages("app Demo\nmodel Task\n  owner ref Person required\n")
    assert any("references missing model" in error for error in errors)


def test_validator_catches_invalid_enum_syntax():
    errors = messages("app Demo\nmodel Task\n  status enum done\n")
    assert any("enum" in error for error in errors)


def test_validator_catches_missing_app_declaration():
    errors = messages("model Task\n  title text required\n")
    assert any("missing app declaration" in error for error in errors)
