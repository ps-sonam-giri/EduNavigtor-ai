import { useQuery } from '@tanstack/react-query'
import { universityApi } from '@/lib/api'
import { Award, ExternalLink, DollarSign, Globe, BookOpen } from 'lucide-react'
import { motion } from 'framer-motion'

const TYPE_COLORS: Record<string, string> = {
  full_tuition:    'badge-green',
  partial_tuition: 'badge-blue',
  living_stipend:  'badge-purple',
  merit:           'badge-orange',
  need_based:      'badge-red',
}

export default function ScholarshipsPage() {
  const { data: scholarships = [], isLoading } = useQuery({
    queryKey: ['scholarships'],
    queryFn: () => universityApi.scholarships({ limit: 50 }).then((r) => r.data),
  })

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Scholarships</h1>
        <p className="text-gray-500 text-sm">Curated scholarship opportunities for Indian students</p>
      </div>

      {isLoading ? (
        <div className="flex items-center justify-center h-40">
          <div className="animate-spin w-8 h-8 border-2 border-brand-500 border-t-transparent rounded-full" />
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
          {scholarships.map((s: any, i: number) => (
            <motion.div
              key={s.id}
              initial={{ opacity: 0, y: 15 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.05 }}
              className="card hover:shadow-md transition-all"
            >
              <div className="flex items-start justify-between mb-3">
                <div className="flex-1">
                  <span className={`badge ${TYPE_COLORS[s.scholarship_type] || 'badge-blue'} mb-2`}>
                    {s.scholarship_type.replace('_', ' ')}
                  </span>
                  <h3 className="font-semibold text-gray-900">{s.name}</h3>
                  <p className="text-sm text-gray-500 mt-0.5">by {s.provider}</p>
                </div>
                <div className="w-10 h-10 rounded-xl bg-amber-100 flex items-center justify-center flex-shrink-0 ml-3">
                  <Award className="w-5 h-5 text-amber-600" />
                </div>
              </div>

              {s.amount_description && (
                <div className="flex items-center gap-2 text-green-700 font-medium text-sm mb-3">
                  <DollarSign className="w-4 h-4" />
                  {s.amount_description}
                </div>
              )}

              {s.description && (
                <p className="text-sm text-gray-600 leading-relaxed mb-3 line-clamp-2">{s.description}</p>
              )}

              <div className="flex flex-wrap gap-3 text-xs text-gray-500">
                {s.eligible_countries?.slice(0, 3).map((c: string) => (
                  <span key={c} className="flex items-center gap-1">
                    <Globe className="w-3 h-3" /> {c}
                  </span>
                ))}
                {s.min_cgpa && (
                  <span className="flex items-center gap-1">
                    <BookOpen className="w-3 h-3" /> Min CGPA: {s.min_cgpa}
                  </span>
                )}
              </div>

              {s.application_url && (
                <a
                  href={s.application_url}
                  target="_blank"
                  rel="noreferrer"
                  className="mt-4 flex items-center gap-1.5 text-brand-500 text-sm font-medium hover:underline"
                >
                  Apply Now <ExternalLink className="w-3.5 h-3.5" />
                </a>
              )}
            </motion.div>
          ))}
        </div>
      )}
    </div>
  )
}
