import { useEffect, useState } from 'react'

import { getAnalyticsSummary, getCountryCompensation, getDepartmentCompensation, getSalaryDistribution } from '../api/analytics'
import CompensationTable from '../components/dashboard/CompensationTable'
import CountryEmployeeChart from '../components/dashboard/CountryEmployeeChart'
import CurrencySummary from '../components/dashboard/CurrencySummary'
import SalaryDistribution from '../components/dashboard/SalaryDistribution'
import SalaryDistributionChart from '../components/dashboard/SalaryDistributionChart'
import SummaryCards from '../components/dashboard/SummaryCards'

function DashboardPage() {
  const [data, setData] = useState(null)
  const [state, setState] = useState('loading')
  const [error, setError] = useState('')

  useEffect(() => {
    let isCurrent = true
    Promise.all([
      getAnalyticsSummary(),
      getCountryCompensation(),
      getDepartmentCompensation(),
      getSalaryDistribution(),
    ]).then(([summary, countries, departments, distribution]) => {
      if (isCurrent) {
        setData({ summary, countries, departments, distribution })
        setState('success')
      }
    }).catch((requestError) => {
      if (isCurrent) {
        setError(requestError.message)
        setState('error')
      }
    })
    return () => { isCurrent = false }
  }, [])

  return (
    <main className="employees-page dashboard-page">
      <header className="page-header">
        <div><p className="eyebrow">COMPENSATION OVERVIEW</p><h1>Compensation Dashboard</h1><p className="page-subtitle">Current workforce and compensation insights by currency.</p></div>
      </header>
      {state === 'loading' && <p className="status" role="status">Loading dashboard...</p>}
      {state === 'error' && <p className="form-error" role="alert">Unable to load dashboard: {error}</p>}
      {state === 'success' && <>
        <SummaryCards summary={data.summary} />
        <CountryEmployeeChart rows={data.countries} />
        <SalaryDistributionChart groups={data.distribution} />
        <CurrencySummary rows={data.summary.compensation} />
        <CompensationTable title="Country Compensation" eyebrow="LOCATION" dimension="country" rows={data.countries} />
        <CompensationTable title="Department Compensation" eyebrow="ORGANIZATION" dimension="department" rows={data.departments} />
        <SalaryDistribution groups={data.distribution} />
      </>}
    </main>
  )
}

export default DashboardPage