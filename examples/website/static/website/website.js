hypergen.ready(() => {
  console.log("OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOo")
  console.log("website.js ready() called.")
  hljs.configure({ignoreUnescapedHTML: true})
  hljs.highlightAll()
  document.querySelectorAll('pre.literal-block').forEach((el) => {
    hljs.highlightElement(el)
  })
}, {partial: true})
