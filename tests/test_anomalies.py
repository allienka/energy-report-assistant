import pandas as pd
import pytest

from fastapi.testclient import TestClient
from backend.main import (
    app,
    create_comparison,
    detect_anomalies,
    get_anomalies
)



def test_cop_drop_is_detected():
    data = pd.DataFrame([
        {
            "Device": "Pump A",
            "Month": "2026-05",
            "COP": 3.5,
            "Alarms": 2
        },
        {
            "Device": "Pump A",
            "Month": "2026-06",
            "COP": 2.1,
            "Alarms": 2
        }
    ])

    comparison = create_comparison(data)

    cop_anomalies, alarm_anomalies = detect_anomalies(comparison)

    assert len(cop_anomalies) == 1
    assert cop_anomalies.iloc[0]["Device"] == "Pump A"
    assert cop_anomalies.iloc[0]["cop_change"] == -1.4
    
    
def test_alarm_increase_is_detected():
    data = pd.DataFrame([
            {
                "Device": "Pump C",
                "Month": "2026-05",
                "COP": 3.2,
                "Alarms": 10
            },
            {
                "Device": "Pump C",
                "Month": "2026-06",
                "COP": 3.2,
                "Alarms": 16
            }
        ])
    
    comparison = create_comparison(data)
    
    cop_anomalies, alarm_anomalies = detect_anomalies(comparison)
    
    assert len(alarm_anomalies) == 1
    assert alarm_anomalies.iloc[0]["Device"] == "Pump C"
    assert alarm_anomalies.iloc[0]["alarms_diff"] == 6
    
def test_small_cop_change_is_not_anomaly():
    data = pd.DataFrame([
        {
            "Device": "Pump A",
            "Month": "2026-05",
            "COP": 3.5,
            "Alarms": 2
        },
        {
            "Device": "Pump A",
            "Month": "2026-06",
            "COP": 3.1,
            "Alarms": 2
        }
    ])

    comparison = create_comparison(data)

    cop_anomalies, alarm_anomalies = detect_anomalies(comparison)

    assert len(cop_anomalies) == 0
    
def test_alarm_increase_at_threshold_is_not_anomaly():
    data = pd.DataFrame([
        {
            "Device": "Pump C",
            "Month": "2026-05",
            "COP": 3.2,
            "Alarms": 10
        },
        {
            "Device": "Pump C",
            "Month": "2026-06",
            "COP": 3.2,
            "Alarms": 15
        }
    ])

    comparison = create_comparison(data)

    cop_anomalies, alarm_anomalies = detect_anomalies(comparison)

    assert len(alarm_anomalies) == 0    

def test_one_month_is_not_enough_for_comparison():
    data = pd.DataFrame({
        "Month": ["June"],
        "Device": ["Pump A"],
        "Consumption_kWh": [1000],
        "COP": [3.5],
        "Alarms": [2]
    })

    with pytest.raises(ValueError):
        create_comparison(data)    

def test_multiple_anomalies_are_detected():
    data = pd.DataFrame({
        "Month": ["2026-05", "2026-05", "2026-06", "2026-06"],
        "Device": ["Pump A", "Pump B", "Pump A", "Pump B"],
        "Consumption_kWh": [1000, 1200, 1100, 1300],
        "COP": [3.5, 3.4, 2.1, 2.0],
        "Alarms": [2, 3, 2, 10]
    })

    comparison = create_comparison(data)
    cop_anomalies, alarm_anomalies = detect_anomalies(comparison)
    

    assert len(cop_anomalies) == 2
    assert len(alarm_anomalies) == 1
    assert alarm_anomalies.iloc[0]["Device"] == "Pump B"        
    
def test_ai_summary_endpoint(monkeypatch):
    fake_findings = [
        {
            "type": "cop_change",
            "device": "Pump C",
            "value": -1.2
        }
    ]

    def fake_get_anomalies():
        return fake_findings

    def fake_ask_ai(findings):
        return "Pump C shows a significant COP decrease."

    monkeypatch.setattr("backend.main.get_anomalies", fake_get_anomalies)
    monkeypatch.setattr("backend.main.ask_ai", fake_ask_ai)

    client = TestClient(app)

    response = client.get("/ai-summary")

    assert response.status_code == 200
    assert response.json()["summary"] == "Pump C shows a significant COP decrease."