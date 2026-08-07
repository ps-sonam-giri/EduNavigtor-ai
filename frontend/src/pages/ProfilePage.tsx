import { useState, useEffect } from 'react'
import { useForm } from 'react-hook-form'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { profileApi } from '@/lib/api'
import toast from 'react-hot-toast'
import { Save, Upload, User, BookOpen, Globe, DollarSign, Briefcase, CheckCircle, Trash2, AlertTriangle, Loader2 } from 'lucide-react'
import { motion } from 'framer-motion'

const COUNTRIES = ['United States', 'United Kingdom', 'Canada', 'Australia', 'Germany', 'Ireland', 'New Zealand']

const NUMBER_FIELDS = [
  'cgpa', 'cgpa_scale', 'backlogs', 'graduation_year',
  'ielts_score', 'toefl_score', 'gre_score', 'gmat_score',
  'total_budget_usd', 'work_experience_years',
]

/** Calculate 6-Pillar Evaluation Matrix Scores based on profile */
function calculateEvaluationMatrix(profile: any) {
  const cgpa = Number(profile?.cgpa || 8.5)
  const scale = Number(profile?.cgpa_scale || 10)
  const normCgpa = Math.min(100, Math.round((cgpa / scale) * 100))

  const ielts = Number(profile?.ielts_score || 7.5)
  const gre = Number(profile?.gre_score || 320)
  const examScore = Math.min(100, Math.round(((ielts / 9) * 50) + ((gre / 340) * 50)))

  const budget = Number(profile?.total_budget_usd || 35000)
  const finScore = budget >= 40000 ? 95 : budget >= 25000 ? 85 : 70

  const exp = Number(profile?.work_experience_years || 2)
  const expScore = exp >= 3 ? 95 : exp >= 1 ? 85 : 70

  const docScore = profile?.documents && Object.keys(profile.documents).length >= 2 ? 90 : 75
  const timelineScore = 90 // Default strong timeframe score

  const overallScore = Math.round(
    (normCgpa * 0.25) +
    (examScore * 0.20) +
    (finScore * 0.20) +
    (expScore * 0.15) +
    (docScore * 0.10) +
    (timelineScore * 0.10)
  )

  return {
    overallScore,
    pillars: [
      { name: 'Academic Competitiveness', weight: '25%', score: normCgpa, status: normCgpa >= 80 ? 'Strong' : 'Average' },
      { name: 'Exam Readiness Index (IELTS/GRE)', weight: '20%', score: examScore, status: examScore >= 80 ? 'Competitive' : 'Target' },
      { name: 'Financial Coverage Viability', weight: '20%', score: finScore, status: finScore >= 80 ? 'Adequate' : 'Partial' },
      { name: 'Work & Research Strength', weight: '15%', score: expScore, status: expScore >= 80 ? 'Solid' : 'Developing' },
      { name: 'Document Readiness (SOP/LOR)', weight: '10%', score: docScore, status: docScore >= 85 ? 'Complete' : 'In Progress' },
      { name: 'Intake Timeline Feasibility', weight: '10%', score: timelineScore, status: 'On Track' },
    ]
  }
}

export default function ProfilePage() {
  const qc = useQueryClient()
  const [selectedCountries, setSelectedCountries] = useState<string[]>([])
  const [saved, setSaved] = useState(false)
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false)

  const { data: profile, isLoading } = useQuery({
    queryKey: ['profile'],
    queryFn: () => profileApi.get().then((r: any) => r.data),
    retry: false,
  })

  const { register, handleSubmit, reset } = useForm()

  // Populate form and countries when profile loads
  useEffect(() => {
    if (profile) {
      reset(profile)
      setSelectedCountries(profile.preferred_countries || [])
    }
  }, [profile, reset])

  const toggleCountry = (c: string) => {
    setSelectedCountries(prev =>
      prev.includes(c) ? prev.filter(x => x !== c) : [...prev, c]
    )
  }

  const mutation = useMutation({
    mutationFn: async (raw: any) => {
      const clean: Record<string, any> = {}
      for (const [key, val] of Object.entries(raw)) {
        if (val === '' || val === undefined) {
          clean[key] = null
        } else if (NUMBER_FIELDS.includes(key)) {
          const n = Number(val)
          clean[key] = isNaN(n) ? null : n
        } else {
          clean[key] = val
        }
      }
      clean.preferred_countries = selectedCountries
      return profile ? profileApi.update(clean) : profileApi.create(clean)
    },
    onSuccess: (res) => {
      toast.success('Profile saved successfully!')
      setSaved(true)
      setTimeout(() => setSaved(false), 3000)
      qc.invalidateQueries({ queryKey: ['profile'] })
      reset(res.data)
    },
    onError: (err: any) => {
      const detail = err?.response?.data?.detail
      toast.error('Save failed: ' + (Array.isArray(detail) ? detail[0]?.msg : detail || err.message))
    },
  })

  const deleteMutation = useMutation({
    mutationFn: () => profileApi.delete(),
    onSuccess: () => {
      toast.success('User profile deleted successfully!')
      setShowDeleteConfirm(false)
      setSelectedCountries([])
      reset({
        cgpa: '', cgpa_scale: 10, degree: '', specialization: '', graduation_year: '', backlogs: '', university_name: '',
        ielts_score: '', toefl_score: '', gre_score: '', gmat_score: '', course_interest: '', target_intake: '', career_goal: '',
        total_budget_usd: '', financial_background: '', work_experience_years: '', work_description: ''
      })
      qc.invalidateQueries({ queryKey: ['profile'] })
    },
    onError: (err: any) => {
      toast.error('Could not delete profile: ' + (err?.response?.data?.detail || err.message))
    },
  })

  const handleDocUpload = async (docType: string, file: File) => {
    try {
      const res: any = await profileApi.uploadDocument(docType, file)
      const ver = res.data?.verification
      if (ver?.message) {
        toast.success(`[${docType.toUpperCase()}] ${ver.message}`)
      } else {
        toast.success(`${docType.toUpperCase()} uploaded & verified!`)
      }
      qc.invalidateQueries({ queryKey: ['profile'] })
    } catch {
      toast.error('Document upload failed')
    }
  }

  if (isLoading) return (
    <div className="flex items-center justify-center h-40">
      <div className="animate-spin w-8 h-8 border-2 border-brand-500 border-t-transparent rounded-full" />
    </div>
  )

  const matrix = calculateEvaluationMatrix(profile)

  return (
    <div className="max-w-3xl space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">My Profile & Evaluation Scorecard</h1>
        <p className="text-gray-500 text-sm">Your academic profile powers AI recommendations and candidate admission scoring</p>
      </div>

      {/* AI Candidate Evaluation Matrix Scorecard */}
      <div className="card space-y-4 border-brand-100 bg-gradient-to-br from-white via-brand-50/10 to-indigo-50/20 shadow-sm">
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2 border-b border-slate-100 pb-3">
          <div>
            <h2 className="text-base font-bold text-slate-900 flex items-center gap-2">
              <CheckCircle className="w-5 h-5 text-brand-500" /> AI Candidate Evaluation Matrix
            </h2>
            <p className="text-xs text-slate-500">6-pillar weighted index for university admission competitiveness</p>
          </div>
          <div className="px-3.5 py-1.5 rounded-full bg-brand-500 text-white text-xs font-bold shadow-xs shrink-0 self-start sm:self-auto">
            Profile Score: {matrix.overallScore} / 100
          </div>
        </div>

        {/* 6 Pillar Progress Bars */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3 pt-1">
          {matrix.pillars.map((p, idx) => (
            <div key={idx} className="p-3 bg-white rounded-xl border border-slate-100 space-y-1.5">
              <div className="flex items-center justify-between text-xs">
                <span className="font-semibold text-slate-800">{p.name} <span className="text-[10px] text-slate-400">({p.weight})</span></span>
                <span className="font-bold text-brand-600">{p.score}%</span>
              </div>
              <div className="w-full bg-slate-100 rounded-full h-2 overflow-hidden">
                <div className="bg-gradient-to-r from-brand-500 to-indigo-600 h-2 rounded-full transition-all duration-500" style={{ width: `${p.score}%` }} />
              </div>
              <div className="flex items-center justify-between text-[11px]">
                <span className="text-slate-400">Status</span>
                <span className="font-semibold text-emerald-600 bg-emerald-50 px-2 py-0.5 rounded-full border border-emerald-200/60">{p.status}</span>
              </div>
            </div>
          ))}
        </div>
      </div>

      <form onSubmit={handleSubmit(d => mutation.mutate(d))} className="space-y-6">

        {/* Academic */}
        <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="card">
          <div className="flex items-center gap-3 mb-5">
            <div className="w-9 h-9 rounded-xl gradient-bg flex items-center justify-center">
              <BookOpen className="w-5 h-5 text-white" />
            </div>
            <h2 className="font-semibold text-gray-900">Academic Background</h2>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="label">CGPA</label>
              <input {...register('cgpa')} type="number" step="0.01" placeholder="8.5" className="input" />
            </div>
            <div>
              <label className="label">CGPA Scale</label>
              <select {...register('cgpa_scale')} className="input">
                <option value={10}>Out of 10</option>
                <option value={4}>Out of 4</option>
              </select>
            </div>
            <div>
              <label className="label">Degree</label>
              <input {...register('degree')} placeholder="B.Tech / B.E." className="input" />
            </div>
            <div>
              <label className="label">Specialization</label>
              <input {...register('specialization')} placeholder="Computer Science" className="input" />
            </div>
            <div>
              <label className="label">Graduation Year</label>
              <input {...register('graduation_year')} type="number" placeholder="2024" className="input" />
            </div>
            <div>
              <label className="label">Backlogs</label>
              <input {...register('backlogs')} type="number" placeholder="0" className="input" />
            </div>
            <div className="md:col-span-2">
              <label className="label">Current University</label>
              <input {...register('university_name')} placeholder="IIT Bombay / VIT / Anna University" className="input" />
            </div>
          </div>
        </motion.div>

        {/* Test Scores */}
        <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.05 }} className="card">
          <div className="flex items-center gap-3 mb-5">
            <div className="w-9 h-9 rounded-xl gradient-bg flex items-center justify-center">
              <User className="w-5 h-5 text-white" />
            </div>
            <h2 className="font-semibold text-gray-900">Test Scores</h2>
          </div>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div>
              <label className="label">IELTS Score</label>
              <input {...register('ielts_score')} type="number" step="0.5" placeholder="7.5" className="input" />
            </div>
            <div>
              <label className="label">TOEFL Score</label>
              <input {...register('toefl_score')} type="number" placeholder="100" className="input" />
            </div>
            <div>
              <label className="label">GRE Score</label>
              <input {...register('gre_score')} type="number" placeholder="315" className="input" />
            </div>
            <div>
              <label className="label">GMAT Score</label>
              <input {...register('gmat_score')} type="number" placeholder="680" className="input" />
            </div>
          </div>
        </motion.div>

        {/* Study Preferences */}
        <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.1 }} className="card">
          <div className="flex items-center gap-3 mb-5">
            <div className="w-9 h-9 rounded-xl gradient-bg flex items-center justify-center">
              <Globe className="w-5 h-5 text-white" />
            </div>
            <h2 className="font-semibold text-gray-900">Study Preferences</h2>
          </div>
          <div className="space-y-4">
            <div>
              <label className="label">Preferred Countries</label>
              <div className="flex flex-wrap gap-2 mt-1">
                {COUNTRIES.map(c => (
                  <button
                    key={c} type="button" onClick={() => toggleCountry(c)}
                    className={`px-3 py-1.5 rounded-lg text-sm font-medium border transition-all ${
                      selectedCountries.includes(c)
                        ? 'bg-brand-500 text-white border-brand-500'
                        : 'bg-white text-gray-600 border-gray-200 hover:border-brand-500'
                    }`}
                  >
                    {c}
                  </button>
                ))}
              </div>
            </div>
            <div className="grid md:grid-cols-2 gap-4">
              <div>
                <label className="label">Course Interest</label>
                <input {...register('course_interest')} placeholder="Computer Science / Data Science / MBA" className="input" />
              </div>
              <div>
                <label className="label">Target Intake</label>
                <select {...register('target_intake')} className="input">
                  <option value="">Select intake</option>
                  {Array.from({ length: (2090 - 2025) * 2 + 2 }, (_, i) => {
                    const year = 2025 + Math.floor(i / 2)
                    const season = i % 2 === 0 ? 'Fall' : 'Spring'
                    return `${season} ${year}`
                  }).map(v => <option key={v} value={v}>{v}</option>)}
                </select>
              </div>
            </div>
            <div>
              <label className="label">Career Goal</label>
              <textarea {...register('career_goal')} rows={2}
                placeholder="e.g. Software Engineer at a top tech company, data scientist in healthcare..."
                className="input resize-none" />
            </div>
          </div>
        </motion.div>

        {/* Financial */}
        <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.15 }} className="card">
          <div className="flex items-center gap-3 mb-5">
            <div className="w-9 h-9 rounded-xl gradient-bg flex items-center justify-center">
              <DollarSign className="w-5 h-5 text-white" />
            </div>
            <h2 className="font-semibold text-gray-900">Financial Background</h2>
          </div>
          <div className="grid md:grid-cols-2 gap-4">
            <div>
              <label className="label">Total Budget (USD)</label>
              <input {...register('total_budget_usd')} type="number" placeholder="60000" className="input" />
              <p className="text-xs text-gray-400 mt-1">Total for entire program (tuition + living)</p>
            </div>
            <div>
              <label className="label">Funding Source</label>
              <select {...register('financial_background')} className="input">
                <option value="">Select source</option>
                <option value="self_funded">Self Funded / Family</option>
                <option value="education_loan">Education Loan</option>
                <option value="partial_scholarship">Partial Scholarship</option>
                <option value="full_scholarship">Seeking Full Scholarship</option>
              </select>
            </div>
          </div>
        </motion.div>

        {/* Work Experience */}
        <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.2 }} className="card">
          <div className="flex items-center gap-3 mb-5">
            <div className="w-9 h-9 rounded-xl gradient-bg flex items-center justify-center">
              <Briefcase className="w-5 h-5 text-white" />
            </div>
            <h2 className="font-semibold text-gray-900">Work Experience</h2>
          </div>
          <div className="space-y-4">
            <div>
              <label className="label">Work Experience (years)</label>
              <input {...register('work_experience_years')} type="number" placeholder="0" className="input w-40" />
            </div>
            <div>
              <label className="label">Work Description</label>
              <textarea {...register('work_description')} rows={2}
                placeholder="e.g. 2 years as Software Developer at TCS"
                className="input resize-none" />
            </div>
          </div>
        </motion.div>

        {/* Documents */}
        <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.25 }} className="card">
          <div className="flex items-center justify-between mb-5">
            <div className="flex items-center gap-3">
              <div className="w-9 h-9 rounded-xl gradient-bg flex items-center justify-center">
                <Upload className="w-5 h-5 text-white" />
              </div>
              <div>
                <h2 className="font-semibold text-gray-900">Documents Verification & Extraction</h2>
                <p className="text-xs text-gray-500">Upload Resume, Marksheet, IELTS Scorecard, or SOP for instant AI verification</p>
              </div>
            </div>
          </div>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
            {(['resume', 'marksheet', 'ielts', 'sop'] as const).map(type => {
              const docInfo = profile?.documents?.[type]
              const isVerified = typeof docInfo === 'object' ? docInfo?.verified : Boolean(docInfo)
              const msg = typeof docInfo === 'object' ? docInfo?.message : null
              const insights = typeof docInfo === 'object' ? docInfo?.extracted_insights : null

              return (
                <label key={type}
                  className={`flex flex-col items-center gap-2 p-4 border-2 border-dashed rounded-xl cursor-pointer transition-all text-center relative ${
                    isVerified 
                      ? 'border-emerald-300 bg-emerald-50/40 hover:bg-emerald-50' 
                      : 'border-gray-200 hover:border-brand-500 hover:bg-brand-50'
                  }`}>
                  {isVerified ? (
                    <CheckCircle className="w-5 h-5 text-emerald-600" />
                  ) : (
                    <Upload className="w-5 h-5 text-gray-400" />
                  )}
                  <div className="flex items-center gap-1">
                    <span className="text-xs font-semibold text-gray-800 uppercase tracking-wide">{type}</span>
                    {isVerified && (
                      <span className="inline-block w-2 h-2 rounded-full bg-emerald-500" title="Verified" />
                    )}
                  </div>
                  <span className="text-[11px] text-gray-400">PDF / DOCX</span>
                  
                  {isVerified && (
                    <span className="text-[10px] font-semibold text-emerald-700 bg-emerald-100/80 px-2 py-0.5 rounded-full mt-1">
                      ✓ Verified
                    </span>
                  )}

                  {insights?.cgpa && (
                    <span className="text-[10px] font-bold text-brand-700 bg-brand-50 px-2 py-0.5 rounded-full border border-brand-200">
                      CGPA: {insights.cgpa}
                    </span>
                  )}
                  {insights?.ielts_score && (
                    <span className="text-[10px] font-bold text-violet-700 bg-violet-50 px-2 py-0.5 rounded-full border border-violet-200">
                      IELTS: {insights.ielts_score}
                    </span>
                  )}

                  <input type="file" accept=".pdf,.docx,.doc,.txt" className="hidden"
                    onChange={e => e.target.files?.[0] && handleDocUpload(type, e.target.files[0])} />
                </label>
              )
            })}
          </div>

          {profile?.documents && Object.keys(profile.documents).length > 0 && (
            <div className="mt-4 p-3 bg-slate-50 rounded-xl border border-slate-200 space-y-1.5">
              <span className="text-xs font-semibold text-slate-700 flex items-center gap-1.5 mb-1">
                <CheckCircle className="w-4 h-4 text-emerald-600" /> Verified Documents Overview:
              </span>
              <div className="flex flex-wrap gap-2">
                {Object.entries(profile.documents).map(([k, val]: [string, any]) => {
                  const statusMsg = typeof val === 'object' ? val?.message : 'Verified'
                  return (
                    <div key={k} className="text-xs bg-white px-3 py-1.5 rounded-lg border border-slate-200 text-slate-700 flex items-center gap-2 shadow-2xs">
                      <span className="font-semibold uppercase text-brand-600">{k}:</span>
                      <span className="text-slate-600">{statusMsg}</span>
                    </div>
                  )
                })}
              </div>
            </div>
          )}
        </motion.div>

        {/* Save & Delete Profile Buttons */}
        <div className="flex items-center justify-between pt-2">
          {/* Delete Profile Button */}
          {profile ? (
            <button
              type="button"
              onClick={() => setShowDeleteConfirm(true)}
              className="text-xs text-red-600 hover:text-red-800 font-semibold flex items-center gap-1.5 px-3 py-2 rounded-lg border border-red-200 hover:bg-red-50 transition-colors"
            >
              <Trash2 className="w-4 h-4 text-red-500" /> Delete Profile
            </button>
          ) : <div />}

          <button
            type="submit"
            disabled={mutation.isPending}
            className="btn-primary flex items-center gap-2"
          >
            {mutation.isPending
              ? <><Loader2 className="w-4 h-4 animate-spin" /> Saving...</>
              : saved
                ? <><CheckCircle className="w-4 h-4" /> Saved!</>
                : <><Save className="w-4 h-4" /> Save Profile</>}
          </button>
        </div>

      </form>

      {/* Delete Confirmation Modal */}
      {showDeleteConfirm && (
        <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center p-4 z-50">
          <motion.div
            initial={{ scale: 0.95, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            className="bg-white rounded-2xl p-6 max-w-md w-full space-y-4 shadow-xl border border-gray-100"
          >
            <div className="flex items-center gap-3 text-red-600">
              <div className="w-10 h-10 rounded-full bg-red-100 flex items-center justify-center shrink-0">
                <AlertTriangle className="w-5 h-5 text-red-600" />
              </div>
              <div>
                <h3 className="font-bold text-gray-900 text-lg">Delete Profile?</h3>
                <p className="text-xs text-gray-500">This action cannot be undone.</p>
              </div>
            </div>

            <p className="text-xs text-gray-600 leading-relaxed bg-red-50 p-3 rounded-xl border border-red-100">
              Deleting your profile will permanently remove your stored academic scores (CGPA, IELTS, GRE), budget preferences, and uploaded documents.
            </p>

            <div className="flex items-center justify-end gap-3 pt-2">
              <button
                type="button"
                onClick={() => setShowDeleteConfirm(false)}
                className="btn-secondary text-xs px-4 py-2"
              >
                Cancel
              </button>
              <button
                type="button"
                onClick={() => deleteMutation.mutate()}
                disabled={deleteMutation.isPending}
                className="bg-red-600 hover:bg-red-700 text-white text-xs font-bold px-4 py-2 rounded-xl transition-colors flex items-center gap-1.5 disabled:opacity-50"
              >
                {deleteMutation.isPending ? <Loader2 className="w-3.5 h-3.5 animate-spin" /> : <Trash2 className="w-3.5 h-3.5" />}
                Yes, Delete Profile
              </button>
            </div>
          </motion.div>
        </div>
      )}
    </div>
  )
}
