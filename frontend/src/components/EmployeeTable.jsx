function EmployeeTable({ employees, onEdit, onDeactivate }) {
  return (
    <div className="table-wrap">
      <table className="employee-table">
        <thead>
          <tr>
            <th>Employee Code</th>
            <th>Name</th>
            <th>Email</th>
            <th>Country</th>
            <th>Department</th>
            <th>Job Title</th>
            <th>Status</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {employees.map((employee) => (
            <tr key={employee.id}>
              <td>{employee.employee_code}</td>
              <td>{employee.first_name} {employee.last_name}</td>
              <td>{employee.email}</td>
              <td>{employee.country}</td>
              <td>{employee.department}</td>
              <td>{employee.job_title}</td>
              <td><span className={`status-pill status-${employee.status}`}>{employee.status}</span></td>
              <td className="table-actions">
                <button type="button" onClick={() => onEdit(employee)}>Edit</button>
                <button
                  type="button"
                  className="button-danger"
                  onClick={() => onDeactivate(employee)}
                  disabled={employee.status === 'inactive'}
                >
                  Deactivate
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

export default EmployeeTable