import morphdom from 'morphdom'
// https://github.com/ccampbell/mousetrap
import mousetrap from 'mousetrap'
import './hypergen'
import * as hypergen from './hypergen'

// Make all exported vars availabe in window.hypergen.
window.hypergen = hypergen

// Shims
if (typeof Array.isArray === 'undefined') {
  Array.isArray = function(obj) {
    return Object.prototype.toString.call(obj) === '[object Array]';
  }
}

// Commands that can be called from the backend.
export const morph = function(id, html) {
  morphdom(
    document.getElementById(id),
    "<div>" + html + "</div>",
    {
      childrenOnly: true,
      onBeforeElUpdated: function(fromEl, toEl) {
        let focused = document.activeElement
        if((fromEl.nodeName == "INPUT" || fromEl.nodeName == "TEXTAREA") && fromEl === focused) {
          let types = ["checkbox", "radio"]
          if (fromEl.nodeName === "INPUT" && types.indexOf(fromEl.type) !== -1) {
            return true
          }
          mergeAttrs(fromEl, toEl)
          return false
        } else if (fromEl.nodeName == "INPUT" && fromEl.type === "file" && fromEl.files.length > 0) {
          mergeAttrs(fromEl, toEl)
          return false
        } else if (fromEl.nodeName === "SCRIPT" && toEl.nodeName === "SCRIPT") {
            var script = document.createElement('script');
            //copy over the attributes
            [...toEl.attributes].forEach( attr => { script.setAttribute(attr.nodeName ,attr.nodeValue) })
            script.innerHTML = toEl.innerHTML;
            fromEl.replaceWith(script)
            return false;
        } else {
          return true
        }
      },
      onNodeAdded: function (node) {
        if (node.nodeName === 'SCRIPT') {
          var script = document.createElement('script');
          //copy over the attributes
          [...node.attributes].forEach( attr => { script.setAttribute(attr.nodeName ,attr.nodeValue) })
          script.innerHTML = node.innerHTML;
          node.replaceWith(script)
        }
      },
    }
  )

  const autofocus = document.querySelectorAll('[autofocus]')[0]
  if (autofocus !== undefined) autofocus.focus()
}

export const remove = function(id) {
  let el = document.getElementById(id);
  el.parentNode.removeChild(el)
}

export const hide = function(id) {
  let el = document.getElementById(id)
  el.style.display = "none"
}

export const display = function(id, value) {
  let el = document.getElementById(id)
  el.style.display = value || "block"
}

export const redirect = function(url) {
  window.location = url
}

// TODO: Dont clutter window.
window.clientState = {}
export const setClientState = function(at, value) {
  let clientState = window.clientState
  for (const path of at.split(".")) {
    if (clientState.path === undefined) clientState[path] = {}
    clientState = clientState[path]
  }
  Object.assign(clientState, value)
  console.log("Setting new state for window.clientState", at, "with value", value, "giving",
              window.clientState)
}

// Callback
var i = 0
var isBlocked = false
export const callback = function(url, args, {debounce=0, confirm_=false, blocks=false, uploadFiles=false,
                                             params={}, meta={}, clear=false, elementId=null, debug=false}={}) {
  let postIt = function() {
    let json
    console.log("REQUEST", url, args, debounce)
    i++

    // The element function must have access to the FormData.
    // TODO: Dont clutter window.
    window.hypergenGlobalFormdata = new FormData()
    window.hypergenUploadFiles = uploadFiles
    try {
      json = JSON.stringify({
        args: args,
        meta: meta,
      })
    } catch(error) {
      if (error === MISSING_ELEMENT_EXCEPTION) {
        console.warn("An element is missing. This can happen if a dom element has multiple event handlers.", url)
        return
      } else {
        throw(error)
      }
    }
    
    let formData = window.hypergenGlobalFormdata
    window.hypergenGlobalFormdata = null
    window.hypergenUploadFiles = null
    formData.append("hypergen_data", json)

    if (blocks === true) {
      if (isBlocked === true) {
        console.error("Callback was blocked")
        return
      } else {
        isBlocked = true
      }
    }
    post(url, formData, (data) => {
      console.log("RESPONSE", data)
      if (data !== null) applyCommands(data)
      isBlocked = false
      if (clear === true) document.getElementById(elementId).value = ""
    }, (data, jsonOk, xhr) => {
      isBlocked = false
      console.error("Hypergen post error occured", data)
      if (debug !== true) {
        if (xhr.getResponseHeader("Content-Type") === "text/plain") {
          data = "<pre><code>" + data + "</pre></code>"
        }
        document.getElementsByTagName("html")[0].innerHTML = data
      }
    }, params)
  }
  if (debounce === 0) {
    if (confirm_ === false) postIt()
    else if (confirm(confirm_)) postIt()
  }
  else throttle(postIt, {delay: debounce, group: url, confirm_}) 
}

// Timing
var _THROTTLE_GROUPS = {}
export let throttle = function (func, {delay=0, group='global', confirm_=false}={}) {
  if (_THROTTLE_GROUPS[group]) {
    clearTimeout(_THROTTLE_GROUPS[group])
    _THROTTLE_GROUPS[group] = null
  }

  _THROTTLE_GROUPS[group] = setTimeout(function () {
      if (confirm_ === false) {
        func()
      } else {
        const confirmed = confirm(confirm_)
        if (confirmed === true) {
          func()
        }
      }
      _THROTTLE_GROUPS[group] = null
    }, delay)
}

export let cancelThrottle = function(group) {
  if (_THROTTLE_GROUPS[group]) {
    clearTimeout(_THROTTLE_GROUPS[group])
    _THROTTLE_GROUPS[group] = null
  }
}

// Internal

const require_ = function(module) {
  try {
    return require(module)
  } catch(e) {
    return false
  }
}

const resolvePath = function(path) {
  const parts = path.split(".")
  let i = -1, obj = null
  for (let part of parts) {
    i++
    if (i === 0) {
      if (window[part] !== undefined) obj = window[part]
      else if (obj = require_(part)) null
      else if (obj = require_("./" + part)) null
      else throw "Could not resolve path: " + path
    } else {
      if (obj[part] !== undefined) {
        try {
          obj = obj[part].bind(obj)
        } catch(e) {
          obj = obj[part]
        }
      }
      else throw "Could not resolve path: " + path
    }
  }
  return obj
}

const applyCommand = function(path, ...args) {
  console.log("apply command", path, args)
  let rpath = resolvePath(path)
  rpath(...args)
  const event = new CustomEvent('hypergen.applyCommand.after', {detail: {path, args}})
  document.dispatchEvent(event)
}

// TODO: Dont clutter window.
window.e = function(event, callbackKey, eventMatches) {
  event.preventDefault()
  event.stopPropagation()
  if (!!eventMatches) {
    for (const k in eventMatches) {
      if (eventMatches[k] !== event[k]) {
        return
      }
    }
  }
  applyCommand(...window.clientState.hypergen.eventHandlerCallbacks[callbackKey])
}

const applyCommands = function(commands) {
  for (let [path, ...args] of commands) {
    applyCommand(path, ...args)
  }
}
// TODO: Dont clutter window.
window.applyCommands = applyCommands

const mergeAttrs = function(target, source){
  source.getAttributeNames().forEach(name => {
    let value = source.getAttribute(name)
    target.setAttribute(name, value)
  })
}

const MISSING_ELEMENT_EXCEPTION = "MISSING_ELEMENT_EXCEPTION" 

// coerce functions
export const coerce = {}
coerce.no = function(value) {
  if (value === "") return null
  return value
}
coerce.str = function(value) {
  if (value === "") return null
  return value === null ? null : "" + value
}
coerce.int = function(value) {
  if (value === "") return null
  value = parseInt(value)
  if (isNaN(value)) return null
  else return value
}
coerce.float = function(value) {
  if (value === "") return null
  value = parseFloat(value)
  if (isNaN(value)) return null
  else return {_: ["float", value]}
}
coerce.date = function(value) {
  if (value === "") return null
  else return {_: ["date", value]}
}
coerce.datetime = function(value) {
  if (value === "") return null
  else return {_: ["datetime", value]}
}
coerce.time = function(value) {
  if (value === "") return null
  else return {_: ["time", value]}
}
coerce.month = function(value) {
  if (value === "") return null
  const parts = value.split("-")
  return {year: parseInt(parts[0]), month: parseInt(parts[1])}
}
coerce.week = function(value) {
  if (value === "") return null
  const parts = value.split("-")
  return {year: parseInt(parts[0]), week: parseInt(parts[1].replace("W", ""))}
}


// DOM element value readers
export const read = {}
read.value = function(id) { // value attribute
  const el = document.getElementById(id)
  if (el === null) {
    throw MISSING_ELEMENT_EXCEPTION
  }
  return el.value.trim()
}
read.checked = function(id) { // checkbox
  const el = document.getElementById(id)
  if (el === null) {
    throw MISSING_ELEMENT_EXCEPTION
  }
  return el.checked
}
read.radio = function(id) { // radio button. Uses name attribute for value.
  const el = document.getElementById(id)
  if (el === null) {
    throw MISSING_ELEMENT_EXCEPTION
  }
  const checked = document.querySelector("input[type=radio][name=" + el.name + "]:checked")
  return checked === null ? null : checked.value
}
read.file = function(id, formData) { // file upload
  const el = document.getElementById(id)
  if (el === null) {
    throw MISSING_ELEMENT_EXCEPTION
  }
  if (el.files.length !== 1) return null
  if (window.hypergenUploadFiles === true) formData.append(id, el.files[0])
  return el.files[0].name
}

export const element = function(valueFunc, coerceFunc, id) {
  this.toJSON = function() {
    const value = resolvePath(valueFunc)(id, window.hypergenGlobalFormdata)
    if (!!coerceFunc) return resolvePath(coerceFunc)(value)
    else return coerce.no(value)
  }
  return this
}

const reviver = function(k, v) {
  if (Array.isArray(v)) {
    if (v.length === 3 && v[0] === "_") {
      if(v[1] === "element_value") {
        return new element(...v[2])
      }
    }
  }
  return v
}
// TODO: Dont clutter window.
window.reviver = reviver

const getCookie = function(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function addParams(url, params) {
  const ret = []
  for (let d in params)
    ret.push(encodeURIComponent(d) + '=' + encodeURIComponent(params[d]))
  if (ret.length === 0) return url
  else return url + "?" + ret.join('&')
}

export const post = function(url, formData, onSuccess, onError, params) {
  url = addParams(url, params)
  
  const xhr = new XMLHttpRequest()
  const progressBar = document.getElementById("hypergen-upload-progress-bar")

  if (progressBar !== null) {
    xhr.upload.onload = () => {
      progressBar.style.visibility = "hidden"
      console.log(`The upload is completed: ${xhr.status} ${xhr.response}`)
    }

    xhr.upload.onerror = () => {
      progressBar.style.visibility = "hidden"
      console.error('Upload failed.')

    }

    xhr.upload.onabort = () => {
      progressBar.style.visibility = "hidden"
      console.error('Upload cancelled.')
    }

    xhr.upload.onprogress = (event) => {
      progressBar.style.visibility = "visible"
      progressBar.value = event.loaded / event.total
      console.log(`Uploaded ${event.loaded} of ${event.total} bytes`)
    }
  }

  xhr.onload = () => {
    var jsonOk = false,
        data = null
    try {
      data = JSON.parse(xhr.responseText, reviver)
      jsonOk = true
    } catch(e) {
      data = xhr.responseText
      jsonOk = false
    }
    if (xhr.readyState == 4 && xhr.status == 200) {
      onSuccess(data, xhr)
    } else {
      onError(data, jsonOk, xhr);
    }
  }

  // TODO
  xhr.onerror = () => {
    onError()
  }

  xhr.onabort = () => {
    console.error('xhr aborted')
  }

  xhr.open('POST', url)
  xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
  xhr.setRequestHeader('X-Pathname', parent.window.location.pathname);
  xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
  xhr.send(formData)
}

// history support.

window.addEventListener("popstate", function(event) {
  if (event.state && event.state.callback_url !== undefined) {
    callback(event.state.callback_url, [], {meta: {is_popstate: true}})
  } else {
    window.location = location.href
  }
})

const pushstate = new Event('hypergen.pushstate')

export const onpushstate = function() {
  document.dispatchEvent(pushstate)
}

// Translations
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
// TODO: Dont clutter window.
window.translations = translations

// On ready

export const ready = function(fn, {partial=false}={}) {
  if (document.readyState != 'loading') {
    fn();
  } else if (document.addEventListener) {
    document.addEventListener('DOMContentLoaded', fn);
  } else {
    document.attachEvent('onreadystatechange', function() {
      if (document.readyState != 'loading')
        fn();
    });
  }
  if (partial) document.addEventListener("hypergen.pushstate", fn)
}
// TODO: Dont clutter window.
window.ready = ready
