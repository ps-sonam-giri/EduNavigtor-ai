import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { Link } from 'react-router-dom'
import { universityApi } from '@/lib/api'
import { Search, Filter, GraduationCap, MapPin, TrendingUp, ArrowRight, Star } from 'lucide-react'
import { motion } from 'framer-motion'

const COUNTRIES = ['All', 'United States', 'United Kingdom', 'Canada', 'Australia', 'Germany']

export default function UniversitiesPage() {
  const [search, setSearch] = useState('')
  const [country, setCountry] = useState('All')
  const [maxTuition, setMaxTuition] = useState('')

  const { data: universities = [], isLoading } = useQuery({
    queryKey: ['universities', country, maxTuition],
    queryFn: () =>
      universityApi.list({
        country: country !== 'All' ? country : undefined,
        max_tuition: maxTuition || undefined,
        limit: 30,
      }).then((r) => r.data),
  })

  const filtered = universities.filter((u: any) =>
    u.name.toLowerCase().includes(search.toLowerCase()) ||
    u.country?.toLowerCase().includes(search.toLowerCase())
  )

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Universities</h1>
        <p className="text-gray-500 text-sm">Browse universities from our AI-curated database</p>
      </div>

      {/* Filters */}
      <div className="card">
        <div className="flex flex-col md:flex-row gap-4">
          <div className="relative flex-1">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
            <input
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Search universities..."
              className="input pl-10"
            />
          </div>
          <select value={country} onChange={(e) => setCountry(e.target.value)} className="input md:w-48">
            {COUNTRIES.map((c) => <option key={c} value={c}>{c}</option>)}
          </select>
          <div className="relative md:w-48">
            <span className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 text-sm">Max $</span>
            <input
              value={maxTuition}
              onChange={(e) => setMaxTuition(e.target.value)}
              placeholder="Max tuition/yr"
              type="number"
              className="input pl-10"
            />
          </div>
        </div>
      </div>

      {isLoading ? (
        <div className="flex items-center justify-center h-40">
          <div className="animate-spin w-8 h-8 border-2 border-brand-500 border-t-transparent rounded-full" />
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
          {filtered.map((uni: any, i: number) => (
            <motion.div
              key={uni.id}
              initial={{ opacity: 0, y: 15 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.04 }}
            >
              <Link to={`/universities/${uni.id}`} className="card hover:shadow-md hover:-translate-y-0.5 transition-all duration-200 block group h-full">
                {/* Rank badge */}
                <div className="flex items-start justify-between mb-3">
                  <div>
                    {uni.qs_world_rank && (
                      <span className="badge badge-purple mb-2 block w-fit">QS #{uni.qs_world_rank}</span>
                    )}
                    <h3 className="font-semibold text-gray-900 group-hover:text-brand-500 transition-colors leading-snug">
                      {uni.name}
                    </h3>
                  </div>
                  {uni.has_scholarships && (
                    <span className="badge badge-green ml-2 whitespace-nowrap flex-shrink-0">Scholarships</span>
                  )}
                </div>

                <div className="space-y-1.5 text-sm text-gray-500 mb-4">
                  <div className="flex items-center gap-1.5">
                    <MapPin className="w-3.5 h-3.5" />
                    {uni.location_city ? `${uni.location_city}, ` : ''}{uni.country}
                  </div>
                  {uni.avg_tuition_usd_per_year && (
                    <div className="flex items-center gap-1.5">
                      <span className="text-green-600 font-medium">
                        ${Number(uni.avg_tuition_usd_per_year).toLocaleString()}/yr
                      </span>
                      <span className="text-gray-400">tuition</span>
                    </div>
                  )}
                  {uni.min_cgpa && (
                    <div className="flex items-center gap-1.5">
                      <TrendingUp className="w-3.5 h-3.5" />
                      Min CGPA: {uni.min_cgpa}
                    </div>
                  )}
                  {uni.graduate_employment_rate && (
                    <div className="flex items-center gap-1.5">
                      <Star className="w-3.5 h-3.5 text-amber-500" />
                      {uni.graduate_employment_rate}% employment rate
                    </div>
                  )}
                </div>

                {uni.programs && uni.programs.length > 0 && (
                  <div className="flex flex-wrap gap-1 mb-4">
                    {uni.programs.slice(0, 2).map((p: any) => (
                      <span key={p.name} className="badge badge-blue text-xs">{p.name}</span>
                    ))}
                    {uni.programs.length > 2 && (
                      <span className="badge badge-blue text-xs">+{uni.programs.length - 2} more</span>
                    )}
                  </div>
                )}

                <div className="flex items-center justify-between text-xs text-gray-400 border-t border-gray-100 pt-3">
                  <span>Acceptance: {uni.acceptance_rate ? `${uni.acceptance_rate}%` : 'N/A'}</span>
                  <ArrowRight className="w-4 h-4 group-hover:text-brand-500 transition-colors" />
                </div>
              </Link>
            </motion.div>
          ))}
        </div>
      )}

      {!isLoading && filtered.length === 0 && (
        <div className="text-center py-12 text-gray-400">
          <GraduationCap className="w-12 h-12 mx-auto mb-3 opacity-30" />
          <p>No universities found for these filters</p>
        </div>
      )}
    </div>
  )
}
