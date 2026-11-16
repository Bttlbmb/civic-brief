// Progressive enhancement: all contact information is available without JavaScript.
(() => {
  const issues = [...document.querySelectorAll('details.issue')];
  if (!issues.length) return;
  const applyHash = (focus = false) => {
    let target;
    try { target = document.getElementById(decodeURIComponent(location.hash.slice(1))); }
    catch { return; }
    if (!target || !issues.includes(target)) return;
    target.open = true;
    if (focus) target.querySelector('summary').focus({ preventScroll: true });
    target.scrollIntoView({ block: 'start' });
  };
  issues.forEach(issue => { issue.open = false; });
  applyHash(Boolean(location.hash));
  addEventListener('hashchange', () => applyHash(true));
})();
