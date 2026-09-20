import { formatCurrency, formatDate } from '../utils/formatters'

function SalaryHistory({ history }) {
  return (
    <section className="salary-section">
      <div className="section-heading"><div><p className="eyebrow">COMPENSATION RECORDS</p><h2>Salary History</h2></div></div>
      {history.length === 0 ? <p className="empty-state">No salary history records.</p> : (
        <div className="table-wrap">
          <table className="employee-table salary-history-table">
            <thead><tr><th>Effective From</th><th>Effective To</th><th>Base Salary</th><th>Bonus</th><th>Currency</th><th>Reason</th></tr></thead>
            <tbody>{history.map((salary) => <tr className={salary.effective_to ? '' : 'current-row'} key={salary.id}><td>{formatDate(salary.effective_from)}</td><td>{salary.effective_to ? formatDate(salary.effective_to) : <span className="current-label">Current</span>}</td><td className="money-value">{formatCurrency(salary.base_salary, salary.currency)}</td><td className="money-value">{formatCurrency(salary.bonus, salary.currency)}</td><td>{salary.currency}</td><td>{salary.reason || '-'}</td></tr>)}</tbody>
          </table>
        </div>
      )}
    </section>
  )
}

export default SalaryHistory