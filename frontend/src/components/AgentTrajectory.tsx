import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Brain, Wrench, CheckCircle2, AlertTriangle, ChevronDown, ChevronUp } from 'lucide-react'

interface TrajectoryProps {
  agentsExecuted?: string[]
  reasoning?: string
  verifierPassed?: boolean
  verifierCritique?: string
}

export default function AgentTrajectory({
  agentsExecuted = [],
  reasoning,
  verifierPassed = true,
  verifierCritique,
}: TrajectoryProps) {
  const [isOpen, setIsOpen] = useState(false)

  if (!agentsExecuted.length && !reasoning) return null

  return (
    <div className="my-2 border border-brand-100 rounded-xl bg-brand-50/40 overflow-hidden text-xs">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="w-full flex items-center justify-between px-3 py-2 bg-brand-50 hover:bg-brand-100/60 transition-colors text-brand-700 font-medium"
      >
        <div className="flex items-center gap-2">
          <Brain className="w-4 h-4 text-brand-600" />
          <span>Agent Thought Trajectory ({agentsExecuted.length} Turns)</span>
          {verifierPassed ? (
            <span className="flex items-center gap-1 text-[10px] px-2 py-0.5 rounded-full bg-emerald-100 text-emerald-700 font-semibold">
              <CheckCircle2 className="w-3 h-3" /> Verified
            </span>
          ) : (
            <span className="flex items-center gap-1 text-[10px] px-2 py-0.5 rounded-full bg-amber-100 text-amber-700 font-semibold">
              <AlertTriangle className="w-3 h-3" /> Critique Flagged
            </span>
          )}
        </div>
        {isOpen ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
      </button>

      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            className="p-3 space-y-2 text-gray-700 border-t border-brand-100 bg-white"
          >
            {reasoning && (
              <div>
                <span className="font-semibold text-brand-600 flex items-center gap-1">
                  <Brain className="w-3.5 h-3.5" /> ReAct Reasoning:
                </span>
                <p className="mt-0.5 text-gray-600 italic pl-4 border-l-2 border-brand-300">{reasoning}</p>
              </div>
            )}

            {agentsExecuted.length > 0 && (
              <div>
                <span className="font-semibold text-gray-600 flex items-center gap-1">
                  <Wrench className="w-3.5 h-3.5" /> Turns & Tools Executed:
                </span>
                <div className="flex flex-wrap gap-1.5 mt-1">
                  {agentsExecuted.map((step, idx) => (
                    <span
                      key={idx}
                      className="px-2 py-0.5 rounded bg-gray-100 text-gray-600 font-mono text-[11px] border border-gray-200"
                    >
                      {step}
                    </span>
                  ))}
                </div>
              </div>
            )}

            {verifierCritique && (
              <div className="mt-2 p-2 rounded bg-amber-50 border border-amber-200 text-amber-800 text-[11px]">
                <span className="font-semibold flex items-center gap-1 text-amber-900">
                  <AlertTriangle className="w-3.5 h-3.5" /> Verifier Pass Feedback:
                </span>
                <pre className="mt-1 whitespace-pre-wrap font-sans">{verifierCritique}</pre>
              </div>
            )}
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}
