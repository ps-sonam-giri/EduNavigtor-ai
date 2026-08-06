import { useState, useMemo } from 'react'
import { useMutation } from '@tanstack/react-query'
import { agentApi } from '@/lib/api'
import { Calendar, CheckCircle, AlertCircle, Clock, Loader2, Zap, Sparkles, Filter, CheckCircle2, Flag, FileText, Landmark, Plane, BookOpen, ExternalLink, GraduationCap, Award, Download } from 'lucide-react'
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

const EXAM_STUDY_MATERIALS = [
  {
    id: 'ielts',
    name: 'IELTS Academic',
    targetScore: 'Band 7.0 – 8.5',
    description: 'Essential for UK, Australia, Canada, Germany & European Master’s admissions.',
    icon: '🇬🇧',
    sections: [
      { name: 'Listening (40 mins)', tips: 'Practice Cambridge IELTS 14–19 audio tests. Focus on spelling & number dictation.' },
      { name: 'Reading (60 mins)', tips: 'Skim academic articles (The Economist, Scientific American). Practice True/False/Not Given questions.' },
      { name: 'Writing (60 mins)', tips: 'Task 1: Describe graphs/charts using trends vocabulary. Task 2: Band 9 4-paragraph essay template.' },
      { name: 'Speaking (11-14 mins)', tips: 'Practice 2025/2026 cue cards. Record your audio responses for fluency & coherence.' }
    ],
    officialResources: [
      { title: 'British Council Free Practice Tests', url: 'https://takeielts.britishcouncil.org/take-ielts/prepare/free-ielts-practice-tests' },
      { title: 'IDP Official IELTS Sample Questions', url: 'https://www.ieltsidpindia.com/prepare/free-study-material' },
      { title: 'Cambridge IELTS Practice Exam Guide', url: 'https://www.cambridgeenglish.org/exams-and-tests/ielts/' }
    ]
  },
  {
    id: 'gre',
    name: 'GRE General Test',
    targetScore: '315 – 330+',
    description: 'Key requirement for US CS/STEM Master’s and competitive global engineering programs.',
    icon: '📊',
    sections: [
      { name: 'Quantitative Reasoning (170)', tips: 'Master Manhattan Prep 5 lb Book. Focus on Algebra, Geometry & Data Interpretation.' },
      { name: 'Verbal Reasoning (170)', tips: 'Learn 1,000 High-Frequency GRE Magoosh Flashcards. Master Text Completion context clues.' },
      { name: 'Analytical Writing (4.0+)', tips: 'Practice Issue Essay argument structure. Focus on logic, clear examples, and transitional phrases.' }
    ],
    officialResources: [
      { title: 'ETS GRE POWERPREP Official Free Practice', url: 'https://www.ets.org/gre/test-takers/general-test/prepare/powerprep.html' },
      { title: 'Manhattan Prep Free GRE Practice Exam', url: 'https://www.manhattanprep.com/gre/resources/' },
      { title: 'ETS Official GRE Math Review Guide', url: 'https://www.ets.org/gre/test-takers/general-test/prepare/math-review.html' }
    ]
  },
  {
    id: 'toefl',
    name: 'TOEFL iBT',
    targetScore: '95 – 110+',
    description: 'Widely accepted across North America, Europe, and global research universities.',
    icon: '🇺🇸',
    sections: [
      { name: 'Reading & Listening', tips: 'Practice ETS TOEFL iBT Free Practice Test. Build stamina for 2-hour online format.' },
      { name: 'Speaking & Writing', tips: 'Master New Academic Discussion writing task. Practice 45-second timed speaking prompts.' }
    ],
    officialResources: [
      { title: 'ETS TOEFL iBT Official Test Prep', url: 'https://www.ets.org/toefl/test-takers/ibt/prepare/tests.html' },
      { title: 'TOEFL Practice Online GoToPrep', url: 'https://www.toeflgo.org' }
    ]
  },
  {
    id: 'gmat',
    name: 'GMAT Focus Edition',
    targetScore: '645 – 715+',
    description: 'Required for top global MBA and specialized Master in Management (MiM) programs.',
    icon: '💼',
    sections: [
      { name: 'Data Insights (DI)', tips: 'Practice Data Sufficiency & Multi-Source Reasoning in GMAT Official Guide.' },
      { name: 'Quantitative & Verbal', tips: 'Master Critical Reasoning logic trees and speed problem-solving.' }
    ],
    officialResources: [
      { title: 'mba.com Official GMAT Focus Starter Kit', url: 'https://www.mba.com/exam-prep/gmat-official-starter-kit' },
      { title: 'GMAT Club Free Diagnostic Practice Tests', url: 'https://gmatclub.com/tests-gmat-focus/' }
    ]
  },
  {
    id: 'german',
    name: 'Goethe German (A1–B2)',
    targetScore: 'A2 / B1 / B2 Certificate',
    description: 'Essential for English/German taught public university degrees and student visa in Germany.',
    icon: '🇩🇪',
    sections: [
      { name: 'Goethe A1-B2 Vocabulary', tips: 'Complete Deutsche Welle Nicos Weg course. Practice Goethe Institut Model Papers.' }
    ],
    officialResources: [
      { title: 'Goethe-Institut Free Exam Practice', url: 'https://www.goethe.de/en/spr/kup/prf/prf.html' },
      { title: 'Deutsche Welle Free Learn German Course', url: 'https://learngerman.dw.com/en/overview' }
    ]
  }
]

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

  // Active Exam Tab state for Study Materials Hub
  const [activeExamId, setActiveExamId] = useState('ielts')

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

      {/* Exam Preparation & Study Materials Hub */}
      <div className="card space-y-4 border-brand-100 bg-gradient-to-br from-white via-brand-50/10 to-indigo-50/20">
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2 border-b border-gray-100 pb-3">
          <div>
            <h2 className="text-base font-bold text-gray-900 flex items-center gap-2">
              <BookOpen className="w-5 h-5 text-brand-500" /> Exam Study Materials & Free Practice Tests
            </h2>
            <p className="text-xs text-gray-500">Official preparation guides, section tips, and free practice resources for your study abroad exams</p>
          </div>
          <span className="text-[11px] font-semibold px-2.5 py-1 rounded-full bg-brand-50 text-brand-600 border border-brand-200 self-start sm:self-auto">
            100% Free Practice Portals
          </span>
        </div>

        {/* Exam Selection Tabs */}
        <div className="flex flex-wrap gap-2">
          {EXAM_STUDY_MATERIALS.map((exam) => (
            <button
              key={exam.id}
              onClick={() => setActiveExamId(exam.id)}
              className={clsx(
                'px-3.5 py-2 rounded-xl text-xs font-semibold transition-all flex items-center gap-2 border',
                activeExamId === exam.id
                  ? 'bg-brand-500 text-white border-brand-500 shadow-xs'
                  : 'bg-white text-gray-700 hover:bg-gray-50 border-gray-200'
              )}
            >
              <span>{exam.icon}</span>
              <span>{exam.name}</span>
            </button>
          ))}
        </div>

        {/* Selected Exam Material View */}
        {(() => {
          const exam = EXAM_STUDY_MATERIALS.find((e) => e.id === activeExamId) || EXAM_STUDY_MATERIALS[0]
          return (
            <div className="space-y-4 pt-2">
              <div className="p-3.5 bg-white rounded-xl border border-gray-100 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2">
                <div>
                  <h3 className="font-bold text-sm text-gray-900 flex items-center gap-2">
                    <span>{exam.icon}</span> {exam.name} Preparation Hub
                  </h3>
                  <p className="text-xs text-gray-600 mt-0.5">{exam.description}</p>
                </div>
                <div className="px-3 py-1.5 rounded-lg bg-emerald-50 text-emerald-800 text-xs font-bold border border-emerald-200 shrink-0">
                  Target: {exam.targetScore}
                </div>
              </div>

              {/* Section Strategies */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                {exam.sections.map((sec, sIdx) => (
                  <div key={sIdx} className="p-3 bg-white/80 rounded-xl border border-gray-100 space-y-1">
                    <h4 className="font-semibold text-xs text-gray-900 flex items-center gap-1.5">
                      <GraduationCap className="w-3.5 h-3.5 text-brand-500" /> {sec.name}
                    </h4>
                    <p className="text-xs text-gray-600 leading-relaxed">{sec.tips}</p>
                  </div>
                ))}
              </div>

              {/* Official Free Download Links */}
              <div className="pt-2">
                <h4 className="text-xs font-bold text-gray-800 mb-2 flex items-center gap-1.5">
                  <Download className="w-3.5 h-3.5 text-brand-500" /> Official Free Practice Tests & Download Links
                </h4>
                <div className="flex flex-wrap gap-2">
                  {exam.officialResources.map((res, rIdx) => (
                    <a
                      key={rIdx}
                      href={res.url}
                      target="_blank"
                      rel="noreferrer"
                      className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-white text-brand-600 hover:bg-brand-500 hover:text-white transition-all text-xs font-semibold border border-brand-200 shadow-2xs group"
                    >
                      <FileText className="w-3.5 h-3.5 text-brand-400 group-hover:text-white" />
                      <span>{res.title}</span>
                      <ExternalLink className="w-3 h-3 text-gray-400 group-hover:text-white" />
                    </a>
                  ))}
                </div>
              </div>
            </div>
          )
        })()}
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
