export interface Complexity {
  time?: string | null
  space?: string | null
}

export interface ProblemMinimal {
  id: string
  slug: string
  title: string
  category: string
  algorithm?: string | null
  difficulty: string
  explanation: string
  tags: string[]
}

export interface ProblemDetail extends ProblemMinimal {
  markdown_content: string
  technologies: string[]
  complexity?: Complexity | null
  created_at: string
}

export interface ProblemList {
  items: ProblemMinimal[]
  total: number
  page: number
  page_size: number
}

export interface SearchResult extends ProblemMinimal {
  score: number
}

export interface Suggestion {
  slug: string
  title: string
  category: string
}

export interface GraphNode {
  id: string
  slug: string
  title: string
  category: string
  difficulty: string
}

export interface GraphEdge {
  source_id: string
  target_id: string
  relationship_type: string
  strength: number
}

export interface GraphResponse {
  root_id: string
  nodes: GraphNode[]
  edges: GraphEdge[]
}

export interface TrendingConcept {
  problem_id: string
  slug: string
  title: string
  category: string
  view_count: number
}

export const CATEGORIES = [
  'API',
  'Concurrency',
  'Data',
  'DevOps',
  'Networking',
  'Observability',
  'Performance',
  'Reliability',
  'Scalability',
  'Security',
] as const
