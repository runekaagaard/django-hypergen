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
    if (href2.startsWith("http") || visited.indexOf(href2) !== -1 || href2.startsWith("#")) continue
    console.log(`    adding ${href2} to queue`)
    queue.push(href2)
  }
}

test('test', async t => {
  while(queue.length > 0) {
    const href = queue.pop()
    console.log(`testing url: ${href}`)
    await t
      .navigateTo(href)
      .expect(logger.contains(r => r.response.statusCode === 200)).ok()
    await visitPage(t, href)
    logger.clear()
  }
})
