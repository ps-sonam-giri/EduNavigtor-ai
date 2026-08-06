"""Seed top universities into EduPilot AI database."""
import psycopg2, json, sys

conn = psycopg2.connect(
    host="localhost", port=5432,
    dbname="edupilot_db", user="edupilot", password="edupilot_pass"
)
cur = conn.cursor()

# ── Add new countries ────────────────────────────────────────
new_countries = [
    ("Singapore","SGP",20000,1400,90,300,1,16,3,"English",6.0,
     "Singapore is a global technology and financial hub with world-class universities.",
     ["Top-ranked universities","Safe country","English language","Asia tech hub"],
     ["High cost of living","Limited post-study work","Small country"],
     ["Computer Science","Finance","Business","Engineering","Biotechnology"]),
    ("Netherlands","NLD",14000,1100,190,120,1,16,15,"English",6.0,
     "The Netherlands offers English-taught programs and excellent quality of life in Europe.",
     ["English taught programs","EU work rights","International environment","Bicycle culture"],
     ["High cost in Amsterdam","Limited post-study work","Dutch adaptation"],
     ["Computer Science","Business","Engineering","Data Science","Finance"]),
    ("Sweden","SWE",15000,1000,120,0,1,20,10,"English",6.5,
     "Sweden offers free healthcare, high quality of life, and English-taught programs.",
     ["High quality of life","English programs","Safe country","Strong tech industry"],
     ["High tuition non-EU","Expensive living","Dark winters"],
     ["Computer Science","Engineering","Business","Data Science","Sustainability"]),
    ("France","FRA",3000,1000,99,0,1,20,20,"French/English",6.0,
     "France offers low tuition at public universities with world-class Grandes Ecoles.",
     ["Low tuition","Grandes Ecoles prestige","EU work rights","Cultural experience"],
     ["French language barrier","Limited English programs","Lower salaries"],
     ["Business","Engineering","Data Science","Fashion","Arts"]),
    ("Japan","JPN",8000,900,40,200,1,28,20,"Japanese/English",6.0,
     "Japan offers low tuition, safety, and MEXT scholarships for international students.",
     ["Low tuition","Safe country","Technology leader","MEXT scholarships"],
     ["Japanese language required","Limited English programs","Cultural adaptation"],
     ["Engineering","Computer Science","Robotics","Business","Research"]),
    ("South Korea","KOR",8000,800,60,200,1,20,10,"Korean/English",6.0,
     "South Korea offers low tuition and GKFS scholarships covering full study costs.",
     ["GKFS full scholarship","Low tuition","Technology leader","Samsung/LG/Hyundai"],
     ["Korean language barrier","Limited English programs","Cultural adaptation"],
     ["Engineering","Computer Science","Business","Technology"]),
]

for row in new_countries:
    cur.execute("""
        INSERT INTO countries (name,code,avg_tuition_usd_per_year,avg_living_cost_usd_per_month,
        visa_fee_usd,health_insurance_usd_per_year,post_study_work_years,part_time_hours_per_week,
        top_ranked_universities_count,language,ielts_min_required,overview,pros,cons,popular_courses,is_active)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,true)
        ON CONFLICT (name) DO NOTHING
    """, (row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],
          row[11],json.dumps(row[12]),json.dumps(row[13]),json.dumps(row[14])))

conn.commit()
print(f"Countries seeded")

# ── University data ──────────────────────────────────────────
# (code, name, short, website, city, qs_rank, accept_rate, min_cgpa, min_ielts,
#  min_gre, tuition, living, app_fee, programs_json, intakes_json,
#  has_sch, overview, strengths_json, emp_rate)
UNIVERSITIES = [
    # USA
    ("USA","Harvard University","Harvard","https://harvard.edu","Cambridge MA",4,3.2,9.0,7.5,325,57000,2200,85,
     '[{"name":"MS CS","duration_years":2,"tuition_usd":57000},{"name":"MBA","duration_years":2,"tuition_usd":73000}]',
     '["September"]',True,"Harvard is the world''s most prestigious university.","[\"Nobel laureates\",\"#1 MBA\",\"Largest endowment\"]",98.0),
    ("USA","California Institute of Technology","Caltech","https://caltech.edu","Pasadena CA",6,3.9,9.0,7.0,330,60000,2000,75,
     '[{"name":"MS CS","duration_years":2,"tuition_usd":60000},{"name":"MS EE","duration_years":2,"tuition_usd":60000}]',
     '["September"]',True,"Caltech is a world-class science and engineering institute.","[\"NASA JPL\",\"Nobel laureates\",\"Top engineering\"]",97.0),
    ("USA","University of Chicago","UChicago","https://uchicago.edu","Chicago IL",21,6.5,8.5,7.0,320,59000,1600,90,
     '[{"name":"MBA Booth","duration_years":2,"tuition_usd":75000},{"name":"MS Statistics","duration_years":1,"tuition_usd":59000}]',
     '["September"]',True,"UChicago is known for its rigorous academics and influential economics department.","[\"#1 MBA Booth\",\"Nobel laureates\",\"Economics\"]",96.0),
    ("USA","Columbia University","Columbia","https://columbia.edu","New York NY",33,3.7,8.5,7.0,320,62000,2500,85,
     '[{"name":"MS CS","duration_years":2,"tuition_usd":62000},{"name":"MBA","duration_years":2,"tuition_usd":78000}]',
     '["September","January"]',True,"Columbia is an Ivy League university in the heart of New York City.","[\"NYC location\",\"Finance hub\",\"Ivy League\"]",96.0),
    ("USA","University of Pennsylvania","Penn","https://upenn.edu","Philadelphia PA",12,5.9,8.5,7.0,320,60000,1800,85,
     '[{"name":"MBA Wharton","duration_years":2,"tuition_usd":82000},{"name":"MS CS","duration_years":2,"tuition_usd":60000}]',
     '["September"]',True,"Penn is home to the world-famous Wharton School of Business.","[\"Wharton #1\",\"Ivy League\",\"Strong finance\"]",97.0),
    ("USA","Princeton University","Princeton","https://princeton.edu","Princeton NJ",13,4.0,9.0,7.5,325,56000,1900,80,
     '[{"name":"MS CS","duration_years":2,"tuition_usd":56000},{"name":"MS EE","duration_years":2,"tuition_usd":56000}]',
     '["September"]',True,"Princeton is an Ivy League university known for research and generous financial aid.","[\"Ivy League\",\"Strong research\",\"Top rankings\"]",97.0),
    ("USA","Yale University","Yale","https://yale.edu","New Haven CT",16,4.5,8.5,7.0,320,44000,1800,80,
     '[{"name":"MS CS","duration_years":2,"tuition_usd":44000},{"name":"MBA SOM","duration_years":2,"tuition_usd":72000}]',
     '["September"]',True,"Yale is an Ivy League university known for its law school and global leadership programs.","[\"Yale Law #1\",\"Ivy League\",\"Strong humanities\"]",96.0),
    ("USA","Cornell University","Cornell","https://cornell.edu","Ithaca NY",12,8.7,8.0,7.0,315,55000,1600,80,
     '[{"name":"MS CS","duration_years":2,"tuition_usd":55000},{"name":"MEng CS","duration_years":1,"tuition_usd":55000}]',
     '["August","January"]',True,"Cornell is an Ivy League university with a top engineering school and NYC tech campus.","[\"Ivy League\",\"Top 5 CS\",\"NYC Tech Campus\"]",95.0),
    ("USA","University of Michigan","UMich","https://umich.edu","Ann Arbor MI",33,20.0,7.5,6.5,310,24000,1200,75,
     '[{"name":"MS CS","duration_years":2,"tuition_usd":24000},{"name":"MBA Ross","duration_years":2,"tuition_usd":67000}]',
     '["September","January"]',True,"UMich is a top public research university with strong business and engineering programs.","[\"Ross MBA\",\"Top public\",\"Affordable\"]",93.0),
    ("USA","Georgia Institute of Technology","Georgia Tech","https://gatech.edu","Atlanta GA",97,16.0,7.5,6.5,310,14000,1300,75,
     '[{"name":"MS CS","duration_years":2,"tuition_usd":14000},{"name":"MS CS Online","duration_years":2,"tuition_usd":7000}]',
     '["August","January"]',True,"Georgia Tech is a top engineering school with the most affordable MSCS program in the US.","[\"Affordable MSCS\",\"Top 10 CS\",\"FAANG placement\",\"Online option\"]",95.0),
    ("USA","Purdue University","Purdue","https://purdue.edu","West Lafayette IN",109,60.0,7.0,6.5,305,28000,1100,60,
     '[{"name":"MS CS","duration_years":2,"tuition_usd":28000},{"name":"MS Data Science","duration_years":2,"tuition_usd":28000}]',
     '["August","January"]',True,"Purdue is a top engineering university known for affordable tuition and strong tech placement.","[\"Affordable\",\"Top engineering\",\"Large Indian community\",\"STEM OPT\"]",92.0),
    ("USA","University of Texas Austin","UT Austin","https://utexas.edu","Austin TX",67,32.0,7.5,6.5,308,20000,1400,65,
     '[{"name":"MS CS","duration_years":2,"tuition_usd":20000},{"name":"MBA McCombs","duration_years":2,"tuition_usd":57000}]',
     '["August","January"]',True,"UT Austin is a top public university in the heart of Austin, the tech hub of Texas.","[\"Austin tech hub\",\"Affordable\",\"Strong CS\"]",92.0),
    ("USA","University of Washington","UW","https://washington.edu","Seattle WA",85,52.0,7.5,6.5,308,22000,1500,65,
     '[{"name":"MS CS","duration_years":2,"tuition_usd":22000},{"name":"MS Data Science","duration_years":2,"tuition_usd":22000}]',
     '["September","March"]',True,"UW Seattle is surrounded by Amazon, Microsoft, and Google.","[\"Seattle tech hub\",\"Amazon/Microsoft nearby\",\"Top CS\"]",94.0),
    ("USA","UC San Diego","UCSD","https://ucsd.edu","San Diego CA",65,34.0,7.5,6.5,308,32000,1600,70,
     '[{"name":"MS CS","duration_years":2,"tuition_usd":32000},{"name":"MS Data Science","duration_years":2,"tuition_usd":32000}]',
     '["September"]',True,"UCSD is a top UC campus known for computing, biomedical, and engineering programs.","[\"Top 5 CS research\",\"Biotech hub\",\"Great weather\"]",93.0),
    ("USA","UCLA","UCLA","https://ucla.edu","Los Angeles CA",44,9.0,8.0,7.0,315,30000,2000,70,
     '[{"name":"MS CS","duration_years":2,"tuition_usd":30000},{"name":"MBA Anderson","duration_years":2,"tuition_usd":68000}]',
     '["September"]',True,"UCLA is a top UC campus in LA with strong entertainment, tech, and healthcare connections.","[\"LA tech scene\",\"Entertainment industry\",\"Top public\"]",93.0),
    ("USA","Arizona State University","ASU","https://asu.edu","Tempe AZ",216,88.0,6.5,6.0,295,32000,1200,70,
     '[{"name":"MS CS","duration_years":2,"tuition_usd":32000},{"name":"MS Software Engineering","duration_years":2,"tuition_usd":32000}]',
     '["August","January"]',True,"ASU has high acceptance rates making it ideal for students with backlogs or lower CGPAs.","[\"High acceptance\",\"Innovative programs\",\"STEM OPT\",\"Backlog-friendly\"]",88.0),
    ("USA","Northeastern University","NEU","https://northeastern.edu","Boston MA",334,18.0,7.0,6.5,305,55000,1800,100,
     '[{"name":"MS CS","duration_years":2,"tuition_usd":55000},{"name":"MS Data Science","duration_years":2,"tuition_usd":55000},{"name":"MS AI","duration_years":2,"tuition_usd":55000}]',
     '["September","January"]',True,"Northeastern is known for its co-op program giving students 6-month paid industry placements.","[\"Co-op program\",\"Boston tech\",\"Industry placement\",\"Multiple intakes\"]",94.0),
    ("USA","University of Southern California","USC","https://usc.edu","Los Angeles CA",149,11.0,7.5,6.5,310,58000,1900,85,
     '[{"name":"MS CS","duration_years":2,"tuition_usd":58000},{"name":"MBA Marshall","duration_years":2,"tuition_usd":68000}]',
     '["August","January"]',True,"USC is a top private university in LA with excellent tech and entertainment industry connections.","[\"LA location\",\"Strong industry\",\"Multiple intakes\",\"Trojan network\"]",93.0),
    ("USA","Stony Brook University","SBU","https://stonybrook.edu","Stony Brook NY",622,41.0,7.0,6.5,305,26000,1500,100,
     '[{"name":"MS CS","duration_years":2,"tuition_usd":26000},{"name":"MS Data Science","duration_years":2,"tuition_usd":26000}]',
     '["August","January"]',True,"Stony Brook is a top public university known for its strong CS program and proximity to NYC.","[\"Affordable public\",\"Near NYC\",\"Strong CS\",\"SUNY system\"]",90.0),
    ("USA","University of Massachusetts Amherst","UMass Amherst","https://umass.edu","Amherst MA",462,64.0,7.0,6.5,305,32000,1200,85,
     '[{"name":"MS CS","duration_years":2,"tuition_usd":32000},{"name":"MS Data Science","duration_years":2,"tuition_usd":32000}]',
     '["September","January"]',True,"UMass Amherst has a strong CS program with excellent research output and a large Indian student community.","[\"Strong CS research\",\"Large Indian community\",\"New England\",\"Affordable\"]",91.0),
]

UK_UNIVERSITIES = [
    ("GBR","University of Cambridge","Cambridge","https://cam.ac.uk","Cambridge",2,21.0,8.5,7.5,None,36000,1400,0,
     '[{"name":"MPhil CS","duration_years":1,"tuition_usd":36000},{"name":"MBA Judge","duration_years":1,"tuition_usd":65000}]',
     '["October"]',True,"Cambridge is the world''s #2 university with 1-year Masters programs.","[\"Top 3 globally\",\"Gates Cambridge Scholarship\",\"1-year Masters\",\"Historic prestige\"]",96.0),
    ("GBR","Imperial College London","Imperial","https://imperial.ac.uk","London",8,14.0,8.0,7.0,None,34000,1800,0,
     '[{"name":"MSc Computing","duration_years":1,"tuition_usd":34000},{"name":"MSc Data Science","duration_years":1,"tuition_usd":34000}]',
     '["October"]',True,"Imperial is a world-class science and technology university in Central London.","[\"Top 10 globally\",\"STEM focus\",\"London location\",\"Strong industry\"]",94.0),
    ("GBR","University College London","UCL","https://ucl.ac.uk","London",9,63.0,7.5,6.5,None,30000,1800,0,
     '[{"name":"MSc CS","duration_years":1,"tuition_usd":30000},{"name":"MSc AI","duration_years":1,"tuition_usd":30000}]',
     '["September"]',True,"UCL is a world top-10 university in Central London.","[\"Top 10 globally\",\"London location\",\"Diverse campus\",\"Strong research\"]",93.0),
    ("GBR","London School of Economics","LSE","https://lse.ac.uk","London",45,16.0,8.0,7.0,None,30000,1900,0,
     '[{"name":"MSc Data Science","duration_years":1,"tuition_usd":30000},{"name":"MSc Finance","duration_years":1,"tuition_usd":32000}]',
     '["September"]',True,"LSE is the world''s leading social science university.","[\"#1 Social Sciences\",\"Finance hub\",\"London location\",\"UN/World Bank alumni\"]",94.0),
    ("GBR","University of Manchester","Manchester","https://manchester.ac.uk","Manchester",32,57.0,7.0,6.5,None,26000,1100,0,
     '[{"name":"MSc CS","duration_years":1,"tuition_usd":26000},{"name":"MBA","duration_years":1,"tuition_usd":38000}]',
     '["September"]',True,"Manchester is a Russell Group university known for business and research.","[\"Russell Group\",\"Affordable city\",\"25 Nobel laureates\"]",90.0),
    ("GBR","King''s College London","KCL","https://kcl.ac.uk","London",40,22.0,7.5,6.5,None,28000,1800,0,
     '[{"name":"MSc CS","duration_years":1,"tuition_usd":28000},{"name":"MSc AI","duration_years":1,"tuition_usd":28000}]',
     '["September"]',True,"KCL is one of the world''s top universities in the heart of London.","[\"Top 40 globally\",\"Central London\",\"Strong health sciences\"]",91.0),
    ("GBR","University of Bristol","Bristol","https://bristol.ac.uk","Bristol",55,69.0,7.0,6.5,None,25000,1100,0,
     '[{"name":"MSc CS","duration_years":1,"tuition_usd":25000},{"name":"MSc Data Science","duration_years":1,"tuition_usd":25000}]',
     '["September"]',True,"Bristol is a Russell Group university in one of the UK''s most vibrant student cities.","[\"Russell Group\",\"Vibrant city\",\"Top 60 globally\"]",89.0),
    ("GBR","University of Warwick","Warwick","https://warwick.ac.uk","Coventry",69,14.0,7.5,6.5,None,26000,1000,0,
     '[{"name":"MSc CS","duration_years":1,"tuition_usd":26000},{"name":"MBA WBS","duration_years":1,"tuition_usd":40000}]',
     '["October"]',True,"Warwick is one of the UK''s leading universities known for its business school.","[\"WBS top MBA\",\"Strong CS\",\"Affordable vs London\"]",90.0),
    ("GBR","University of Glasgow","Glasgow","https://gla.ac.uk","Glasgow",78,70.0,6.5,6.5,None,22000,900,0,
     '[{"name":"MSc CS","duration_years":1,"tuition_usd":22000},{"name":"MSc Data Science","duration_years":1,"tuition_usd":22000}]',
     '["September"]',True,"Glasgow is one of the oldest universities in the world in Scotland''s largest city.","[\"Ancient university\",\"Affordable Scotland\",\"PSW 2 years\"]",88.0),
    ("GBR","University of Nottingham","Nottingham","https://nottingham.ac.uk","Nottingham",110,71.0,7.0,6.0,None,22000,1000,0,
     '[{"name":"MSc CS","duration_years":1,"tuition_usd":22000},{"name":"MSc Data Science","duration_years":1,"tuition_usd":22000}]',
     '["September"]',True,"Nottingham is a top UK university with campuses in the UK, China and Malaysia.","[\"Global campuses\",\"Affordable\",\"Strong research\",\"Russell Group\"]",88.0),
    ("GBR","University of Sheffield","Sheffield","https://sheffield.ac.uk","Sheffield",105,72.0,6.5,6.0,None,21000,900,0,
     '[{"name":"MSc CS","duration_years":1,"tuition_usd":21000},{"name":"MSc AI","duration_years":1,"tuition_usd":21000}]',
     '["September"]',True,"Sheffield is a Russell Group university known for engineering excellence.","[\"Russell Group\",\"Affordable\",\"Engineering excellence\",\"PSW 2 years\"]",87.0),
    ("GBR","Queen Mary University London","QMUL","https://qmul.ac.uk","London",150,52.0,7.0,6.5,None,24000,1700,0,
     '[{"name":"MSc CS","duration_years":1,"tuition_usd":24000},{"name":"MSc Data Science","duration_years":1,"tuition_usd":24000}]',
     '["September"]',True,"QMUL is a research-intensive university in East London with great tech industry links.","[\"London location\",\"Affordable vs central\",\"Tech industry links\",\"PSW 2 years\"]",87.0),
]

CANADA_UNIVERSITIES = [
    ("CAN","McGill University","McGill","https://mcgill.ca","Montreal",32,46.0,7.5,6.5,None,24000,1000,110,
     '[{"name":"MSc CS","duration_years":2,"tuition_usd":24000},{"name":"MBA Desautels","duration_years":2,"tuition_usd":48000}]',
     '["September","January"]',True,"McGill is Canada''s most international university ranked top 35 worldwide.","[\"Top 35 globally\",\"Bilingual city\",\"Affordable\",\"PGWP 3 years\"]",91.0),
    ("CAN","University of Waterloo","Waterloo","https://uwaterloo.ca","Waterloo",154,53.0,7.5,7.0,None,26000,1100,100,
     '[{"name":"MEng CS","duration_years":1,"tuition_usd":26000},{"name":"MSc CS","duration_years":2,"tuition_usd":26000}]',
     '["September","January"]',True,"Waterloo is Canada''s top tech university with the best co-op program.","[\"#1 tech Canada\",\"Co-op program\",\"Startup ecosystem\",\"PGWP 3 years\"]",94.0),
    ("CAN","Western University","Western","https://uwo.ca","London Ontario",211,57.0,7.0,6.5,None,20000,1000,100,
     '[{"name":"MSc CS","duration_years":2,"tuition_usd":20000},{"name":"MBA Ivey","duration_years":1,"tuition_usd":70000}]',
     '["September"]',True,"Western is known for its Ivey Business School, top MBA program in Canada.","[\"Ivey #1 MBA\",\"PGWP 3 years\",\"Safe city\"]",89.0),
    ("CAN","Simon Fraser University","SFU","https://sfu.ca","Burnaby BC",318,65.0,7.0,6.5,None,18000,1300,100,
     '[{"name":"MSc Computing Science","duration_years":2,"tuition_usd":18000},{"name":"MSc Data Science","duration_years":2,"tuition_usd":18000}]',
     '["September","January"]',True,"SFU is a comprehensive university in metro Vancouver with multiple campuses.","[\"Vancouver proximity\",\"Multiple intakes\",\"Affordable\",\"Co-op programs\"]",88.0),
    ("CAN","Dalhousie University","Dal","https://dal.ca","Halifax NS",501,75.0,6.5,6.5,None,18000,900,90,
     '[{"name":"MEng CS","duration_years":2,"tuition_usd":18000},{"name":"MSc CS","duration_years":2,"tuition_usd":18000}]',
     '["September","January"]',True,"Dalhousie is a leading research university in Atlantic Canada with lower costs.","[\"Lower cost\",\"High acceptance\",\"PGWP 3 years\",\"Ocean city\"]",85.0),
    ("CAN","University of Calgary","UCalgary","https://ucalgary.ca","Calgary AB",291,55.0,7.0,6.5,None,16000,1100,100,
     '[{"name":"MSc CS","duration_years":2,"tuition_usd":16000},{"name":"MBA Haskayne","duration_years":2,"tuition_usd":35000}]',
     '["September","January"]',True,"University of Calgary is a leading Canadian university in the energy capital of Canada.","[\"Affordable\",\"Energy sector\",\"PGWP 3 years\",\"Growing tech scene\"]",87.0),
    ("CAN","University of Ottawa","uOttawa","https://uottawa.ca","Ottawa ON",379,66.0,6.5,6.5,None,17000,1100,75,
     '[{"name":"MSc CS","duration_years":2,"tuition_usd":17000},{"name":"MSc Data Science","duration_years":2,"tuition_usd":17000}]',
     '["September","January"]',True,"Ottawa is Canada''s capital city university with bilingual English/French programs.","[\"Capital city\",\"Bilingual\",\"PGWP 3 years\",\"Government connections\"]",86.0),
]

AUS_UNIVERSITIES = [
    ("AUS","Australian National University","ANU","https://anu.edu.au","Canberra",34,35.0,7.0,6.5,None,30000,1200,0,
     '[{"name":"Master Computing","duration_years":2,"tuition_usd":30000},{"name":"Master Data Science","duration_years":2,"tuition_usd":30000}]',
     '["February","July"]',True,"ANU is Australia''s national university and highest-ranked institution.","[\"#1 Australia\",\"Government connections\",\"Post-study 4 years\",\"Research excellence\"]",90.0),
    ("AUS","University of Sydney","USyd","https://sydney.edu.au","Sydney",39,30.0,7.0,6.5,None,34000,1500,0,
     '[{"name":"Master IT","duration_years":2,"tuition_usd":34000},{"name":"Master Data Science","duration_years":2,"tuition_usd":34000}]',
     '["February","July"]',True,"USyd is Australia''s oldest university in Sydney with strong industry connections.","[\"Top 40 globally\",\"Sydney CBD\",\"Strong alumni\",\"Post-study 4 years\"]",91.0),
    ("AUS","Monash University","Monash","https://monash.edu","Melbourne",57,65.0,6.5,6.5,None,26000,1200,0,
     '[{"name":"Master CS","duration_years":2,"tuition_usd":26000},{"name":"Master Data Science","duration_years":2,"tuition_usd":26000}]',
     '["February","July"]',True,"Monash is Australia''s largest university with multiple campuses.","[\"Large network\",\"Multiple intakes\",\"Scholarships\",\"Post-study 4 years\"]",89.0),
    ("AUS","University of Queensland","UQ","https://uq.edu.au","Brisbane",47,40.0,7.0,6.5,None,28000,1200,0,
     '[{"name":"Master IT","duration_years":2,"tuition_usd":28000},{"name":"Master Data Science","duration_years":2,"tuition_usd":28000}]',
     '["February","July"]',True,"UQ is a top Australian university in Brisbane known for research excellence.","[\"Top 50 globally\",\"Brisbane lifestyle\",\"Research excellence\",\"Post-study 4 years\"]",90.0),
    ("AUS","RMIT University","RMIT","https://rmit.edu.au","Melbourne",150,70.0,6.0,6.0,None,22000,1200,0,
     '[{"name":"Master CS","duration_years":2,"tuition_usd":22000},{"name":"Master AI","duration_years":2,"tuition_usd":22000}]',
     '["February","July"]',True,"RMIT is a practice-based university with high acceptance of international students.","[\"Industry focused\",\"High acceptance\",\"Backlog-friendly\",\"Melbourne CBD\"]",86.0),
    ("AUS","Deakin University","Deakin","https://deakin.edu.au","Melbourne",511,75.0,6.0,6.0,None,20000,1100,0,
     '[{"name":"Master CS","duration_years":2,"tuition_usd":20000},{"name":"Master Data Analytics","duration_years":2,"tuition_usd":20000}]',
     '["February","July"]',True,"Deakin is known for its online programs and flexible learning with high acceptance rates.","[\"Flexible learning\",\"High acceptance\",\"Affordable\",\"Post-study 4 years\"]",84.0),
    ("AUS","Macquarie University","Macquarie","https://mq.edu.au","Sydney",195,67.0,6.5,6.0,None,26000,1500,0,
     '[{"name":"Master CS","duration_years":2,"tuition_usd":26000},{"name":"Master Data Science","duration_years":2,"tuition_usd":26000}]',
     '["February","July"]',True,"Macquarie is a top Sydney university known for its corporate and finance connections.","[\"Sydney location\",\"Finance connections\",\"Post-study 4 years\",\"Modern campus\"]",87.0),
]

GER_UNIVERSITIES = [
    ("DEU","Ludwig Maximilian University Munich","LMU Munich","https://lmu.de","Munich",54,15.0,7.5,6.5,None,500,900,0,
     '[{"name":"MSc CS","duration_years":2,"tuition_usd":500},{"name":"MSc Informatics","duration_years":2,"tuition_usd":500}]',
     '["October","April"]',True,"LMU Munich is Germany''s second-ranked university with near-free education.","[\"Near-free tuition\",\"Top 60 globally\",\"Munich tech scene\",\"DAAD scholarships\"]",93.0),
    ("DEU","Karlsruhe Institute of Technology","KIT","https://kit.edu","Karlsruhe",119,20.0,7.5,6.5,None,500,800,0,
     '[{"name":"MSc CS","duration_years":2,"tuition_usd":500},{"name":"MSc EE","duration_years":2,"tuition_usd":500}]',
     '["October","April"]',True,"KIT is Germany''s top technology institute combining university with national research.","[\"Free tuition\",\"Research excellence\",\"Industry partnerships\",\"18-month job seeker visa\"]",92.0),
    ("DEU","RWTH Aachen University","RWTH Aachen","https://rwth-aachen.de","Aachen",106,25.0,7.5,6.5,None,500,800,0,
     '[{"name":"MSc CS","duration_years":2,"tuition_usd":500},{"name":"MSc Mechanical Engineering","duration_years":2,"tuition_usd":500}]',
     '["October","April"]',True,"RWTH Aachen is Germany''s largest technical university with strong industry partnerships.","[\"Free tuition\",\"Top engineering\",\"Industry focused\",\"18-month job seeker visa\"]",92.0),
    ("DEU","Technische Universitat Berlin","TU Berlin","https://tu.berlin","Berlin",154,30.0,7.0,6.5,None,500,1000,0,
     '[{"name":"MSc CS","duration_years":2,"tuition_usd":500},{"name":"MSc Data Engineering","duration_years":2,"tuition_usd":500}]',
     '["October","April"]',True,"TU Berlin is Germany''s top technical university in Europe''s startup capital.","[\"Free tuition\",\"Berlin startup scene\",\"Tech hub\",\"18-month job seeker visa\"]",90.0),
    ("DEU","University of Stuttgart","Stuttgart","https://uni-stuttgart.de","Stuttgart",254,30.0,7.0,6.5,None,500,850,0,
     '[{"name":"MSc CS","duration_years":2,"tuition_usd":500},{"name":"MSc Automotive Engineering","duration_years":2,"tuition_usd":500}]',
     '["October","April"]',True,"Stuttgart is in Germany''s automotive hub, home to Mercedes-Benz, Porsche, and Bosch.","[\"Free tuition\",\"Automotive hub\",\"Mercedes/Porsche\",\"18-month job seeker visa\"]",90.0),
    ("DEU","University of Hamburg","Uni Hamburg","https://uni-hamburg.de","Hamburg",302,50.0,6.5,6.0,None,500,900,0,
     '[{"name":"MSc CS","duration_years":2,"tuition_usd":500},{"name":"MSc Data Science","duration_years":2,"tuition_usd":500}]',
     '["October","April"]',True,"University of Hamburg is Germany''s largest university in Europe''s second-largest port city.","[\"Free tuition\",\"Backlog-friendly\",\"Hamburg port city\",\"18-month job seeker visa\"]",87.0),
    ("DEU","Deggendorf Institute of Technology","THD","https://th-deg.de","Deggendorf",None,85.0,6.0,6.0,None,500,750,0,
     '[{"name":"MSc AI","duration_years":2,"tuition_usd":500},{"name":"MSc CS","duration_years":2,"tuition_usd":500}]',
     '["October","April"]',True,"THD is a modern university of applied sciences with a high acceptance rate.","[\"Free tuition\",\"Backlog-friendly\",\"High acceptance\",\"18-month job seeker visa\"]",85.0),
    ("DEU","Hochschule Fulda","HS Fulda","https://hs-fulda.de","Fulda",None,88.0,6.0,6.0,None,500,750,0,
     '[{"name":"MSc CS","duration_years":2,"tuition_usd":500},{"name":"MSc Applied CS","duration_years":2,"tuition_usd":500}]',
     '["October","April"]',True,"HS Fulda is a university of applied sciences with very high acceptance rates.","[\"Free tuition\",\"Very high acceptance\",\"Backlog-friendly\",\"18-month job seeker visa\"]",83.0),
    ("DEU","Hochschule Anhalt","HA","https://hs-anhalt.de","Kothen",None,90.0,6.0,6.0,None,500,700,0,
     '[{"name":"MSc CS","duration_years":2,"tuition_usd":500},{"name":"MSc AI","duration_years":2,"tuition_usd":500}]',
     '["October","April"]',True,"Hochschule Anhalt is a university of applied sciences accepting students with backlogs.","[\"Free tuition\",\"Backlog-friendly\",\"Very high acceptance\",\"18-month job seeker visa\"]",82.0),
]

OTHER_UNIVERSITIES = [
    # Ireland
    ("IRL","Trinity College Dublin","TCD","https://tcd.ie","Dublin",98,25.0,7.5,6.5,None,20000,1300,0,
     '[{"name":"MSc CS","duration_years":1,"tuition_usd":20000},{"name":"MSc Data Science","duration_years":1,"tuition_usd":20000}]',
     '["September"]',True,"Trinity is Ireland''s oldest and most prestigious university.","[\"Oldest Irish university\",\"Google/Meta nearby\",\"2-year stay-back\",\"EU location\"]",90.0),
    ("IRL","University College Dublin","UCD","https://ucd.ie","Dublin",181,40.0,7.0,6.5,None,18000,1300,0,
     '[{"name":"MSc CS","duration_years":1,"tuition_usd":18000},{"name":"MBA Smurfit","duration_years":1,"tuition_usd":25000}]',
     '["September"]',True,"UCD is Ireland''s largest university with globally recognised business school.","[\"Smurfit MBA\",\"Tech industry\",\"2-year stay-back\",\"EU location\"]",89.0),
    # New Zealand
    ("NZL","University of Auckland","UoA","https://auckland.ac.nz","Auckland",68,62.0,6.5,6.0,None,22000,1100,0,
     '[{"name":"Master CS","duration_years":2,"tuition_usd":22000},{"name":"Master Data Science","duration_years":2,"tuition_usd":22000}]',
     '["February","July"]',True,"Auckland is NZ''s top university offering multicultural environment.","[\"Top 70 globally\",\"3-year post-study\",\"Scenic country\",\"Safe\"]",88.0),
    ("NZL","Victoria University Wellington","VUW","https://wgtn.ac.nz","Wellington",244,70.0,6.5,6.0,None,20000,1000,0,
     '[{"name":"Master CS","duration_years":2,"tuition_usd":20000},{"name":"Master Data Science","duration_years":2,"tuition_usd":20000}]',
     '["February","July"]',True,"VUW is NZ''s capital city university known for law, politics and CS.","[\"Capital city\",\"Affordable\",\"3-year post-study\",\"Safe country\"]",86.0),
    # Singapore
    ("SGP","National University of Singapore","NUS","https://nus.edu.sg","Singapore",8,18.0,8.0,6.5,None,22000,1400,0,
     '[{"name":"MSc CS","duration_years":2,"tuition_usd":22000},{"name":"MSc Data Science","duration_years":2,"tuition_usd":22000}]',
     '["August","January"]',True,"NUS is Asia''s top university and world top 10.","[\"Top 10 globally\",\"Asia hub\",\"Google/Meta offices\",\"Strong research\"]",96.0),
    ("SGP","Nanyang Technological University","NTU","https://ntu.edu.sg","Singapore",15,22.0,7.5,6.5,None,20000,1400,0,
     '[{"name":"MSc CS","duration_years":2,"tuition_usd":20000},{"name":"MSc AI","duration_years":2,"tuition_usd":20000}]',
     '["August","January"]',True,"NTU is one of the world''s top 15 universities, known for engineering and business.","[\"Top 15 globally\",\"Engineering excellence\",\"Asia hub\",\"Research funding\"]",95.0),
    # Netherlands
    ("NLD","Delft University of Technology","TU Delft","https://tudelft.nl","Delft",47,35.0,7.5,6.5,None,16000,1100,0,
     '[{"name":"MSc CS","duration_years":2,"tuition_usd":16000},{"name":"MSc EE","duration_years":2,"tuition_usd":16000}]',
     '["September","February"]',True,"TU Delft is Europe''s top engineering university.","[\"Top 50 globally\",\"Engineering excellence\",\"EU work permit\",\"Shell/ASML\"]",93.0),
    ("NLD","University of Amsterdam","UvA","https://uva.nl","Amsterdam",55,55.0,7.0,6.5,None,14000,1300,0,
     '[{"name":"MSc CS","duration_years":2,"tuition_usd":14000},{"name":"MSc AI","duration_years":2,"tuition_usd":14000}]',
     '["September","February"]',True,"UvA is a top research university in Europe''s most international city.","[\"Top 60 globally\",\"Amsterdam location\",\"EU work rights\",\"Vibrant city\"]",91.0),
    # Sweden
    ("SWE","KTH Royal Institute of Technology","KTH","https://kth.se","Stockholm",89,30.0,7.5,6.5,None,16000,1100,0,
     '[{"name":"MSc CS","duration_years":2,"tuition_usd":16000},{"name":"MSc Machine Learning","duration_years":2,"tuition_usd":16000}]',
     '["August"]',True,"KTH is Scandinavia''s largest technical university in Stockholm.","[\"Top 100 globally\",\"Stockholm tech\",\"Spotify/Ericsson\",\"Swedish Institute Scholarship\"]",92.0),
    ("SWE","Chalmers University of Technology","Chalmers","https://chalmers.se","Gothenburg",171,35.0,7.0,6.5,None,15000,1000,0,
     '[{"name":"MSc CS","duration_years":2,"tuition_usd":15000},{"name":"MSc Data Science","duration_years":2,"tuition_usd":15000}]',
     '["September"]',True,"Chalmers is a leading technology university with strong automotive industry links.","[\"Volvo/Volvocars industry\",\"Swedish Scholarship\",\"Strong research\",\"Job-seeking visa\"]",90.0),
    # France
    ("FRA","Ecole Polytechnique","Polytechnique","https://polytechnique.edu","Paris",37,8.0,8.5,7.0,None,15000,1200,0,
     '[{"name":"MSc Data Science","duration_years":2,"tuition_usd":15000},{"name":"MSc CS","duration_years":2,"tuition_usd":15000}]',
     '["September"]',True,"Ecole Polytechnique is France''s most prestigious engineering school.","[\"Top 40 globally\",\"French engineering excellence\",\"EU work rights\"]",94.0),
    ("FRA","HEC Paris","HEC","https://hec.edu","Paris",33,12.0,8.0,7.0,None,35000,1500,0,
     '[{"name":"MBA","duration_years":2,"tuition_usd":75000},{"name":"MSc Management","duration_years":2,"tuition_usd":35000}]',
     '["September","January"]',True,"HEC Paris is Europe''s top business school.","[\"#1 MBA Europe\",\"Finance focus\",\"EU work rights\",\"Paris location\"]",96.0),
    # Japan
    ("JPN","University of Tokyo","UTokyo","https://u-tokyo.ac.jp","Tokyo",28,35.0,8.0,6.5,None,8000,1000,0,
     '[{"name":"MS CS","duration_years":2,"tuition_usd":8000},{"name":"MS Engineering","duration_years":2,"tuition_usd":8000}]',
     '["April","October"]',True,"UTokyo is Japan''s top university ranked among Asia''s best.","[\"Top 30 globally\",\"MEXT scholarship\",\"Low tuition\",\"Research excellence\"]",93.0),
    ("JPN","Kyoto University","Kyoto","https://kyoto-u.ac.jp","Kyoto",46,40.0,7.5,6.5,None,8000,900,0,
     '[{"name":"MS CS","duration_years":2,"tuition_usd":8000},{"name":"MS Informatics","duration_years":2,"tuition_usd":8000}]',
     '["April","October"]',True,"Kyoto University is Japan''s second-ranked university with 28 Nobel Prize winners.","[\"Top 50 globally\",\"28 Nobel laureates\",\"MEXT scholarship\",\"Historic city\"]",92.0),
    # South Korea
    ("KOR","KAIST","KAIST","https://kaist.ac.kr","Daejeon",65,24.0,7.5,6.5,None,5000,800,0,
     '[{"name":"MS CS","duration_years":2,"tuition_usd":5000},{"name":"MS AI","duration_years":2,"tuition_usd":5000}]',
     '["March","September"]',True,"KAIST is South Korea''s top science and technology institute.","[\"Top 70 globally\",\"GKFS scholarship\",\"Low tuition\",\"Samsung/LG connections\"]",93.0),
    ("KOR","Seoul National University","SNU","https://snu.ac.kr","Seoul",41,28.0,7.5,6.5,None,6000,900,0,
     '[{"name":"MS CS","duration_years":2,"tuition_usd":6000},{"name":"MS Data Science","duration_years":2,"tuition_usd":6000}]',
     '["March","September"]',True,"SNU is South Korea''s most prestigious university.","[\"Top 45 globally\",\"Low tuition\",\"GKFS scholarship\",\"Seoul tech scene\"]",92.0),
]

# ── Insert all universities ──────────────────────────────────
def insert_unis(unis, default_min_gre=None):
    inserted = 0
    for row in unis:
        code = row[0]
        cur.execute("SELECT id FROM countries WHERE code=%s", (code,))
        country = cur.fetchone()
        if not country:
            print(f"  SKIP: country {code} not found")
            continue
        country_id = country[0]
        # row: code, name, short, website, city, qs_rank, accept_rate, min_cgpa,
        #      min_ielts, min_gre, tuition, living, app_fee, programs, intakes,
        #      has_sch, overview, strengths, emp_rate
        min_gre = row[9] if row[9] is not None else default_min_gre
        try:
            cur.execute("""
                INSERT INTO universities
                (country_id,name,short_name,website,location_city,qs_world_rank,
                 acceptance_rate,min_cgpa,min_ielts,min_gre,
                 avg_tuition_usd_per_year,avg_living_cost_usd_per_month,application_fee_usd,
                 programs,intake_months,has_scholarships,overview,strengths,
                 graduate_employment_rate,is_active)
                SELECT %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,true
                WHERE NOT EXISTS (SELECT 1 FROM universities WHERE name=%s)
            """, (country_id,row[1],row[2],row[3],row[4],row[5],row[6],row[7],
                  row[8],min_gre,row[10],row[11],row[12],row[13],row[14],
                  row[15],row[16],row[17],row[18],row[1]))
            inserted += cur.rowcount
        except Exception as e:
            print(f"  ERROR inserting {row[1]}: {e}")
            conn.rollback()
    conn.commit()
    return inserted

all_groups = [
    (UNIVERSITIES, None),
    (UK_UNIVERSITIES, None),
    (CANADA_UNIVERSITIES, None),
    (AUS_UNIVERSITIES, None),
    (GER_UNIVERSITIES, None),
    (OTHER_UNIVERSITIES, None),
]

total = 0
for group, default_gre in all_groups:
    n = insert_unis(group, default_gre)
    total += n

print(f"\n✅ Done! {total} new universities inserted.")

# Check total
cur.execute("SELECT COUNT(*) FROM universities")
print(f"   Total universities in DB: {cur.fetchone()[0]}")
cur.execute("SELECT COUNT(*) FROM countries")
print(f"   Total countries in DB: {cur.fetchone()[0]}")

cur.close()
conn.close()
