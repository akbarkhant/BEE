import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { getSuggestions } from '@/api/client'
import { useDebounce } from '@/hooks/useDebounce'
import { useUiStore } from '@/stores/uiStore'
import type { Suggestion } from '@/types'
import styles from './CommandPalette.module.css'

export function CommandPalette() {
  const open = useUiStore((s) => s.commandPaletteOpen)
  const setOpen = useUiStore((s) => s.setCommandPaletteOpen)
  const [query, setQuery] = useState('')
  const [suggestions, setSuggestions] = useState<Suggestion[]>([])
  const debounced = useDebounce(query, 250)
  const navigate = useNavigate()

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault()
        useUiStore.getState().toggleCommandPalette()
      }
      if (e.key === 'Escape') setOpen(false)
    }
    window.addEventListener('keydown', onKey)
    return () => window.removeEventListener('keydown', onKey)
  }, [setOpen])

  useEffect(() => {
    if (!open) {
      setQuery('')
      setSuggestions([])
      return
    }
    if (debounced.length < 1) {
      setSuggestions([])
      return
    }
    getSuggestions(debounced)
      .then(setSuggestions)
      .catch(() => setSuggestions([]))
  }, [debounced, open])

  if (!open) return null

  const select = (slug: string) => {
    setOpen(false)
    navigate(`/problems/${slug}`)
  }

  return (
    <div className={styles.overlay} onClick={() => setOpen(false)}>
      <div className={styles.panel} onClick={(e) => e.stopPropagation()}>
        <input
          autoFocus
          className={styles.input}
          placeholder="Search backend engineering concepts…"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === 'Enter' && suggestions[0]) select(suggestions[0].slug)
          }}
        />
        <ul className={styles.results}>
          {suggestions.map((s) => (
            <li key={s.slug}>
              <button type="button" className={styles.result} onClick={() => select(s.slug)}>
                <span className={styles.title}>{s.title}</span>
                <span className={styles.meta}>{s.category}</span>
              </button>
            </li>
          ))}
          {query && suggestions.length === 0 && (
            <li className={styles.empty}>No matches for "{query}"</li>
          )}
        </ul>
      </div>
    </div>
  )
}
