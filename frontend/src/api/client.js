import axios from 'axios'

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
  headers: {
    Accept: 'application/json',
  },
})

apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    const message = error.response?.data?.detail || error.message || 'Request failed'
    const normalizedError = new Error(message)
    normalizedError.status = error.response?.status
    return Promise.reject(normalizedError)
  },
)

export default apiClient