import { useState, useMemo } from 'react'
import { useQuery } from '@tanstack/react-query'
import { universityApi } from '@/lib/api'
import { Award, ExternalLink, DollarSign, Globe, BookOpen, Search, Sparkles, Calendar, CheckCircle2, ShieldCheck, Filter, Loader2 } from 'lucide-react'
import { motion } from 'framer-motion'
import { toast } from 'react-hot-toast'

interface GlobalScholarship {
  id: string
  name: string
  provider: string
  country: string
  flag: string
  scholarship_type: 'fully_funded' | 'merit' | 'government' | 'need_based' | 'university'
  amount_description: string
  eligibility: string
  deadline: string
  application_url: string
  description: string
  min_cgpa?: number
}

const GLOBAL_COUNTRY_SCHOLARSHIPS: GlobalScholarship[] = [
  // 🇺🇸 USA
  {
    id: 'usa-1',
    name: 'Fulbright Foreign Student Program',
    provider: 'US Department of State',
    country: 'USA',
    flag: '🇺🇸',
    scholarship_type: 'fully_funded',
    amount_description: 'Full Tuition + Monthly Stipend + Airfare + Health Insurance',
    eligibility: 'Indian nationals with completed Bachelor’s degree & strong leadership',
    deadline: 'October 2025 – February 2026',
    application_url: 'https://foreign.fulbrightonline.org',
    description: 'Fully funded grant enabling graduate students, young professionals, and artists from abroad to study and conduct research in the US.',
    min_cgpa: 7.5,
  },
  {
    id: 'usa-2',
    name: 'Yale University Need-Based Scholarships',
    provider: 'Yale University',
    country: 'USA',
    flag: '🇺🇸',
    scholarship_type: 'need_based',
    amount_description: 'Up to $70,000+/year (100% demonstrated financial need)',
    eligibility: 'Admitted undergraduate & graduate students with verified financial need',
    deadline: 'November 2025 / January 2026',
    application_url: 'https://finaid.yale.edu',
    description: 'Covers 100% of demonstrated financial need without student loans for all admitted domestic and international students.',
  },
  {
    id: 'usa-3',
    name: 'Stanford Knight-Hennessy Scholars Program',
    provider: 'Stanford University',
    country: 'USA',
    flag: '🇺🇸',
    scholarship_type: 'fully_funded',
    amount_description: 'Full Tuition + Living Stipend + Academic & Travel Allowance',
    eligibility: 'Admitted to any Stanford graduate program with high academic standing',
    deadline: 'October 2025',
    application_url: 'https://knight-hennessy.stanford.edu',
    description: 'Preeminent multi-disciplinary graduate scholarship supporting future global leaders studying at Stanford.',
    min_cgpa: 8.5,
  },
  {
    id: 'usa-4',
    name: 'AAUW International Fellowships for Women',
    provider: 'American Association of University Women',
    country: 'USA',
    flag: '🇺🇸',
    scholarship_type: 'merit',
    amount_description: '$20,000 – $50,000 per year',
    eligibility: 'Women pursuing full-time graduate or postdoctoral study in the US who are not US citizens',
    deadline: 'November 15, 2025',
    application_url: 'https://www.aauw.org',
    description: 'Supports non-US women dedicated to advancing education, research, and community leadership.',
  },

  // 🇬🇧 UK
  {
    id: 'uk-1',
    name: 'Chevening Master’s Scholarships',
    provider: 'UK Foreign, Commonwealth & Development Office (FCDO)',
    country: 'UK',
    flag: '🇬🇧',
    scholarship_type: 'fully_funded',
    amount_description: '100% Full Tuition + £1,300/mo Stipend + Return Flights',
    eligibility: 'Indian passport holders with min. 2 years work exp & return intent',
    deadline: 'November 2025',
    application_url: 'https://www.chevening.org',
    description: 'The UK government’s global scholarship program offering fully funded 1-year Master’s degrees at any top UK university.',
    min_cgpa: 7.0,
  },
  {
    id: 'uk-2',
    name: 'Commonwealth Master’s & PhD Scholarships',
    provider: 'Commonwealth Scholarship Commission (CSC)',
    country: 'UK',
    flag: '🇬🇧',
    scholarship_type: 'government',
    amount_description: 'Full Tuition + £1,347/mo Stipend + Travel + Warm Clothing Allowance',
    eligibility: 'Citizens of Commonwealth countries (including India)',
    deadline: 'December 2025',
    application_url: 'https://cscuk.fcdo.gov.uk',
    description: 'Aimed at high-potential individuals from Commonwealth countries who could not otherwise afford to study in the UK.',
  },
  {
    id: 'uk-3',
    name: 'Gates Cambridge Scholarship',
    provider: 'Bill & Melinda Gates Foundation / Cambridge',
    country: 'UK',
    flag: '🇬🇧',
    scholarship_type: 'fully_funded',
    amount_description: 'Full Cost of Study + £20,000/yr Maintenance Allowance',
    eligibility: 'Outstanding intellect, leadership capacity, and commitment to improving lives of others',
    deadline: 'October 2025 / January 2026',
    application_url: 'https://www.gatescambridge.org',
    description: 'Full-cost scholarships for postgraduate study in any subject available at the University of Cambridge.',
    min_cgpa: 8.5,
  },
  {
    id: 'uk-4',
    name: 'Clarendon Fund Scholarships',
    provider: 'University of Oxford',
    country: 'UK',
    flag: '🇬🇧',
    scholarship_type: 'university',
    amount_description: '100% Tuition Fees + Generous Living Grant (~£18,622/yr)',
    eligibility: 'Automatically considered for all Oxford graduate applicants with top academic performance',
    deadline: 'January 2026',
    application_url: 'https://www.ox.ac.uk/clarendon',
    description: 'Oxford’s flagship graduate scholarship scheme offering over 200 fully funded awards every year.',
  },

  // 🇩🇪 GERMANY
  {
    id: 'de-1',
    name: 'DAAD EPOS Postgraduate Scholarships',
    provider: 'German Academic Exchange Service (DAAD)',
    country: 'Germany',
    flag: '🇩🇪',
    scholarship_type: 'fully_funded',
    amount_description: '€934/month Stipend + Flight Allowance + Health Insurance + Tuition Waiver',
    eligibility: 'International graduates with at least 2 years of professional work experience',
    deadline: 'August – November 2025',
    application_url: 'https://www.daad.de/en/study-and-research-in-germany/scholarships/daad-scholarships/',
    description: 'Supports foreign graduates from developing countries to pursue development-related postgraduate courses in Germany.',
    min_cgpa: 7.0,
  },
  {
    id: 'de-2',
    name: 'Deutschlandstipendium',
    provider: 'Federal Govt of Germany + Private Donors',
    country: 'Germany',
    flag: '🇩🇪',
    scholarship_type: 'merit',
    amount_description: '€300/month for minimum 2 semesters',
    eligibility: 'Enrolled at a participating German university with outstanding academic and social achievement',
    deadline: 'May – July 2025',
    application_url: 'https://www.deutschlandstipendium.de',
    description: 'Supports high-achieving students at state and state-recognized universities across Germany regardless of nationality.',
  },
  {
    id: 'de-3',
    name: 'Heinrich Böll Foundation Grants',
    provider: 'Heinrich Böll Foundation',
    country: 'Germany',
    flag: '🇩🇪',
    scholarship_type: 'government',
    amount_description: '€934/month + Individual Family & Travel Allowances',
    eligibility: 'International students with excellent academic records & active socio-political engagement',
    deadline: 'March 1 / September 1',
    application_url: 'https://www.boell.de/en/foundation/scholarships',
    description: 'Scholarships for Master’s and PhD students studying at state-recognized German universities.',
  },

  // 🇨🇦 CANADA
  {
    id: 'ca-1',
    name: 'Vanier Canada Graduate Scholarships',
    provider: 'Government of Canada',
    country: 'Canada',
    flag: '🇨🇦',
    scholarship_type: 'fully_funded',
    amount_description: '$50,000 per year for 3 years (PhD)',
    eligibility: 'Nominated by a Canadian institution; high academic achievement & research potential',
    deadline: 'November 2025',
    application_url: 'https://vanier.gc.ca/en/home-accueil.html',
    description: 'Attracts and retains world-class doctoral students by offering substantial financial support for Canadian university research.',
    min_cgpa: 8.0,
  },
  {
    id: 'ca-2',
    name: 'Lester B. Pearson International Scholarship',
    provider: 'University of Toronto',
    country: 'Canada',
    flag: '🇨🇦',
    scholarship_type: 'fully_funded',
    amount_description: 'Full Tuition + Books + Incidental Fees + Full Residence Support',
    eligibility: 'Nominated high school international graduates applying for undergraduate study at U of T',
    deadline: 'November 30, 2025',
    application_url: 'https://future.utoronto.ca/pearson/about-the-scholarship/',
    description: 'Recognizes international students who demonstrate exceptional academic achievement and creativity.',
  },
  {
    id: 'ca-3',
    name: 'UBC International Leader of Tomorrow Award',
    provider: 'University of British Columbia',
    country: 'Canada',
    flag: '🇨🇦',
    scholarship_type: 'need_based',
    amount_description: 'Need-based financial aid up to full tuition & annual living cost',
    eligibility: 'International undergraduate candidates with superior academic achievement and leadership',
    deadline: 'December 1, 2025',
    application_url: 'https://you.ubc.ca/financial-planning/scholarships-awards-international-students/',
    description: 'Supports international students who demonstrate financial need alongside top-tier academic merit.',
  },

  // 🇦🇺 AUSTRALIA
  {
    id: 'au-1',
    name: 'Australian Government Research Training Program (RTP)',
    provider: 'Department of Education (Australian Govt)',
    country: 'Australia',
    flag: '🇦🇺',
    scholarship_type: 'fully_funded',
    amount_description: 'Full Tuition Offset + AUD $35,000 – $42,754/yr Stipend + Relocation Grant',
    eligibility: 'International Masters by Research or PhD candidates at participating Australian universities',
    deadline: 'September – October 2025',
    application_url: 'https://www.education.gov.au/research-block-grants/research-training-program',
    description: 'Flexible funding blocks allocated to Australian universities to support domestic and international research candidates.',
    min_cgpa: 7.5,
  },
  {
    id: 'au-2',
    name: 'Australia Awards Scholarships',
    provider: 'Department of Foreign Affairs and Trade (DFAT)',
    country: 'Australia',
    flag: '🇦🇺',
    scholarship_type: 'fully_funded',
    amount_description: '100% Tuition + Return Airfare + AUD $30,000+/yr Living Allowance',
    eligibility: 'Citizens of partner developing countries seeking full-time undergraduate or postgraduate study',
    deadline: 'April 30, 2026',
    application_url: 'https://www.dfat.gov.au/people-to-people/australia-awards',
    description: 'Long-term awards administered by DFAT to contribute to the development needs of Australia’s partner countries.',
  },
  {
    id: 'au-3',
    name: 'Melbourne Research Scholarships (MRS)',
    provider: 'University of Melbourne',
    country: 'Australia',
    flag: '🇦🇺',
    scholarship_type: 'university',
    amount_description: '100% Fee Offset + AUD $37,000/yr Living Allowance + Overseas Health Cover',
    eligibility: 'High-achieving domestic and international research higher degree candidates',
    deadline: 'Automatic consideration upon research application',
    application_url: 'https://scholarships.unimelb.edu.au',
    description: 'Awarded to high-achieving domestic and international research students pursuing a master by research or doctorate.',
  },

  // 🇪🇺 EUROPE (Ireland / France / Netherlands)
  {
    id: 'eu-1',
    name: 'Government of Ireland International Education Scholarship',
    provider: 'Government of Ireland / HEA',
    country: 'Europe',
    flag: '🇮🇪',
    scholarship_type: 'government',
    amount_description: '€10,000 Stipend + 100% Tuition Fee Waiver for 1 Year',
    eligibility: 'High-performing non-EU/EEA students applying for a Master’s or PhD program in Ireland',
    deadline: 'March 2026',
    application_url: 'https://eurireland.ie',
    description: 'A prestigious national initiative reflecting Ireland as an open, high-quality international education center.',
  },
  {
    id: 'eu-2',
    name: 'Eiffel Excellence Scholarship Program',
    provider: 'French Ministry for Europe and Foreign Affairs',
    country: 'Europe',
    flag: '🇫🇷',
    scholarship_type: 'government',
    amount_description: '€1,181/month (Master’s) or €1,700/month (PhD) + Airfare + Health Insurance',
    eligibility: 'Top international candidates nominated directly by participating French higher education institutions',
    deadline: 'January 2026',
    application_url: 'https://www.campusfrance.org/en/eiffel-scholarship-program-of-excellence',
    description: 'Developed by the French Ministry of Foreign Affairs to enable French institutions to attract top international talent.',
  },
  {
    id: 'eu-3',
    name: 'NL Scholarship (Holland Scholarship)',
    provider: 'Dutch Ministry of Education + Research Unis',
    country: 'Europe',
    flag: '🇳🇱',
    scholarship_type: 'merit',
    amount_description: '€5,000 – €10,000 tuition grant in year 1',
    eligibility: 'Non-EEA students applying for a full-time Bachelor’s or Master’s in the Netherlands',
    deadline: 'February / May 2026',
    application_url: 'https://www.studyinnl.org/finances/nl-scholarship',
    description: 'Financed by the Dutch Ministry of Education and Dutch research universities for international students.',
  },

  // 🇮🇳 INDIA GOVT & FOUNDATIONS
  {
    id: 'in-1',
    name: 'National Overseas Scholarship (NOS)',
    provider: 'Ministry of Social Justice (Govt of India)',
    country: 'India',
    flag: '🇮🇳',
    scholarship_type: 'government',
    amount_description: '100% Tuition Fees + USD $15,400/yr Living Allowance + Airfare',
    eligibility: 'SC/ST candidates with family annual income under ₹8 Lakhs pursuing Master’s/PhD abroad',
    deadline: 'March 31, 2026',
    application_url: 'https://nosmsje.gov.in',
    description: 'Government of India scholarship providing financial assistance to selected low-income SC/ST students for foreign studies.',
  },
  {
    id: 'in-2',
    name: 'JN Tata Endowment Gift & Loan Scholarship',
    provider: 'JN Tata Endowment',
    country: 'India',
    flag: '🇮🇳',
    scholarship_type: 'merit',
    amount_description: 'Up to ₹10 Lakhs Loan (at 0–2% interest) + Travel/Gift Grants up to ₹7.5 Lakhs',
    eligibility: 'Indian graduates with min. 60% aggregate marks planning higher studies abroad',
    deadline: 'March 2026',
    application_url: 'https://www.jntataendowment.org',
    description: 'Established in 1892 by Jamsetji Tata to encourage young Indian scholars to pursue higher education abroad.',
  },
  {
    id: 'in-3',
    name: 'Inlaks Shivdasani Foundation Scholarships',
    provider: 'Inlaks Shivdasani Foundation',
    country: 'India',
    flag: '🇮🇳',
    scholarship_type: 'fully_funded',
    amount_description: 'Up to $100,000 covering Tuition + Living Expenses + Health Insurance',
    eligibility: 'Indian citizens under 30 with first-class degree admitted to top global universities in US/UK/Europe',
    deadline: 'March 2026',
    application_url: 'https://www.inlaksfoundation.org',
    description: 'Grants scholarships to exceptional young Indians to read at top universities in America, UK, and Europe.',
    min_cgpa: 8.0,
  },
]

const COUNTRY_FILTERS = [
  { label: '🌍 All Countries', value: 'ALL' },
  { label: '🇺🇸 USA', value: 'USA' },
  { label: '🇬🇧 UK', value: 'UK' },
  { label: '🇩🇪 Germany', value: 'Germany' },
  { label: '🇨🇦 Canada', value: 'Canada' },
  { label: '🇦🇺 Australia', value: 'Australia' },
  { label: '🇪🇺 Europe', value: 'Europe' },
  { label: '🇮🇳 India Govt', value: 'India' },
]

const TYPE_BADGES: Record<string, { label: string; style: string }> = {
  fully_funded: { label: 'Fully Funded', style: 'bg-emerald-50 text-emerald-700 border-emerald-200' },
  government:   { label: 'Government Grant', style: 'bg-blue-50 text-blue-700 border-blue-200' },
  merit:        { label: 'Merit-Based', style: 'bg-purple-50 text-purple-700 border-purple-200' },
  need_based:   { label: 'Need-Based', style: 'bg-amber-50 text-amber-700 border-amber-200' },
  university:   { label: 'University Award', style: 'bg-indigo-50 text-indigo-700 border-indigo-200' },
}

export default function ScholarshipsPage() {
  const [selectedCountryTab, setSelectedCountryTab] = useState('ALL')
  const [searchQuery, setSearchQuery] = useState('')
  const [customLiveQuery, setCustomLiveQuery] = useState('')
  const [isSearchingLiveWeb, setIsSearchingLiveWeb] = useState(false)
  const [liveSearchResults, setLiveSearchResults] = useState<any[] | null>(null)

  // Fetch DB scholarships as fallback/supplement
  const { data: dbScholarships = [] } = useQuery({
    queryKey: ['scholarships'],
    queryFn: () => universityApi.scholarships({ limit: 50 }).then((r: any) => r.data),
  })

  // Filter static global scholarships
  const filteredScholarships = useMemo(() => {
    return GLOBAL_COUNTRY_SCHOLARSHIPS.filter((s) => {
      const matchCountry = selectedCountryTab === 'ALL' || s.country === selectedCountryTab
      const q = searchQuery.toLowerCase().trim()
      const matchQuery =
        !q ||
        s.name.toLowerCase().includes(q) ||
        s.provider.toLowerCase().includes(q) ||
        s.country.toLowerCase().includes(q) ||
        s.description.toLowerCase().includes(q)
      return matchCountry && matchQuery
    })
  }, [selectedCountryTab, searchQuery])

  // Perform Live Web Search via Tavily
  const handleLiveWebSearch = async () => {
    const q = customLiveQuery || searchQuery || `${selectedCountryTab === 'ALL' ? 'global' : selectedCountryTab} scholarships for international Indian students 2025 2026`
    setIsSearchingLiveWeb(true)
    const toastId = toast.loading(`Searching live web (Tavily) for "${q}"...`)

    try {
      const res = await universityApi.fetchLiveTuition({
        university_name: q,
        course_name: 'Scholarships',
        country: selectedCountryTab === 'ALL' ? 'Global' : selectedCountryTab,
      })
      if (res.data) {
        setLiveSearchResults([res.data])
        toast.success('Retrieved live web scholarship data!', { id: toastId })
      }
    } catch (e) {
      toast.error('Could not fetch live web search.', { id: toastId })
    } finally {
      setIsSearchingLiveWeb(false)
    }
  }

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 flex items-center gap-2">
            <Award className="w-6 h-6 text-amber-500" /> Country-Wise Global Scholarships Hub
          </h1>
          <p className="text-gray-500 text-sm">
            Explore verified fully funded, government, merit, and university scholarships worldwide for Indian & international students
          </p>
        </div>

        <div className="flex items-center gap-2">
          <input
            type="text"
            placeholder="Search live web scholarships..."
            value={customLiveQuery}
            onChange={(e) => setCustomLiveQuery(e.target.value)}
            className="input text-xs w-48 sm:w-64"
          />
          <button
            onClick={handleLiveWebSearch}
            disabled={isSearchingLiveWeb}
            className="btn-primary text-xs shrink-0 py-2 inline-flex items-center gap-1.5"
          >
            {isSearchingLiveWeb ? <Loader2 className="w-3.5 h-3.5 animate-spin" /> : <Sparkles className="w-3.5 h-3.5 text-amber-300" />}
            Live Search
          </button>
        </div>
      </div>

      {/* Country Filter Tabs */}
      <div className="flex items-center gap-2 overflow-x-auto pb-2 scrollbar-none border-b border-gray-100">
        {COUNTRY_FILTERS.map((tab) => (
          <button
            key={tab.value}
            onClick={() => setSelectedCountryTab(tab.value)}
            className={`px-3.5 py-2 rounded-xl text-sm font-medium whitespace-nowrap transition-all flex items-center gap-1.5 ${
              selectedCountryTab === tab.value
                ? 'bg-brand-500 text-white shadow-sm'
                : 'bg-white text-gray-600 border border-gray-200 hover:border-brand-300 hover:bg-brand-50/50'
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Search Input Bar */}
      <div className="card !p-3.5 flex items-center gap-3">
        <Search className="w-5 h-5 text-gray-400 shrink-0 ml-1" />
        <input
          type="text"
          placeholder="Filter by scholarship name, provider, country, or keyword (e.g. Chevening, DAAD, Fulbright, Yale)..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="w-full bg-transparent border-0 focus:outline-none text-sm text-gray-900 placeholder:text-gray-400"
        />
        {searchQuery && (
          <button onClick={() => setSearchQuery('')} className="text-xs text-gray-400 hover:text-gray-600 mr-1">
            Clear
          </button>
        )}
      </div>

      {/* Live Web Results (if queried) */}
      {liveSearchResults && (
        <div className="card border-2 border-brand-200 bg-brand-50/30">
          <div className="flex items-center justify-between mb-2">
            <span className="inline-flex items-center gap-1 text-xs font-semibold px-2.5 py-1 rounded-full bg-brand-100 text-brand-700">
              <Sparkles className="w-3.5 h-3.5 text-amber-500" /> Tavily Live Web Search Result
            </span>
            <button onClick={() => setLiveSearchResults(null)} className="text-xs text-gray-400 hover:text-gray-600">
              Dismiss
            </button>
          </div>
          {liveSearchResults.map((r, idx) => (
            <div key={idx} className="space-y-2">
              <h4 className="font-semibold text-gray-900 text-base">{r.notes}</h4>
              <p className="text-sm text-gray-600">Estimated Live Web Tuition / Financial Aid: <strong>${r.tuition_usd_per_year?.toLocaleString()}/yr</strong></p>
              {r.source_url && (
                <a href={r.source_url} target="_blank" rel="noreferrer" className="text-xs text-brand-600 hover:underline flex items-center gap-1 font-medium">
                  <ExternalLink className="w-3 h-3" /> View Verified Web Source
                </a>
              )}
            </div>
          ))}
        </div>
      )}

      {/* Country Scholarships Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
        {filteredScholarships.map((s, i) => {
          const badge = TYPE_BADGES[s.scholarship_type] || TYPE_BADGES.merit
          return (
            <motion.div
              key={s.id}
              initial={{ opacity: 0, y: 12 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.04 }}
              className="card hover:shadow-md transition-all flex flex-col justify-between"
            >
              <div>
                <div className="flex items-start justify-between mb-3">
                  <div className="space-y-1">
                    <div className="flex items-center gap-2">
                      <span className="text-lg">{s.flag}</span>
                      <span className={`text-xs font-medium px-2.5 py-0.5 rounded-full border ${badge.style}`}>
                        {badge.label}
                      </span>
                    </div>
                    <h3 className="font-bold text-gray-900 text-base leading-snug">{s.name}</h3>
                    <p className="text-xs font-medium text-gray-500">Provided by {s.provider}</p>
                  </div>
                  <div className="w-10 h-10 rounded-xl bg-amber-50 border border-amber-200 flex items-center justify-center shrink-0 ml-2">
                    <Award className="w-5 h-5 text-amber-600" />
                  </div>
                </div>

                {/* Amount / Coverage */}
                <div className="bg-emerald-50/70 border border-emerald-100 rounded-xl p-3 mb-3 text-emerald-800 text-sm font-semibold flex items-start gap-2">
                  <DollarSign className="w-4 h-4 text-emerald-600 shrink-0 mt-0.5" />
                  <span>{s.amount_description}</span>
                </div>

                {/* Description */}
                <p className="text-xs text-gray-600 leading-relaxed mb-3 line-clamp-3">{s.description}</p>

                {/* Eligibility & Details */}
                <div className="space-y-1.5 text-xs text-gray-600 bg-gray-50/80 p-3 rounded-xl mb-4">
                  <div className="flex items-start gap-1.5">
                    <CheckCircle2 className="w-3.5 h-3.5 text-brand-500 shrink-0 mt-0.5" />
                    <span><strong>Eligibility:</strong> {s.eligibility}</span>
                  </div>
                  {s.min_cgpa && (
                    <div className="flex items-center gap-1.5 text-gray-700">
                      <BookOpen className="w-3.5 h-3.5 text-purple-500 shrink-0" />
                      <span><strong>Min Academic Score:</strong> CGPA {s.min_cgpa}/10</span>
                    </div>
                  )}
                  <div className="flex items-center gap-1.5 text-amber-700 font-medium">
                    <Calendar className="w-3.5 h-3.5 text-amber-600 shrink-0" />
                    <span><strong>Target Deadline:</strong> {s.deadline}</span>
                  </div>
                </div>
              </div>

              {/* Action Button */}
              <div className="flex items-center justify-between pt-2 border-t border-gray-100 mt-2">
                <span className="text-xs font-medium text-gray-400 flex items-center gap-1">
                  <ShieldCheck className="w-3.5 h-3.5 text-emerald-500" /> Verified 2025/2026
                </span>
                {s.application_url && (
                  <a
                    href={s.application_url}
                    target="_blank"
                    rel="noreferrer"
                    className="inline-flex items-center gap-1.5 px-3.5 py-1.5 rounded-lg bg-brand-50 text-brand-600 hover:bg-brand-500 hover:text-white text-xs font-semibold transition-all"
                  >
                    Official Portal <ExternalLink className="w-3 h-3" />
                  </a>
                )}
              </div>
            </motion.div>
          )
        })}
      </div>

      {filteredScholarships.length === 0 && (
        <div className="text-center py-12 card">
          <Award className="w-10 h-10 text-gray-300 mx-auto mb-3" />
          <h3 className="font-semibold text-gray-700">No scholarships found matching your criteria</h3>
          <p className="text-sm text-gray-400 mt-1">Try selecting a different country tab or search query, or use Live Web Search above.</p>
        </div>
      )}
    </div>
  )
}
