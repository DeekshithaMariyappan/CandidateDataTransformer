export default function CanonicalProfileViewer({ profile }) {
  if (!profile) return null;

  const renderValue = (value) => {
    if (value === null || value === undefined || value === '') return <span className="text-muted">N/A</span>;
    
    if (typeof value === 'string' || typeof value === 'number') {
      return <span>{value}</span>;
    }
    
    if (Array.isArray(value)) {
      if (value.length === 0) return <span className="text-muted">None</span>;
      
      // If array of strings (like skills, emails)
      if (typeof value[0] === 'string' || typeof value[0] === 'number') {
        return (
          <div className="skills-container">
            {value.map((item, i) => (
              <span key={i} className="skill-tag">{item}</span>
            ))}
          </div>
        );
      }
      
      // If array of objects (like experience, education)
      return (
        <ul className="timeline-list">
          {value.map((item, i) => (
            <li key={i}>
              <pre className="dynamic-pre">{JSON.stringify(item, null, 2)}</pre>
            </li>
          ))}
        </ul>
      );
    }
    
    if (typeof value === 'object') {
      return <pre className="dynamic-pre">{JSON.stringify(value, null, 2)}</pre>;
    }
    
    return String(value);
  };

  const formatKey = (key) => {
    return key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
  };

  return (
    <>
      <div className="card canonical-card">
        <div className="profile-header">
          <div className="avatar">
            {profile.full_name ? profile.full_name.charAt(0).toUpperCase() : '?'}
          </div>
          <div className="header-info">
            <h2>{profile.full_name || 'Candidate Profile'}</h2>
            {profile.headline && <p className="headline">{profile.headline}</p>}
          </div>
        </div>

        <div className="profile-body">
          {Object.entries(profile).map(([key, value]) => {
            // Skip fields rendered in the header or internal fields
            if (key === 'full_name' || key === 'headline') return null;
            
            return (
              <div key={key} className="section">
                <h3>{formatKey(key)}</h3>
                <div className="section-content">
                  {renderValue(value)}
                </div>
              </div>
            );
          })}
        </div>
      </div>

      <div className="card canonical-card" style={{ marginTop: '1.5rem' }}>
        <h3 style={{ marginBottom: '0.5rem' }}><span className="icon">📄</span> Projected Output JSON</h3>
        <p className="text-muted" style={{ marginBottom: '1rem', fontSize: '0.9rem' }}>
          This data exactly matches the structure defined in your projection configuration.
        </p>
        <div className="json-container">
          {JSON.stringify(profile, null, 2)}
        </div>
      </div>
    </>
  );
}
