# credit-card-analysis-dashboard
Interactive credit card analytics dashboard using Flask, Pandas, and Plotly


# Credit Card Analysis Dashboard

An interactive web-based dashboard built using Flask that analyzes credit card customer data and provides insights into spending behavior, repayment trends, customer segmentation, and product usage.

---

## Overview

This project allows users to upload an Excel dataset containing credit card transaction data and instantly visualize key metrics and insights through dynamic charts and summaries.

The dashboard is designed to simulate real-world financial analytics used in banking and fintech industries.

---

## Features

* Upload Excel dataset (.xlsx)
* Interactive dashboard with multiple tabs:

  * Customer Overview
  * Spending Insights
  * Repayment Trends
  * Spend vs Repay Analysis
  * Product Limits
* Summary metrics:

  * Total customers
  * Average age
  * Total and average credit limits
  * Total and average spending
  * Total and average repayment
* Auto-generated insights panel
* Clean, responsive UI with pastel theme
* Interactive charts powered by Plotly

---

## Tech Stack

* **Backend:** Flask (Python)
* **Data Processing:** Pandas
* **Visualization:** Plotly
* **Frontend:** HTML, CSS
* **Session Handling:** Flask-Session

---

## Project Structure

```
credit-card-analysis-dashboard/
│
├── app.py
├── templates/
│   └── index.html
├── static/
│   └── style.css
├── requirements.txt
├── README.md
```

---

## Installation & Setup

### 1. Clone the repository

```
git clone https://github.com/YOUR_USERNAME/credit-card-analysis-dashboard.git
cd credit-card-analysis-dashboard
```

### 2. Create virtual environment

```
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```
pip install -r requirements.txt
```

---

## Run the Application

```
python app.py
```

Open in browser:

```
http://127.0.0.1:61968
```

---

## Dataset Requirements

The uploaded Excel file must contain the following sheets:

* **Customer Acqusition**
* **Spend**
* **Repayment**

Each sheet should include relevant columns such as:

* Customer
* Age
* Limit
* Amount
* Month
* Segment
* City

---

## Key Functionalities

### Data Processing

* Reads Excel file using Pandas
* Cleans and standardizes column names
* Aggregates data for analysis

### Visualization

* Histograms, pie charts, bar graphs, line charts, scatter plots
* Styled using Plotly templates for consistency

### Dashboard Tabs

* Organized into multiple sections for better analysis
* Each tab focuses on a specific business insight

### Insights Generation

* Displays pre-defined analytical insights based on patterns in data

---

## Sample Insights

* Majority of customers fall in the 30–40 age group
* Spending and repayment trends are closely correlated
* Top cities contribute significantly to overall transactions
* High-value customers dominate spending patterns

---

## How It Works

1. User uploads Excel dataset
2. Data is stored temporarily using session
3. Backend processes and aggregates data
4. Plotly generates interactive charts
5. Dashboard renders insights and visuals

---

## Future Improvements

* Add real-time filtering options
* Export reports as PDF
* Add authentication system
* Deploy on cloud (AWS / Render)
* Add machine learning-based predictions

---

## Known Limitations

* Requires structured Excel format
* No real-time database integration
* Static insights (not dynamically generated)

---

## Author

**Janhvi Singh**

---

## License

This project is intended for educational and portfolio use.
