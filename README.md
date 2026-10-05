# Global Seismic Trends: Data-Driven Earthquake Insights

## 📌 Project Overview

**Global Seismic Trends: Data-Driven Earthquake Insights** is a data analytics project that analyzes global earthquake activity using data collected from the **USGS Earthquake API**.

The project uses **Python, Pandas, MySQL, SQL, and Streamlit** to collect, clean, store, analyze, and visualize earthquake data from approximately the past five years.

The main objective is to identify earthquake patterns and trends based on magnitude, depth, location, time, seismic networks, tsunami indicators, and other available earthquake characteristics.

---

## 🎯 Objectives

* Collect global earthquake data from the USGS Earthquake API.
* Clean and preprocess the raw earthquake dataset using Python and Pandas.
* Handle missing values, duplicate records, timestamps, and data types.
* Extract geographical information such as region and country.
* Create derived analytical features.
* Store the cleaned dataset in MySQL.
* Perform analytical queries using SQL.
* Build an interactive Streamlit dashboard.
* Identify patterns and trends in global seismic activity.

---

## 🛠️ Technologies Used

* **Python**
* **Pandas**
* **NumPy**
* **Regular Expressions (Regex)**
* **MySQL**
* **SQL**
* **Streamlit**
* **Plotly**
* **Google Colab**
* **USGS Earthquake API**

---

## 🔄 Project Workflow

```text
USGS Earthquake API
        ↓
Data Collection
        ↓
Google Colab
        ↓
Python + Pandas
        ↓
Data Cleaning & Preprocessing
        ↓
Feature Engineering
        ↓
Cleaned Dataset
        ↓
MySQL Database
        ↓
SQL Analysis
        ↓
Streamlit Dashboard
        ↓
Interactive Earthquake Insights
```

---

## 📊 Dataset

The dataset was collected from the **United States Geological Survey (USGS) Earthquake API**.

The cleaned dataset contains approximately:

* **136,973 earthquake records**
* **34 columns**
* **26 original USGS features**
* **8 derived features**

### Original Features

The dataset includes fields such as:

* `id`
* `time`
* `updated`
* `latitude`
* `longitude`
* `depth_km`
* `mag`
* `magType`
* `place`
* `status`
* `tsunami`
* `sig`
* `net`
* `nst`
* `dmin`
* `rms`
* `gap`
* `magError`
* `depthError`
* `magNst`
* `locationSource`
* `magSource`
* `types`
* `ids`
* `sources`
* `type`

### Derived Features

The following features were created during preprocessing:

* `region`
* `country`
* `year`
* `month`
* `day`
* `day_of_week`
* `depth_category`
* `strong_earthquake`

### Depth Classification

Earthquakes were categorized based on depth:

| Depth                 | Category     |
| --------------------- | ------------ |
| ≤ 300 km              | Shallow      |
| > 300 km and ≤ 600 km | Intermediate |
| > 600 km              | Deep         |

### Strong Earthquake Definition

For this project, an earthquake with:

```text
Magnitude >= 6.0
```

is classified as a **strong earthquake**.

---

## 🧹 Data Preprocessing

The data preprocessing stage was performed using Python and Pandas in Google Colab.

The major preprocessing steps included:

1. Retrieving earthquake records from the USGS API.
2. Converting API data into a Pandas DataFrame.
3. Converting timestamps into datetime format.
4. Checking and removing duplicate earthquake IDs.
5. Converting numerical fields to appropriate numeric types.
6. Cleaning text fields.
7. Handling missing values.
8. Extracting region and country information from the `place` field.
9. Creating year, month, day, and weekday features.
10. Creating earthquake depth categories.
11. Creating the strong earthquake indicator.
12. Validating the final dataset.
13. Saving the cleaned dataset.

---

## 🗄️ MySQL Database

The cleaned earthquake dataset was stored in a MySQL database named:

```text
earthquake_db
```

The main table is:

```text
earthquakes
```

The table contains the original USGS features together with the derived analytical features.

---

## 🔎 SQL Analysis

SQL was used to perform analytical exploration of the earthquake dataset.

The SQL queries are provided in:

```text
earthquake_analysis.sql
```

The analysis includes tasks such as:

* Top 10 strongest earthquakes
* Top 10 deepest earthquakes
* Shallow earthquakes with high magnitude
* Average magnitude by magnitude type
* Earthquake counts by year
* Earthquake counts by month
* Earthquake counts by weekday
* Earthquake counts by hour
* Most active seismic networks
* Reviewed vs automatic events
* Event type distribution
* USGS data/product type distribution
* High station coverage events
* Tsunami events by year
* Top countries by average magnitude
* Countries with both shallow and deep earthquakes
* Year-over-year earthquake growth
* Regional activity score
* Earthquakes near the equator
* Shallow/deep earthquake ratio
* Tsunami vs non-tsunami average magnitude
* Reliability indicator using GAP and RMS
* Consecutive earthquake events within distance/time limits
* Deep-focus earthquake regions

---

## 📈 Streamlit Dashboard

An interactive dashboard was developed using **Streamlit** and **Plotly**.

The dashboard provides sections for:

* Overview
* Strength & Depth
* Time Analysis
* Geographic Analysis
* Magnitude Analysis
* Network & Data Quality
* Event Analysis
* Earthquake Map
* Detailed Data

The dashboard allows users to explore earthquake records through interactive filters and visualizations.

### Live Dashboard

**Streamlit App:**

https://global-seismic-trends-adl8zmhyisodpvswxvbyew.streamlit.app/

---

## 📁 Repository Structure

```text
Global-Seismic-Trends/
│
├── app.py
├── requirements.txt
├── global_earthquake_cleaned.csv.gz
├── earthquake_analysis.sql
└── README.md
```

### File Description

| File                               | Description                                       |
| ---------------------------------- | ------------------------------------------------- |
| `app.py`                           | Streamlit dashboard application                   |
| `requirements.txt`                 | Python dependencies required to run the dashboard |
| `global_earthquake_cleaned.csv.gz` | Compressed cleaned earthquake dataset             |
| `earthquake_analysis.sql`          | SQL analytical queries                            |
| `README.md`                        | Project documentation                             |

---

## ▶️ How to Run the Streamlit Dashboard

### 1. Clone the repository

```bash
git clone https://github.com/Dinesh04gv/Global-Seismic-Trends.git
```

### 2. Open the project folder

```bash
cd Global-Seismic-Trends
```

### 3. Install the required packages

```bash
pip install -r requirements.txt
```

### 4. Run the Streamlit application

```bash
streamlit run app.py
```

The application will open in the browser.

---

## ⚠️ Data Limitations

Some analyst tasks require information such as:

* Casualties/fatalities
* Economic loss
* Alert level
* Continent

These fields are not included in the current USGS dataset used for this project. Therefore, those specific analyses cannot be calculated accurately without additional data sources.

The `country` and `region` fields were derived from the USGS `place` field and may not perfectly represent every event location.

The `tsunami` field represents the USGS tsunami indicator associated with the earthquake record and should not automatically be interpreted as confirmation of a damaging tsunami.

The `activity_score` and GAP/RMS reliability indicator used in this project are project-defined analytical metrics and are not official USGS hazard or reliability scores.

---

## 👩‍💻 Project Skills Demonstrated

This project demonstrates practical skills in:

* Data Collection
* REST API usage
* Python
* Pandas
* Data Cleaning
* Regex
* Feature Engineering
* SQL
* MySQL
* Data Analysis
* Data Visualization
* Streamlit Dashboard Development
* Exploratory Data Analysis

---

## 📌 Conclusion

The project provides a data-driven approach to understanding global seismic activity. By combining Python-based preprocessing, MySQL database storage, SQL analytics, and interactive Streamlit visualization, the system helps identify patterns in earthquake magnitude, depth, geographic distribution, temporal trends, seismic networks, and other earthquake characteristics.
