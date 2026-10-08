# Energy Consumption Management & Analysis System

## 1. Project Objective

Develop a Python application that maintains energy-use records and provides useful
consumption analysis.

## 2. Functional Requirements Covered

- Record energy observations.
- Search/filter records by appliance and month.
- Calculate total consumption, average consumption and total cost.
- Compare appliances.
- Compare categories.
- Compare monthly periods.
- Identify high-usage patterns.
- Generate at least two meaningful visual reports.
- Store records permanently in a CSV file.
- GUI created using Tkinter.
- Input validation and exception handling.
- Uses NumPy and Pandas for analysis.
- Uses Matplotlib for visual reports.

## 3. User-Defined Modules

The project contains more than the required 3 modules:

1. `data_manager.py` - file storage, validation and filtering.
2. `analysis.py` - calculations and comparisons.
3. `reports.py` - Matplotlib visual reports.
4. `main.py` - Tkinter GUI and application control.

## 4. Installation

Open the project folder in VS Code terminal and run:

```bash
pip install -r requirements.txt
```

## 5. Run

```bash
python main.py
```

## 6. Project Structure

```text
Energy_Consumption_Analysis_Project/
│
├── main.py
├── data_manager.py
├── analysis.py
├── reports.py
├── requirements.txt
├── README.md
│
├── data/
│   └── energy_records.csv
│
├── reports/
│   └── generated PNG reports
│
└── tests/
    └── test_energy.py
```

## 7. Reports

The program creates:

- `reports/appliance_consumption.png`
- `reports/monthly_consumption_trend.png`

## 8. Data Storage

The application uses CSV file handling. New observations are appended to
`data/energy_records.csv`, so data remains available after the program closes.

## 9. Validation

The program checks:

- Empty appliance/category
- Correct date format
- Numeric units and cost
- Non-negative units
- Non-negative cost

Invalid input is reported using a custom `EnergyValidationError` and Tkinter
exception messages.

## 10. Testing

Run:

```bash
python -m unittest discover -s tests -v
```

## 11. Example Analysis

The dashboard displays:

- Total energy consumption in kWh
- Average energy consumption
- Total cost
- Highest-use appliance

The high-usage feature finds observations above the overall average.

## 12. Documentation / Testing Notes

This project is designed for an academic practical/project submission.
The code is separated into modules so that data handling, analysis, reports,
and GUI logic are easier to understand and test.
