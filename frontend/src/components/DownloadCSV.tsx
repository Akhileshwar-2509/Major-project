import React from 'react'
import axios from 'axios'

type Props = { apiBase: string, crop: string, pred: any, rec: any, opt: any }

export default function DownloadCSV({ apiBase, crop, pred, rec, opt }: Props) {
  async function download() {
    const cover_recs = (rec?.recommendations || []).map((r:any)=> `${r.name}: ${r.score}`)
    const fert = (opt?.schedule || []).map((d:any)=> `${d.time}: N ${d.n}, P ${d.p}, K ${d.k}`)
    const res = await axios.post(`${apiBase}/export/csv`, {
      crop,
      predicted_yield_per_acre: pred?.predicted_yield_per_acre || 0,
      ci_low: pred?.lower_ci || 0,
      ci_high: pred?.upper_ci || 0,
      cover_recs: cover_recs,
      fertilizer_schedule: fert,
    }, { responseType: 'blob' })
    const url = window.URL.createObjectURL(new Blob([res.data]))
    const a = document.createElement('a')
    a.href = url
    a.download = 'advisory.csv'
    a.click()
    window.URL.revokeObjectURL(url)
  }
  return (
    <button onClick={download} className="px-3 py-2 bg-indigo-600 text-white rounded">Download CSV</button>
  )
}

