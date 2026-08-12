import { useState, useMemo } from 'react'
import { useQuery } from '@tanstack/react-query'
import { Link } from 'react-router-dom'
import { universityApi } from '@/lib/api'
import { Search, MapPin, TrendingUp, ArrowRight, Star, Award, DollarSign, CheckCircle2, ShieldCheck } from 'lucide-react'
import { motion } from 'framer-motion'

import { ALL_WORLD_COUNTRIES, TOP_POPULAR_COUNTRIES } from './ProfilePage'
import { Globe, Sparkles, Loader2 } from 'lucide-react'

const COUNTRY_TABS = [
  { label: '🌍 All Countries', value: 'All' },
  { label: '🇩🇪 Germany', value: 'Germany' },
  { label: '🇺🇸 United States', value: 'United States' },
  { label: '🇬🇧 United Kingdom', value: 'United Kingdom' },
  { label: '🇨🇦 Canada', value: 'Canada' },
  { label: '🇦🇺 Australia', value: 'Australia' },
  { label: '🇮🇪 Ireland', value: 'Ireland' },
  { label: '🇫🇷 France', value: 'France' },
  { label: '🇳🇱 Netherlands', value: 'Netherlands' },
  { label: '🇸🇪 Sweden', value: 'Sweden' },
  { label: '🇨🇭 Switzerland', value: 'Switzerland' },
  { label: '🇸🇬 Singapore', value: 'Singapore' },
  { label: '🇯🇵 Japan', value: 'Japan' },
  { label: '🇰🇷 South Korea', value: 'South Korea' },
  { label: '🇮🇹 Italy', value: 'Italy' },
  { label: '🇪🇸 Spain', value: 'Spain' },
  { label: '🇦🇪 UAE', value: 'United Arab Emirates' },
  { label: '🇮🇳 India', value: 'India' },
]

const DEFAULT_MEDIA: Record<string, { image: string; flag: string; offered: string[]; accepted: string[] }> = {
  'Technical University of Munich': {
    image: 'https://images.unsplash.com/photo-1592285850226-4579458e8996?auto=format&fit=crop&w=800&q=80',
    flag: '🇩🇪',
    offered: ['TUM Dean’s Excellence Grant (€1,500/sem)', 'TUM Merit Tuition Waiver', 'Graduate Research Assistantship'],
    accepted: ['DAAD EPOS Scholarship', 'Deutschlandstipendium (€300/mo)', 'National Overseas Scholarship (NOS India)'],
  },
  'LMU Munich': {
    image: 'https://images.unsplash.com/photo-1541339907198-e08756dedf3f?auto=format&fit=crop&w=800&q=80',
    flag: '🇩🇪',
    offered: ['LMU Merit Entrance Award', 'International Student Emergency Grant'],
    accepted: ['DAAD Scholarship', 'Deutschlandstipendium', 'Konrad-Adenauer-Stiftung Grant', 'JN Tata Endowment'],
  },
  'RWTH Aachen University': {
    image: 'https://images.unsplash.com/photo-1562774053-701939374585?auto=format&fit=crop&w=800&q=80',
    flag: '🇩🇪',
    offered: ['RWTH Aachen Excellence Stipend', 'Research Assistantship (HiWi)'],
    accepted: ['DAAD EPOS Scholarship', 'Deutschlandstipendium', 'National Overseas Scholarship (NOS)'],
  },
  'Massachusetts Institute of Technology': {
    image: 'https://images.unsplash.com/photo-1564981797816-1043664bf78d?auto=format&fit=crop&w=800&q=80',
    flag: '🇺🇸',
    offered: ['MIT Graduate Fellowship (Full Tuition + $40k/yr)', 'Research Assistantship (RA)', 'Teaching Assistantship (TA)'],
    accepted: ['Fulbright Foreign Student Program', 'AAUW International Fellowship', 'JN Tata Endowment', 'Inlaks Foundation'],
  },
  'Stanford University': {
    image: 'https://images.unsplash.com/photo-1580582932707-520aed937b7b?auto=format&fit=crop&w=800&q=80',
    flag: '🇺🇸',
    offered: ['Knight-Hennessy Scholars (Full Tuition + Living)', 'Stanford Graduate Fellowship', 'Engineering Need Grant'],
    accepted: ['Fulbright Scholarship', 'AAUW Fellowship', 'Inlaks Foundation Grant', 'JN Tata Endowment'],
  },
  'Carnegie Mellon University': {
    image: 'https://images.unsplash.com/photo-1498243691581-b145c3f54a5a?auto=format&fit=crop&w=800&q=80',
    flag: '🇺🇸',
    offered: ['SCS Graduate Merit Fellowship ($15,000)', 'CMU Dean’s Tuition Grant', 'Research Assistantship'],
    accepted: ['Fulbright Foreign Student Grant', 'JN Tata Endowment', 'Aga Khan International Scholarship'],
  },
  'University of Oxford': {
    image: 'https://images.unsplash.com/photo-1534447677768-be436bb09401?auto=format&fit=crop&w=800&q=80',
    flag: '🇬🇧',
    offered: ['Clarendon Fund Scholarship (Full Tuition + £18,622/yr)', 'Oxford-Weidenfeld and Hoffmann Award'],
    accepted: ['Chevening Master’s Scholarship', 'Commonwealth Scholarship', 'Gates Cambridge', 'Inlaks Foundation'],
  },
  'University of Cambridge': {
    image: 'https://images.unsplash.com/photo-1520986606214-8b456906c813?auto=format&fit=crop&w=800&q=80',
    flag: '🇬🇧',
    offered: ['Gates Cambridge Scholarship (Full Cost + £20,000/yr)', 'Cambridge Trust International Scholarship'],
    accepted: ['Chevening Scholarship', 'Commonwealth Master’s/PhD', 'JN Tata Endowment', 'Inlaks Foundation'],
  },
  'University of Toronto': {
    image: 'https://images.unsplash.com/photo-1523050854058-8df90110c9f1?auto=format&fit=crop&w=800&q=80',
    flag: '🇨🇦',
    offered: ['Lester B. Pearson International Scholarship (100% Tuition + Housing)', 'U of T International Scholar Award ($20k/yr)'],
    accepted: ['Vanier Canada Graduate Scholarship ($50,000/yr)', 'Pierre Elliott Trudeau Doctoral Award', 'NOS India'],
  },
  'University of British Columbia': {
    image: 'https://images.unsplash.com/photo-1509062522246-3755977927d7?auto=format&fit=crop&w=800&q=80',
    flag: '🇨🇦',
    offered: ['Karen McKellin International Leader of Tomorrow Award', 'UBC Graduate Support Initiative (GSI)'],
    accepted: ['Vanier Canada Graduate Scholarship', 'International Major Entrance Scholarship (IMES)'],
  },
  'University of Melbourne': {
    image: 'https://images.unsplash.com/photo-1541829070764-84a7d30dd3f3?auto=format&fit=crop&w=800&q=80',
    flag: '🇦🇺',
    offered: ['Melbourne Research Scholarship (100% Tuition + AUD $37,000/yr)', 'Melbourne International Undergraduate Scholarship'],
    accepted: ['Australian Govt Research Training Program (RTP)', 'Australia Awards Scholarship'],
  },
  'Trinity College Dublin': {
    image: 'https://images.unsplash.com/photo-1590012314607-cda9d9b699ae?auto=format&fit=crop&w=800&q=80',
    flag: '🇮🇪',
    offered: ['Global Excellence Postgraduate Scholarship (€5,000)', 'TCD School of Computer Science Merit Award'],
    accepted: ['Government of Ireland International Education Scholarship (€10,000 + 100% Waiver)', 'JN Tata Endowment'],
  },
}

export default function UniversitiesPage() {
  const [search, setSearch] = useState('')
  const [selectedCountryTab, setSelectedCountryTab] = useState('All')
  const [maxTuition, setMaxTuition] = useState('')
  const [isLiveSearch, setIsLiveSearch] = useState(false)

  const { data: universities = [], isLoading, isFetching } = useQuery({
    queryKey: ['universities', selectedCountryTab, search, maxTuition, isLiveSearch],
    queryFn: () =>
      universityApi.list({
        country: selectedCountryTab !== 'All' ? selectedCountryTab : undefined,
        search: search || undefined,
        max_tuition: maxTuition || undefined,
        live: isLiveSearch,
        limit: 50,
      }).then((r: any) => r.data),
  })

  const filtered = useMemo(() => {
    return universities.filter((u: any) => {
      const q = search.toLowerCase().trim()
      const matchSearch =
        !q ||
        u.name.toLowerCase().includes(q) ||
        u.country?.toLowerCase().includes(q) ||
        u.location_city?.toLowerCase().includes(q)
      const matchCountry =
        selectedCountryTab === 'All' ||
        (u.country && u.country.toLowerCase().includes(selectedCountryTab.toLowerCase()))
      return matchSearch && matchCountry
    })
  }, [universities, search, selectedCountryTab])

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-3">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Worldwide Universities & Campus Explorer</h1>
          <p className="text-gray-500 text-sm">Explore top universities across all 195+ countries with live web search, tuition fees, and scholarship waivers</p>
        </div>

        <button
          type="button"
          onClick={() => setIsLiveSearch(!isLiveSearch)}
          className={`px-4 py-2 rounded-xl text-xs font-bold transition-all flex items-center gap-2 shadow-xs shrink-0 self-start md:self-auto ${
            isLiveSearch
              ? 'bg-gradient-to-r from-purple-600 to-indigo-600 text-white shadow-md'
              : 'bg-white text-gray-700 border border-gray-200 hover:border-purple-400 hover:bg-purple-50/50'
          }`}
        >
          {isLiveSearch ? <Sparkles className="w-4 h-4 text-amber-300 animate-pulse" /> : <Globe className="w-4 h-4 text-brand-600" />}
          {isLiveSearch ? '🌐 Live Web Search Mode Active' : 'Search Live Web Worldwide'}
        </button>
      </div>

      {/* Country Tabs & Dropdown */}
      <div className="space-y-3">
        <div className="flex items-center gap-2 overflow-x-auto pb-1 scrollbar-none border-b border-gray-100">
          {COUNTRY_TABS.map((tab) => (
            <button
              key={tab.value}
              onClick={() => setSelectedCountryTab(tab.value)}
              className={`px-3.5 py-2 rounded-xl text-xs font-semibold whitespace-nowrap transition-all flex items-center gap-1.5 ${
                selectedCountryTab === tab.value
                  ? 'bg-brand-500 text-white shadow-xs'
                  : 'bg-white text-gray-600 border border-gray-200 hover:border-brand-300 hover:bg-brand-50/50'
              }`}
            >
              {tab.label}
            </button>
          ))}
        </div>

        {/* 195+ Countries Dropdown */}
        <div className="flex items-center gap-2">
          <label className="text-xs font-medium text-slate-500 whitespace-nowrap">Filter by 195+ World Countries:</label>
          <select
            value={selectedCountryTab}
            onChange={(e) => setSelectedCountryTab(e.target.value)}
            className="input text-xs py-1.5 font-medium cursor-pointer bg-white max-w-xs"
          >
            <option value="All">🌍 All Countries (Global)</option>
            <optgroup label="🔥 Popular Study Abroad Destinations">
              {TOP_POPULAR_COUNTRIES.map((c) => (
                <option key={c.name} value={c.name}>
                  {c.flag} {c.name}
                </option>
              ))}
            </optgroup>
            <optgroup label="🌐 All Sovereign Nations (195+ Available)">
              {ALL_WORLD_COUNTRIES.map((c) => {
                const topMatch = TOP_POPULAR_COUNTRIES.find((item) => item.name === c)
                const flag = topMatch ? topMatch.flag : '🌐'
                return (
                  <option key={c} value={c}>
                    {flag} {c}
                  </option>
                )
              })}
            </optgroup>
          </select>
        </div>
      </div>

      {/* Filter Inputs */}
      <div className="card">
        <div className="flex flex-col md:flex-row gap-4">
          <div className="relative flex-1">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
            <input
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Search any university worldwide (e.g. Sorbonne, ETH Zurich, NUS, Harvard, TUM, Tokyo...)"
              className="input pl-10 text-sm"
            />
          </div>
          <div className="relative md:w-56">
            <span className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 text-sm">Max $</span>
            <input
              value={maxTuition}
              onChange={(e) => setMaxTuition(e.target.value)}
              placeholder="Max tuition budget/yr"
              type="number"
              className="input pl-14 text-sm"
            />
          </div>
        </div>
      </div>

      {isLoading ? (
        <div className="flex items-center justify-center h-48">
          <div className="animate-spin w-8 h-8 border-2 border-brand-500 border-t-transparent rounded-full" />
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filtered.map((uni: any, i: number) => {
            const media = DEFAULT_MEDIA[uni.name] || {
              image: uni.image_url || 'https://images.unsplash.com/photo-1541339907198-e08756dedf3f?auto=format&fit=crop&w=800&q=80',
              flag: uni.country_flag || '🎓',
              offered: uni.offered_scholarships || ['University Entrance Merit Scholarship', 'Graduate Teaching/Research Assistantship'],
              accepted: uni.accepted_scholarships || ['DAAD Scholarship', 'Fulbright Program', 'Chevening Grant', 'NOS India'],
            }

            const tuitionVal = Number(uni.avg_tuition_usd_per_year)
            const tuitionLabel = tuitionVal === 0 ? 'Free Tuition ($0/yr)' : `$${tuitionVal.toLocaleString()}/yr`

            return (
              <motion.div
                key={uni.id}
                initial={{ opacity: 0, y: 15 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: i * 0.04 }}
              >
                <Link
                  to={`/universities/${uni.id}`}
                  className="card !p-0 overflow-hidden hover:shadow-lg hover:-translate-y-1 transition-all duration-200 block group h-full flex flex-col justify-between"
                >
                  <div>
                    {/* Campus Picture Banner */}
                    <div className="relative h-44 w-full overflow-hidden bg-gray-100">
                      <img
                        src={uni.image_url || media.image}
                        alt={uni.name}
                        className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                        onError={(e) => {
                          // Fallback photo
                          ;(e.target as HTMLImageElement).src = 'https://images.unsplash.com/photo-1541339907198-e08756dedf3f?auto=format&fit=crop&w=800&q=80'
                        }}
                      />
                      <div className="absolute inset-0 bg-gradient-to-t from-black/70 via-black/20 to-transparent" />

                      {/* Top Badges */}
                      <div className="absolute top-3 left-3 right-3 flex items-center justify-between">
                        <span className="text-sm px-2.5 py-1 rounded-full bg-white/90 backdrop-blur-md text-gray-900 font-semibold shadow-sm flex items-center gap-1">
                          <span>{media.flag}</span> {uni.country}
                        </span>

                        {uni.qs_world_rank && (
                          <span className="text-xs px-2.5 py-1 rounded-full bg-purple-600/90 backdrop-blur-md text-white font-bold shadow-sm">
                            QS World Rank #{uni.qs_world_rank}
                          </span>
                        )}
                      </div>

                      {/* Bottom Title on Image */}
                      <div className="absolute bottom-3 left-3 right-3 text-white">
                        <h3 className="font-bold text-lg leading-snug group-hover:text-amber-300 transition-colors drop-shadow-md">
                          {uni.name}
                        </h3>
                        <p className="text-xs text-gray-200 flex items-center gap-1 mt-0.5">
                          <MapPin className="w-3.5 h-3.5 text-amber-400 shrink-0" />
                          {uni.location_city ? `${uni.location_city}, ` : ''}{uni.country}
                        </p>
                      </div>
                    </div>

                    {/* Stats & Tuition */}
                    <div className="p-4 space-y-3">
                      <div className="flex items-center justify-between py-2 px-3 bg-gray-50 rounded-xl text-xs">
                        <div>
                          <span className="text-gray-400 block text-[11px]">Tuition Fee</span>
                          <span className={`font-bold ${tuitionVal === 0 ? 'text-emerald-600' : 'text-gray-900'}`}>
                            {tuitionLabel}
                          </span>
                        </div>
                        {uni.acceptance_rate && (
                          <div>
                            <span className="text-gray-400 block text-[11px]">Acceptance</span>
                            <span className="font-bold text-gray-900">{uni.acceptance_rate}%</span>
                          </div>
                        )}
                        {uni.min_cgpa && (
                          <div>
                            <span className="text-gray-400 block text-[11px]">Min CGPA</span>
                            <span className="font-bold text-purple-700">{uni.min_cgpa}/10</span>
                          </div>
                        )}
                      </div>

                      {/* Offered & Accepted Scholarships Box */}
                      <div className="space-y-2 bg-amber-50/60 border border-amber-100 rounded-xl p-3 text-xs">
                        <div className="flex items-center gap-1.5 font-bold text-amber-900 text-xs">
                          <Award className="w-4 h-4 text-amber-600 shrink-0" />
                          <span>Offered & Accepted Scholarships</span>
                        </div>

                        <div className="space-y-1">
                          <p className="text-[11px] font-semibold text-amber-800">🏛️ University Offered:</p>
                          <ul className="space-y-0.5 text-gray-700 pl-1">
                            {media.offered.slice(0, 2).map((off, idx) => (
                              <li key={idx} className="flex items-start gap-1 line-clamp-1">
                                <CheckCircle2 className="w-3 h-3 text-amber-600 shrink-0 mt-0.5" />
                                <span>{off}</span>
                              </li>
                            ))}
                          </ul>
                        </div>

                        <div className="space-y-1 pt-1 border-t border-amber-200/50">
                          <p className="text-[11px] font-semibold text-amber-800">🌐 External Grants Accepted:</p>
                          <p className="text-[11px] text-gray-600 font-medium leading-tight">
                            {media.accepted.slice(0, 3).join(' • ')}
                          </p>
                        </div>
                      </div>
                    </div>
                  </div>

                  {/* Footer */}
                  <div className="px-4 py-3 bg-gray-50/50 border-t border-gray-100 flex items-center justify-between text-xs text-brand-600 font-semibold group-hover:bg-brand-50/50 transition-colors">
                    <span className="flex items-center gap-1">
                      <ShieldCheck className="w-3.5 h-3.5 text-emerald-500" /> View Full Campus & Scholarships
                    </span>
                    <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
                  </div>
                </Link>
              </motion.div>
            )
          })}
        </div>
      )}

      {!isLoading && filtered.length === 0 && (
        <div className="text-center py-12 card">
          <MapPin className="w-10 h-10 text-gray-300 mx-auto mb-3" />
          <h3 className="font-semibold text-gray-700">No universities found for this country filter</h3>
          <p className="text-sm text-gray-400 mt-1">Try selecting '🌍 All Countries' or clear your tuition limit.</p>
        </div>
      )}
    </div>
  )
}
