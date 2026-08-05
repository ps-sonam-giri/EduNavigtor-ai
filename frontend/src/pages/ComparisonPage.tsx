import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { universityApi } from '@/lib/api'
import { Plus, X, TrendingUp, DollarSign, Award, MapPin, CheckCircle } from 'lucide-react'
import { motion } from 'framer-motion'

export default function ComparisonPage() {
  const [selected, setSelected] = useState<any[]>([])
  const [search, setSearch] = useState('')

  const { data: universities = [] } = useQuery({
    queryKey: ['universities'],
    queryFn: () => universityApi.list({ limit: 50 }).then((r) => r.data),
  })

  const filtered = universities.filter(
    (u: any) =>
      u.name.toLowerCase().includes(search.toLowerCase()) &&
      !selected.find((s) => s.id === u.id)
  )

  const addUni = (u: any) => {
    if (selected.length >= 4) return
    setSelected((prev) => [...prev, u])
  }

  const removeUni = (id: string) => setSelected((prev) => prev.filter((u) => u.id !== id))

  const compareFields = [
    { label: 'QS World Rank', key: 'qs_world_rank', format: (v: any) => v ? `#${v}` : 'N/A', icon: TrendingUp },
    { label: 'Tuition/year (USD)', key: 'avg_tuition_usd_per_year', format: (v: any) => v ? `$${Number(v).toLocaleString()}` : 'N/A', icon: DollarSign },
    { label: 'Acceptance Rate', key: 'acceptance_rate', format: (v: any) => v ? `${v}%` : 'N/A', icon: CheckCircle },
    { label: 'Min CGPA', key: 'min_cgpa', format: (v: any) => v || 'N/A', icon: TrendingUp },
    { label: 'Min IELTS', key: 'min_ielts', format: (v: any) => v || 'N/A', icon: CheckCircle },
    { label: 'Employment Rate', key: 'graduate_employment_rate', format: (v: any) => v ? `${v}%` : 'N/A', icon: Award },
    { label: 'Country', key: 'country', format: (v: any) => v || 'N/A', icon: MapPin },
  ]

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Compare Universities</h1>
        <p className="text-gray-500 text-sm">Add up to 4 universities for side-by-side comparison</p>
      </div>

      {/* Search */}
      <div className="card">
        <input
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          placeholder="Search and add a university..."
          className="input mb-3"
        />
        {search && (
          <div className="max-h-48 overflow-y-auto space-y-1">
            {filtered.slice(0, 8).map((u: any) => (
              <button
                key={u.id}
                onClick={() => addUni(u)}
                disabled={selected.length >= 4}
                className="w-full flex items-center justify-between px-3 py-2 hover:bg-brand-50 rounded-lg text-left transition-colors disabled:opacity-40"
              >
                <div>
                  <p className="text-sm font-medium text-gray-800">{u.name}</p>
                  <p className="text-xs text-gray-400">{u.country}</p>
                </div>
                <Plus className="w-4 h-4 text-brand-500" />
              </button>
            ))}
          </div>
        )}
      </div>

      {/* Selected chips */}
      {selected.length > 0 && (
        <div className="flex flex-wrap gap-2">
          {selected.map((u) => (
            <div key={u.id} className="flex items-center gap-2 bg-brand-500 text-white px-3 py-1.5 rounded-full text-sm">
              {u.name}
              <button onClick={() => removeUni(u.id)}><X className="w-3.5 h-3.5" /></button>
            </div>
          ))}
        </div>
      )}

      {/* Comparison table */}
      {selected.length >= 2 ? (
        <div className="card overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-gray-100">
                <th className="text-left py-3 pr-4 text-gray-500 font-medium w-40">Metric</th>
                {selected.map((u) => (
                  <th key={u.id} className="text-left py-3 px-4 text-gray-900 font-semibold min-w-40">
                    <p className="leading-snug">{u.name}</p>
                    <p className="text-xs text-gray-400 font-normal">{u.country}</p>
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {compareFields.map(({ label, key, format, icon: Icon }) => {
                const values = selected.map((u) => u[key])
                const best = key === 'qs_world_rank'
                  ? Math.min(...values.filter(Boolean))
                  : key === 'avg_tuition_usd_per_year'
                  ? Math.min(...values.filter(Boolean))
                  : key === 'graduate_employment_rate' || key === 'acceptance_rate'
                  ? Math.max(...values.filter(Boolean))
                  : null

                return (
                  <tr key={key} className="border-b border-gray-50 hover:bg-gray-50 transition-colors">
                    <td className="py-3 pr-4 text-gray-500 flex items-center gap-1.5">
                      <Icon className="w-3.5 h-3.5" /> {label}
                    </td>
                    {selected.map((u) => {
                      const val = u[key]
                      const isBest = best !== null && val === best
                      return (
                        <td key={u.id} className={`py-3 px-4 font-medium ${isBest ? 'text-green-600' : 'text-gray-800'}`}>
                          {isBest && <span className="text-xs mr-1">✓</span>}
                          {format(val)}
                        </td>
                      )
                    })}
                  </tr>
                )
              })}
            </tbody>
          </table>
        </div>
      ) : (
        <div className="text-center py-16 text-gray-400">
          <TrendingUp className="w-12 h-12 mx-auto mb-3 opacity-30" />
          <p className="font-medium">Add at least 2 universities to compare</p>
          <p className="text-sm mt-1">Search above to add universities</p>
        </div>
      )}
    </div>
  )
}
