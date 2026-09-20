import './App.css'
import { useState } from 'react'

import AppLayout from './components/AppLayout'
import DashboardPage from './pages/DashboardPage'
import EmployeeDetailsPage from './pages/EmployeeDetailsPage'
import EmployeesPage from './pages/EmployeesPage'

function App() {
  const [activePage, setActivePage] = useState('dashboard')
  const [selectedEmployee, setSelectedEmployee] = useState(null)

  function navigate(page) {
    setSelectedEmployee(null)
    setActivePage(page)
  }

  const content = selectedEmployee
    ? <EmployeeDetailsPage employee={selectedEmployee} onBack={() => setSelectedEmployee(null)} />
    : activePage === 'employees'
      ? <EmployeesPage onView={setSelectedEmployee} />
      : <DashboardPage />

  return <AppLayout activePage={selectedEmployee ? 'employees' : activePage} onNavigate={navigate}>{content}</AppLayout>
}

export default App
