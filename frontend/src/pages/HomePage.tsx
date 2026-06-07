import { useEffect, useState } from 'react'
import { Link, useSearchParams } from 'react-router-dom'
import { listProblems, getTrending } from '@/api/client'
import { DifficultyBadge } from '@/components/display/DifficultyBadge'
import type { ProblemMinimal, TrendingConcept } from '@/types'
import styles from './HomePage.module.css'

export function HomePage() {
  const [params] = useSearchParams()
  const category = params.get('category') ?? undefined
  const [problems, setProblems] = useState<ProblemMinimal[]>([])
  const [trending, setTrending] = useState<TrendingConcept[]>([])
  const [total, setTotal] = useState(0)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    setLoading(true)
    Promise.all([
      listProblems({ page: 1, pageSize: 12, category }),
      getTrending(),
    ])
      .then(([list, trends]) => {
        setProblems(list.items)
        setTotal(list.total)
        setTrending(trends)
      })
      .catch(console.error)
      .finally(() => setLoading(false))
  }, [category])

  return (
    <div className={styles.page}>
      <section className={styles.hero}>
        <h1 className={styles.heroTitle}>
          BEE is a backend engineering encyclopidia
        </h1>
        <p className={styles.heroSub}>
          Search-first knowledge for performance, scalability, reliability, and
          everything in between. Press <kbd>⌘K</kbd> to explore.
        </p>
        <div className={styles.stats}>
          <span>{total} articles</span>
          <span>·</span>
          <span>10 categories</span>
        </div>
      </section>

      {trending.length > 0 && (
        <section className={styles.section}>
          <h2 className={styles.sectionTitle}>Trending</h2>
          <div className={styles.trendingRow}>
            {trending.slice(0, 5).map((t) => (
              <Link key={t.problem_id} to={`/problems/${t.slug}`} className={styles.trendCard}>
                <span className={styles.trendCat}>{t.category}</span>
                <span className={styles.trendTitle}>{t.title}</span>
              </Link>
            ))}
          </div>
        </section>
      )}

      <section className={styles.section}>
        <h2 className={styles.sectionTitle}>
          {category ? `${category} Articles` : 'All Articles'}
        </h2>
        {loading ? (
          <p className={styles.loading}>Loading…</p>
        ) : (
          <div className={styles.grid}>
            {problems.map((p) => (
              <Link key={p.id} to={`/problems/${p.slug}`} className={styles.card}>
                <div className={styles.cardTop}>
                  <span className={styles.cat}>{p.category}</span>
                  <DifficultyBadge difficulty={p.difficulty} />
                </div>
                <h3 className={styles.cardTitle}>{p.title}</h3>
                <p className={styles.cardDesc}>{p.explanation}</p>
                {p.algorithm && (
                  <span className={styles.algo}>{p.algorithm}</span>
                )}
              </Link>
            ))}
          </div>
        )}
      </section>
    </div>
  )
}
