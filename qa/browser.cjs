// Optional maintenance check. The published site does not depend on Playwright.
// Set PLAYWRIGHT_MODULE to an installed Playwright module, or install it in your
// testing environment. First argument: the local HTTP project directory URL.
const assert = require('node:assert/strict');
const { chromium } = require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const base = new URL(process.argv[2] || 'http://127.0.0.1:8791/');
if (!base.pathname.endsWith('/')) base.pathname += '/';
if (!['localhost', '127.0.0.1', '[::1]'].includes(base.hostname)) {
  throw new Error('Run only against a local test address.');
}

async function main() {
  const browser = await chromium.launch(
    process.env.BROWSER_CHANNEL ? { channel: process.env.BROWSER_CHANNEL } : {}
  );
  try {
    const context = await browser.newContext({ viewport: { width: 390, height: 844 } });
    const page = await context.newPage();
    const failed = [];
    page.on('pageerror', error => failed.push(error.message));
    context.on('request', request => {
      if (!request.url().startsWith(base.href)) failed.push(request.url());
    });
    const response = await page.goto(base.href);
    assert.equal(response.status(), 200);
    assert.equal(await page.locator('h1').innerText(), 'Bobingen');
    assert.equal(await page.locator('article.card').count(), 3);
    await page.keyboard.press('Tab');
    assert.equal(await page.locator(':focus').textContent(), 'Skip to content');
    await page.keyboard.press('Enter');
    assert.equal(await page.locator(':focus').getAttribute('id'), 'content');

    const mobileLink = page.getByRole('link', { name: 'Who represents me?', exact: true });
    const position = await mobileLink.boundingBox();
    assert.ok(position.y >= 0 && position.y + position.height <= 844);
    await mobileLink.click();
    assert.match(page.url(), /bobingen-representatives\.html$/);
    await page.getByText('Choose a level of government').click();
    await page.getByRole('navigation', { name: 'Levels of government' })
      .getByRole('link', { name: 'EU', exact: true }).click();
    await page.locator('#europe .mobile-level-return a').click();
    assert.equal(await page.locator(':focus').getAttribute('id'), 'levels-menu');
    assert.ok(await page.getByRole('navigation', { name: 'Levels of government' }).isVisible());
    await page.getByRole('navigation', { name: 'Levels of government' })
      .getByRole('link', { name: 'Germany', exact: true }).click();
    assert.match(page.url(), /#federal$/);
    await page.getByRole('link', { name: 'Augsburg', exact: true }).click();
    assert.match(page.url(), /augsburg-representatives\.html$/);
    assert.equal(await page.locator('#district').count(), 0);
    await page.getByText('Choose a level of government').click();
    await page.getByRole('navigation', { name: 'Levels of government' })
      .getByRole('link', { name: /Swabia/ }).click();
    await page.getByRole('link', { name: 'Find your city district' }).click();
    const input = page.getByRole('combobox', { name: 'Your city district' });
    await input.selectOption('06');
    assert.match(await page.getByRole('status').innerText(), /Leo Dietz/);
    await input.selectOption('32');
    assert.match(await page.getByRole('status').innerText(), /Erwin Gerblinger/);
    await input.selectOption('');
    assert.equal(await page.getByRole('status').innerText(), '');

    // Compare matching levels; Augsburg handles county-level duties as a city.
    await page.locator('#federal .compare a').click();
    assert.match(page.url(), /bobingen-representatives\.html#federal$/);
    await page.locator('#district .compare a').click();
    assert.match(page.url(), /augsburg-representatives\.html#city$/);
    assert.match(await page.locator('#city').innerText(), /independent city/i);

    const routes = ['', 'augsburg.html', 'bobingen-representatives.html',
      'augsburg-representatives.html', 'sources-bobingen.html', 'sources-augsburg.html'];
    for (const width of [320, 768, 1366]) {
      await page.setViewportSize({ width, height: 844 });
      for (const route of routes) {
        await page.goto(new URL(route, base).href);
        assert.ok(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth),
          'Horizontal overflow: ' + width + ' · ' + route);
      }
    }
    assert.deepEqual(failed, []);

    const noJS = await browser.newContext({
      javaScriptEnabled: false, viewport: { width: 320, height: 844 }
    });
    const plain = await noJS.newPage();
    await plain.goto(new URL('augsburg-representatives.html#constituency', base).href);
    assert.equal(await plain.locator('#district-controls').isVisible(), false);
    await plain.getByText('Browse all 42 city districts').click();
    assert.ok(await plain.getByRole('rowheader', { name: '42 Bergheim' }).isVisible());
    const lookupTable = plain.getByRole('table', { name: 'City districts in number order' });
    assert.equal(await lookupTable.getByRole('rowheader').count(), 42);
    await lookupTable.getByRole('row', { name: /06 Rechts der Wertach/ }).getByRole('link').click();
    assert.match(await plain.locator(':target').innerText(), /Leo Dietz/);
    await lookupTable.getByRole('row', { name: /12 Siebenbrunn/ }).getByRole('link').click();
    assert.match(await plain.locator(':target').innerText(), /Erwin Gerblinger/);
    await plain.goto(new URL('bobingen-representatives.html#europe', base).href);
    await plain.locator('#europe .mobile-level-return a').click();
    assert.equal(await plain.locator(':focus').getAttribute('id'), 'levels-menu');
    await plain.getByRole('navigation', { name: 'Levels of government' })
      .getByRole('link', { name: 'Bavaria', exact: true }).click();
    assert.match(await plain.locator(':target').innerText(), /Carolina Trautner/);
    console.log('City switching, subpath, keyboard, districts, mobile widths and JavaScript-free access: OK');
  } finally {
    await browser.close();
  }
}

main().catch(error => { console.error(error); process.exitCode = 1; });
