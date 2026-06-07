import { useEffect, useState } from 'react'
import { Link, useSearchParams } from 'react-router-dom'
import { searchProblems } from '@/api/client'
import { DifficultyBadge } from '@/components/display/DifficultyBadge'
import { useDebounce } from '@/hooks/useDebounce'
import type { SearchResult } from '@/types'
import styles from './SearchPage.module.css'

export function SearchPage() {
  const [params, setParams] = useSearchParams()
  const q = params.get('q') ?? ''
  const [input, setInput] = useState(q)
  const debounced = useDebounce(input, 300)
  const [results, setResults] = useState<SearchResult[]>([])
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    if (debounced.length < 1) {
      setResults([])
      return
    }
    setParams({ q: debounced })
    setLoading(true)
    searchProblems(debounced)
      .then(setResults)
      .catch(console.error)
      .finally(() => setLoading(false))
  }, [debounced, setParams])

  return (
    <div className={styles.page}>
      <h1 className={styles.title}>Search</h1>
      <input
        className={styles.input}
        placeholder="Query the encyclopedia…"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        autoFocus
      />
      {loading && <p className={styles.meta}>Searching…</p>}
      {!loading && debounced && (
        <p className={styles.meta}>{results.length} results for "{debounced}"</p>
      )}
      <ul className={styles.list}>
        {results.map((r) => (
          <li key={r.id}>
            <Link to={`/problems/${r.slug}`} className={styles.result}>
              <div className={styles.resultTop}>
                <span className={styles.cat}>{r.category}</span>
                <DifficultyBadge difficulty={r.difficulty} />
              </div>
              <h2 className={styles.resultTitle}>{r.title}</h2>
              <p className={styles.resultDesc}>{r.explanation}</p>
            </Link>
          </li>
        ))}
      </ul>
    </div>
  )
}
