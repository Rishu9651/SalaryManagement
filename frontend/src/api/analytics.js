import apiClient from './client'

export async function getAnalyticsSummary() {
  const response = await apiClient.get('/api/analytics/summary')
  return response.data
}

export async function getCountryCompensation() {
  const response = await apiClient.get('/api/analytics/countries')
  return response.data
}

export async function getDepartmentCompensation() {
  const response = await apiClient.get('/api/analytics/departments')
  return response.data
}

export async function getSalaryDistribution() {
  const response = await apiClient.get('/api/analytics/salary-distribution')
  return response.data
}