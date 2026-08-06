import { useState } from 'react'
import { useQuery, useQueryClient } from '@tanstack/react-query'
import { reportApi } from '@/lib/api'
import { FileText, Download, Mail, Loader2, Clock, Send, CheckCircle, HelpCircle, ShieldCheck, KeyRound } from 'lucide-react'
import { motion } from 'framer-motion'
import toast from 'react-hot-toast'

export default function ReportsPage() {
  const qc = useQueryClient()
  const [emailInputs, setEmailInputs] = useState<Record<string, string>>({})
  const [sendingEmail, setSendingEmail] = useState<string | null>(null)
  const [downloadingId, setDownloadingId] = useState<string | null>(null)
  const [showEmailHelp, setShowEmailHelp] = useState(false)

  const { data: reports = [], isLoading, refetch } = useQuery({
    queryKey: ['reports'],
    queryFn: () => reportApi.list().then(r => r.data),
    refetchInterval: 8000,
  })

  const handleDownload = async (id: string, title: string) => {
    setDownloadingId(id)
    try {
      const res = await reportApi.download(id)
      const url = URL.createObjectURL(new Blob([res.data], { type: 'application/pdf' }))
      const a = document.createElement('a')
      a.href = url
      a.download = `edupilot_report_${id.slice(0, 8)}.pdf`
      a.click()
      URL.revokeObjectURL(url)
      toast.success('Downloaded PDF report!')
    } catch {
      toast.error('PDF still generating — try downloading again in 15 seconds')
    } finally {
      setDownloadingId(null)
    }
  }

  const handleSendEmail = async (reportId: string) => {
    const email = emailInputs[reportId]?.trim()
    if (!email) {
      toast.error('Please enter a valid email address')
      return
    }
    setSendingEmail(reportId)
    try {
      await reportApi.email({ report_id: reportId, recipient: email })
      toast.success(`Email dispatch initiated for ${email}!`)
      qc.invalidateQueries({ queryKey: ['reports'] })
    } catch {
      toast.error('Email dispatch failed. Please check SMTP settings in backend/.env.')
    } finally {
      setSendingEmail(null)
    }
  }

  return (
    <div className="space-y-6 max-w-5xl">
      {/* Header */}
      <div className="flex items-start justify-between flex-wrap gap-4">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Study Abroad PDF Reports</h1>
          <p className="text-gray-500 text-sm">Download or email your personalized university & budget analysis reports</p>
        </div>
        <button onClick={() => refetch()} className="btn-secondary text-sm py-2 flex items-center gap-2">
          Refresh List
        </button>
      </div>

      {/* How Reports & Emailing Work Banner */}
      <div className="bg-gradient-to-br from-brand-50 to-purple-50 border border-brand-100 rounded-2xl p-5 space-y-3">
        <div className="flex items-center justify-between">
          <h3 className="font-bold text-brand-900 text-sm flex items-center gap-2">
            <FileText className="w-4 h-4 text-brand-600" /> PDF Reports & Email Dispatch Setup
          </h3>
          <button
            onClick={() => setShowEmailHelp(!showEmailHelp)}
            className="text-xs font-semibold text-brand-600 hover:text-brand-800 flex items-center gap-1 bg-white px-3 py-1 rounded-full border border-brand-200"
          >
            <HelpCircle className="w-3.5 h-3.5" /> {showEmailHelp ? 'Hide Setup Guide' : 'How to receive email directly'}
          </button>
        </div>

        <ul className="text-xs text-brand-800 space-y-1 leading-relaxed">
          <li>• Reports are <strong>automatically generated</strong> whenever you ask AI Copilot for recommendations.</li>
          <li>• Click <strong>"Download PDF"</strong> below to instantly view your full report document anytime.</li>
        </ul>

        {/* Expandable Email Setup Helper */}
        {showEmailHelp && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            className="mt-3 pt-3 border-t border-brand-200/60 text-xs text-gray-700 bg-white/80 backdrop-blur-md p-4 rounded-xl space-y-2 border border-brand-100"
          >
            <h4 className="font-bold text-gray-900 flex items-center gap-1.5">
              <KeyRound className="w-4 h-4 text-amber-500" /> Enable Direct Email Delivery to Your Inbox
            </h4>
            <p className="text-gray-600">To send reports directly to any Gmail or email inbox, add your Gmail App Password to <code className="bg-gray-100 px-1 py-0.5 rounded text-red-600">backend/.env</code>:</p>
            <div className="bg-gray-900 text-gray-100 p-3 rounded-lg font-mono text-[11px] space-y-1">
              <p><span className="text-gray-400"># Open backend/.env and set your Gmail details:</span></p>
              <p><span className="text-amber-400">SMTP_SERVER</span>=smtp.gmail.com</p>
              <p><span className="text-amber-400">SMTP_PORT</span>=587</p>
              <p><span className="text-amber-400">SMTP_USERNAME</span>=your-email@gmail.com</p>
              <p><span className="text-amber-400">SMTP_PASSWORD</span>=your-16-char-gmail-app-password</p>
            </div>
            <p className="text-[11px] text-gray-500">
              💡 <strong>How to get a Gmail App Password:</strong> Go to your Google Account → Security → 2-Step Verification → App Passwords → Create App Password.
            </p>
          </motion.div>
        )}
      </div>

      {isLoading ? (
        <div className="flex items-center justify-center h-40">
          <Loader2 className="w-8 h-8 animate-spin text-brand-500" />
        </div>
      ) : reports.length === 0 ? (
        <div className="text-center py-16 text-gray-400 card">
          <FileText className="w-12 h-12 mx-auto mb-3 opacity-30" />
          <p className="font-semibold text-gray-700">No reports generated yet</p>
          <p className="text-xs text-gray-400 mt-1">Go to AI Copilot and request a university recommendation or budget study plan. Your PDF report will be created automatically.</p>
        </div>
      ) : (
        <div className="space-y-4">
          {reports.map((report: any, i: number) => (
            <motion.div
              key={report.id}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.04 }}
              className="card"
            >
              <div className="flex items-start gap-4 flex-wrap">
                <div className="w-12 h-12 rounded-xl gradient-bg flex items-center justify-center shrink-0">
                  <FileText className="w-6 h-6 text-white" />
                </div>
                <div className="flex-1 min-w-0">
                  <h3 className="font-bold text-gray-900">{report.title}</h3>
                  <div className="flex items-center gap-3 mt-1.5 flex-wrap">
                    <span className="badge badge-blue">{report.report_type}</span>
                    <span className="text-xs text-gray-500 flex items-center gap-1">
                      <Clock className="w-3.5 h-3.5 text-gray-400" />
                      {new Date(report.created_at).toLocaleDateString('en-IN', {
                        day: 'numeric', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit'
                      })}
                    </span>
                    {report.email_sent ? (
                      <span className="badge badge-green flex items-center gap-1">
                        <CheckCircle className="w-3 h-3" /> Email delivered to {report.email_recipient || 'user'}
                      </span>
                    ) : (
                      <span className="badge badge-purple flex items-center gap-1 text-[11px]">
                        <ShieldCheck className="w-3 h-3" /> Ready for Download / Email
                      </span>
                    )}
                    {!report.pdf_path && (
                      <span className="badge badge-orange text-xs flex items-center gap-1">
                        <Loader2 className="w-3 h-3 animate-spin" /> Generating PDF...
                      </span>
                    )}
                  </div>
                  {report.summary && (
                    <p className="text-xs text-gray-600 mt-2 leading-relaxed">{report.summary}</p>
                  )}
                </div>
              </div>

              {/* Actions */}
              <div className="mt-5 pt-4 border-t border-gray-100 flex flex-wrap gap-3 items-end">
                {/* Download Button */}
                <button
                  onClick={() => handleDownload(report.id, report.title)}
                  disabled={downloadingId === report.id || !report.pdf_path}
                  className="btn-secondary flex items-center gap-2 text-sm py-2 disabled:opacity-50"
                  title={!report.pdf_path ? 'PDF still generating...' : 'Download PDF Report'}
                >
                  {downloadingId === report.id
                    ? <Loader2 className="w-4 h-4 animate-spin" />
                    : <Download className="w-4 h-4 text-brand-600" />}
                  {report.pdf_path ? 'Download PDF Report' : 'PDF Generating...'}
                </button>

                {/* Send Email Input & Button */}
                <div className="flex gap-2 flex-1 min-w-[280px]">
                  <div className="relative flex-1">
                    <Mail className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
                    <input
                      type="email"
                      placeholder="Enter your email to receive PDF report..."
                      value={emailInputs[report.id] || ''}
                      onChange={e => setEmailInputs(prev => ({ ...prev, [report.id]: e.target.value }))}
                      className="input pl-9 text-xs py-2 w-full"
                    />
                  </div>
                  <button
                    onClick={() => handleSendEmail(report.id)}
                    disabled={sendingEmail === report.id || !emailInputs[report.id]}
                    className="btn-primary flex items-center gap-2 text-xs py-2 disabled:opacity-50 whitespace-nowrap"
                  >
                    {sendingEmail === report.id
                      ? <Loader2 className="w-4 h-4 animate-spin" />
                      : <Send className="w-4 h-4" />}
                    Send Report to Email
                  </button>
                </div>
              </div>
            </motion.div>
          ))}
        </div>
      )}
    </div>
  )
}
