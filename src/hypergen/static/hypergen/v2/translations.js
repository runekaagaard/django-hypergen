const translations = function(url, T) {
  // TODO: Dont clutter window.
  window.t = {T}
  
  window.t.post = function(a, b, b0) {
    let form = new FormData()
    form.append("hypergen_data", JSON.stringify({args: [a, b], meta: {}}))
    console.log("Translating", JSON.stringify(a), "to", JSON.stringify(b))
    post(
      url,
      form,
      () => { replaceInText(null, b0, (b === "RESET" ? a : b)); console.log("Server said, THANKYOUSE!") },
      () => { alert("Something went wrong when posting translation string to server.")},
      {},
    )
  }
  
  window.t.help = function() {
    console.log(`Hi user, you have the following commands:

    t.list() // Shows all translatable strings on this page and their reference number
    t.translate() // Runs t.list and then prompts for reference number and then translation.

Use "RESET" to reset back to the original content.
      `)
  }

  var stringsOnPage = function() {
    var html = document.body.innerHTML
    return T.filter(x => html.includes(x[1]))
  }
  
  window.t.list = function() {
    var xs = stringsOnPage()
    console.log("I found the following translatable strings on this page:\n\n" + xs.map(
      (x, i) => `${i}: ${x[0]}`).join("\n"))
  }
  window.t.translate = function() {
    var xs = stringsOnPage()
    window.t.list()
    i = Number(prompt("Which number string do you want to translate?"))
    if (i != 0 && !i) {
      console.error("Dont know that number", i, "try again!")
      return
    }
    var x = xs[i]
    if (!x) {
      console.error("Dont know that number", i, "try again!")
      return
    }
  
    var b = prompt("Input translation for: \n\n    '" + x[1] + "'", x[1])
    if (!b || b.trim() === "") {
      console.error("You did not write anything. Try again!")
      return
    }
    window.t.post(x[0], b, x[1])
  }
}

const replaceInText = function(element, pattern, replacement) {
  if (element === null) element = document.querySelector("body")
  
  for (let node of element.childNodes) {
    switch (node.nodeType) {
      case Node.ELEMENT_NODE:
        replaceInText(node, pattern, replacement);
        break;
      case Node.TEXT_NODE:
        node.textContent = node.textContent.replace(pattern, replacement);
        break;
      case Node.DOCUMENT_NODE:
        replaceInText(node, pattern, replacement);
    }
  }
}

// TODO: Dont clutter window.
window.translations = translations
