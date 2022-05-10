hypergen.ready(() => {
  console.log("website.js ready() called.")
  hljs.configure({ignoreUnescapedHTML: true})
  hljs.highlightAll()
  document.querySelectorAll('pre.literal-block').forEach((el) => {
    hljs.highlightElement(el)
  })
}, {partial: true})

window.showTerminal = function(outer, inner, a) {
  document.querySelectorAll("#" + outer + " pre").forEach((x) => x.style.display = "none")
  document.querySelectorAll("#" + inner).forEach((x) => x.style.display = "block")
  document.querySelectorAll("#" + outer + " a").forEach((x) => x.classList.remove("selected"))
  document.getElementById(a).classList.add("selected")
}
