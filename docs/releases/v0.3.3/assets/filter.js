'use strict';
// Local text filtering only. No requests, uploads, storage or telemetry.
const field = document.getElementById('filter');
if (field) {
  const entries = Array.from(document.querySelectorAll('.entry'));
  const status = document.getElementById('filter-status');
  function filter() {
    const query = field.value.trim().toLowerCase();
    let visible = 0;
    entries.forEach(entry => {
      entry.hidden = !entry.textContent.toLowerCase().includes(query);
      if (!entry.hidden) visible += 1;
    });
    status.textContent = `${visible} of ${entries.length} entries shown`;
  }
  function reveal(hash) {
    const target = document.getElementById(decodeURIComponent(hash.slice(1)));
    if (target && target.closest('.entry')?.hidden) {
      field.value = '';
      filter();
    }
  }
  field.addEventListener('input', filter);
  document.addEventListener('click', event => {
    const anchor = event.target.closest('a[href^="#"]');
    if (anchor) reveal(anchor.getAttribute('href'));
  });
  window.addEventListener('hashchange', () => reveal(location.hash));
}
