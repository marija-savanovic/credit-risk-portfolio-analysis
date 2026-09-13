SELECT
    loan_grade,
    cb_person_default_on_file,
    COUNT(*) AS applicant_count,
    SUM(loan_status) AS default_count,
    ROUND(AVG(loan_status) * 100, 2) AS default_rate_pct,
    ROUND(SUM(loan_amnt), 2) AS total_loan_amount
FROM credit_risk
GROUP BY
    loan_grade,
    cb_person_default_on_file
HAVING COUNT(*) >= 30
ORDER BY default_rate_pct DESC;