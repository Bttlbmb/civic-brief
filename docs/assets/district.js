// Optional enhancement. The native disclosure holds the complete static answer.
(() => {
  const controls = document.getElementById('district-controls');
  if (!controls) return;
  const select = document.getElementById('district-choice');
  const output = document.getElementById('district-answer');
  const results = new Map(
    [...document.querySelectorAll('[data-result]')].map(el => [el.dataset.result, el])
  );

  function update() {
    const result = results.get(select.selectedOptions[0]?.dataset.half);
    output.replaceChildren();
    if (!result) return;
    const title = document.createElement('strong');
    title.textContent = 'Your constituency: ' + result.querySelector('h4').textContent;
    output.append(title, result.querySelector('.mandates').cloneNode(true));
  }
  controls.hidden = false;
  select.addEventListener('change', update);
  window.addEventListener('pageshow', update);
  update();
})();
