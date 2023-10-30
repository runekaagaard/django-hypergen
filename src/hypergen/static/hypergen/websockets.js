import Sockette from 'sockette'

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
  if (!WEBSOCKETS[url]) {
    log(null, "ALREADY_CLOSED_BYE", url, null)
    return
  }
  WEBSOCKETS[url].close()
  delete WEBSOCKETS[url]
  log(null, "CLOSED_AND_DELETED", url, null)
}
