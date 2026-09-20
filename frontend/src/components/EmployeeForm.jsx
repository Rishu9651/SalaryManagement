import { useState } from 'react'

const COUNTRIES = ['India', 'United States', 'United Kingdom', 'Germany', 'Canada', 'Australia']
const DEPARTMENTS = ['Engineering', 'Product', 'Finance', 'Human Resources', 'Sales', 'Marketing', 'Operations', 'Legal', 'Customer Support']

const emptyForm = {
  employee_code: '',
  first_name: '',
  last_name: '',
  email: '',
  country: '',
  department: '',
  job_title: '',
}

function EmployeeForm({ employee, isSubmitting, onSubmit, onCancel }) {
  const [form, setForm] = useState(() => employee ? {
    employee_code: employee.employee_code,
    first_name: employee.first_name,
    last_name: employee.last_name,
    email: employee.email,
    country: employee.country,
    department: employee.department,
    job_title: employee.job_title,
  } : emptyForm)
  const [error, setError] = useState('')
  const isEditing = Boolean(employee)

  function handleChange(event) {
    const { name, value } = event.target
    setForm((current) => ({ ...current, [name]: value }))
  }

  function handleSubmit(event) {
    event.preventDefault()
    const requiredFields = isEditing
      ? ['first_name', 'last_name', 'email', 'country', 'department', 'job_title']
      : Object.keys(emptyForm)
    const missingField = requiredFields.find((field) => !form[field].trim())

    if (missingField) {
      setError('Please complete all required fields.')
      return
    }

    if (isEditing) {
      const editableFields = { ...form }
      delete editableFields.employee_code
      onSubmit(editableFields)
    } else {
      onSubmit(form)
    }
  }

  return (
    <div className="modal-backdrop" role="presentation">
      <section className="modal" role="dialog" aria-modal="true" aria-labelledby="employee-form-title">
        <div className="modal-heading">
          <div>
            <p className="eyebrow">EMPLOYEE RECORD</p>
            <h2 id="employee-form-title">{isEditing ? 'Edit Employee' : 'Add Employee'}</h2>
          </div>
          <button type="button" className="icon-button" aria-label="Close form" onClick={onCancel}>×</button>
        </div>
        <form onSubmit={handleSubmit} noValidate>
          <div className="form-grid">
            <label>Employee code<input name="employee_code" value={form.employee_code} onChange={handleChange} disabled={isEditing} required={!isEditing} /></label>
            <label>Email<input name="email" type="email" value={form.email} onChange={handleChange} required /></label>
            <label>First name<input name="first_name" value={form.first_name} onChange={handleChange} required /></label>
            <label>Last name<input name="last_name" value={form.last_name} onChange={handleChange} required /></label>
            <label>Country<select name="country" value={form.country} onChange={handleChange} required><option value="">Select country</option>{COUNTRIES.map((country) => <option key={country}>{country}</option>)}</select></label>
            <label>Department<select name="department" value={form.department} onChange={handleChange} required><option value="">Select department</option>{DEPARTMENTS.map((department) => <option key={department}>{department}</option>)}</select></label>
            <label className="field-wide">Job title<input name="job_title" value={form.job_title} onChange={handleChange} required /></label>
          </div>
          {error && <p className="form-error" role="alert">{error}</p>}
          <div className="form-actions">
            <button type="button" className="button-secondary" onClick={onCancel}>Cancel</button>
            <button type="submit" disabled={isSubmitting}>{isSubmitting ? 'Saving...' : isEditing ? 'Save changes' : 'Add employee'}</button>
          </div>
        </form>
      </section>
    </div>
  )
}

export default EmployeeForm