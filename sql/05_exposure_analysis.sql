SELECT
    loan_grade,
    COUNT(*) AS applicant_count,

    ROUND(
        SUM(loan_amnt),
        2
    ) AS total_loan_amount,

    ROUND(
        SUM(
            CASE
                WHEN loan_status = 1
                THEN loan_amnt
                ELSE 0
            END
        ),
        2
    ) AS defaulted_loan_amount,

    ROUND(
        AVG(loan_status) * 100,
        2
    ) AS default_rate_pct,

    ROUND(
        SUM(
            CASE
                WHEN loan_status = 1
                THEN loan_amnt
                ELSE 0
            END
        )
        /
        SUM(loan_amnt)
        * 100,
        2
    ) AS defaulted_amount_pct

FROM credit_risk

GROUP BY loan_grade

ORDER BY defaulted_loan_amount DESC;