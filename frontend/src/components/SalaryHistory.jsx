function SalaryHistory({ history }) {
  return (
    <section className="salary-section">
      <div className="section-heading"><div><p className="eyebrow">COMPENSATION RECORDS</p><h2>Salary History</h2></div></div>
      {history.length === 0 ? <p className="empty-state">No salary history records.</p> : (
        <div className="table-wrap">
          <table className="employee-table salary-history-table">
            <thead><tr><th>Effective From</th><th>Effective To</th><th>Base Salary</th><th>Bonus</th><th>Currency</th><th>Reason</th></tr></thead>
            <tbody>{history.map((salary) => <tr key={salary.id}><td>{salary.effective_from}</td><td>{salary.effective_to || 'Current'}</td><td>{salary.base_salary}</td><td>{salary.bonus}</td><td>{salary.currency}</td><td>{salary.reason || '-'}</td></tr>)}</tbody>
          </table>
        </div>
      )}
    </section>
  )
}

export default SalaryHistory