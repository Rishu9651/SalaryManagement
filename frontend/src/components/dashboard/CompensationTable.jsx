function CompensationTable({ title, eyebrow, dimension, rows }) {
  return (
    <section className="dashboard-section">
      <div className="section-heading"><div><p className="eyebrow">{eyebrow}</p><h2>{title}</h2></div></div>
      {rows.length === 0 ? <p className="empty-state">No compensation data is available.</p> : (
        <div className="table-wrap"><table className="employee-table analytics-table"><thead><tr><th>{dimension}</th><th>Currency</th><th>Employee Count</th><th>Average Base Salary</th><th>Total Base Salary</th><th>Average Bonus</th><th>Total Bonus</th></tr></thead><tbody>{rows.map((row) => <tr key={`${row[dimension]}-${row.currency}`}><td>{row[dimension]}</td><td>{row.currency}</td><td>{row.employee_count}</td><td>{row.average_base_salary} {row.currency}</td><td>{row.total_base_salary} {row.currency}</td><td>{row.average_bonus} {row.currency}</td><td>{row.total_bonus} {row.currency}</td></tr>)}</tbody></table></div>
      )}
    </section>
  )
}

export default CompensationTable