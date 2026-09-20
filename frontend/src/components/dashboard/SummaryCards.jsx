function SummaryCards({ summary }) {
  return (
    <section className="summary-cards" aria-label="Employee summary">
      <article className="summary-card"><span>Total Employees</span><strong>{summary.total_employees}</strong></article>
      <article className="summary-card"><span>Employees With Current Salary</span><strong>{summary.employees_with_salary}</strong></article>
    </section>
  )
}

export default SummaryCards