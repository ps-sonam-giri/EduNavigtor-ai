import { useState } from 'react'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'
import { Calculator, DollarSign, TrendingDown, Info } from 'lucide-react'
import { motion } from 'framer-motion'

const COUNTRIES_DATA = [
  { country: 'USA',       tuition: 35000, living: 18000, visa: 185, insurance: 1200 },
  { country: 'UK',        tuition: 25000, living: 14400, visa: 490, insurance: 470  },
  { country: 'Canada',    tuition: 22000, living: 13200, visa: 150, insurance: 600  },
  { country: 'Australia', tuition: 28000, living: 15600, visa: 620, insurance: 500  },
  { country: 'Germany',   tuition: 500,   living: 10800, visa: 75,  insurance: 100  },
  { country: 'Ireland',   tuition: 18000, living: 13200, visa: 100, insurance: 500  },
]

const USD_TO_INR = 83

export default function BudgetPage() {
  const [selectedCountry, setSelectedCountry] = useState('Canada')
  const [duration, setDuration] = useState(2)
  const [scholarship, setScholarship] = useState(0)

  const data = COUNTRIES_DATA.find((c) => c.country === selectedCountry) || COUNTRIES_DATA[0]
  const yearlyTotal = data.tuition + data.living + data.visa + data.insurance + 2000
  const totalCost = (yearlyTotal * duration) - (scholarship * 1000)
  const totalINR = totalCost * USD_TO_INR

  const chartData = COUNTRIES_DATA.map((c) => ({
    country: c.country,
    Tuition: c.tuition,
    Living: c.living,
    'Visa & Insurance': c.visa + c.insurance,
    Misc: 2000,
  }))

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Budget Calculator</h1>
        <p className="text-gray-500 text-sm">Estimate your total study abroad cost</p>
      </div>

      {/* Calculator */}
      <div className="grid md:grid-cols-2 gap-6">
        <div className="card space-y-5">
          <h2 className="font-semibold text-gray-900 flex items-center gap-2">
            <Calculator className="w-5 h-5 text-brand-500" /> Customise Estimate
          </h2>

          <div>
            <label className="label">Destination Country</label>
            <select value={selectedCountry} onChange={(e) => setSelectedCountry(e.target.value)} className="input">
              {COUNTRIES_DATA.map((c) => <option key={c.country}>{c.country}</option>)}
            </select>
          </div>

          <div>
            <label className="label">Program Duration</label>
            <div className="flex gap-2">
              {[1, 1.5, 2, 3].map((y) => (
                <button
                  key={y}
                  onClick={() => setDuration(y)}
                  className={`flex-1 py-2 rounded-xl text-sm font-medium border transition-all ${
                    duration === y ? 'bg-brand-500 text-white border-brand-500' : 'border-gray-200 text-gray-600 hover:border-brand-500'
                  }`}
                >
                  {y} yr{y !== 1 ? 's' : ''}
                </button>
              ))}
            </div>
          </div>

          <div>
            <label className="label">Scholarship Amount (×$1,000 USD)</label>
            <input
              type="range" min={0} max={50} value={scholarship}
              onChange={(e) => setScholarship(Number(e.target.value))}
              className="w-full accent-brand-500"
            />
            <div className="flex justify-between text-xs text-gray-400 mt-1">
              <span>$0</span>
              <span className="font-semibold text-brand-500">${scholarship},000</span>
              <span>$50,000</span>
            </div>
          </div>
        </div>

        {/* Summary */}
        <div className="card">
          <h2 className="font-semibold text-gray-900 mb-5 flex items-center gap-2">
            <DollarSign className="w-5 h-5 text-green-500" /> Cost Breakdown – {selectedCountry}
          </h2>
          <div className="space-y-3">
            {[
              { label: 'Tuition', value: data.tuition, yearly: true },
              { label: 'Living Cost', value: data.living, yearly: true },
              { label: 'Visa Fee', value: data.visa, yearly: false },
              { label: 'Health Insurance', value: data.insurance, yearly: true },
              { label: 'Miscellaneous', value: 2000, yearly: true },
            ].map(({ label, value, yearly }) => (
              <div key={label} className="flex justify-between items-center py-2 border-b border-gray-50 last:border-0">
                <span className="text-sm text-gray-600">{label} {yearly ? '(per year)' : ''}</span>
                <span className="font-medium">${Number(value).toLocaleString()}</span>
              </div>
            ))}
            {scholarship > 0 && (
              <div className="flex justify-between items-center py-2 text-green-600">
                <span className="text-sm font-medium flex items-center gap-1">
                  <TrendingDown className="w-4 h-4" /> Scholarship Saving
                </span>
                <span className="font-semibold">-${(scholarship * 1000).toLocaleString()}</span>
              </div>
            )}
          </div>

          <div className="mt-5 p-4 gradient-bg rounded-xl text-white">
            <p className="text-sm text-white/80">Total for {duration} year{duration !== 1 ? 's' : ''}</p>
            <p className="text-3xl font-bold mt-1">${totalCost.toLocaleString()}</p>
            <p className="text-sm text-white/80 mt-1">≈ ₹{(totalINR / 100000).toFixed(1)} Lakhs</p>
          </div>
        </div>
      </div>

      {/* Comparison chart */}
      <div className="card">
        <h2 className="font-semibold text-gray-900 mb-5 flex items-center gap-2">
          <Info className="w-5 h-5 text-brand-500" /> Annual Cost Comparison (USD)
        </h2>
        <ResponsiveContainer width="100%" height={320}>
          <BarChart data={chartData} margin={{ top: 5, right: 20, left: 0, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
            <XAxis dataKey="country" tick={{ fontSize: 12 }} />
            <YAxis tick={{ fontSize: 12 }} tickFormatter={(v) => `$${(v / 1000).toFixed(0)}k`} />
            <Tooltip formatter={(v: number) => [`$${v.toLocaleString()}`, '']} />
            <Legend />
            <Bar dataKey="Tuition" stackId="a" fill="#667eea" radius={[0, 0, 0, 0]} />
            <Bar dataKey="Living" stackId="a" fill="#764ba2" />
            <Bar dataKey="Visa & Insurance" stackId="a" fill="#f59e0b" />
            <Bar dataKey="Misc" stackId="a" fill="#e5e7eb" radius={[4, 4, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  )
}
