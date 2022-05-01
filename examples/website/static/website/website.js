ready(() => {
  hljs.highlightAll()
  document.querySelectorAll('pre.literal-block').forEach((el) => {
    hljs.highlightElement(el)
  })
})
