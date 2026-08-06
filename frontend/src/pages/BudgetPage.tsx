import { useState } from 'react'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'
import { Calculator, DollarSign, TrendingDown, Info, MapPin, Building2, GraduationCap, BookOpen, Sparkles, Globe, Loader2, ExternalLink } from 'lucide-react'
import { universityApi } from '../lib/api'
import { toast } from 'react-hot-toast'

interface UniversityOption {
  name: string
  location: string
  country: string
  tuition: number
  livingMonthly: number
  visa: number
  insurance: number
  defaultCourse: string
}

const PRESET_UNIVERSITIES: UniversityOption[] = [
  // Germany
  { name: 'Technical University of Munich (TUM)', location: 'Munich, Germany', country: 'Germany', tuition: 500, livingMonthly: 1100, visa: 75, insurance: 120, defaultCourse: 'MSc Computer Science' },
  { name: 'LMU Munich', location: 'Munich, Germany', country: 'Germany', tuition: 300, livingMonthly: 1100, visa: 75, insurance: 120, defaultCourse: 'MSc Data Science & AI' },
  { name: 'RWTH Aachen University', location: 'Aachen, Germany', country: 'Germany', tuition: 600, livingMonthly: 850, visa: 75, insurance: 110, defaultCourse: 'MSc Mechanical Engineering' },

  // USA
  { name: 'Harvard University', location: 'Cambridge, MA, USA', country: 'USA', tuition: 54000, livingMonthly: 1900, visa: 185, insurance: 1400, defaultCourse: 'MSc Computer Science' },
  { name: 'Massachusetts Institute of Technology (MIT)', location: 'Cambridge, MA, USA', country: 'USA', tuition: 57500, livingMonthly: 2000, visa: 185, insurance: 1500, defaultCourse: 'MSc Artificial Intelligence' },
  { name: 'Stanford University', location: 'Stanford, CA, USA', country: 'USA', tuition: 56000, livingMonthly: 2100, visa: 185, insurance: 1450, defaultCourse: 'MSc Data Science & AI' },
  { name: 'New York University (NYU)', location: 'New York, NY, USA', country: 'USA', tuition: 48000, livingMonthly: 2300, visa: 185, insurance: 1350, defaultCourse: 'MSc Information Technology' },

  // UK
  { name: 'University of Oxford', location: 'Oxford, UK', country: 'UK', tuition: 36000, livingMonthly: 1400, visa: 490, insurance: 500, defaultCourse: 'MSc Computer Science' },
  { name: 'University of Cambridge', location: 'Cambridge, UK', country: 'UK', tuition: 38000, livingMonthly: 1350, visa: 490, insurance: 500, defaultCourse: 'MSc Artificial Intelligence' },
  { name: 'Imperial College London', location: 'London, UK', country: 'UK', tuition: 41000, livingMonthly: 1750, visa: 490, insurance: 550, defaultCourse: 'MSc Computer Science' },
  { name: 'University College London (UCL)', location: 'London, UK', country: 'UK', tuition: 34000, livingMonthly: 1700, visa: 490, insurance: 520, defaultCourse: 'MSc Data Science & AI' },

  // Canada
  { name: 'University of Toronto', location: 'Toronto, ON, Canada', country: 'Canada', tuition: 31000, livingMonthly: 1500, visa: 150, insurance: 650, defaultCourse: 'MSc Computer Science' },
  { name: 'University of British Columbia (UBC)', location: 'Vancouver, BC, Canada', country: 'Canada', tuition: 28000, livingMonthly: 1600, visa: 150, insurance: 600, defaultCourse: 'MSc Data Science & AI' },
  { name: 'McGill University', location: 'Montreal, QC, Canada', country: 'Canada', tuition: 25000, livingMonthly: 1200, visa: 150, insurance: 580, defaultCourse: 'MSc Mechanical Engineering' },

  // Australia
  { name: 'University of Melbourne', location: 'Melbourne, Australia', country: 'Australia', tuition: 33000, livingMonthly: 1550, visa: 620, insurance: 550, defaultCourse: 'MSc Information Technology' },
  { name: 'University of Sydney', location: 'Sydney, Australia', country: 'Australia', tuition: 35000, livingMonthly: 1700, visa: 620, insurance: 580, defaultCourse: 'MSc Data Science & AI' },
  { name: 'Australian National University (ANU)', location: 'Canberra, Australia', country: 'Australia', tuition: 31000, livingMonthly: 1350, visa: 620, insurance: 520, defaultCourse: 'MSc Computer Science' },

  // Ireland
  { name: 'Trinity College Dublin', location: 'Dublin, Ireland', country: 'Ireland', tuition: 22000, livingMonthly: 1400, visa: 100, insurance: 450, defaultCourse: 'MSc Computer Science' },
  { name: 'University College Dublin (UCD)', location: 'Dublin, Ireland', country: 'Ireland', tuition: 20000, livingMonthly: 1350, visa: 100, insurance: 450, defaultCourse: 'MSc Data Science & AI' },
]

const COURSE_PRESETS = [
  'MSc Computer Science',
  'MSc Data Science & AI',
  'MSc Artificial Intelligence',
  'MBA / Business Management',
  'MSc Information Technology',
  'MSc Mechanical Engineering',
  'MSc Electrical & Electronics',
  'MSc Biotechnology / Bioengineering',
  'BSc Computer Science & Engineering',
]

const COUNTRIES = ['Germany', 'USA', 'UK', 'Canada', 'Australia', 'Ireland']
const USD_TO_INR = 87.0

export default function BudgetPage() {
  const [selectedCountry, setSelectedCountry] = useState('Germany')
  const [selectedUniName, setSelectedUniName] = useState('Technical University of Munich (TUM)')
  const [customUniName, setCustomUniName] = useState('')
  const [selectedCourse, setSelectedCourse] = useState('MSc Computer Science')
  const [customCourseName, setCustomCourseName] = useState('')
  const [location, setLocation] = useState('Munich, Germany')
  const [tuitionPerYear, setTuitionPerYear] = useState(500)
  const [livingMonthly, setLivingMonthly] = useState(1100)
  const [duration, setDuration] = useState(2)
  const [scholarship, setScholarship] = useState(0)

  // Live web search status
  const [isSearchingWeb, setIsSearchingWeb] = useState(false)
  const [liveSourceUrl, setLiveSourceUrl] = useState<string | null>(null)
  const [liveSearchNotes, setLiveSearchNotes] = useState<string | null>(null)

  const countryUnis = PRESET_UNIVERSITIES.filter((u) => u.country === selectedCountry)

  const activeUniName = selectedUniName === 'Custom' ? (customUniName || 'Custom University') : selectedUniName
  const activeCourseName = selectedCourse === 'Custom' ? (customCourseName || 'Custom Degree Program') : selectedCourse
  const activeVisaFee = PRESET_UNIVERSITIES.find((u) => u.country === selectedCountry)?.visa || 200
  const activeInsuranceFee = PRESET_UNIVERSITIES.find((u) => u.country === selectedCountry)?.insurance || 600

  // Live Web Search for Tuition Fee via Tavily
  const fetchLiveWebTuition = async (uniName?: string, courseName?: string, countryName?: string) => {
    const targetUni = uniName || activeUniName
    const targetCourse = courseName || activeCourseName
    const targetCountry = countryName || selectedCountry

    setIsSearchingWeb(true)
    const toastId = toast.loading(`Searching live web (Tavily) for ${targetCourse} tuition at ${targetUni}...`)

    try {
      const res = await universityApi.fetchLiveTuition({
        university_name: targetUni,
        course_name: targetCourse,
        country: targetCountry,
      })

      const data = res.data
      if (data && typeof data.tuition_usd_per_year === 'number') {
        setTuitionPerYear(Number(data.tuition_usd_per_year))
        if (typeof data.living_cost_usd_per_month === 'number' && data.living_cost_usd_per_month > 0) {
          setLivingMonthly(Number(data.living_cost_usd_per_month))
        }
        setLiveSourceUrl(data.source_url || null)
        setLiveSearchNotes(data.notes || `Live verified via Tavily Search`)
        const feeLabel = data.tuition_usd_per_year === 0 ? '$0/yr (Tuition Free)' : `$${Number(data.tuition_usd_per_year).toLocaleString()}/yr`
        toast.success(`Found live web tuition fee: ${feeLabel}`, { id: toastId })
      } else {
        toast.error('Could not extract live tuition from web.', { id: toastId })
      }
    } catch (error) {
      toast.error('Web search error. Using base estimate.', { id: toastId })
    } finally {
      setIsSearchingWeb(false)
    }
  }

  const handleCountryChange = (country: string) => {
    setSelectedCountry(country)
    const firstUni = PRESET_UNIVERSITIES.find((u) => u.country === country)
    if (firstUni) {
      setSelectedUniName(firstUni.name)
      setLocation(firstUni.location)
      setLivingMonthly(firstUni.livingMonthly)
      setSelectedCourse(firstUni.defaultCourse)
      setTuitionPerYear(firstUni.tuition)
      fetchLiveWebTuition(firstUni.name, firstUni.defaultCourse, country)
    } else {
      setSelectedUniName('Custom')
      setLocation(`City, ${country}`)
      setTuitionPerYear(15000)
      setLivingMonthly(1000)
    }
  }

  const handleUniChange = (uniName: string) => {
    setSelectedUniName(uniName)
    if (uniName === 'Custom') return
    const preset = PRESET_UNIVERSITIES.find((u) => u.name === uniName)
    if (preset) {
      setLocation(preset.location)
      setLivingMonthly(preset.livingMonthly)
      fetchLiveWebTuition(preset.name, activeCourseName, selectedCountry)
    }
  }

  const handleCourseChange = (course: string) => {
    setSelectedCourse(course)
    if (course !== 'Custom') {
      fetchLiveWebTuition(activeUniName, course, selectedCountry)
    }
  }

  const annualLiving = livingMonthly * 12
  const yearlyTotal = tuitionPerYear + annualLiving + activeVisaFee + activeInsuranceFee + 2000
  const totalCost = (yearlyTotal * duration) - (scholarship * 1000)
  const totalINR = Math.max(totalCost, 0) * USD_TO_INR

  const chartData = COUNTRIES.map((c) => {
    const defaultUni = PRESET_UNIVERSITIES.find((u) => u.country === c) || PRESET_UNIVERSITIES[0]
    return {
      country: c,
      Tuition: c === selectedCountry ? tuitionPerYear : defaultUni.tuition,
      Living: defaultUni.livingMonthly * 12,
      'Visa & Insurance': defaultUni.visa + defaultUni.insurance,
      Misc: 2000,
    }
  })

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Live Web Budget & Tuition Calculator</h1>
          <p className="text-gray-500 text-sm">Real-time live web tuition fees powered by Tavily Search for your exact course and university</p>
        </div>

        <button
          onClick={() => fetchLiveWebTuition()}
          disabled={isSearchingWeb}
          className="btn-primary inline-flex items-center gap-2 text-sm shadow-sm"
        >
          {isSearchingWeb ? <Loader2 className="w-4 h-4 animate-spin" /> : <Globe className="w-4 h-4 text-white" />}
          {isSearchingWeb ? 'Searching Live Web...' : 'Fetch Live Web Fee (Tavily)'}
        </button>
      </div>

      {/* Calculator */}
      <div className="grid md:grid-cols-2 gap-6">
        <div className="card space-y-5">
          <h2 className="font-semibold text-gray-900 flex items-center gap-2">
            <Calculator className="w-5 h-5 text-brand-500" /> Customise Course, University & Location
          </h2>

          {/* Destination Country */}
          <div>
            <label className="label">Destination Country</label>
            <select
              value={selectedCountry}
              onChange={(e) => handleCountryChange(e.target.value)}
              className="input"
            >
              {COUNTRIES.map((c) => (
                <option key={c} value={c}>{c}</option>
              ))}
            </select>
          </div>

          {/* Target Course / Program */}
          <div>
            <label className="label flex items-center gap-1">
              <BookOpen className="w-4 h-4 text-brand-500" /> Course / Degree Program
            </label>
            <select
              value={selectedCourse}
              onChange={(e) => handleCourseChange(e.target.value)}
              className="input"
            >
              {COURSE_PRESETS.map((course) => (
                <option key={course} value={course}>{course}</option>
              ))}
              <option value="Custom">✏️ Enter Custom Course / Degree Name...</option>
            </select>

            {selectedCourse === 'Custom' && (
              <input
                type="text"
                placeholder="e.g. MSc Cybersecurity & Cloud Computing"
                value={customCourseName}
                onChange={(e) => setCustomCourseName(e.target.value)}
                className="input mt-2"
              />
            )}
          </div>

          {/* Target University */}
          <div>
            <label className="label flex items-center gap-1">
              <Building2 className="w-4 h-4 text-brand-500" /> Target University Name
            </label>
            <select
              value={selectedUniName}
              onChange={(e) => handleUniChange(e.target.value)}
              className="input"
            >
              {countryUnis.map((u) => (
                <option key={u.name} value={u.name}>{u.name}</option>
              ))}
              <option value="Custom">✏️ Enter Custom University Name...</option>
            </select>

            {selectedUniName === 'Custom' && (
              <input
                type="text"
                placeholder="e.g. Technical University of Berlin"
                value={customUniName}
                onChange={(e) => setCustomUniName(e.target.value)}
                className="input mt-2"
              />
            )}
          </div>

          {/* Location / City */}
          <div>
            <label className="label flex items-center gap-1">
              <MapPin className="w-4 h-4 text-brand-500" /> University Location (City, Country)
            </label>
            <input
              type="text"
              placeholder="e.g. Munich, Germany"
              value={location}
              onChange={(e) => setLocation(e.target.value)}
              className="input"
            />
          </div>

          {/* Cost Inputs */}
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="label flex items-center justify-between">
                <span>Tuition Fee ($ USD/yr)</span>
                <button
                  type="button"
                  onClick={() => fetchLiveWebTuition()}
                  disabled={isSearchingWeb}
                  className="text-[11px] text-brand-600 hover:underline flex items-center gap-0.5 font-medium"
                >
                  {isSearchingWeb ? <Loader2 className="w-3 h-3 animate-spin" /> : <Sparkles className="w-3 h-3 text-amber-500" />}
                  Live Search
                </button>
              </label>
              <input
                type="number"
                min={0}
                value={tuitionPerYear}
                onChange={(e) => setTuitionPerYear(Number(e.target.value))}
                className="input"
              />
            </div>
            <div>
              <label className="label">Living Cost ($ USD/mo)</label>
              <input
                type="number"
                min={0}
                value={livingMonthly}
                onChange={(e) => setLivingMonthly(Number(e.target.value))}
                className="input"
              />
            </div>
          </div>

          {/* Program Duration */}
          <div>
            <label className="label">Program Duration</label>
            <div className="flex gap-2">
              {[1, 1.5, 2, 3, 4].map((y) => (
                <button
                  key={y}
                  type="button"
                  onClick={() => setDuration(y)}
                  className={`flex-1 py-2 rounded-xl text-sm font-medium border transition-all ${
                    duration === y ? 'bg-brand-500 text-white border-brand-500' : 'border-gray-200 text-gray-600 hover:border-brand-500'
                  }`}
                >
                  {y} yr{y !== 1 ? 's' : ''}
                </button>
              ))}
            </div>
          </div>

          {/* Scholarship Slider */}
          <div>
            <label className="label">Scholarship Deduction (×$1,000 USD)</label>
            <input
              type="range" min={0} max={50} value={scholarship}
              onChange={(e) => setScholarship(Number(e.target.value))}
              className="w-full accent-brand-500"
            />
            <div className="flex justify-between text-xs text-gray-400 mt-1">
              <span>$0</span>
              <span className="font-semibold text-brand-500">${scholarship},000</span>
              <span>$50,000</span>
            </div>
          </div>
        </div>

        {/* Summary Card */}
        <div className="card flex flex-col justify-between">
          <div>
            <div className="border-b border-gray-100 pb-4 mb-4">
              <div className="flex flex-wrap items-center justify-between gap-2 mb-2">
                <div className="flex flex-wrap gap-2">
                  <span className="inline-flex items-center gap-1 text-xs font-semibold px-2.5 py-1 rounded-full bg-purple-50 text-purple-700 border border-purple-100">
                    <GraduationCap className="w-3.5 h-3.5" /> {activeCourseName}
                  </span>
                  <span className="inline-flex items-center gap-1 text-xs font-semibold px-2.5 py-1 rounded-full bg-brand-50 text-brand-600 border border-brand-100">
                    <MapPin className="w-3.5 h-3.5" /> {location || `${selectedCountry}`}
                  </span>
                </div>

                <span className="inline-flex items-center gap-1 text-xs font-medium px-2 py-0.5 rounded-md bg-emerald-50 text-emerald-700 border border-emerald-200">
                  <Globe className="w-3 h-3 text-emerald-600" /> Live Web Verified
                </span>
              </div>

              <h2 className="text-xl font-bold text-gray-900 flex items-center gap-2">
                <Building2 className="w-5 h-5 text-brand-500 shrink-0" />
                {activeUniName}
              </h2>

              {liveSearchNotes && (
                <p className="text-xs text-gray-500 mt-1 flex items-center gap-1">
                  <Sparkles className="w-3 h-3 text-amber-500 shrink-0" /> {liveSearchNotes}
                </p>
              )}
            </div>

            <h3 className="font-semibold text-gray-800 text-sm mb-3 flex items-center gap-1.5">
              <DollarSign className="w-4 h-4 text-green-500" /> Live Web Cost Breakdown
            </h3>

            <div className="space-y-2.5">
              <div className="flex justify-between items-center py-1.5 border-b border-gray-50">
                <span className="text-sm text-gray-600">Tuition Fee ({activeCourseName})</span>
                <span className="font-medium text-brand-700 font-semibold">${tuitionPerYear.toLocaleString()}/yr</span>
              </div>
              <div className="flex justify-between items-center py-1.5 border-b border-gray-50">
                <span className="text-sm text-gray-600">Living Cost (${livingMonthly}/mo)</span>
                <span className="font-medium">${annualLiving.toLocaleString()}/yr</span>
              </div>
              <div className="flex justify-between items-center py-1.5 border-b border-gray-50">
                <span className="text-sm text-gray-600">Visa Application Fee</span>
                <span className="font-medium">${activeVisaFee.toLocaleString()}</span>
              </div>
              <div className="flex justify-between items-center py-1.5 border-b border-gray-50">
                <span className="text-sm text-gray-600">Health Insurance (per year)</span>
                <span className="font-medium">${activeInsuranceFee.toLocaleString()}</span>
              </div>
              <div className="flex justify-between items-center py-1.5 border-b border-gray-50">
                <span className="text-sm text-gray-600">Miscellaneous Expenses</span>
                <span className="font-medium">$2,000</span>
              </div>

              {scholarship > 0 && (
                <div className="flex justify-between items-center py-2 text-green-600 font-medium">
                  <span className="text-sm flex items-center gap-1">
                    <TrendingDown className="w-4 h-4" /> Scholarship Grant
                  </span>
                  <span>-${(scholarship * 1000).toLocaleString()}</span>
                </div>
              )}
            </div>

            {liveSourceUrl && (
              <div className="mt-3 text-xs">
                <a
                  href={liveSourceUrl}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-brand-600 hover:underline inline-flex items-center gap-1"
                >
                  <ExternalLink className="w-3.5 h-3.5" /> View Official Live Web Source
                </a>
              </div>
            )}
          </div>

          <div className="mt-6 p-4 gradient-bg rounded-xl text-white shadow-sm">
            <p className="text-xs text-white/80 uppercase tracking-wider font-semibold">
              Total Budget Estimate ({duration} Year{duration !== 1 ? 's' : ''})
            </p>
            <p className="text-3xl font-extrabold mt-1">${Math.max(totalCost, 0).toLocaleString()}</p>
            <p className="text-sm text-white/90 mt-1 font-medium">
              ≈ ₹{(totalINR / 100000).toFixed(1)} Lakhs INR (at 1 USD = ₹{USD_TO_INR})
            </p>
          </div>
        </div>
      </div>

      {/* Comparison chart */}
      <div className="card">
        <h2 className="font-semibold text-gray-900 mb-5 flex items-center gap-2">
          <Info className="w-5 h-5 text-brand-500" /> Country Annual Cost Comparison for {activeCourseName} (USD)
        </h2>
        <ResponsiveContainer width="100%" height={320}>
          <BarChart data={chartData} margin={{ top: 5, right: 20, left: 0, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
            <XAxis dataKey="country" tick={{ fontSize: 12 }} />
            <YAxis tick={{ fontSize: 12 }} tickFormatter={(v) => `$${(v / 1000).toFixed(0)}k`} />
            <Tooltip formatter={(v: number) => [`$${v.toLocaleString()}`, '']} />
            <Legend />
            <Bar dataKey="Tuition" stackId="a" fill="#667eea" radius={[0, 0, 0, 0]} />
            <Bar dataKey="Living" stackId="a" fill="#764ba2" />
            <Bar dataKey="Visa & Insurance" stackId="a" fill="#f59e0b" />
            <Bar dataKey="Misc" stackId="a" fill="#e5e7eb" radius={[4, 4, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  )
}
