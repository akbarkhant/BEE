import styles from './DifficultyBadge.module.css'

const MAP: Record<string, string> = {
  Easy: 'easy',
  Medium: 'medium',
  Hard: 'hard',
  beginner: 'easy',
  intermediate: 'medium',
  advanced: 'hard',
}

export function DifficultyBadge({ difficulty }: { difficulty: string }) {
  const level = MAP[difficulty] ?? 'medium'
  return (
    <span className={`${styles.badge} ${styles[level]}`}>
      {difficulty}
    </span>
  )
}
