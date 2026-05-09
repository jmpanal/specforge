from specforge.privacy import scan


def test_privacy_scan_finds_suspicious_match(tmp_path):
    path = tmp_path / "sample.txt"
    path.write_text("api_key = value\n", encoding="utf-8")
    matches = scan(tmp_path)
    assert matches
    assert matches[0][1] == 1
