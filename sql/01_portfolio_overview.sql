SELECT
    COUNT(*) AS number_of_loans,
    ROUND(SUM(loan_amnt), 2) AS total_loan_amount,
    ROUND(AVG(loan_amnt), 2) AS average_loan_amount,
    ROUND(AVG(loan_int_rate), 2) AS average_interest_rate,
    SUM(loan_status) AS number_of_defaults,
    ROUND(AVG(loan_status) * 100, 2) AS default_rate_pct
FROM credit_risk;