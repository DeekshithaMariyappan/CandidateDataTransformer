import { useState } from 'react'
import axios from 'axios'
import UploadSection from './components/UploadSection'
import Dashboard from './components/Dashboard'
import CanonicalProfileViewer from './components/CanonicalProfileViewer'


function App() {
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)

  const handleTransform = async () => {
    setLoading(true)
    setError(null)
    try {
      const response = await axios.post('http://localhost:8000/api/transform')
      setResult(response.data)
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'An error occurred during transformation')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app-container">
      <header className="app-header">
        <h1>Candidate Data Transformer</h1>
      </header>

      <main className="app-main">
        <section className="left-panel">
          <UploadSection onTransform={handleTransform} loading={loading} />
          {error && <div className="error-banner">{error}</div>}
        </section>

        {result && (
          <section className="right-panel slide-in">

            <div className="panel-content">
              <CanonicalProfileViewer profile={result.profile} />
              <Dashboard
                confidence={result.confidence}
                overallConfidence={result.overall_confidence}
                provenance={result.provenance}
                conflicts={result.conflicts}
              />

            </div>
          </section>
        )}
      </main>
    </div>
  )
}

export default App
