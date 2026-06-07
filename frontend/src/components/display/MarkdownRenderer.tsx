import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import styles from './MarkdownRenderer.module.css'

export function MarkdownRenderer({ content }: { content: string }) {
  return (
    <article className={styles.article}>
      <ReactMarkdown remarkPlugins={[remarkGfm]}>{content}</ReactMarkdown>
    </article>
  )
}
