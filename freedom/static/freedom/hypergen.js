import $ from "jquery";
window.jQuery = $
window.$ = $

import morphdom from 'morphdom'
import './hypergen'

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
  el.parentNode.removeChild(el);
}

export const hide = function(id) {
  let el = document.getElementById(id);
  el.style.display = "none"
}

export const redirect = function(url) {
  window.location = url
}

window.eventHandlerCache = {}
export const setEventHandlerCache = function(id, newCache) {
  if (window.eventHandlerCache[id] === undefined) {
    window.eventHandlerCache[id] = {}
  }
  window.eventHandlerCache[id] = Object.assign(window.eventHandlerCache[id], newCache)
  console.log("Setting new state at", id, window.eventHandlerCache)
}

// Callback
var i = 0
var isBlocked = false
export const callback = function(url, args, {debounce=0, confirm_=false, blocks=false, uploadFiles=false,
                                             params={}, meta={}, clear=false, elementId=null}={}) {
  let postIt = function() {
    let json
    console.log("REQUEST", url, args, debounce)
    i++

    // The element function must have access to the FormData.
    window.hypergenGlobalFormdata = new FormData()
    window.hypergenUploadFiles = uploadFiles
    try {
      json = JSON.stringify({
        args: args,
        meta: meta,
        id_prefix: "h" + i + "-",
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
      console.log("BLOCKS")
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
    }, (data) => {
      isBlocked = false
      console.error("Hypergen post error occured")
      document.getElementsByTagName("html")[0].innerHTML = data
    }, params)
  }
  throttle(postIt, {delay: debounce, group: url, confirm_})
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
}
window.e = function(event, targetId, dataId, eventMatches) {
  event.preventDefault()
  event.stopPropagation()
  if (!!eventMatches) {
    for (const k in eventMatches) {
      if (eventMatches[k] !== event[k]) {
        return
      }
    }
  }
  applyCommand(...window.eventHandlerCache[targetId][dataId])
}

const applyCommands = function(commands) {
  for (let [path, ...args] of commands) {
    applyCommand(path, ...args)
  }
}
window.applyCommands = applyCommands

const mergeAttrs = function(target, source){
  source.getAttributeNames().forEach(name => {
    let value = source.getAttribute(name)
    target.setAttribute(name, value)
  })
}

const MISSING_ELEMENT_EXCEPTION = "MISSING_ELEMENT_EXCEPTION" 

// DOM element value readers
export const v = {}
v.i = function(id) { 
  const el = $(document.getElementById(id))
  return parseInt(el.val())
}
v.f = function(id) {
  const el = $(document.getElementById(id))
  if (el.val() === undefined) {
    throw MISSING_ELEMENT_EXCEPTION
  }
  return parseFloat(el.val())
}
v.s = function(id) {
  const el = $(document.getElementById(id)) 
  if (el.val() === undefined) {
    throw MISSING_ELEMENT_EXCEPTION
  }
  return "" + el.val().trim()
}
v.c = function(id) { 
  const el = document.getElementById(id)
  if (el.val() === undefined) {
    throw MISSING_ELEMENT_EXCEPTION
  }
  return el.checked
}
v.g = function(id) { 
  const el = $(document.getElementById(id))
  if (el.val() === undefined) {
    throw MISSING_ELEMENT_EXCEPTION
  }
  var v = el.val()
  var v1 = parseInt(v)
  return !isNaN(v1) ? v1 : v
}
v.t = function(id) { 
  const el = $(document.getElementById(id))
  if (el.val() === undefined) {
    throw MISSING_ELEMENT_EXCEPTION
  }
  return "" + el.val().trim()
}
v.r = function(id) {
  const el = $(document.getElementById(id))
  if (el.val() === undefined) {
    throw MISSING_ELEMENT_EXCEPTION
  }
  const v = $("input:radio[name ='" + el.attr("name") + "']:checked").val()
  return v === undefined ? null : v
}
v.u = function(id, formData) {
  const el = document.getElementById(id)
  if (el.val() === undefined) {
    throw MISSING_ELEMENT_EXCEPTION
  }
  if (el.files.length !== 1) return null
  if (window.hypergenUploadFiles === true) formData.append(id, el.files[0])
  return el.files[0].name
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

export const element = function(valueFunc, id) {
  this.toJSON = function() {
    return resolvePath(valueFunc)(id, window.hypergenGlobalFormdata)
  }
  return this
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
      onError(data, jsonOk);
    }
  }

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

window.addEventListener("popstate", function(event) {
  if (event.state && event.state.callback_url !== undefined) {
    callback(event.state.callback_url, [], {meta: {is_popstate: true}})
  } else {
    window.location = location.href
  }
})
