import { Selector, ClientFunction, RequestLogger } from 'testcafe';

const url = "http://127.0.0.1:8002/"

const logger = RequestLogger();

fixture("Test All")
  .page(url)
  .requestHooks(logger);

var queue = ["/"]
var visited = []

async function visitPage(t, href) {
  console.log("visiting new page:", href)
  visited.push(href)
  
  const links = Selector('a')
  const count = await links.count
  console.log(`    found ${count} links`)
  
  for (let i = 0; i < count; i++) {
    const link = await links.nth(i)
    const href2 = await link.getAttribute("href")
    const onclick = await link.getAttribute("onclick")
    if (href2.startsWith("http") || visited.indexOf(href2) !== -1 || href2.startsWith("#") || !!onclick) continue
    console.log(`    adding ${href2} to queue`)
    queue.push(href2)
  }
}

async function onclickEvents(t, href) {
  // TODO: Make todomvc work.
  if (["/gameofcython/", "/t9n/", "/todomvc/"].indexOf(href) !== -1) return
  const els = Selector('*').withAttribute('onclick')
  const count = await els.count
  for (let i = 0; i < count; i++) {
    const el = await els.nth(i)
    const onclick = await el.getAttribute("onclick")
    if (onclick.includes("redirect__")) continue
    console.log(`    running onclick event: ${onclick}`, i)
    await t
      .setNativeDialogHandler(() => true)
      .click(el)
      .expect(logger.contains(r => r.response.statusCode === 200)).ok()
    logger.clear()
  }
}

test('test', async t => {
  while(queue.length > 0) {
    const href = queue.pop()
    console.log(`testing url: ${href}`)
    await t
      .navigateTo(href)
      .expect(logger.contains(r => r.response.statusCode === 200)).ok()
    logger.clear()
    await onclickEvents(t, href)
    await visitPage(t, href)
  }
})
