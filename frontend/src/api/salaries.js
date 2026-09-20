import apiClient from './client'

export async function getCurrentSalary(employeeId) {
  try {
    const response = await apiClient.get(`/api/employees/${employeeId}/salary`)
    return response.data
  } catch (error) {
    if (error.status === 404) return null
    throw error
  }
}

export async function getSalaryHistory(employeeId) {
  const response = await apiClient.get(`/api/employees/${employeeId}/salary-history`)
  return response.data
}

export async function createSalary(employeeId, salary) {
  const response = await apiClient.post(`/api/employees/${employeeId}/salary`, salary)
  return response.data
}