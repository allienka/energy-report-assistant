from backend.main import get_anomalies


def test_get_anomalies():
    findings = get_anomalies()

    assert isinstance(findings, list)

def test_no_anomalies():
    findings = get_anomalies()

    assert findings == []    