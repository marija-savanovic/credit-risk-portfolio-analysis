SELECT
    loan_intent,
    COUNT(*) AS applicant_count,
    SUM(loan_status) AS default_count,
    ROUND(AVG(loan_status) * 100, 2) AS default_rate_pct,
    ROUND(SUM(loan_amnt), 2) AS total_loan_amount,
    ROUND(AVG(loan_amnt), 2) AS average_loan_amount
FROM credit_risk
GROUP BY loan_intent
ORDER BY default_rate_pct DESC;