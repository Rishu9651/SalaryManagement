import apiClient from './client'

export async function listEmployees({ page = 1, pageSize = 25, search, country, department } = {}) {
  const response = await apiClient.get('/api/employees', {
    params: {
      page,
      page_size: pageSize,
      ...(search ? { search } : {}),
      ...(country ? { country } : {}),
      ...(department ? { department } : {}),
    },
  })
  return response.data
}

export async function createEmployee(employee) {
  const response = await apiClient.post('/api/employees', employee)
  return response.data
}

export async function updateEmployee(employeeId, employee) {
  const response = await apiClient.patch(`/api/employees/${employeeId}`, employee)
  return response.data
}

export async function deactivateEmployee(employeeId) {
  const response = await apiClient.delete(`/api/employees/${employeeId}`)
  return response.data
}