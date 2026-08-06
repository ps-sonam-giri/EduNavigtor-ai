import { useParams, Link } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { universityApi } from '@/lib/api'
import { ArrowLeft, Globe, MapPin, TrendingUp, Award, DollarSign, Calendar, CheckCircle, ShieldCheck, CheckCircle2, Building2, BookOpen } from 'lucide-react'
import { motion } from 'framer-motion'

const DEFAULT_MEDIA: Record<string, { image: string; flag: string; offered: string[]; accepted: string[] }> = {
  'Technical University of Munich': {
    image: 'https://images.unsplash.com/photo-1592285850226-4579458e8996?auto=format&fit=crop&w=1200&q=80',
    flag: '🇩🇪',
    offered: ['TUM Dean’s Excellence Grant (€1,500/semester)', 'TUM Merit Tuition Waiver', 'Graduate Research Assistantship (HiWi)'],
    accepted: ['DAAD EPOS Postgraduate Scholarship', 'Deutschlandstipendium (€300/mo)', 'Heinrich Böll Foundation Grant', 'National Overseas Scholarship (NOS India)'],
  },
  'LMU Munich': {
    image: 'https://images.unsplash.com/photo-1541339907198-e08756dedf3f?auto=format&fit=crop&w=1200&q=80',
    flag: '🇩🇪',
    offered: ['LMU Merit Entrance Award', 'International Student Emergency Grant'],
    accepted: ['DAAD Scholarship', 'Deutschlandstipendium', 'Konrad-Adenauer-Stiftung Grant', 'JN Tata Endowment Loan'],
  },
  'RWTH Aachen University': {
    image: 'https://images.unsplash.com/photo-1562774053-701939374585?auto=format&fit=crop&w=1200&q=80',
    flag: '🇩🇪',
    offered: ['RWTH Aachen Excellence Stipend', 'Research Assistantship (HiWi)'],
    accepted: ['DAAD EPOS Scholarship', 'Deutschlandstipendium', 'National Overseas Scholarship (NOS)'],
  },
  'Massachusetts Institute of Technology': {
    image: 'https://images.unsplash.com/photo-1564981797816-1043664bf78d?auto=format&fit=crop&w=1200&q=80',
    flag: '🇺🇸',
    offered: ['MIT Graduate Fellowship (Full Tuition + $40,000/yr Stipend)', 'Research Assistantship (RA)', 'Teaching Assistantship (TA)'],
    accepted: ['Fulbright Foreign Student Program', 'AAUW International Fellowship', 'JN Tata Endowment', 'Inlaks Shivdasani Foundation'],
  },
  'Stanford University': {
    image: 'https://images.unsplash.com/photo-1580582932707-520aed937b7b?auto=format&fit=crop&w=1200&q=80',
    flag: '🇺🇸',
    offered: ['Knight-Hennessy Scholars (Full Tuition + Living Allowance)', 'Stanford Graduate Fellowship', 'School of Engineering Need Grant'],
    accepted: ['Fulbright Scholarship', 'AAUW Fellowship', 'Inlaks Foundation Grant', 'JN Tata Endowment'],
  },
  'Carnegie Mellon University': {
    image: 'https://images.unsplash.com/photo-1498243691581-b145c3f54a5a?auto=format&fit=crop&w=1200&q=80',
    flag: '🇺🇸',
    offered: ['SCS Graduate Merit Fellowship ($15,000)', 'CMU Dean’s Tuition Grant', 'Research Assistantship'],
    accepted: ['Fulbright Foreign Student Grant', 'JN Tata Endowment', 'Aga Khan International Scholarship'],
  },
  'University of Oxford': {
    image: 'https://images.unsplash.com/photo-1534447677768-be436bb09401?auto=format&fit=crop&w=1200&q=80',
    flag: '🇬🇧',
    offered: ['Clarendon Fund Scholarship (Full Tuition + £18,622/yr Grant)', 'Oxford-Weidenfeld and Hoffmann Scholarship'],
    accepted: ['Chevening Master’s Scholarship', 'Commonwealth Scholarship', 'Gates Cambridge', 'Inlaks Shivdasani Foundation'],
  },
  'University of Cambridge': {
    image: 'https://images.unsplash.com/photo-1520986606214-8b456906c813?auto=format&fit=crop&w=1200&q=80',
    flag: '🇬🇧',
    offered: ['Gates Cambridge Scholarship (Full Cost + £20,000/yr)', 'Cambridge Trust International Scholarship'],
    accepted: ['Chevening Scholarship', 'Commonwealth Master’s/PhD', 'JN Tata Endowment', 'Inlaks Foundation'],
  },
  'University of Toronto': {
    image: 'https://images.unsplash.com/photo-1523050854058-8df90110c9f1?auto=format&fit=crop&w=1200&q=80',
    flag: '🇨🇦',
    offered: ['Lester B. Pearson International Scholarship (100% Tuition + Housing)', 'U of T International Scholar Award ($20,000/yr)'],
    accepted: ['Vanier Canada Graduate Scholarship ($50,000/yr)', 'Pierre Elliott Trudeau Doctoral Award', 'National Overseas Scholarship'],
  },
  'University of British Columbia': {
    image: 'https://images.unsplash.com/photo-1509062522246-3755977927d7?auto=format&fit=crop&w=1200&q=80',
    flag: '🇨🇦',
    offered: ['Karen McKellin International Leader of Tomorrow Award', 'UBC Graduate Support Initiative (GSI)'],
    accepted: ['Vanier Canada Graduate Scholarship', 'International Major Entrance Scholarship (IMES)'],
  },
  'University of Melbourne': {
    image: 'https://images.unsplash.com/photo-1541829070764-84a7d30dd3f3?auto=format&fit=crop&w=1200&q=80',
    flag: '🇦🇺',
    offered: ['Melbourne Research Scholarship (100% Tuition + AUD $37,000/yr)', 'Melbourne International Undergraduate Scholarship'],
    accepted: ['Australian Govt Research Training Program (RTP)', 'Australia Awards Scholarship'],
  },
  'Trinity College Dublin': {
    image: 'https://images.unsplash.com/photo-1590012314607-cda9d9b699ae?auto=format&fit=crop&w=1200&q=80',
    flag: '🇮🇪',
    offered: ['Global Excellence Postgraduate Scholarship (€5,000)', 'TCD School of Computer Science Merit Award'],
    accepted: ['Government of Ireland International Education Scholarship (€10,000 + 100% Fee Waiver)', 'JN Tata Endowment'],
  },
}

export default function UniversityDetailPage() {
  const { id } = useParams<{ id: string }>()

  const { data: uni, isLoading } = useQuery({
    queryKey: ['university', id],
    queryFn: () => universityApi.get(id!).then((r) => r.data),
  })

  if (isLoading)
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin w-8 h-8 border-2 border-brand-500 border-t-transparent rounded-full" />
      </div>
    )

  if (!uni) return <div className="text-center text-gray-400 py-12">University not found</div>

  const media = DEFAULT_MEDIA[uni.name] || {
    image: uni.image_url || 'https://images.unsplash.com/photo-1541339907198-e08756dedf3f?auto=format&fit=crop&w=1200&q=80',
    flag: uni.country_flag || '🎓',
    offered: uni.offered_scholarships || ['University Merit Entrance Scholarship', 'Graduate Teaching/Research Assistantship'],
    accepted: uni.accepted_scholarships || ['DAAD EPOS', 'Fulbright Foreign Student Program', 'Chevening Grant', 'National Overseas Scholarship (NOS)'],
  }

  const tuitionVal = Number(uni.avg_tuition_usd_per_year)
  const tuitionDisplay = tuitionVal === 0 ? '$0 / yr (Tuition Free)' : `$${tuitionVal.toLocaleString()} / yr`

  return (
    <div className="max-w-4xl space-y-6">
      <Link to="/universities" className="inline-flex items-center gap-2 text-gray-500 hover:text-brand-500 transition-colors text-sm">
        <ArrowLeft className="w-4 h-4" /> Back to Universities
      </Link>

      {/* Hero Campus Picture Banner */}
      <motion.div initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }} className="card !p-0 overflow-hidden relative shadow-md">
        <div className="relative h-64 sm:h-80 w-full overflow-hidden bg-gray-900">
          <img
            src={uni.image_url || media.image}
            alt={uni.name}
            className="w-full h-full object-cover"
            onError={(e) => {
              ;(e.target as HTMLImageElement).src = 'https://images.unsplash.com/photo-1541339907198-e08756dedf3f?auto=format&fit=crop&w=1200&q=80'
            }}
          />
          <div className="absolute inset-0 bg-gradient-to-t from-black/85 via-black/30 to-transparent" />

          {/* Badges Overlay */}
          <div className="absolute top-4 left-4 right-4 flex items-center justify-between">
            <span className="text-sm px-3 py-1 rounded-full bg-white/90 backdrop-blur-md text-gray-900 font-bold shadow">
              <span>{media.flag}</span> {uni.country}
            </span>
            {uni.qs_world_rank && (
              <span className="text-xs px-3 py-1 rounded-full bg-purple-600/90 backdrop-blur-md text-white font-bold shadow">
                QS World Rank #{uni.qs_world_rank}
              </span>
            )}
          </div>

          {/* Title Banner */}
          <div className="absolute bottom-4 left-4 right-4 text-white">
            <h1 className="text-2xl sm:text-3xl font-extrabold leading-tight drop-shadow-md">{uni.name}</h1>
            <div className="flex items-center gap-4 text-sm text-gray-200 mt-1 flex-wrap">
              <span className="flex items-center gap-1">
                <MapPin className="w-4 h-4 text-amber-400" />
                {uni.location_city ? `${uni.location_city}, ` : ''}{uni.country}
              </span>
              {uni.website && (
                <a href={uni.website} target="_blank" rel="noreferrer" className="flex items-center gap-1 text-amber-300 hover:underline">
                  <Globe className="w-3.5 h-3.5" /> Official Website
                </a>
              )}
            </div>
          </div>
        </div>

        {uni.overview && (
          <div className="p-5 bg-white">
            <p className="text-gray-700 leading-relaxed text-sm">{uni.overview}</p>
          </div>
        )}
      </motion.div>

      {/* Stats Grid */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {[
          { label: 'Tuition Fee / Year', value: tuitionDisplay, icon: DollarSign, color: tuitionVal === 0 ? 'text-emerald-600 font-extrabold' : 'text-green-600' },
          { label: 'Acceptance Rate', value: uni.acceptance_rate ? `${uni.acceptance_rate}%` : 'N/A', icon: TrendingUp, color: 'text-blue-600' },
          { label: 'Min CGPA Required', value: uni.min_cgpa ? `${uni.min_cgpa}/10` : 'N/A', icon: CheckCircle, color: 'text-purple-600' },
          { label: 'Graduate Employment', value: uni.graduate_employment_rate ? `${uni.graduate_employment_rate}%` : 'N/A', icon: Award, color: 'text-amber-600' },
        ].map(({ label, value, icon: Icon, color }) => (
          <div key={label} className="card flex items-center gap-3">
            <Icon className={`w-8 h-8 ${color} shrink-0`} />
            <div>
              <p className="text-xs text-gray-400 font-medium">{label}</p>
              <p className={`text-base font-bold text-gray-900 ${color}`}>{String(value)}</p>
            </div>
          </div>
        ))}
      </div>

      {/* Dedicated Offered & Accepted Scholarships Section */}
      <div className="card space-y-4 border-2 border-amber-200 bg-amber-50/30">
        <div className="flex items-center gap-2 border-b border-amber-200/60 pb-3">
          <Award className="w-6 h-6 text-amber-600" />
          <div>
            <h2 className="text-lg font-bold text-gray-900">Offered & Accepted Scholarships</h2>
            <p className="text-xs text-gray-500">Scholarships provided directly by {uni.name} and external global grants accepted</p>
          </div>
        </div>

        <div className="grid md:grid-cols-2 gap-4">
          {/* Internal University Scholarships */}
          <div className="bg-white p-4 rounded-xl border border-amber-100 space-y-3">
            <h3 className="text-sm font-bold text-amber-900 flex items-center gap-1.5">
              <Building2 className="w-4 h-4 text-amber-600" /> University Offered Grants & Assistantships
            </h3>
            <ul className="space-y-2">
              {media.offered.map((off, idx) => (
                <li key={idx} className="flex items-start gap-2 text-xs text-gray-700">
                  <CheckCircle2 className="w-4 h-4 text-emerald-500 shrink-0 mt-0.5" />
                  <span className="font-medium">{off}</span>
                </li>
              ))}
            </ul>
          </div>

          {/* External & Government Scholarships Accepted */}
          <div className="bg-white p-4 rounded-xl border border-amber-100 space-y-3">
            <h3 className="text-sm font-bold text-blue-900 flex items-center gap-1.5">
              <ShieldCheck className="w-4 h-4 text-blue-600" /> Accepted External & Government Grants
            </h3>
            <ul className="space-y-2">
              {media.accepted.map((acc, idx) => (
                <li key={idx} className="flex items-start gap-2 text-xs text-gray-700">
                  <CheckCircle2 className="w-4 h-4 text-blue-500 shrink-0 mt-0.5" />
                  <span className="font-medium">{acc}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>
      </div>

      <div className="grid md:grid-cols-2 gap-6">
        {/* Admission Requirements */}
        <div className="card">
          <h2 className="font-bold text-gray-900 mb-4 text-base">Admission Criteria</h2>
          <dl className="space-y-2.5 text-sm">
            {[
              ['Min CGPA', uni.min_cgpa ? `${uni.min_cgpa} / 10` : 'Evaluated Case-by-Case'],
              ['Min IELTS', uni.min_ielts ? `Band ${uni.min_ielts}` : 'Waived if medium of instruction was English'],
              ['Min GRE', uni.min_gre ? `${uni.min_gre}` : 'Not Required / Department Specific'],
              ['Application Fee', uni.application_fee_usd ? `$${uni.application_fee_usd}` : 'Free / Waived'],
            ].map(([k, v]) => (
              <div key={String(k)} className="flex justify-between py-1.5 border-b border-gray-50">
                <dt className="text-gray-500">{String(k)}</dt>
                <dd className="font-semibold text-gray-900">{String(v)}</dd>
              </div>
            ))}
          </dl>
        </div>

        {/* Programs */}
        <div className="card">
          <h2 className="font-bold text-gray-900 mb-4 text-base">Popular Programs & Duration</h2>
          <div className="space-y-2.5">
            {uni.programs?.map((p: any) => (
              <div key={p.name} className="flex items-center justify-between py-2 border-b border-gray-50 last:border-0">
                <div>
                  <p className="text-sm font-semibold text-gray-800">{p.name}</p>
                  <p className="text-xs text-gray-400">{p.duration_years} year{p.duration_years !== 1 ? 's' : ''}</p>
                </div>
                {p.tuition_usd !== undefined && (
                  <span className="text-xs font-bold text-emerald-600">
                    {Number(p.tuition_usd) === 0 ? 'Tuition Free' : `$${Number(p.tuition_usd).toLocaleString()}/yr`}
                  </span>
                )}
              </div>
            ))}
          </div>
          <div className="mt-4 flex items-center gap-2 text-xs text-gray-500">
            <Calendar className="w-4 h-4 text-brand-500" />
            Primary Intakes: {uni.intake_months?.join(', ') || 'September / January'}
          </div>
        </div>
      </div>
    </div>
  )
}
