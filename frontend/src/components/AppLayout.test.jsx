import { fireEvent, render, screen } from '@testing-library/react'
import { describe, expect, it, vi } from 'vitest'

import AppLayout from './AppLayout'

describe('AppLayout', () => {
  it('marks the active page and navigates from the main navigation', () => {
    const onNavigate = vi.fn()
    render(<AppLayout activePage="employees" onNavigate={onNavigate}>Content</AppLayout>)

    expect(screen.getByRole('button', { name: 'Employees' })).toHaveAttribute('aria-current', 'page')
    fireEvent.click(screen.getByRole('button', { name: 'Dashboard' }))
    expect(onNavigate).toHaveBeenCalledWith('dashboard')
  })
})