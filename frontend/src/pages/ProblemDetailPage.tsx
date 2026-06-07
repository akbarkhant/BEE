import { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { getProblem, getRecommendations } from '@/api/client'
import { DifficultyBadge } from '@/components/display/DifficultyBadge'
import { MarkdownRenderer } from '@/components/display/MarkdownRenderer'
import type { ProblemDetail, ProblemMinimal } from '@/types'
import styles from './ProblemDetailPage.module.css'

export function ProblemDetailPage() {
  const { slug } = useParams<{ slug: string }>()
  const [problem, setProblem] = useState<ProblemDetail | null>(null)
  const [related, setRelated] = useState<ProblemMinimal[]>([])
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (!slug) return
    setError(null)
    getProblem(slug)
      .then((p) => {
        setProblem(p)
        return getRecommendations(p.id)
      })
      .then(setRelated)
      .catch(() => setError('Article not found.'))
  }, [slug])

  if (error) {
    return <p className={styles.error}>{error}</p>
  }

  if (!problem) {
    return <p className={styles.loading}>Loading article…</p>
  }

  return (
    <div className={styles.layout}>
      <article className={styles.content}>
        <header className={styles.header}>
          <div className={styles.meta}>
            <span className={styles.cat}>{problem.category}</span>
            <DifficultyBadge difficulty={problem.difficulty} />
          </div>
          <h1 className={styles.title}>{problem.title}</h1>
          {problem.algorithm && (
            <p className={styles.algo}>{problem.algorithm}</p>
          )}
          <p className={styles.summary}>{problem.explanation}</p>
          <Link to={`/graph/${problem.id}`} className={styles.graphLink}>
            View in Graph Explorer →
          </Link>
        </header>
        <MarkdownRenderer content={problem.markdown_content} />
      </article>

      <aside className={styles.sidebar}>
        {problem.technologies.length > 0 && (
          <div className={styles.panel}>
            <h3 className={styles.panelTitle}>Technologies</h3>
            <div className={styles.tags}>
              {problem.technologies.map((t) => (
                <span key={t} className={styles.tag}>{t}</span>
              ))}
            </div>
          </div>
        )}
        {problem.complexity && (
          <div className={styles.panel}>
            <h3 className={styles.panelTitle}>Complexity</h3>
            <dl className={styles.dl}>
              <dt>Time</dt>
              <dd>{problem.complexity.time ?? '—'}</dd>
              <dt>Space</dt>
              <dd>{problem.complexity.space ?? '—'}</dd>
            </dl>
          </div>
        )}
        {related.length > 0 && (
          <div className={styles.panel}>
            <h3 className={styles.panelTitle}>Related</h3>
            <ul className={styles.related}>
              {related.map((r) => (
                <li key={r.id}>
                  <Link to={`/problems/${r.slug}`}>{r.title}</Link>
                </li>
              ))}
            </ul>
          </div>
        )}
      </aside>
    </div>
  )
}
