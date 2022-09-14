import { Selector, ClientFunction, RequestLogger } from 'testcafe';

const url = "http://127.0.0.1:8002/"

const logger = RequestLogger();

fixture("Test All")
  .page(url)
  .requestHooks(logger);

var queue = ["/documentation/", "/misc/index/"]
var visited = []

async function visitPage(t, href) {
  await t
    .navigateTo(href)
    .expect(logger.contains(r => r.response.statusCode === 200)).ok()
  console.log("visiting new page:", href)
  visited.push(href)
  const links = Selector('a')
  const count = await links.count
  console.log(`    found ${count} links`)
  
  for (let i = 0; i < count; i++) {
    const link = await links.nth(i)
    const href2 = await link.getAttribute("href")
    if (!href2) continue
    const onclick = await link.getAttribute("onclick")
    if (href2.startsWith("http") || visited.indexOf(href2) !== -1 || href2.startsWith("#") ||
        href2.startsWith("localhost"))
    {
      continue
    }
    console.log(`    adding ${href2} to queue`)
    queue.push(href2)
  }
}

async function onclickEvents(t, href) {
  if (["/gameofcython/", "/t9n/", "/djangotemplates/", "/misc/v19/", "/misc/v16/"].indexOf(href) !== -1) return
  await t
      .navigateTo(href)
      .expect(logger.contains(r => r.response.statusCode === 200)).ok()
  const els = Selector('*').withAttribute('onclick')
  const count = await els.count
  for (let i = 0; i < count; i++) {
    const el = await els.nth(i)
    const onclick = await el.getAttribute("onclick")
    if (onclick.includes("redirect__")) continue
    if (["hypergen.event(event, 'b3__onclick')"].indexOf(onclick) !== -1) continue
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
    if (["/djangolander/lander/", "/misc/v13/", "/misc/v14/",
         "/misc/v15/", "/gameofcython/", "/djangotemplates/"].indexOf(href) !== -1) continue
    console.log(`testing url: ${href}`)
    
    logger.clear()
    await onclickEvents(t, href)
    await visitPage(t, href)
  }
})

