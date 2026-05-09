from specforge.demo import MESSAGE, demo_output


def test_demo_contains_before_after_story():
    output = demo_output()
    assert MESSAGE in output
    assert "database model" in output
    assert "workflow ApproveSoftwareRequest" in output
    assert "Generated file plan:" in output
