ready(() => {
  console.log("website.js ready() called.")
  hljs.highlightAll()
  document.querySelectorAll('pre.literal-block').forEach((el) => {
    hljs.highlightElement(el)
  })
}, {runOnHypergenPushstate: true})
