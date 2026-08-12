"""Seed top universities worldwide into EduPilot AI database."""
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
    ("Switzerland","CHE",2000,1800,100,200,1,15,5,"German/French/English",6.5,
     "Switzerland is home to world top-10 universities like ETH Zurich with affordable tuition.",
     ["World top 10 universities","Low tuition fees","High salary potential","Innovation hub"],
     ["High cost of living","Competitive admission","Strict visa regulations"],
     ["Computer Science","Engineering","Finance","Physics","Biotechnology"]),
    ("Italy","ITA",2000,900,80,150,1,20,10,"Italian/English",6.0,
     "Italy offers low tuition fees at public universities and generous DSU government scholarships.",
     ["Low tuition","DSU full scholarships","EU post-study rights","Rich cultural heritage"],
     ["Bureaucracy","Italian language required for job market","Slower economy"],
     ["Engineering","Architecture","Fashion","Design","Computer Science"]),
    ("Spain","ESP",3000,900,80,150,1,20,10,"Spanish/English",6.0,
     "Spain provides top business schools, low cost of living, and access to European labor market.",
     ["Top business schools","Vibrant lifestyle","Low living costs","EU work rights"],
     ["Spanish language needed for local jobs","Higher youth unemployment","Warm summer heat"],
     ["Business","Computer Science","Data Science","Tourism","Biotechnology"]),
    ("United Arab Emirates","ARE",18000,1500,250,500,2,20,5,"English",6.0,
     "UAE is a tax-free financial and technology hub in the Middle East with satellite campuses of top global unis.",
     ["Tax-free salaries","Safe region","Global trade hub","Top international campuses"],
     ["High living costs","Warm climate","High tuition fees"],
     ["Business","Artificial Intelligence","Civil Engineering","Finance","Data Science"]),
    ("Saudi Arabia","SAU",0,1000,0,0,2,20,3,"English",6.5,
     "Saudi Arabia offers 100% full scholarships with generous stipends for international graduate students.",
     ["Full tuition waiver","Monthly stipend provided","State-of-the-art research labs","Free housing"],
     ["Strict cultural norms","Warm desert climate","Limited post-study work for non-citizens"],
     ["Computer Science","Petroleum Engineering","AI & Robotics","Material Science"]),
    ("China","CHN",4000,600,100,100,1,20,15,"Chinese/English",6.0,
     "China offers top-ranked global research universities and CSC Chinese Government Scholarships.",
     ["CSC full scholarships","Low cost of living","Tech manufacturing giant","Top research funding"],
     ["Language barrier","Internet regulations","Strict work visa after study"],
     ["Computer Science","Engineering","AI","International Trade","Medicine"]),
    ("Hong Kong","HKG",18000,1400,100,300,2,20,5,"English",6.5,
     "Hong Kong is Asia's financial center connecting global markets with top English-taught universities.",
     ["Top 50 global universities","English medium","Financial gateway to Asia","High starting salaries"],
     ["High cost of housing","Competitive admissions","Small city space"],
     ["Finance","Computer Science","Data Science","Business","Law"]),
    ("Taiwan","TWN",3500,500,50,100,1,20,5,"Mandarin/English",6.0,
     "Taiwan is the semiconductor capital of the world with affordable high-tech education.",
     ["World semiconductor hub","Very affordable tuition & living","Safe and welcoming","Tech job market"],
     ["Mandarin helpful","Earthquake zone","Humidity"],
     ["Electrical Engineering","Computer Science","Semiconductors","Business"]),
    ("India","IND",3000,300,20,50,0,20,20,"English",6.0,
     "India is a global IT powerhouse with prestigious Premier Institutes like IISc and IITs.",
     ["Global IT & software hub","Very low cost of living","English instruction","Strong technical rigor"],
     ["Intense competition","Air quality in major cities","Infrastructure variation"],
     ["Computer Science","Engineering","Data Analytics","Business Administration"]),
    ("New Zealand","NZL",22000,1200,200,300,3,20,5,"English",6.5,
     "New Zealand offers 3-year post-study work rights and world-class universities in safe natural surroundings.",
     ["3-year post study visa","Beautiful nature","Safe environment","Quality education"],
     ["Distance from Europe/US","Higher living costs","Small population market"],
     ["Computer Science","Data Science","Environmental Science","Agriculture","Business"]),
    ("Brazil","BRA",2000,500,50,100,1,20,2,"Portuguese/English",6.0,
     "Brazil offers free tuition at top public federal universities for competitive international applicants.",
     ["Free tuition at federal universities","Vibrant culture","Largest economy in South America"],
     ["Portuguese required","Safety considerations","Bureaucracy"],
     ["Computer Science","Engineering","Agriculture","Medicine","Data Science"]),
    ("South Africa","ZAF",4000,600,60,150,1,20,3,"English",6.0,
     "South Africa features the highest-ranked universities in Africa with low cost of living and English medium.",
     ["Top-ranked universities in Africa","Affordable fees","English taught","Rich biodiversity"],
     ["Power grid fluctuations","Safety concerns","Economic volatility"],
     ["Mining Engineering","Computer Science","Business","Environmental Science"]),
    ("Egypt","EGY",3000,400,50,100,1,20,2,"Arabic/English",6.0,
     "Egypt is the academic center of the Arab world offering rich history and affordable study.",
     ["Affordable tuition & living","Historic heritage","Middle East gateway"],
     ["Arabic language useful","Economy fluctuations","Warm climate"],
     ["Computer Science","Engineering","Archaeology","Business"]),
    ("Mexico","MEX",4000,500,40,100,1,20,3,"Spanish/English",6.0,
     "Mexico offers premier universities in Latin America with close ties to North American industry.",
     ["Proximity to USA","Low living costs","Rich culture","Top tech hubs in Guadalajara/Monterrey"],
     ["Spanish required for most jobs","Safety variation","Bureaucracy"],
     ["Computer Science","Industrial Engineering","Business","Data Analytics"]),
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
UNIVERSITIES = [
    # USA
    ("USA","Harvard University","Harvard","https://harvard.edu","Cambridge MA",4,3.2,9.0,7.5,325,57000,2200,85,
     '[{"name":"MS CS","duration_years":2,"tuition_usd":57000},{"name":"MBA","duration_years":2,"tuition_usd":73000}]',
     '["September"]',True,"Harvard is the world's most prestigious university.","[\"Nobel laureates\",\"#1 MBA\",\"Largest endowment\"]",98.0),
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
]

UK_UNIVERSITIES = [
    ("GBR","University of Cambridge","Cambridge","https://cam.ac.uk","Cambridge",2,21.0,8.5,7.5,None,36000,1400,0,
     '[{"name":"MPhil CS","duration_years":1,"tuition_usd":36000},{"name":"MBA Judge","duration_years":1,"tuition_usd":65000}]',
     '["October"]',True,"Cambridge is the world's #2 university with 1-year Masters programs.","[\"Top 3 globally\",\"Gates Cambridge Scholarship\",\"1-year Masters\",\"Historic prestige\"]",96.0),
    ("GBR","Imperial College London","Imperial","https://imperial.ac.uk","London",8,14.0,8.0,7.0,None,34000,1800,0,
     '[{"name":"MSc Computing","duration_years":1,"tuition_usd":34000},{"name":"MSc Data Science","duration_years":1,"tuition_usd":34000}]',
     '["October"]',True,"Imperial is a world-class science and technology university in Central London.","[\"Top 10 globally\",\"STEM focus\",\"London location\",\"Strong industry\"]",94.0),
    ("GBR","University College London","UCL","https://ucl.ac.uk","London",9,63.0,7.5,6.5,None,30000,1800,0,
     '[{"name":"MSc CS","duration_years":1,"tuition_usd":30000},{"name":"MSc AI","duration_years":1,"tuition_usd":30000}]',
     '["September"]',True,"UCL is a world top-10 university in Central London.","[\"Top 10 globally\",\"London location\",\"Diverse campus\",\"Strong research\"]",93.0),
]

GLOBAL_UNIVERSITIES = [
    # Switzerland
    ("CHE","ETH Zurich","ETH Zurich","https://ethz.ch","Zurich",7,20.0,8.5,7.0,None,1500,1800,150,
     '[{"name":"MSc Computer Science","duration_years":2,"tuition_usd":1500},{"name":"MSc Robotics","duration_years":2,"tuition_usd":1500}]',
     '["September"]',True,"ETH Zurich is Continental Europe's top university and world leader in engineering and science.","[\"#1 in Continental Europe\",\"Affordable tuition\",\"Einstein alma mater\",\"High salary market\"]",96.0),
    ("CHE","EPFL","EPFL","https://epfl.ch","Lausanne",36,25.0,8.0,7.0,None,1500,1800,150,
     '[{"name":"MSc Computer Science","duration_years":2,"tuition_usd":1500},{"name":"MSc Data Science","duration_years":2,"tuition_usd":1500}]',
     '["September"]',True,"EPFL is a world-class research institute in French-speaking Switzerland.","[\"Top 40 globally\",\"Low tuition fees\",\"Cutting-edge AI labs\",\"High placement\"]",95.0),
    # Italy
    ("ITA","Politecnico di Milano","PoliMi","https://polimi.it","Milan",123,28.0,7.5,6.5,None,3800,900,50,
     '[{"name":"MSc Computer Science Engineering","duration_years":2,"tuition_usd":3800},{"name":"MSc Automation Engineering","duration_years":2,"tuition_usd":3800}]',
     '["September","February"]',True,"Politecnico di Milano is Italy's leading technical university with English taught programs.","[\"Top 20 Engineering Europe\",\"DSU full scholarship\",\"Fashion & Design hub\",\"Low tuition\"]",90.0),
    ("ITA","Sapienza University of Rome","Sapienza","https://uniroma1.it","Rome",134,35.0,7.0,6.0,None,2500,850,50,
     '[{"name":"MSc AI and Robotics","duration_years":2,"tuition_usd":2500},{"name":"MSc Data Science","duration_years":2,"tuition_usd":2500}]',
     '["September"]',True,"Sapienza is one of Europe's largest and oldest universities located in Rome.","[\"Historic city\",\"DSU scholarship eligible\",\"Low tuition fees\",\"Strong research\"]",88.0),
    # Spain
    ("ESP","Universitat de Barcelona","UB","https://ub.edu","Barcelona",164,45.0,7.0,6.5,None,3000,900,50,
     '[{"name":"MSc Data Science","duration_years":1,"tuition_usd":3000},{"name":"MSc Artificial Intelligence","duration_years":2,"tuition_usd":3000}]',
     '["September"]',True,"UB is Catalonia's premier public research university in Barcelona.","[\"Vibrant Barcelona campus\",\"Low tuition fees\",\"Mediterranean tech hub\"]",88.0),
    ("ESP","IE University","IE","https://ie.edu","Madrid",250,30.0,7.5,7.0,310,32000,1200,120,
     '[{"name":"Master in Computer Science","duration_years":1,"tuition_usd":32000},{"name":"IE International MBA","duration_years":1,"tuition_usd":65000}]',
     '["September","January"]',True,"IE University is a top international private university renowned for business and tech innovation.","[\"Top 10 European MBA\",\"Vibrant Madrid hub\",\"Global student body\"]",94.0),
    # UAE
    ("ARE","Khalifa University","KU","https://ku.ac.ae","Abu Dhabi",230,22.0,8.0,6.5,None,18000,1500,0,
     '[{"name":"MSc Computer Science","duration_years":2,"tuition_usd":18000},{"name":"MSc AI and Machine Learning","duration_years":2,"tuition_usd":18000}]',
     '["August","January"]',True,"Khalifa University is the UAE's top-ranked research university offering generous scholarships.","[\"#1 in UAE\",\"Full tuition waivers\",\"State of the art campus\",\"Tax-free job market\"]",92.0),
    # Saudi Arabia
    ("SAU","King Abdullah University of Science and Technology","KAUST","https://kaust.edu.sa","Thuwal",200,15.0,8.5,6.5,None,0,1000,0,
     '[{"name":"MS Computer Science","duration_years":2,"tuition_usd":0},{"name":"MS Electrical Engineering","duration_years":2,"tuition_usd":0}]',
     '["September"]',True,"KAUST provides 100% full scholarships with housing and stipends for all admitted graduate students.","[\"100% Full Scholarship\",\"Free housing + stipend\",\"World-class research facilities\"]",96.0),
    # China
    ("CHN","Tsinghua University","Tsinghua","https://tsinghua.edu.cn","Beijing",14,16.0,8.5,6.5,None,4500,600,100,
     '[{"name":"MS Computer Science","duration_years":2,"tuition_usd":4500},{"name":"Schwarzman Scholars Master","duration_years":1,"tuition_usd":0}]',
     '["September"]',True,"Tsinghua University is China's #1 tech university often called the MIT of China.","[\"#1 in China\",\"Top 15 globally\",\"CSC scholarship\",\"China tech giant partnerships\"]",96.0),
    ("CHN","Peking University","PKU","https://pku.edu.cn","Beijing",17,14.0,8.5,6.5,None,4500,600,100,
     '[{"name":"MS Computer Science","duration_years":2,"tuition_usd":4500},{"name":"Master of Finance","duration_years":2,"tuition_usd":6000}]',
     '["September"]',True,"Peking University is China's premier comprehensive university known for global research.","[\"Top 20 globally\",\"CSC full scholarship\",\"Beijing location\"]",95.0),
    # Hong Kong
    ("HKG","University of Hong Kong","HKU","https://hku.hk","Hong Kong",26,18.0,8.0,6.5,None,22000,1400,50,
     '[{"name":"MSc Computer Science","duration_years":1,"tuition_usd":22000},{"name":"MSc Financial Technology","duration_years":1,"tuition_usd":24000}]',
     '["September"]',True,"HKU is Hong Kong's oldest and highest ranked English-medium university.","[\"Top 30 globally\",\"English taught\",\"Global finance gateway\"]",94.0),
    # Taiwan
    ("TWN","National Taiwan University","NTU","https://ntu.edu.tw","Taipei",69,20.0,7.5,6.5,None,3500,500,50,
     '[{"name":"MS Computer Science","duration_years":2,"tuition_usd":3500},{"name":"MS Electronics Engineering","duration_years":2,"tuition_usd":3500}]',
     '["September","February"]',True,"NTU is Taiwan's top university located in Taipei, at the heart of global semiconductor manufacturing.","[\"Semiconductor center\",\"Very low tuition\",\"TSMC research partner\"]",93.0),
    # India
    ("IND","Indian Institute of Science","IISc Bangalore","https://iisc.ac.in","Bangalore",155,10.0,8.5,6.5,None,1500,300,20,
     '[{"name":"MTech Computer Science","duration_years":2,"tuition_usd":1500},{"name":"MTech Artificial Intelligence","duration_years":2,"tuition_usd":1500}]',
     '["August"]',True,"IISc is India's premier institute for advanced scientific and technological research in Silicon Valley of India.","[\"#1 University in India\",\"Bangalore tech hub\",\"Under $2,000 tuition\"]",95.0),
    ("IND","Indian Institute of Technology Bombay","IIT Bombay","https://iitb.ac.in","Mumbai",149,5.0,8.5,6.5,None,2000,300,20,
     '[{"name":"MTech Computer Science","duration_years":2,"tuition_usd":2000},{"name":"MTech Data Science","duration_years":2,"tuition_usd":2000}]',
     '["August"]',True,"IIT Bombay is India's most competitive technology institute with world-famous engineering alumni.","[\"Premier IIT\",\"Mumbai economic capital\",\"Unmatched tech placement\"]",96.0),
    # Brazil
    ("BRA","Universidade de São Paulo","USP","https://usp.br","São Paulo",85,15.0,7.5,6.0,None,0,500,0,
     '[{"name":"MSc Computer Science","duration_years":2,"tuition_usd":0},{"name":"MSc Data Science","duration_years":2,"tuition_usd":0}]',
     '["March","August"]',True,"USP is Latin America's #1 ranked public federal research university with free tuition.","[\"#1 in Latin America\",\"Free tuition\",\"Latin America financial capital\"]",91.0),
    # South Africa
    ("ZAF","University of Cape Town","UCT","https://uct.ac.za","Cape Town",173,35.0,7.0,6.5,None,4500,600,50,
     '[{"name":"MSc Computer Science","duration_years":2,"tuition_usd":4500},{"name":"MSc Data Science","duration_years":2,"tuition_usd":4500}]',
     '["February"]',True,"UCT is Africa's highest ranked university situated under Table Mountain in Cape Town.","[\"#1 in Africa\",\"Scenic location\",\"English taught\",\"Affordable fees\"]",89.0),
    # Egypt
    ("EGY","American University in Cairo","AUC","https://aucegypt.edu","Cairo",410,40.0,7.0,6.5,None,12000,500,50,
     '[{"name":"MSc Computer Science","duration_years":2,"tuition_usd":12000},{"name":"MBA","duration_years":2,"tuition_usd":18000}]',
     '["September","February"]',True,"AUC is Egypt's leading US-accredited English language private research university.","[\"US accreditation\",\"Middle East hub\",\"English taught\"]",88.0),
    # Mexico
    ("MEX","Tecnológico de Monterrey","ITESM","https://tec.mx","Monterrey",170,35.0,7.5,6.5,None,12000,500,50,
     '[{"name":"Master in Computer Science","duration_years":2,"tuition_usd":12000},{"name":"MBA Tec","duration_years":2,"tuition_usd":20000}]',
     '["August","January"]',True,"Tec de Monterrey is Mexico's top private university with strong US industry partnerships.","[\"Top private uni Mexico\",\"US industry connections\",\"Entrepreneurship focus\"]",90.0),
]

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
    (GLOBAL_UNIVERSITIES, None),
]

total = 0
for group, default_gre in all_groups:
    n = insert_unis(group, default_gre)
    total += n

print(f"\n[OK] Done! {total} new universities inserted.")

cur.execute("SELECT COUNT(*) FROM universities")
print(f"   Total universities in DB: {cur.fetchone()[0]}")
cur.execute("SELECT COUNT(*) FROM countries")
print(f"   Total countries in DB: {cur.fetchone()[0]}")

cur.close()
conn.close()
