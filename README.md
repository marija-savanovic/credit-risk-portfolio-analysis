# Credit Risk Portfolio Analysis & Default Prediction

An end-to-end credit risk analysis project using **Python, SQL, SQLite, and logistic regression** to explore portfolio risk, identify higher-risk borrower segments, and estimate default probability.

## Project Overview

This project analyzes a simulated consumer credit dataset and combines three parts of a typical analytical workflow:

1. **Data understanding and cleaning**
2. **Portfolio and SQL analysis**
3. **Explainable default prediction**

The goal is not to build a production lending system. Instead, the project demonstrates how credit-risk data can be cleaned, explored, queried, and modeled in a transparent and reproducible way.

## Business Questions

The analysis focuses on questions such as:

- What does the overall loan portfolio look like?
- How often do borrowers default?
- Which loan grades and loan purposes are associated with higher observed default rates?
- How does home ownership relate to default risk?
- How does previous default history relate to current default risk?
- Which grades contribute the largest amount of defaulted loan exposure?
- Can borrower and loan characteristics be used to estimate default probability?
- How much predictive information is contained in the lender-assigned `loan_grade`?

## Dataset

The project uses the **Credit Risk Dataset** from Kaggle:

https://www.kaggle.com/datasets/laotse/credit-risk-dataset

The dataset contains **32,581 loan records** and 12 original variables describing borrower characteristics, loan characteristics, previous default history, and loan status.

The target variable is:

- `loan_status = 0` → non-default
- `loan_status = 1` → default

The raw dataset is **not stored in this repository**. To reproduce the project, download the Kaggle CSV and save it as:

```text
data/raw/credit_risk_dataset.csv
```

## Tools & Technologies

- **Python**
- **pandas**
- **NumPy**
- **Matplotlib**
- **scikit-learn**
- **SQLite**
- **SQL**
- **Jupyter Notebook**
- **Git / GitHub**

## Project Workflow

```text
Kaggle dataset
      ↓
01_data_understanding.ipynb
      ↓
02_data_cleaning.ipynb
      ↓
credit_risk_clean.csv
      ↓
03_portfolio_analysis.ipynb
      ↓
SQLite database
      ↓
SQL portfolio analysis
      ↓
reports/sql_results/

Raw dataset
      ↓
04_default_model.ipynb
      ↓
Preprocessing pipeline
      ↓
Logistic regression
      ↓
Model evaluation and risk bands
```

The portfolio analysis uses the cleaned dataset produced in Notebook 02.

For the predictive model, missing-value imputation and categorical encoding are handled inside the scikit-learn pipeline so preprocessing is learned as part of the modeling workflow.

## Data Understanding

The original dataset contains:

- **32,581 rows**
- **12 columns**
- **3,116 missing values** in `loan_int_rate`
- **895 missing values** in `person_emp_length`
- an overall default rate of approximately **21.82%**

The data-understanding notebook also checks category distributions, descriptive statistics, duplicate-looking rows, and the target-class distribution.

## Data Cleaning

The cleaning workflow includes:

- creation of missing-value indicator columns
- median imputation for `person_emp_length`
- grade-based median imputation for `loan_int_rate`
- inspection of unusual values and potential outliers
- validation of categorical variables
- export of the cleaned dataset to:

```text
data/processed/credit_risk_clean.csv
```

## Portfolio Analysis

The cleaned portfolio contains:

| Metric | Value |
|---|---:|
| Number of loans | 32,581 |
| Total loan amount | 312,431,300 |
| Average loan amount | 9,589.37 |
| Average interest rate | 11.01% |
| Number of defaults | 7,108 |
| Default rate | 21.82% |

### Default Rate by Loan Grade

Observed default risk rises strongly across loan grades:

| Loan Grade | Applicants | Default Rate |
|---|---:|---:|
| A | 10,777 | 9.96% |
| B | 10,451 | 16.28% |
| C | 6,458 | 20.73% |
| D | 3,626 | 59.05% |
| E | 964 | 64.42% |
| F | 241 | 70.54% |
| G | 64 | 98.44% |

The very high observed default rate for Grade G should be interpreted cautiously because the group contains only **64 applicants**.

### Default Rate by Loan Purpose

| Loan Purpose | Default Rate |
|---|---:|
| Debt consolidation | 28.59% |
| Medical | 26.70% |
| Home improvement | 26.10% |
| Personal | 19.89% |
| Education | 17.22% |
| Venture | 14.81% |

Debt-consolidation loans have the highest observed default rate in the portfolio, while venture loans have the lowest.

### Home Ownership

Observed default rates also differ across home-ownership groups:

| Home Ownership | Default Rate |
|---|---:|
| Rent | 31.57% |
| Other | 30.84% |
| Mortgage | 12.57% |
| Own | 7.47% |

The `OTHER` group contains only 107 observations, so its percentage should be interpreted with caution.

### Previous Default History

Borrowers with a previous default on file show a substantially higher observed default rate:

| Previous Default | Default Rate |
|---|---:|
| Yes | 37.81% |
| No | 18.39% |

These results are descriptive associations in this dataset and should not be interpreted as causal relationships.

## SQL Analysis

The project includes five SQL queries:

```text
sql/
├── 01_portfolio_overview.sql
├── 02_default_by_grade.sql
├── 03_default_by_purpose.sql
├── 04_high_risk_segments.sql
└── 05_exposure_analysis.sql
```

The queries calculate:

- overall portfolio metrics
- default rates by loan grade
- default rates by loan purpose
- higher-risk grade / previous-default segments
- loan exposure and defaulted loan amount by grade

The SQL results are exported automatically to:

```text
reports/sql_results/
```

### Exposure Analysis

Default rate alone does not show how much money is associated with defaults.

For example:

| Loan Grade | Default Rate | Defaulted Loan Amount | Defaulted Amount Share |
|---|---:|---:|---:|
| D | 59.05% | 22,800,100 | 57.96% |
| B | 16.28% | 19,120,425 | 18.30% |
| C | 20.73% | 13,579,600 | 22.82% |
| A | 9.96% | 10,202,525 | 11.09% |
| E | 64.42% | 7,826,925 | 62.86% |
| F | 70.54% | 2,496,875 | 70.40% |
| G | 98.44% | 1,098,925 | 99.85% |

Grade D has the **largest defaulted loan amount**, even though Grades E, F, and G have higher default rates. This illustrates why portfolio risk should be evaluated using both **default frequency** and **monetary exposure**.

## Default Prediction Model

An interpretable **logistic regression** model is used to estimate borrower default probability.

The modeling pipeline includes:

- median imputation for numerical variables
- standardization of numerical variables
- most-frequent imputation for categorical variables
- one-hot encoding for categorical variables
- class balancing with `class_weight="balanced"`
- an 80/20 stratified train-test split

The model is evaluated using:

- ROC-AUC
- precision
- recall
- F1-score
- confusion matrix
- predicted default probabilities

## Model Performance

Two versions of the same logistic regression model are compared:

- **Model A:** includes `loan_grade`
- **Model B:** excludes `loan_grade`

This comparison tests how much predictive information is already contained in the lender-assigned loan grade.

| Metric | With Loan Grade | Without Loan Grade |
|---|---:|---:|
| ROC-AUC | **0.871** | **0.856** |
| Precision | **55.3%** | **48.8%** |
| Recall | **78.0%** | **77.9%** |
| F1-score | **0.647** | **0.600** |

Including `loan_grade` improves ROC-AUC by approximately **0.015**.

Recall is almost unchanged, but precision is noticeably higher when loan grade is included.

The confusion matrices show the same pattern:

| Result | With Loan Grade | Without Loan Grade |
|---|---:|---:|
| True negatives | 4,199 | 3,933 |
| False positives | 896 | 1,162 |
| False negatives | 313 | 314 |
| True positives | 1,109 | 1,108 |

Removing loan grade barely changes the number of actual defaults detected, but it increases false-positive default predictions substantially.

This suggests that, in this model, `loan_grade` contributes primarily to **precision rather than recall**.

## Predicted Risk Bands

Predicted default probabilities are grouped into four analytical risk bands:

| Risk Band | Applicants | Observed Default Rate | Avg. Predicted Probability |
|---|---:|---:|---:|
| Low | 1,137 | 1.76% | 5.92% |
| Moderate | 1,823 | 6.69% | 16.64% |
| High | 1,552 | 11.02% | 35.94% |
| Very High | 2,005 | 55.31% | 77.20% |

The observed default rate rises substantially across the predicted risk bands, from **1.76%** in the Low group to **55.31%** in the Very High group.

The risk-band thresholds are illustrative and are not intended to represent production lending cutoffs.

## Key Findings

- The overall observed default rate is **21.82%**.
- Default risk increases strongly across loan grades.
- Debt-consolidation loans have the highest observed default rate by purpose at **28.59%**.
- Renters have an observed default rate of **31.57%**, compared with **7.47%** for borrowers who own their home.
- Borrowers with a previous default on file have an observed default rate of **37.81%**, compared with **18.39%** for those without one.
- Grade D contributes the largest amount of defaulted loan exposure at approximately **22.8 million** in dataset units.
- The logistic regression model achieves a **ROC-AUC of 0.871** with loan grade.
- Excluding loan grade reduces precision more than recall, indicating that loan grade mainly helps reduce false-positive default predictions.
- The model's predicted risk bands show a clear increase in observed default rates from Low to Very High risk.

## Project Structure

```text
credit-risk-portfolio-analysis/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── notebooks/
│   ├── 01_data_understanding.ipynb
│   ├── 02_data_cleaning.ipynb
│   ├── 03_portfolio_analysis.ipynb
│   └── 04_default_model.ipynb
│
├── reports/
│   └── sql_results/
│       ├── 01_portfolio_overview.csv
│       ├── 02_default_by_grade.csv
│       ├── 03_default_by_purpose.csv
│       ├── 04_high_risk_segments.csv
│       └── 05_exposure_analysis.csv
│
├── sql/
│   ├── 01_portfolio_overview.sql
│   ├── 02_default_by_grade.sql
│   ├── 03_default_by_purpose.sql
│   ├── 04_high_risk_segments.sql
│   └── 05_exposure_analysis.sql
│
├── src/
│   ├── create_database.py
│   └── run_sql_queries.py
│
├── .gitignore
├── README.md
└── requirements.txt
```

## How to Run the Project

### 1. Clone the repository

```bash
git clone https://github.com/marija-savanovic/credit-risk-portfolio-analysis.git
cd credit-risk-portfolio-analysis
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
```

On macOS / Linux:

```bash
source .venv/bin/activate
```

On Windows:

```bash
.venv\Scripts\activate
```

### 3. Install the required packages

```bash
pip install -r requirements.txt
```

### 4. Download the dataset

Download the Credit Risk Dataset from Kaggle:

https://www.kaggle.com/datasets/laotse/credit-risk-dataset

Place the CSV here:

```text
data/raw/credit_risk_dataset.csv
```

### 5. Run the notebooks

Run the notebooks in order:

```text
01_data_understanding.ipynb
02_data_cleaning.ipynb
03_portfolio_analysis.ipynb
04_default_model.ipynb
```

Notebook 02 generates:

```text
data/processed/credit_risk_clean.csv
```

### 6. Create the SQLite database

```bash
python src/create_database.py
```

This creates:

```text
data/processed/credit_risk.db
```

### 7. Run the SQL analysis

```bash
python src/run_sql_queries.py
```

The query outputs are written to:

```text
reports/sql_results/
```

## Limitations

This project is an educational portfolio analysis and should not be interpreted as a production credit decision system.

Important limitations include:

- the dataset is simulated and may not represent a real lending portfolio
- the model uses a single train-test split rather than out-of-time validation
- predicted default probabilities are not calibrated for production use
- risk-band thresholds were selected for analytical purposes
- the project estimates probability of default but does not model loss given default (LGD) or exposure at default (EAD)
- `loan_grade` may already contain information from an existing lender risk assessment
- a real credit model would require additional validation, fairness testing, regulatory review, monitoring, and governance

## Repository Purpose

This project was created as a portfolio project to demonstrate practical skills in:

- data cleaning
- exploratory analysis
- credit-risk portfolio analysis
- SQL
- reproducible data workflows
- interpretable machine learning
- model evaluation
- communicating analytical findings

