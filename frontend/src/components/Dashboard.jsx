export default function Dashboard({ confidence, overallConfidence, provenance, conflicts }) {
  
  const renderConfidenceChip = (field, score, isOverall = false) => {
    const percentage = Math.round(score * 100);
    const colorClass = percentage >= 90 ? 'high' : percentage >= 80 ? 'medium' : 'low';
    const statusText = percentage >= 90 ? 'High' : percentage >= 80 ? 'Fair' : 'Low';
    
    return (
      <div key={isOverall ? 'overall' : field} className={`confidence-chip ${isOverall ? 'overall-chip' : ''}`}>
        <span className="chip-label">{field.replace('_', ' ')}</span>
        <div className="chip-value-area">
          <span className="chip-percentage">{percentage}%</span>
          <span className={`chip-badge badge-${colorClass}`}>{statusText}</span>
        </div>
      </div>
    );
  };

  return (
    <div className="dashboard-container">
      <div className="dashboard-row">
        {/* Confidence Dashboard */}
        <div className="card dashboard-card">
          <h3><span className="icon">📊</span> Confidence Scores</h3>
          <div className="overall-score-container">
            {renderConfidenceChip('Overall Profile Quality', overallConfidence, true)}
          </div>
          <div className="field-scores-grid">
            {Object.entries(confidence).map(([field, score]) => (
              renderConfidenceChip(field, score)
            ))}
          </div>
        </div>

        {/* Provenance Dashboard */}
        <div className="card dashboard-card">
          <h3><span className="icon">🔍</span> Data Provenance</h3>
          <ul className="provenance-list">
            {provenance.map((prov, index) => (
              <li key={index} className="provenance-item">
                <span className="field-name">{prov.field}</span>
                <span className="arrow">→</span>
                <span className={`source-badge ${prov.source.includes('csv') ? 'source-csv' : 'source-llm'}`}>
                  {prov.source}
                </span>
              </li>
            ))}
          </ul>
        </div>
      </div>

      {/* Conflict Resolution Dashboard */}
      {conflicts && conflicts.length > 0 && (
        <div className="card full-width-card conflict-card">
          <h3><span className="icon">⚖️</span> Conflict Resolution</h3>
          <div className="conflict-grid">
            <div className="conflict-header">
              <div>Field</div>
              <div>CSV Data</div>
              <div>Resume Data</div>
              <div>Selected Value</div>
              <div>Reason</div>
            </div>
            {conflicts.map((conflict, index) => (
              <div key={index} className="conflict-row">
                <div className="field-name">{conflict.field}</div>
                <div className="val csv-val">{JSON.stringify(conflict.csv_value) || '-'}</div>
                <div className="val resume-val">{JSON.stringify(conflict.resume_value) || '-'}</div>
                <div className="val selected-val">{JSON.stringify(conflict.selected)}</div>
                <div className="reason-badge">{conflict.reason}</div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
