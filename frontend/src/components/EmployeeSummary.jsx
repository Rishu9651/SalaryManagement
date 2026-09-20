import { formatStatus } from '../utils/formatters'

function EmployeeSummary({ employee, onBack }) {
  return (
    <section className="employee-summary">
      <button type="button" className="button-secondary" onClick={onBack}>Back to employees</button>
      <p className="eyebrow">EMPLOYEE DETAILS</p>
      <h1>{employee.first_name} {employee.last_name}</h1>
      <dl className="details-grid">
        <div><dt>Employee Code</dt><dd>{employee.employee_code}</dd></div>
        <div><dt>Email</dt><dd>{employee.email}</dd></div>
        <div><dt>Country</dt><dd>{employee.country}</dd></div>
        <div><dt>Department</dt><dd>{employee.department}</dd></div>
        <div><dt>Job Title</dt><dd>{employee.job_title}</dd></div>
        <div><dt>Status</dt><dd><span className={`status-pill status-${employee.status}`}><span className="status-dot" aria-hidden="true" />{formatStatus(employee.status)}</span></dd></div>
      </dl>
    </section>
  )
}

export default EmployeeSummary