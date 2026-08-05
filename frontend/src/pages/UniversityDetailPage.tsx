import { useParams, Link } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { universityApi } from '@/lib/api'
import { ArrowLeft, Globe, MapPin, TrendingUp, Award, DollarSign, Calendar, CheckCircle } from 'lucide-react'
import { motion } from 'framer-motion'

export default function UniversityDetailPage() {
  const { id } = useParams<{ id: string }>()

  const { data: uni, isLoading } = useQuery({
    queryKey: ['university', id],
    queryFn: () => universityApi.get(id!).then((r) => r.data),
  })

  if (isLoading) return (
    <div className="flex items-center justify-center h-64">
      <div className="animate-spin w-8 h-8 border-2 border-brand-500 border-t-transparent rounded-full" />
    </div>
  )

  if (!uni) return <div className="text-center text-gray-400 py-12">University not found</div>

  return (
    <div className="max-w-4xl space-y-6">
      <Link to="/universities" className="flex items-center gap-2 text-gray-500 hover:text-brand-500 transition-colors text-sm">
        <ArrowLeft className="w-4 h-4" /> Back to Universities
      </Link>

      {/* Header */}
      <motion.div initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }} className="card">
        <div className="flex items-start justify-between flex-wrap gap-4">
          <div>
            {uni.qs_world_rank && <span className="badge badge-purple mb-2">QS World Rank #{uni.qs_world_rank}</span>}
            <h1 className="text-2xl font-bold text-gray-900 mt-1">{uni.name}</h1>
            <div className="flex items-center gap-2 text-gray-500 mt-2">
              <MapPin className="w-4 h-4" />
              {uni.location_city ? `${uni.location_city}, ` : ''}{uni.country}
            </div>
            {uni.website && (
              <a href={uni.website} target="_blank" rel="noreferrer" className="flex items-center gap-1 text-brand-500 text-sm mt-1 hover:underline">
                <Globe className="w-3.5 h-3.5" /> {uni.website}
              </a>
            )}
          </div>
          <div className="flex gap-2">
            {uni.has_scholarships && <span className="badge badge-green">Scholarships Available</span>}
          </div>
        </div>
        {uni.overview && <p className="text-gray-600 mt-4 leading-relaxed">{uni.overview}</p>}
      </motion.div>

      {/* Stats grid */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {[
          { label: 'Tuition/year', value: uni.avg_tuition_usd_per_year ? `$${Number(uni.avg_tuition_usd_per_year).toLocaleString()}` : 'N/A', icon: DollarSign, color: 'text-green-500' },
          { label: 'Acceptance Rate', value: uni.acceptance_rate ? `${uni.acceptance_rate}%` : 'N/A', icon: TrendingUp, color: 'text-blue-500' },
          { label: 'Min CGPA', value: uni.min_cgpa || 'N/A', icon: CheckCircle, color: 'text-purple-500' },
          { label: 'Employment Rate', value: uni.graduate_employment_rate ? `${uni.graduate_employment_rate}%` : 'N/A', icon: Award, color: 'text-orange-500' },
        ].map(({ label, value, icon: Icon, color }) => (
          <div key={label} className="card flex items-center gap-3">
            <Icon className={`w-8 h-8 ${color} flex-shrink-0`} />
            <div>
              <p className="text-xs text-gray-400">{label}</p>
              <p className="font-bold text-gray-900">{String(value)}</p>
            </div>
          </div>
        ))}
      </div>

      <div className="grid md:grid-cols-2 gap-6">
        {/* Admission Requirements */}
        <div className="card">
          <h2 className="font-semibold text-gray-900 mb-4">Admission Requirements</h2>
          <dl className="space-y-2 text-sm">
            {[
              ['Min CGPA', uni.min_cgpa],
              ['Min IELTS', uni.min_ielts],
              ['Min TOEFL', uni.min_toefl],
              ['Min GRE', uni.min_gre],
              ['Application Fee', uni.application_fee_usd ? `$${uni.application_fee_usd}` : null],
            ].map(([k, v]) => v ? (
              <div key={String(k)} className="flex justify-between py-1 border-b border-gray-50">
                <dt className="text-gray-500">{String(k)}</dt>
                <dd className="font-medium text-gray-900">{String(v)}</dd>
              </div>
            ) : null)}
          </dl>
        </div>

        {/* Programs */}
        <div className="card">
          <h2 className="font-semibold text-gray-900 mb-4">Available Programs</h2>
          <div className="space-y-2">
            {uni.programs?.map((p: any) => (
              <div key={p.name} className="flex items-center justify-between py-2 border-b border-gray-50 last:border-0">
                <div>
                  <p className="text-sm font-medium text-gray-800">{p.name}</p>
                  <p className="text-xs text-gray-400">{p.duration_years} year{p.duration_years !== 1 ? 's' : ''}</p>
                </div>
                {p.tuition_usd && (
                  <span className="text-sm font-semibold text-green-600">${Number(p.tuition_usd).toLocaleString()}/yr</span>
                )}
              </div>
            ))}
          </div>
          <div className="mt-4 flex items-center gap-2 text-sm text-gray-500">
            <Calendar className="w-4 h-4" />
            Intake: {uni.intake_months?.join(', ') || 'N/A'}
          </div>
        </div>

        {/* Strengths */}
        {uni.strengths?.length > 0 && (
          <div className="card">
            <h2 className="font-semibold text-gray-900 mb-4">Key Strengths</h2>
            <ul className="space-y-2">
              {uni.strengths.map((s: string) => (
                <li key={s} className="flex items-start gap-2 text-sm text-gray-700">
                  <CheckCircle className="w-4 h-4 text-green-500 flex-shrink-0 mt-0.5" />
                  {s}
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Scholarships */}
        {uni.scholarships?.length > 0 && (
          <div className="card">
            <h2 className="font-semibold text-gray-900 mb-4">Scholarships at {uni.name}</h2>
            <div className="space-y-2">
              {uni.scholarships.map((s: any) => (
                <div key={s.id} className="p-3 bg-amber-50 rounded-xl">
                  <p className="text-sm font-medium text-gray-800">{s.name}</p>
                  {s.amount_description && <p className="text-xs text-amber-700 mt-0.5">{s.amount_description}</p>}
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
