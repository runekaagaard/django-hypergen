(()=>{function e(e,t,n,o){Object.defineProperty(e,t,{get:n,set:o,enumerable:!0,configurable:!0})}var t,n,o={};e(o,"morph",()=>b),e(o,"remove",()=>N),e(o,"hide",()=>T),e(o,"display",()=>S),e(o,"visible",()=>C),e(o,"hidden",()=>w),e(o,"redirect",()=>A),e(o,"append",()=>I),e(o,"prepend",()=>O),e(o,"setClientState",()=>k),e(o,"intervalSet",()=>R),e(o,"applyCommands",()=>K),e(o,"intervalClear",()=>B),e(o,"addEventListener",()=>_),e(o,"callback",()=>F),e(o,"keypressToCallback",()=>H),e(o,"keypressToCallbackRemove",()=>P),e(o,"throttle",()=>q),e(o,"partialLoad",()=>W),e(o,"onpushstate",()=>ei),e(o,"cancelThrottle",()=>V),e(o,"event",()=>Y),e(o,"coerce",()=>Q),e(o,"read",()=>Z),e(o,"when",()=>ee),e(o,"element",()=>et),e(o,"reviver",()=>en),e(o,"ready",()=>ea);var r="undefined"==typeof document?void 0:document,l=!!r&&"content"in r.createElement("template"),i=!!r&&r.createRange&&"createContextualFragment"in r.createRange();/**
 * Returns true if two node's names are the same.
 *
 * NOTE: We don't bother checking `namespaceURI` because you will never find two HTML elements with the same
 *       nodeName and different namespace URIs.
 *
 * @param {Element} a
 * @param {Element} b The target element
 * @return {boolean}
 */function a(e,t){var n,o,r=e.nodeName,l=t.nodeName;return r===l||((n=r.charCodeAt(0),o=l.charCodeAt(0),n<=90&&o>=97)?r===l.toUpperCase():o<=90&&n>=97&&l===r.toUpperCase())}function d(e,t,n){e[n]!==t[n]&&(e[n]=t[n],e[n]?e.setAttribute(n,""):e.removeAttribute(n))}var u={OPTION:function(e,t){var n=e.parentNode;if(n){var o=n.nodeName.toUpperCase();"OPTGROUP"===o&&(o=(n=n.parentNode)&&n.nodeName.toUpperCase()),"SELECT"!==o||n.hasAttribute("multiple")||(e.hasAttribute("selected")&&!t.selected&&(// Workaround for MS Edge bug where the 'selected' attribute can only be
// removed if set to a non-empty value:
// https://developer.microsoft.com/en-us/microsoft-edge/platform/issues/12087679/
e.setAttribute("selected","selected"),e.removeAttribute("selected")),// We have to reset select element's selectedIndex to -1, otherwise setting
// fromEl.selected using the syncBooleanAttrProp below has no effect.
// The correct selectedIndex will be set in the SELECT special handler below.
n.selectedIndex=-1)}d(e,t,"selected")},/**
     * The "value" attribute is special for the <input> element since it sets
     * the initial value. Changing the "value" attribute without changing the
     * "value" property will have no effect since it is only used to the set the
     * initial value.  Similar for the "checked" attribute, and "disabled".
     */INPUT:function(e,t){d(e,t,"checked"),d(e,t,"disabled"),e.value!==t.value&&(e.value=t.value),t.hasAttribute("value")||e.removeAttribute("value")},TEXTAREA:function(e,t){var n=t.value;e.value!==n&&(e.value=n);var o=e.firstChild;if(o){// Needed for IE. Apparently IE sets the placeholder as the
// node value and vise versa. This ignores an empty update.
var r=o.nodeValue;if(r==n||!n&&r==e.placeholder)return;o.nodeValue=n}},SELECT:function(e,t){if(!t.hasAttribute("multiple")){for(var n,o,r=-1,l=0,i=e.firstChild;i;)if("OPTGROUP"===(o=i.nodeName&&i.nodeName.toUpperCase()))i=(n=i).firstChild;else{if("OPTION"===o){if(i.hasAttribute("selected")){r=l;break}l++}(i=i.nextSibling)||!n||(i=n.nextSibling,n=null)}e.selectedIndex=r}}};function c(){}function s(e){if(e)return e.getAttribute&&e.getAttribute("id")||e.id}var f=(t=function(e,t){var n,o,r,l,i=t.attributes;// document-fragments dont have attributes so lets not do anything
if(11!==t.nodeType&&11!==e.nodeType){// update attributes on original DOM element
for(var a=i.length-1;a>=0;a--)o=(n=i[a]).name,r=n.namespaceURI,l=n.value,r?(o=n.localName||o,e.getAttributeNS(r,o)!==l&&("xmlns"===n.prefix&&(o=n.name),e.setAttributeNS(r,o,l))):e.getAttribute(o)!==l&&e.setAttribute(o,l);for(var d=e.attributes,u=d.length-1;u>=0;u--)o=(n=d[u]).name,(r=n.namespaceURI)?(o=n.localName||o,t.hasAttributeNS(r,o)||e.removeAttributeNS(r,o)):t.hasAttribute(o)||e.removeAttribute(o)}},function(e,o,d){if(d||(d={}),"string"==typeof o){if("#document"===e.nodeName||"HTML"===e.nodeName||"BODY"===e.nodeName){var f,p,m,h,g,v,y,E,b=o;(o=r.createElement("html")).innerHTML=b}else f=(f=o).trim(),o=l?(p=f,(m=r.createElement("template")).innerHTML=p,m.content.childNodes[0]):i?(h=f,n||(n=r.createRange()).selectNode(r.body),n.createContextualFragment(h).childNodes[0]):(g=f,(v=r.createElement("body")).innerHTML=g,v.childNodes[0])}var N=d.getNodeKey||s,T=d.onBeforeNodeAdded||c,S=d.onNodeAdded||c,C=d.onBeforeElUpdated||c,w=d.onElUpdated||c,A=d.onBeforeNodeDiscarded||c,I=d.onNodeDiscarded||c,O=d.onBeforeElChildrenUpdated||c,k=!0===d.childrenOnly,L=Object.create(null),R=[];function B(e){R.push(e)}/**
         * Removes a DOM node out of the original DOM
         *
         * @param  {Node} node The node to remove
         * @param  {Node} parentNode The nodes parent
         * @param  {Boolean} skipKeyedNodes If true then elements with keys will be skipped and not discarded.
         * @return {undefined}
         */function _(e,t,n){!1!==A(e)&&(t&&t.removeChild(e),I(e),function e(t,n){if(1===t.nodeType)for(var o=t.firstChild;o;){var r=void 0;n&&(r=N(o))?// to a list so that it can be handled at the very end.
B(r):(// Only report the node as discarded if it is not keyed. We do this because
// at the end we loop through all keyed elements that were unmatched
// and then discard them in one final pass.
I(o),o.firstChild&&e(o,n)),o=o.nextSibling}}(e,n))}!// // TreeWalker implementation is no faster, but keeping this around in case this changes in the future
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
function e(t){if(1===t.nodeType||11===t.nodeType)for(var n=t.firstChild;n;){var o=N(n);o&&(L[o]=n),// Walk recursively
e(n),n=n.nextSibling}}(e);var U=e,x=U.nodeType,H=o.nodeType;if(!k){// Handle the case where we are given two DOM nodes that are not
// compatible (e.g. <div> --> <span> or <div> --> TEXT)
if(1===x)1===H?a(e,o)||(I(e),U=/**
 * Copies the children of one DOM element to another DOM element
 */function(e,t){for(var n=e.firstChild;n;){var o=n.nextSibling;t.appendChild(n),n=o}return t}(e,(y=o.nodeName,(E=o.namespaceURI)&&"http://www.w3.org/1999/xhtml"!==E?r.createElementNS(E,y):r.createElement(y)))):U=o;else if(3===x||8===x){if(H===x)return U.nodeValue!==o.nodeValue&&(U.nodeValue=o.nodeValue),U;U=o}}if(U===o)// toss out the "from node" and use the "to node"
I(e);else{if(o.isSameNode&&o.isSameNode(U))return;// We now need to loop over any keyed nodes that might need to be
// removed. We only do the removal if we know that the keyed node
// never found a match. When a keyed node is matched up we remove
// it out of fromNodesLookup and we use fromNodesLookup to determine
// if a keyed node has been matched up or not
if(function e(n,o,l){var i=N(o);i&&// DOM so clear it out of the saved elements collection
delete L[i],(l||!1!==C(n,o)&&(// update attributes on original DOM element first
t(n,o),// optional
w(n),!1!==O(n,o)))&&("TEXTAREA"!==n.nodeName?function(t,n){var o,l,i,d,c,s=n.firstChild,f=t.firstChild;// walk the children
e:for(;s;){// walk the fromNode children all the way through
for(d=s.nextSibling,o=N(s);f;){if(i=f.nextSibling,s.isSameNode&&s.isSameNode(f)){s=d,f=i;continue e}l=N(f);var p=f.nodeType,m=void 0;if(p===s.nodeType&&(1===p?(o?o!==l&&((c=L[o])?i===c?// DOM node out of the tree (since that can break CSS transitions, etc.),
// we will instead discard the current node and wait until the next
// iteration to properly match up the keyed target element with its matching
// element in the original tree
m=!1:(// We found a matching keyed element somewhere in the original DOM tree.
// Let's move the original DOM node into the current position and morph
// it.
// NOTE: We use insertBefore instead of replaceChild because we want to go through
// the `removeNode()` function for the node that is being discarded so that
// all lifecycle hooks are correctly invoked
t.insertBefore(c,f),l?// the actual removal to later
B(l)://       still a chance they will be matched up later
_(f,t,!0),f=c):// is no matching keyed node in the source tree
m=!1):l&&(m=!1),(m=!1!==m&&a(f,s))&&// the current "from" node to match the current
// target DOM node.
// MORPH
e(f,s)):(3===p||8==p)&&(// Both nodes being compared are Text or Comment nodes
m=!0,f.nodeValue!==s.nodeValue&&(f.nodeValue=s.nodeValue))),m){// Advance both the "to" child and the "from" child since we found a match
// Nothing else to do as we already recursively called morphChildren above
s=d,f=i;continue e}l?// the actual removal to later
B(l)://       still a chance they will be matched up later
_(f,t,!0),f=i}// END: while(curFromNodeChild) {}
// If we got this far then we did not find a candidate match for
// our "to node" and we exhausted all of the children "from"
// nodes. Therefore, we will just append the current "to" node
// to the end
if(o&&(c=L[o])&&a(c,s))t.appendChild(c),// MORPH
e(c,s);else{var h=T(s);!1!==h&&(h&&(s=h),s.actualize&&(s=s.actualize(t.ownerDocument||r)),t.appendChild(s),function t(n){S(n);for(var o=n.firstChild;o;){var r=o.nextSibling,l=N(o);if(l){var i=L[l];// if we find a duplicate #id node in cache, replace `el` with cache value
// and morph it to the child node.
i&&a(o,i)?(o.parentNode.replaceChild(i,o),e(i,o)):t(o)}else // fromNodesLookup
t(o);o=r}}(s))}s=d,f=i}!function(e,t,n){// We have processed all of the "to nodes". If curFromNodeChild is
// non-null then we still have some from nodes left over that need
// to be removed
for(;t;){var o=t.nextSibling;(n=N(t))?// the actual removal to later
B(n)://       still a chance they will be matched up later
_(t,e,!0),t=o}}(t,f,l);var g=u[t.nodeName];g&&g(t,n)}// END: morphChildren(...)
(n,o):u.TEXTAREA(n,o))}(U,o,k),R)for(var P=0,D=R.length;P<D;P++){var M=L[R[P]];M&&_(M,M.parentNode,!1)}}return!k&&U!==e&&e.parentNode&&(U.actualize&&(U=U.actualize(e.ownerDocument||r)),// If we had to swap out the from node with a new node because the old
// node was not compatible with the target node then we need to
// replace the old DOM node in the original DOM tree. This is only
// possible if the original DOM node was part of a DOM tree which
// we know is the case if it has a parent node.
e.parentNode.replaceChild(U,e)),U}),p={};function m(){}function h(e,t){var n,o=0,r=1,l={},i=(t=t||{}).maxAttempts||1/0;return l.open=function(){(n=new WebSocket(e,t.protocols||[])).onmessage=t.onmessage||m,n.onopen=function(e){(t.onopen||m)(e),o=0},n.onclose=function(e){1e3===e.code||1001===e.code||1005===e.code||l.reconnect(e),(t.onclose||m)(e)},n.onerror=function(e){e&&"ECONNREFUSED"===e.code?l.reconnect(e):(t.onerror||m)(e)}},l.reconnect=function(e){r&&o++<i?r=setTimeout(function(){(t.onreconnect||m)(e),l.open()},t.timeout||1e3):(t.onmaximum||m)(e)},l.json=function(e){n.send(JSON.stringify(e))},l.send=function(e){n.send(e)},l.close=function(e,t){r=clearTimeout(r),n.close(e||1e3,t)},l.open(),l}e(p,"WEBSOCKETS",()=>g),e(p,"open",()=>y),e(p,"close",()=>E);let g={},v=function(e,t,n,o){console.log("Websocket "+t+" to url",n,"with options",o,"and event",e)},y=function(e,t){if(t||(t={}),g[e]){v(null,"ALREADY_OPENED_BYE",e,t);return}g[e]=new h(e,Object.assign({timeout:1e3,maxAttempts:Number.MAX_SAFE_INTEGER,onopen:n=>v(n,"OPENED",e,t),onmessage:e=>{hypergen.applyCommands(JSON.parse(e.data))},onreconnect:n=>v(n,"RECONNECTING",e,t),onmaximum:n=>v(n,"MAX_RECONNECTS_BYE",e,t),onclose:n=>{v(n,"CLOSED",e,t)},onerror:e=>console.log("Error:",e)},t))},E=function(e){if(!g[e]){v(null,"ALREADY_CLOSED_BYE",e,null);return}g[e].close(),delete g[e],v(null,"CLOSED_AND_DELETED",e,null)};// Make all exported vars availabe inside window.hypergen.
window.hypergen=o,window.hypergen.websocket=p,void 0===Array.isArray&&(Array.isArray=function(e){return"[object Array]"===Object.prototype.toString.call(e)});let b=function(e,t){let n=document.getElementById(e);if(!n){console.error("Trying to morph into an element with id='"+e+"' that does not exist. Please check your target_id.");return}f(n,"<div>"+t+"</div>",{childrenOnly:!0,onBeforeElUpdated:function(e,t){let n=document.activeElement;if(("INPUT"==e.nodeName||"TEXTAREA"==e.nodeName)&&e===n)return"INPUT"===e.nodeName&&-1!==["checkbox","radio"].indexOf(e.type)||(z(e,t),!1);if("INPUT"==e.nodeName&&"file"===e.type&&e.files.length>0)return z(e,t),!1;if("SCRIPT"!==e.nodeName||"SCRIPT"!==t.nodeName)return!0;var o=document.createElement("script");return(//copy over the attributes
[...t.attributes].forEach(e=>{o.setAttribute(e.nodeName,e.nodeValue)}),o.innerHTML=t.innerHTML,e.replaceWith(o),!1)},onNodeAdded:function(e){if("SCRIPT"===e.nodeName){var t=document.createElement("script");//copy over the attributes
[...e.attributes].forEach(e=>{t.setAttribute(e.nodeName,e.nodeValue)}),t.innerHTML=e.innerHTML,e.replaceWith(t)}}});let o=document.querySelectorAll("[autofocus]")[0];void 0!==o&&o.focus()},N=function(e){let t=document.getElementById(e);t.parentNode.removeChild(t)},T=function(e){document.getElementById(e).style.display="none"},S=function(e,t){document.getElementById(e).style.display=t||"block"},C=function(e,t){document.getElementById(e).style.visibility="visible"},w=function(e,t){document.getElementById(e).style.visibility="hidden"},A=function(e){window.location=e},I=function(e,t){let n=document.getElementById(e);n||console.error("Cannot append to missing element",e),n.innerHTML+=t},O=function(e,t){let n=document.getElementById(e);n||console.error("Cannot prepend to missing element",e),n.innerHTML=t+n.innerHTML};o.clientState={};let k=function(e,t){let n=o.clientState;for(let t of e.split("."))void 0===n[t]&&(n[t]={}),n=n[t];Object.assign(n,t),console.log("Setting new state for hypergen.clientState",e,"with value",t,"giving",o.clientState)};/* WARNING NOT STABLE */var L={};let R=function(e,t,n){let o=setInterval(()=>K(e),t);n&&(L[n]=o)},B=function(e){L[e]&&(console.log("Clearing",L[e]),clearInterval(L[e]))},_=function(e,t,n,o){document.querySelector(e).addEventListener(t,e=>K(n),o||{})},U={},x=function(e){let[t,n,o]=U;F(t,[e.key,...n||[]],o||{})},H=function(e,t,n){U=[e,t,n],window.addEventListener("keydown",x)},P=function(e,t,n){window.removeEventListener("keydown",x)};/* END WARNING STABLE AGAIN */// Callback
var D=0,M=!1;let F=function(e,t,{debounce:n=0,confirm_:r=!1,blocks:l=!1,uploadFiles:i=!1,params:a={},meta:d={},clear:u=!1,elementId:c=null,debug:s=!1,event:f=null,headers:p={},onSucces:m=null}={}){f&&(f.preventDefault(),f.stopPropagation());let h=e.startsWith("ws://")||e.startsWith("wss://")?function(){let r;console.log("WEBSOCKET",e,t,n);try{r=JSON.stringify({args:t,meta:d})}catch(t){if(t===$){console.warn("An element is missing. This can happen if a dom element has multiple event handlers.",e);return}throw t}if(!o.websocket.WEBSOCKETS[e]){console.error("Cannot send WS to non existing connection:",e);return}o.websocket.WEBSOCKETS[e].send(r),!0===u&&(document.getElementById(c).value="")}:function(){let r;console.log("REQUEST",e,t,n),D++,// The element function must have access to the FormData.
o.hypergenGlobalFormdata=new FormData,o.hypergenUploadFiles=i;try{r=JSON.stringify({args:t,meta:d})}catch(t){if(t===$){console.warn("An element is missing. This can happen if a dom element has multiple event handlers.",e);return}throw t}let f=o.hypergenGlobalFormdata;if(o.hypergenGlobalFormdata=null,o.hypergenUploadFiles=null,f.append("hypergen_data",r),!0===l){if(!0===M){console.error("Callback was blocked");return}M=!0}er(e,f,e=>{null!==e&&K(e),M=!1,!0===u&&(document.getElementById(c).value=""),m&&m()},(e,t,n)=>{console.log(n),M=!1,console.error("Hypergen post error occured",e),!0!==s&&("text/plain"===n.getResponseHeader("Content-Type")&&(e="<pre><code>"+e+"</pre></code>"),document.getElementsByTagName("html")[0].innerHTML=e)},a,p)};0===n?!1===r?h():confirm(r)&&h():q(h,{delay:n,group:e,confirm_:r})},W=function(e,t,n){console.log("partialLoad to",t,n),window.dispatchEvent(new CustomEvent("hypergen.partialLoad.before",{detail:{event:e,url:t,pushState:n}})),F(t,[],{event:e,headers:{"X-Hypergen-Partial":"1"},onSucces:function(){n&&(console.log("pushing state!"),history.pushState({callback_url:t},"",t),ei(),history.forward(),window.dispatchEvent(new CustomEvent("hypergen.partialLoad.after",{detail:{event:e,url:t,pushState:n}})))}})};// Timing
var X={};let q=function(e,{delay:t=0,group:n="global",confirm_:o=!1}={}){X[n]&&(clearTimeout(X[n]),X[n]=null),X[n]=setTimeout(function(){if(!1===o)e();else{let t=confirm(o);!0===t&&e()}X[n]=null},t)},V=function(e){X[e]&&(clearTimeout(X[e]),X[e]=null)},G=function(e){try{return require(e)}catch(e){return!1}},j=function(e){let t=e.split("."),n=-1,o=null;for(let r of t)if(0==++n){if(void 0!==window[r])o=window[r];else if(o=G(r));else if(o=G("./"+r));else throw"Could not resolve path: "+e}else if(void 0!==o[r])try{o=o[r].bind(o)}catch(e){o=o[r]}else throw"Could not resolve path: "+e;return o},J=function(e,...t){console.log("apply command",e,t);let n=j(e),o=n(...t),r=new CustomEvent("hypergen.applyCommand.after",{detail:{path:e,args:t}});return document.dispatchEvent(r),o},Y=function(e,t,n){e.preventDefault(),e.stopPropagation(),(!n||J(...n,e))&&J(...o.clientState.hypergen.eventHandlerCallbacks[t])},K=function(e){for(let[t,...n]of(e._&&2===e._.length&&"deque"===e._[0]&&(e=e._[1]),e))J(t,...n)},z=function(e,t){t.getAttributeNames().forEach(n=>{let o=t.getAttribute(n);e.setAttribute(n,o)})},$="MISSING_ELEMENT_EXCEPTION",Q={};Q.no=function(e){return""===e?null:e},Q.str=function(e){return""===e?null:null===e?null:""+e},Q.int=function(e){return""===e?null:isNaN(e=parseInt(e))?null:e},Q.float=function(e){return""===e?null:isNaN(e=parseFloat(e))?null:{_:["float",e]}},Q.date=function(e){return""===e?null:{_:["date",e]}},Q.datetime=function(e){return""===e?null:{_:["datetime",e]}},Q.time=function(e){return""===e?null:{_:["time",e]}},Q.month=function(e){if(""===e)return null;let t=e.split("-");return{year:parseInt(t[0]),month:parseInt(t[1])}},Q.week=function(e){if(""===e)return null;let t=e.split("-");return{year:parseInt(t[0]),week:parseInt(t[1].replace("W",""))}};let Z={};Z.value=function(e){let t=document.getElementById(e);if(null===t)throw $;return t.value.trim()},Z.checked=function(e){let t=document.getElementById(e);if(null===t)throw $;return t.checked},Z.radio=function(e){let t=document.getElementById(e);if(null===t)throw $;let n=document.querySelector("input[type=radio][name="+t.name+"]:checked");return null===n?null:n.value},Z.file=function(e,t){let n=document.getElementById(e);if(null===n)throw $;return 1!==n.files.length?null:(!0===o.hypergenUploadFiles&&t.append(e,n.files[0]),n.files[0].name)},Z.contenteditable=function(e,t){let n=document.getElementById(e);if(null===n)throw $;return n.innerHTML};let ee={};ee.keycode=function(e,t){return t.code==e};let et=function(e,t,n){return this.toJSON=function(){let r=j(e)(n,o.hypergenGlobalFormdata);return t?j(t)(r):Q.no(r)},this},en=function(e,t){return Array.isArray(t)&&3===t.length&&"_"===t[0]&&"element_value"===t[1]?new et(...t[2]):t},eo=function(e){let t=null;if(document.cookie&&""!==document.cookie){let n=document.cookie.split(";");for(let o=0;o<n.length;o++){let r=n[o].trim();// Does this cookie string begin with the name we want?
if(r.substring(0,e.length+1)===e+"="){t=decodeURIComponent(r.substring(e.length+1));break}}}return t},er=function(e,t,n,o,r,l){e=function(e,t){let n=[];for(let e in t)n.push(encodeURIComponent(e)+"="+encodeURIComponent(t[e]));return 0===n.length?e:e+"?"+n.join("&")}(e,r);let i=new XMLHttpRequest,a=document.getElementById("hypergen-upload-progress-bar");if(null!==a&&(i.upload.onload=()=>{a.style.visibility="hidden",console.log(`The upload is completed: ${i.status} ${i.response}`)},i.upload.onerror=()=>{a.style.visibility="hidden",console.error("Upload failed.")},i.upload.onabort=()=>{a.style.visibility="hidden",console.error("Upload cancelled.")},i.upload.onprogress=e=>{a.style.visibility="visible",a.value=e.loaded/e.total,console.log(`Uploaded ${e.loaded} of ${e.total} bytes`)}),i.onload=()=>{var e=!1,t=null;try{t=JSON.parse(i.responseText,en),e=!0}catch(n){t=i.responseText,e=!1}4==i.readyState&&(200==i.status||302==i.status)?n(t,i):o(t,e,i)},i.onerror=()=>{o()},i.onabort=()=>{console.error("xhr aborted")},i.open("POST",e),i.setRequestHeader("X-Requested-With","XMLHttpRequest"),i.setRequestHeader("X-Pathname",parent.window.location.pathname),i.setRequestHeader("X-CSRFToken",eo("csrftoken")),l)for(let e in l)console.log("Setting custom header",e,"to",l[e]),i.setRequestHeader(e,l[e]);i.send(t)};// history support.
window.addEventListener("popstate",function(e){e.state&&void 0!==e.state.callback_url?(console.log("popstate to partial load"),W(e,e.state.callback_url)):window.location=location.href});let el=new Event("hypergen.pushstate"),ei=function(){document.dispatchEvent(el)},ea=function(e,{partial:t=!1}={}){"loading"!=document.readyState?e():document.addEventListener?document.addEventListener("DOMContentLoaded",e):document.attachEvent("onreadystatechange",function(){"loading"!=document.readyState&&e()}),t&&document.addEventListener("hypergen.pushstate",e)}})();//# sourceMappingURL=hypergen.js.map

//# sourceMappingURL=hypergen.js.map
