import $ from "jquery";
window.jQuery = $
window.$ = $

import morphdom from 'morphdom'
import './freedom'

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
        } else {
          return true
        }
      },
    }
  )
}                     

var eventHandlerCache = {}
export const setEventHandlerCache = function(id, newCache) {
  eventHandlerCache[id] = newCache
  console.log("Setting new state at", id, eventHandlerCache)
}

// Callback
var i = 0
export const callback = function(url, args, kwargs, {debounce=50}={}) {
  i++
  var args2 = []
  parseArgs(args, args2)
  console.log("REQUEST", url, args, kwargs, debounce)
  $.ajax({
    url: url,
    type: 'POST',
    data: JSON.stringify({
      args: args2,
      kwargs: kwargs,
      id_prefix: "h" + i + "-",
    }),
    contentType: 'application/json; charset=utf-8',
    dataType: 'json',
    headers: {
      'X-Requested-With': 'XMLHttpRequest'
    },
    success: function(data) {
      console.log("RESPONSE", data)
      if (data === null) return
      applyCommands(data)
    },
  })
}

// Internal
const parseArgs = function(args, data) {
    for (var i=0; i<args.length; i++) {
      var x = args[i]
      if (typeof x === "function") {
        data.push(x())  
      } else if (Array.isArray(x)) {
        if (x.length === 3 && x[0] === "_") {
          if(x[1] === "element_value") {
            let func = resolvePath(x[2].cb_name)
            data.push(func(x[2].id))
          } else {
            throw "Unknown custom data"
          }
        } else {
          var tmp = []
          parseArgs(x, tmp)
          data.push(tmp)
        }
      } else {
        data.push(x)
      }
    }
  }

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
      if (obj[part] !== undefined) obj = obj[part]
      else throw "Could not resolve path: " + path
    }
  }
  return obj
}

const applyCommand = function(path, ...args) {
    resolvePath(path)(...args)
}
window.e = function(targetId, dataId) {
  applyCommand(...eventHandlerCache[targetId][dataId])
}

const applyCommands = function(commands) {
  for (let [path, ...args] of commands) {
    applyCommand(path, ...args)
  }
}
window.applyCommands = applyCommands

const isDomEntity = entity => {
  return typeof entity === 'object' && entity.nodeType !== undefined
}

const mergeAttrs = function(target, source){
  source.getAttributeNames().forEach(name => {
    let value = source.getAttribute(name)
    target.setAttribute(name, value)
  })
}

// DOM element value readers
export const v = {}
v.i = function(id) { 
  const el = isDomEntity(id) ? $(id) : $("#" + id) 
  return parseInt(el.val())
}
v.f = function(id) { return 
  const el = isDomEntity(id) ? $(id) : $("#" + id) 
  return parseFloat(el.val())
}
v.s = function(id) { 
  const el = isDomEntity(id) ? $(id) : $("#" + id) 
  return "" + el.val().trim()
}
v.c = function(id) { 
  const el = isDomEntity(id) ? $(id) : document.getElementById(id) 
  return el.checked
}
v.g = function(id) { 
  const el = isDomEntity(id) ? $(id) : $("#" + id) 
  var v = el.val()
  var v1 = parseInt(v)
  return !isNaN(v1) ? v1 : v
}
v.t = function(id) { 
  const el = isDomEntity(id) ? $(id) : $("#" + id) 
  return "" + el.val().trim()
}

