import './App.css'
import { useState } from 'react'

import DashboardPage from './pages/DashboardPage'
import EmployeeDetailsPage from './pages/EmployeeDetailsPage'
import EmployeesPage from './pages/EmployeesPage'

function App() {
  const [activePage, setActivePage] = useState('dashboard')
  const [selectedEmployee, setSelectedEmployee] = useState(null)

  if (selectedEmployee) {
    return <EmployeeDetailsPage employee={selectedEmployee} onBack={() => setSelectedEmployee(null)} />
  }
  if (activePage === 'employees') {
    return <EmployeesPage onView={setSelectedEmployee} onNavigate={setActivePage} />
  }
  return <DashboardPage onNavigate={setActivePage} />
}

export default App
