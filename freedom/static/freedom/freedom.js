import $ from "jquery";
window.jQuery = $

import morphdom from 'morphdom'

import './freedom'

export const morph = function(id, html) {
  morphdom(
    document.getElementById(id),
    "<div>" + html + "</div>",
    {childrenOnly: true}
  )
}                     

export const setEventHandlerCache = function(id, newCache) {
  H.e[id] = newCache
  console.log("Setting new state at", id, H.e)
}

const applyCommands = function(commands) {
  for (let [module, funcs, args, ...rst] of commands) {
    let func
    try {
      func = require(module)
    } catch(e) {
      if (window[module] !== undefined) {
        func = window[module]
      } else {
        throw "Unknown module or window propery:" + module
      }
    }
    if (!!funcs) {
      for (let name of funcs) {
        func = func[name]
      }
    }
    func(...args)
  }
}
window.applyCommands = applyCommands

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
    return parseInt($("#" + id).val())
  }}
  cbs.f = function(id) { return function() {
    return parseFloat($("#" + id).val())
  }}
  cbs.s = function(id) { return function() {
    return "" + $("#" + id).val().trim()
  }}
  cbs.c = function(id) { return function() {
    return document.getElementById(id).checked
  }}
  cbs.g = function(id) { return function() {
    var v = $("#" + id).val()
    var v1 = parseInt(v)
    return !isNaN(v1) ? v1 : v
  }}
  cbs.t = function(id) { return function() {
    return "" + $("#" + id).val().trim()
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
  
  var cb = function() {
    H.i++
    var
      url = arguments[0],
      args = [],
      data = [],
      idPrefix = "h" + H.i + "-"

    for (var i=1; i<arguments.length; i++) {
      args.push(arguments[i])
    }
    
    parseArgs(args, data)
    console.log("REQUEST", data)
    $.ajax({
      url: url,
      type: 'POST',
      data: JSON.stringify({
        args: data,
        id_prefix: idPrefix,
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


