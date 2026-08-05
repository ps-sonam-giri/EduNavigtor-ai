import { useQuery } from '@tanstack/react-query'
import { Link } from 'react-router-dom'
import { profileApi, agentApi } from '@/lib/api'
import { motion } from 'framer-motion'
import {
  GraduationCap, Award, Calculator, Calendar,
  MessageSquare, FileText, ArrowRight, Zap,
  TrendingUp, Globe, CheckCircle, AlertCircle
} from 'lucide-react'

const cards = [
  { to: '/chat',         icon: MessageSquare, label: 'AI Copilot',     color: 'from-purple-500 to-indigo-600',  desc: 'Chat with your AI study advisor' },
  { to: '/universities', icon: GraduationCap, label: 'Universities',   color: 'from-blue-500 to-cyan-600',      desc: 'Browse & discover universities' },
  { to: '/scholarships', icon: Award,         label: 'Scholarships',   color: 'from-amber-500 to-orange-600',   desc: 'Find funding opportunities' },
  { to: '/budget',       icon: Calculator,    label: 'Budget Planner', color: 'from-green-500 to-teal-600',     desc: 'Plan your finances' },
  { to: '/timeline',     icon: Calendar,      label: 'Timeline',       color: 'from-rose-500 to-pink-600',      desc: 'Your application roadmap' },
  { to: '/reports',      icon: FileText,      label: 'Reports',        color: 'from-violet-500 to-purple-600',  desc: 'Download full AI reports' },
]

export default function DashboardPage() {
  const { data: profile } = useQuery({
    queryKey: ['profile'],
    queryFn: () => profileApi.get().then((r) => r.data),
    retry: false,
  })

  const { data: logs } = useQuery({
    queryKey: ['agent-logs'],
    queryFn: () => agentApi.getLogs().then((r) => r.data),
    retry: false,
  })

  const profileComplete = profile?.cgpa && profile?.course_interest && profile?.total_budget_usd

  return (
    <div className="space-y-8">
      {/* Hero */}
      <motion.div
        initial={{ opacity: 0, y: -10 }}
        animate={{ opacity: 1, y: 0 }}
        className="gradient-bg rounded-2xl p-8 text-white"
      >
        <div className="flex items-start justify-between">
          <div>
            <p className="text-white/70 text-sm mb-1">Welcome to</p>
            <h1 className="text-3xl font-bold mb-2">EduPilot AI 🎓</h1>
            <p className="text-white/80">
              {profileComplete
                ? 'Your profile is complete. Start the AI Copilot for your full recommendation.'
                : 'Set up your profile to get personalised study abroad recommendations.'}
            </p>
          </div>
          <GraduationCap className="hidden md:block w-16 h-16 text-white/30" />
        </div>
        <div className="flex gap-3 mt-6">
          <Link to="/chat" className="bg-white text-brand-500 px-5 py-2.5 rounded-xl font-semibold text-sm flex items-center gap-2 hover:bg-white/90 transition-colors">
            <Zap className="w-4 h-4" /> Start AI Planning
          </Link>
          {!profileComplete && (
            <Link to="/profile" className="bg-white/20 text-white px-5 py-2.5 rounded-xl font-semibold text-sm flex items-center gap-2 hover:bg-white/30 transition-colors">
              Set up Profile <ArrowRight className="w-4 h-4" />
            </Link>
          )}
        </div>
      </motion.div>

      {/* Profile missing banner */}
      {!profileComplete && (
        <div className="bg-amber-50 border border-amber-200 rounded-2xl p-5 flex items-start gap-4">
          <AlertCircle className="w-6 h-6 text-amber-500 flex-shrink-0 mt-0.5" />
          <div className="flex-1">
            <h3 className="font-semibold text-amber-800 mb-1">Profile Incomplete</h3>
            <p className="text-amber-700 text-sm">Add your CGPA, course interest, and budget to unlock personalised AI recommendations.</p>
          </div>
          <Link to="/profile" className="text-amber-600 hover:text-amber-800 text-sm font-semibold whitespace-nowrap flex items-center gap-1">
            Set up <ArrowRight className="w-3 h-3" />
          </Link>
        </div>
      )}

      {/* Stats */}
      {profile && (
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {[
            { label: 'CGPA', value: profile.cgpa ? `${profile.cgpa} / ${profile.cgpa_scale}` : '—', icon: TrendingUp, color: 'text-blue-500' },
            { label: 'IELTS Score', value: profile.ielts_score || '—', icon: CheckCircle, color: 'text-green-500' },
            { label: 'Budget (USD)', value: profile.total_budget_usd ? `$${Number(profile.total_budget_usd).toLocaleString()}` : '—', icon: Calculator, color: 'text-purple-500' },
            { label: 'Countries', value: profile.preferred_countries?.length || 0, icon: Globe, color: 'text-orange-500' },
          ].map(({ label, value, icon: Icon, color }) => (
            <div key={label} className="card flex items-center gap-4">
              <div className={`w-10 h-10 rounded-xl bg-gray-50 flex items-center justify-center ${color}`}>
                <Icon className="w-5 h-5" />
              </div>
              <div>
                <p className="text-xs text-gray-500">{label}</p>
                <p className="font-bold text-gray-900">{String(value)}</p>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Feature cards */}
      <div>
        <h2 className="text-xl font-bold text-gray-900 mb-4">What would you like to do?</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {cards.map(({ to, icon: Icon, label, color, desc }, i) => (
            <motion.div
              key={to}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.05 }}
            >
              <Link to={to} className="card hover:shadow-md transition-all duration-200 flex items-start gap-4 group hover:-translate-y-0.5">
                <div className={`w-12 h-12 rounded-xl bg-gradient-to-br ${color} flex items-center justify-center flex-shrink-0`}>
                  <Icon className="w-6 h-6 text-white" />
                </div>
                <div className="flex-1 min-w-0">
                  <h3 className="font-semibold text-gray-900 group-hover:text-brand-500 transition-colors">{label}</h3>
                  <p className="text-gray-500 text-sm mt-0.5">{desc}</p>
                </div>
                <ArrowRight className="w-4 h-4 text-gray-300 group-hover:text-brand-500 transition-colors mt-1 flex-shrink-0" />
              </Link>
            </motion.div>
          ))}
        </div>
      </div>

      {/* Recent activity */}
      {logs && logs.length > 0 && (
        <div>
          <h2 className="text-xl font-bold text-gray-900 mb-4">Recent AI Activity</h2>
          <div className="card divide-y divide-gray-100">
            {logs.slice(0, 5).map((log: any) => (
              <div key={log.id} className="flex items-center gap-4 py-3 first:pt-0 last:pb-0">
                <div className={`w-2 h-2 rounded-full ${log.status === 'success' ? 'bg-green-500' : 'bg-red-400'}`} />
                <div className="flex-1">
                  <p className="text-sm font-medium text-gray-800 capitalize">{log.agent_name.replace('_', ' ')}</p>
                  <p className="text-xs text-gray-500">Session {log.session_id.slice(-8)}</p>
                </div>
                <span className={`badge ${log.status === 'success' ? 'badge-green' : 'badge-red'}`}>{log.status}</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
