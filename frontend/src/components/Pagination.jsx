function Pagination({ page, totalPages, onPageChange }) {
  return (
    <nav className="pagination" aria-label="Employee pages">
      <button type="button" onClick={() => onPageChange(page - 1)} disabled={page <= 1}>Previous</button>
      <span>Page {page} of {totalPages || 1}</span>
      <button type="button" onClick={() => onPageChange(page + 1)} disabled={page >= totalPages}>Next</button>
    </nav>
  )
}

export default Pagination