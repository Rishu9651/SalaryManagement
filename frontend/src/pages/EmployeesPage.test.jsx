import { fireEvent, render, screen, waitFor, within } from '@testing-library/react'
import { beforeEach, describe, expect, it, vi } from 'vitest'

import {
  createEmployee,
  deactivateEmployee,
  listEmployees,
  updateEmployee,
} from '../api/employees'
import EmployeesPage from './EmployeesPage'

vi.mock('../api/employees', () => ({
  createEmployee: vi.fn(),
  deactivateEmployee: vi.fn(),
  listEmployees: vi.fn(),
  updateEmployee: vi.fn(),
}))

const employee = {
  id: 1,
  employee_code: 'EMP00001',
  first_name: 'Aisha',
  last_name: 'Patel',
  email: 'aisha@example.com',
  country: 'India',
  department: 'Engineering',
  job_title: 'Software Engineer',
  status: 'active',
}

const page = (items = [employee], overrides = {}) => ({
  items,
  total: items.length,
  page: 1,
  page_size: 25,
  total_pages: 1,
  ...overrides,
})

beforeEach(() => {
  vi.clearAllMocks()
  listEmployees.mockResolvedValue(page())
  createEmployee.mockResolvedValue(employee)
  updateEmployee.mockResolvedValue(employee)
  deactivateEmployee.mockResolvedValue({ ...employee, status: 'inactive' })
})

describe('EmployeesPage', () => {
  it('renders loading and then employee list data', async () => {
    let resolveRequest
    listEmployees.mockReturnValue(new Promise((resolve) => { resolveRequest = resolve }))
    render(<EmployeesPage />)

    expect(screen.getByText('Loading employees...')).toBeInTheDocument()
    resolveRequest(page())

    expect(await screen.findByText('EMP00001')).toBeInTheDocument()
    expect(screen.getByText('Aisha Patel')).toBeInTheDocument()
  })

  it('shows an API error', async () => {
    listEmployees.mockRejectedValue(new Error('Service unavailable'))
    render(<EmployeesPage />)

    expect(await screen.findByRole('alert')).toHaveTextContent('Service unavailable')
  })

  it('sends search and filter changes to the server and resets to page one', async () => {
    render(<EmployeesPage />)
    await screen.findByText('EMP00001')

    fireEvent.change(screen.getByPlaceholderText('Name, code, or email'), { target: { value: 'Aisha' } })
    fireEvent.change(screen.getByLabelText('Country'), { target: { value: 'India' } })

    await waitFor(() => expect(listEmployees).toHaveBeenLastCalledWith({
      page: 1,
      pageSize: 25,
      search: 'Aisha',
      country: 'India',
      department: '',
    }))
  })

  it('changes pages through the server-side pagination control', async () => {
    listEmployees.mockResolvedValueOnce(page([employee], { total: 26, total_pages: 2 }))
      .mockResolvedValueOnce(page([], { page: 2, total: 26, total_pages: 2 }))
    render(<EmployeesPage />)
    await screen.findByText('EMP00001')

    fireEvent.click(screen.getByRole('button', { name: 'Next' }))

    await waitFor(() => expect(listEmployees).toHaveBeenLastCalledWith({
      page: 2,
      pageSize: 25,
      search: '',
      country: '',
      department: '',
    }))
  })

  it('validates required fields before creating an employee', async () => {
    render(<EmployeesPage />)
    await screen.findByText('EMP00001')
    fireEvent.click(screen.getByRole('button', { name: 'Add Employee' }))
    fireEvent.click(screen.getByRole('button', { name: 'Add employee' }))

    expect(screen.getByRole('alert')).toHaveTextContent('Please complete all required fields.')
    expect(createEmployee).not.toHaveBeenCalled()
  })

  it('creates an employee and refreshes the list', async () => {
    render(<EmployeesPage />)
    await screen.findByText('EMP00001')
    fireEvent.click(screen.getByRole('button', { name: 'Add Employee' }))

    const dialog = screen.getByRole('dialog')
    const values = {
      employee_code: 'EMP00002', first_name: 'Raj', last_name: 'Khan',
      email: 'raj@example.com', country: 'India', department: 'Finance', job_title: 'Analyst',
    }
    Object.entries(values).forEach(([name, value]) => fireEvent.change(within(dialog).getByLabelText(new RegExp(name.replace('_', ' '), 'i')), { target: { value } }))
    fireEvent.click(within(dialog).getByRole('button', { name: 'Add employee' }))

    await waitFor(() => expect(createEmployee).toHaveBeenCalledWith(values))
    expect(await screen.findByText('Employee added successfully.')).toBeInTheDocument()
  })

  it('edits an employee without sending employee_code', async () => {
    render(<EmployeesPage />)
    await screen.findByText('EMP00001')
    fireEvent.click(screen.getByRole('button', { name: 'Edit' }))
    fireEvent.change(screen.getByRole('textbox', { name: /First name/i }), { target: { value: 'Amelia' } })
    fireEvent.click(screen.getByRole('button', { name: 'Save changes' }))

    await waitFor(() => expect(updateEmployee).toHaveBeenCalledWith(1, expect.objectContaining({ first_name: 'Amelia' })))
    expect(updateEmployee.mock.calls[0][1]).not.toHaveProperty('employee_code')
  })

  it('confirms before deactivating an employee', async () => {
    window.confirm = vi.fn(() => false)
    render(<EmployeesPage />)
    await screen.findByText('EMP00001')
    fireEvent.click(screen.getByRole('button', { name: 'Deactivate' }))
    expect(window.confirm).toHaveBeenCalledWith('Deactivate Aisha Patel?')
    expect(deactivateEmployee).not.toHaveBeenCalled()

    window.confirm = vi.fn(() => true)
    fireEvent.click(screen.getByRole('button', { name: 'Deactivate' }))
    await waitFor(() => expect(deactivateEmployee).toHaveBeenCalledWith(1))
  })
})