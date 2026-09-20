import { useEffect, useState } from 'react'

import { getHealthStatus } from '../api/health'

function HealthStatusPage() {
  const [status, setStatus] = useState({ state: 'loading', data: null, error: null })

  useEffect(() => {
    let isCurrent = true

    getHealthStatus()
      .then((data) => {
        if (isCurrent) {
          setStatus({ state: 'success', data, error: null })
        }
      })
      .catch((error) => {
        if (isCurrent) {
          setStatus({ state: 'error', data: null, error: error.message })
        }
      })

    return () => {
      isCurrent = false
    }
  }, [])

  return (
    <main className="health-page">
      <p className="eyebrow">ACME / SALARY MANAGEMENT</p>
      <h1>Backend Status</h1>

      {status.state === 'loading' && (
        <p className="status" role="status">
          Checking backend connection...
        </p>
      )}

      {status.state === 'success' && (
        <p className="status status-success" role="status">
          {status.data.status || 'Backend is available.'}
        </p>
      )}

      {status.state === 'error' && (
        <p className="status status-error" role="alert">
          Unable to reach the backend: {status.error}
        </p>
      )}
    </main>
  )
}

export default HealthStatusPage