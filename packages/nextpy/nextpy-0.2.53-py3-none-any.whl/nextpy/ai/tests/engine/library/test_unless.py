from nextpy.ai import engine
import pytest

@pytest.mark.parametrize("flag, expected_output", [
    (True, "Answer: "),
    (1, "Answer: "),
    ("random text", "Answer: "),
    (False, "Answer: Yes"),
    (0, "Answer: Yes"),
    ("", "Answer: Yes")
])
def test_unless(flag, expected_output):
    """ Test the behavior of `unless`.
    """

    program = engine("""Answer: {{#unless flag}}Yes{{/unless}}""")
    out = program(flag=flag)
    assert str(out) == expected_output
