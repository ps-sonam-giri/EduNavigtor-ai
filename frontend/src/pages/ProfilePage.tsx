import { useState, useEffect } from 'react'
import { useForm } from 'react-hook-form'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { profileApi } from '@/lib/api'
import toast from 'react-hot-toast'
import { Save, Upload, User, BookOpen, Globe, DollarSign, Briefcase, CheckCircle } from 'lucide-react'
import { motion } from 'framer-motion'

const COUNTRIES = ['United States', 'United Kingdom', 'Canada', 'Australia', 'Germany', 'Ireland', 'New Zealand']

const NUMBER_FIELDS = [
  'cgpa', 'cgpa_scale', 'backlogs', 'graduation_year',
  'ielts_score', 'toefl_score', 'gre_score', 'gmat_score',
  'total_budget_usd', 'work_experience_years',
]

export default function ProfilePage() {
  const qc = useQueryClient()
  const [selectedCountries, setSelectedCountries] = useState<string[]>([])
  const [saved, setSaved] = useState(false)

  const { data: profile, isLoading } = useQuery({
    queryKey: ['profile'],
    queryFn: () => profileApi.get().then(r => r.data),
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
      // Clean: empty string → null, strings → numbers for numeric fields
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
      toast.success('Profile saved!')
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

  const handleDocUpload = async (docType: string, file: File) => {
    try {
      await profileApi.uploadDocument(docType, file)
      toast.success(`${docType} uploaded`)
      qc.invalidateQueries({ queryKey: ['profile'] })
    } catch {
      toast.error('Upload failed')
    }
  }

  if (isLoading) return (
    <div className="flex items-center justify-center h-40">
      <div className="animate-spin w-8 h-8 border-2 border-brand-500 border-t-transparent rounded-full" />
    </div>
  )

  return (
    <div className="max-w-3xl space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">My Profile</h1>
        <p className="text-gray-500 text-sm">Your academic profile powers all AI recommendations</p>
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
          <div className="flex items-center gap-3 mb-5">
            <div className="w-9 h-9 rounded-xl gradient-bg flex items-center justify-center">
              <Upload className="w-5 h-5 text-white" />
            </div>
            <h2 className="font-semibold text-gray-900">Documents (Auto-Extract)</h2>
          </div>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
            {(['resume', 'marksheet', 'ielts', 'sop'] as const).map(type => (
              <label key={type}
                className="flex flex-col items-center gap-2 p-4 border-2 border-dashed border-gray-200 rounded-xl cursor-pointer hover:border-brand-500 hover:bg-brand-50 transition-all text-center">
                <Upload className="w-5 h-5 text-gray-400" />
                <span className="text-xs font-medium text-gray-600 capitalize">{type}</span>
                <span className="text-xs text-gray-400">PDF / DOCX</span>
                <input type="file" accept=".pdf,.docx,.doc" className="hidden"
                  onChange={e => e.target.files?.[0] && handleDocUpload(type, e.target.files[0])} />
              </label>
            ))}
          </div>
          {profile?.documents && Object.keys(profile.documents).length > 0 && (
            <div className="mt-4 flex flex-wrap gap-2">
              {Object.entries(profile.documents).map(([k]) => (
                <span key={k} className="badge badge-green flex items-center gap-1">
                  <CheckCircle className="w-3 h-3" /> {k}
                </span>
              ))}
            </div>
          )}
        </motion.div>

        {/* Save */}
        <div className="flex justify-end">
          <button type="submit" disabled={mutation.isPending}
            className="btn-primary flex items-center gap-2">
            {mutation.isPending
              ? <><div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" /> Saving...</>
              : saved
                ? <><CheckCircle className="w-4 h-4" /> Saved!</>
                : <><Save className="w-4 h-4" /> Save Profile</>}
          </button>
        </div>

      </form>
    </div>
  )
}
