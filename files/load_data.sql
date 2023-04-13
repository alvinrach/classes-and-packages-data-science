CREATE TABLE kaggle_creditscore (
    person_age INTEGER,
    person_income INTEGER,
    person_home_ownership TEXT,
    person_emp_length NUMERIC,
    loan_intent TEXT,
    loan_grade TEXT,
    loan_amnt INTEGER,
    loan_int_rate NUMERIC,
    loan_status INTEGER,
    loan_percent_income NUMERIC,
    cb_person_default_on_file TEXT,
    cb_person_cred_hist_length INTEGER
);

COPY kaggle_creditscore (person_age, person_income, person_home_ownership, person_emp_length, loan_intent, loan_grade, loan_amnt, loan_int_rate, loan_status, loan_percent_income, cb_person_default_on_file, cb_person_cred_hist_length)
FROM '/tmp/credit_risk_dataset.csv'
WITH (FORMAT csv, HEADER true, DELIMITER ',');