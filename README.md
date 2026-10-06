# Energy Report Assistant

AI-powered application for analyzing monthly energy reports, detecting anomalies, and generating professional summaries.

## What the project does

The application analyzes energy data from CSV reports and:

- Compares the latest two months automatically
- Calculates changes in energy consumption, COP, and alarms
- Detects significant COP changes and increases in alarms
- Provides monthly comparison results through a REST API
- Generates AI-powered summaries of detected anomalies
- Handles cases where no significant anomalies are detected

## Architecture

```text
CSV report
    ↓
Pandas
    ↓
Monthly comparison
    ↓
Anomaly detection
    ↓
Findings
    ↓
OpenAI
    ↓
AI-generated summary
    ↓
FastAPI

Technology Stack
Python
Pandas
FastAPI
OpenAI API
Pytest
REST API
Git & GitHub
API Endpoints
Endpoint	Description
/	Basic application information
/health	Health check
/report-summary	Summary statistics from the report
/monthly-comparison	Comparison between the latest two months
/anomalies	Detected anomalies
/ai-summary	AI-generated summary of detected anomalies
Anomaly Detection

The application currently detects:

Significant COP changes
Significant increases in alarm counts

The thresholds are defined as named configuration values in the application, making them easy to adjust.

Testing

The project includes automated tests covering:

COP anomaly detection
Alarm anomaly detection
Threshold boundaries
Insufficient data
Multiple simultaneous anomalies
AI summary with findings
AI summary with no findings

Run the tests with:

python -m pytest

Current test status:

8 passed
Project Structure
energy-report-assistant/
│
├── backend/
│   ├── main.py
│   ├── ai.py
│   └── __init__.py
│
├── data/
│   └── sample_report.csv
│
├── notebooks/
│   └── analysis.ipynb
│
├── tests/
│   └── test_anomalies.py
│
├── .gitignore
├── README.md
└── requirements.txt
Running the Application

Install the dependencies:

pip install -r requirements.txt

Create a .env file and add your OpenAI API key:

OPENAI_API_KEY=your_api_key_here

Start the FastAPI application:

uvicorn backend.main:app --reload

The API will be available at:

http://127.0.0.1:8000

Interactive API documentation is available at:

http://127.0.0.1:8000/docs
Future Improvements

Possible future improvements include:

Support for Excel reports
Automated report ingestion
Additional anomaly detection methods
Azure deployment
More advanced data pipelines
Natural-language questions about report data

