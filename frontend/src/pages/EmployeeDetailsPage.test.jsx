import { fireEvent, render, screen, waitFor, within } from '@testing-library/react'
import { beforeEach, describe, expect, it, vi } from 'vitest'

import { createSalary, getCurrentSalary, getSalaryHistory } from '../api/salaries'
import EmployeeDetailsPage from './EmployeeDetailsPage'

vi.mock('../api/salaries', () => ({
  createSalary: vi.fn(),
  getCurrentSalary: vi.fn(),
  getSalaryHistory: vi.fn(),
}))

const employee = {
  id: 7,
  employee_code: 'EMP00007',
  first_name: 'Maya',
  last_name: 'Shah',
  email: 'maya@example.com',
  country: 'India',
  department: 'Engineering',
  job_title: 'Software Engineer',
  status: 'active',
}

const currentSalary = {
  id: 10,
  employee_id: 7,
  base_salary: '1500000.00',
  bonus: '100000.00',
  currency: 'INR',
  effective_from: '2026-01-01',
  effective_to: null,
  reason: 'Initial salary',
}

const history = [
  { ...currentSalary },
  { ...currentSalary, id: 9, base_salary: '1200000.00', effective_to: '2025-12-31', reason: 'Promotion' },
]

beforeEach(() => {
  vi.clearAllMocks()
  getCurrentSalary.mockResolvedValue(currentSalary)
  getSalaryHistory.mockResolvedValue(history)
  createSalary.mockResolvedValue(currentSalary)
})

describe('EmployeeDetailsPage', () => {
  it('renders employee details and current salary', async () => {
    render(<EmployeeDetailsPage employee={employee} onBack={vi.fn()} />)

    expect(screen.getByText('Loading compensation...')).toBeInTheDocument()
    expect(await screen.findByText('Maya Shah')).toBeInTheDocument()
    expect(screen.getAllByText(/15,00,000\.00/)).toHaveLength(2)
    expect(screen.getAllByText('Initial salary')).toHaveLength(2)
    expect(getCurrentSalary).toHaveBeenCalledWith(7)
    expect(getSalaryHistory).toHaveBeenCalledWith(7)
  })

  it('shows a clear empty state when no current salary exists', async () => {
    getCurrentSalary.mockResolvedValue(null)
    getSalaryHistory.mockResolvedValue([])
    render(<EmployeeDetailsPage employee={employee} onBack={vi.fn()} />)

    expect(await screen.findByText('No current salary record.')).toBeInTheDocument()
    expect(screen.getByText('No salary history records.')).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'Add Salary' })).toBeInTheDocument()
  })

  it('renders salary history records', async () => {
    render(<EmployeeDetailsPage employee={employee} onBack={vi.fn()} />)

    expect(await screen.findByText('31 Dec 2025')).toBeInTheDocument()
    expect(screen.getByText('Promotion')).toBeInTheDocument()
  })

  it('validates the salary form before submission', async () => {
    render(<EmployeeDetailsPage employee={employee} onBack={vi.fn()} />)
    await screen.findByRole('button', { name: 'Revise Salary' })
    fireEvent.click(screen.getByRole('button', { name: 'Revise Salary' }))
    fireEvent.click(screen.getByRole('button', { name: 'Save salary' }))

    expect(screen.getByRole('alert')).toHaveTextContent('Base salary must be greater than 0.')
    expect(createSalary).not.toHaveBeenCalled()
  })

  it('submits a salary revision and refreshes current salary and history', async () => {
    render(<EmployeeDetailsPage employee={employee} onBack={vi.fn()} />)
    await screen.findByRole('button', { name: 'Revise Salary' })
    fireEvent.click(screen.getByRole('button', { name: 'Revise Salary' }))
    const dialog = screen.getByRole('dialog')
    const values = {
      base_salary: '1800000',
      bonus: '150000',
      currency: 'INR',
      effective_from: '2027-01-01',
      reason: 'Annual review',
    }
    Object.entries(values).forEach(([name, value]) => {
      const label = name === 'effective_from' ? 'Effective date' : name.replace('_', ' ')
      fireEvent.change(within(dialog).getByLabelText(new RegExp(label, 'i')), { target: { value } })
    })
    fireEvent.click(within(dialog).getByRole('button', { name: 'Save salary' }))

    await waitFor(() => expect(createSalary).toHaveBeenCalledWith(7, values))
    expect(await screen.findByText('Salary revision saved successfully.')).toBeInTheDocument()
    expect(getCurrentSalary).toHaveBeenCalledTimes(2)
    expect(getSalaryHistory).toHaveBeenCalledTimes(2)
  })

  it('shows a readable API error when salary submission fails', async () => {
    createSalary.mockRejectedValue(new Error('Salary effective date overlaps existing history'))
    render(<EmployeeDetailsPage employee={employee} onBack={vi.fn()} />)
    await screen.findByRole('button', { name: 'Revise Salary' })
    fireEvent.click(screen.getByRole('button', { name: 'Revise Salary' }))
    const dialog = screen.getByRole('dialog')
    fireEvent.change(within(dialog).getByRole('spinbutton', { name: /Base Salary/i }), { target: { value: '1800000' } })
    fireEvent.change(within(dialog).getByRole('combobox', { name: /Currency/i }), { target: { value: 'INR' } })
    fireEvent.change(dialog.querySelector('input[name="effective_from"]'), { target: { value: '2027-01-01' } })
    fireEvent.click(within(dialog).getByRole('button', { name: 'Save salary' }))

    expect(await screen.findByRole('alert')).toHaveTextContent('Salary effective date overlaps existing history')
  })
})