export default function OllamaPreview({ data }) {
  if (!data) return null;

  return (
    <div className="card ollama-card">
      <div className="card-header">
        <h3><span className="icon">🦙</span> Ollama Extraction Preview (Llama 3.2)</h3>
        <span className="badge">Raw JSON</span>
      </div>
      <div className="json-container">
        <pre>
          <code>{JSON.stringify(data, null, 2)}</code>
        </pre>
      </div>
    </div>
  )
}
