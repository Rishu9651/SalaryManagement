function CountryEmployeeChart({ rows }) {
  const maxCount = Math.max(...rows.map((row) => row.employee_count), 0)

  return (
    <section className="dashboard-section visualization-section">
      <div className="section-heading"><div><p className="eyebrow">WORKFORCE MIX</p><h2>Employee Count by Country</h2></div></div>
      {rows.length === 0 ? <p className="empty-state">No country employee data is available.</p> : (
        <div className="bar-chart" aria-label="Employee count by country">
          {rows.map((row) => (
            <div className="bar-chart-row" key={`${row.country}-${row.currency}`}>
              <div className="bar-chart-label"><span>{row.country}</span><small>{row.currency}</small></div>
              <div className="bar-track"><span className="bar-fill country-bar" style={{ width: `${maxCount ? (row.employee_count / maxCount) * 100 : 0}%` }} /></div>
              <strong>{row.employee_count}</strong>
            </div>
          ))}
        </div>
      )}
    </section>
  )
}

export default CountryEmployeeChart