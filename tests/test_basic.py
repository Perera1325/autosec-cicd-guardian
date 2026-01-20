from src.app import calculate_risk_score

def test_risk_score_bounds():
    score = calculate_risk_score(10, 10, True)
    assert 0 <= score <= 100

def test_risk_score_logic():
    score = calculate_risk_score(1, 0, False)
    assert score == 30
