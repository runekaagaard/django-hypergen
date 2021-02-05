import $ from "jquery";
window.jQuery = $
window.$ = $

import morphdom from 'morphdom'

import './freedom'

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

export const setEventHandlerCache = function(id, newCache) {
  H.e[id] = newCache
  console.log("Setting new state at", id, H.e)
}

export const addCallback = function(url, id, eventName, cbArgs, cbKwargs, {debounce=50}={}) {
  console.log("Adding callback", url, id, eventName, cbArgs, cbKwargs, debounce)
  document.getElementById(id).addEventListener(eventName, () => {
    H.cb(url, cbArgs, cbKwargs)
    console.log("GOT EVENT!!!", url, cbArgs, cbKwargs)
  })
}

// Other stuff.

const required = function(module) {
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
      else if (obj = required(part)) null
      else if (obj = required("./" + part)) null
      else throw "Could not resolve path: " + path
    } else {
      if (obj[part] !== undefined) obj = obj[part]
      else throw "Could not resolve path: " + path
    }
  }
  return obj
}

const applyCommands = function(commands) {
  for (let [path, ...args] of commands) {
    resolvePath(path)(...args)
  }
}
window.applyCommands = applyCommands

const isDomEntity = entity => {
  return typeof entity   === 'object' && entity.nodeType !== undefined
}

const mergeAttrs = function(target, source){
  source.getAttributeNames().forEach(name => {
    let value = source.getAttribute(name)
    target.setAttribute(name, value)
  })
}

// Stub solution.
window.H = (function() {
  // Shims
  if (typeof Array.isArray === 'undefined') {
    Array.isArray = function(obj) {
      return Object.prototype.toString.call(obj) === '[object Array]';
    }
  };

  // Callback handlers.
  console.log("RECEIVING", arguments)
  var cbs = {}
  cbs.i = function(id) { return function() {
    const el = isDomEntity(id) ? $(id) : $("#" + id) 
    return parseInt(el.val())
  }}
  cbs.f = function(id) { return function() {
    const el = isDomEntity(id) ? $(id) : $("#" + id) 
    return parseFloat(el.val())
  }}
  cbs.s = function(id) { return function() {
    const el = isDomEntity(id) ? $(id) : $("#" + id) 
    return "" + el.val().trim()
  }}
  cbs.c = function(id) { return function() {
    const el = isDomEntity(id) ? $(id) : document.getElementById(id) 
    return el.checked
  }}
  cbs.g = function(id) { return function() {
    const el = isDomEntity(id) ? $(id) : $("#" + id) 
    var v = el.val()
    var v1 = parseInt(v)
    return !isNaN(v1) ? v1 : v
  }}
  cbs.t = function(id) { return function() {
    const el = isDomEntity(id) ? $(id) : $("#" + id) 
    return "" + el.val().trim()
  }}

  function parseArgs(args, data) {
    for (var i=0; i<args.length; i++) {
      var x = args[i]
      if (typeof x === "function") {
        data.push(x())  
      } else if (Array.isArray(x)) {
        if (x.length === 3 && x[0] === "_") {
          if(x[1] === "element_value") {
            let cb_name = x[2].cb_name
            data.push(cbs[cb_name](x[2].id)())
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
  // console..ee
  var cb = function(url, args, kwargs) {
    H.i++
    /* var
     *   url = arguments[0],
     *   args = [],
     *   data = [],
     *   idPrefix = "h" + H.i + "-"

     * for (var i=1; i<arguments.length; i++) {
     *   args.push(arguments[i])
     * }
     * console.log(args, data)
     * parseArgs(args, data) */
    console.log("REQUEST", url, args, kwargs)
    $.ajax({
      url: url,
      type: 'POST',
      data: JSON.stringify({
        args: args,
        kwargs: kwargs,
        id_prefix: "h" + H.i + "-",
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
  cb.i = 0

  return {
    cb: cb,
    cbs: cbs,
    i: 0,
    // eventHandlerCache
    e: {},
  }
})()


