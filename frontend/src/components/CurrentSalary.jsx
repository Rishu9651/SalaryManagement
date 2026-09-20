function CurrentSalary({ salary, onRevise }) {
  return (
    <section className="salary-section">
      <div className="section-heading">
        <div><p className="eyebrow">COMPENSATION</p><h2>Current Salary</h2></div>
        <button type="button" onClick={onRevise}>{salary ? 'Revise Salary' : 'Add Salary'}</button>
      </div>
      {salary ? (
        <dl className="details-grid compensation-grid">
          <div><dt>Base Salary</dt><dd>{salary.base_salary} {salary.currency}</dd></div>
          <div><dt>Bonus</dt><dd>{salary.bonus} {salary.currency}</dd></div>
          <div><dt>Currency</dt><dd>{salary.currency}</dd></div>
          <div><dt>Effective From</dt><dd>{salary.effective_from}</dd></div>
          {salary.reason && <div className="field-wide"><dt>Reason</dt><dd>{salary.reason}</dd></div>}
        </dl>
      ) : <p className="empty-state">No current salary record.</p>}
    </section>
  )
}

export default CurrentSalary