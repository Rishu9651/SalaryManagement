import { describe, expect, it } from 'vitest'

import { formatCurrency, formatDate, formatStatus } from './formatters'

describe('formatters', () => {
  it('formats API dates without changing the stored value', () => {
    expect(formatDate('2026-04-01')).toBe('01 Apr 2026')
    expect(formatDate(null)).toBe('-')
  })

  it('formats money using the supplied currency without conversion', () => {
    expect(formatCurrency('1500000.00', 'INR')).toContain('₹')
    expect(formatCurrency('95000.00', 'USD')).toContain('$')
    expect(formatCurrency('95000.00', 'USD')).not.toBe(formatCurrency('95000.00', 'INR'))
  })

  it('makes status text readable', () => {
    expect(formatStatus('active')).toBe('Active')
    expect(formatStatus('inactive')).toBe('Inactive')
  })
})