export default function CanonicalProfileViewer({ profile }) {
  if (!profile) return null;

  return (
    <div className="card canonical-card">
      <div className="profile-header">
        <div className="avatar">
          {profile.full_name ? profile.full_name.charAt(0).toUpperCase() : '?'}
        </div>
        <div className="header-info">
          <h2>{profile.full_name || 'Unknown Candidate'}</h2>
          {profile.headline && <p className="headline">{profile.headline}</p>}
        </div>
      </div>

      <div className="profile-body">
        <div className="contact-info">
          <div className="info-pill">
            <span className="icon">📧</span> {profile.emails?.join(', ') || 'No email'}
          </div>
          <div className="info-pill">
            <span className="icon">📱</span> {profile.phones?.join(', ') || 'No phone'}
          </div>
        </div>

        <div className="section">
          <h3>Skills</h3>
          <div className="skills-container">
            {profile.skills?.map((skill, i) => (
              <span key={i} className="skill-tag">{skill}</span>
            ))}
          </div>
        </div>

        <div className="section">
          <h3>Education</h3>
          <ul className="timeline-list">
            {profile.education?.map((edu, i) => (
              <li key={i}>{typeof edu === 'string' ? edu : JSON.stringify(edu)}</li>
            ))}
          </ul>
        </div>

        <div className="section">
          <h3>Experience</h3>
          <ul className="timeline-list">
            {profile.experience?.map((exp, i) => (
              <li key={i}>
                {typeof exp === 'string' ? exp : (
                  <div>
                    <strong>{exp.title}</strong> at {exp.company}
                    <div className="dates">{exp.dates}</div>
                    <p>{exp.description}</p>
                  </div>
                )}
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  )
}
