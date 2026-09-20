import apiClient from './client'

export async function getHealthStatus() {
  const response = await apiClient.get('/health')
  return response.data
}