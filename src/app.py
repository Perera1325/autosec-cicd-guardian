def calculate_risk_score(secrets_found: int, vuln_count: int, workflow_risky: bool) -> int:
    """
    Simple Day-1 risk score formula (will evolve later with AI).
    """
    score = 0
    score += secrets_found * 30
    score += vuln_count * 10
    if workflow_risky:
        score += 25

    # clamp 0..100
    return max(0, min(100, score))


if __name__ == "__main__":
    # Example run
    print("AutoSec CI/CD Guardian - Day 1 running ✅")
    print("Sample risk score:", calculate_risk_score(1, 2, True))
