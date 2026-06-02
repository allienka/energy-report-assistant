from fastapi import FastAPI
import pandas as pd



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