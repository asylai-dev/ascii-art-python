from calculator import multiply

def test_multiply():
    assert multiply(6,8) == 48

def test_multiply_negative():
    assert multiply(-5, -5) == 25
    