import axios from 'axios'
import type {
  GraphResponse,
  ProblemDetail,
  ProblemList,
  ProblemMinimal,
  SearchResult,
  Suggestion,
  TrendingConcept,
} from '@/types'

const API_BASE = import.meta.env.VITE_API_URL ?? '/api/v1'

export const api = axios.create({
  baseURL: API_BASE,
  timeout: 15000,
  headers: { Accept: 'application/json' },
})

export async function listProblems(params?: {
  page?: number
  pageSize?: number
  category?: string
  difficulty?: string
}): Promise<ProblemList> {
  const { data } = await api.get<ProblemList>('/problems', { params })
  return data
}

export async function getProblem(slug: string): Promise<ProblemDetail> {
  const { data } = await api.get<ProblemDetail>(`/problems/${slug}`)
  return data
}

export async function searchProblems(
  q: string,
  filters?: { category?: string; difficulty?: string; tags?: string[] },
): Promise<SearchResult[]> {
  const { data } = await api.get<SearchResult[]>('/search', {
    params: { q, ...filters },
  })
  return data
}

export async function getSuggestions(q: string): Promise<Suggestion[]> {
  const { data } = await api.get<Suggestion[]>('/search/suggestions', { params: { q } })
  return data
}

export async function getGraph(problemId: string, depth = 2): Promise<GraphResponse> {
  const { data } = await api.get<GraphResponse>(`/graph/${problemId}`, { params: { depth } })
  return data
}

export async function getClusterGraph(category: string): Promise<GraphResponse> {
  const { data } = await api.get<GraphResponse>(`/graph/cluster/${category}`)
  return {
    root_id: '',
    nodes: data.nodes,
    edges: data.edges,
  }
}

export async function getTrending(): Promise<TrendingConcept[]> {
  const { data } = await api.get<TrendingConcept[]>('/trending')
  return data
}

export async function getRecommendations(problemId: string): Promise<ProblemMinimal[]> {
  const { data } = await api.get<ProblemMinimal[]>(`/recommendations/${problemId}`)
  return data
}
