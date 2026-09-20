function AppLayout({ activePage, onNavigate, children }) {
  return (
    <div className="app-shell">
      <header className="app-header">
        <div className="brand-lockup">
          <span className="brand-mark">A</span>
          <div><strong>ACME</strong><span>Salary Management</span></div>
        </div>
        <nav className="main-nav" aria-label="Main navigation">
          <button type="button" className={activePage === 'dashboard' ? 'nav-link active' : 'nav-link'} aria-current={activePage === 'dashboard' ? 'page' : undefined} onClick={() => onNavigate('dashboard')}>Dashboard</button>
          <button type="button" className={activePage === 'employees' ? 'nav-link active' : 'nav-link'} aria-current={activePage === 'employees' ? 'page' : undefined} onClick={() => onNavigate('employees')}>Employees</button>
        </nav>
      </header>
      <div className="app-content">{children}</div>
    </div>
  )
}

export default AppLayout