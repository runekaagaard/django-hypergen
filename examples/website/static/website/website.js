hljs.highlightAll()

document.addEventListener('DOMContentLoaded', (event) => {
    document.querySelectorAll('pre.literal-block').forEach((el) => {
      hljs.highlightElement(el)
    })
})
