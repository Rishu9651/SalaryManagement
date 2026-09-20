import { useState } from 'react'

const CURRENCIES = ['INR', 'USD', 'GBP', 'EUR', 'CAD', 'AUD']
const emptyForm = { base_salary: '', bonus: '0', currency: '', effective_from: '', reason: '' }

function SalaryForm({ isSubmitting, onSubmit, onCancel }) {
  const [form, setForm] = useState(emptyForm)
  const [error, setError] = useState('')

  function handleChange(event) {
    const { name, value } = event.target
    setForm((current) => ({ ...current, [name]: value }))
  }

  function handleSubmit(event) {
    event.preventDefault()
    if (!form.base_salary || Number(form.base_salary) <= 0) {
      setError('Base salary must be greater than 0.')
      return
    }
    if (form.bonus === '' || Number(form.bonus) < 0) {
      setError('Bonus cannot be negative.')
      return
    }
    if (!form.currency || !form.effective_from) {
      setError('Currency and effective date are required.')
      return
    }
    setError('')
    onSubmit(form)
  }

  return (
    <div className="modal-backdrop" role="presentation">
      <section className="modal" role="dialog" aria-modal="true" aria-labelledby="salary-form-title">
        <div className="modal-heading"><div><p className="eyebrow">COMPENSATION</p><h2 id="salary-form-title">Revise Salary</h2></div><button type="button" className="icon-button" aria-label="Close form" onClick={onCancel}>×</button></div>
        <form onSubmit={handleSubmit} noValidate>
          <div className="form-grid">
            <label>Base Salary<span className="required-marker">Required</span><input name="base_salary" type="number" min="0.01" step="0.01" value={form.base_salary} onChange={handleChange} /></label>
            <label>Bonus<span className="field-hint">Optional</span><input name="bonus" type="number" min="0" step="0.01" value={form.bonus} onChange={handleChange} /></label>
            <label>Currency<span className="required-marker">Required</span><select name="currency" value={form.currency} onChange={handleChange}><option value="">Select currency</option>{CURRENCIES.map((currency) => <option key={currency}>{currency}</option>)}</select></label>
            <label>Effective date<span className="required-marker">Required</span><input name="effective_from" type="date" value={form.effective_from} onChange={handleChange} /></label>
            <label className="field-wide">Reason<textarea name="reason" maxLength="500" value={form.reason} onChange={handleChange} rows="3" /></label>
          </div>
          {error && <p className="form-error" role="alert">{error}</p>}
          <div className="form-actions"><button type="button" className="button-secondary" onClick={onCancel}>Cancel</button><button type="submit" disabled={isSubmitting}>{isSubmitting ? 'Saving...' : 'Save salary'}</button></div>
        </form>
      </section>
    </div>
  )
}

export default SalaryForm