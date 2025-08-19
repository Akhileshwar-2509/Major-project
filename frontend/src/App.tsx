import React, { useState } from 'react'
import axios from 'axios'
import { YieldBar, SuppressionGauge } from './components/Charts'
import DownloadCSV from './components/DownloadCSV'

type Soil = { n: number; p: number; k: number; ph: number; organic_matter: number; ec: number; texture: string }

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000'

export default function App() {
  const [soil, setSoil] = useState<Soil>({ n: 100, p: 20, k: 60, ph: 6.5, organic_matter: 2.0, ec: 0.3, texture: 'loam' })
  const [crop, setCrop] = useState('maize')
  const [covers, setCovers] = useState<string>('rye,mustard')
  const [weeds, setWeeds] = useState<string>('amaranthus')
  const [location, setLocation] = useState('Ames, IA')
  const [season, setSeason] = useState('kharif')

  const [yieldResult, setYieldResult] = useState<any>(null)
  const [recResult, setRecResult] = useState<any>(null)
  const [classResult, setClassResult] = useState<any>(null)
  const [optResult, setOptResult] = useState<any>(null)
  const [whyResult, setWhyResult] = useState<any>(null)

  async function runAll() {
    const coverList = covers.split(',').map(s => s.trim()).filter(Boolean)
    const weedList = weeds.split(',').map(s => s.trim()).filter(Boolean)

    const [pred, rec, cls, opt, why] = await Promise.all([
      axios.post(`${API_BASE}/predict/yield`, { soil, crop, candidate_cover_crops: coverList, weed_species: weedList, location, season }).then(r => r.data),
      axios.post(`${API_BASE}/recommend/cover`, { crop, soil_texture: soil.texture, weed_species: weedList, candidates: coverList }).then(r => r.data),
      axios.post(`${API_BASE}/classify/weed`, { weeds: weedList, crop }).then(r => r.data),
      axios.post(`${API_BASE}/optimize/fertilizer`, { crop, n: soil.n, p: soil.p, k: soil.k, season }).then(r => r.data),
      axios.post(`${API_BASE}/explain/why`, { crop, cover_crops: coverList, weeds: weedList }).then(r => r.data),
    ])
    setYieldResult(pred)
    setRecResult(rec)
    setClassResult(cls)
    setOptResult(opt)
    setWhyResult(why)
  }

  return (
    <div className="max-w-6xl mx-auto p-6">
      <h1 className="text-2xl font-semibold mb-4">Allelopathy Advisor</h1>
      <div className="grid md:grid-cols-2 gap-6">
        <div className="bg-white shadow p-4 rounded">
          <h2 className="font-semibold mb-2">Inputs</h2>
          <div className="grid grid-cols-2 gap-2 text-sm">
            <label className="col-span-1">Crop
              <input value={crop} onChange={e=>setCrop(e.target.value)} className="w-full border rounded p-1" />
            </label>
            <label className="col-span-1">Texture
              <input value={soil.texture} onChange={e=>setSoil({...soil, texture: e.target.value})} className="w-full border rounded p-1" />
            </label>
            {([['N','n'],['P','p'],['K','k'],['pH','ph'],['OM','organic_matter'],['EC','ec']] as [string, keyof Soil][]) .map(([lab,key]) => (
              <label key={key as string} className="col-span-1">{lab}
                <input type="number" value={soil[key] as number}
                  onChange={e=>setSoil({...soil, [key]: Number(e.target.value)})}
                  className="w-full border rounded p-1" />
              </label>
            ))}
            <label className="col-span-2">Candidate cover crops (comma-separated)
              <input value={covers} onChange={e=>setCovers(e.target.value)} className="w-full border rounded p-1" />
            </label>
            <label className="col-span-2">Weeds (comma-separated)
              <input value={weeds} onChange={e=>setWeeds(e.target.value)} className="w-full border rounded p-1" />
            </label>
            <label className="col-span-1">Location
              <input value={location} onChange={e=>setLocation(e.target.value)} className="w-full border rounded p-1" />
            </label>
            <label className="col-span-1">Season
              <input value={season} onChange={e=>setSeason(e.target.value)} className="w-full border rounded p-1" />
            </label>
          </div>
          <div className="flex gap-2 mt-3">
            <button onClick={runAll} className="px-3 py-2 bg-green-600 text-white rounded">Run</button>
            <DownloadCSV apiBase={API_BASE} crop={crop} pred={yieldResult} rec={recResult} opt={optResult} />
          </div>
        </div>

        <div className="space-y-4">
          <div className="bg-white shadow p-4 rounded">
            <h2 className="font-semibold mb-2">Predicted yield</h2>
            {yieldResult && (
              <div className="text-sm">
                <YieldBar value={yieldResult.predicted_yield_per_acre} low={yieldResult.lower_ci} high={yieldResult.upper_ci} />
              </div>
            )}
          </div>
          <div className="bg-white shadow p-4 rounded">
            <h2 className="font-semibold mb-2">Cover crop recommendations</h2>
            <ul className="text-sm list-disc pl-5">
              {recResult?.recommendations?.map((r:any)=> (
                <li key={r.name}>{r.name} — score {r.score}
                  <ul className="list-disc pl-5 text-gray-600">
                    {r.reasons.map((x:string,i:number)=>(<li key={i}>{x}</li>))}
                  </ul>
                </li>
              ))}
            </ul>
          </div>
          <div className="bg-white shadow p-4 rounded">
            <h2 className="font-semibold mb-2">Weed classification</h2>
            <ul className="text-sm list-disc pl-5">
              {classResult?.weeds?.map((w:any)=> (
                <li key={w.name}>{w.name}: {w.label} — {w.explanation}</li>
              ))}
            </ul>
            {recResult?.recommendations?.length ? (
              <div className="mt-2">
                <SuppressionGauge score={Math.min(100, Math.max(0, Math.round((recResult.recommendations[0].score - 50) * 2)))} />
              </div>
            ) : null}
          </div>
          <div className="bg-white shadow p-4 rounded">
            <h2 className="font-semibold mb-2">NPK schedule</h2>
            <ol className="text-sm list-decimal pl-5">
              {optResult?.schedule?.map((d:any)=> (
                <li key={d.time}>{d.time}: N {d.n}, P {d.p}, K {d.k} — {d.note}</li>
              ))}
            </ol>
          </div>
          <div className="bg-white shadow p-4 rounded">
            <h2 className="font-semibold mb-2">Explain why</h2>
            <ul className="text-sm list-disc pl-5">
              {whyResult?.narrative?.map((x:string,i:number)=> (<li key={i}>{x}</li>))}
            </ul>
          </div>
        </div>
      </div>
    </div>
  )
}

