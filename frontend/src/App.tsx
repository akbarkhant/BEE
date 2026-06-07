import { BrowserRouter, Route, Routes } from 'react-router-dom'
import { AppShell } from '@/components/layout/AppShell'
import { GraphExplorerPage } from '@/pages/GraphExplorerPage'
import { HomePage } from '@/pages/HomePage'
import { ProblemDetailPage } from '@/pages/ProblemDetailPage'
import { SearchPage } from '@/pages/SearchPage'

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<AppShell />}>
          <Route index element={<HomePage />} />
          <Route path="search" element={<SearchPage />} />
          <Route path="problems/:slug" element={<ProblemDetailPage />} />
          <Route path="graph" element={<GraphExplorerPage />} />
          <Route path="graph/:problemId" element={<GraphExplorerPage />} />
        </Route>
      </Routes>
    </BrowserRouter>
  )
}
