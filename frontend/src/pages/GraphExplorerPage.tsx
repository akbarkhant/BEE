import { useCallback, useEffect, useState, type MouseEvent } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import {
  ReactFlow,
  Background,
  Controls,
  MiniMap,
  useNodesState,
  useEdgesState,
  type Node,
  type Edge,
} from '@xyflow/react'
import '@xyflow/react/dist/style.css'
import { getClusterGraph, getGraph } from '@/api/client'
import { CATEGORIES } from '@/types'
import styles from './GraphExplorerPage.module.css'

export function GraphExplorerPage() {
  const { problemId } = useParams<{ problemId?: string }>()
  const [category, setCategory] = useState('Performance')
  const [nodes, setNodes, onNodesChange] = useNodesState<Node>([])
  const [edges, setEdges, onEdgesChange] = useEdgesState<Edge>([])
  const [loading, setLoading] = useState(true)
  const navigate = useNavigate()

  const loadGraph = useCallback(async () => {
    setLoading(true)
    try {
      const data = problemId
        ? await getGraph(problemId, 2)
        : await getClusterGraph(category)

      const flowNodes: Node[] = data.nodes.map((n, i) => ({
        id: n.id,
        position: { x: (i % 6) * 220, y: Math.floor(i / 6) * 120 },
        data: { label: n.title },
        style: {
          background: '#201f22',
          color: '#e5e1e4',
          border: '1px solid #464554',
          borderRadius: 4,
          fontSize: 12,
          padding: 8,
          maxWidth: 180,
        },
      }))

      const flowEdges: Edge[] = data.edges.map((e) => ({
        id: `${e.source_id}-${e.target_id}`,
        source: e.source_id,
        target: e.target_id,
        label: e.relationship_type,
        style: { stroke: '#8083ff' },
        labelStyle: { fill: '#c7c4d7', fontSize: 10 },
      }))

      setNodes(flowNodes)
      setEdges(flowEdges)
    } catch (err) {
      console.error(err)
      setNodes([])
      setEdges([])
    } finally {
      setLoading(false)
    }
  }, [problemId, category, setNodes, setEdges])

  useEffect(() => {
    loadGraph()
  }, [loadGraph])

  const onNodeClick = (_: MouseEvent, node: Node) => {
    navigate(`/graph/${node.id}`)
  }

  return (
    <div className={styles.page}>
      <div className={styles.toolbar}>
        <h1 className={styles.title}>Graph Explorer</h1>
        {!problemId && (
          <select
            className={styles.select}
            value={category}
            onChange={(e) => setCategory(e.target.value)}
          >
            {CATEGORIES.map((c) => (
              <option key={c} value={c}>{c}</option>
            ))}
          </select>
        )}
        {problemId && (
          <button type="button" className={styles.btn} onClick={() => navigate('/graph')}>
            View all clusters
          </button>
        )}
      </div>
      <div className={styles.canvas}>
        {loading ? (
          <p className={styles.loading}>Loading graph…</p>
        ) : nodes.length === 0 ? (
          <p className={styles.loading}>No nodes to display.</p>
        ) : (
          <ReactFlow
            nodes={nodes}
            edges={edges}
            onNodesChange={onNodesChange}
            onEdgesChange={onEdgesChange}
            onNodeClick={onNodeClick}
            fitView
            colorMode="dark"
          >
            <Background color="#27272a" gap={20} />
            <Controls />
            <MiniMap nodeColor="#353437" maskColor="rgba(9,9,11,0.8)" />
          </ReactFlow>
        )}
      </div>
    </div>
  )
}
