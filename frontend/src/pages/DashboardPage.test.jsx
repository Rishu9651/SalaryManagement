import { fireEvent, render, screen } from '@testing-library/react'
import { beforeEach, describe, expect, it, vi } from 'vitest'

import {
  getAnalyticsSummary,
  getCountryCompensation,
  getDepartmentCompensation,
  getSalaryDistribution,
} from '../api/analytics'
import DashboardPage from './DashboardPage'

vi.mock('../api/analytics', () => ({
  getAnalyticsSummary: vi.fn(),
  getCountryCompensation: vi.fn(),
  getDepartmentCompensation: vi.fn(),
  getSalaryDistribution: vi.fn(),
}))

const summary = {
  total_employees: 100,
  employees_with_salary: 92,
  compensation: [{
    currency: 'INR',
    employee_count: 60,
    average_base_salary: '1500000.00',
    total_base_salary: '90000000.00',
    average_bonus: '100000.00',
    total_bonus: '6000000.00',
  }, {
    currency: 'USD',
    employee_count: 32,
    average_base_salary: '95000.00',
    total_base_salary: '3040000.00',
    average_bonus: '9000.00',
    total_bonus: '288000.00',
  }],
}

const countries = [{
  country: 'India', currency: 'INR', employee_count: 60,
  average_base_salary: '1500000.00', total_base_salary: '90000000.00',
  average_bonus: '100000.00', total_bonus: '6000000.00',
}]

const departments = [{
  department: 'Engineering', currency: 'USD', employee_count: 20,
  average_base_salary: '95000.00', total_base_salary: '1900000.00',
  average_bonus: '9000.00', total_bonus: '180000.00',
}]

const distribution = [{
  currency: 'INR',
  bands: [{ label: '10-20L', employee_count: 60 }],
}, { currency: 'USD', bands: [{ label: '50-100K', employee_count: 32 }] }]

function resolveAnalytics() {
  getAnalyticsSummary.mockResolvedValue(summary)
  getCountryCompensation.mockResolvedValue(countries)
  getDepartmentCompensation.mockResolvedValue(departments)
  getSalaryDistribution.mockResolvedValue(distribution)
}

beforeEach(() => {
  vi.clearAllMocks()
  resolveAnalytics()
})

describe('DashboardPage', () => {
  it('shows a loading state while analytics are loading', () => {
    getAnalyticsSummary.mockReturnValue(new Promise(() => {}))
    getCountryCompensation.mockReturnValue(new Promise(() => {}))
    getDepartmentCompensation.mockReturnValue(new Promise(() => {}))
    getSalaryDistribution.mockReturnValue(new Promise(() => {}))
    render(<DashboardPage onNavigate={vi.fn()} />)

    expect(screen.getByText('Loading dashboard...')).toBeInTheDocument()
  })

  it('renders summary cards and all analytics sections from API data', async () => {
    render(<DashboardPage onNavigate={vi.fn()} />)

    expect(await screen.findByText('100')).toBeInTheDocument()
    expect(screen.getByText('92')).toBeInTheDocument()
    expect(screen.getByText('Employee Count by Country')).toBeInTheDocument()
    expect(screen.getAllByText('Salary Distribution')).toHaveLength(2)
    expect(screen.getAllByText(/15,00,000\.00/)).toHaveLength(2)
    expect(screen.getAllByText('India')).toHaveLength(2)
    expect(screen.getByText('Engineering')).toBeInTheDocument()
    expect(screen.getAllByText('10-20L')).toHaveLength(2)
    expect(screen.getByText('50-100K')).toBeInTheDocument()
  })

  it('changes the salary distribution visualization by currency', async () => {
    render(<DashboardPage onNavigate={vi.fn()} />)
    await screen.findByText('Employee Count by Country')

    fireEvent.change(screen.getByLabelText('Currency'), { target: { value: 'USD' } })

    expect(screen.getByLabelText('Salary distribution in USD')).toBeInTheDocument()
    expect(screen.getAllByText('50-100K')).toHaveLength(2)
  })

  it('keeps compensation values separated by currency', async () => {
    render(<DashboardPage onNavigate={vi.fn()} />)

    await screen.findAllByText(/15,00,000\.00/)
    expect(screen.getAllByText('$95,000.00')).toHaveLength(2)
    expect(screen.queryByText(/2450000/)).not.toBeInTheDocument()
  })

  it('shows meaningful empty states when analytics arrays are empty', async () => {
    getAnalyticsSummary.mockResolvedValue({ total_employees: 0, employees_with_salary: 0, compensation: [] })
    getCountryCompensation.mockResolvedValue([])
    getDepartmentCompensation.mockResolvedValue([])
    getSalaryDistribution.mockResolvedValue([])
    render(<DashboardPage onNavigate={vi.fn()} />)

    expect(await screen.findByText('No compensation summary is available.')).toBeInTheDocument()
    expect(screen.getAllByText('No compensation data is available.')).toHaveLength(2)
    expect(screen.getAllByText('No salary distribution data is available.')).toHaveLength(2)
  })

  it('shows an API error instead of partial analytics data', async () => {
    getCountryCompensation.mockRejectedValue(new Error('Analytics service unavailable'))
    render(<DashboardPage onNavigate={vi.fn()} />)

    expect(await screen.findByRole('alert')).toHaveTextContent('Analytics service unavailable')
    expect(screen.queryByText('Summary by Currency')).not.toBeInTheDocument()
  })

})