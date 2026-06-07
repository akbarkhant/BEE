import { Link, useLocation } from 'react-router-dom'
import { useUiStore } from '@/stores/uiStore'
import styles from './Header.module.css'

export function Header() {
  const location = useLocation()
  const toggleCommandPalette = useUiStore((s) => s.toggleCommandPalette)

  return (
    <header className={styles.header}>
      <div className={styles.left}>
        <Link to="/" className={styles.brand}>
          BEE
        </Link>
        <nav className={styles.nav}>
          <Link
            to="/"
            className={location.pathname === '/' ? styles.active : styles.link}
          >
            Home
          </Link>
          <Link
            to="/search"
            className={location.pathname.startsWith('/search') ? styles.active : styles.link}
          >
            Search
          </Link>
          <Link
            to="/graph"
            className={location.pathname.startsWith('/graph') ? styles.active : styles.link}
          >
            Graph
          </Link>
        </nav>
      </div>
      <div className={styles.actions}>
        <button type="button" className={styles.cmdBtn} onClick={toggleCommandPalette}>
          <span>Search</span>
          <kbd>⌘K</kbd>
        </button>
      </div>
    </header>
  )
}
