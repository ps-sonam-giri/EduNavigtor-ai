import AgentTrajectory from '@/components/AgentTrajectory'
import { useState, useRef, useEffect } from 'react'
import { useQuery, useQueryClient } from '@tanstack/react-query'
import { agentApi } from '@/lib/api'
import { motion, AnimatePresence } from 'framer-motion'
import {
  Send, Bot, User, Loader2, Zap, BookOpen,
  Globe, DollarSign, Clock, MessageSquare,
  Plus, Trash2, ChevronLeft, ChevronRight
} from 'lucide-react'
import toast from 'react-hot-toast'
import clsx from 'clsx'

interface Message {
  role: 'user' | 'assistant'
  content: string
  agents_used?: string[]
  timestamp: string
  duration_ms?: number
}

const SUGGESTIONS = [
  { icon: Globe, text: 'Which countries are best for me?' },
  { icon: BookOpen, text: 'Recommend universities for my profile' },
  { icon: DollarSign, text: 'What scholarships am I eligible for?' },
  { icon: Zap, text: 'Give me my complete study abroad plan' },
]

/** Render AI response: markdown tables, blockquotes, bullet points, headers */
function MessageContent({ content }: { content: string }) {
  const lines = content.split('\n')
  const elements: JSX.Element[] = []
  let i = 0

  while (i < lines.length) {
    const line = lines[i]

    // Markdown table detection
    if (line.startsWith('|') && lines[i + 1]?.match(/^\|[-| ]+\|$/)) {
      const headers = line.split('|').filter(Boolean).map(h => h.trim())
      i += 2 // skip header and separator
      const rows: string[][] = []
      while (i < lines.length && lines[i].startsWith('|')) {
        rows.push(lines[i].split('|').filter(Boolean).map(c => c.trim()))
        i++
      }
      elements.push(
        <div key={`table-${i}`} className="overflow-x-auto my-3.5 rounded-xl border border-brand-200/80 shadow-sm bg-white">
          <table className="w-full text-xs">
            <thead>
              <tr className="bg-gradient-to-r from-brand-600 via-indigo-600 to-purple-600 text-white">
                {headers.map((h, j) => (
                  <th key={j} className="px-4 py-2.5 text-left font-semibold tracking-wider text-[11px] uppercase whitespace-nowrap"
                    dangerouslySetInnerHTML={{ __html: h.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>') }} />
                ))}
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {rows.map((row, ri) => (
                <tr key={ri} className={clsx('transition-colors', ri % 2 === 0 ? 'bg-white hover:bg-brand-50/30' : 'bg-slate-50/50 hover:bg-brand-50/40')}>
                  {row.map((cell, ci) => {
                    // Format status pills
                    let cellFormatted = cell
                      .replace(/🟢\s*(High|Safe|High Match)/g, '<span class="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[11px] font-semibold bg-emerald-50 text-emerald-700 border border-emerald-200">🟢 $1</span>')
                      .replace(/🟡\s*(Medium|Target|Medium Match)/g, '<span class="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[11px] font-semibold bg-amber-50 text-amber-700 border border-amber-200">🟡 $1</span>')
                      .replace(/🔴\s*(Low|Reach|Low Match)/g, '<span class="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[11px] font-semibold bg-rose-50 text-rose-700 border border-rose-200">🔴 $1</span>')
                      .replace(/\*\*(.+?)\*\*/g, '<strong class="font-semibold text-slate-900">$1</strong>')
                      .replace(/\[(.+?)\]\((https?:\/\/.+?)\)/g, '<a href="$2" target="_blank" rel="noreferrer" class="inline-flex items-center gap-1 px-2.5 py-1 rounded-lg bg-brand-50 text-brand-600 hover:bg-brand-600 hover:text-white transition-all text-[11px] font-semibold border border-brand-200/80 shadow-xs">$1 ↗</a>')

                    return (
                      <td key={ci} className="px-4 py-2.5 text-slate-700 whitespace-nowrap text-xs"
                        dangerouslySetInnerHTML={{ __html: cellFormatted }} />
                    )
                  })}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )
      continue
    }

    if (!line.trim()) {
      elements.push(<div key={`empty-${i}`} className="h-2" />)
    } else {
      const formatted = line
        .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
        .replace(/\[(.+?)\]\((https?:\/\/.+?)\)/g, '<a href="$2" target="_blank" rel="noreferrer" class="text-brand-500 font-semibold underline hover:text-brand-600">$1 ↗</a>')

      // Blockquotes / Callout boxes
      if (line.startsWith('> ')) {
        elements.push(
          <div key={`quote-${i}`} className="my-2 p-3 bg-amber-50/80 border-l-4 border-amber-500 rounded-r-xl text-xs text-amber-900 font-medium">
            <span dangerouslySetInnerHTML={{ __html: formatted.replace(/^>\s*/, '') }} />
          </div>
        )
      }
      // Section Headers (### or ##)
      else if (line.startsWith('### ') || line.startsWith('## ')) {
        elements.push(
          <div key={`header-${i}`} className="mt-4 mb-2 flex items-center gap-2">
            <span className="h-2 w-2 rounded-full gradient-bg flex-shrink-0" />
            <h3 className="text-sm font-bold text-gray-900 uppercase tracking-wide"
              dangerouslySetInnerHTML={{ __html: formatted.replace(/^#+\s*/, '') }} />
          </div>
        )
      }
      // Bullet points
      else if (line.startsWith('• ') || line.startsWith('- ') || line.startsWith('  - ')) {
        const indent = line.startsWith('  - ')
        elements.push(
          <div key={`bullet-${i}`} className={`flex items-start gap-2 text-sm leading-relaxed ${indent ? 'ml-4 text-gray-600' : 'text-gray-800'}`}>
            <span className="text-brand-500 font-bold mt-0.5 flex-shrink-0">{indent ? '◦' : '•'}</span>
            <span dangerouslySetInnerHTML={{ __html: formatted.replace(/^[\s•\-◦]+/, '') }} />
          </div>
        )
      }
      // Numbered items (1. 2. 3.)
      else if (line.match(/^\d+\.\s/)) {
        const numMatch = line.match(/^(\d+)\.\s/)?.[1]
        elements.push(
          <div key={`num-${i}`} className="flex items-start gap-2.5 text-sm leading-relaxed my-1">
            <span className="w-5 h-5 rounded-full bg-brand-50 text-brand-700 font-bold text-xs flex items-center justify-center flex-shrink-0 mt-0.5 border border-brand-200">
              {numMatch}
            </span>
            <span dangerouslySetInnerHTML={{ __html: formatted.replace(/^\d+\.\s/, '') }} />
          </div>
        )
      }
      // Bold subheaders
      else if (line.match(/^\*\*.*\*\*$/) || line.match(/^\*\*.+\*\*/)) {
        elements.push(
          <p key={`bold-${i}`} className="text-sm font-semibold text-gray-900 mt-3 mb-1"
            dangerouslySetInnerHTML={{ __html: formatted }} />
        )
      }
      // Standard body paragraph
      else {
        elements.push(
          <p key={`text-${i}`} className="text-sm leading-relaxed text-gray-800"
            dangerouslySetInnerHTML={{ __html: formatted }} />
        )
      }
    }
    i++
  }

  return <div className="space-y-1">{elements}</div>
}

export default function ChatPage() {
  const qc = useQueryClient()
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [elapsed, setElapsed] = useState(0)
  const [sessionId, setSessionId] = useState<string>(() => `chat_${Date.now()}`)
  const [sidebarOpen, setSidebarOpen] = useState(true)
  const bottomRef = useRef<HTMLDivElement>(null)
  const timerRef = useRef<ReturnType<typeof setInterval> | null>(null)

  // Load session list
  const { data: sessions = [] } = useQuery({
    queryKey: ['chat-sessions'],
    queryFn: () => agentApi.getSessions().then(r => r.data),
    refetchInterval: 5000,
  })

  // Load current session messages
  useQuery({
    queryKey: ['chat-session', sessionId],
    queryFn: async () => {
      try {
        const r = await agentApi.getSession(sessionId)
        const msgs = r.data.messages || []
        if (msgs.length > 0) setMessages(msgs)
        return r.data
      } catch { return null }
    },
    enabled: !!sessionId,
    staleTime: Infinity,
  })

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  useEffect(() => {
    if (loading) {
      const t = Date.now()
      setElapsed(0)
      timerRef.current = setInterval(() => setElapsed(Math.floor((Date.now() - t) / 1000)), 1000)
    } else {
      if (timerRef.current) clearInterval(timerRef.current)
    }
    return () => { if (timerRef.current) clearInterval(timerRef.current) }
  }, [loading])

  const startNewChat = () => {
    const newId = `chat_${Date.now()}`
    setSessionId(newId)
    setMessages([])
    qc.invalidateQueries({ queryKey: ['chat-sessions'] })
  }

  const loadSession = async (sid: string) => {
    setSessionId(sid)
    setMessages([])
    try {
      const r = await agentApi.getSession(sid)
      setMessages(r.data.messages || [])
    } catch { toast.error('Could not load session') }
  }

  const deleteSession = async (sid: string, e: React.MouseEvent) => {
    e.stopPropagation()
    await agentApi.deleteSession(sid)
    if (sid === sessionId) startNewChat()
    qc.invalidateQueries({ queryKey: ['chat-sessions'] })
    toast.success('Session deleted')
  }

  const sendMessage = async (text?: string) => {
    const msg = text || input.trim()
    if (!msg || loading) return

    const userMsg: Message = {
      role: 'user',
      content: msg,
      timestamp: new Date().toISOString(),
    }
    setMessages(prev => [...prev, userMsg])
    setInput('')
    setLoading(true)

    const t0 = Date.now()
    try {
      const res = await agentApi.chat({ message: msg, session_id: sessionId, history: [] })
      const duration_ms = Date.now() - t0
      const aiMsg: Message = {
        role: 'assistant',
        content: res.data.content || 'Done! Check the relevant section for details.',
        agents_used: res.data.agents_used,
        timestamp: new Date().toISOString(),
        duration_ms,
      }
      setMessages(prev => [...prev, aiMsg])
      qc.invalidateQueries({ queryKey: ['chat-sessions'] })
      qc.invalidateQueries({ queryKey: ['reports'] })
    } catch {
      toast.error('Request failed. Please try again.')
      setMessages(prev => prev.slice(0, -1))
    } finally {
      setLoading(false)
    }
  }

  const noMessages = messages.length === 0

  return (
    <div className="flex h-[calc(100vh-5rem)] gap-4">

      {/* Sidebar – session history */}
      <AnimatePresence initial={false}>
        {sidebarOpen && (
          <motion.aside
            initial={{ width: 0, opacity: 0 }}
            animate={{ width: 260, opacity: 1 }}
            exit={{ width: 0, opacity: 0 }}
            transition={{ duration: 0.2 }}
            className="flex-shrink-0 bg-white rounded-2xl border border-gray-100 shadow-sm flex flex-col overflow-hidden"
          >
            <div className="p-4 border-b border-gray-100 flex items-center justify-between">
              <h3 className="font-semibold text-gray-900 text-sm">Chat History</h3>
              <button
                onClick={startNewChat}
                className="w-7 h-7 rounded-lg bg-brand-500 text-white flex items-center justify-center hover:bg-brand-600 transition-colors"
                title="New chat"
              >
                <Plus className="w-4 h-4" />
              </button>
            </div>

            <div className="flex-1 overflow-y-auto p-2 space-y-1">
              {sessions.length === 0 && (
                <p className="text-xs text-gray-400 text-center mt-4">No previous chats</p>
              )}
              {sessions.map((s: any) => (
                <button
                  key={s.session_id}
                  onClick={() => loadSession(s.session_id)}
                  className={clsx(
                    'w-full text-left px-3 py-2.5 rounded-xl text-sm transition-all group flex items-start gap-2',
                    s.session_id === sessionId
                      ? 'bg-brand-50 text-brand-700'
                      : 'hover:bg-gray-50 text-gray-700'
                  )}
                >
                  <MessageSquare className="w-3.5 h-3.5 flex-shrink-0 mt-0.5 text-gray-400" />
                  <div className="flex-1 min-w-0">
                    <p className="truncate font-medium text-xs">{s.title}</p>
                    <p className="text-xs text-gray-400 mt-0.5">{s.message_count} messages</p>
                  </div>
                  <button
                    onClick={(e) => deleteSession(s.session_id, e)}
                    className="opacity-0 group-hover:opacity-100 transition-opacity p-0.5 rounded hover:text-red-500"
                  >
                    <Trash2 className="w-3 h-3" />
                  </button>
                </button>
              ))}
            </div>
          </motion.aside>
        )}
      </AnimatePresence>

      {/* Main chat area */}
      <div className="flex-1 flex flex-col min-w-0">
        {/* Header */}
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-3">
            <button
              onClick={() => setSidebarOpen(!sidebarOpen)}
              className="p-2 rounded-xl hover:bg-gray-100 transition-colors"
            >
              {sidebarOpen ? <ChevronLeft className="w-4 h-4" /> : <ChevronRight className="w-4 h-4" />}
            </button>
            <div>
              <h1 className="text-xl font-bold text-gray-900">AI Copilot</h1>
              <p className="text-gray-500 text-xs">Powered by Gemini 3.5 Flash Lite + LangGraph</p>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <div className="text-xs text-gray-400 bg-gray-100 px-3 py-1.5 rounded-full flex items-center gap-1.5">
              <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse" />
              Gemini Active
            </div>
            <button onClick={startNewChat} className="btn-secondary text-xs py-1.5 px-3 flex items-center gap-1.5">
              <Plus className="w-3.5 h-3.5" /> New Chat
            </button>
          </div>
        </div>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto space-y-4 pr-1">
          {noMessages && (
            <div className="flex flex-col items-center justify-center h-full space-y-6">
              <div className="w-16 h-16 rounded-2xl gradient-bg flex items-center justify-center">
                <Bot className="w-8 h-8 text-white" />
              </div>
              <div className="text-center">
                <h2 className="text-xl font-bold text-gray-900">EduPilot AI Copilot</h2>
                <p className="text-gray-500 text-sm mt-1">Ask me anything about studying abroad</p>
              </div>
              <div className="grid grid-cols-2 gap-3 w-full max-w-lg">
                {SUGGESTIONS.map(({ icon: Icon, text }) => (
                  <button
                    key={text}
                    onClick={() => sendMessage(text)}
                    className="flex items-center gap-2 p-3 rounded-xl border border-gray-200 bg-white text-left hover:border-brand-500 hover:bg-brand-50 transition-all text-sm text-gray-700 hover:text-brand-600"
                  >
                    <Icon className="w-4 h-4 flex-shrink-0 text-brand-400" />
                    {text}
                  </button>
                ))}
              </div>
            </div>
          )}

          {messages.map((msg, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              className={`flex gap-3 ${msg.role === 'user' ? 'flex-row-reverse' : ''}`}
            >
              <div className={clsx(
                'w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0',
                msg.role === 'assistant' ? 'gradient-bg' : 'bg-gray-200'
              )}>
                {msg.role === 'assistant'
                  ? <Bot className="w-4 h-4 text-white" />
                  : <User className="w-4 h-4 text-gray-600" />}
              </div>

              <div className={clsx(
                'max-w-[78%] rounded-2xl px-4 py-3',
                msg.role === 'user'
                  ? 'bg-brand-500 text-white rounded-br-sm'
                  : 'bg-white border border-gray-100 shadow-sm rounded-bl-sm'
              )}>
                {msg.role === 'assistant'
                  ? <MessageContent content={msg.content} />
                  : <p className="text-sm">{msg.content}</p>}

                {msg.role === 'assistant' && (
                  <AgentTrajectory agentsExecuted={msg.agents_used} />
                )}

                <p className={clsx(
                  'text-xs mt-1.5 flex items-center gap-2',
                  msg.role === 'user' ? 'text-white/60' : 'text-gray-400'
                )}>
                  {new Date(msg.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                  {msg.duration_ms && (
                    <span className="flex items-center gap-1">
                      <Clock className="w-3 h-3" />
                      {(msg.duration_ms / 1000).toFixed(1)}s
                    </span>
                  )}
                </p>
              </div>
            </motion.div>
          ))}

          {/* Loading */}
          <AnimatePresence>
            {loading && (
              <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} className="flex gap-3">
                <div className="w-8 h-8 rounded-full gradient-bg flex items-center justify-center">
                  <Bot className="w-4 h-4 text-white" />
                </div>
                <div className="bg-white border border-gray-100 shadow-sm rounded-2xl rounded-bl-sm px-4 py-3 flex items-center gap-3">
                  <Loader2 className="w-4 h-4 animate-spin text-brand-500 flex-shrink-0" />
                  <div>
                    <p className="text-sm text-gray-600">AI agents are thinking...</p>
                    <p className="text-xs text-gray-400 mt-0.5 flex items-center gap-1">
                      <Clock className="w-3 h-3" /> {elapsed}s elapsed · Gemini 3.5 Flash Lite
                    </p>
                  </div>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
          <div ref={bottomRef} />
        </div>

        {/* Input */}
        <div className="pt-4 border-t border-gray-100">
          <form onSubmit={e => { e.preventDefault(); sendMessage() }} className="flex gap-3">
            <input
              value={input}
              onChange={e => setInput(e.target.value)}
              placeholder="Ask about universities, scholarships, budget, timeline..."
              className="flex-1 input"
              disabled={loading}
              aria-label="Chat input"
            />
            <button
              type="submit"
              disabled={loading || !input.trim()}
              className="btn-primary px-4 flex items-center justify-center"
              aria-label="Send"
            >
              {loading ? <Loader2 className="w-5 h-5 animate-spin" /> : <Send className="w-5 h-5" />}
            </button>
          </form>
        </div>
      </div>
    </div>
  )
}
