"""Small local SVG icons used by the static renderer."""
ICONS = {
    'pin': '<path d="M19 10c0 5-7 11-7 11S5 15 5 10a7 7 0 1114 0Z"/><circle cx="12" cy="10" r="2.3"/>',
    'doc': '<path d="M6 3h8l4 4v14H6zM14 3v5h4M9 12h6m-6 4h5"/>',
    'paper': '<path d="M3 5h16v14H5a2 2 0 01-2-2zm16 3h2v9a2 2 0 01-2 2M6 9h4v4H6zm7 0h3m-3 4h3m-10 3h10"/>',
    'out': '<path d="M7 17 18 6M8 6h10v10"/>',
    'arr': '<path d="m9 5 7 7-7 7"/>',
    'back': '<path d="m11 5-7 7 7 7m-7-7h16"/>',
    'city': '<path d="M3 21h18M5 21V9h14v12M4 9l8-6 8 6M9 12v4m6-4v4m-4 5v-4h2v4"/>',
    'district': '<circle cx="12" cy="6" r="3"/><circle cx="5" cy="17" r="3"/><circle cx="19" cy="17" r="3"/><path d="m7 14 3-5m4 0 3 5m-9 3h8"/>',
    'region': '<path d="m3 8 9-5 9 5-9 5zM3 12l9 5 9-5M3 16l9 5 9-5"/>',
    'state': '<path d="M5 21V4m0 1q4-3 8 0t7 0v9q-4 3-8 0t-7 0"/>',
    'federal': '<path d="m2 9 10-6 10 6zM4 20h16M6 12v5m4-5v5m4-5v5m4-5v5"/>',
    'europe': '<circle cx="12" cy="12" r="8.5"/><ellipse cx="12" cy="12" rx="4" ry="8.5"/><path d="M4 9h16M4 15h16"/>',
    'users': '<circle cx="9" cy="8" r="3"/><path d="M3 20v-2a6 6 0 0112 0v2m1-15a3 3 0 010 6m2 3a5 5 0 013 5"/>',
    'clock': '<circle cx="12" cy="12" r="8"/><path d="M12 7v5l3 2"/>',
    'check': '<path d="m4 12 5 5L20 6"/>',
}

def icon(k): return f'<svg class="{k}" aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round">{ICONS[k]}</svg>'

logo='<svg aria-hidden="true" viewBox="0 0 36 36" fill="none"><rect x="1" y="1" width="34" height="34" rx="8" stroke="#c8d8b8"/><path d="m7 22 7-11 6 4 9-5v6l-9 5-6-4-7 11z" fill="#d8e6bb"/><circle cx="26" cy="8" r="2" fill="#f2d591"/></svg>'
