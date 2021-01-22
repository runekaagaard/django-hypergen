import $ from "jquery";
import morphdom from 'morphdom'
import './freedom'

export const morph = function(id, html) {
  morphdom(
    document.getElementById(id),
    "<div>" + html + "</div>",
    {childrenOnly: true}
  )
}

export const notify = function(message, {type="error", sticky=false}={}) {
  console.log("notifying", message, type, sticky)
}

const load = function(actions) {
  for (let [module, funcs, kwargs, ...args] of actions) {
    let func = require(module)
    if (!!funcs) {
      for (let name of funcs) {
        func = func[name]
      }
    }
    func(...args, kwargs)
  }
}

// Debugging.
$(() => {
  load([
    ["./freedom", ["morph"], {}, "content", "<div>HEJ</div>"],
    ["./freedom", ["notify"], {type: "warning"}, "Oh nooooh"]
  ])
})

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
    return "" + $("#" + id).val()
  }}
  cbs.c = function(id) { return function() {
    return document.getElementById(id).checked
  }}
  cbs.g = function(id) { return function() {
    var v = $("#" + id).val()
    var v1 = parseInt(v)
    return !isNaN(v1) ? v1 : v
  }}

  function parseArgs(args, data) {
    for (var i=0; i<args.length; i++) {
      var x = args[i]
      if (typeof x === "function") {
        data.push(x())  
      } else if (Array.isArray(x)) {
        var tmp = []
        parseArgs(x, tmp)
        data.push(tmp)
      } else {
        data.push(x)
      }
    }
  }
  
  var cb = function() {
    H.i++
    var
      UPDATE = 1,
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
        console.log("")
        if (data === null) return
        for (var i=0; i<data.length; i++) {
          var
            item = data[i],
            cmd = item[0],
            target_id = item[1],
            html = item[2]
          if (cmd === UPDATE) {
            morphdom(
              document.getElementById(target_id),
              "<div>" + html + "</div>",
              {childrenOnly: true}
            )
          } else {
            throw("Unknown command: " + cmd)
          }
        }
      }
    })
  }
  cb.i = 0

  return {
    cb: cb,
    cbs: cbs,
    i: 0,
  }
})()


