import { useEffect, useState } from 'react'

import { createSalary, getCurrentSalary, getSalaryHistory } from '../api/salaries'
import CurrentSalary from '../components/CurrentSalary'
import EmployeeSummary from '../components/EmployeeSummary'
import SalaryForm from '../components/SalaryForm'
import SalaryHistory from '../components/SalaryHistory'

function EmployeeDetailsPage({ employee, onBack }) {
  const [currentSalary, setCurrentSalary] = useState(null)
  const [history, setHistory] = useState([])
  const [state, setState] = useState('loading')
  const [error, setError] = useState('')
  const [isFormOpen, setIsFormOpen] = useState(false)
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [notice, setNotice] = useState('')

  async function loadSalaryData() {
    setState((current) => current === 'loading' ? 'loading' : 'refreshing')
    setError('')
    const [salaryResult, historyResult] = await Promise.allSettled([
      getCurrentSalary(employee.id),
      getSalaryHistory(employee.id),
    ])
    if (salaryResult.status === 'fulfilled') setCurrentSalary(salaryResult.value)
    else setError(salaryResult.reason.message)
    if (historyResult.status === 'fulfilled') setHistory(historyResult.value)
    else setError((current) => current || historyResult.reason.message)
    setState('success')
  }

  // eslint-disable-next-line react-hooks/set-state-in-effect, react-hooks/exhaustive-deps
  useEffect(() => { loadSalaryData() }, [employee.id])

  async function handleSalarySubmit(salary) {
    setIsSubmitting(true)
    setError('')
    try {
      await createSalary(employee.id, salary)
      setIsFormOpen(false)
      setNotice('Salary revision saved successfully.')
      await loadSalaryData()
    } catch (requestError) {
      setError(requestError.message)
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <main className="employees-page">
      <EmployeeSummary employee={employee} onBack={onBack} />
      {notice && <p className="notice" role="status">{notice}</p>}
      {error && <p className="form-error" role="alert">{error}</p>}
      {state === 'loading' && <p className="status" role="status">Loading compensation...</p>}
      {state === 'refreshing' && <p className="status" role="status">Refreshing compensation...</p>}
      {state !== 'loading' && <><CurrentSalary salary={currentSalary} onRevise={() => setIsFormOpen(true)} /><SalaryHistory history={history} /></>}
      {isFormOpen && <SalaryForm isSubmitting={isSubmitting} onSubmit={handleSalarySubmit} onCancel={() => setIsFormOpen(false)} />}
    </main>
  )
}

export default EmployeeDetailsPage