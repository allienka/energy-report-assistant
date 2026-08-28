from fastapi import FastAPI
import pandas as pd
from backend.ai import ask_ai




app = FastAPI(
    title="Energy Report Assistant",
    description="AI-powered platform for energy and operational report analysis",
    version="0.1.0"
)


@app.get("/")
def root():
    return {
        "project": "Energy Report Assistant",
        "status": "running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }

@app.get("/report-summary")
def report_summary():
    df = pd.read_csv("data/sample_report.csv")

    return {
        "total_consumption": int(df["Consumption_kWh"].sum()),
        "highest_consumer": df.loc[
            df["Consumption_kWh"].idxmax(),
            "Device"
        ],
        "average_cop": round(df["COP"].mean(), 2),
        "total_alarms": int(df["Alarms"].sum())
    }  
def create_comparison(df):
    
    months = sorted(df["Month"].unique())

    if len(months) < 2:
        raise ValueError("At least two months are needed for comparison")

    previous_month = months[-2]
    latest_month = months[-1]

    previous = df[df["Month"] == previous_month]
    latest = df[df["Month"] == latest_month]

    comparison = previous.merge(
        latest,
        on="Device",
        suffixes=("_previous", "_latest")
    )

    return comparison

@app.get("/monthly-comparison")
def monthly_comparison():
    df = pd.read_csv("data/sample_report.csv")
    comparison = create_comparison()

    # Calculate changes
    comparison["consumption_change"] = (
        comparison["Consumption_kWh_latest"]
        - comparison["Consumption_kWh_previous"]
    )

    comparison["cop_change"] = (
        comparison["COP_latest"]
        - comparison["COP_previous"]
    )

    # Largest consumption increase
    largest_increase = comparison.loc[
        comparison["consumption_change"].idxmax()
    ]

    # Largest COP drop
    largest_cop_drop = comparison.loc[
        comparison["cop_change"].idxmin()
    ]

    # Most alarms
    df["TotalAlarms"] = df.groupby("Device")["Alarms"].transform("sum")

    most_alarms = df.loc[
        df["TotalAlarms"].idxmax()
    ]

    return {
        "largest_consumption_increase": {
            "device": largest_increase["Device"],
            "increase_kwh": int(
                largest_increase["consumption_change"]
            )
        },
        "largest_cop_drop": {
            "device": largest_cop_drop["Device"],
            "drop": round(
                abs(largest_cop_drop["cop_change"]),
                2
            )
        },
        "most_alarms": {
            "device": most_alarms["Device"],
            "alarms": int(
                most_alarms["TotalAlarms"]
            )
        }
    }
def detect_anomalies(comparison):

    comparison["cop_change"] = (
        comparison["COP_latest"]
        - comparison["COP_previous"]
    )

    comparison["alarms_diff"] = (
        comparison["Alarms_latest"]
        - comparison["Alarms_previous"]
    )

    cop_anomalies = comparison[
        abs(comparison["cop_change"]) > 1
    ]

    alarm_anomalies = comparison[
        comparison["alarms_diff"] > 5
    ]

    return cop_anomalies, alarm_anomalies

def get_anomalies():
    
    df = pd.read_csv("data/sample_report.csv")
    comparison = create_comparison(df)
    cop_anomalies, alarm_anomalies = detect_anomalies(comparison)
    
    findings = []
    
    for index, row in cop_anomalies.iterrows():
            findings.append({
                "type": "cop_change",
                "device": row["Device"],
                "value": round(row["cop_change"], 2)
            })
    
    for index, row in alarm_anomalies.iterrows():
            findings.append({
                "type": "alarm_increase",
                "device": row["Device"],
                "value": int(row["alarms_diff"])
            })
    
    return findings     
        
       
@app.get("/anomalies")
def anomalies():
    findings=get_anomalies()
    
    return {
        "findings": findings
    }
    
@app.get("/ai-summary")
def ai_summary():
    findings = get_anomalies()
    if not findings:
        return {"summary": "No significant anomalies detected."}
    
    summary = ask_ai(findings)

    return {
        "summary": summary
    }