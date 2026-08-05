-- ============================================================
-- EduPilot AI – Initial PostgreSQL Schema
-- Run with: psql -U edupilot -d edupilot_db -f 001_initial_schema.sql
-- ============================================================

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";   -- for fuzzy text search

-- ────────────────────────────────────────────────────────────
-- USERS
-- ────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS users (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email           VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255)        NOT NULL,
    full_name       VARCHAR(255)        NOT NULL,
    is_active       BOOLEAN             NOT NULL DEFAULT TRUE,
    is_verified     BOOLEAN             NOT NULL DEFAULT FALSE,
    gmail_token     VARCHAR(2048),
    created_at      TIMESTAMPTZ         NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ         NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);

-- ────────────────────────────────────────────────────────────
-- COUNTRIES
-- ────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS countries (
    id                              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name                            VARCHAR(100) UNIQUE NOT NULL,
    code                            VARCHAR(3)   UNIQUE NOT NULL,
    avg_tuition_usd_per_year        NUMERIC(10,2),
    avg_living_cost_usd_per_month   NUMERIC(10,2),
    visa_fee_usd                    NUMERIC(10,2),
    health_insurance_usd_per_year   NUMERIC(10,2),
    post_study_work_years           INTEGER      NOT NULL DEFAULT 0,
    part_time_hours_per_week        INTEGER      NOT NULL DEFAULT 0,
    top_ranked_universities_count   INTEGER      NOT NULL DEFAULT 0,
    language                        VARCHAR(50)  NOT NULL DEFAULT 'English',
    ielts_min_required              NUMERIC(3,1),
    overview                        TEXT,
    pros                            JSONB        NOT NULL DEFAULT '[]',
    cons                            JSONB        NOT NULL DEFAULT '[]',
    popular_courses                 JSONB        NOT NULL DEFAULT '[]',
    is_active                       BOOLEAN      NOT NULL DEFAULT TRUE
);

-- ────────────────────────────────────────────────────────────
-- UNIVERSITIES
-- ────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS universities (
    id                          UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    country_id                  UUID         NOT NULL REFERENCES countries(id) ON DELETE RESTRICT,
    name                        VARCHAR(300) NOT NULL,
    short_name                  VARCHAR(50),
    website                     VARCHAR(500),
    location_city               VARCHAR(100),
    qs_world_rank               INTEGER,
    qs_subject_rank             INTEGER,
    times_rank                  INTEGER,
    acceptance_rate             NUMERIC(5,2),
    min_cgpa                    NUMERIC(4,2),
    min_ielts                   NUMERIC(3,1),
    min_toefl                   INTEGER,
    min_gre                     INTEGER,
    requires_gmat               BOOLEAN      NOT NULL DEFAULT FALSE,
    avg_tuition_usd_per_year    NUMERIC(10,2),
    avg_living_cost_usd_per_month NUMERIC(10,2),
    application_fee_usd         NUMERIC(8,2),
    programs                    JSONB        NOT NULL DEFAULT '[]',
    intake_months               JSONB        NOT NULL DEFAULT '[]',
    has_scholarships            BOOLEAN      NOT NULL DEFAULT FALSE,
    overview                    TEXT,
    strengths                   JSONB        NOT NULL DEFAULT '[]',
    notable_alumni              JSONB        NOT NULL DEFAULT '[]',
    graduate_employment_rate    NUMERIC(5,2),
    avg_starting_salary_usd     NUMERIC(10,2),
    is_active                   BOOLEAN      NOT NULL DEFAULT TRUE
);
CREATE INDEX IF NOT EXISTS idx_universities_country_id  ON universities(country_id);
CREATE INDEX IF NOT EXISTS idx_universities_qs_rank     ON universities(qs_world_rank);
CREATE INDEX IF NOT EXISTS idx_universities_name        ON universities USING gin(name gin_trgm_ops);

-- ────────────────────────────────────────────────────────────
-- SCHOLARSHIPS
-- ────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS scholarships (
    id                          UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    university_id               UUID         REFERENCES universities(id) ON DELETE SET NULL,
    name                        VARCHAR(300) NOT NULL,
    provider                    VARCHAR(200) NOT NULL,
    scholarship_type            VARCHAR(50)  NOT NULL,
    amount_usd                  NUMERIC(10,2),
    amount_description          VARCHAR(300),
    eligible_countries          JSONB        NOT NULL DEFAULT '[]',
    eligible_courses            JSONB        NOT NULL DEFAULT '[]',
    min_cgpa                    NUMERIC(4,2),
    min_ielts                   NUMERIC(3,1),
    requires_work_experience    BOOLEAN      NOT NULL DEFAULT FALSE,
    min_work_experience_years   INTEGER      NOT NULL DEFAULT 0,
    application_deadline        VARCHAR(100),
    application_url             VARCHAR(500),
    description                 TEXT,
    eligibility_criteria        TEXT,
    is_active                   BOOLEAN      NOT NULL DEFAULT TRUE
);
CREATE INDEX IF NOT EXISTS idx_scholarships_university_id ON scholarships(university_id);

-- ────────────────────────────────────────────────────────────
-- STUDENT PROFILES
-- ────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS student_profiles (
    id                      UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id                 UUID UNIQUE NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    cgpa                    NUMERIC(4,2),
    cgpa_scale              NUMERIC(4,2) NOT NULL DEFAULT 10.0,
    backlogs                INTEGER      NOT NULL DEFAULT 0,
    degree                  VARCHAR(100),
    specialization          VARCHAR(200),
    graduation_year         INTEGER,
    university_name         VARCHAR(300),
    ielts_score             NUMERIC(3,1),
    toefl_score             INTEGER,
    pte_score               INTEGER,
    gre_score               INTEGER,
    gmat_score              INTEGER,
    preferred_countries     JSONB        NOT NULL DEFAULT '[]',
    course_interest         VARCHAR(200),
    career_goal             TEXT,
    target_intake           VARCHAR(50),
    total_budget_usd        NUMERIC(12,2),
    financial_background    VARCHAR(50),
    work_experience_years   INTEGER      NOT NULL DEFAULT 0,
    work_description        TEXT,
    documents               JSONB        NOT NULL DEFAULT '{}',
    extracted_data          JSONB        NOT NULL DEFAULT '{}',
    created_at              TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    updated_at              TIMESTAMPTZ  NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_profiles_user_id ON student_profiles(user_id);

-- ────────────────────────────────────────────────────────────
-- APPLICATIONS
-- ────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS applications (
    id                      UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id                 UUID        NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    university_id           UUID        NOT NULL REFERENCES universities(id) ON DELETE RESTRICT,
    program_name            VARCHAR(300),
    intake                  VARCHAR(50),
    status                  VARCHAR(50) NOT NULL DEFAULT 'shortlisted',
    notes                   TEXT,
    documents_submitted     JSONB       NOT NULL DEFAULT '[]',
    deadlines               JSONB       NOT NULL DEFAULT '{}',
    created_at              TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at              TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_applications_user_id       ON applications(user_id);
CREATE INDEX IF NOT EXISTS idx_applications_university_id ON applications(university_id);
CREATE INDEX IF NOT EXISTS idx_applications_status        ON applications(status);

-- ────────────────────────────────────────────────────────────
-- REPORTS
-- ────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS reports (
    id               UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id          UUID         NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    session_id       VARCHAR(100) NOT NULL,
    report_type      VARCHAR(50)  NOT NULL DEFAULT 'full',
    title            VARCHAR(300) NOT NULL,
    summary          TEXT,
    content          JSONB        NOT NULL DEFAULT '{}',
    pdf_path         VARCHAR(500),
    docx_path        VARCHAR(500),
    email_sent       BOOLEAN      NOT NULL DEFAULT FALSE,
    email_sent_at    TIMESTAMPTZ,
    email_recipient  VARCHAR(255),
    created_at       TIMESTAMPTZ  NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_reports_user_id    ON reports(user_id);
CREATE INDEX IF NOT EXISTS idx_reports_session_id ON reports(session_id);

-- ────────────────────────────────────────────────────────────
-- AGENT LOGS
-- ────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS agent_logs (
    id                  UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id             UUID         NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    session_id          VARCHAR(100) NOT NULL,
    agent_name          VARCHAR(100) NOT NULL,
    action              VARCHAR(200),
    status              VARCHAR(20)  NOT NULL DEFAULT 'running',
    input_data          JSONB        NOT NULL DEFAULT '{}',
    output_data         JSONB        NOT NULL DEFAULT '{}',
    reasoning           TEXT,
    tokens_used         INTEGER      NOT NULL DEFAULT 0,
    execution_time_ms   NUMERIC(10,2),
    error_message       TEXT,
    created_at          TIMESTAMPTZ  NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_agent_logs_user_id    ON agent_logs(user_id);
CREATE INDEX IF NOT EXISTS idx_agent_logs_session_id ON agent_logs(session_id);
CREATE INDEX IF NOT EXISTS idx_agent_logs_agent_name ON agent_logs(agent_name);

-- ────────────────────────────────────────────────────────────
-- SEED DATA – Countries
-- ────────────────────────────────────────────────────────────
INSERT INTO countries (name, code, avg_tuition_usd_per_year, avg_living_cost_usd_per_month,
    visa_fee_usd, health_insurance_usd_per_year, post_study_work_years,
    part_time_hours_per_week, top_ranked_universities_count, ielts_min_required,
    overview, pros, cons, popular_courses)
VALUES
('United States', 'USA', 35000, 1500, 185, 1200, 3, 20, 200, 6.5,
 'The USA offers world-class universities, cutting-edge research, and the largest number of international students globally.',
 '["Top QS ranked universities","OPT/STEM OPT extension (up to 3 years)","Strong alumni networks","High graduate salaries"]',
 '["Very high tuition costs","Health insurance mandatory and expensive","Visa process complex"]',
 '["Computer Science","Data Science","MBA","Engineering","Biotechnology"]'),

('United Kingdom', 'GBR', 25000, 1200, 490, 470, 2, 20, 100, 6.0,
 'The UK offers shorter degree programs (1-year Masters), globally recognised qualifications, and a rich cultural experience.',
 '["1-year Masters saves time and money","PSW visa – 2 years post-study work","World-renowned institutions"]',
 '["High living cost in London","Limited part-time work hours","Brexit impact on some students"]',
 '["Finance","Law","Business","Computer Science","Medicine"]'),

('Canada', 'CAN', 22000, 1100, 150, 600, 3, 20, 30, 6.0,
 'Canada is a top destination for Indian students with welcoming immigration policies and excellent quality of life.',
 '["PGWP up to 3 years","Path to permanent residency","Safe and multicultural","Lower tuition than USA/UK"]',
 '["Cold winters","Competitive job market","Processing delays for visas"]',
 '["Engineering","Business","Computer Science","Healthcare","Hospitality"]'),

('Australia', 'AUS', 28000, 1300, 620, 500, 4, 48, 40, 6.0,
 'Australia offers a high quality of life, strong job market, and one of the most generous post-study work visa policies.',
 '["Post-study work visa 2-4 years","High minimum wage","World-class universities","Sunny lifestyle"]',
 '["High cost of living in Sydney/Melbourne","Far from India","Bushfire/climate concerns"]',
 '["Engineering","Business","Medicine","Agriculture","Information Technology"]'),

('Germany', 'DEU', 500, 900, 75, 100, 18, 20, 50, 6.0,
 'Germany offers free or near-free education at public universities, making it the most affordable study destination in Europe.',
 '["Near-zero tuition at public universities","18-month job seeker visa post-study","Strong engineering industry","Safe country"]',
 '["Language barrier for non-German programs","Lower English-taught options","Adapting to German culture"]',
 '["Engineering","Computer Science","Automotive","Physics","Business"]'),

('Ireland', 'IRL', 18000, 1100, 100, 500, 2, 20, 10, 6.0,
 'Ireland is the only English-speaking EU country post-Brexit, making it attractive for IT and finance careers.',
 '["EU country with English language","Hub for tech giants (Google, Meta, Microsoft)","2-year stay-back visa"]',
 '["Limited universities","High Dublin rent","Smaller job market than UK/USA"]',
 '["Computer Science","Finance","Pharmaceuticals","Data Analytics"]'),

('New Zealand', 'NZL', 20000, 1000, 190, 350, 3, 20, 8, 5.5,
 'New Zealand offers a scenic lifestyle, quality education, and strong post-study work rights.',
 '["Open Work Visa for partners","Post-study work 1-3 years","Safe and peaceful environment"]',
 '["Small economy","Limited industry diversity","Remote location"]',
 '["Agriculture","Tourism","IT","Engineering","Healthcare"]')
ON CONFLICT (name) DO NOTHING;
