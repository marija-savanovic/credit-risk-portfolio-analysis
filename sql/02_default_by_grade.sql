SELECT
    loan_grade,
    COUNT(*) AS applicant_count,
    SUM(loan_status) AS default_count,
    ROUND(AVG(loan_status) * 100, 2) AS default_rate_pct,
    ROUND(SUM(loan_amnt), 2) AS total_loan_amount,
    ROUND(AVG(loan_int_rate), 2) AS average_interest_rate
FROM credit_risk
GROUP BY loan_grade
ORDER BY default_rate_pct DESC;