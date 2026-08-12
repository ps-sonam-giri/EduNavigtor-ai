import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { universityApi } from '@/lib/api'
import { Plus, X, TrendingUp, DollarSign, Award, MapPin, CheckCircle, Search, Globe, Sparkles, Trash2, ArrowUpRight, GraduationCap } from 'lucide-react'
import { motion, AnimatePresence } from 'framer-motion'

const WORLD_COUNTRIES = [
  { label: 'All World 🌐', value: 'All' },
  { label: 'USA 🇺🇸', value: 'United States' },
  { label: 'UK 🇬🇧', value: 'United Kingdom' },
  { label: 'Canada 🇨🇦', value: 'Canada' },
  { label: 'Germany 🇩🇪', value: 'Germany' },
  { label: 'Australia 🇦🇺', value: 'Australia' },
  { label: 'Singapore 🇸🇬', value: 'Singapore' },
  { label: 'Japan 🇯🇵', value: 'Japan' },
  { label: 'India 🇮🇳', value: 'India' },
  { label: 'Switzerland 🇨🇭', value: 'Switzerland' },
  { label: 'France 🇫🇷', value: 'France' },
  { label: 'Netherlands 🇳🇱', value: 'Netherlands' },
  { label: 'Saudi Arabia 🇸🇦', value: 'Saudi Arabia' },
  { label: 'South Korea 🇰🇷', value: 'South Korea' },
]

export default function ComparisonPage() {
  const [selected, setSelected] = useState<any[]>([])
  const [search, setSearch] = useState('')
  const [countryFilter, setCountryFilter] = useState('All')
  const [isSearchFocused, setIsSearchFocused] = useState(false)

  // Dynamic backend search across all universities in database & live web engine worldwide
  const { data: universities = [], isLoading } = useQuery({
    queryKey: ['universities-compare', search, countryFilter],
    queryFn: () =>
      universityApi
        .list({
          search: search.trim() || undefined,
          country: countryFilter !== 'All' ? countryFilter : undefined,
          limit: 100,
        })
        .then((r) => r.data || []),
  })

  // Filter out already selected unis
  const searchResults = universities.filter(
    (u: any) => !selected.some((s) => s.name?.toLowerCase() === u.name?.toLowerCase())
  )

  const addUni = (u: any) => {
    if (selected.length >= 4) return
    setSelected((prev) => [...prev, u])
    setSearch('')
  }

  const removeUni = (id: string) => setSelected((prev) => prev.filter((u) => u.id !== id))
  const clearAll = () => setSelected([])

  // Presets for quick world comparisons
  const loadPreset = (presetNames: string[]) => {
    const matches = universities.filter((u: any) =>
      presetNames.some((p) => u.name.toLowerCase().includes(p.toLowerCase()))
    )
    if (matches.length > 0) {
      setSelected(matches.slice(0, 4))
    }
  }

  const compareFields = [
    {
      label: 'QS World Rank',
      key: 'qs_world_rank',
      format: (v: any) => (v ? `#${v}` : 'N/A'),
      icon: TrendingUp,
      isBetter: (a: number, b: number) => a < b,
    },
    {
      label: 'Tuition / Year (USD)',
      key: 'avg_tuition_usd_per_year',
      format: (v: any) => (v !== undefined && v !== null ? `$${Number(v).toLocaleString()}` : 'N/A'),
      icon: DollarSign,
      isBetter: (a: number, b: number) => a < b,
    },
    {
      label: 'Tuition / Year (INR)',
      key: 'avg_tuition_usd_per_year',
      format: (v: any) => (v !== undefined && v !== null ? `₹${(Number(v) * 83).toLocaleString('en-IN')}` : 'N/A'),
      icon: DollarSign,
      isBetter: (a: number, b: number) => a < b,
    },
    {
      label: 'Acceptance Rate',
      key: 'acceptance_rate',
      format: (v: any) => (v ? `${v}%` : 'N/A'),
      icon: CheckCircle,
      isBetter: (a: number, b: number) => a > b,
    },
    {
      label: 'Graduate Employment Rate',
      key: 'graduate_employment_rate',
      format: (v: any) => (v ? `${v}%` : 'N/A'),
      icon: Award,
      isBetter: (a: number, b: number) => a > b,
    },
    {
      label: 'Min CGPA Requirement',
      key: 'min_cgpa',
      format: (v: any) => (v ? `${v} / 10.0` : 'N/A'),
      icon: TrendingUp,
    },
    {
      label: 'Min IELTS Requirement',
      key: 'min_ielts',
      format: (v: any) => (v ? `${v} Band` : 'N/A'),
      icon: CheckCircle,
    },
    {
      label: 'Country & Flag',
      key: 'country',
      format: (v: any, u: any) => `${u.country_flag || '🎓'} ${v || 'Global'}`,
      icon: MapPin,
    },
    {
      label: 'Location / City',
      key: 'location_city',
      format: (v: any) => v || 'Main Campus',
      icon: MapPin,
    },
  ]

  return (
    <div className="space-y-6 max-w-7xl mx-auto pb-12">
      {/* Page Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-gradient-to-r from-brand-900 via-indigo-900 to-slate-900 p-6 rounded-2xl text-white shadow-xl relative overflow-hidden">
        <div className="relative z-10 space-y-1">
          <div className="flex items-center gap-2 text-brand-300 font-semibold text-xs tracking-wider uppercase">
            <Globe className="w-4 h-4 text-brand-400 animate-spin-slow" /> Global University Comparison Engine
          </div>
          <h1 className="text-2xl md:text-3xl font-extrabold text-white">Compare Universities Worldwide</h1>
          <p className="text-gray-300 text-sm max-w-2xl">
            Search & compare top global universities across tuition costs, QS rankings, admission criteria, scholarships, and career outcomes.
          </p>
        </div>
        {selected.length > 0 && (
          <button
            onClick={clearAll}
            className="relative z-10 flex items-center gap-1.5 px-4 py-2 bg-red-500/20 hover:bg-red-500/30 text-red-200 border border-red-500/40 rounded-xl text-xs font-semibold transition-all self-start md:self-auto"
          >
            <Trash2 className="w-3.5 h-3.5" /> Clear All ({selected.length})
          </button>
        )}
      </div>

      {/* World Region Selector */}
      <div className="flex items-center gap-2 overflow-x-auto pb-2 scrollbar-none">
        <span className="text-xs font-semibold text-gray-500 whitespace-nowrap flex items-center gap-1 mr-1">
          <Globe className="w-3.5 h-3.5" /> Region:
        </span>
        {WORLD_COUNTRIES.map((c) => (
          <button
            key={c.value}
            onClick={() => setCountryFilter(c.value)}
            className={`px-3 py-1.5 rounded-full text-xs font-medium whitespace-nowrap transition-all ${
              countryFilter === c.value
                ? 'bg-brand-600 text-white shadow-md shadow-brand-500/20'
                : 'bg-white text-gray-700 hover:bg-gray-100 border border-gray-200'
            }`}
          >
            {c.label}
          </button>
        ))}
      </div>

      {/* Search Bar & Auto-Suggest */}
      <div className="relative">
        <div className="relative">
          <Search className="absolute left-4 top-3.5 w-5 h-5 text-gray-400" />
          <input
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            onFocus={() => setIsSearchFocused(true)}
            placeholder="Search any university worldwide (e.g., Harvard, Oxford, TUM Munich, ETH Zurich, NUS Singapore, IIT Bombay)..."
            className="w-full pl-12 pr-4 py-3.5 bg-white border border-gray-200 rounded-xl shadow-sm focus:outline-none focus:ring-2 focus:ring-brand-500 focus:border-brand-500 text-sm font-medium text-gray-900 placeholder-gray-400 transition-all"
          />
          {search && (
            <button
              onClick={() => setSearch('')}
              className="absolute right-4 top-3.5 text-gray-400 hover:text-gray-600"
            >
              <X className="w-5 h-5" />
            </button>
          )}
        </div>

        {/* Dropdown search results */}
        {(isSearchFocused || search) && searchResults.length > 0 && (
          <div className="absolute top-full left-0 right-0 mt-2 bg-white rounded-xl shadow-2xl border border-gray-100 max-h-72 overflow-y-auto z-30 divide-y divide-gray-100">
            {isLoading ? (
              <div className="p-4 text-center text-xs text-gray-400">Searching global universities database & web engine...</div>
            ) : (
              searchResults.slice(0, 10).map((u: any) => (
                <div
                  key={u.id || u.name}
                  onClick={() => addUni(u)}
                  className="p-3 hover:bg-brand-50 cursor-pointer flex items-center justify-between transition-colors group"
                >
                  <div className="flex items-center gap-3">
                    <span className="text-xl">{u.country_flag || '🎓'}</span>
                    <div>
                      <p className="text-sm font-semibold text-gray-900 group-hover:text-brand-600">
                        {u.name}
                      </p>
                      <p className="text-xs text-gray-500 flex items-center gap-2">
                        <span>{u.country || 'Global'}</span>
                        {u.qs_world_rank && (
                          <span className="text-brand-600 font-semibold bg-brand-50 px-1.5 py-0.5 rounded text-[10px]">
                            QS #{u.qs_world_rank}
                          </span>
                        )}
                        {u.avg_tuition_usd_per_year !== undefined && (
                          <span>${Number(u.avg_tuition_usd_per_year).toLocaleString()}/yr</span>
                        )}
                      </p>
                    </div>
                  </div>
                  <button
                    disabled={selected.length >= 4}
                    className="flex items-center gap-1 text-xs font-medium text-brand-600 bg-brand-50 hover:bg-brand-100 px-3 py-1.5 rounded-lg transition-colors disabled:opacity-40"
                  >
                    <Plus className="w-3.5 h-3.5" /> Add to Compare
                  </button>
                </div>
              ))
            )}
          </div>
        )}
      </div>

      {/* Suggested Quick Comparison Presets */}
      {selected.length === 0 && (
        <div className="bg-white p-5 rounded-2xl border border-gray-100 shadow-sm space-y-3">
          <div className="flex items-center gap-2 text-xs font-semibold text-gray-700">
            <Sparkles className="w-4 h-4 text-amber-500" /> Popular Worldwide Presets (One-Click Compare):
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
            <button
              onClick={() => loadPreset(['Harvard', 'Stanford', 'Massachusetts Institute of Technology', 'Columbia'])}
              className="p-3 bg-gradient-to-br from-amber-50 to-orange-50 border border-amber-200/60 rounded-xl text-left hover:shadow-md transition-all group"
            >
              <p className="text-xs font-bold text-amber-900 group-hover:text-amber-700">🇺🇸 Ivy League & Top US</p>
              <p className="text-[11px] text-amber-700 mt-0.5">Harvard vs Stanford vs MIT vs Columbia</p>
            </button>
            <button
              onClick={() => loadPreset(['Technical University of Munich', 'ETH Zurich', 'Politecnico di Milano', 'Universitat de Barcelona'])}
              className="p-3 bg-gradient-to-br from-blue-50 to-cyan-50 border border-blue-200/60 rounded-xl text-left hover:shadow-md transition-all group"
            >
              <p className="text-xs font-bold text-blue-900 group-hover:text-blue-700">🇪🇺 Top Europe (Low Tuition)</p>
              <p className="text-[11px] text-blue-700 mt-0.5">TUM Germany vs ETH Zurich vs PoliMi</p>
            </button>
            <button
              onClick={() => loadPreset(['National University of Singapore', 'University of Tokyo', 'Tsinghua', 'Indian Institute of Science'])}
              className="p-3 bg-gradient-to-br from-emerald-50 to-teal-50 border border-emerald-200/60 rounded-xl text-left hover:shadow-md transition-all group"
            >
              <p className="text-xs font-bold text-emerald-900 group-hover:text-emerald-700">🌏 Asia Tech Leaders</p>
              <p className="text-[11px] text-emerald-700 mt-0.5">NUS vs Tokyo vs Tsinghua vs IISc</p>
            </button>
            <button
              onClick={() => loadPreset(['Georgia Institute of Technology', 'Purdue', 'UT Austin', 'UMich'])}
              className="p-3 bg-gradient-to-br from-purple-50 to-indigo-50 border border-purple-200/60 rounded-xl text-left hover:shadow-md transition-all group"
            >
              <p className="text-xs font-bold text-purple-900 group-hover:text-purple-700">🚀 High ROI Public US</p>
              <p className="text-[11px] text-purple-700 mt-0.5">Georgia Tech vs Purdue vs UT Austin</p>
            </button>
          </div>
        </div>
      )}

      {/* Selected Chips */}
      {selected.length > 0 && (
        <div className="flex flex-wrap items-center gap-2 bg-white p-3.5 rounded-xl border border-gray-200 shadow-sm">
          <span className="text-xs font-semibold text-gray-500 mr-1">Selected ({selected.length}/4):</span>
          {selected.map((u) => (
            <span
              key={u.id || u.name}
              className="inline-flex items-center gap-1.5 px-3 py-1.5 bg-brand-50 text-brand-700 border border-brand-200 rounded-full text-xs font-semibold shadow-sm"
            >
              <span>{u.country_flag || '🎓'}</span>
              <span>{u.name}</span>
              <button
                onClick={() => removeUni(u.id)}
                className="hover:bg-brand-200 rounded-full p-0.5 transition-colors text-brand-600"
              >
                <X className="w-3.5 h-3.5" />
              </button>
            </span>
          ))}
        </div>
      )}

      {/* Comparison Table */}
      {selected.length >= 2 ? (
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-white rounded-2xl border border-gray-200 shadow-md overflow-hidden"
        >
          <div className="overflow-x-auto">
            <table className="w-full text-sm border-collapse">
              <thead>
                <tr className="bg-gray-50 border-b border-gray-200">
                  <th className="text-left p-4 text-xs font-bold uppercase tracking-wider text-gray-500 w-48 bg-gray-50 sticky left-0 z-10 shadow-sm">
                    Comparison Metrics
                  </th>
                  {selected.map((u) => (
                    <th key={u.id || u.name} className="p-4 text-left min-w-64 border-l border-gray-200">
                      <div className="flex items-start justify-between">
                        <div>
                          <span className="text-2xl">{u.country_flag || '🎓'}</span>
                          <h3 className="font-bold text-gray-900 text-base leading-tight mt-1">{u.name}</h3>
                          <p className="text-xs text-gray-500 mt-0.5">{u.country || 'Global'} • {u.location_city || 'Campus'}</p>
                        </div>
                        <button
                          onClick={() => removeUni(u.id)}
                          className="text-gray-400 hover:text-red-500 p-1"
                        >
                          <X className="w-4 h-4" />
                        </button>
                      </div>
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100">
                {compareFields.map(({ label, key, format, icon: Icon, isBetter }) => {
                  const values = selected.map((u) => u[key]).filter((v) => v !== undefined && v !== null)
                  let bestVal: any = null
                  if (isBetter && values.length > 1) {
                    bestVal = values.reduce((prev, curr) => (isBetter(curr, prev) ? curr : prev))
                  }

                  return (
                    <tr key={label} className="hover:bg-gray-50/80 transition-colors">
                      <td className="p-4 font-semibold text-gray-700 bg-white sticky left-0 z-10 border-r border-gray-100 flex items-center gap-2">
                        <Icon className="w-4 h-4 text-brand-500" />
                        {label}
                      </td>
                      {selected.map((u) => {
                        const val = u[key]
                        const isWinner = bestVal !== null && val === bestVal

                        return (
                          <td
                            key={u.id || u.name}
                            className={`p-4 border-l border-gray-100 ${
                              isWinner ? 'bg-emerald-50/60 font-bold text-emerald-900' : 'text-gray-800'
                            }`}
                          >
                            <div className="flex items-center justify-between">
                              <span>{format(val, u)}</span>
                              {isWinner && (
                                <span className="inline-flex items-center gap-1 px-2 py-0.5 bg-emerald-100 text-emerald-700 rounded text-[10px] font-bold">
                                  <CheckCircle className="w-3 h-3" /> Best Choice
                                </span>
                              )}
                            </div>
                          </td>
                        )
                      })}
                    </tr>
                  )
                })}

                {/* Programs Offered */}
                <tr className="hover:bg-gray-50/80 transition-colors">
                  <td className="p-4 font-semibold text-gray-700 bg-white sticky left-0 z-10 border-r border-gray-100 flex items-center gap-2">
                    <GraduationCap className="w-4 h-4 text-indigo-500" /> Key Programs & Degrees
                  </td>
                  {selected.map((u) => (
                    <td key={u.id || u.name} className="p-4 border-l border-gray-100 text-xs text-gray-700">
                      {Array.isArray(u.programs) && u.programs.length > 0 ? (
                        <ul className="space-y-1">
                          {u.programs.slice(0, 3).map((p: any, idx: number) => (
                            <li key={idx} className="flex items-center gap-1.5">
                              <span className="w-1.5 h-1.5 bg-indigo-500 rounded-full"></span>
                              <span>{typeof p === 'string' ? p : p.name || 'Master Program'}</span>
                            </li>
                          ))}
                        </ul>
                      ) : (
                        <span>MSc Computer Science, Data Science, MBA</span>
                      )}
                    </td>
                  ))}
                </tr>

                {/* Scholarships */}
                <tr className="hover:bg-gray-50/80 transition-colors">
                  <td className="p-4 font-semibold text-gray-700 bg-white sticky left-0 z-10 border-r border-gray-100 flex items-center gap-2">
                    <Award className="w-4 h-4 text-amber-500" /> Scholarships Offered
                  </td>
                  {selected.map((u) => (
                    <td key={u.id || u.name} className="p-4 border-l border-gray-100 text-xs">
                      {Array.isArray(u.offered_scholarships) && u.offered_scholarships.length > 0 ? (
                        <div className="flex flex-wrap gap-1">
                          {u.offered_scholarships.map((s: string, idx: number) => (
                            <span key={idx} className="px-2 py-0.5 bg-amber-50 text-amber-800 border border-amber-200 rounded text-[11px]">
                              {s}
                            </span>
                          ))}
                        </div>
                      ) : (
                        <span className="text-gray-500">Merit Entrance Grants Available</span>
                      )}
                    </td>
                  ))}
                </tr>
              </tbody>
            </table>
          </div>
        </motion.div>
      ) : (
        /* Empty State */
        <div className="bg-white rounded-2xl border border-gray-200 p-12 text-center shadow-sm">
          <div className="w-16 h-16 bg-brand-50 text-brand-500 rounded-2xl flex items-center justify-center mx-auto mb-4 shadow-inner">
            <Globe className="w-8 h-8" />
          </div>
          <h3 className="text-lg font-bold text-gray-900">Select at least 2 universities to compare</h3>
          <p className="text-gray-500 text-sm max-w-md mx-auto mt-1">
            Search any university worldwide in the search bar above or choose one of our popular presets to compare rankings, fees, and career outcomes.
          </p>
        </div>
      )}
    </div>
  )
}

