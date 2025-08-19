import React from 'react'

type YieldProps = { value: number, low: number, high: number }

export function YieldBar({ value, low, high }: YieldProps) {
  const width = 260
  const min = 0
  const max = Math.max(high * 1.1, value * 1.2, 10)
  const scale = (x:number) => Math.max(0, Math.min(width, (x-min)/(max-min) * width))
  return (
    <svg width={width} height={36} className="overflow-visible">
      <rect x={0} y={12} width={width} height={12} fill="#e5e7eb" rx={6} />
      <rect x={0} y={12} width={scale(value)} height={12} fill="#16a34a" rx={6} />
      <line x1={scale(low)} x2={scale(high)} y1={18} y2={18} stroke="#111827" strokeWidth={2} />
      <circle cx={scale(low)} cy={18} r={3} fill="#111827" />
      <circle cx={scale(high)} cy={18} r={3} fill="#111827" />
      <text x={scale(value)+6} y={10} fontSize={10} fill="#111827">{value.toFixed(1)} bu/ac</text>
    </svg>
  )
}

type GaugeProps = { score: number }
export function SuppressionGauge({ score }: GaugeProps) {
  const pct = Math.max(0, Math.min(100, score))
  return (
    <div className="w-64">
      <div className="w-full bg-gray-200 h-3 rounded">
        <div className="h-3 rounded bg-indigo-600" style={{ width: `${pct}%` }}></div>
      </div>
      <div className="text-xs text-gray-600 mt-1">Weed suppression: {pct}%</div>
    </div>
  )
}

