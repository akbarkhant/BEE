import { Link, useSearchParams } from 'react-router-dom'
import { CATEGORIES } from '@/types'
import styles from './Sidebar.module.css'

export function Sidebar() {
  const [params] = useSearchParams()
  const activeCategory = params.get('category')

  return (
    <aside className={styles.sidebar}>
      <p className={styles.label}>Categories</p>
      <ul className={styles.list}>
        <li>
          <Link
            to="/"
            className={!activeCategory ? styles.active : styles.item}
          >
            All
          </Link>
        </li>
        {CATEGORIES.map((cat) => (
          <li key={cat}>
            <Link
              to={`/?category=${encodeURIComponent(cat)}`}
              className={activeCategory === cat ? styles.active : styles.item}
            >
              {cat}
            </Link>
          </li>
        ))}
      </ul>
    </aside>
  )
}
