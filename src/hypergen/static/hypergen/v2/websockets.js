import Sockette from 'sockette'
import * as websockets from './websockets'

window.hypergen_websockets = websockets

const WEBSOCKETS = {}

const log = function(e, action, id, url, options) {
  console.log('Websocket ' + action + ' with id:', id, "to url", url, "with options", options, "and event", e)
}

export const open = function(id, url, options) {
  if (!options) options = {}
  
  WEBSOCKETS[id] = new Sockette(url, Object.assign({
    timeout: 5e3,
    maxAttempts: Number.MAX_SAFE_INTEGER,
    onopen: e => log(e, "OPENED", id, url, options),
    onmessage: e => {
      hypergen.applyCommands(JSON.parse(e.data))
    },
    onreconnect: e => log(e, "RECONNECTING", id, url, options),
    onmaximum: e => log(e, "MAX_RECONNECTS_BYE", id, url, options),
    onclose: e => {
      log(e, "CLOSED", id, url, options)
      delete WEBSOCKETS[id]
    },
    onerror: e => console.log('Error:', e),
  }, options))
}

export const close = function(id, url) {
  WEBSOCKETS[id].close()
}

hypergen.append = function(id, html) {
 const el = document.getElementById(id)
 el.innerHTML = el.innerHTML + html
}

window.myapp = {}
window.myapp.sendChatMessage = function(e, id) {
  if (e.keyCode !== 13)  return
  if (!WEBSOCKETS.chat) {
    console.log("Websocket is DEAD. SRY!")
    return
  }

  WEBSOCKETS.chat.send(JSON.stringify({
      'message': e.target.value
  }));
  e.target.value = '';
}
