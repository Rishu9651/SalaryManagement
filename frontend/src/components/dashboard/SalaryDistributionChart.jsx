import { useState } from 'react'

function SalaryDistributionChart({ groups }) {
  const [selectedCurrency, setSelectedCurrency] = useState(groups[0]?.currency || '')
  const selectedGroup = groups.find((group) => group.currency === selectedCurrency) || groups[0]
  const maxCount = Math.max(...(selectedGroup?.bands || []).map((band) => band.employee_count), 0)

  return (
    <section className="dashboard-section visualization-section">
      <div className="section-heading">
        <div><p className="eyebrow">ONE CURRENCY AT A TIME</p><h2>Salary Distribution</h2></div>
        {groups.length > 0 && <label className="chart-select">Currency<select value={selectedGroup?.currency || ''} onChange={(event) => setSelectedCurrency(event.target.value)}>{groups.map((group) => <option key={group.currency}>{group.currency}</option>)}</select></label>}
      </div>
      {!selectedGroup ? <p className="empty-state">No salary distribution data is available.</p> : (
        <div className="bar-chart" aria-label={`Salary distribution in ${selectedGroup.currency}`}>
          {selectedGroup.bands.map((band) => (
            <div className="bar-chart-row" key={band.label}>
              <div className="bar-chart-label"><span>{band.label}</span><small>{selectedGroup.currency}</small></div>
              <div className="bar-track"><span className="bar-fill salary-bar" style={{ width: `${maxCount ? (band.employee_count / maxCount) * 100 : 0}%` }} /></div>
              <strong>{band.employee_count}</strong>
            </div>
          ))}
        </div>
      )}
    </section>
  )
}

export default SalaryDistributionChart