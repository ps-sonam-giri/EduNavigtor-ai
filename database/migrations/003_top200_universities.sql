-- ============================================================
-- EduPilot AI – Top 200 Universities Worldwide
-- Run: psql -U edupilot -d edupilot_db -f 003_top200_universities.sql
-- ============================================================

-- ── USA ──────────────────────────────────────────────────────────────────────
INSERT INTO universities (country_id, name, short_name, website, location_city, qs_world_rank, acceptance_rate, min_cgpa, min_ielts, min_gre, avg_tuition_usd_per_year, avg_living_cost_usd_per_month, application_fee_usd, programs, intake_months, has_scholarships, overview, strengths, graduate_employment_rate, is_active)
SELECT c.id, 'Harvard University', 'Harvard', 'https://www.harvard.edu', 'Cambridge MA', 4, 3.2, 9.0, 7.5, 325, 57000, 2200, 85,
'[{"name":"MS Computer Science","duration_years":2,"tuition_usd":57000},{"name":"MBA","duration_years":2,"tuition_usd":73000},{"name":"MS Data Science","duration_years":2,"tuition_usd":57000}]',
'["September"]', true, 'Harvard University is the oldest university in the USA, consistently ranked among the top universities worldwide.',
'["#1 MBA","Nobel laureates","Research excellence","Largest endowment"]', 98.0 FROM countries c WHERE c.code='USA' ON CONFLICT DO NOTHING;

INSERT INTO universities (country_id, name, short_name, website, location_city, qs_world_rank, acceptance_rate, min_cgpa, min_ielts, min_gre, avg_tuition_usd_per_year, avg_living_cost_usd_per_month, application_fee_usd, programs, intake_months, has_scholarships, overview, strengths, graduate_employment_rate, is_active)
SELECT c.id, 'California Institute of Technology', 'Caltech', 'https://www.caltech.edu', 'Pasadena CA', 6, 3.9, 9.0, 7.0, 330, 60000, 2000, 75,
'[{"name":"MS Computer Science","duration_years":2,"tuition_usd":60000},{"name":"MS Electrical Engineering","duration_years":2,"tuition_usd":60000}]',
'["September"]', true, 'Caltech is a world-class science and engineering institute known for rigorous academics and groundbreaking research.',
'["Top engineering","NASA JPL partner","Nobel laureates","Small class sizes"]', 97.0 FROM countries c WHERE c.code='USA' ON CONFLICT DO NOTHING;

INSERT INTO universities (country_id, name, short_name, website, location_city, qs_world_rank, acceptance_rate, min_cgpa, min_ielts, min_gre, avg_tuition_usd_per_year, avg_living_cost_usd_per_month, application_fee_usd, programs, intake_months, has_scholarships, overview, strengths, graduate_employment_rate, is_active)
SELECT c.id, 'University of Chicago', 'UChicago', 'https://www.uchicago.edu', 'Chicago IL', 21, 6.5, 8.5, 7.0, 320, 59000, 1600, 90,
'[{"name":"MBA (Booth)","duration_years":2,"tuition_usd":75000},{"name":"MS Computer Science","duration_years":2,"tuition_usd":59000},{"name":"MS Statistics","duration_years":1,"tuition_usd":59000}]',
'["September"]', true, 'University of Chicago is known for its rigorous academics, influential economics department, and the Booth School of Business.',
'["#1 Economics","Booth MBA","100 Nobel laureates","Strong research culture"]', 96.0 FROM countries c WHERE c.code='USA' ON CONFLICT DO NOTHING;

INSERT INTO universities (country_id, name, short_name, website, location_city, qs_world_rank, acceptance_rate, min_cgpa, min_ielts, min_gre, avg_tuition_usd_per_year, avg_living_cost_usd_per_month, application_fee_usd, programs, intake_months, has_scholarships, overview, strengths, graduate_employment_rate, is_active)
SELECT c.id, 'Columbia University', 'Columbia', 'https://www.columbia.edu', 'New York NY', 33, 3.7, 8.5, 7.0, 320, 62000, 2500, 85,
'[{"name":"MS Computer Science","duration_years":2,"tuition_usd":62000},{"name":"MBA","duration_years":2,"tuition_usd":78000},{"name":"MS Data Science","duration_years":1,"tuition_usd":62000}]',
'["September","January"]', true, 'Columbia University is an Ivy League university in the heart of New York City, offering unmatched access to finance and tech industries.',
'["NYC location","Finance hub","Ivy League prestige","Strong alumni network"]', 96.0 FROM countries c WHERE c.code='USA' ON CONFLICT DO NOTHING;

INSERT INTO universities (country_id, name, short_name, website, location_city, qs_world_rank, acceptance_rate, min_cgpa, min_ielts, min_gre, avg_tuition_usd_per_year, avg_living_cost_usd_per_month, application_fee_usd, programs, intake_months, has_scholarships, overview, strengths, graduate_employment_rate, is_active)
SELECT c.id, 'University of Pennsylvania', 'Penn', 'https://www.upenn.edu', 'Philadelphia PA', 12, 5.9, 8.5, 7.0, 320, 60000, 1800, 85,
'[{"name":"MBA (Wharton)","duration_years":2,"tuition_usd":82000},{"name":"MS Computer Science","duration_years":2,"tuition_usd":60000},{"name":"MS Engineering","duration_years":2,"tuition_usd":60000}]',
'["September"]', true, 'Penn is an Ivy League university home to the world-famous Wharton School of Business.',
'["Wharton #1 MBA","Strong finance","Ivy League","Philadelphia location"]', 97.0 FROM countries c WHERE c.code='USA' ON CONFLICT DO NOTHING;

INSERT INTO universities (country_id, name, short_name, website, location_city, qs_world_rank, acceptance_rate, min_cgpa, min_ielts, min_gre, avg_tuition_usd_per_year, avg_living_cost_usd_per_month, application_fee_usd, programs, intake_months, has_scholarships, overview, strengths, graduate_employment_rate, is_active)
SELECT c.id, 'Princeton University', 'Princeton', 'https://www.princeton.edu', 'Princeton NJ', 13, 4.0, 9.0, 7.5, 325, 56000, 1900, 80,
'[{"name":"MS Computer Science","duration_years":2,"tuition_usd":56000},{"name":"MS Electrical Engineering","duration_years":2,"tuition_usd":56000}]',
'["September"]', true, 'Princeton is an Ivy League research university known for academic excellence and generous financial aid.',
'["Ivy League","Strong research funding","Beautiful campus","Top rankings"]', 97.0 FROM countries c WHERE c.code='USA' ON CONFLICT DO NOTHING;

INSERT INTO universities (country_id, name, short_name, website, location_city, qs_world_rank, acceptance_rate, min_cgpa, min_ielts, min_gre, avg_tuition_usd_per_year, avg_living_cost_usd_per_month, application_fee_usd, programs, intake_months, has_scholarships, overview, strengths, graduate_employment_rate, is_active)
SELECT c.id, 'Yale University', 'Yale', 'https://www.yale.edu', 'New Haven CT', 16, 4.5, 8.5, 7.0, 320, 44000, 1800, 80,
'[{"name":"MS Computer Science","duration_years":2,"tuition_usd":44000},{"name":"MBA (SOM)","duration_years":2,"tuition_usd":72000},{"name":"MS Data Science","duration_years":1,"tuition_usd":44000}]',
'["September"]', true, 'Yale is an Ivy League research university known for its law school, liberal arts, and global leadership programs.',
'["Ivy League","Yale Law #1","Strong humanities","Global network"]', 96.0 FROM countries c WHERE c.code='USA' ON CONFLICT DO NOTHING;

INSERT INTO universities (country_id, name, short_name, website, location_city, qs_world_rank, acceptance_rate, min_cgpa, min_ielts, min_gre, avg_tuition_usd_per_year, avg_living_cost_usd_per_month, application_fee_usd, programs, intake_months, has_scholarships, overview, strengths, graduate_employment_rate, is_active)
SELECT c.id, 'Cornell University', 'Cornell', 'https://www.cornell.edu', 'Ithaca NY', 12, 8.7, 8.0, 7.0, 315, 55000, 1600, 80,
'[{"name":"MS Computer Science","duration_years":2,"tuition_usd":55000},{"name":"MEng Computer Science","duration_years":1,"tuition_usd":55000},{"name":"MBA (Johnson)","duration_years":2,"tuition_usd":68000}]',
'["August","January"]', true, 'Cornell is an Ivy League university with a top-ranked engineering school and a thriving tech ecosystem in NYC.',
'["Ivy League","Top 5 CS","NYC Tech Campus","Strong Indian community"]', 95.0 FROM countries c WHERE c.code='USA' ON CONFLICT DO NOTHING;

INSERT INTO universities (country_id, name, short_name, website, location_city, qs_world_rank, acceptance_rate, min_cgpa, min_ielts, min_gre, avg_tuition_usd_per_year, avg_living_cost_usd_per_month, application_fee_usd, programs, intake_months, has_scholarships, overview, strengths, graduate_employment_rate, is_active)
SELECT c.id, 'University of Michigan Ann Arbor', 'UMich', 'https://umich.edu', 'Ann Arbor MI', 33, 20.0, 7.5, 6.5, 310, 24000, 1200, 75,
'[{"name":"MS Computer Science","duration_years":2,"tuition_usd":24000},{"name":"MS Data Science","duration_years":2,"tuition_usd":24000},{"name":"MBA (Ross)","duration_years":2,"tuition_usd":67000}]',
'["September","January"]', true, 'University of Michigan is a top public research university known for its Ross School of Business and engineering programs.',
'["Top public university","Affordable for out-of-state","Ross MBA","Strong research"]', 93.0 FROM countries c WHERE c.code='USA' ON CONFLICT DO NOTHING;

INSERT INTO universities (country_id, name, short_name, website, location_city, qs_world_rank, acceptance_rate, min_cgpa, min_ielts, min_gre, avg_tuition_usd_per_year, avg_living_cost_usd_per_month, application_fee_usd, programs, intake_months, has_scholarships, overview, strengths, graduate_employment_rate, is_active)
SELECT c.id, 'Georgia Institute of Technology', 'Georgia Tech', 'https://www.gatech.edu', 'Atlanta GA', 97, 16.0, 7.5, 6.5, 310, 14000, 1300, 75,
'[{"name":"MS Computer Science (Online)","duration_years":2,"tuition_usd":7000},{"name":"MS Computer Science","duration_years":2,"tuition_usd":14000},{"name":"MS Data Analytics","duration_years":2,"tuition_usd":14000}]',
'["August","January"]', true, 'Georgia Tech is a top engineering school known for its affordable MSCS program and strong industry placement.',
'["Affordable MSCS","Top 10 CS","FAANG placement","Online options"]', 95.0 FROM countries c WHERE c.code='USA' ON CONFLICT DO NOTHING;

INSERT INTO universities (country_id, name, short_name, website, location_city, qs_world_rank, acceptance_rate, min_cgpa, min_ielts, min_gre, avg_tuition_usd_per_year, avg_living_cost_usd_per_month, application_fee_usd, programs, intake_months, has_scholarships, overview, strengths, graduate_employment_rate, is_active)
SELECT c.id, 'Purdue University', 'Purdue', 'https://www.purdue.edu', 'West Lafayette IN', 109, 60.0, 7.0, 6.5, 305, 28000, 1100, 60,
'[{"name":"MS Computer Science","duration_years":2,"tuition_usd":28000},{"name":"MS Electrical Engineering","duration_years":2,"tuition_usd":28000},{"name":"MS Data Science","duration_years":2,"tuition_usd":28000}]',
'["August","January"]', true, 'Purdue is a top engineering university known for its affordable tuition and strong placement in tech companies.',
'["Affordable","Top engineering","Large Indian community","STEM OPT"]', 92.0 FROM countries c WHERE c.code='USA' ON CONFLICT DO NOTHING;

INSERT INTO universities (country_id, name, short_name, website, location_city, qs_world_rank, acceptance_rate, min_cgpa, min_ielts, min_gre, avg_tuition_usd_per_year, avg_living_cost_usd_per_month, application_fee_usd, programs, intake_months, has_scholarships, overview, strengths, graduate_employment_rate, is_active)
SELECT c.id, 'University of Texas at Austin', 'UT Austin', 'https://www.utexas.edu', 'Austin TX', 67, 32.0, 7.5, 6.5, 308, 20000, 1400, 65,
'[{"name":"MS Computer Science","duration_years":2,"tuition_usd":20000},{"name":"MS Data Science","duration_years":2,"tuition_usd":20000},{"name":"MBA (McCombs)","duration_years":2,"tuition_usd":57000}]',
'["August","January"]', true, 'UT Austin is a top public university in the heart of Austin, the tech hub of Texas.',
'["Austin tech hub","Affordable","Dell Medical","Strong CS"]', 92.0 FROM countries c WHERE c.code='USA' ON CONFLICT DO NOTHING;

INSERT INTO universities (country_id, name, short_name, website, location_city, qs_world_rank, acceptance_rate, min_cgpa, min_ielts, min_gre, avg_tuition_usd_per_year, avg_living_cost_usd_per_month, application_fee_usd, programs, intake_months, has_scholarships, overview, strengths, graduate_employment_rate, is_active)
SELECT c.id, 'University of Washington', 'UW', 'https://www.washington.edu', 'Seattle WA', 85, 52.0, 7.5, 6.5, 308, 22000, 1500, 65,
'[{"name":"MS Computer Science","duration_years":2,"tuition_usd":22000},{"name":"MS Information Management","duration_years":2,"tuition_usd":22000},{"name":"MS Data Science","duration_years":2,"tuition_usd":22000}]',
'["September","March"]', true, 'UW Seattle is surrounded by Amazon, Microsoft, Google, and Boeing — one of the best locations for tech careers.',
'["Seattle tech hub","Amazon/Microsoft proximity","Top CS research","Affordable"]', 94.0 FROM countries c WHERE c.code='USA' ON CONFLICT DO NOTHING;

INSERT INTO universities (country_id, name, short_name, website, location_city, qs_world_rank, acceptance_rate, min_cgpa, min_ielts, min_gre, avg_tuition_usd_per_year, avg_living_cost_usd_per_month, application_fee_usd, programs, intake_months, has_scholarships, overview, strengths, graduate_employment_rate, is_active)
SELECT c.id, 'University of California San Diego', 'UCSD', 'https://ucsd.edu', 'San Diego CA', 65, 34.0, 7.5, 6.5, 308, 32000, 1600, 70,
'[{"name":"MS Computer Science","duration_years":2,"tuition_usd":32000},{"name":"MS Data Science","duration_years":2,"tuition_usd":32000},{"name":"MS Electrical Engineering","duration_years":2,"tuition_usd":32000}]',
'["September"]', true, 'UCSD is a top UC campus known for its computing, biomedical, and engineering programs in sunny San Diego.',
'["Top 5 CS research","Biotech hub","Great weather","Strong industry ties"]', 93.0 FROM countries c WHERE c.code='USA' ON CONFLICT DO NOTHING;

INSERT INTO universities (country_id, name, short_name, website, location_city, qs_world_rank, acceptance_rate, min_cgpa, min_ielts, min_gre, avg_tuition_usd_per_year, avg_living_cost_usd_per_month, application_fee_usd, programs, intake_months, has_scholarships, overview, strengths, graduate_employment_rate, is_active)
SELECT c.id, 'University of California Los Angeles', 'UCLA', 'https://www.ucla.edu', 'Los Angeles CA', 44, 9.0, 8.0, 7.0, 315, 30000, 2000, 70,
'[{"name":"MS Computer Science","duration_years":2,"tuition_usd":30000},{"name":"MBA (Anderson)","duration_years":2,"tuition_usd":68000},{"name":"MS Data Science Engineering","duration_years":2,"tuition_usd":30000}]',
'["September"]', true, 'UCLA is a top UC campus in Los Angeles with strong connections to the entertainment, tech, and healthcare industries.',
'["LA tech scene","Entertainment industry","Top public university","Strong research"]', 93.0 FROM countries c WHERE c.code='USA' ON CONFLICT DO NOTHING;

INSERT INTO universities (country_id, name, short_name, website, location_city, qs_world_rank, acceptance_rate, min_cgpa, min_ielts, min_gre, avg_tuition_usd_per_year, avg_living_cost_usd_per_month, application_fee_usd, programs, intake_months, has_scholarships, overview, strengths, graduate_employment_rate, is_active)
SELECT c.id, 'Arizona State University', 'ASU', 'https://www.asu.edu', 'Tempe AZ', 216, 88.0, 6.5, 6.0, 295, 32000, 1200, 70,
'[{"name":"MS Computer Science","duration_years":2,"tuition_usd":32000},{"name":"MS Software Engineering","duration_years":2,"tuition_usd":32000},{"name":"MS Data Science","duration_years":2,"tuition_usd":32000}]',
'["August","January"]', true, 'ASU is a top innovation university with a high acceptance rate, making it ideal for students with backlogs or lower CGPAs.',
'["High acceptance rate","Innovative programs","STEM OPT","Diverse campus"]', 88.0 FROM countries c WHERE c.code='USA' ON CONFLICT DO NOTHING;

INSERT INTO universities (country_id, name, short_name, website, location_city, qs_world_rank, acceptance_rate, min_cgpa, min_ielts, min_gre, avg_tuition_usd_per_year, avg_living_cost_usd_per_month, application_fee_usd, programs, intake_months, has_scholarships, overview, strengths, graduate_employment_rate, is_active)
SELECT c.id, 'Northeastern University', 'NEU', 'https://www.northeastern.edu', 'Boston MA', 334, 18.0, 7.0, 6.5, 305, 55000, 1800, 100,
'[{"name":"MS Computer Science","duration_years":2,"tuition_usd":55000},{"name":"MS Data Science","duration_years":2,"tuition_usd":55000},{"name":"MS Artificial Intelligence","duration_years":2,"tuition_usd":55000}]',
'["September","January"]', true, 'Northeastern is known for its co-op program giving students 6-month paid industry placements at top companies.',
'["Co-op program","Boston tech scene","Industry placement","Multiple intakes"]', 94.0 FROM countries c WHERE c.code='USA' ON CONFLICT DO NOTHING;

-- ── UK ───────────────────────────────────────────────────────────────────────
INSERT INTO universities (country_id, name, short_name, website, location_city, qs_world_rank, acceptance_rate, min_cgpa, min_ielts, avg_tuition_usd_per_year, avg_living_cost_usd_per_month, application_fee_usd, programs, intake_months, has_scholarships, overview, strengths, graduate_employment_rate, is_active)
SELECT c.id, 'University of Cambridge', 'Cambridge', 'https://www.cam.ac.uk', 'Cambridge', 2, 21.0, 8.5, 7.5, 36000, 1400, 0,
'[{"name":"MPhil Computer Science","duration_years":1,"tuition_usd":36000},{"name":"MBA (Judge)","duration_years":1,"tuition_usd":65000},{"name":"MPhil Machine Learning","duration_years":1,"tuition_usd":36000}]',
'["October"]', true, 'Cambridge is the second-oldest English-speaking university, ranked consistently in the global top 3.',
'["Top 3 globally","Gates Cambridge Scholarship","1-year Masters","Historic prestige"]', 96.0 FROM countries c WHERE c.code='GBR' ON CONFLICT DO NOTHING;

INSERT INTO universities (country_id, name, short_name, website, location_city, qs_world_rank, acceptance_rate, min_cgpa, min_ielts, avg_tuition_usd_per_year, avg_living_cost_usd_per_month, application_fee_usd, programs, intake_months, has_scholarships, overview, strengths, graduate_employment_rate, is_active)
SELECT c.id, 'Imperial College London', 'Imperial', 'https://www.imperial.ac.uk', 'London', 8, 14.0, 8.0, 7.0, 34000, 1800, 0,
'[{"name":"MSc Computing","duration_years":1,"tuition_usd":34000},{"name":"MSc Data Science","duration_years":1,"tuition_usd":34000},{"name":"MSc AI","duration_years":1,"tuition_usd":34000}]',
'["October"]', true, 'Imperial College London is a world-class science and technology university in Central London.',
'["Top 10 globally","STEM focus","London location","Strong industry links"]', 94.0 FROM countries c WHERE c.code='GBR' ON CONFLICT DO NOTHING;

INSERT INTO universities (country_id, name, short_name, website, location_city, qs_world_rank, acceptance_rate, min_cgpa, min_ielts, avg_tuition_usd_per_year, avg_living_cost_usd_per_month, application_fee_usd, programs, intake_months, has_scholarships, overview, strengths, graduate_employment_rate, is_active)
SELECT c.id, 'University College London', 'UCL', 'https://www.ucl.ac.uk', 'London', 9, 63.0, 7.5, 6.5, 30000, 1800, 0,
'[{"name":"MSc Computer Science","duration_years":1,"tuition_usd":30000},{"name":"MSc Artificial Intelligence","duration_years":1,"tuition_usd":30000},{"name":"MSc Data Science","duration_years":1,"tuition_usd":30000}]',
'["September"]', true, 'UCL is a world top-10 university in Central London known for research excellence and a diverse international community.',
'["Top 10 globally","London location","Diverse campus","Strong research"]', 93.0 FROM countries c WHERE c.code='GBR' ON CONFLICT DO NOTHING;

INSERT INTO universities (country_id, name, short_name, website, location_city, qs_world_rank, acceptance_rate, min_cgpa, min_ielts, avg_tuition_usd_per_year, avg_living_cost_usd_per_month, application_fee_usd, programs, intake_months, has_scholarships, overview, strengths, graduate_employment_rate, is_active)
SELECT c.id, 'London School of Economics', 'LSE', 'https://www.lse.ac.uk', 'London', 45, 16.0, 8.0, 7.0, 30000, 1900, 0,
'[{"name":"MSc Data Science","duration_years":1,"tuition_usd":30000},{"name":"MSc Finance","duration_years":1,"tuition_usd":32000},{"name":"MBA","duration_years":1,"tuition_usd":50000}]',
'["September"]', true, 'LSE is the world''s leading social science university, known for its influence on global policy and finance.',
'["#1 Social Sciences","Finance hub","UN/World Bank alumni","London location"]', 94.0 FROM countries c WHERE c.code='GBR' ON CONFLICT DO NOTHING;

INSERT INTO universities (country_id, name, short_name, website, location_city, qs_world_rank, acceptance_rate, min_cgpa, min_ielts, avg_tuition_usd_per_year, avg_living_cost_usd_per_month, application_fee_usd, programs, intake_months, has_scholarships, overview, strengths, graduate_employment_rate, is_active)
SELECT c.id, 'University of Manchester', 'Manchester', 'https://www.manchester.ac.uk', 'Manchester', 32, 57.0, 7.0, 6.5, 26000, 1100, 0,
'[{"name":"MSc Computer Science","duration_years":1,"tuition_usd":26000},{"name":"MSc Data Science","duration_years":1,"tuition_usd":26000},{"name":"MBA","duration_years":1,"tuition_usd":38000}]',
'["September"]', true, 'University of Manchester is a Russell Group university known for its business school and research output.',
'["Russell Group","Affordable city","25 Nobel laureates","Strong industry links"]', 90.0 FROM countries c WHERE c.code='GBR' ON CONFLICT DO NOTHING;

INSERT INTO universities (country_id, name, short_name, website, location_city, qs_world_rank, acceptance_rate, min_cgpa, min_ielts, avg_tuition_usd_per_year, avg_living_cost_usd_per_month, application_fee_usd, programs, intake_months, has_scholarships, overview, strengths, graduate_employment_rate, is_active)
SELECT c.id, 'King''s College London', 'KCL', 'https://www.kcl.ac.uk', 'London', 40, 22.0, 7.5, 6.5, 28000, 1800, 0,
'[{"name":"MSc Computer Science","duration_years":1,"tuition_usd":28000},{"name":"MSc Artificial Intelligence","duration_years":1,"tuition_usd":28000},{"name":"MSc Data Science","duration_years":1,"tuition_usd":28000}]',
'["September"]', true, 'King''s College London is one of the world''s top universities, located in the heart of London.',
'["Top 40 globally","Central London","Strong health sciences","Diverse community"]', 91.0 FROM countries c WHERE c.code='GBR' ON CONFLICT DO NOTHING;

INSERT INTO universities (country_id, name, short_name, website, location_city, qs_world_rank, acceptance_rate, min_cgpa, min_ielts, avg_tuition_usd_per_year, avg_living_cost_usd_per_month, application_fee_usd, programs, intake_months, has_scholarships, overview, strengths, graduate_employment_rate, is_active)
SELECT c.id, 'University of Bristol', 'Bristol', 'https://www.bristol.ac.uk', 'Bristol', 55, 69.0, 7.0, 6.5, 25000, 1100, 0,
'[{"name":"MSc Computer Science","duration_years":1,"tuition_usd":25000},{"name":"MSc Data Science","duration_years":1,"tuition_usd":25000},{"name":"MSc Machine Learning","duration_years":1,"tuition_usd":25000}]',
'["September"]', true, 'University of Bristol is a Russell Group university in one of the UK''s most vibrant student cities.',
'["Russell Group","Vibrant student city","Top 60 globally","Strong research"]', 89.0 FROM countries c WHERE c.code='GBR' ON CONFLICT DO NOTHING;

INSERT INTO universities (country_id, name, short_name, website, location_city, qs_world_rank, acceptance_rate, min_cgpa, min_ielts, avg_tuition_usd_per_year, avg_living_cost_usd_per_month, application_fee_usd, programs, intake_months, has_scholarships, overview, strengths, graduate_employment_rate, is_active)
SELECT c.id, 'University of Warwick', 'Warwick', 'https://www.warwick.ac.uk', 'Coventry', 69, 14.0, 7.5, 6.5, 26000, 1000, 0,
'[{"name":"MSc Computer Science","duration_years":1,"tuition_usd":26000},{"name":"MSc Data Analytics","duration_years":1,"tuition_usd":26000},{"name":"MBA (WBS)","duration_years":1,"tuition_usd":40000}]',
'["October"]', true, 'University of Warwick is one of the UK''s leading universities known for its business school and computing department.',
'["WBS top MBA","Strong CS","Affordable vs London","Research excellence"]', 90.0 FROM countries c WHERE c.code='GBR' ON CONFLICT DO NOTHING;

INSERT INTO universities (country_id, name, short_name, website, location_city, qs_world_rank, acceptance_rate, min_cgpa, min_ielts, avg_tuition_usd_per_year, avg_living_cost_usd_per_month, application_fee_usd, programs, intake_months, has_scholarships, overview, strengths, graduate_employment_rate, is_active)
SELECT c.id, 'University of Glasgow', 'Glasgow', 'https://www.gla.ac.uk', 'Glasgow', 78, 70.0, 6.5, 6.5, 22000, 900, 0,
'[{"name":"MSc Computer Science","duration_years":1,"tuition_usd":22000},{"name":"MSc Data Science","duration_years":1,"tuition_usd":22000},{"name":"MSc AI","duration_years":1,"tuition_usd":22000}]',
'["September"]', true, 'University of Glasgow is one of the oldest universities in the world, located in Scotland''s largest city.',
'["Ancient university","Affordable Scotland","PSW 2 years","Friendly city"]', 88.0 FROM countries c WHERE c.code='GBR' ON CONFLICT DO NOTHING;

-- ── CANADA ───────────────────────────────────────────────────────────────────
INSERT INTO universities (country_id, name, short_name, website, location_city, qs_world_rank, acceptance_rate, min_cgpa, min_ielts, avg_tuition_usd_per_year, avg_living_cost_usd_per_month, application_fee_usd, programs, intake_months, has_scholarships, overview, strengths, graduate_employment_rate, is_active)
SELECT c.id, 'McGill University', 'McGill', 'https://www.mcgill.ca', 'Montreal', 32, 46.0, 7.5, 6.5, 24000, 1000, 110,
'[{"name":"MSc Computer Science","duration_years":2,"tuition_usd":24000},{"name":"MBA (Desautels)","duration_years":2,"tuition_usd":48000},{"name":"MSc Data Science","duration_years":2,"tuition_usd":24000}]',
'["September","January"]', true, 'McGill is Canada''s most international university, consistently ranked among the top 35 universities worldwide.',
'["Top 35 globally","Bilingual city","Affordable","PGWP 3 years"]', 91.0 FROM countries c WHERE c.code='CAN' ON CONFLICT DO NOTHING;

INSERT INTO universities (country_id, name, short_name, website, location_city, qs_world_rank, acceptance_rate, min_cgpa, min_ielts, avg_tuition_usd_per_year, avg_living_cost_usd_per_month, application_fee_usd, programs, intake_months, has_scholarships, overview, strengths, graduate_employment_rate, is_active)
SELECT c.id, 'University of Waterloo', 'Waterloo', 'https://uwaterloo.ca', 'Waterloo', 154, 53.0, 7.5, 7.0, 26000, 1100, 100,
'[{"name":"MEng Computer Engineering","duration_years":1,"tuition_usd":26000},{"name":"MSc Computer Science","duration_years":2,"tuition_usd":26000},{"name":"MS Data Science","duration_years":2,"tuition_usd":26000}]',
'["September","January"]', true, 'University of Waterloo is Canada''s top tech university, known as the "Silicon Valley of the North" with the best co-op program.',
'["#1 tech university Canada","Co-op program","Startup ecosystem","PGWP 3 years"]', 94.0 FROM countries c WHERE c.code='CAN' ON CONFLICT DO NOTHING;

INSERT INTO universities (country_id, name, short_name, website, location_city, qs_world_rank, acceptance_rate, min_cgpa, min_ielts, avg_tuition_usd_per_year, avg_living_cost_usd_per_month, application_fee_usd, programs, intake_months, has_scholarships, overview, strengths, graduate_employment_rate, is_active)
SELECT c.id, 'Western University', 'Western', 'https://www.uwo.ca', 'London Ontario', 211, 57.0, 7.0, 6.5, 20000, 1000, 100,
'[{"name":"MSc Computer Science","duration_years":2,"tuition_usd":20000},{"name":"MBA (Ivey)","duration_years":1,"tuition_usd":70000},{"name":"MSc Data Analytics","duration_years":2,"tuition_usd":20000}]',
'["September"]', true, 'Western University is known for its Ivey Business School, one of the top MBA programs in Canada.',
'["Ivey #1 MBA Canada","PGWP 3 years","Safe city","Strong research"]', 89.0 FROM countries c WHERE c.code='CAN' ON CONFLICT DO NOTHING;

INSERT INTO universities (country_id, name, short_name, website, location_city, qs_world_rank, acceptance_rate, min_cgpa, min_ielts, avg_tuition_usd_per_year, avg_living_cost_usd_per_month, application_fee_usd, programs, intake_months, has_scholarships, overview, strengths, graduate_employment_rate, is_active)
SELECT c.id, 'Simon Fraser University', 'SFU', 'https://www.sfu.ca', 'Burnaby BC', 318, 65.0, 7.0, 6.5, 18000, 1300, 100,
'[{"name":"MSc Computing Science","duration_years":2,"tuition_usd":18000},{"name":"MSc Data Science","duration_years":2,"tuition_usd":18000},{"name":"MBA (Beedie)","duration_years":2,"tuition_usd":38000}]',
'["September","January"]', true, 'SFU is a comprehensive university in metro Vancouver known for its applied research and multiple campuses.',
'["Vancouver proximity","Multiple intakes","Affordable","Co-op programs"]', 88.0 FROM countries c WHERE c.code='CAN' ON CONFLICT DO NOTHING;

INSERT INTO universities (country_id, name, short_name, website, location_city, qs_world_rank, acceptance_rate, min_cgpa, min_ielts, avg_tuition_usd_per_year, avg_living_cost_usd_per_month, application_fee_usd, programs, intake_months, has_scholarships, overview, strengths, graduate_employment_rate, is_active)
SELECT c.id, 'Dalhousie University', 'Dal', 'https://www.dal.ca', 'Halifax NS', 501, 75.0, 6.5, 6.5, 18000, 900, 90,
'[{"name":"MEng Computer Engineering","duration_years":2,"tuition_usd":18000},{"name":"MSc Computer Science","duration_years":2,"tuition_usd":18000},{"name":"MSc Data Science","duration_years":2,"tuition_usd":18000}]',
'["September","January"]', true, 'Dalhousie is a leading research university in Atlantic Canada with lower costs and high acceptance rates.',
'["Lower cost of living","High acceptance","PGWP 3 years","Ocean city"]', 85.0 FROM countries c WHERE c.code='CAN' ON CONFLICT DO NOTHING;

-- ── AUSTRALIA ────────────────────────────────────────────────────────────────
INSERT INTO universities (country_id, name, short_name, website, location_city, qs_world_rank, acceptance_rate, min_cgpa, min_ielts, avg_tuition_usd_per_year, avg_living_cost_usd_per_month, application_fee_usd, programs, intake_months, has_scholarships, overview, strengths, graduate_employment_rate, is_active)
SELECT c.id, 'Australian National University', 'ANU', 'https://www.anu.edu.au', 'Canberra', 34, 35.0, 7.0, 6.5, 30000, 1200, 0,
'[{"name":"Master of Computing","duration_years":2,"tuition_usd":30000},{"name":"Master of Data Science","duration_years":2,"tuition_usd":30000},{"name":"MBA","duration_years":2,"tuition_usd":40000}]',
'["February","July"]', true, 'ANU is Australia''s national university and consistently the highest-ranked Australian university.',
'["#1 in Australia","Government connections","Post-study 4 years","Research excellence"]', 90.0 FROM countries c WHERE c.code='AUS' ON CONFLICT DO NOTHING;

INSERT INTO universities (country_id, name, short_name, website, location_city, qs_world_rank, acceptance_rate, min_cgpa, min_ielts, avg_tuition_usd_per_year, avg_living_cost_usd_per_month, application_fee_usd, programs, intake_months, has_scholarships, overview, strengths, graduate_employment_rate, is_active)
SELECT c.id, 'University of Sydney', 'USyd', 'https://www.sydney.edu.au', 'Sydney', 39, 30.0, 7.0, 6.5, 34000, 1500, 0,
'[{"name":"Master of Information Technology","duration_years":2,"tuition_usd":34000},{"name":"Master of Data Science","duration_years":2,"tuition_usd":34000},{"name":"MBA","duration_years":2,"tuition_usd":45000}]',
'["February","July"]', true, 'University of Sydney is Australia''s oldest university, located in Sydney with strong industry connections.',
'["Top 40 globally","Sydney CBD","Strong alumni","Post-study 4 years"]', 91.0 FROM countries c WHERE c.code='AUS' ON CONFLICT DO NOTHING;

INSERT INTO universities (country_id, name, short_name, website, location_city, qs_world_rank, acceptance_rate, min_cgpa, min_ielts, avg_tuition_usd_per_year, avg_living_cost_usd_per_month, application_fee_usd, programs, intake_months, has_scholarships, overview, strengths, graduate_employment_rate, is_active)
SELECT c.id, 'Monash University', 'Monash', 'https://www.monash.edu', 'Melbourne', 57, 65.0, 6.5, 6.5, 26000, 1200, 0,
'[{"name":"Master of Computer Science","duration_years":2,"tuition_usd":26000},{"name":"Master of Data Science","duration_years":2,"tuition_usd":26000},{"name":"MBA","duration_years":2,"tuition_usd":38000}]',
'["February","July"]', true, 'Monash University is Australia''s largest university with campuses in Melbourne and internationally.',
'["Large network","Multiple intakes","Scholarships available","Post-study 4 years"]', 89.0 FROM countries c WHERE c.code='AUS' ON CONFLICT DO NOTHING;

INSERT INTO universities (country_id, name, short_name, website, location_city, qs_world_rank, acceptance_rate, min_cgpa, min_ielts, avg_tuition_usd_per_year, avg_living_cost_usd_per_month, application_fee_usd, programs, intake_months, has_scholarships, overview, strengths, graduate_employment_rate, is_active)
SELECT c.id, 'University of Queensland', 'UQ', 'https://www.uq.edu.au', 'Brisbane', 47, 40.0, 7.0, 6.5, 28000, 1200, 0,
'[{"name":"Master of Information Technology","duration_years":2,"tuition_usd":28000},{"name":"Master of Data Science","duration_years":2,"tuition_usd":28000},{"name":"MBA","duration_years":2,"tuition_usd":40000}]',
'["February","July"]', true, 'UQ is a top Australian university in Brisbane known for research excellence and strong graduate outcomes.',
'["Top 50 globally","Brisbane lifestyle","Research excellence","Post-study 4 years"]', 90.0 FROM countries c WHERE c.code='AUS' ON CONFLICT DO NOTHING;

INSERT INTO universities (country_id, name, short_name, website, location_city, qs_world_rank, acceptance_rate, min_cgpa, min_ielts, avg_tuition_usd_per_year, avg_living_cost_usd_per_month, application_fee_usd, programs, intake_months, has_scholarships, overview, strengths, graduate_employment_rate, is_active)
SELECT c.id, 'RMIT University', 'RMIT', 'https://www.rmit.edu.au', 'Melbourne', 150, 70.0, 6.0, 6.0, 22000, 1200, 0,
'[{"name":"Master of Computer Science","duration_years":2,"tuition_usd":22000},{"name":"Master of AI","duration_years":2,"tuition_usd":22000},{"name":"Master of Data Science","duration_years":2,"tuition_usd":22000}]',
'["February","July"]', true, 'RMIT is a practice-based university known for its industry connections and high acceptance of international students.',
'["Industry focused","High acceptance","Backlog-friendly","Melbourne CBD"]', 86.0 FROM countries c WHERE c.code='AUS' ON CONFLICT DO NOTHING;

-- ── GERMANY ──────────────────────────────────────────────────────────────────
INSERT INTO universities (country_id, name, short_name, website, location_city, qs_world_rank, acceptance_rate, min_cgpa, min_ielts, avg_tuition_usd_per_year, avg_living_cost_usd_per_month, application_fee_usd, programs, intake_months, has_scholarships, overview, strengths, graduate_employment_rate, is_active)
SELECT c.id, 'Ludwig Maximilian University Munich', 'LMU Munich', 'https://www.lmu.de', 'Munich', 54, 15.0, 7.5, 6.5, 500, 900, 0,
'[{"name":"MSc Computer Science","duration_years":2,"tuition_usd":500},{"name":"MSc Data Science","duration_years":2,"tuition_usd":500},{"name":"MSc Informatics","duration_years":2,"tuition_usd":500}]',
'["October","April"]', true, 'LMU Munich is Germany''s second-ranked university, offering near-free education with world-class research facilities.',
'["Near-free tuition","Top 60 globally","Munich tech scene","DAAD scholarships"]', 93.0 FROM countries c WHERE c.code='DEU' ON CONFLICT DO NOTHING;

INSERT INTO universities (country_id, name, short_name, website, location_city, qs_world_rank, acceptance_rate, min_cgpa, min_ielts, avg_tuition_usd_per_year, avg_living_cost_usd_per_month, application_fee_usd, programs, intake_months, has_scholarships, overview, strengths, graduate_employment_rate, is_active)
SELECT c.id, 'Karlsruhe Institute of Technology', 'KIT', 'https://www.kit.edu', 'Karlsruhe', 119, 20.0, 7.5, 6.5, 500, 800, 0,
'[{"name":"MSc Computer Science","duration_years":2,"tuition_usd":500},{"name":"MSc Electrical Engineering","duration_years":2,"tuition_usd":500},{"name":"MSc Informatics","duration_years":2,"tuition_usd":500}]',
'["October","April"]', true, 'KIT is Germany''s top technology institute, combining a university with a national research center.',
'["Free tuition","Research excellence","Industry partnerships","18-month job seeker visa"]', 92.0 FROM countries c WHERE c.code='DEU' ON CONFLICT DO NOTHING;

INSERT INTO universities (country_id, name, short_name, website, location_city, qs_world_rank, acceptance_rate, min_cgpa, min_ielts, avg_tuition_usd_per_year, avg_living_cost_usd_per_month, application_fee_usd, programs, intake_months, has_scholarships, overview, strengths, graduate_employment_rate, is_active)
SELECT c.id, 'RWTH Aachen University', 'RWTH Aachen', 'https://www.rwth-aachen.de', 'Aachen', 106, 25.0, 7.5, 6.5, 500, 800, 0,
'[{"name":"MSc Computer Science","duration_years":2,"tuition_usd":500},{"name":"MSc Electrical Engineering","duration_years":2,"tuition_usd":500},{"name":"MSc Mechanical Engineering","duration_years":2,"tuition_usd":500}]',
'["October","April"]', true, 'RWTH Aachen is Germany''s largest technical university, known for engineering and close industry partnerships.',
'["Free tuition","Top engineering","Industry focused","18-month job seeker visa"]', 92.0 FROM countries c WHERE c.code='DEU' ON CONFLICT DO NOTHING;

INSERT INTO universities (country_id, name, short_name, website, location_city, qs_world_rank, acceptance_rate, min_cgpa, min_ielts, avg_tuition_usd_per_year, avg_living_cost_usd_per_month, application_fee_usd, programs, intake_months, has_scholarships, overview, strengths, graduate_employment_rate, is_active)
SELECT c.id, 'University of Stuttgart', 'Stuttgart', 'https://www.uni-stuttgart.de', 'Stuttgart', 254, 30.0, 7.0, 6.5, 500, 850, 0,
'[{"name":"MSc Computer Science","duration_years":2,"tuition_usd":500},{"name":"MSc Aerospace Engineering","duration_years":2,"tuition_usd":500},{"name":"MSc Electrical Engineering","duration_years":2,"tuition_usd":500}]',
'["October","April"]', true, 'University of Stuttgart is located in Germany''s automotive hub, home to Mercedes-Benz, Porsche, and Bosch.',
'["Free tuition","Automotive hub","Mercedes/Porsche/Bosch","18-month job seeker visa"]', 90.0 FROM countries c WHERE c.code='DEU' ON CONFLICT DO NOTHING;

INSERT INTO universities (country_id, name, short_name, website, location_city, qs_world_rank, acceptance_rate, min_cgpa, min_ielts, avg_tuition_usd_per_year, avg_living_cost_usd_per_month, application_fee_usd, programs, intake_months, has_scholarships, overview, strengths, graduate_employment_rate, is_active)
SELECT c.id, 'University of Hamburg', 'Uni Hamburg', 'https://www.uni-hamburg.de', 'Hamburg', 302, 50.0, 6.5, 6.0, 500, 900, 0,
'[{"name":"MSc Computer Science","duration_years":2,"tuition_usd":500},{"name":"MSc Data Science","duration_years":2,"tuition_usd":500},{"name":"MSc Business Informatics","duration_years":2,"tuition_usd":500}]',
'["October","April"]', true, 'University of Hamburg is one of Germany''s largest universities in Europe''s second-largest port city.',
'["Free tuition","Backlog-friendly","Hamburg port city","18-month job seeker visa"]', 87.0 FROM countries c WHERE c.code='DEU' ON CONFLICT DO NOTHING;

INSERT INTO universities (country_id, name, short_name, website, location_city, qs_world_rank, acceptance_rate, min_cgpa, min_ielts, avg_tuition_usd_per_year, avg_living_cost_usd_per_month, application_fee_usd, programs, intake_months, has_scholarships, overview, strengths, graduate_employment_rate, is_active)
SELECT c.id, 'Technische Universitat Berlin', 'TU Berlin', 'https://www.tu.berlin', 'Berlin', 154, 30.0, 7.0, 6.5, 500, 1000, 0,
'[{"name":"MSc Computer Science","duration_years":2,"tuition_usd":500},{"name":"MSc Data Engineering","duration_years":2,"tuition_usd":500},{"name":"MSc Information Systems","duration_years":2,"tuition_usd":500}]',
'["October","April"]', true, 'TU Berlin is Germany''s leading technical university located in the startup capital of Europe.',
'["Free tuition","Berlin startup scene","Tech hub","18-month job seeker visa"]', 90.0 FROM countries c WHERE c.code='DEU' ON CONFLICT DO NOTHING;

INSERT INTO universities (country_id, name, short_name, website, location_city, qs_world_rank, acceptance_rate, min_cgpa, min_ielts, avg_tuition_usd_per_year, avg_living_cost_usd_per_month, application_fee_usd, programs, intake_months, has_scholarships, overview, strengths, graduate_employment_rate, is_active)
SELECT c.id, 'Deggendorf Institute of Technology', 'THD', 'https://www.th-deg.de', 'Deggendorf', NULL, 85.0, 6.0, 6.0, 500, 750, 0,
'[{"name":"MSc Artificial Intelligence","duration_years":2,"tuition_usd":500},{"name":"MSc Computer Science","duration_years":2,"tuition_usd":500},{"name":"MSc Data Engineering","duration_years":2,"tuition_usd":500}]',
'["October","April"]', true, 'THD is a modern university of applied sciences with a high acceptance rate, accepting students with backlogs.',
'["Free tuition","Backlog-friendly","High acceptance","18-month job seeker visa"]', 85.0 FROM countries c WHERE c.code='DEU' ON CONFLICT DO NOTHING;

INSERT INTO universities (country_id, name, short_name, website, location_city, qs_world_rank, acceptance_rate, min_cgpa, min_ielts, avg_tuition_usd_per_year, avg_living_cost_usd_per_month, application_fee_usd, programs, intake_months, has_scholarships, overview, strengths, graduate_employment_rate, is_active)
SELECT c.id, 'Hochschule Fulda', 'HS Fulda', 'https://www.hs-fulda.de', 'Fulda', NULL, 88.0, 6.0, 6.0, 500, 750, 0,
'[{"name":"MSc Computer Science","duration_years":2,"tuition_usd":500},{"name":"MSc Applied Computer Science","duration_years":2,"tuition_usd":500}]',
'["October","April"]', true, 'Hochschule Fulda is a university of applied sciences with very high acceptance rates, suitable for students with backlogs.',
'["Free tuition","Very high acceptance","Backlog-friendly","18-month job seeker visa"]', 83.0 FROM countries c WHERE c.code='DEU' ON CONFLICT DO NOTHING;

-- ── IRELAND ───────────────────────────────────────────────────────────────────
INSERT INTO universities (country_id, name, short_name, website, location_city, qs_world_rank, acceptance_rate, min_cgpa, min_ielts, avg_tuition_usd_per_year, avg_living_cost_usd_per_month, application_fee_usd, programs, intake_months, has_scholarships, overview, strengths, graduate_employment_rate, is_active)
SELECT c.id, 'Trinity College Dublin', 'TCD', 'https://www.tcd.ie', 'Dublin', 98, 25.0, 7.5, 6.5, 20000, 1300, 0,
'[{"name":"MSc Computer Science","duration_years":1,"tuition_usd":20000},{"name":"MSc Data Science","duration_years":1,"tuition_usd":20000},{"name":"MBA","duration_years":1,"tuition_usd":28000}]',
'["September"]', true, 'Trinity College Dublin is Ireland''s oldest and most prestigious university, located in the heart of Dublin.',
'["Oldest Irish university","Google/Meta/Microsoft nearby","2-year stay-back","EU location"]', 90.0 FROM countries c WHERE c.code='IRL' ON CONFLICT DO NOTHING;

INSERT INTO universities (country_id, name, short_name, website, location_city, qs_world_rank, acceptance_rate, min_cgpa, min_ielts, avg_tuition_usd_per_year, avg_living_cost_usd_per_month, application_fee_usd, programs, intake_months, has_scholarships, overview, strengths, graduate_employment_rate, is_active)
SELECT c.id, 'University College Dublin', 'UCD', 'https://www.ucd.ie', 'Dublin', 181, 40.0, 7.0, 6.5, 18000, 1300, 0,
'[{"name":"MSc Computer Science","duration_years":1,"tuition_usd":18000},{"name":"MSc Data Analytics","duration_years":1,"tuition_usd":18000},{"name":"MBA (Smurfit)","duration_years":1,"tuition_usd":25000}]',
'["September"]', true, 'UCD is Ireland''s largest university with a globally recognised business school and strong tech industry links.',
'["Smurfit MBA","Tech industry links","2-year stay-back","EU location"]', 89.0 FROM countries c WHERE c.code='IRL' ON CONFLICT DO NOTHING;

-- ── NEW ZEALAND ──────────────────────────────────────────────────────────────
INSERT INTO universities (country_id, name, short_name, website, location_city, qs_world_rank, acceptance_rate, min_cgpa, min_ielts, avg_tuition_usd_per_year, avg_living_cost_usd_per_month, application_fee_usd, programs, intake_months, has_scholarships, overview, strengths, graduate_employment_rate, is_active)
SELECT c.id, 'University of Auckland', 'UoA', 'https://www.auckland.ac.nz', 'Auckland', 68, 62.0, 6.5, 6.0, 22000, 1100, 0,
'[{"name":"Master of Computer Science","duration_years":2,"tuition_usd":22000},{"name":"Master of Data Science","duration_years":2,"tuition_usd":22000},{"name":"MBA","duration_years":2,"tuition_usd":32000}]',
'["February","July"]', true, 'University of Auckland is New Zealand''s top university, offering a multicultural environment and scenic lifestyle.',
'["Top 70 globally","3-year post-study visa","Scenic country","Safe environment"]', 88.0 FROM countries c WHERE c.code='NZL' ON CONFLICT DO NOTHING;

INSERT INTO universities (country_id, name, short_name, website, location_city, qs_world_rank, acceptance_rate, min_cgpa, min_ielts, avg_tuition_usd_per_year, avg_living_cost_usd_per_month, application_fee_usd, programs, intake_months, has_scholarships, overview, strengths, graduate_employment_rate, is_active)
SELECT c.id, 'Victoria University of Wellington', 'VUW', 'https://www.wgtn.ac.nz', 'Wellington', 244, 70.0, 6.5, 6.0, 20000, 1000, 0,
'[{"name":"Master of Computer Science","duration_years":2,"tuition_usd":20000},{"name":"Master of Data Science","duration_years":2,"tuition_usd":20000}]',
'["February","July"]', true, 'VUW is New Zealand''s capital city university, known for law, politics, and computer science.',
'["Capital city","Affordable","3-year post-study visa","Safe country"]', 86.0 FROM countries c WHERE c.code='NZL' ON CONFLICT DO NOTHING;

-- ── SINGAPORE ────────────────────────────────────────────────────────────────
INSERT INTO countries (name, code, avg_tuition_usd_per_year, avg_living_cost_usd_per_month, visa_fee_usd, health_insurance_usd_per_year, post_study_work_years, part_time_hours_per_week, top_ranked_universities_count, language, ielts_min_required, overview, pros, cons, popular_courses, is_active)
VALUES ('Singapore', 'SGP', 20000, 1400, 90, 300, 1, 16, 3, 'English', 6.0,
'Singapore is a global financial and technology hub with world-class universities and a strategic location in Asia.',
'["Top-ranked universities","Safe country","English language","Asia hub"]',
'["High cost of living","Limited post-study work","Small country"]',
'["Computer Science","Finance","Business","Engineering","Biotechnology"]', true)
ON CONFLICT (name) DO NOTHING;

INSERT INTO universities (country_id, name, short_name, website, location_city, qs_world_rank, acceptance_rate, min_cgpa, min_ielts, avg_tuition_usd_per_year, avg_living_cost_usd_per_month, application_fee_usd, programs, intake_months, has_scholarships, overview, strengths, graduate_employment_rate, is_active)
SELECT c.id, 'National University of Singapore', 'NUS', 'https://www.nus.edu.sg', 'Singapore', 8, 18.0, 8.0, 6.5, 22000, 1400, 0,
'[{"name":"MSc Computer Science","duration_years":2,"tuition_usd":22000},{"name":"MSc Data Science","duration_years":2,"tuition_usd":22000},{"name":"MBA","duration_years":2,"tuition_usd":55000}]',
'["August","January"]', true, 'NUS is Asia''s top university and one of the world''s top 10, located in Singapore''s dynamic tech ecosystem.',
'["Top 10 globally","Asia hub","Google/Meta/Amazon offices","Strong research"]', 96.0 FROM countries c WHERE c.code='SGP' ON CONFLICT DO NOTHING;

INSERT INTO universities (country_id, name, short_name, website, location_city, qs_world_rank, acceptance_rate, min_cgpa, min_ielts, avg_tuition_usd_per_year, avg_living_cost_usd_per_month, application_fee_usd, programs, intake_months, has_scholarships, overview, strengths, graduate_employment_rate, is_active)
SELECT c.id, 'Nanyang Technological University', 'NTU', 'https://www.ntu.edu.sg', 'Singapore', 15, 22.0, 7.5, 6.5, 20000, 1400, 0,
'[{"name":"MSc Computer Science","duration_years":2,"tuition_usd":20000},{"name":"MSc AI","duration_years":2,"tuition_usd":20000},{"name":"MSc Data Science","duration_years":2,"tuition_usd":20000}]',
'["August","January"]', true, 'NTU is one of the world''s top 15 universities, known for engineering and business excellence.',
'["Top 15 globally","Engineering excellence","Asia hub","Research funding"]', 95.0 FROM countries c WHERE c.code='SGP' ON CONFLICT DO NOTHING;

-- ── NETHERLANDS ──────────────────────────────────────────────────────────────
INSERT INTO countries (name, code, avg_tuition_usd_per_year, avg_living_cost_usd_per_month, visa_fee_usd, health_insurance_usd_per_year, post_study_work_years, part_time_hours_per_week, top_ranked_universities_count, language, ielts_min_required, overview, pros, cons, popular_courses, is_active)
VALUES ('Netherlands', 'NLD', 14000, 1100, 190, 120, 1, 16, 15, 'English', 6.0,
'The Netherlands offers English-taught programs, a vibrant international student community, and excellent quality of life.',
'["English taught programs","EU work rights","Bicycle culture","International environment"]',
'["High cost in Amsterdam","Limited post-study work","Dutch culture adaptation"]',
'["Computer Science","Business","Engineering","Finance","Data Science"]', true)
ON CONFLICT (name) DO NOTHING;

INSERT INTO universities (country_id, name, short_name, website, location_city, qs_world_rank, acceptance_rate, min_cgpa, min_ielts, avg_tuition_usd_per_year, avg_living_cost_usd_per_month, application_fee_usd, programs, intake_months, has_scholarships, overview, strengths, graduate_employment_rate, is_active)
SELECT c.id, 'Delft University of Technology', 'TU Delft', 'https://www.tudelft.nl', 'Delft', 47, 35.0, 7.5, 6.5, 16000, 1100, 0,
'[{"name":"MSc Computer Science","duration_years":2,"tuition_usd":16000},{"name":"MSc Electrical Engineering","duration_years":2,"tuition_usd":16000},{"name":"MSc Data Science","duration_years":2,"tuition_usd":16000}]',
'["September","February"]', true, 'TU Delft is Europe''s top engineering university, known for research excellence and strong industry partnerships.',
'["Top 50 globally","Engineering excellence","EU work permit","Shell/ASML partnerships"]', 93.0 FROM countries c WHERE c.code='NLD' ON CONFLICT DO NOTHING;

INSERT INTO universities (country_id, name, short_name, website, location_city, qs_world_rank, acceptance_rate, min_cgpa, min_ielts, avg_tuition_usd_per_year, avg_living_cost_usd_per_month, application_fee_usd, programs, intake_months, has_scholarships, overview, strengths, graduate_employment_rate, is_active)
SELECT c.id, 'University of Amsterdam', 'UvA', 'https://www.uva.nl', 'Amsterdam', 55, 55.0, 7.0, 6.5, 14000, 1300, 0,
'[{"name":"MSc Computer Science","duration_years":2,"tuition_usd":14000},{"name":"MSc AI","duration_years":2,"tuition_usd":14000},{"name":"MSc Data Science","duration_years":2,"tuition_usd":14000}]',
'["September","February"]', true, 'University of Amsterdam is a top research university in Europe''s most international city.',
'["Top 60 globally","Amsterdam location","EU work rights","Vibrant city"]', 91.0 FROM countries c WHERE c.code='NLD' ON CONFLICT DO NOTHING;

-- ── SWEDEN ───────────────────────────────────────────────────────────────────
INSERT INTO countries (name, code, avg_tuition_usd_per_year, avg_living_cost_usd_per_month, visa_fee_usd, health_insurance_usd_per_year, post_study_work_years, part_time_hours_per_week, top_ranked_universities_count, language, ielts_min_required, overview, pros, cons, popular_courses, is_active)
VALUES ('Sweden', 'SWE', 15000, 1000, 120, 0, 1, 20, 10, 'English', 6.5,
'Sweden offers free healthcare, high quality of life, and English-taught programs at world-class universities.',
'["High quality of life","English taught programs","Safe country","Strong tech industry"]',
'["High tuition for non-EU students","Expensive living","Dark winters"]',
'["Computer Science","Engineering","Business","Data Science","Sustainability"]', true)
ON CONFLICT (name) DO NOTHING;

INSERT INTO universities (country_id, name, short_name, website, location_city, qs_world_rank, acceptance_rate, min_cgpa, min_ielts, avg_tuition_usd_per_year, avg_living_cost_usd_per_month, application_fee_usd, programs, intake_months, has_scholarships, overview, strengths, graduate_employment_rate, is_active)
SELECT c.id, 'KTH Royal Institute of Technology', 'KTH', 'https://www.kth.se', 'Stockholm', 89, 30.0, 7.5, 6.5, 16000, 1100, 0,
'[{"name":"MSc Computer Science","duration_years":2,"tuition_usd":16000},{"name":"MSc Machine Learning","duration_years":2,"tuition_usd":16000},{"name":"MSc Data Science","duration_years":2,"tuition_usd":16000}]',
'["August"]', true, 'KTH is Scandinavia''s largest technical university, located in Stockholm — home to Spotify, Ericsson, and Klarna.',
'["Top 100 globally","Stockholm tech scene","Spotify/Ericsson","Swedish Institute Scholarship"]', 92.0 FROM countries c WHERE c.code='SWE' ON CONFLICT DO NOTHING;

INSERT INTO universities (country_id, name, short_name, website, location_city, qs_world_rank, acceptance_rate, min_cgpa, min_ielts, avg_tuition_usd_per_year, avg_living_cost_usd_per_month, application_fee_usd, programs, intake_months, has_scholarships, overview, strengths, graduate_employment_rate, is_active)
SELECT c.id, 'Chalmers University of Technology', 'Chalmers', 'https://www.chalmers.se', 'Gothenburg', 171, 35.0, 7.0, 6.5, 15000, 1000, 0,
'[{"name":"MSc Computer Science","duration_years":2,"tuition_usd":15000},{"name":"MSc Software Engineering","duration_years":2,"tuition_usd":15000},{"name":"MSc Data Science","duration_years":2,"tuition_usd":15000}]',
'["September"]', true, 'Chalmers is a leading technology university in Gothenburg with strong automotive and engineering industry links.',
'["Volvo/Volvocars industry","Swedish Institute Scholarship","Strong research","1-year job-seeking visa"]', 90.0 FROM countries c WHERE c.code='SWE' ON CONFLICT DO NOTHING;

-- ── FRANCE ───────────────────────────────────────────────────────────────────
INSERT INTO countries (name, code, avg_tuition_usd_per_year, avg_living_cost_usd_per_month, visa_fee_usd, health_insurance_usd_per_year, post_study_work_years, part_time_hours_per_week, top_ranked_universities_count, language, ielts_min_required, overview, pros, cons, popular_courses, is_active)
VALUES ('France', 'FRA', 3000, 1000, 99, 0, 1, 20, 20, 'French/English', 6.0,
'France offers some of the lowest tuition fees in Europe at public universities, with world-class Grandes Ecoles.',
'["Low tuition","Grandes Ecoles prestige","EU work rights","Cultural experience"]',
'["French language barrier","Limited English programs","Lower starting salaries"]',
'["Business","Engineering","Data Science","Fashion","Arts"]', true)
ON CONFLICT (name) DO NOTHING;

INSERT INTO universities (country_id, name, short_name, website, location_city, qs_world_rank, acceptance_rate, min_cgpa, min_ielts, avg_tuition_usd_per_year, avg_living_cost_usd_per_month, application_fee_usd, programs, intake_months, has_scholarships, overview, strengths, graduate_employment_rate, is_active)
SELECT c.id, 'Ecole Polytechnique', 'Polytechnique', 'https://www.polytechnique.edu', 'Paris', 37, 8.0, 8.5, 7.0, 15000, 1200, 0,
'[{"name":"MSc Data Science for Business","duration_years":2,"tuition_usd":15000},{"name":"MSc Computer Science","duration_years":2,"tuition_usd":15000}]',
'["September"]', true, 'Ecole Polytechnique is France''s most prestigious engineering school, known as the "X".',
'["Top 40 globally","French engineering excellence","EU work rights","Research focus"]', 94.0 FROM countries c WHERE c.code='FRA' ON CONFLICT DO NOTHING;

INSERT INTO universities (country_id, name, short_name, website, location_city, qs_world_rank, acceptance_rate, min_cgpa, min_ielts, avg_tuition_usd_per_year, avg_living_cost_usd_per_month, application_fee_usd, programs, intake_months, has_scholarships, overview, strengths, graduate_employment_rate, is_active)
SELECT c.id, 'HEC Paris', 'HEC', 'https://www.hec.edu', 'Paris', 33, 12.0, 8.0, 7.0, 35000, 1500, 0,
'[{"name":"MBA","duration_years":2,"tuition_usd":75000},{"name":"MSc Data Analytics","duration_years":1,"tuition_usd":35000},{"name":"MSc Management","duration_years":2,"tuition_usd":35000}]',
'["September","January"]', true, 'HEC Paris is Europe''s top business school, consistently ranked among the world''s best MBA programs.',
'["#1 MBA Europe","INSEAD rival","Finance focus","EU work rights"]', 96.0 FROM countries c WHERE c.code='FRA' ON CONFLICT DO NOTHING;

-- ── JAPAN ────────────────────────────────────────────────────────────────────
INSERT INTO countries (name, code, avg_tuition_usd_per_year, avg_living_cost_usd_per_month, visa_fee_usd, health_insurance_usd_per_year, post_study_work_years, part_time_hours_per_week, top_ranked_universities_count, language, ielts_min_required, overview, pros, cons, popular_courses, is_active)
VALUES ('Japan', 'JPN', 8000, 900, 40, 200, 1, 28, 20, 'Japanese/English', 6.0,
'Japan offers low tuition at national universities, a safe environment, and the world''s third-largest economy.',
'["Low tuition","Safe country","Technology leader","MEXT scholarships"]',
'["Japanese language required","Limited English programs","Cultural adaptation"]',
'["Engineering","Computer Science","Robotics","Business","Research"]', true)
ON CONFLICT (name) DO NOTHING;

INSERT INTO universities (country_id, name, short_name, website, location_city, qs_world_rank, acceptance_rate, min_cgpa, min_ielts, avg_tuition_usd_per_year, avg_living_cost_usd_per_month, application_fee_usd, programs, intake_months, has_scholarships, overview, strengths, graduate_employment_rate, is_active)
SELECT c.id, 'University of Tokyo', 'UTokyo', 'https://www.u-tokyo.ac.jp', 'Tokyo', 28, 35.0, 8.0, 6.5, 8000, 1000, 0,
'[{"name":"MS Computer Science","duration_years":2,"tuition_usd":8000},{"name":"MS Engineering","duration_years":2,"tuition_usd":8000},{"name":"MS Data Science","duration_years":2,"tuition_usd":8000}]',
'["April","October"]', true, 'University of Tokyo is Japan''s top university, consistently ranked among Asia''s best institutions.',
'["Top 30 globally","MEXT scholarship","Low tuition","Research excellence"]', 93.0 FROM countries c WHERE c.code='JPN' ON CONFLICT DO NOTHING;

INSERT INTO universities (country_id, name, short_name, website, location_city, qs_world_rank, acceptance_rate, min_cgpa, min_ielts, avg_tuition_usd_per_year, avg_living_cost_usd_per_month, application_fee_usd, programs, intake_months, has_scholarships, overview, strengths, graduate_employment_rate, is_active)
SELECT c.id, 'Kyoto University', 'Kyoto', 'https://www.kyoto-u.ac.jp', 'Kyoto', 46, 40.0, 7.5, 6.5, 8000, 900, 0,
'[{"name":"MS Computer Science","duration_years":2,"tuition_usd":8000},{"name":"MS Informatics","duration_years":2,"tuition_usd":8000}]',
'["April","October"]', true, 'Kyoto University is Japan''s second-ranked university, known for research excellence and 28 Nobel Prize winners.',
'["Top 50 globally","28 Nobel laureates","MEXT scholarship","Historic city"]', 92.0 FROM countries c WHERE c.code='JPN' ON CONFLICT DO NOTHING;

-- ── SOUTH KOREA ──────────────────────────────────────────────────────────────
INSERT INTO countries (name, code, avg_tuition_usd_per_year, avg_living_cost_usd_per_month, visa_fee_usd, health_insurance_usd_per_year, post_study_work_years, part_time_hours_per_week, top_ranked_universities_count, language, ielts_min_required, overview, pros, cons, popular_courses, is_active)
VALUES ('South Korea', 'KOR', 8000, 800, 60, 200, 1, 20, 10, 'Korean/English', 6.0,
'South Korea offers low tuition, cutting-edge technology, and GKFS scholarships covering full study costs.',
'["GKFS full scholarship","Low tuition","Technology leader","Samsung/LG/Hyundai"]',
'["Korean language barrier","Limited English programs","Cultural adaptation"]',
'["Engineering","Computer Science","Business","Technology"]', true)
ON CONFLICT (name) DO NOTHING;

INSERT INTO universities (country_id, name, short_name, website, location_city, qs_world_rank, acceptance_rate, min_cgpa, min_ielts, avg_tuition_usd_per_year, avg_living_cost_usd_per_month, application_fee_usd, programs, intake_months, has_scholarships, overview, strengths, graduate_employment_rate, is_active)
SELECT c.id, 'KAIST', 'KAIST', 'https://www.kaist.ac.kr', 'Daejeon', 65, 24.0, 7.5, 6.5, 5000, 800, 0,
'[{"name":"MS Computer Science","duration_years":2,"tuition_usd":5000},{"name":"MS AI","duration_years":2,"tuition_usd":5000},{"name":"MS Electrical Engineering","duration_years":2,"tuition_usd":5000}]',
'["March","September"]', true, 'KAIST is South Korea''s top science and technology institute, known for AI and robotics research.',
'["Top 70 globally","GKFS scholarship","Low tuition","Samsung/LG connections"]', 93.0 FROM countries c WHERE c.code='KOR' ON CONFLICT DO NOTHING;

INSERT INTO universities (country_id, name, short_name, website, location_city, qs_world_rank, acceptance_rate, min_cgpa, min_ielts, avg_tuition_usd_per_year, avg_living_cost_usd_per_month, application_fee_usd, programs, intake_months, has_scholarships, overview, strengths, graduate_employment_rate, is_active)
SELECT c.id, 'Seoul National University', 'SNU', 'https://www.snu.ac.kr', 'Seoul', 41, 28.0, 7.5, 6.5, 6000, 900, 0,
'[{"name":"MS Computer Science","duration_years":2,"tuition_usd":6000},{"name":"MS Data Science","duration_years":2,"tuition_usd":6000},{"name":"MBA","duration_years":2,"tuition_usd":15000}]',
'["March","September"]', true, 'Seoul National University is South Korea''s most prestigious university, known as the Harvard of Korea.',
'["Top 45 globally","Low tuition","GKFS scholarship","Seoul tech scene"]', 92.0 FROM countries c WHERE c.code='KOR' ON CONFLICT DO NOTHING;

-- ── Update scholarship linked to new universities ─────────────────────────────
UPDATE scholarships SET eligible_countries = '["India","All"]' WHERE eligible_countries = '["All"]';
