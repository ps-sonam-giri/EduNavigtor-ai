-- ============================================================
-- EduPilot AI – University & Scholarship Seed Data
-- ============================================================

-- USA Universities
INSERT INTO universities (country_id, name, short_name, website, location_city,
    qs_world_rank, acceptance_rate, min_cgpa, min_ielts, min_gre,
    avg_tuition_usd_per_year, avg_living_cost_usd_per_month, application_fee_usd,
    programs, intake_months, has_scholarships, overview, strengths, graduate_employment_rate)
SELECT c.id,
    'Massachusetts Institute of Technology', 'MIT', 'https://www.mit.edu', 'Cambridge MA',
    1, 4.0, 8.5, 7.0, 320,
    55000, 2000, 75,
    '[{"name":"MS Computer Science","duration_years":2,"tuition_usd":55000},{"name":"MS AI","duration_years":2,"tuition_usd":55000},{"name":"MS Electrical Engineering","duration_years":2,"tuition_usd":55000}]',
    '["September"]',
    true,
    'MIT is the world''s leading science and technology university, known for innovation, research, and producing Nobel laureates.',
    '["#1 in Engineering","#1 in Computer Science","Strong industry partnerships","Exceptional research funding"]',
    97.0
FROM countries c WHERE c.code = 'USA'
ON CONFLICT DO NOTHING;

INSERT INTO universities (country_id, name, short_name, website, location_city,
    qs_world_rank, acceptance_rate, min_cgpa, min_ielts, min_gre,
    avg_tuition_usd_per_year, avg_living_cost_usd_per_month, application_fee_usd,
    programs, intake_months, has_scholarships, overview, strengths, graduate_employment_rate)
SELECT c.id,
    'Stanford University', 'Stanford', 'https://www.stanford.edu', 'Stanford CA',
    3, 5.2, 8.0, 7.0, 315,
    58000, 2200, 90,
    '[{"name":"MS Computer Science","duration_years":2,"tuition_usd":58000},{"name":"MBA","duration_years":2,"tuition_usd":74000},{"name":"MS Data Science","duration_years":1,"tuition_usd":58000}]',
    '["September"]',
    true,
    'Stanford is at the heart of Silicon Valley, offering unmatched access to tech industry, venture capital, and entrepreneurship ecosystems.',
    '["Silicon Valley location","#1 MBA globally","Strong entrepreneurship culture","Huge alumni network"]',
    98.0
FROM countries c WHERE c.code = 'USA'
ON CONFLICT DO NOTHING;

INSERT INTO universities (country_id, name, short_name, website, location_city,
    qs_world_rank, acceptance_rate, min_cgpa, min_ielts, min_gre,
    avg_tuition_usd_per_year, avg_living_cost_usd_per_month, application_fee_usd,
    programs, intake_months, has_scholarships, overview, strengths, graduate_employment_rate)
SELECT c.id,
    'Carnegie Mellon University', 'CMU', 'https://www.cmu.edu', 'Pittsburgh PA',
    52, 17.0, 8.0, 7.0, 315,
    52000, 1600, 75,
    '[{"name":"MS Computer Science","duration_years":2,"tuition_usd":52000},{"name":"MS Machine Learning","duration_years":2,"tuition_usd":52000},{"name":"MS Software Engineering","duration_years":1.5,"tuition_usd":52000}]',
    '["September", "January"]',
    true,
    'CMU is world-renowned for Computer Science and AI, with the highest placement rate in top tech companies.',
    '["#1 CS program in USA","Strong AI/ML research","FAANG placement rate >60%","Strong Indian student community"]',
    96.0
FROM countries c WHERE c.code = 'USA'
ON CONFLICT DO NOTHING;

INSERT INTO universities (country_id, name, short_name, website, location_city,
    qs_world_rank, acceptance_rate, min_cgpa, min_ielts, min_gre,
    avg_tuition_usd_per_year, avg_living_cost_usd_per_month, application_fee_usd,
    programs, intake_months, has_scholarships, overview, strengths, graduate_employment_rate)
SELECT c.id,
    'University of Illinois Urbana-Champaign', 'UIUC', 'https://illinois.edu', 'Urbana IL',
    82, 44.0, 7.5, 6.5, 305,
    32000, 1100, 70,
    '[{"name":"MS Computer Science","duration_years":2,"tuition_usd":32000},{"name":"MS Data Science","duration_years":2,"tuition_usd":32000},{"name":"MS Electrical Engineering","duration_years":2,"tuition_usd":32000}]',
    '["August", "January"]',
    true,
    'UIUC is a top public university known for engineering excellence, affordability, and a massive Indian student community.',
    '["Affordable public university","Top 10 CS program","Strong research output","Large Indian diaspora"]',
    93.0
FROM countries c WHERE c.code = 'USA'
ON CONFLICT DO NOTHING;

-- UK Universities
INSERT INTO universities (country_id, name, short_name, website, location_city,
    qs_world_rank, acceptance_rate, min_cgpa, min_ielts,
    avg_tuition_usd_per_year, avg_living_cost_usd_per_month, application_fee_usd,
    programs, intake_months, has_scholarships, overview, strengths, graduate_employment_rate)
SELECT c.id,
    'University of Oxford', 'Oxford', 'https://www.ox.ac.uk', 'Oxford',
    3, 18.0, 8.5, 7.0,
    35000, 1400, 0,
    '[{"name":"MSc Computer Science","duration_years":1,"tuition_usd":35000},{"name":"MBA","duration_years":1,"tuition_usd":70000},{"name":"MSc Data Science","duration_years":1,"tuition_usd":35000}]',
    '["October"]',
    true,
    'Oxford is one of the world''s oldest and most prestigious universities with an unmatched global reputation.',
    '["#3 globally QS ranked","Historic prestige","1-year Masters","Rhodes Scholarship available"]',
    95.0
FROM countries c WHERE c.code = 'GBR'
ON CONFLICT DO NOTHING;

INSERT INTO universities (country_id, name, short_name, website, location_city,
    qs_world_rank, acceptance_rate, min_cgpa, min_ielts,
    avg_tuition_usd_per_year, avg_living_cost_usd_per_month, application_fee_usd,
    programs, intake_months, has_scholarships, overview, strengths, graduate_employment_rate)
SELECT c.id,
    'University of Edinburgh', 'Edinburgh', 'https://www.ed.ac.uk', 'Edinburgh',
    22, 36.0, 7.0, 6.5,
    28000, 1100, 0,
    '[{"name":"MSc Artificial Intelligence","duration_years":1,"tuition_usd":28000},{"name":"MSc Data Science","duration_years":1,"tuition_usd":26000},{"name":"MSc Computer Science","duration_years":1,"tuition_usd":28000}]',
    '["September"]',
    true,
    'Edinburgh is Scotland''s top university with a world-class AI programme and affordable living costs.',
    '["Top AI programme in UK","Affordable living vs London","Safe vibrant student city","Strong research output"]',
    91.0
FROM countries c WHERE c.code = 'GBR'
ON CONFLICT DO NOTHING;

-- Canada Universities
INSERT INTO universities (country_id, name, short_name, website, location_city,
    qs_world_rank, acceptance_rate, min_cgpa, min_ielts,
    avg_tuition_usd_per_year, avg_living_cost_usd_per_month, application_fee_usd,
    programs, intake_months, has_scholarships, overview, strengths, graduate_employment_rate)
SELECT c.id,
    'University of Toronto', 'UofT', 'https://www.utoronto.ca', 'Toronto',
    21, 43.0, 7.5, 6.5,
    26000, 1200, 125,
    '[{"name":"MEng Computer Engineering","duration_years":1,"tuition_usd":26000},{"name":"MSc Data Science","duration_years":2,"tuition_usd":24000},{"name":"MBA","duration_years":2,"tuition_usd":50000}]',
    '["September", "January"]',
    true,
    'University of Toronto is Canada''s top university, consistently ranked among the global top 25, with strong research and PGWP pathway.',
    '["Top 25 globally","Toronto tech hub","PGWP 3 years","Strong Indian community"]',
    92.0
FROM countries c WHERE c.code = 'CAN'
ON CONFLICT DO NOTHING;

INSERT INTO universities (country_id, name, short_name, website, location_city,
    qs_world_rank, acceptance_rate, min_cgpa, min_ielts,
    avg_tuition_usd_per_year, avg_living_cost_usd_per_month, application_fee_usd,
    programs, intake_months, has_scholarships, overview, strengths, graduate_employment_rate)
SELECT c.id,
    'University of British Columbia', 'UBC', 'https://www.ubc.ca', 'Vancouver',
    34, 52.0, 7.0, 6.5,
    22000, 1300, 102,
    '[{"name":"MEng Computer Science","duration_years":1,"tuition_usd":22000},{"name":"MSc Data Science","duration_years":2,"tuition_usd":20000},{"name":"MSc Business Analytics","duration_years":1,"tuition_usd":30000}]',
    '["September"]',
    true,
    'UBC in Vancouver offers world-class education with an incredible Pacific coast lifestyle and strong tech industry ties.',
    '["Top 40 globally","Beautiful Vancouver campus","Strong sustainability programs","High quality of life"]',
    90.0
FROM countries c WHERE c.code = 'CAN'
ON CONFLICT DO NOTHING;

-- Germany Universities
INSERT INTO universities (country_id, name, short_name, website, location_city,
    qs_world_rank, acceptance_rate, min_cgpa, min_ielts,
    avg_tuition_usd_per_year, avg_living_cost_usd_per_month, application_fee_usd,
    programs, intake_months, has_scholarships, overview, strengths, graduate_employment_rate)
SELECT c.id,
    'Technical University of Munich', 'TUM', 'https://www.tum.de', 'Munich',
    37, 8.0, 7.5, 6.5,
    500, 900, 0,
    '[{"name":"MSc Computer Science","duration_years":2,"tuition_usd":500},{"name":"MSc Data Engineering","duration_years":2,"tuition_usd":500},{"name":"MSc Electrical Engineering","duration_years":2,"tuition_usd":500}]',
    '["October", "April"]',
    true,
    'TUM is Germany''s top technical university, offering almost free education with world-class engineering and research facilities.',
    '["Nearly free education","#1 university in Germany","18-month job seeker visa","BMW/Siemens/Airbus partnerships"]',
    95.0
FROM countries c WHERE c.code = 'DEU'
ON CONFLICT DO NOTHING;

-- Australia Universities
INSERT INTO universities (country_id, name, short_name, website, location_city,
    qs_world_rank, acceptance_rate, min_cgpa, min_ielts,
    avg_tuition_usd_per_year, avg_living_cost_usd_per_month, application_fee_usd,
    programs, intake_months, has_scholarships, overview, strengths, graduate_employment_rate)
SELECT c.id,
    'University of Melbourne', 'UniMelb', 'https://www.unimelb.edu.au', 'Melbourne',
    33, 70.0, 6.5, 6.5,
    32000, 1300, 0,
    '[{"name":"Master of Computer Science","duration_years":2,"tuition_usd":32000},{"name":"Master of Data Science","duration_years":2,"tuition_usd":30000},{"name":"Master of Business","duration_years":2,"tuition_usd":38000}]',
    '["February", "July"]',
    true,
    'UniMelb is Australia''s most highly ranked university with a multicultural campus, strong research, and excellent employment outcomes.',
    '["#1 in Australia","Melbourne Graduate Scholarship","4-year Post-Study Work Visa","World-class campus"]',
    91.0
FROM countries c WHERE c.code = 'AUS'
ON CONFLICT DO NOTHING;

-- ────────────────────────────────────────────────────────────
-- SEED DATA – Scholarships
-- ────────────────────────────────────────────────────────────
INSERT INTO scholarships (name, provider, scholarship_type, amount_usd, amount_description,
    eligible_countries, eligible_courses, min_cgpa, min_ielts,
    description, eligibility_criteria, is_active)
VALUES
('Commonwealth Scholarship', 'UK Government', 'full_tuition', 50000,
 'Full tuition + living allowance + return airfare',
 '["India","Pakistan","Bangladesh","Sri Lanka"]',
 '["All postgraduate programs"]',
 7.5, 6.5,
 'The Commonwealth Scholarship is awarded to outstanding students from Commonwealth countries to study in the UK.',
 'Must be a citizen of a Commonwealth country, hold a good first degree, not have studied in UK before on a Commonwealth scholarship.',
 true),

('Chevening Scholarship', 'UK Foreign Commonwealth Office', 'full_tuition', 45000,
 'Full tuition + living stipend + flights',
 '["India","All"]',
 '["All Masters programs"]',
 NULL, 6.5,
 'Chevening is the UK Government''s international awards programme, offering scholarships to future leaders worldwide.',
 'Minimum 2 years work experience, leadership qualities, return to home country after studies.',
 true),

('Australia Awards Scholarship', 'Australian Government', 'full_tuition', 40000,
 'Full tuition + return airfare + living allowance',
 '["India","All developing nations"]',
 '["All postgraduate programs"]',
 NULL, 6.5,
 'Prestigious international award offered by the Australian Government for students from developing countries.',
 'Must be from an eligible developing country, under 55 years old, not Australian citizen or PR.',
 true),

('DAAD Scholarship', 'German Academic Exchange Service', 'living_stipend', 12000,
 'Monthly stipend of €934 + travel allowance',
 '["India","All"]',
 '["All programs at German universities"]',
 NULL, 6.0,
 'DAAD is the most prestigious German scholarship for international students, covering living costs at German universities.',
 'Must be enrolled or applying to a German university, excellent academic record, research proposal required.',
 true),

('Vanier Canada Graduate Scholarship', 'Government of Canada', 'merit', 50000,
 'CAD 50,000 per year for 3 years',
 '["India","All"]',
 '["PhD programs in Canada"]',
 NULL, 7.0,
 'Canada''s most prestigious doctoral scholarship, aimed at attracting world-class doctoral students.',
 'Must be nominated by a Canadian university, exceptional academic achievement, leadership skills.',
 true),

('Inlaks Scholarship', 'Inlaks Shivdasani Foundation', 'partial_tuition', 100000,
 'Up to USD 100,000 for top institutions',
 '["India"]',
 '["All Masters programs"]',
 8.0, 6.5,
 'The Inlaks scholarship supports outstanding Indian students to pursue Masters degrees at top world universities.',
 'Indian citizens only, under 30 years old, admission to top-ranked university required, strong academic record.',
 true),

('JN Tata Endowment Scholarship', 'Tata Education Trust', 'partial_tuition', 20000,
 'Loan scholarship up to INR 10 lakhs',
 '["India"]',
 '["All postgraduate programs"]',
 7.5, NULL,
 'One of India''s oldest and most prestigious scholarships for postgraduate studies abroad.',
 'Indian nationals only, outstanding academic record, admission to a reputed foreign university.',
 true),

('QS Merit Scholarship', 'University Merit', 'partial_tuition', 10000,
 'Varies by university – typically 10-25% tuition waiver',
 '["All"]',
 '["All programs"]',
 8.0, 7.0,
 'Many universities offer merit-based scholarships to students with exceptional academic records.',
 'Strong CGPA (typically 8.0+), high test scores, early application recommended.',
 true);
