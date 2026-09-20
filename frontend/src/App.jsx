import './App.css'
import { useState } from 'react'

import EmployeeDetailsPage from './pages/EmployeeDetailsPage'
import EmployeesPage from './pages/EmployeesPage'

function App() {
  const [selectedEmployee, setSelectedEmployee] = useState(null)
  return selectedEmployee
    ? <EmployeeDetailsPage employee={selectedEmployee} onBack={() => setSelectedEmployee(null)} />
    : <EmployeesPage onView={setSelectedEmployee} />
}

export default App
