import { useState } from 'react'
import axios from 'axios'

export default function UploadSection({ onTransform, loading }) {
  const [csvFile, setCsvFile] = useState(null)
  const [pdfFile, setPdfFile] = useState(null)
  const [configFile, setConfigFile] = useState(null)
  const [uploadStatus, setUploadStatus] = useState('')
  const [uploading, setUploading] = useState(false)

  const handleUpload = async (e) => {
    e.preventDefault()
    if (!csvFile || !pdfFile) {
        setUploadStatus('Please select both a CSV and a PDF resume.')
        return
    }

    setUploading(true)
    const formData = new FormData()
    formData.append('csv_file', csvFile)
    formData.append('pdf_file', pdfFile)
    if (configFile) {
        formData.append('config_file', configFile)
    }

    try {
      await axios.post('http://localhost:8000/api/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })
      setUploadStatus('Files uploaded successfully! Ready to transform.')
    } catch (error) {
      setUploadStatus('Failed to upload files: ' + (error.response?.data?.detail || error.message))
    } finally {
      setUploading(false)
    }
  }

  return (
    <div className="card upload-section">
      <h2>1. Data Sources</h2>
      <form onSubmit={handleUpload} className="upload-form">
        
        <div className="file-group">
            <label className="file-label">
                <span className="icon">📄</span>
                <span className="text">Recruiter CSV Data</span>
                <input type="file" accept=".csv" onChange={(e) => setCsvFile(e.target.files[0])} />
                {csvFile && <span className="file-name">{csvFile.name}</span>}
            </label>
        </div>

        <div className="file-group">
            <label className="file-label">
                <span className="icon">📑</span>
                <span className="text">Candidate Resume (PDF)</span>
                <input type="file" accept=".pdf" onChange={(e) => setPdfFile(e.target.files[0])} />
                {pdfFile && <span className="file-name">{pdfFile.name}</span>}
            </label>
        </div>

        <div className="file-group">
            <label className="file-label config-label">
                <span className="icon">⚙️</span>
                <span className="text">Projection Config JSON (Optional)</span>
                <input type="file" accept=".json" onChange={(e) => setConfigFile(e.target.files[0])} />
                {configFile && <span className="file-name">{configFile.name}</span>}
            </label>
        </div>

        <div className="actions">
            <button type="submit" className="btn primary-btn" disabled={uploading}>
                {uploading ? 'Uploading...' : 'Upload Data Files'}
            </button>
        </div>
      </form>
      
      {uploadStatus && <div className="status-message">{uploadStatus}</div>}

      <div className="transform-action">
          <h2>2. Process</h2>
          <button 
            className="btn action-btn pulse-anim" 
            onClick={onTransform} 
            disabled={loading || !uploadStatus.includes('successfully')}
          >
              {loading ? (
                  <span className="loader">Processing (Llama 3.2)...</span>
              ) : (
                  <span>Generate Canonical Profile ✨</span>
              )}
          </button>
      </div>
    </div>
  )
}
