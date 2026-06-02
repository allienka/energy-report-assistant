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

@app.get("/monthly-comparison")
def monthly_comparison():
    df = pd.read_csv("data/sample_report.csv")

    # Split data by month
    may = df[df["Month"] == "2026-05"]
    june = df[df["Month"] == "2026-06"]

    # Join months by device
    comparison = may.merge(
        june,
        on="Device",
        suffixes=("_may", "_june")
    )

    # Calculate changes
    comparison["consumption_change"] = (
        comparison["Consumption_kWh_june"]
        - comparison["Consumption_kWh_may"]
    )

    comparison["cop_change"] = (
        comparison["COP_june"]
        - comparison["COP_may"]
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