def test_check_HDL_Normal():
    from blood_calculator import check_HDL
    answer = check_HDL(85)
    expected = "Normal"
    assert answer == expected
    
def test_check_HDL_BorderlineLow():
    from blood_calculator import check_HDL
    answer = check_HDL(45)
    expected = "Borderline Low"
    assert answer == expected
    
def test_check_Low():
    from blood_calculator import check_HDL
    answer = check_HDL(25)
    expected = "Low"
    assert answer == expected