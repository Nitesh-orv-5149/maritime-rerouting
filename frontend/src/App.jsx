import { useState, useRef, useEffect } from 'react'

function App() {
  const [shipId, setShipId] = useState('Voyager-X')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState('')
  const [logs, setLogs] = useState('')
  const [error, setError] = useState('')
  const logEndRef = useRef(null)

  useEffect(() => {
    if (logEndRef.current) {
      logEndRef.current.scrollIntoView({ behavior: 'smooth' })
    }
  }, [logs])

  const handleAnalyze = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError('')
    setResult('')
    setLogs('')

    try {
      const response = await fetch('http://localhost:8000/api/reroute', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ ship_id: shipId })
      })

      if (!response.ok) {
        throw new Error('Failed to start analysis stream')
      }

      const reader = response.body.getReader()
      const decoder = new TextDecoder()
      let done = false
      let accumulated = ''

      while (!done) {
        const { value, done: doneReading } = await reader.read()
        done = doneReading
        const chunk = decoder.decode(value, { stream: !done })
        accumulated += chunk

        const resultParts = accumulated.split('\n__RESULT__\n')
        if (resultParts.length > 1) {
          setResult(resultParts[1])
          setLogs(resultParts[0])
        } else {
          const errorParts = accumulated.split('\n__ERROR__\n')
          if (errorParts.length > 1) {
            setError(errorParts[1])
            setLogs(errorParts[0])
          } else {
            setLogs(accumulated)
          }
        }
      }
    } catch (err) {
      setError(err.message || 'An error occurred')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={{ maxWidth: '800px', margin: '40px auto', padding: '0 20px', textAlign: 'left' }}>
      <h1>Maritime Supply Chain Rerouter</h1>
      
      <form onSubmit={handleAnalyze} style={{ display: 'flex', gap: '12px', marginBottom: '24px' }}>
        <select 
          value={shipId} 
          onChange={(e) => setShipId(e.target.value)}
          style={{ padding: '8px 12px', fontSize: '16px', borderRadius: '4px', border: '1px solid var(--border)', background: 'var(--bg)', color: 'var(--text-h)' }}
        >
          <option value="Voyager-X">Voyager-X (Delayed)</option>
          <option value="Titan-Liner">Titan-Liner (On Schedule)</option>
        </select>
        
        <button 
          type="submit" 
          disabled={loading}
          style={{ 
            padding: '8px 16px', 
            fontSize: '16px', 
            borderRadius: '4px', 
            border: 'none', 
            background: 'var(--accent)', 
            color: 'white', 
            cursor: loading ? 'not-allowed' : 'pointer',
            opacity: loading ? 0.7 : 1
          }}
        >
          {loading ? 'Analyzing...' : 'Run Rerouting Strategy'}
        </button>
      </form>

      {logs && (
        <div style={{ marginBottom: '24px' }}>
          <h2>Live Terminal Updates</h2>
          <div style={{ 
            padding: '16px', 
            backgroundColor: '#1e1e2e', 
            color: '#a6adc8', 
            borderRadius: '4px', 
            height: '250px', 
            overflowY: 'auto',
            fontFamily: 'var(--mono)',
            fontSize: '13px',
            whiteSpace: 'pre-wrap',
            lineHeight: '1.5'
          }}>
            {logs}
            <div ref={logEndRef} />
          </div>
        </div>
      )}

      {error && (
        <div style={{ padding: '16px', backgroundColor: 'rgba(239, 68, 68, 0.1)', color: '#ef4444', borderRadius: '4px', border: '1px solid rgba(239, 68, 68, 0.3)', marginBottom: '24px' }}>
          <strong>Error:</strong> {error}
        </div>
      )}

      {result && (
        <div style={{ marginTop: '24px' }}>
          <h2>Mitigation & Rerouting Brief</h2>
          <div style={{ 
            padding: '20px', 
            backgroundColor: 'var(--code-bg)', 
            border: '1px solid var(--border)', 
            borderRadius: '4px', 
            whiteSpace: 'pre-wrap',
            fontFamily: 'var(--mono)',
            fontSize: '14px',
            lineHeight: '1.6',
            color: 'var(--text-h)'
          }}>
            {result}
          </div>
        </div>
      )}
    </div>
  )
}

export default App
