import Sockette from 'sockette'
import * as websockets from './websockets'

window.hypergen_websockets = websockets

export const WEBSOCKETS = {}

const log = function(e, action, url, options) {
  console.log('Websocket ' + action + " to url", url, "with options", options, "and event", e)
}

export const open = function(url, options) {
  if (!options) options = {}
  if (!!WEBSOCKETS[url]) {
    log(null, "ALREADY_OPENED_BYE", url, options)
    return
  }
  
  WEBSOCKETS[url] = new Sockette(url, Object.assign({
    timeout: 1e3,
    maxAttempts: Number.MAX_SAFE_INTEGER,
    onopen: e => log(e, "OPENED", url, options),
    onmessage: e => {
      hypergen.applyCommands(JSON.parse(e.data))
    },
    onreconnect: e => log(e, "RECONNECTING", url, options),
    onmaximum: e => log(e, "MAX_RECONNECTS_BYE", url, options),
    onclose: e => {
      log(e, "CLOSED", url, options)
    },
    onerror: e => console.log('Error:', e),
  }, options))
}

export const close = function(url) {
  WEBSOCKETS[url].close()
  delete WEBSOCKETS[url]
}

window.myapp = {}
window.myapp.sendChatMessage = function(e, url) {
  if (e.keyCode !== 13)  return
  if (!WEBSOCKETS[url]) {
    console.log("Websocket is DEAD. SRY!")
    return
  }

  WEBSOCKETS[url].send(JSON.stringify({
      'message': e.target.value
  }));
  e.target.value = '';
}
