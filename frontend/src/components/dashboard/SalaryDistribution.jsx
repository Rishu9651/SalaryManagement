function SalaryDistribution({ groups }) {
  return (
    <section className="dashboard-section">
      <div className="section-heading"><div><p className="eyebrow">CURRENT SALARIES</p><h2>Salary Distribution</h2></div></div>
      {groups.length === 0 ? <p className="empty-state">No salary distribution data is available.</p> : <div className="distribution-grid">{groups.map((group) => <article className="distribution-card" key={group.currency}><h3>{group.currency}</h3><div className="band-list">{group.bands.map((band) => <div className="band-row" key={band.label}><span>{band.label}</span><strong>{band.employee_count}</strong></div>)}</div></article>)}</div>}
    </section>
  )
}

export default SalaryDistribution