from main import get_start

def test_space_start():
    assert get_start(" ") == 0

def test_exclamation_start():
    assert get_start("!") == 9

def test_A_start():
    assert get_start("A") == 297

def test_zero_start():
    assert get_start("0") == 144