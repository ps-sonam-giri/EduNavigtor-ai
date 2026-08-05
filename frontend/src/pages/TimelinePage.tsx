import { useState } from 'react'
import { useMutation } from '@tanstack/react-query'
import { agentApi } from '@/lib/api'
import { Calendar, CheckCircle, AlertCircle, Clock, Loader2, Zap } from 'lucide-react'
import { motion } from 'framer-motion'
import toast from 'react-hot-toast'
import clsx from 'clsx'

const PRIORITY_STYLES: Record<string, string> = {
  critical: 'border-l-red-500 bg-red-50',
  high:     'border-l-orange-500 bg-orange-50',
  medium:   'border-l-blue-500 bg-blue-50',
  low:      'border-l-gray-300 bg-gray-50',
}

const CATEGORY_ICONS: Record<string, typeof CheckCircle> = {
  test_prep:    Clock,
  documents:    CheckCircle,
  applications: Zap,
  scholarships: AlertCircle,
  visa:         AlertCircle,
  decision:     CheckCircle,
  travel:       Calendar,
}

const SAMPLE_TIMELINE = [
  { month_offset: 0, milestone: 'IELTS Enrollment', phase: 'Test Preparation', description: 'Enroll in IELTS coaching. Target band 7.0+.', priority: 'critical', category: 'test_prep' },
  { month_offset: 2, milestone: 'GRE Preparation', phase: 'Test Preparation', description: 'Begin GRE preparation if applying to US/Canada programs. Target 310+.', priority: 'high', category: 'test_prep' },
  { month_offset: 3, milestone: 'SOP & LOR Drafting', phase: 'Document Preparation', description: 'Draft Statement of Purpose and request 3 Letters of Recommendation.', priority: 'critical', category: 'documents' },
  { month_offset: 4, milestone: 'University Applications', phase: 'Application', description: 'Submit applications to shortlisted universities.', priority: 'critical', category: 'applications' },
  { month_offset: 5, milestone: 'Scholarship Applications', phase: 'Scholarship', description: 'Apply for Chevening, Commonwealth, and other matched scholarships.', priority: 'high', category: 'scholarships' },
  { month_offset: 7, milestone: 'Offer Letter Decision', phase: 'Decision', description: 'Evaluate offer letters and compare financial aid packages.', priority: 'critical', category: 'decision' },
  { month_offset: 8, milestone: 'Student Visa Application', phase: 'Visa', description: 'Gather all visa documents and submit student visa application.', priority: 'critical', category: 'visa' },
  { month_offset: 10, milestone: 'Pre-Departure Prep', phase: 'Travel', description: 'Book flights, arrange accommodation, open bank account, get forex card.', priority: 'medium', category: 'travel' },
]

export default function TimelinePage() {
  const [timeline, setTimeline] = useState(SAMPLE_TIMELINE)
  const [completed, setCompleted] = useState<number[]>([])

  const mutation = useMutation({
    mutationFn: () => agentApi.run({ query: 'Generate my personalised application timeline based on my profile' }),
    onSuccess: (res) => {
      const tl = res.data?.result?.application_timeline
      if (tl && tl.length > 0) {
        setTimeline(tl)
        toast.success('Timeline generated from your profile!')
      } else {
        toast('Using standard timeline template')
      }
    },
    onError: () => toast.error('Could not generate personalised timeline. Showing template.'),
  })

  const toggleComplete = (i: number) => {
    setCompleted((prev) => prev.includes(i) ? prev.filter((x) => x !== i) : [...prev, i])
  }

  const grouped = timeline.reduce<Record<string, typeof SAMPLE_TIMELINE>>((acc, item) => {
    const phase = item.phase || 'Other'
    if (!acc[phase]) acc[phase] = []
    acc[phase].push(item)
    return acc
  }, {})

  const progress = Math.round((completed.length / timeline.length) * 100)

  return (
    <div className="max-w-3xl space-y-6">
      <div className="flex items-start justify-between flex-wrap gap-4">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Application Timeline</h1>
          <p className="text-gray-500 text-sm">Your personalised study abroad roadmap</p>
        </div>
        <button
          onClick={() => mutation.mutate()}
          disabled={mutation.isPending}
          className="btn-primary flex items-center gap-2"
        >
          {mutation.isPending ? <Loader2 className="w-4 h-4 animate-spin" /> : <Zap className="w-4 h-4" />}
          Generate AI Timeline
        </button>
      </div>

      {/* Progress */}
      <div className="card">
        <div className="flex items-center justify-between mb-3">
          <span className="text-sm font-medium text-gray-700">Overall Progress</span>
          <span className="text-sm font-bold text-brand-500">{progress}%</span>
        </div>
        <div className="w-full bg-gray-100 rounded-full h-3">
          <motion.div
            className="gradient-bg h-3 rounded-full"
            initial={{ width: 0 }}
            animate={{ width: `${progress}%` }}
            transition={{ duration: 0.5 }}
          />
        </div>
        <p className="text-xs text-gray-400 mt-2">{completed.length} of {timeline.length} milestones completed</p>
      </div>

      {/* Timeline phases */}
      {Object.entries(grouped).map(([phase, items]) => (
        <div key={phase}>
          <h2 className="text-sm font-semibold text-gray-500 uppercase tracking-wide mb-3">{phase}</h2>
          <div className="space-y-3">
            {items.map((item, idx) => {
              const globalIdx = timeline.indexOf(item)
              const done = completed.includes(globalIdx)
              const Icon = CATEGORY_ICONS[item.category] || Calendar

              return (
                <motion.div
                  key={globalIdx}
                  initial={{ opacity: 0, x: -10 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: idx * 0.05 }}
                  className={clsx(
                    'border-l-4 pl-4 py-3 pr-4 rounded-r-xl cursor-pointer transition-all',
                    done ? 'border-l-green-500 bg-green-50 opacity-70' : PRIORITY_STYLES[item.priority] || 'border-l-gray-300 bg-gray-50'
                  )}
                  onClick={() => toggleComplete(globalIdx)}
                >
                  <div className="flex items-start gap-3">
                    <div className={`mt-0.5 flex-shrink-0 ${done ? 'text-green-500' : 'text-gray-400'}`}>
                      {done
                        ? <CheckCircle className="w-5 h-5" />
                        : <Icon className="w-5 h-5" />}
                    </div>
                    <div className="flex-1">
                      <div className="flex items-center gap-2 flex-wrap">
                        <h3 className={`font-semibold ${done ? 'line-through text-gray-400' : 'text-gray-900'}`}>
                          {item.milestone}
                        </h3>
                        <span className={clsx('badge text-xs', {
                          'bg-red-100 text-red-700': item.priority === 'critical',
                          'bg-orange-100 text-orange-700': item.priority === 'high',
                          'bg-blue-100 text-blue-700': item.priority === 'medium',
                        })}>
                          {item.priority}
                        </span>
                        <span className="text-xs text-gray-400">Month {item.month_offset + 1}</span>
                      </div>
                      <p className="text-sm text-gray-600 mt-1">{item.description}</p>
                    </div>
                  </div>
                </motion.div>
              )
            })}
          </div>
        </div>
      ))}
    </div>
  )
}
