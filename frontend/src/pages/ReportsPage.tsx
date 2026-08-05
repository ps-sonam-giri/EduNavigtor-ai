import { useState } from 'react'
import { useQuery, useQueryClient } from '@tanstack/react-query'
import { reportApi } from '@/lib/api'
import { FileText, Download, Mail, Loader2, Clock, Send, CheckCircle } from 'lucide-react'
import { motion } from 'framer-motion'
import toast from 'react-hot-toast'

export default function ReportsPage() {
  const qc = useQueryClient()
  const [emailInputs, setEmailInputs] = useState<Record<string, string>>({})
  const [sendingEmail, setSendingEmail] = useState<string | null>(null)
  const [downloadingId, setDownloadingId] = useState<string | null>(null)

  const { data: reports = [], isLoading, refetch } = useQuery({
    queryKey: ['reports'],
    queryFn: () => reportApi.list().then(r => r.data),
    refetchInterval: 10000, // auto-refresh every 10s
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
    } catch {
      toast.error('PDF still generating — try again in 30 seconds')
    } finally {
      setDownloadingId(null)
    }
  }

  const handleSendEmail = async (reportId: string) => {
    const email = emailInputs[reportId]?.trim()
    if (!email) { toast.error('Enter an email address first'); return }
    setSendingEmail(reportId)
    try {
      await reportApi.email({ report_id: reportId, recipient: email })
      toast.success(`Report sent to ${email}`)
      qc.invalidateQueries({ queryKey: ['reports'] })
    } catch {
      toast.error('Email send failed. Check Gmail configuration.')
    } finally {
      setSendingEmail(null)
    }
  }

  return (
    <div className="space-y-6">
      <div className="flex items-start justify-between flex-wrap gap-4">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Reports</h1>
          <p className="text-gray-500 text-sm">AI-generated study abroad reports — auto-created after every agent run</p>
        </div>
        <button onClick={() => refetch()} className="btn-secondary text-sm py-2 flex items-center gap-2">
          Refresh
        </button>
      </div>

      {/* How it works */}
      <div className="bg-brand-50 border border-brand-100 rounded-2xl p-5">
        <h3 className="font-semibold text-brand-700 mb-2">How reports work</h3>
        <ul className="text-sm text-brand-700 space-y-1">
          <li>• Reports are <strong>automatically generated</strong> after every AI Copilot conversation</li>
          <li>• The PDF is ready within 30-60 seconds after the chat completes</li>
          <li>• You can download the PDF or send it directly to your Gmail</li>
        </ul>
      </div>

      {isLoading ? (
        <div className="flex items-center justify-center h-40">
          <Loader2 className="w-8 h-8 animate-spin text-brand-500" />
        </div>
      ) : reports.length === 0 ? (
        <div className="text-center py-16 text-gray-400 card">
          <FileText className="w-12 h-12 mx-auto mb-3 opacity-30" />
          <p className="font-medium text-gray-600">No reports yet</p>
          <p className="text-sm mt-1">Go to AI Copilot and ask for university recommendations or a complete study plan. Your report will appear here automatically.</p>
        </div>
      ) : (
        <div className="space-y-4">
          {reports.map((report: any, i: number) => (
            <motion.div
              key={report.id}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.05 }}
              className="card"
            >
              <div className="flex items-start gap-4 flex-wrap">
                <div className="w-12 h-12 rounded-xl gradient-bg flex items-center justify-center flex-shrink-0">
                  <FileText className="w-6 h-6 text-white" />
                </div>
                <div className="flex-1 min-w-0">
                  <h3 className="font-semibold text-gray-900">{report.title}</h3>
                  <div className="flex items-center gap-3 mt-1 flex-wrap">
                    <span className="badge badge-blue">{report.report_type}</span>
                    <span className="text-xs text-gray-500 flex items-center gap-1">
                      <Clock className="w-3.5 h-3.5" />
                      {new Date(report.created_at).toLocaleDateString('en-IN', {
                        day: 'numeric', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit'
                      })}
                    </span>
                    {report.email_sent && (
                      <span className="badge badge-green flex items-center gap-1">
                        <CheckCircle className="w-3 h-3" /> Email sent
                      </span>
                    )}
                    {!report.pdf_path && (
                      <span className="badge badge-orange text-xs flex items-center gap-1">
                        <Loader2 className="w-3 h-3 animate-spin" /> Generating PDF...
                      </span>
                    )}
                  </div>
                  {report.summary && (
                    <p className="text-sm text-gray-500 mt-2">{report.summary}</p>
                  )}
                </div>
              </div>

              {/* Actions */}
              <div className="mt-5 pt-4 border-t border-gray-100 flex flex-wrap gap-3 items-end">
                {/* Download */}
                <button
                  onClick={() => handleDownload(report.id, report.title)}
                  disabled={downloadingId === report.id || !report.pdf_path}
                  className="btn-secondary flex items-center gap-2 text-sm py-2 disabled:opacity-50"
                  title={!report.pdf_path ? 'PDF still generating...' : 'Download PDF'}
                >
                  {downloadingId === report.id
                    ? <Loader2 className="w-4 h-4 animate-spin" />
                    : <Download className="w-4 h-4" />}
                  {report.pdf_path ? 'Download PDF' : 'PDF Generating...'}
                </button>

                {/* Send to Gmail */}
                <div className="flex gap-2 flex-1 min-w-0">
                  <div className="relative flex-1 min-w-0">
                    <Mail className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
                    <input
                      type="email"
                      placeholder="Enter Gmail address to send report"
                      value={emailInputs[report.id] || ''}
                      onChange={e => setEmailInputs(prev => ({ ...prev, [report.id]: e.target.value }))}
                      className="input pl-9 text-sm py-2 w-full"
                    />
                  </div>
                  <button
                    onClick={() => handleSendEmail(report.id)}
                    disabled={sendingEmail === report.id || !emailInputs[report.id]}
                    className="btn-primary flex items-center gap-2 text-sm py-2 disabled:opacity-50 whitespace-nowrap"
                  >
                    {sendingEmail === report.id
                      ? <Loader2 className="w-4 h-4 animate-spin" />
                      : <Send className="w-4 h-4" />}
                    Send to Gmail
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
