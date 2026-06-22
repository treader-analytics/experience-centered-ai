-- Experience-Centered AI Industry & Company Analysis
-- SQL schema for storing company, scoring, and ranking data.

DROP TABLE IF EXISTS companies;
DROP TABLE IF EXISTS company_scores;
DROP TABLE IF EXISTS final_rankings;

CREATE TABLE companies (
    company_id INTEGER PRIMARY KEY,
    company TEXT NOT NULL,
    ticker TEXT NOT NULL,
    industry TEXT NOT NULL,
    business_model TEXT,
    public_status TEXT
);

CREATE TABLE company_scores (
    company_id INTEGER PRIMARY KEY,
    experience_intensity REAL NOT NULL,
    ai_enhancement REAL NOT NULL,
    repeat_usage REAL NOT NULL,
    agency_preservation REAL NOT NULL,
    revenue_capture REAL NOT NULL,
    network_effects REAL NOT NULL,
    experience_ai_score REAL NOT NULL,
    FOREIGN KEY (company_id) REFERENCES companies(company_id)
);

CREATE TABLE final_rankings (
    rank INTEGER PRIMARY KEY,
    company_id INTEGER NOT NULL,
    company TEXT NOT NULL,
    industry TEXT NOT NULL,
    experience_ai_score REAL NOT NULL,
    FOREIGN KEY (company_id) REFERENCES companies(company_id)
);