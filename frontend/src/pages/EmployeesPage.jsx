import { useCallback, useEffect, useState } from 'react'

import { createEmployee, deactivateEmployee, listEmployees, updateEmployee } from '../api/employees'
import EmployeeForm from '../components/EmployeeForm'
import EmployeeTable from '../components/EmployeeTable'
import Pagination from '../components/Pagination'

const COUNTRIES = ['India', 'United States', 'United Kingdom', 'Germany', 'Canada', 'Australia']
const DEPARTMENTS = ['Engineering', 'Product', 'Finance', 'Human Resources', 'Sales', 'Marketing', 'Operations', 'Legal', 'Customer Support']
const PAGE_SIZE = 25

function EmployeesPage({ onView }) {
  const [filters, setFilters] = useState({ search: '', country: '', department: '' })
  const [page, setPage] = useState(1)
  const [data, setData] = useState({ items: [], total: 0, page: 1, total_pages: 0 })
  const [state, setState] = useState('loading')
  const [error, setError] = useState('')
  const [formEmployee, setFormEmployee] = useState(null)
  const [isFormOpen, setIsFormOpen] = useState(false)
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [notice, setNotice] = useState('')

  const loadEmployees = useCallback(async () => {
    setState((current) => current === 'loading' ? 'loading' : 'refreshing')
    setError('')
    try {
      const result = await listEmployees({ page, pageSize: PAGE_SIZE, ...filters })
      setData(result)
      setState('success')
    } catch (requestError) {
      setError(requestError.message)
      setState('error')
    }
  }, [filters, page])

  // eslint-disable-next-line react-hooks/set-state-in-effect
  useEffect(() => { loadEmployees() }, [loadEmployees])

  function updateFilter(event) {
    const { name, value } = event.target
    setFilters((current) => ({ ...current, [name]: value }))
    setPage(1)
  }

  function openCreateForm() {
    setFormEmployee(null)
    setIsFormOpen(true)
  }

  function openEditForm(employee) {
    setFormEmployee(employee)
    setIsFormOpen(true)
  }

  async function handleFormSubmit(employee) {
    setIsSubmitting(true)
    setError('')
    try {
      if (formEmployee) {
        await updateEmployee(formEmployee.id, employee)
        setNotice('Employee updated successfully.')
      } else {
        await createEmployee(employee)
        setNotice('Employee added successfully.')
      }
      setIsFormOpen(false)
      setFormEmployee(null)
      setPage(1)
      if (page === 1) await loadEmployees()
    } catch (requestError) {
      setError(requestError.message)
    } finally {
      setIsSubmitting(false)
    }
  }

  async function handleDeactivate(employee) {
    if (!window.confirm(`Deactivate ${employee.first_name} ${employee.last_name}?`)) return
    setError('')
    try {
      await deactivateEmployee(employee.id)
      setNotice('Employee deactivated successfully.')
      await loadEmployees()
    } catch (requestError) {
      setError(requestError.message)
    }
  }

  return (
    <main className="employees-page">
      <header className="page-header">
        <div><p className="eyebrow">ACME / SALARY MANAGEMENT</p><h1>Employees</h1><p className="page-subtitle">Manage employee records and employment status.</p></div>
        <button type="button" onClick={openCreateForm}>Add Employee</button>
      </header>

      <section className="filter-bar" aria-label="Employee filters">
        <label className="search-field">Search<input name="search" value={filters.search} onChange={updateFilter} placeholder="Name, code, or email" /></label>
        <label>Country<select name="country" value={filters.country} onChange={updateFilter}><option value="">All countries</option>{COUNTRIES.map((country) => <option key={country}>{country}</option>)}</select></label>
        <label>Department<select name="department" value={filters.department} onChange={updateFilter}><option value="">All departments</option>{DEPARTMENTS.map((department) => <option key={department}>{department}</option>)}</select></label>
      </section>

      {notice && <p className="notice" role="status">{notice}</p>}
      {error && <p className="form-error" role="alert">{error}</p>}
      {state === 'loading' && <p className="status" role="status">Loading employees...</p>}
      {state === 'refreshing' && <p className="status" role="status">Refreshing employees...</p>}
      {state === 'error' && <button type="button" onClick={loadEmployees}>Try again</button>}
      {state === 'success' && data.items.length === 0 && <p className="empty-state">No employees match the current filters.</p>}
      {state === 'success' && data.items.length > 0 && <EmployeeTable employees={data.items} onView={onView} onEdit={openEditForm} onDeactivate={handleDeactivate} />}
      {state === 'success' && <Pagination page={data.page || page} totalPages={data.total_pages} onPageChange={setPage} />}

      {isFormOpen && <EmployeeForm key={formEmployee?.id || 'new'} employee={formEmployee} isSubmitting={isSubmitting} onSubmit={handleFormSubmit} onCancel={() => setIsFormOpen(false)} />}
    </main>
  )
}

export default EmployeesPage