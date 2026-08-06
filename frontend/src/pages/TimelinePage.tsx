import { useState, useMemo } from 'react'
import { useMutation } from '@tanstack/react-query'
import { agentApi } from '@/lib/api'
import { Calendar, CheckCircle, AlertCircle, Clock, Loader2, Zap, Sparkles, Filter, CheckCircle2, Flag, FileText, Landmark, Plane } from 'lucide-react'
import { motion } from 'framer-motion'
import toast from 'react-hot-toast'
import clsx from 'clsx'

interface MilestoneItem {
  id: string
  milestone: string
  phase: string
  timeframe: string
  description: string
  priority: 'critical' | 'high' | 'medium'
  category: 'test_prep' | 'documents' | 'applications' | 'scholarships' | 'visa' | 'travel'
  countrySpecific?: string
}

const INTAKES = [
  { label: 'Fall 2026 (Sep 2026 Start) — Recommended', value: 'Fall 2026', startYear: 2026, startMonth: 9 },
  { label: 'Spring 2027 (Jan 2027 Start) — Open', value: 'Spring 2027', startYear: 2027, startMonth: 1 },
  { label: 'Spring 2026 (Jan 2026 Start) — Late / Closed', value: 'Spring 2026', startYear: 2026, startMonth: 1 },
  { label: 'Fall 2025 (Sep 2025 Start) — Closed', value: 'Fall 2025', startYear: 2025, startMonth: 9 },
  { label: 'Spring 2025 (Jan 2025 Start) — Closed', value: 'Spring 2025', startYear: 2025, startMonth: 1 },
]

const COUNTRIES = ['Germany', 'USA', 'UK', 'Canada', 'Australia', 'Ireland']
const DEGREES = ["Master's / MSc", "Bachelor's / BSc", 'MBA', 'PhD / Doctorate']

/** Calculate dynamic month-by-month calendar labels based on target intake */
function getIntakeTimeline(
  targetIntake: string,
  country: string,
  degree: string,
  hasIELTS: boolean,
  hasGRE: boolean,
  hasSOP: boolean
): MilestoneItem[] {
  const isFall = targetIntake.includes('Fall')
  const year = targetIntake.includes('2026') ? 2026 : 2025

  const m1 = isFall ? `Aug – Oct ${year - 1}` : `May – Jun ${year - 1}`
  const m2 = isFall ? `Nov – Dec ${year - 1}` : `Jul – Aug ${year - 1}`
  const m3 = isFall ? `Jan – Mar ${year}` : `Sep – Oct ${year - 1}`
  const m4 = isFall ? `Apr – May ${year}` : `Nov ${year - 1}`
  const m5 = isFall ? `Jun – Jul ${year}` : `Dec ${year - 1}`
  const m6 = isFall ? `Aug ${year}` : `Jan ${year}`

  const baseMilestones: MilestoneItem[] = [
    // Phase 1: Preparation & Exams
    {
      id: 'm1',
      milestone: 'IELTS / TOEFL Language Exam Preparation',
      phase: '1. Test Preparation & Profile Building',
      timeframe: m1,
      description: hasIELTS ? 'Completed! Language test requirement fulfilled.' : 'Enroll in IELTS/TOEFL coaching. Target Band 7.0+ for top universities.',
      priority: 'critical',
      category: 'test_prep',
    },
    {
      id: 'm2',
      milestone: 'GRE / GMAT Standardized Exam (If Applicable)',
      phase: '1. Test Preparation & Profile Building',
      timeframe: m1,
      description: hasGRE ? 'Completed! GRE score ready for submission.' : country === 'USA' ? 'Required for top US CS/STEM programs. Target score 315+.' : 'Optional for Germany/UK public programs unless specified by department.',
      priority: country === 'USA' ? 'critical' : 'medium',
      category: 'test_prep',
    },

    // Phase 2: Documents & Shortlisting
    {
      id: 'm3',
      milestone: 'SOP Drafting & Recommendation Letters (LORs)',
      phase: '2. Document Preparation & Shortlisting',
      timeframe: m2,
      description: hasSOP ? 'SOP & LORs ready for upload.' : 'Draft custom Statement of Purpose (SOP) & secure 2-3 academic/professional LORs.',
      priority: 'critical',
      category: 'documents',
    },
    {
      id: 'm4',
      milestone: country === 'Germany' ? 'APS Certificate & Uni-Assist Evaluation' : country === 'USA' ? 'WES Transcript Evaluation' : 'Academic Transcripts & Degree Certificate Verification',
      phase: '2. Document Preparation & Shortlisting',
      timeframe: m2,
      description: country === 'Germany' ? 'Mandatory APS India certificate verification & Uni-Assist portal document submission.' : 'Verify official university marksheets, backlog certificates, and degree transcripts.',
      priority: 'critical',
      category: 'documents',
      countrySpecific: country,
    },

    // Phase 3: Applications & Scholarships
    {
      id: 'm5',
      milestone: `Submit ${country} University Applications`,
      phase: '3. Application Submission & Scholarships',
      timeframe: m3,
      description: `Submit online applications for chosen ${degree} programs in ${country} before priority deadlines.`,
      priority: 'critical',
      category: 'applications',
    },
    {
      id: 'm6',
      milestone: country === 'Germany' ? 'DAAD & Deutschlandstipendium Applications' : country === 'UK' ? 'Chevening & Commonwealth Scholarships' : country === 'USA' ? 'Fulbright & Yale/Stanford Grants' : 'Matched Government & Merit Scholarships',
      phase: '3. Application Submission & Scholarships',
      timeframe: m3,
      description: `Apply for matched scholarships for ${country} to reduce overall tuition & living costs.`,
      priority: 'high',
      category: 'scholarships',
    },

    // Phase 4: Admission & Financials
    {
      id: 'm7',
      milestone: 'Admission Offer Acceptance & Deposit Payment',
      phase: '4. Admission Offer & Financial Proof',
      timeframe: m4,
      description: 'Review offer letters, accept target university offer, and pay confirmation deposit.',
      priority: 'critical',
      category: 'applications',
    },
    {
      id: 'm8',
      milestone: country === 'Germany' ? 'Open Blocked Account (Sperrkonto €11,208)' : country === 'Canada' ? 'Open GIC Account ($20,635 CAD)' : country === 'UK' ? 'CAS Statement & Financial Proof' : country === 'USA' ? 'I-20 Form Issuance & Bank Balance Certificate' : 'Proof of Funds & Financial Solvency',
      phase: '4. Admission Offer & Financial Proof',
      timeframe: m4,
      description: country === 'Germany' ? 'Open German Blocked Account (Fintiba/Expatrio) & deposit mandatory €11,208 living funds.' : 'Arrange bank balance statement, education loan approval, or GIC for visa filing.',
      priority: 'critical',
      category: 'visa',
      countrySpecific: country,
    },

    // Phase 5: Student Visa
    {
      id: 'm9',
      milestone: `${country} Student Visa Application & Interview`,
      phase: '5. Student Visa & Insurance',
      timeframe: m5,
      description: `Book visa appointment at VFS / Embassy, complete biometric scan & attend student visa interview for ${country}.`,
      priority: 'critical',
      category: 'visa',
    },

    // Phase 6: Pre-Departure
    {
      id: 'm10',
      milestone: 'Flights, Student Housing & Forex Card',
      phase: '6. Pre-Departure & Travel',
      timeframe: m6,
      description: 'Book student flight tickets, finalize university housing/apartment, get international student SIM & Forex card.',
      priority: 'high',
      category: 'travel',
    },
  ]

  return baseMilestones
}

export default function TimelinePage() {
  // User Inputs for Personalized Timeline
  const [targetIntake, setTargetIntake] = useState('Fall 2026')
  const [selectedCountry, setSelectedCountry] = useState('Germany')
  const [selectedDegree, setSelectedDegree] = useState("Master's / MSc")

  // Current Prep Status
  const [hasIELTS, setHasIELTS] = useState(false)
  const [hasGRE, setHasGRE] = useState(false)
  const [hasSOP, setHasSOP] = useState(false)

  // Completed Milestones tracking
  const [completedIds, setCompletedIds] = useState<string[]>([])

  // Calculate dynamic user-tailored timeline
  const activeTimeline = useMemo(() => {
    return getIntakeTimeline(targetIntake, selectedCountry, selectedDegree, hasIELTS, hasGRE, hasSOP)
  }, [targetIntake, selectedCountry, selectedDegree, hasIELTS, hasGRE, hasSOP])

  const mutation = useMutation({
    mutationFn: () => agentApi.run({
      query: `Generate my personalised application timeline for ${selectedDegree} in ${selectedCountry} starting ${targetIntake}`
    }),
    onSuccess: (res) => {
      const msg = res.data?.result?.message || 'AI Custom Timeline Generated!'
      toast.success(msg)
    },
    onError: () => toast.error('Could not run AI agent. Using user-configured roadmap.'),
  })

  const toggleComplete = (id: string) => {
    setCompletedIds((prev) => (prev.includes(id) ? prev.filter((x) => x !== id) : [...prev, id]))
  }

  // Group by Phase
  const groupedPhases = useMemo(() => {
    return activeTimeline.reduce<Record<string, MilestoneItem[]>>((acc, item) => {
      if (!acc[item.phase]) acc[item.phase] = []
      acc[item.phase].push(item)
      return acc
    }, {})
  }, [activeTimeline])

  const progressPercent = Math.round((completedIds.length / activeTimeline.length) * 100)

  return (
    <div className="max-w-4xl space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 flex items-center gap-2">
            <Calendar className="w-6 h-6 text-brand-500" /> User-Personalized Application Timeline
          </h1>
          <p className="text-gray-500 text-sm">Custom month-by-month study abroad roadmap tailored to your intake, country, & progress</p>
        </div>

        <button
          onClick={() => mutation.mutate()}
          disabled={mutation.isPending}
          className="btn-primary inline-flex items-center gap-2 shadow-sm text-sm"
        >
          {mutation.isPending ? <Loader2 className="w-4 h-4 animate-spin" /> : <Zap className="w-4 h-4 text-amber-300" />}
          Generate AI Custom Roadmap
        </button>
      </div>

      {/* User Controls Panel */}
      <div className="card space-y-4 bg-gradient-to-br from-white to-brand-50/20 border-brand-100">
        <h2 className="font-semibold text-gray-900 text-sm flex items-center gap-2 border-b border-gray-100 pb-3">
          <Filter className="w-4 h-4 text-brand-500" /> Personalise Your Roadmap Settings
        </h2>

        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          {/* Target Intake */}
          <div>
            <label className="label">Target Start Term / Intake</label>
            <select
              value={targetIntake}
              onChange={(e) => setTargetIntake(e.target.value)}
              className="input text-xs"
            >
              {INTAKES.map((i) => (
                <option key={i.value} value={i.value}>{i.label}</option>
              ))}
            </select>
          </div>

          {/* Destination Country */}
          <div>
            <label className="label">Destination Country</label>
            <select
              value={selectedCountry}
              onChange={(e) => setSelectedCountry(e.target.value)}
              className="input text-xs"
            >
              {COUNTRIES.map((c) => (
                <option key={c} value={c}>{c}</option>
              ))}
            </select>
          </div>

          {/* Degree Level */}
          <div>
            <label className="label">Degree Level</label>
            <select
              value={selectedDegree}
              onChange={(e) => setSelectedDegree(e.target.value)}
              className="input text-xs"
            >
              {DEGREES.map((d) => (
                <option key={d} value={d}>{d}</option>
              ))}
            </select>
          </div>
        </div>

        {/* Status Checkboxes */}
        <div className="pt-2 border-t border-gray-100">
          <label className="label mb-2">Current Preparation Status</label>
          <div className="flex flex-wrap gap-4 text-xs">
            <label className="flex items-center gap-2 cursor-pointer text-gray-700">
              <input
                type="checkbox"
                checked={hasIELTS}
                onChange={(e) => setHasIELTS(e.target.checked)}
                className="rounded text-brand-500 accent-brand-500 w-4 h-4"
              />
              <span>IELTS/TOEFL Passed</span>
            </label>

            <label className="flex items-center gap-2 cursor-pointer text-gray-700">
              <input
                type="checkbox"
                checked={hasGRE}
                onChange={(e) => setHasGRE(e.target.checked)}
                className="rounded text-brand-500 accent-brand-500 w-4 h-4"
              />
              <span>GRE/GMAT Passed / Waived</span>
            </label>

            <label className="flex items-center gap-2 cursor-pointer text-gray-700">
              <input
                type="checkbox"
                checked={hasSOP}
                onChange={(e) => setHasSOP(e.target.checked)}
                className="rounded text-brand-500 accent-brand-500 w-4 h-4"
              />
              <span>SOP & LORs Ready</span>
            </label>
          </div>
        </div>
      </div>

      {/* Past Intake Warning Banner */}
      {(targetIntake.includes('2025') || targetIntake.includes('Spring 2026') || targetIntake.includes('Summer 2026')) && (
        <div className="p-4 bg-amber-50 border border-amber-200 rounded-xl flex items-start gap-3 text-amber-800 text-sm shadow-sm">
          <AlertCircle className="w-5 h-5 text-amber-600 flex-shrink-0 mt-0.5" />
          <div>
            <p className="font-semibold text-amber-900">⏰ You are late to apply for {targetIntake}!</p>
            <p className="text-xs text-amber-700 mt-0.5">
              The intake term you selected ({targetIntake}) has already closed or passed prior to August 2026. Please select <strong>Fall 2026 (Sep 2026)</strong> or <strong>Spring 2027 (Jan 2027)</strong> for active open application windows.
            </p>
          </div>
        </div>
      )}

      {/* Progress Bar */}
      <div className="card">
        <div className="flex items-center justify-between mb-2">
          <span className="text-sm font-semibold text-gray-800">Your Journey Progress</span>
          <span className="text-sm font-bold text-brand-600">{progressPercent}%</span>
        </div>
        <div className="w-full bg-gray-100 rounded-full h-3">
          <motion.div
            className="gradient-bg h-3 rounded-full"
            initial={{ width: 0 }}
            animate={{ width: `${progressPercent}%` }}
            transition={{ duration: 0.4 }}
          />
        </div>
        <p className="text-xs text-gray-400 mt-2">
          {completedIds.length} of {activeTimeline.length} milestones completed for {selectedDegree} ({selectedCountry} – {targetIntake})
        </p>
      </div>

      {/* Timeline Phases & Milestones */}
      <div className="space-y-6">
        {Object.entries(groupedPhases).map(([phaseTitle, items]) => (
          <div key={phaseTitle} className="space-y-3">
            <h2 className="text-sm font-bold text-brand-600 uppercase tracking-wider flex items-center gap-2">
              <Sparkles className="w-4 h-4 text-amber-500" /> {phaseTitle}
            </h2>

            <div className="space-y-3">
              {items.map((item) => {
                const isDone = completedIds.includes(item.id)
                return (
                  <motion.div
                    key={item.id}
                    initial={{ opacity: 0, y: 8 }}
                    animate={{ opacity: 1, y: 0 }}
                    onClick={() => toggleComplete(item.id)}
                    className={clsx(
                      'card !p-4 cursor-pointer transition-all border-l-4 hover:shadow-md',
                      isDone
                        ? 'border-l-green-500 bg-green-50/50 opacity-80'
                        : item.priority === 'critical'
                        ? 'border-l-red-500'
                        : item.priority === 'high'
                        ? 'border-l-amber-500'
                        : 'border-l-blue-500'
                    )}
                  >
                    <div className="flex items-start gap-3">
                      <div className={`mt-0.5 shrink-0 ${isDone ? 'text-green-600' : 'text-gray-400'}`}>
                        {isDone ? <CheckCircle2 className="w-5 h-5 text-green-600" /> : <Clock className="w-5 h-5" />}
                      </div>

                      <div className="flex-1 space-y-1">
                        <div className="flex items-center justify-between flex-wrap gap-2">
                          <h3 className={clsx('font-bold text-sm', isDone ? 'line-through text-gray-400' : 'text-gray-900')}>
                            {item.milestone}
                          </h3>

                          <div className="flex items-center gap-2">
                            <span className="text-xs font-semibold px-2 py-0.5 rounded-full bg-brand-50 text-brand-600 border border-brand-100">
                              {item.timeframe}
                            </span>
                            <span className={clsx('text-[11px] font-semibold px-2 py-0.5 rounded-full uppercase', {
                              'bg-red-50 text-red-700 border border-red-100': item.priority === 'critical',
                              'bg-amber-50 text-amber-700 border border-amber-100': item.priority === 'high',
                              'bg-blue-50 text-blue-700 border border-blue-100': item.priority === 'medium',
                            })}>
                              {item.priority}
                            </span>
                          </div>
                        </div>

                        <p className="text-xs text-gray-600 leading-relaxed">{item.description}</p>

                        {item.countrySpecific && (
                          <span className="inline-block text-[11px] font-medium text-purple-700 bg-purple-50 px-2 py-0.5 rounded border border-purple-100 mt-1">
                            📍 Specific to {item.countrySpecific}
                          </span>
                        )}
                      </div>
                    </div>
                  </motion.div>
                )
              })}
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
