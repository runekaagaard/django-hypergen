// modules are defined as an array
// [ module function, map of requires ]
//
// map of requires is short require name -> numeric require
//
// anything defined in a previous bundle is accessed via the
// orig method which is the require for previous bundles

(function (modules, entry, mainEntry, parcelRequireName, globalName) {
  /* eslint-disable no-undef */
  var globalObject =
    typeof globalThis !== 'undefined'
      ? globalThis
      : typeof self !== 'undefined'
      ? self
      : typeof window !== 'undefined'
      ? window
      : typeof global !== 'undefined'
      ? global
      : {};
  /* eslint-enable no-undef */

  // Save the require from previous bundle to this closure if any
  var previousRequire =
    typeof globalObject[parcelRequireName] === 'function' &&
    globalObject[parcelRequireName];

  var cache = previousRequire.cache || {};
  // Do not use `require` to prevent Webpack from trying to bundle this call
  var nodeRequire =
    typeof module !== 'undefined' &&
    typeof module.require === 'function' &&
    module.require.bind(module);

  function newRequire(name, jumped) {
    if (!cache[name]) {
      if (!modules[name]) {
        // if we cannot find the module within our internal map or
        // cache jump to the current global require ie. the last bundle
        // that was added to the page.
        var currentRequire =
          typeof globalObject[parcelRequireName] === 'function' &&
          globalObject[parcelRequireName];
        if (!jumped && currentRequire) {
          return currentRequire(name, true);
        }

        // If there are other bundles on this page the require from the
        // previous one is saved to 'previousRequire'. Repeat this as
        // many times as there are bundles until the module is found or
        // we exhaust the require chain.
        if (previousRequire) {
          return previousRequire(name, true);
        }

        // Try the node require function if it exists.
        if (nodeRequire && typeof name === 'string') {
          return nodeRequire(name);
        }

        var err = new Error("Cannot find module '" + name + "'");
        err.code = 'MODULE_NOT_FOUND';
        throw err;
      }

      localRequire.resolve = resolve;
      localRequire.cache = {};

      var module = (cache[name] = new newRequire.Module(name));

      modules[name][0].call(
        module.exports,
        localRequire,
        module,
        module.exports,
        this
      );
    }

    return cache[name].exports;

    function localRequire(x) {
      var res = localRequire.resolve(x);
      return res === false ? {} : newRequire(res);
    }

    function resolve(x) {
      var id = modules[name][1][x];
      return id != null ? id : x;
    }
  }

  function Module(moduleName) {
    this.id = moduleName;
    this.bundle = newRequire;
    this.exports = {};
  }

  newRequire.isParcelRequire = true;
  newRequire.Module = Module;
  newRequire.modules = modules;
  newRequire.cache = cache;
  newRequire.parent = previousRequire;
  newRequire.register = function (id, exports) {
    modules[id] = [
      function (require, module) {
        module.exports = exports;
      },
      {},
    ];
  };

  Object.defineProperty(newRequire, 'root', {
    get: function () {
      return globalObject[parcelRequireName];
    },
  });

  globalObject[parcelRequireName] = newRequire;

  for (var i = 0; i < entry.length; i++) {
    newRequire(entry[i]);
  }

  if (mainEntry) {
    // Expose entry point to Node, AMD or browser globals
    // Based on https://github.com/ForbesLindesay/umd/blob/master/template.js
    var mainExports = newRequire(mainEntry);

    // CommonJS
    if (typeof exports === 'object' && typeof module !== 'undefined') {
      module.exports = mainExports;

      // RequireJS
    } else if (typeof define === 'function' && define.amd) {
      define(function () {
        return mainExports;
      });

      // <script>
    } else if (globalName) {
      this[globalName] = mainExports;
    }
  }
})({"jgsYR":[function(require,module,exports) {
var global = arguments[3];
var HMR_HOST = null;
var HMR_PORT = null;
var HMR_SECURE = false;
var HMR_ENV_HASH = "d6ea1d42532a7575";
module.bundle.HMR_BUNDLE_ID = "19cb7e455cde6bca";
"use strict";
/* global HMR_HOST, HMR_PORT, HMR_ENV_HASH, HMR_SECURE, chrome, browser, __parcel__import__, __parcel__importScripts__, ServiceWorkerGlobalScope */ /*::
import type {
  HMRAsset,
  HMRMessage,
} from '@parcel/reporter-dev-server/src/HMRServer.js';
interface ParcelRequire {
  (string): mixed;
  cache: {|[string]: ParcelModule|};
  hotData: {|[string]: mixed|};
  Module: any;
  parent: ?ParcelRequire;
  isParcelRequire: true;
  modules: {|[string]: [Function, {|[string]: string|}]|};
  HMR_BUNDLE_ID: string;
  root: ParcelRequire;
}
interface ParcelModule {
  hot: {|
    data: mixed,
    accept(cb: (Function) => void): void,
    dispose(cb: (mixed) => void): void,
    // accept(deps: Array<string> | string, cb: (Function) => void): void,
    // decline(): void,
    _acceptCallbacks: Array<(Function) => void>,
    _disposeCallbacks: Array<(mixed) => void>,
  |};
}
interface ExtensionContext {
  runtime: {|
    reload(): void,
    getURL(url: string): string;
    getManifest(): {manifest_version: number, ...};
  |};
}
declare var module: {bundle: ParcelRequire, ...};
declare var HMR_HOST: string;
declare var HMR_PORT: string;
declare var HMR_ENV_HASH: string;
declare var HMR_SECURE: boolean;
declare var chrome: ExtensionContext;
declare var browser: ExtensionContext;
declare var __parcel__import__: (string) => Promise<void>;
declare var __parcel__importScripts__: (string) => Promise<void>;
declare var globalThis: typeof self;
declare var ServiceWorkerGlobalScope: Object;
*/ var OVERLAY_ID = "__parcel__error__overlay__";
var OldModule = module.bundle.Module;
function Module(moduleName) {
    OldModule.call(this, moduleName);
    this.hot = {
        data: module.bundle.hotData[moduleName],
        _acceptCallbacks: [],
        _disposeCallbacks: [],
        accept: function(fn) {
            this._acceptCallbacks.push(fn || function() {});
        },
        dispose: function(fn) {
            this._disposeCallbacks.push(fn);
        }
    };
    module.bundle.hotData[moduleName] = undefined;
}
module.bundle.Module = Module;
module.bundle.hotData = {};
var checkedAssets /*: {|[string]: boolean|} */ , assetsToDispose /*: Array<[ParcelRequire, string]> */ , assetsToAccept /*: Array<[ParcelRequire, string]> */ ;
function getHostname() {
    return HMR_HOST || (location.protocol.indexOf("http") === 0 ? location.hostname : "localhost");
}
function getPort() {
    return HMR_PORT || location.port;
}
// eslint-disable-next-line no-redeclare
var parent = module.bundle.parent;
if ((!parent || !parent.isParcelRequire) && typeof WebSocket !== "undefined") {
    var hostname = getHostname();
    var port = getPort();
    var protocol = HMR_SECURE || location.protocol == "https:" && !/localhost|127.0.0.1|0.0.0.0/.test(hostname) ? "wss" : "ws";
    var ws = new WebSocket(protocol + "://" + hostname + (port ? ":" + port : "") + "/");
    // Web extension context
    var extCtx = typeof chrome === "undefined" ? typeof browser === "undefined" ? null : browser : chrome;
    // Safari doesn't support sourceURL in error stacks.
    // eval may also be disabled via CSP, so do a quick check.
    var supportsSourceURL = false;
    try {
        (0, eval)('throw new Error("test"); //# sourceURL=test.js');
    } catch (err) {
        supportsSourceURL = err.stack.includes("test.js");
    }
    // $FlowFixMe
    ws.onmessage = async function(event /*: {data: string, ...} */ ) {
        checkedAssets = {} /*: {|[string]: boolean|} */ ;
        assetsToAccept = [];
        assetsToDispose = [];
        var data /*: HMRMessage */  = JSON.parse(event.data);
        if (data.type === "update") {
            // Remove error overlay if there is one
            if (typeof document !== "undefined") removeErrorOverlay();
            let assets = data.assets.filter((asset)=>asset.envHash === HMR_ENV_HASH);
            // Handle HMR Update
            let handled = assets.every((asset)=>{
                return asset.type === "css" || asset.type === "js" && hmrAcceptCheck(module.bundle.root, asset.id, asset.depsByBundle);
            });
            if (handled) {
                console.clear();
                // Dispatch custom event so other runtimes (e.g React Refresh) are aware.
                if (typeof window !== "undefined" && typeof CustomEvent !== "undefined") window.dispatchEvent(new CustomEvent("parcelhmraccept"));
                await hmrApplyUpdates(assets);
                // Dispose all old assets.
                let processedAssets = {} /*: {|[string]: boolean|} */ ;
                for(let i = 0; i < assetsToDispose.length; i++){
                    let id = assetsToDispose[i][1];
                    if (!processedAssets[id]) {
                        hmrDispose(assetsToDispose[i][0], id);
                        processedAssets[id] = true;
                    }
                }
                // Run accept callbacks. This will also re-execute other disposed assets in topological order.
                processedAssets = {};
                for(let i = 0; i < assetsToAccept.length; i++){
                    let id = assetsToAccept[i][1];
                    if (!processedAssets[id]) {
                        hmrAccept(assetsToAccept[i][0], id);
                        processedAssets[id] = true;
                    }
                }
            } else fullReload();
        }
        if (data.type === "error") {
            // Log parcel errors to console
            for (let ansiDiagnostic of data.diagnostics.ansi){
                let stack = ansiDiagnostic.codeframe ? ansiDiagnostic.codeframe : ansiDiagnostic.stack;
                console.error("\uD83D\uDEA8 [parcel]: " + ansiDiagnostic.message + "\n" + stack + "\n\n" + ansiDiagnostic.hints.join("\n"));
            }
            if (typeof document !== "undefined") {
                // Render the fancy html overlay
                removeErrorOverlay();
                var overlay = createErrorOverlay(data.diagnostics.html);
                // $FlowFixMe
                document.body.appendChild(overlay);
            }
        }
    };
    ws.onerror = function(e) {
        console.error(e.message);
    };
    ws.onclose = function() {
        console.warn("[parcel] \uD83D\uDEA8 Connection to the HMR server was lost");
    };
}
function removeErrorOverlay() {
    var overlay = document.getElementById(OVERLAY_ID);
    if (overlay) {
        overlay.remove();
        console.log("[parcel] ✨ Error resolved");
    }
}
function createErrorOverlay(diagnostics) {
    var overlay = document.createElement("div");
    overlay.id = OVERLAY_ID;
    let errorHTML = '<div style="background: black; opacity: 0.85; font-size: 16px; color: white; position: fixed; height: 100%; width: 100%; top: 0px; left: 0px; padding: 30px; font-family: Menlo, Consolas, monospace; z-index: 9999;">';
    for (let diagnostic of diagnostics){
        let stack = diagnostic.frames.length ? diagnostic.frames.reduce((p, frame)=>{
            return `${p}
<a href="/__parcel_launch_editor?file=${encodeURIComponent(frame.location)}" style="text-decoration: underline; color: #888" onclick="fetch(this.href); return false">${frame.location}</a>
${frame.code}`;
        }, "") : diagnostic.stack;
        errorHTML += `
      <div>
        <div style="font-size: 18px; font-weight: bold; margin-top: 20px;">
          🚨 ${diagnostic.message}
        </div>
        <pre>${stack}</pre>
        <div>
          ${diagnostic.hints.map((hint)=>"<div>\uD83D\uDCA1 " + hint + "</div>").join("")}
        </div>
        ${diagnostic.documentation ? `<div>📝 <a style="color: violet" href="${diagnostic.documentation}" target="_blank">Learn more</a></div>` : ""}
      </div>
    `;
    }
    errorHTML += "</div>";
    overlay.innerHTML = errorHTML;
    return overlay;
}
function fullReload() {
    if ("reload" in location) location.reload();
    else if (extCtx && extCtx.runtime && extCtx.runtime.reload) extCtx.runtime.reload();
}
function getParents(bundle, id) /*: Array<[ParcelRequire, string]> */ {
    var modules = bundle.modules;
    if (!modules) return [];
    var parents = [];
    var k, d, dep;
    for(k in modules)for(d in modules[k][1]){
        dep = modules[k][1][d];
        if (dep === id || Array.isArray(dep) && dep[dep.length - 1] === id) parents.push([
            bundle,
            k
        ]);
    }
    if (bundle.parent) parents = parents.concat(getParents(bundle.parent, id));
    return parents;
}
function updateLink(link) {
    var href = link.getAttribute("href");
    if (!href) return;
    var newLink = link.cloneNode();
    newLink.onload = function() {
        if (link.parentNode !== null) // $FlowFixMe
        link.parentNode.removeChild(link);
    };
    newLink.setAttribute("href", // $FlowFixMe
    href.split("?")[0] + "?" + Date.now());
    // $FlowFixMe
    link.parentNode.insertBefore(newLink, link.nextSibling);
}
var cssTimeout = null;
function reloadCSS() {
    if (cssTimeout) return;
    cssTimeout = setTimeout(function() {
        var links = document.querySelectorAll('link[rel="stylesheet"]');
        for(var i = 0; i < links.length; i++){
            // $FlowFixMe[incompatible-type]
            var href /*: string */  = links[i].getAttribute("href");
            var hostname = getHostname();
            var servedFromHMRServer = hostname === "localhost" ? new RegExp("^(https?:\\/\\/(0.0.0.0|127.0.0.1)|localhost):" + getPort()).test(href) : href.indexOf(hostname + ":" + getPort());
            var absolute = /^https?:\/\//i.test(href) && href.indexOf(location.origin) !== 0 && !servedFromHMRServer;
            if (!absolute) updateLink(links[i]);
        }
        cssTimeout = null;
    }, 50);
}
function hmrDownload(asset) {
    if (asset.type === "js") {
        if (typeof document !== "undefined") {
            let script = document.createElement("script");
            script.src = asset.url + "?t=" + Date.now();
            if (asset.outputFormat === "esmodule") script.type = "module";
            return new Promise((resolve, reject)=>{
                var _document$head;
                script.onload = ()=>resolve(script);
                script.onerror = reject;
                (_document$head = document.head) === null || _document$head === void 0 || _document$head.appendChild(script);
            });
        } else if (typeof importScripts === "function") {
            // Worker scripts
            if (asset.outputFormat === "esmodule") return import(asset.url + "?t=" + Date.now());
            else return new Promise((resolve, reject)=>{
                try {
                    importScripts(asset.url + "?t=" + Date.now());
                    resolve();
                } catch (err) {
                    reject(err);
                }
            });
        }
    }
}
async function hmrApplyUpdates(assets) {
    global.parcelHotUpdate = Object.create(null);
    let scriptsToRemove;
    try {
        // If sourceURL comments aren't supported in eval, we need to load
        // the update from the dev server over HTTP so that stack traces
        // are correct in errors/logs. This is much slower than eval, so
        // we only do it if needed (currently just Safari).
        // https://bugs.webkit.org/show_bug.cgi?id=137297
        // This path is also taken if a CSP disallows eval.
        if (!supportsSourceURL) {
            let promises = assets.map((asset)=>{
                var _hmrDownload;
                return (_hmrDownload = hmrDownload(asset)) === null || _hmrDownload === void 0 ? void 0 : _hmrDownload.catch((err)=>{
                    // Web extension bugfix for Chromium
                    // https://bugs.chromium.org/p/chromium/issues/detail?id=1255412#c12
                    if (extCtx && extCtx.runtime && extCtx.runtime.getManifest().manifest_version == 3) {
                        if (typeof ServiceWorkerGlobalScope != "undefined" && global instanceof ServiceWorkerGlobalScope) {
                            extCtx.runtime.reload();
                            return;
                        }
                        asset.url = extCtx.runtime.getURL("/__parcel_hmr_proxy__?url=" + encodeURIComponent(asset.url + "?t=" + Date.now()));
                        return hmrDownload(asset);
                    }
                    throw err;
                });
            });
            scriptsToRemove = await Promise.all(promises);
        }
        assets.forEach(function(asset) {
            hmrApply(module.bundle.root, asset);
        });
    } finally{
        delete global.parcelHotUpdate;
        if (scriptsToRemove) scriptsToRemove.forEach((script)=>{
            if (script) {
                var _document$head2;
                (_document$head2 = document.head) === null || _document$head2 === void 0 || _document$head2.removeChild(script);
            }
        });
    }
}
function hmrApply(bundle /*: ParcelRequire */ , asset /*:  HMRAsset */ ) {
    var modules = bundle.modules;
    if (!modules) return;
    if (asset.type === "css") reloadCSS();
    else if (asset.type === "js") {
        let deps = asset.depsByBundle[bundle.HMR_BUNDLE_ID];
        if (deps) {
            if (modules[asset.id]) {
                // Remove dependencies that are removed and will become orphaned.
                // This is necessary so that if the asset is added back again, the cache is gone, and we prevent a full page reload.
                let oldDeps = modules[asset.id][1];
                for(let dep in oldDeps)if (!deps[dep] || deps[dep] !== oldDeps[dep]) {
                    let id = oldDeps[dep];
                    let parents = getParents(module.bundle.root, id);
                    if (parents.length === 1) hmrDelete(module.bundle.root, id);
                }
            }
            if (supportsSourceURL) // Global eval. We would use `new Function` here but browser
            // support for source maps is better with eval.
            (0, eval)(asset.output);
            // $FlowFixMe
            let fn = global.parcelHotUpdate[asset.id];
            modules[asset.id] = [
                fn,
                deps
            ];
        } else if (bundle.parent) hmrApply(bundle.parent, asset);
    }
}
function hmrDelete(bundle, id) {
    let modules = bundle.modules;
    if (!modules) return;
    if (modules[id]) {
        // Collect dependencies that will become orphaned when this module is deleted.
        let deps = modules[id][1];
        let orphans = [];
        for(let dep in deps){
            let parents = getParents(module.bundle.root, deps[dep]);
            if (parents.length === 1) orphans.push(deps[dep]);
        }
        // Delete the module. This must be done before deleting dependencies in case of circular dependencies.
        delete modules[id];
        delete bundle.cache[id];
        // Now delete the orphans.
        orphans.forEach((id)=>{
            hmrDelete(module.bundle.root, id);
        });
    } else if (bundle.parent) hmrDelete(bundle.parent, id);
}
function hmrAcceptCheck(bundle /*: ParcelRequire */ , id /*: string */ , depsByBundle /*: ?{ [string]: { [string]: string } }*/ ) {
    if (hmrAcceptCheckOne(bundle, id, depsByBundle)) return true;
    // Traverse parents breadth first. All possible ancestries must accept the HMR update, or we'll reload.
    let parents = getParents(module.bundle.root, id);
    let accepted = false;
    while(parents.length > 0){
        let v = parents.shift();
        let a = hmrAcceptCheckOne(v[0], v[1], null);
        if (a) // If this parent accepts, stop traversing upward, but still consider siblings.
        accepted = true;
        else {
            // Otherwise, queue the parents in the next level upward.
            let p = getParents(module.bundle.root, v[1]);
            if (p.length === 0) {
                // If there are no parents, then we've reached an entry without accepting. Reload.
                accepted = false;
                break;
            }
            parents.push(...p);
        }
    }
    return accepted;
}
function hmrAcceptCheckOne(bundle /*: ParcelRequire */ , id /*: string */ , depsByBundle /*: ?{ [string]: { [string]: string } }*/ ) {
    var modules = bundle.modules;
    if (!modules) return;
    if (depsByBundle && !depsByBundle[bundle.HMR_BUNDLE_ID]) {
        // If we reached the root bundle without finding where the asset should go,
        // there's nothing to do. Mark as "accepted" so we don't reload the page.
        if (!bundle.parent) return true;
        return hmrAcceptCheck(bundle.parent, id, depsByBundle);
    }
    if (checkedAssets[id]) return true;
    checkedAssets[id] = true;
    var cached = bundle.cache[id];
    assetsToDispose.push([
        bundle,
        id
    ]);
    if (!cached || cached.hot && cached.hot._acceptCallbacks.length) {
        assetsToAccept.push([
            bundle,
            id
        ]);
        return true;
    }
}
function hmrDispose(bundle /*: ParcelRequire */ , id /*: string */ ) {
    var cached = bundle.cache[id];
    bundle.hotData[id] = {};
    if (cached && cached.hot) cached.hot.data = bundle.hotData[id];
    if (cached && cached.hot && cached.hot._disposeCallbacks.length) cached.hot._disposeCallbacks.forEach(function(cb) {
        cb(bundle.hotData[id]);
    });
    delete bundle.cache[id];
}
function hmrAccept(bundle /*: ParcelRequire */ , id /*: string */ ) {
    // Execute the module.
    bundle(id);
    // Run the accept callbacks in the new version of the module.
    var cached = bundle.cache[id];
    if (cached && cached.hot && cached.hot._acceptCallbacks.length) cached.hot._acceptCallbacks.forEach(function(cb) {
        var assetsToAlsoAccept = cb(function() {
            return getParents(module.bundle.root, id);
        });
        if (assetsToAlsoAccept && assetsToAccept.length) {
            assetsToAlsoAccept.forEach(function(a) {
                hmrDispose(a[0], a[1]);
            });
            // $FlowFixMe[method-unbinding]
            assetsToAccept.push.apply(assetsToAccept, assetsToAlsoAccept);
        }
    });
}

},{}],"5r9D8":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
parcelHelpers.export(exports, "morph", ()=>morph);
parcelHelpers.export(exports, "remove", ()=>remove);
parcelHelpers.export(exports, "hide", ()=>hide);
parcelHelpers.export(exports, "display", ()=>display);
parcelHelpers.export(exports, "visible", ()=>visible);
parcelHelpers.export(exports, "hidden", ()=>hidden);
parcelHelpers.export(exports, "redirect", ()=>redirect);
parcelHelpers.export(exports, "append", ()=>append);
parcelHelpers.export(exports, "prepend", ()=>prepend);
parcelHelpers.export(exports, "setClientState", ()=>setClientState);
parcelHelpers.export(exports, "intervalSet", ()=>intervalSet);
parcelHelpers.export(exports, "intervalClear", ()=>intervalClear);
parcelHelpers.export(exports, "addEventListener", ()=>addEventListener);
parcelHelpers.export(exports, "keypressToCallback", ()=>keypressToCallback);
parcelHelpers.export(exports, "keypressToCallbackRemove", ()=>keypressToCallbackRemove);
parcelHelpers.export(exports, "callback", ()=>callback);
parcelHelpers.export(exports, "partialLoad", ()=>partialLoad);
parcelHelpers.export(exports, "throttle", ()=>throttle);
parcelHelpers.export(exports, "cancelThrottle", ()=>cancelThrottle);
parcelHelpers.export(exports, "event", ()=>event);
parcelHelpers.export(exports, "applyCommands", ()=>applyCommands);
parcelHelpers.export(exports, "coerce", ()=>coerce);
parcelHelpers.export(exports, "read", ()=>read);
parcelHelpers.export(exports, "when", ()=>when);
parcelHelpers.export(exports, "element", ()=>element);
parcelHelpers.export(exports, "reviver", ()=>reviver);
parcelHelpers.export(exports, "onpushstate", ()=>onpushstate);
parcelHelpers.export(exports, "ready", ()=>ready);
var _morphdom = require("morphdom");
var _morphdomDefault = parcelHelpers.interopDefault(_morphdom);
var _hypergen = require("./hypergen");
var _websocket = require("./websocket");
// Make all exported vars availabe inside window.hypergen.
window.hypergen = _hypergen;
window.hypergen.websocket = _websocket;
// Shims
if (typeof Array.isArray === "undefined") Array.isArray = function(obj) {
    return Object.prototype.toString.call(obj) === "[object Array]";
};
const morph = function(id, html) {
    const element = document.getElementById(id);
    if (!element) {
        console.error("Trying to morph into an element with id='" + id + "' that does not exist. Please check your target_id.");
        return;
    }
    (0, _morphdomDefault.default)(element, "<div>" + html + "</div>", {
        childrenOnly: true,
        onBeforeElUpdated: function(fromEl, toEl) {
            let focused = document.activeElement;
            if ((fromEl.nodeName == "INPUT" || fromEl.nodeName == "TEXTAREA") && fromEl === focused) {
                let types = [
                    "checkbox",
                    "radio"
                ];
                if (fromEl.nodeName === "INPUT" && types.indexOf(fromEl.type) !== -1) return true;
                mergeAttrs(fromEl, toEl);
                return false;
            } else if (fromEl.nodeName == "INPUT" && fromEl.type === "file" && fromEl.files.length > 0) {
                mergeAttrs(fromEl, toEl);
                return false;
            } else if (fromEl.nodeName === "SCRIPT" && toEl.nodeName === "SCRIPT") {
                var script = document.createElement("script");
                //copy over the attributes
                [
                    ...toEl.attributes
                ].forEach((attr)=>{
                    script.setAttribute(attr.nodeName, attr.nodeValue);
                });
                script.innerHTML = toEl.innerHTML;
                fromEl.replaceWith(script);
                return false;
            } else return true;
        },
        onNodeAdded: function(node) {
            if (node.nodeName === "SCRIPT") {
                var script = document.createElement("script");
                //copy over the attributes
                [
                    ...node.attributes
                ].forEach((attr)=>{
                    script.setAttribute(attr.nodeName, attr.nodeValue);
                });
                script.innerHTML = node.innerHTML;
                node.replaceWith(script);
            }
        }
    });
    const autofocus = document.querySelectorAll("[autofocus]")[0];
    if (autofocus !== undefined) autofocus.focus();
};
const remove = function(id) {
    let el = document.getElementById(id);
    el.parentNode.removeChild(el);
};
const hide = function(id) {
    let el = document.getElementById(id);
    el.style.display = "none";
};
const display = function(id, value) {
    let el = document.getElementById(id);
    el.style.display = value || "block";
};
const visible = function(id, value) {
    let el = document.getElementById(id);
    el.style.visibility = "visible";
};
const hidden = function(id, value) {
    let el = document.getElementById(id);
    el.style.visibility = "hidden";
};
const redirect = function(url) {
    /*
  One would expect to simply do a window.location = url but that does not work in an ajax request on safari, because
  (i think) the ajax request is async and the redirect is thus triggered directly during a user event.
  This is a workaround, but might stop working some day.
  */ const link = document.createElement("a");
    link.href = url;
    link.style.display = "none";
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
};
const append = function(id, html) {
    const el = document.getElementById(id);
    if (!el) console.error("Cannot append to missing element", id);
    el.innerHTML += html;
};
const prepend = function(id, html) {
    const el = document.getElementById(id);
    if (!el) console.error("Cannot prepend to missing element", id);
    el.innerHTML = html + el.innerHTML;
};
_hypergen.clientState = {};
const setClientState = function(at, value) {
    let clientState = _hypergen.clientState;
    for (const path of at.split(".")){
        if (clientState[path] === undefined) clientState[path] = {};
        clientState = clientState[path];
    }
    Object.assign(clientState, value);
    console.log("Setting new state for hypergen.clientState", at, "with value", value, "giving", _hypergen.clientState);
};
/* WARNING NOT STABLE */ var INTERVALS = {};
const intervalSet = function(commands, interval, name) {
    const i = setInterval(()=>applyCommands(commands), interval);
    if (!!name) INTERVALS[name] = i;
};
const intervalClear = function(name) {
    if (INTERVALS[name]) {
        console.log("Clearing", INTERVALS[name]);
        clearInterval(INTERVALS[name]);
    }
};
const addEventListener = function(querySelectorString, type, commands, options) {
    document.querySelector(querySelectorString).addEventListener(type, (event)=>applyCommands(commands), options || {});
};
let _TTT = {};
const keypressToCallbackFunc = function(e) {
    const [url, args, options] = _TTT;
    callback(url, [
        e.key,
        ...args || []
    ], options || {});
};
const keypressToCallback = function(url, args, options) {
    _TTT = [
        url,
        args,
        options
    ];
    window.addEventListener("keydown", keypressToCallbackFunc);
};
const keypressToCallbackRemove = function(url, args, options) {
    window.removeEventListener("keydown", keypressToCallbackFunc);
};
/* END WARNING STABLE AGAIN */ // Callback
var i = 0;
var isBlocked = false;
var urlBlocks = {};
const callback = function(url, args, { debounce = 0, confirm_ = false, blocks = false, blocksEachUrl = true, uploadFiles = false, params = {}, meta = {}, clear = false, elementId = null, debug = false, event = null, headers = {}, onSucces = null, timeout = 20000 } = {}) {
    const isWebsocket = url.startsWith("ws://") || url.startsWith("wss://");
    if (!!event) {
        event.preventDefault();
        event.stopPropagation();
    }
    let postIt = function() {
        let json;
        console.log("REQUEST", url, args, debounce);
        i++;
        // The element function must have access to the FormData.
        _hypergen.hypergenGlobalFormdata = new FormData();
        _hypergen.hypergenUploadFiles = uploadFiles;
        try {
            json = JSON.stringify({
                args: args,
                meta: meta
            });
        } catch (error) {
            if (error === MISSING_ELEMENT_EXCEPTION) {
                console.warn("An element is missing. This can happen if a dom element has multiple event handlers.", url);
                return;
            } else throw error;
        }
        let formData = _hypergen.hypergenGlobalFormdata;
        _hypergen.hypergenGlobalFormdata = null;
        _hypergen.hypergenUploadFiles = null;
        formData.append("hypergen_data", json);
        if (blocks === true) {
            if (isBlocked === true) {
                console.error("Callback was blocked");
                return;
            } else isBlocked = true;
        }
        if (blocksEachUrl === true && !isWebsocket) {
            if (!!urlBlocks[url]) {
                console.error("Callback to " + url + " was blocked");
                return;
            }
            urlBlocks[url] = true;
        }
        post(url, formData, (data)=>{
            if (data !== null) applyCommands(data);
            isBlocked = false;
            if (blocksEachUrl === true && !isWebsocket) delete urlBlocks[url];
            if (clear === true) document.getElementById(elementId).value = "";
            if (!!onSucces) onSucces();
        }, (data, jsonOk, xhr)=>{
            console.log("xhr:", xhr);
            isBlocked = false;
            if (blocksEachUrl === true && !isWebsocket) delete urlBlocks[url];
            console.error("Hypergen post error occured", data);
            if (debug !== true) {
                if (xhr.getResponseHeader("Content-Type") === "text/plain") data = "<pre><code>" + data + "</pre></code>";
                document.getElementsByTagName("html")[0].innerHTML = data;
            }
        }, params, headers, {
            timeout
        });
    };
    const postItWebsocket = function() {
        console.log("WEBSOCKET", url, args, debounce);
        let json;
        try {
            json = JSON.stringify({
                args: args,
                meta: meta
            });
        } catch (error) {
            if (error === MISSING_ELEMENT_EXCEPTION) {
                console.warn("An element is missing. This can happen if a dom element has multiple event handlers.", url);
                return;
            } else throw error;
        }
        if (!_hypergen.websocket.WEBSOCKETS[url]) {
            console.error("Cannot send WS to non existing connection:", url);
            return;
        }
        _hypergen.websocket.WEBSOCKETS[url].send(json);
        if (clear === true) document.getElementById(elementId).value = "";
    };
    const func = isWebsocket ? postItWebsocket : postIt;
    if (debounce === 0) {
        if (confirm_ === false) func();
        else if (confirm(confirm_)) func();
    } else throttle(func, {
        delay: debounce,
        group: url,
        confirm_
    });
};
const partialLoad = function(event, url, pushState) {
    console.log("partialLoad to", url, pushState);
    window.dispatchEvent(new CustomEvent("hypergen.partialLoad.before", {
        detail: {
            event,
            url,
            pushState
        }
    }));
    callback(url, [], {
        "event": event,
        "headers": {
            "X-Hypergen-Partial": "1"
        },
        onSucces: function() {
            if (!!pushState) {
                console.log("pushing state!");
                history.pushState({
                    callback_url: url
                }, "", url);
                onpushstate();
                history.forward();
                window.dispatchEvent(new CustomEvent("hypergen.partialLoad.after", {
                    detail: {
                        event,
                        url,
                        pushState
                    }
                }));
            }
        }
    });
};
// Timing
var _THROTTLE_GROUPS = {};
let throttle = function(func, { delay = 0, group = "global", confirm_ = false } = {}) {
    if (_THROTTLE_GROUPS[group]) {
        clearTimeout(_THROTTLE_GROUPS[group]);
        _THROTTLE_GROUPS[group] = null;
    }
    _THROTTLE_GROUPS[group] = setTimeout(function() {
        if (confirm_ === false) func();
        else {
            const confirmed = confirm(confirm_);
            if (confirmed === true) func();
        }
        _THROTTLE_GROUPS[group] = null;
    }, delay);
};
let cancelThrottle = function(group) {
    if (_THROTTLE_GROUPS[group]) {
        clearTimeout(_THROTTLE_GROUPS[group]);
        _THROTTLE_GROUPS[group] = null;
    }
};
// Internal
const require_ = function(module) {
    try {
        return require(module);
    } catch (e) {
        return false;
    }
};
const resolvePath = function(path) {
    const parts = path.split(".");
    let i = -1, obj = null;
    for (let part of parts){
        i++;
        if (i === 0) {
            if (window[part] !== undefined) obj = window[part];
            else if (obj = require_(part)) ;
            else if (obj = require_("./" + part)) ;
            else throw "Could not resolve path: " + path;
        } else {
            if (obj[part] !== undefined) try {
                obj = obj[part].bind(obj);
            } catch (e) {
                obj = obj[part];
            }
            else throw "Could not resolve path: " + path;
        }
    }
    return obj;
};
const applyCommand = function(path, ...args) {
    console.log("apply command", path, args);
    let rpath = resolvePath(path);
    const result = rpath(...args);
    const event = new CustomEvent("hypergen.applyCommand.after", {
        detail: {
            path,
            args
        }
    });
    document.dispatchEvent(event);
    return result;
};
const event = function(event, callbackKey, when) {
    event.preventDefault();
    event.stopPropagation();
    if (!!when && !applyCommand(...when, event)) return;
    applyCommand(..._hypergen.clientState.hypergen.eventHandlerCallbacks[callbackKey]);
};
const applyCommands = function(commands) {
    if (!!commands._ && commands._.length === 2 && commands._[0] === "deque") commands = commands._[1];
    for (let [path, ...args] of commands)applyCommand(path, ...args);
};
const mergeAttrs = function(target, source) {
    source.getAttributeNames().forEach((name)=>{
        let value = source.getAttribute(name);
        target.setAttribute(name, value);
    });
};
const MISSING_ELEMENT_EXCEPTION = "MISSING_ELEMENT_EXCEPTION";
const coerce = {};
coerce.no = function(value) {
    if (value === "") return null;
    return value;
};
coerce.str = function(value) {
    if (value === "") return null;
    return value === null ? null : "" + value;
};
coerce.int = function(value) {
    if (value === "") return null;
    value = parseInt(value);
    if (isNaN(value)) return null;
    else return value;
};
coerce.intlist = function(value) {
    return value.map((x)=>parseInt(x));
};
coerce.float = function(value) {
    if (value === "") return null;
    value = parseFloat(value);
    if (isNaN(value)) return null;
    else return {
        _: [
            "float",
            value
        ]
    };
};
coerce.date = function(value) {
    if (value === "") return null;
    else return {
        _: [
            "date",
            value
        ]
    };
};
coerce.datetime = function(value) {
    if (value === "") return null;
    else return {
        _: [
            "datetime",
            value
        ]
    };
};
coerce.time = function(value) {
    if (value === "") return null;
    else return {
        _: [
            "time",
            value
        ]
    };
};
coerce.month = function(value) {
    if (value === "") return null;
    const parts = value.split("-");
    return {
        year: parseInt(parts[0]),
        month: parseInt(parts[1])
    };
};
coerce.week = function(value) {
    if (value === "") return null;
    const parts = value.split("-");
    return {
        year: parseInt(parts[0]),
        week: parseInt(parts[1].replace("W", ""))
    };
};
const read = {};
read.value = function(id) {
    const el = document.getElementById(id);
    if (el === null) throw MISSING_ELEMENT_EXCEPTION;
    return el.value.trim();
};
read.checked = function(id) {
    const el = document.getElementById(id);
    if (el === null) throw MISSING_ELEMENT_EXCEPTION;
    return el.checked;
};
read.radio = function(id) {
    const el = document.getElementById(id);
    if (el === null) throw MISSING_ELEMENT_EXCEPTION;
    const checked = document.querySelector("input[type=radio][name=" + el.name + "]:checked");
    return checked === null ? null : checked.value;
};
read.contenteditable = function(id) {
    const el = document.getElementById(id);
    if (el === null) throw MISSING_ELEMENT_EXCEPTION;
    return el.innerHTML;
};
read.selectMultiple = function(id) {
    const el = document.getElementById(id);
    if (el === null) throw MISSING_ELEMENT_EXCEPTION;
    return Array.from(el.selectedOptions).map((option)=>option.value);
};
read.file = function(id, formData) {
    const el = document.getElementById(id);
    if (el === null) throw MISSING_ELEMENT_EXCEPTION;
    if (el.files.length !== 1) return null;
    if (_hypergen.hypergenUploadFiles === true) formData.append(id, el.files[0]);
    return el.files[0].name;
};
const when = {};
when.keycode = function(keycode, event) {
    return event.code == keycode;
};
const element = function(valueFunc, coerceFunc, id) {
    this.toJSON = function() {
        const value = resolvePath(valueFunc)(id, _hypergen.hypergenGlobalFormdata);
        if (!!coerceFunc) return resolvePath(coerceFunc)(value);
        else return coerce.no(value);
    };
    return this;
};
const reviver = function(k, v) {
    if (Array.isArray(v)) {
        if (v.length === 3 && v[0] === "_") {
            if (v[1] === "element_value") return new element(...v[2]);
        }
    }
    return v;
};
const getCookie = function(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for(let i = 0; i < cookies.length; i++){
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === name + "=") {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
};
function addParams(url, params) {
    const ret = [];
    for(let d in params)ret.push(encodeURIComponent(d) + "=" + encodeURIComponent(params[d]));
    if (ret.length === 0) return url;
    else return url + "?" + ret.join("&");
}
const post = function(url, formData, onSuccess, onError, params, headers, { timeout = 20000 } = {}) {
    url = addParams(url, params);
    const xhr = new XMLHttpRequest();
    xhr.timeout = timeout;
    const progressBar = document.getElementById("hypergen-upload-progress-bar");
    if (progressBar !== null) {
        xhr.upload.onload = ()=>{
            progressBar.style.visibility = "hidden";
            console.log(`The upload is completed: ${xhr.status} ${xhr.response}`);
        };
        xhr.upload.onerror = ()=>{
            progressBar.style.visibility = "hidden";
            console.error("Upload failed.");
        };
        xhr.upload.onabort = ()=>{
            progressBar.style.visibility = "hidden";
            console.error("Upload cancelled.");
        };
        xhr.upload.onprogress = (event)=>{
            progressBar.style.visibility = "visible";
            progressBar.value = event.loaded / event.total;
            console.log(`Uploaded ${event.loaded} of ${event.total} bytes`);
        };
    }
    xhr.onload = ()=>{
        var jsonOk = false, data = null;
        try {
            data = JSON.parse(xhr.responseText, reviver);
            jsonOk = true;
        } catch (e) {
            data = xhr.responseText;
            jsonOk = false;
        }
        if (xhr.readyState == 4 && (xhr.status == 200 || xhr.status == 302)) {
            window.dispatchEvent(new CustomEvent("hypergen.post.after"));
            onSuccess(data, xhr);
        } else {
            window.dispatchEvent(new CustomEvent("hypergen.post.after"));
            onError(data, jsonOk, xhr);
        }
    };
    xhr.onerror = ()=>{
        console.error("xhr onerror");
        window.dispatchEvent(new CustomEvent("hypergen.post.after"));
        onError();
    };
    xhr.onabort = ()=>{
        console.error("xhr onabort");
        window.dispatchEvent(new CustomEvent("hypergen.post.after"));
        onError();
    };
    xhr.ontimeout = ()=>{
        console.error("xhr ontimeout");
        window.dispatchEvent(new CustomEvent("hypergen.post.after"));
        onError();
    };
    xhr.open("POST", url);
    xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest");
    xhr.setRequestHeader("X-Pathname", parent.window.location.pathname);
    xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
    if (!!headers) for(let k in headers){
        console.log("Setting custom header", k, "to", headers[k]);
        xhr.setRequestHeader(k, headers[k]);
    }
    window.dispatchEvent(new CustomEvent("hypergen.post.before"));
    xhr.send(formData);
};
// history support.
window.addEventListener("popstate", function(event) {
    if (event.state && event.state.callback_url !== undefined) {
        console.log("popstate to partial load");
        partialLoad(event, event.state.callback_url);
    } else window.location = location.href;
});
const pushstate = new Event("hypergen.pushstate");
const onpushstate = function() {
    document.dispatchEvent(pushstate);
};
const ready = function(fn, { partial = false } = {}) {
    if (document.readyState != "loading") fn();
    else if (document.addEventListener) document.addEventListener("DOMContentLoaded", fn);
    else document.attachEvent("onreadystatechange", function() {
        if (document.readyState != "loading") fn();
    });
    if (partial) document.addEventListener("hypergen.pushstate", fn);
};

},{"morphdom":"ggNB9","./hypergen":"5r9D8","@parcel/transformer-js/src/esmodule-helpers.js":"gkKU3","./websocket":"htIzP"}],"ggNB9":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
var DOCUMENT_FRAGMENT_NODE = 11;
function morphAttrs(fromNode, toNode) {
    var toNodeAttrs = toNode.attributes;
    var attr;
    var attrName;
    var attrNamespaceURI;
    var attrValue;
    var fromValue;
    // document-fragments dont have attributes so lets not do anything
    if (toNode.nodeType === DOCUMENT_FRAGMENT_NODE || fromNode.nodeType === DOCUMENT_FRAGMENT_NODE) return;
    // update attributes on original DOM element
    for(var i = toNodeAttrs.length - 1; i >= 0; i--){
        attr = toNodeAttrs[i];
        attrName = attr.name;
        attrNamespaceURI = attr.namespaceURI;
        attrValue = attr.value;
        if (attrNamespaceURI) {
            attrName = attr.localName || attrName;
            fromValue = fromNode.getAttributeNS(attrNamespaceURI, attrName);
            if (fromValue !== attrValue) {
                if (attr.prefix === "xmlns") attrName = attr.name; // It's not allowed to set an attribute with the XMLNS namespace without specifying the `xmlns` prefix
                fromNode.setAttributeNS(attrNamespaceURI, attrName, attrValue);
            }
        } else {
            fromValue = fromNode.getAttribute(attrName);
            if (fromValue !== attrValue) fromNode.setAttribute(attrName, attrValue);
        }
    }
    // Remove any extra attributes found on the original DOM element that
    // weren't found on the target element.
    var fromNodeAttrs = fromNode.attributes;
    for(var d = fromNodeAttrs.length - 1; d >= 0; d--){
        attr = fromNodeAttrs[d];
        attrName = attr.name;
        attrNamespaceURI = attr.namespaceURI;
        if (attrNamespaceURI) {
            attrName = attr.localName || attrName;
            if (!toNode.hasAttributeNS(attrNamespaceURI, attrName)) fromNode.removeAttributeNS(attrNamespaceURI, attrName);
        } else if (!toNode.hasAttribute(attrName)) fromNode.removeAttribute(attrName);
    }
}
var range; // Create a range object for efficently rendering strings to elements.
var NS_XHTML = "http://www.w3.org/1999/xhtml";
var doc = typeof document === "undefined" ? undefined : document;
var HAS_TEMPLATE_SUPPORT = !!doc && "content" in doc.createElement("template");
var HAS_RANGE_SUPPORT = !!doc && doc.createRange && "createContextualFragment" in doc.createRange();
function createFragmentFromTemplate(str) {
    var template = doc.createElement("template");
    template.innerHTML = str;
    return template.content.childNodes[0];
}
function createFragmentFromRange(str) {
    if (!range) {
        range = doc.createRange();
        range.selectNode(doc.body);
    }
    var fragment = range.createContextualFragment(str);
    return fragment.childNodes[0];
}
function createFragmentFromWrap(str) {
    var fragment = doc.createElement("body");
    fragment.innerHTML = str;
    return fragment.childNodes[0];
}
/**
 * This is about the same
 * var html = new DOMParser().parseFromString(str, 'text/html');
 * return html.body.firstChild;
 *
 * @method toElement
 * @param {String} str
 */ function toElement(str) {
    str = str.trim();
    if (HAS_TEMPLATE_SUPPORT) // avoid restrictions on content for things like `<tr><th>Hi</th></tr>` which
    // createContextualFragment doesn't support
    // <template> support not available in IE
    return createFragmentFromTemplate(str);
    else if (HAS_RANGE_SUPPORT) return createFragmentFromRange(str);
    return createFragmentFromWrap(str);
}
/**
 * Returns true if two node's names are the same.
 *
 * NOTE: We don't bother checking `namespaceURI` because you will never find two HTML elements with the same
 *       nodeName and different namespace URIs.
 *
 * @param {Element} a
 * @param {Element} b The target element
 * @return {boolean}
 */ function compareNodeNames(fromEl, toEl) {
    var fromNodeName = fromEl.nodeName;
    var toNodeName = toEl.nodeName;
    var fromCodeStart, toCodeStart;
    if (fromNodeName === toNodeName) return true;
    fromCodeStart = fromNodeName.charCodeAt(0);
    toCodeStart = toNodeName.charCodeAt(0);
    // If the target element is a virtual DOM node or SVG node then we may
    // need to normalize the tag name before comparing. Normal HTML elements that are
    // in the "http://www.w3.org/1999/xhtml"
    // are converted to upper case
    if (fromCodeStart <= 90 && toCodeStart >= 97) return fromNodeName === toNodeName.toUpperCase();
    else if (toCodeStart <= 90 && fromCodeStart >= 97) return toNodeName === fromNodeName.toUpperCase();
    else return false;
}
/**
 * Create an element, optionally with a known namespace URI.
 *
 * @param {string} name the element name, e.g. 'div' or 'svg'
 * @param {string} [namespaceURI] the element's namespace URI, i.e. the value of
 * its `xmlns` attribute or its inferred namespace.
 *
 * @return {Element}
 */ function createElementNS(name, namespaceURI) {
    return !namespaceURI || namespaceURI === NS_XHTML ? doc.createElement(name) : doc.createElementNS(namespaceURI, name);
}
/**
 * Copies the children of one DOM element to another DOM element
 */ function moveChildren(fromEl, toEl) {
    var curChild = fromEl.firstChild;
    while(curChild){
        var nextChild = curChild.nextSibling;
        toEl.appendChild(curChild);
        curChild = nextChild;
    }
    return toEl;
}
function syncBooleanAttrProp(fromEl, toEl, name) {
    if (fromEl[name] !== toEl[name]) {
        fromEl[name] = toEl[name];
        if (fromEl[name]) fromEl.setAttribute(name, "");
        else fromEl.removeAttribute(name);
    }
}
var specialElHandlers = {
    OPTION: function(fromEl, toEl) {
        var parentNode = fromEl.parentNode;
        if (parentNode) {
            var parentName = parentNode.nodeName.toUpperCase();
            if (parentName === "OPTGROUP") {
                parentNode = parentNode.parentNode;
                parentName = parentNode && parentNode.nodeName.toUpperCase();
            }
            if (parentName === "SELECT" && !parentNode.hasAttribute("multiple")) {
                if (fromEl.hasAttribute("selected") && !toEl.selected) {
                    // Workaround for MS Edge bug where the 'selected' attribute can only be
                    // removed if set to a non-empty value:
                    // https://developer.microsoft.com/en-us/microsoft-edge/platform/issues/12087679/
                    fromEl.setAttribute("selected", "selected");
                    fromEl.removeAttribute("selected");
                }
                // We have to reset select element's selectedIndex to -1, otherwise setting
                // fromEl.selected using the syncBooleanAttrProp below has no effect.
                // The correct selectedIndex will be set in the SELECT special handler below.
                parentNode.selectedIndex = -1;
            }
        }
        syncBooleanAttrProp(fromEl, toEl, "selected");
    },
    /**
     * The "value" attribute is special for the <input> element since it sets
     * the initial value. Changing the "value" attribute without changing the
     * "value" property will have no effect since it is only used to the set the
     * initial value.  Similar for the "checked" attribute, and "disabled".
     */ INPUT: function(fromEl, toEl) {
        syncBooleanAttrProp(fromEl, toEl, "checked");
        syncBooleanAttrProp(fromEl, toEl, "disabled");
        if (fromEl.value !== toEl.value) fromEl.value = toEl.value;
        if (!toEl.hasAttribute("value")) fromEl.removeAttribute("value");
    },
    TEXTAREA: function(fromEl, toEl) {
        var newValue = toEl.value;
        if (fromEl.value !== newValue) fromEl.value = newValue;
        var firstChild = fromEl.firstChild;
        if (firstChild) {
            // Needed for IE. Apparently IE sets the placeholder as the
            // node value and vise versa. This ignores an empty update.
            var oldValue = firstChild.nodeValue;
            if (oldValue == newValue || !newValue && oldValue == fromEl.placeholder) return;
            firstChild.nodeValue = newValue;
        }
    },
    SELECT: function(fromEl, toEl) {
        if (!toEl.hasAttribute("multiple")) {
            var selectedIndex = -1;
            var i = 0;
            // We have to loop through children of fromEl, not toEl since nodes can be moved
            // from toEl to fromEl directly when morphing.
            // At the time this special handler is invoked, all children have already been morphed
            // and appended to / removed from fromEl, so using fromEl here is safe and correct.
            var curChild = fromEl.firstChild;
            var optgroup;
            var nodeName;
            while(curChild){
                nodeName = curChild.nodeName && curChild.nodeName.toUpperCase();
                if (nodeName === "OPTGROUP") {
                    optgroup = curChild;
                    curChild = optgroup.firstChild;
                } else {
                    if (nodeName === "OPTION") {
                        if (curChild.hasAttribute("selected")) {
                            selectedIndex = i;
                            break;
                        }
                        i++;
                    }
                    curChild = curChild.nextSibling;
                    if (!curChild && optgroup) {
                        curChild = optgroup.nextSibling;
                        optgroup = null;
                    }
                }
            }
            fromEl.selectedIndex = selectedIndex;
        }
    }
};
var ELEMENT_NODE = 1;
var DOCUMENT_FRAGMENT_NODE$1 = 11;
var TEXT_NODE = 3;
var COMMENT_NODE = 8;
function noop() {}
function defaultGetNodeKey(node) {
    if (node) return node.getAttribute && node.getAttribute("id") || node.id;
}
function morphdomFactory(morphAttrs) {
    return function morphdom(fromNode, toNode, options) {
        if (!options) options = {};
        if (typeof toNode === "string") {
            if (fromNode.nodeName === "#document" || fromNode.nodeName === "HTML" || fromNode.nodeName === "BODY") {
                var toNodeHtml = toNode;
                toNode = doc.createElement("html");
                toNode.innerHTML = toNodeHtml;
            } else toNode = toElement(toNode);
        }
        var getNodeKey = options.getNodeKey || defaultGetNodeKey;
        var onBeforeNodeAdded = options.onBeforeNodeAdded || noop;
        var onNodeAdded = options.onNodeAdded || noop;
        var onBeforeElUpdated = options.onBeforeElUpdated || noop;
        var onElUpdated = options.onElUpdated || noop;
        var onBeforeNodeDiscarded = options.onBeforeNodeDiscarded || noop;
        var onNodeDiscarded = options.onNodeDiscarded || noop;
        var onBeforeElChildrenUpdated = options.onBeforeElChildrenUpdated || noop;
        var childrenOnly = options.childrenOnly === true;
        // This object is used as a lookup to quickly find all keyed elements in the original DOM tree.
        var fromNodesLookup = Object.create(null);
        var keyedRemovalList = [];
        function addKeyedRemoval(key) {
            keyedRemovalList.push(key);
        }
        function walkDiscardedChildNodes(node, skipKeyedNodes) {
            if (node.nodeType === ELEMENT_NODE) {
                var curChild = node.firstChild;
                while(curChild){
                    var key = undefined;
                    if (skipKeyedNodes && (key = getNodeKey(curChild))) // If we are skipping keyed nodes then we add the key
                    // to a list so that it can be handled at the very end.
                    addKeyedRemoval(key);
                    else {
                        // Only report the node as discarded if it is not keyed. We do this because
                        // at the end we loop through all keyed elements that were unmatched
                        // and then discard them in one final pass.
                        onNodeDiscarded(curChild);
                        if (curChild.firstChild) walkDiscardedChildNodes(curChild, skipKeyedNodes);
                    }
                    curChild = curChild.nextSibling;
                }
            }
        }
        /**
         * Removes a DOM node out of the original DOM
         *
         * @param  {Node} node The node to remove
         * @param  {Node} parentNode The nodes parent
         * @param  {Boolean} skipKeyedNodes If true then elements with keys will be skipped and not discarded.
         * @return {undefined}
         */ function removeNode(node, parentNode, skipKeyedNodes) {
            if (onBeforeNodeDiscarded(node) === false) return;
            if (parentNode) parentNode.removeChild(node);
            onNodeDiscarded(node);
            walkDiscardedChildNodes(node, skipKeyedNodes);
        }
        // // TreeWalker implementation is no faster, but keeping this around in case this changes in the future
        // function indexTree(root) {
        //     var treeWalker = document.createTreeWalker(
        //         root,
        //         NodeFilter.SHOW_ELEMENT);
        //
        //     var el;
        //     while((el = treeWalker.nextNode())) {
        //         var key = getNodeKey(el);
        //         if (key) {
        //             fromNodesLookup[key] = el;
        //         }
        //     }
        // }
        // // NodeIterator implementation is no faster, but keeping this around in case this changes in the future
        //
        // function indexTree(node) {
        //     var nodeIterator = document.createNodeIterator(node, NodeFilter.SHOW_ELEMENT);
        //     var el;
        //     while((el = nodeIterator.nextNode())) {
        //         var key = getNodeKey(el);
        //         if (key) {
        //             fromNodesLookup[key] = el;
        //         }
        //     }
        // }
        function indexTree(node) {
            if (node.nodeType === ELEMENT_NODE || node.nodeType === DOCUMENT_FRAGMENT_NODE$1) {
                var curChild = node.firstChild;
                while(curChild){
                    var key = getNodeKey(curChild);
                    if (key) fromNodesLookup[key] = curChild;
                    // Walk recursively
                    indexTree(curChild);
                    curChild = curChild.nextSibling;
                }
            }
        }
        indexTree(fromNode);
        function handleNodeAdded(el) {
            onNodeAdded(el);
            var curChild = el.firstChild;
            while(curChild){
                var nextSibling = curChild.nextSibling;
                var key = getNodeKey(curChild);
                if (key) {
                    var unmatchedFromEl = fromNodesLookup[key];
                    // if we find a duplicate #id node in cache, replace `el` with cache value
                    // and morph it to the child node.
                    if (unmatchedFromEl && compareNodeNames(curChild, unmatchedFromEl)) {
                        curChild.parentNode.replaceChild(unmatchedFromEl, curChild);
                        morphEl(unmatchedFromEl, curChild);
                    } else handleNodeAdded(curChild);
                } else // recursively call for curChild and it's children to see if we find something in
                // fromNodesLookup
                handleNodeAdded(curChild);
                curChild = nextSibling;
            }
        }
        function cleanupFromEl(fromEl, curFromNodeChild, curFromNodeKey) {
            // We have processed all of the "to nodes". If curFromNodeChild is
            // non-null then we still have some from nodes left over that need
            // to be removed
            while(curFromNodeChild){
                var fromNextSibling = curFromNodeChild.nextSibling;
                if (curFromNodeKey = getNodeKey(curFromNodeChild)) // Since the node is keyed it might be matched up later so we defer
                // the actual removal to later
                addKeyedRemoval(curFromNodeKey);
                else // NOTE: we skip nested keyed nodes from being removed since there is
                //       still a chance they will be matched up later
                removeNode(curFromNodeChild, fromEl, true);
                curFromNodeChild = fromNextSibling;
            }
        }
        function morphEl(fromEl, toEl, childrenOnly) {
            var toElKey = getNodeKey(toEl);
            if (toElKey) // If an element with an ID is being morphed then it will be in the final
            // DOM so clear it out of the saved elements collection
            delete fromNodesLookup[toElKey];
            if (!childrenOnly) {
                // optional
                if (onBeforeElUpdated(fromEl, toEl) === false) return;
                // update attributes on original DOM element first
                morphAttrs(fromEl, toEl);
                // optional
                onElUpdated(fromEl);
                if (onBeforeElChildrenUpdated(fromEl, toEl) === false) return;
            }
            if (fromEl.nodeName !== "TEXTAREA") morphChildren(fromEl, toEl);
            else specialElHandlers.TEXTAREA(fromEl, toEl);
        }
        function morphChildren(fromEl, toEl) {
            var curToNodeChild = toEl.firstChild;
            var curFromNodeChild = fromEl.firstChild;
            var curToNodeKey;
            var curFromNodeKey;
            var fromNextSibling;
            var toNextSibling;
            var matchingFromEl;
            // walk the children
            outer: while(curToNodeChild){
                toNextSibling = curToNodeChild.nextSibling;
                curToNodeKey = getNodeKey(curToNodeChild);
                // walk the fromNode children all the way through
                while(curFromNodeChild){
                    fromNextSibling = curFromNodeChild.nextSibling;
                    if (curToNodeChild.isSameNode && curToNodeChild.isSameNode(curFromNodeChild)) {
                        curToNodeChild = toNextSibling;
                        curFromNodeChild = fromNextSibling;
                        continue outer;
                    }
                    curFromNodeKey = getNodeKey(curFromNodeChild);
                    var curFromNodeType = curFromNodeChild.nodeType;
                    // this means if the curFromNodeChild doesnt have a match with the curToNodeChild
                    var isCompatible = undefined;
                    if (curFromNodeType === curToNodeChild.nodeType) {
                        if (curFromNodeType === ELEMENT_NODE) {
                            // Both nodes being compared are Element nodes
                            if (curToNodeKey) // The target node has a key so we want to match it up with the correct element
                            // in the original DOM tree
                            {
                                if (curToNodeKey !== curFromNodeKey) {
                                    // The current element in the original DOM tree does not have a matching key so
                                    // let's check our lookup to see if there is a matching element in the original
                                    // DOM tree
                                    if (matchingFromEl = fromNodesLookup[curToNodeKey]) {
                                        if (fromNextSibling === matchingFromEl) // Special case for single element removals. To avoid removing the original
                                        // DOM node out of the tree (since that can break CSS transitions, etc.),
                                        // we will instead discard the current node and wait until the next
                                        // iteration to properly match up the keyed target element with its matching
                                        // element in the original tree
                                        isCompatible = false;
                                        else {
                                            // We found a matching keyed element somewhere in the original DOM tree.
                                            // Let's move the original DOM node into the current position and morph
                                            // it.
                                            // NOTE: We use insertBefore instead of replaceChild because we want to go through
                                            // the `removeNode()` function for the node that is being discarded so that
                                            // all lifecycle hooks are correctly invoked
                                            fromEl.insertBefore(matchingFromEl, curFromNodeChild);
                                            // fromNextSibling = curFromNodeChild.nextSibling;
                                            if (curFromNodeKey) // Since the node is keyed it might be matched up later so we defer
                                            // the actual removal to later
                                            addKeyedRemoval(curFromNodeKey);
                                            else // NOTE: we skip nested keyed nodes from being removed since there is
                                            //       still a chance they will be matched up later
                                            removeNode(curFromNodeChild, fromEl, true);
                                            curFromNodeChild = matchingFromEl;
                                        }
                                    } else // The nodes are not compatible since the "to" node has a key and there
                                    // is no matching keyed node in the source tree
                                    isCompatible = false;
                                }
                            } else if (curFromNodeKey) // The original has a key
                            isCompatible = false;
                            isCompatible = isCompatible !== false && compareNodeNames(curFromNodeChild, curToNodeChild);
                            if (isCompatible) // We found compatible DOM elements so transform
                            // the current "from" node to match the current
                            // target DOM node.
                            // MORPH
                            morphEl(curFromNodeChild, curToNodeChild);
                        } else if (curFromNodeType === TEXT_NODE || curFromNodeType == COMMENT_NODE) {
                            // Both nodes being compared are Text or Comment nodes
                            isCompatible = true;
                            // Simply update nodeValue on the original node to
                            // change the text value
                            if (curFromNodeChild.nodeValue !== curToNodeChild.nodeValue) curFromNodeChild.nodeValue = curToNodeChild.nodeValue;
                        }
                    }
                    if (isCompatible) {
                        // Advance both the "to" child and the "from" child since we found a match
                        // Nothing else to do as we already recursively called morphChildren above
                        curToNodeChild = toNextSibling;
                        curFromNodeChild = fromNextSibling;
                        continue outer;
                    }
                    // No compatible match so remove the old node from the DOM and continue trying to find a
                    // match in the original DOM. However, we only do this if the from node is not keyed
                    // since it is possible that a keyed node might match up with a node somewhere else in the
                    // target tree and we don't want to discard it just yet since it still might find a
                    // home in the final DOM tree. After everything is done we will remove any keyed nodes
                    // that didn't find a home
                    if (curFromNodeKey) // Since the node is keyed it might be matched up later so we defer
                    // the actual removal to later
                    addKeyedRemoval(curFromNodeKey);
                    else // NOTE: we skip nested keyed nodes from being removed since there is
                    //       still a chance they will be matched up later
                    removeNode(curFromNodeChild, fromEl, true);
                    curFromNodeChild = fromNextSibling;
                } // END: while(curFromNodeChild) {}
                // If we got this far then we did not find a candidate match for
                // our "to node" and we exhausted all of the children "from"
                // nodes. Therefore, we will just append the current "to" node
                // to the end
                if (curToNodeKey && (matchingFromEl = fromNodesLookup[curToNodeKey]) && compareNodeNames(matchingFromEl, curToNodeChild)) {
                    fromEl.appendChild(matchingFromEl);
                    // MORPH
                    morphEl(matchingFromEl, curToNodeChild);
                } else {
                    var onBeforeNodeAddedResult = onBeforeNodeAdded(curToNodeChild);
                    if (onBeforeNodeAddedResult !== false) {
                        if (onBeforeNodeAddedResult) curToNodeChild = onBeforeNodeAddedResult;
                        if (curToNodeChild.actualize) curToNodeChild = curToNodeChild.actualize(fromEl.ownerDocument || doc);
                        fromEl.appendChild(curToNodeChild);
                        handleNodeAdded(curToNodeChild);
                    }
                }
                curToNodeChild = toNextSibling;
                curFromNodeChild = fromNextSibling;
            }
            cleanupFromEl(fromEl, curFromNodeChild, curFromNodeKey);
            var specialElHandler = specialElHandlers[fromEl.nodeName];
            if (specialElHandler) specialElHandler(fromEl, toEl);
        } // END: morphChildren(...)
        var morphedNode = fromNode;
        var morphedNodeType = morphedNode.nodeType;
        var toNodeType = toNode.nodeType;
        if (!childrenOnly) {
            // Handle the case where we are given two DOM nodes that are not
            // compatible (e.g. <div> --> <span> or <div> --> TEXT)
            if (morphedNodeType === ELEMENT_NODE) {
                if (toNodeType === ELEMENT_NODE) {
                    if (!compareNodeNames(fromNode, toNode)) {
                        onNodeDiscarded(fromNode);
                        morphedNode = moveChildren(fromNode, createElementNS(toNode.nodeName, toNode.namespaceURI));
                    }
                } else // Going from an element node to a text node
                morphedNode = toNode;
            } else if (morphedNodeType === TEXT_NODE || morphedNodeType === COMMENT_NODE) {
                if (toNodeType === morphedNodeType) {
                    if (morphedNode.nodeValue !== toNode.nodeValue) morphedNode.nodeValue = toNode.nodeValue;
                    return morphedNode;
                } else // Text node to something else
                morphedNode = toNode;
            }
        }
        if (morphedNode === toNode) // The "to node" was not compatible with the "from node" so we had to
        // toss out the "from node" and use the "to node"
        onNodeDiscarded(fromNode);
        else {
            if (toNode.isSameNode && toNode.isSameNode(morphedNode)) return;
            morphEl(morphedNode, toNode, childrenOnly);
            // We now need to loop over any keyed nodes that might need to be
            // removed. We only do the removal if we know that the keyed node
            // never found a match. When a keyed node is matched up we remove
            // it out of fromNodesLookup and we use fromNodesLookup to determine
            // if a keyed node has been matched up or not
            if (keyedRemovalList) for(var i = 0, len = keyedRemovalList.length; i < len; i++){
                var elToRemove = fromNodesLookup[keyedRemovalList[i]];
                if (elToRemove) removeNode(elToRemove, elToRemove.parentNode, false);
            }
        }
        if (!childrenOnly && morphedNode !== fromNode && fromNode.parentNode) {
            if (morphedNode.actualize) morphedNode = morphedNode.actualize(fromNode.ownerDocument || doc);
            // If we had to swap out the from node with a new node because the old
            // node was not compatible with the target node then we need to
            // replace the old DOM node in the original DOM tree. This is only
            // possible if the original DOM node was part of a DOM tree which
            // we know is the case if it has a parent node.
            fromNode.parentNode.replaceChild(morphedNode, fromNode);
        }
        return morphedNode;
    };
}
var morphdom = morphdomFactory(morphAttrs);
exports.default = morphdom;

},{"@parcel/transformer-js/src/esmodule-helpers.js":"gkKU3"}],"gkKU3":[function(require,module,exports) {
exports.interopDefault = function(a) {
    return a && a.__esModule ? a : {
        default: a
    };
};
exports.defineInteropFlag = function(a) {
    Object.defineProperty(a, "__esModule", {
        value: true
    });
};
exports.exportAll = function(source, dest) {
    Object.keys(source).forEach(function(key) {
        if (key === "default" || key === "__esModule" || dest.hasOwnProperty(key)) return;
        Object.defineProperty(dest, key, {
            enumerable: true,
            get: function() {
                return source[key];
            }
        });
    });
    return dest;
};
exports.export = function(dest, destName, get) {
    Object.defineProperty(dest, destName, {
        enumerable: true,
        get: get
    });
};

},{}],"htIzP":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
parcelHelpers.export(exports, "WEBSOCKETS", ()=>WEBSOCKETS);
parcelHelpers.export(exports, "open", ()=>open);
parcelHelpers.export(exports, "close", ()=>close);
var _sockette = require("sockette");
var _socketteDefault = parcelHelpers.interopDefault(_sockette);
const WEBSOCKETS = {};
const log = function(e, action, url, options) {
    console.log("Websocket " + action + " to url", url, "with options", options, "and event", e);
};
const open = function(url, options) {
    if (!options) options = {};
    if (!!WEBSOCKETS[url]) {
        log(null, "ALREADY_OPENED_BYE", url, options);
        return;
    }
    WEBSOCKETS[url] = new (0, _socketteDefault.default)(url, Object.assign({
        timeout: 1e3,
        maxAttempts: Number.MAX_SAFE_INTEGER,
        onopen: (e)=>log(e, "OPENED", url, options),
        onmessage: (e)=>{
            hypergen.applyCommands(JSON.parse(e.data));
        },
        onreconnect: (e)=>log(e, "RECONNECTING", url, options),
        onmaximum: (e)=>log(e, "MAX_RECONNECTS_BYE", url, options),
        onclose: (e)=>{
            log(e, "CLOSED", url, options);
        },
        onerror: (e)=>console.log("Error:", e)
    }, options));
};
const close = function(url) {
    if (!WEBSOCKETS[url]) {
        log(null, "ALREADY_CLOSED_BYE", url, null);
        return;
    }
    WEBSOCKETS[url].close();
    delete WEBSOCKETS[url];
    log(null, "CLOSED_AND_DELETED", url, null);
};

},{"sockette":"60KBR","@parcel/transformer-js/src/esmodule-helpers.js":"gkKU3"}],"60KBR":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
parcelHelpers.export(exports, "default", ()=>function(url, opts) {
        opts = opts || {};
        var ws, num = 0, timer = 1, $ = {};
        var max = opts.maxAttempts || Infinity;
        $.open = function() {
            ws = new WebSocket(url, opts.protocols || []);
            ws.onmessage = opts.onmessage || noop;
            ws.onopen = function(e) {
                (opts.onopen || noop)(e);
                num = 0;
            };
            ws.onclose = function(e) {
                e.code === 1e3 || e.code === 1001 || e.code === 1005 || $.reconnect(e);
                (opts.onclose || noop)(e);
            };
            ws.onerror = function(e) {
                e && e.code === "ECONNREFUSED" ? $.reconnect(e) : (opts.onerror || noop)(e);
            };
        };
        $.reconnect = function(e) {
            if (timer && num++ < max) timer = setTimeout(function() {
                (opts.onreconnect || noop)(e);
                $.open();
            }, opts.timeout || 1e3);
            else (opts.onmaximum || noop)(e);
        };
        $.json = function(x) {
            ws.send(JSON.stringify(x));
        };
        $.send = function(x) {
            ws.send(x);
        };
        $.close = function(x, y) {
            timer = clearTimeout(timer);
            ws.close(x || 1e3, y);
        };
        $.open(); // init
        return $;
    });
function noop() {}

},{"@parcel/transformer-js/src/esmodule-helpers.js":"gkKU3"}]},["jgsYR","5r9D8"], "5r9D8", "parcelRequire94c2")

//# sourceMappingURL=hypergen.js.map
