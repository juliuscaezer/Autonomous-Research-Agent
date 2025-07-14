import { useState } from 'react'
import axios from 'axios'
import ResultCard from './components/ResultCard.jsx'
import './App.css'

function App() {
  const [query, setQuery] = useState('')
  const [results, setResults] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleSearch = async () => {
    if (!query.trim()) return
    setLoading(true)
    setError(null)

    try {
      const response = await axios.get(`http://localhost:8000/research`, {
        params: { query }
      })
      setResults(response.data.results)
    } catch (err) {
      console.error(err)
      setError('Failed to fetch results.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app-container">
      <h1>Autonomous Research Agent</h1>
      <div className="search-box">
        <input
          type="text"
          placeholder="Enter research topic (e.g., AI in finance)"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
        <button onClick={handleSearch} disabled={loading}>
          {loading ? 'Searching...' : 'Search'}
        </button>
      </div>

      {error && <p className="error">{error}</p>}

      <div className="results">
        {results.map((item, index) => (
          <ResultCard key={index} url={item.url} summary={item.summary} />
        ))}
      </div>
    </div>
  )
}

export default App
