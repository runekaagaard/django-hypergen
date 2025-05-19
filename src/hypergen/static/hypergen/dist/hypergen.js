(()=>{function e(e,t,n,o){Object.defineProperty(e,t,{get:n,set:o,enumerable:!0,configurable:!0})}var t,n,o={};e(o,"morph",()=>b),e(o,"remove",()=>w),e(o,"hide",()=>N),e(o,"display",()=>C),e(o,"visible",()=>T),e(o,"hidden",()=>S),e(o,"redirect",()=>A),e(o,"append",()=>I),e(o,"prepend",()=>k),e(o,"setClientState",()=>O),e(o,"intervalSet",()=>R),e(o,"applyCommands",()=>z),e(o,"intervalClear",()=>B),e(o,"addEventListener",()=>x),e(o,"callback",()=>W),e(o,"keypressToCallback",()=>H),e(o,"keypressToCallbackRemove",()=>P),e(o,"throttle",()=>V),e(o,"partialLoad",()=>X),e(o,"onpushstate",()=>ea),e(o,"cancelThrottle",()=>G),e(o,"event",()=>K),e(o,"coerce",()=>Z),e(o,"read",()=>ee),e(o,"when",()=>et),e(o,"element",()=>en),e(o,"reviver",()=>eo),e(o,"ready",()=>ed);var r="undefined"==typeof document?void 0:document,l=!!r&&"content"in r.createElement("template"),i=!!r&&r.createRange&&"createContextualFragment"in r.createRange();/**
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
for(var a=i.length-1;a>=0;a--)o=(n=i[a]).name,r=n.namespaceURI,l=n.value,r?(o=n.localName||o,e.getAttributeNS(r,o)!==l&&("xmlns"===n.prefix&&(o=n.name),e.setAttributeNS(r,o,l))):e.getAttribute(o)!==l&&e.setAttribute(o,l);for(var d=e.attributes,u=d.length-1;u>=0;u--)o=(n=d[u]).name,(r=n.namespaceURI)?(o=n.localName||o,t.hasAttributeNS(r,o)||e.removeAttributeNS(r,o)):t.hasAttribute(o)||e.removeAttribute(o)}},function(e,o,d){if(d||(d={}),"string"==typeof o){if("#document"===e.nodeName||"HTML"===e.nodeName||"BODY"===e.nodeName){var f,p,m,h,v,g,y,E,b=o;(o=r.createElement("html")).innerHTML=b}else f=(f=o).trim(),o=l?(p=f,(m=r.createElement("template")).innerHTML=p,m.content.childNodes[0]):i?(h=f,n||(n=r.createRange()).selectNode(r.body),n.createContextualFragment(h).childNodes[0]):(v=f,(g=r.createElement("body")).innerHTML=v,g.childNodes[0])}var w=d.getNodeKey||s,N=d.onBeforeNodeAdded||c,C=d.onNodeAdded||c,T=d.onBeforeElUpdated||c,S=d.onElUpdated||c,A=d.onBeforeNodeDiscarded||c,I=d.onNodeDiscarded||c,k=d.onBeforeElChildrenUpdated||c,O=!0===d.childrenOnly,L=Object.create(null),R=[];function B(e){R.push(e)}/**
         * Removes a DOM node out of the original DOM
         *
         * @param  {Node} node The node to remove
         * @param  {Node} parentNode The nodes parent
         * @param  {Boolean} skipKeyedNodes If true then elements with keys will be skipped and not discarded.
         * @return {undefined}
         */function x(e,t,n){!1!==A(e)&&(t&&t.removeChild(e),I(e),function e(t,n){if(1===t.nodeType)for(var o=t.firstChild;o;){var r=void 0;n&&(r=w(o))?// to a list so that it can be handled at the very end.
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
function e(t){if(1===t.nodeType||11===t.nodeType)for(var n=t.firstChild;n;){var o=w(n);o&&(L[o]=n),// Walk recursively
e(n),n=n.nextSibling}}(e);var U=e,_=U.nodeType,H=o.nodeType;if(!O){// Handle the case where we are given two DOM nodes that are not
// compatible (e.g. <div> --> <span> or <div> --> TEXT)
if(1===_)1===H?a(e,o)||(I(e),U=/**
 * Copies the children of one DOM element to another DOM element
 */function(e,t){for(var n=e.firstChild;n;){var o=n.nextSibling;t.appendChild(n),n=o}return t}(e,(y=o.nodeName,(E=o.namespaceURI)&&"http://www.w3.org/1999/xhtml"!==E?r.createElementNS(E,y):r.createElement(y)))):U=o;else if(3===_||8===_){if(H===_)return U.nodeValue!==o.nodeValue&&(U.nodeValue=o.nodeValue),U;U=o}}if(U===o)// toss out the "from node" and use the "to node"
I(e);else{if(o.isSameNode&&o.isSameNode(U))return;// We now need to loop over any keyed nodes that might need to be
// removed. We only do the removal if we know that the keyed node
// never found a match. When a keyed node is matched up we remove
// it out of fromNodesLookup and we use fromNodesLookup to determine
// if a keyed node has been matched up or not
if(function e(n,o,l){var i=w(o);i&&// DOM so clear it out of the saved elements collection
delete L[i],(l||!1!==T(n,o)&&(// update attributes on original DOM element first
t(n,o),// optional
S(n),!1!==k(n,o)))&&("TEXTAREA"!==n.nodeName?function(t,n){var o,l,i,d,c,s=n.firstChild,f=t.firstChild;// walk the children
e:for(;s;){// walk the fromNode children all the way through
for(d=s.nextSibling,o=w(s);f;){if(i=f.nextSibling,s.isSameNode&&s.isSameNode(f)){s=d,f=i;continue e}l=w(f);var p=f.nodeType,m=void 0;if(p===s.nodeType&&(1===p?(o?o!==l&&((c=L[o])?i===c?// DOM node out of the tree (since that can break CSS transitions, etc.),
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
x(f,t,!0),f=c):// is no matching keyed node in the source tree
m=!1):l&&(m=!1),(m=!1!==m&&a(f,s))&&// the current "from" node to match the current
// target DOM node.
// MORPH
e(f,s)):(3===p||8==p)&&(// Both nodes being compared are Text or Comment nodes
m=!0,f.nodeValue!==s.nodeValue&&(f.nodeValue=s.nodeValue))),m){// Advance both the "to" child and the "from" child since we found a match
// Nothing else to do as we already recursively called morphChildren above
s=d,f=i;continue e}l?// the actual removal to later
B(l)://       still a chance they will be matched up later
x(f,t,!0),f=i}// END: while(curFromNodeChild) {}
// If we got this far then we did not find a candidate match for
// our "to node" and we exhausted all of the children "from"
// nodes. Therefore, we will just append the current "to" node
// to the end
if(o&&(c=L[o])&&a(c,s))t.appendChild(c),// MORPH
e(c,s);else{var h=N(s);!1!==h&&(h&&(s=h),s.actualize&&(s=s.actualize(t.ownerDocument||r)),t.appendChild(s),function t(n){C(n);for(var o=n.firstChild;o;){var r=o.nextSibling,l=w(o);if(l){var i=L[l];// if we find a duplicate #id node in cache, replace `el` with cache value
// and morph it to the child node.
i&&a(o,i)?(o.parentNode.replaceChild(i,o),e(i,o)):t(o)}else // fromNodesLookup
t(o);o=r}}(s))}s=d,f=i}!function(e,t,n){// We have processed all of the "to nodes". If curFromNodeChild is
// non-null then we still have some from nodes left over that need
// to be removed
for(;t;){var o=t.nextSibling;(n=w(t))?// the actual removal to later
B(n)://       still a chance they will be matched up later
x(t,e,!0),t=o}}(t,f,l);var v=u[t.nodeName];v&&v(t,n)}// END: morphChildren(...)
(n,o):u.TEXTAREA(n,o))}(U,o,O),R)for(var P=0,M=R.length;P<M;P++){var D=L[R[P]];D&&x(D,D.parentNode,!1)}}return!O&&U!==e&&e.parentNode&&(U.actualize&&(U=U.actualize(e.ownerDocument||r)),// If we had to swap out the from node with a new node because the old
// node was not compatible with the target node then we need to
// replace the old DOM node in the original DOM tree. This is only
// possible if the original DOM node was part of a DOM tree which
// we know is the case if it has a parent node.
e.parentNode.replaceChild(U,e)),U}),p={};function m(){}function h(e,t){var n,o=0,r=1,l={},i=(t=t||{}).maxAttempts||1/0;return l.open=function(){(n=new WebSocket(e,t.protocols||[])).onmessage=t.onmessage||m,n.onopen=function(e){(t.onopen||m)(e),o=0},n.onclose=function(e){1e3===e.code||1001===e.code||1005===e.code||l.reconnect(e),(t.onclose||m)(e)},n.onerror=function(e){e&&"ECONNREFUSED"===e.code?l.reconnect(e):(t.onerror||m)(e)}},l.reconnect=function(e){r&&o++<i?r=setTimeout(function(){(t.onreconnect||m)(e),l.open()},t.timeout||1e3):(t.onmaximum||m)(e)},l.json=function(e){n.send(JSON.stringify(e))},l.send=function(e){n.send(e)},l.close=function(e,t){r=clearTimeout(r),n.close(e||1e3,t)},l.open(),l}e(p,"WEBSOCKETS",()=>v),e(p,"open",()=>y),e(p,"close",()=>E);let v={},g=function(e,t,n,o){console.log("Websocket "+t+" to url",n,"with options",o,"and event",e)},y=function(e,t){if(t||(t={}),v[e]){g(null,"ALREADY_OPENED_BYE",e,t);return}v[e]=new h(e,Object.assign({timeout:1e3,maxAttempts:Number.MAX_SAFE_INTEGER,onopen:n=>g(n,"OPENED",e,t),onmessage:e=>{hypergen.applyCommands(JSON.parse(e.data))},onreconnect:n=>g(n,"RECONNECTING",e,t),onmaximum:n=>g(n,"MAX_RECONNECTS_BYE",e,t),onclose:n=>{g(n,"CLOSED",e,t)},onerror:e=>console.log("Error:",e)},t))},E=function(e){if(!v[e]){g(null,"ALREADY_CLOSED_BYE",e,null);return}v[e].close(),delete v[e],g(null,"CLOSED_AND_DELETED",e,null)};// Make all exported vars availabe inside window.hypergen.
window.hypergen=o,window.hypergen.websocket=p,void 0===Array.isArray&&(Array.isArray=function(e){return"[object Array]"===Object.prototype.toString.call(e)});let b=function(e,t){let n=document.getElementById(e);if(!n){console.error("Trying to morph into an element with id='"+e+"' that does not exist. Please check your target_id.");return}f(n,"<div>"+t+"</div>",{childrenOnly:!0,onBeforeElUpdated:function(e,t){let n=document.activeElement;if(("INPUT"==e.nodeName||"TEXTAREA"==e.nodeName)&&e===n)return"INPUT"===e.nodeName&&-1!==["checkbox","radio"].indexOf(e.type)||($(e,t),!1);if("INPUT"==e.nodeName&&"file"===e.type&&e.files.length>0)return $(e,t),!1;if("SCRIPT"!==e.nodeName||"SCRIPT"!==t.nodeName)return!0;var o=document.createElement("script");return(//copy over the attributes
[...t.attributes].forEach(e=>{o.setAttribute(e.nodeName,e.nodeValue)}),o.innerHTML=t.innerHTML,e.replaceWith(o),!1)},onNodeAdded:function(e){if("SCRIPT"===e.nodeName){var t=document.createElement("script");//copy over the attributes
[...e.attributes].forEach(e=>{t.setAttribute(e.nodeName,e.nodeValue)}),t.innerHTML=e.innerHTML,e.replaceWith(t)}}});let o=document.querySelectorAll("[autofocus]")[0];void 0!==o&&o.focus()},w=function(e){let t=document.getElementById(e);t.parentNode.removeChild(t)},N=function(e){document.getElementById(e).style.display="none"},C=function(e,t){document.getElementById(e).style.display=t||"block"},T=function(e,t){document.getElementById(e).style.visibility="visible"},S=function(e,t){document.getElementById(e).style.visibility="hidden"},A=function(e){/*
  One would expect to simply do a window.location = url but that does not work in an ajax request on safari, because
  (i think) the ajax request is async and the redirect is thus triggered directly during a user event.
  This is a workaround, but might stop working some day.
  */let t=document.createElement("a");t.href=e,t.style.display="none",document.body.appendChild(t),t.click(),document.body.removeChild(t)},I=function(e,t){let n=document.getElementById(e);n||console.error("Cannot append to missing element",e),n.innerHTML+=t},k=function(e,t){let n=document.getElementById(e);n||console.error("Cannot prepend to missing element",e),n.innerHTML=t+n.innerHTML};o.clientState={};let O=function(e,t){let n=o.clientState;for(let t of e.split("."))void 0===n[t]&&(n[t]={}),n=n[t];Object.assign(n,t),console.log("Setting new state for hypergen.clientState",e,"with value",t,"giving",o.clientState)};/* WARNING NOT STABLE */var L={};let R=function(e,t,n){let o=setInterval(()=>z(e),t);n&&(L[n]=o)},B=function(e){L[e]&&(console.log("Clearing",L[e]),clearInterval(L[e]))},x=function(e,t,n,o){document.querySelector(e).addEventListener(t,e=>z(n),o||{})},U={},_=function(e){let[t,n,o]=U;W(t,[e.key,...n||[]],o||{})},H=function(e,t,n){U=[e,t,n],window.addEventListener("keydown",_)},P=function(e,t,n){window.removeEventListener("keydown",_)};/* END WARNING STABLE AGAIN */// Callback
var M=0,D=!1,F={};let W=function(e,t,{debounce:n=0,confirm_:r=!1,blocks:l=!1,blocksEachUrl:i=!0,uploadFiles:a=!1,params:d={},meta:u={},clear:c=!1,elementId:s=null,debug:f=!1,event:p=null,headers:m={},onSucces:h=null,timeout:v=2e4}={}){let g=e.startsWith("ws://")||e.startsWith("wss://");p&&(p.preventDefault(),p.stopPropagation());let y=g?function(){let r;console.log("WEBSOCKET",e,t,n);try{r=JSON.stringify({args:t,meta:u})}catch(t){if(t===Q){console.warn("An element is missing. This can happen if a dom element has multiple event handlers.",e);return}throw t}if(!o.websocket.WEBSOCKETS[e]){console.error("Cannot send WS to non existing connection:",e);return}o.websocket.WEBSOCKETS[e].send(r),!0===c&&(document.getElementById(s).value="")}:function(){let r;console.log("REQUEST",e,t,n),M++,// The element function must have access to the FormData.
o.hypergenGlobalFormdata=new FormData,o.hypergenUploadFiles=a;try{r=JSON.stringify({args:t,meta:u})}catch(t){if(t===Q){console.warn("An element is missing. This can happen if a dom element has multiple event handlers.",e);return}throw t}let p=o.hypergenGlobalFormdata;if(o.hypergenGlobalFormdata=null,o.hypergenUploadFiles=null,p.append("hypergen_data",r),!0===l){if(!0===D){console.error("Callback was blocked");return}D=!0}if(!0===i&&!g){if(F[e]){console.error("Callback to "+e+" was blocked");return}F[e]=!0}el(e,p,t=>{null!==t&&z(t),D=!1,!0!==i||g||delete F[e],!0===c&&(document.getElementById(s).value=""),h&&h()},(t,n,o)=>{console.log("xhr:",o),D=!1,!0!==i||g||delete F[e],console.error("Hypergen post error occured",t),!0!==f&&("text/plain"===o.getResponseHeader("Content-Type")&&(t="<pre><code>"+t+"</pre></code>"),document.getElementsByTagName("html")[0].innerHTML=t)},d,m,{timeout:v})};0===n?!1===r?y():confirm(r)&&y():V(y,{delay:n,group:e,confirm_:r})},X=function(e,t,n){console.log("partialLoad to",t,n),window.dispatchEvent(new CustomEvent("hypergen.partialLoad.before",{detail:{event:e,url:t,pushState:n}})),W(t,[],{event:e,headers:{"X-Hypergen-Partial":"1"},onSucces:function(){n&&(console.log("pushing state!"),history.pushState({callback_url:t},"",t),ea(),history.forward(),window.dispatchEvent(new CustomEvent("hypergen.partialLoad.after",{detail:{event:e,url:t,pushState:n}})))}})};// Timing
var q={};let V=function(e,{delay:t=0,group:n="global",confirm_:o=!1}={}){q[n]&&(clearTimeout(q[n]),q[n]=null),q[n]=setTimeout(function(){if(!1===o)e();else{let t=confirm(o);!0===t&&e()}q[n]=null},t)},G=function(e){q[e]&&(clearTimeout(q[e]),q[e]=null)},j=function(e){try{return require(e)}catch(e){return!1}},J=function(e){let t=e.split("."),n=-1,o=null;for(let r of t)if(0==++n){if(void 0!==window[r])o=window[r];else if(o=j(r));else if(o=j("./"+r));else throw"Could not resolve path: "+e}else if(void 0!==o[r])try{o=o[r].bind(o)}catch(e){o=o[r]}else throw"Could not resolve path: "+e;return o},Y=function(e,...t){console.log("apply command",e,t);let n=J(e),o=n(...t),r=new CustomEvent("hypergen.applyCommand.after",{detail:{path:e,args:t}});return document.dispatchEvent(r),o},K=function(e,t,n){e.preventDefault(),e.stopPropagation(),(!n||Y(...n,e))&&Y(...o.clientState.hypergen.eventHandlerCallbacks[t])},z=function(e){for(let[t,...n]of(e._&&2===e._.length&&"deque"===e._[0]&&(e=e._[1]),e))Y(t,...n)},$=function(e,t){t.getAttributeNames().forEach(n=>{let o=t.getAttribute(n);e.setAttribute(n,o)})},Q="MISSING_ELEMENT_EXCEPTION",Z={};Z.no=function(e){return""===e?null:e},Z.str=function(e){return""===e?null:null===e?null:""+e},Z.int=function(e){return""===e?null:isNaN(e=parseInt(e))?null:e},Z.intlist=function(e){return e.map(e=>parseInt(e))},Z.float=function(e){return""===e?null:isNaN(e=parseFloat(e))?null:{_:["float",e]}},Z.date=function(e){return""===e?null:{_:["date",e]}},Z.datetime=function(e){return""===e?null:{_:["datetime",e]}},Z.time=function(e){return""===e?null:{_:["time",e]}},Z.month=function(e){if(""===e)return null;let t=e.split("-");return{year:parseInt(t[0]),month:parseInt(t[1])}},Z.week=function(e){if(""===e)return null;let t=e.split("-");return{year:parseInt(t[0]),week:parseInt(t[1].replace("W",""))}};let ee={};ee.value=function(e){let t=document.getElementById(e);if(null===t)throw Q;return t.value.trim()},ee.checked=function(e){let t=document.getElementById(e);if(null===t)throw Q;return t.checked},ee.radio=function(e){let t=document.getElementById(e);if(null===t)throw Q;let n=document.querySelector("input[type=radio][name="+t.name+"]:checked");return null===n?null:n.value},ee.contenteditable=function(e){let t=document.getElementById(e);if(null===t)throw Q;return t.innerHTML},ee.selectMultiple=function(e){let t=document.getElementById(e);if(null===t)throw Q;return Array.from(t.selectedOptions).map(e=>e.value)},ee.file=function(e,t){let n=document.getElementById(e);if(null===n)throw Q;return 1!==n.files.length?null:(!0===o.hypergenUploadFiles&&t.append(e,n.files[0]),n.files[0].name)};let et={};et.keycode=function(e,t){return t.code==e};let en=function(e,t,n){return this.toJSON=function(){let r=J(e)(n,o.hypergenGlobalFormdata);return t?J(t)(r):Z.no(r)},this},eo=function(e,t){return Array.isArray(t)&&3===t.length&&"_"===t[0]&&"element_value"===t[1]?new en(...t[2]):t},er=function(e){let t=null;if(document.cookie&&""!==document.cookie){let n=document.cookie.split(";");for(let o=0;o<n.length;o++){let r=n[o].trim();// Does this cookie string begin with the name we want?
if(r.substring(0,e.length+1)===e+"="){t=decodeURIComponent(r.substring(e.length+1));break}}}return t},el=function(e,t,n,o,r,l,{timeout:i=2e4}={}){e=function(e,t){let n=[];for(let e in t)n.push(encodeURIComponent(e)+"="+encodeURIComponent(t[e]));return 0===n.length?e:e+"?"+n.join("&")}(e,r);let a=new XMLHttpRequest;a.timeout=i;let d=document.getElementById("hypergen-upload-progress-bar");if(null!==d&&(a.upload.onload=()=>{d.style.visibility="hidden",console.log(`The upload is completed: ${a.status} ${a.response}`)},a.upload.onerror=()=>{d.style.visibility="hidden",console.error("Upload failed.")},a.upload.onabort=()=>{d.style.visibility="hidden",console.error("Upload cancelled.")},a.upload.onprogress=e=>{d.style.visibility="visible",d.value=e.loaded/e.total,console.log(`Uploaded ${e.loaded} of ${e.total} bytes`)}),a.onload=()=>{var e=!1,t=null;try{t=JSON.parse(a.responseText,eo),e=!0}catch(n){t=a.responseText,e=!1}4==a.readyState&&(200==a.status||302==a.status)?(window.dispatchEvent(new CustomEvent("hypergen.post.after")),n(t,a)):(window.dispatchEvent(new CustomEvent("hypergen.post.after")),o(t,e,a))},a.onerror=()=>{console.error("xhr onerror"),window.dispatchEvent(new CustomEvent("hypergen.post.after")),o()},a.onabort=()=>{console.error("xhr onabort"),window.dispatchEvent(new CustomEvent("hypergen.post.after")),o()},a.ontimeout=()=>{console.error("xhr ontimeout"),window.dispatchEvent(new CustomEvent("hypergen.post.after")),o()},a.open("POST",e),a.setRequestHeader("X-Requested-With","XMLHttpRequest"),a.setRequestHeader("X-Pathname",parent.window.location.pathname),a.setRequestHeader("X-CSRFToken",er("csrftoken")),l)for(let e in l)console.log("Setting custom header",e,"to",l[e]),a.setRequestHeader(e,l[e]);window.dispatchEvent(new CustomEvent("hypergen.post.before")),a.send(t)};// history support.
window.addEventListener("popstate",function(e){e.state&&void 0!==e.state.callback_url?(console.log("popstate to partial load"),X(e,e.state.callback_url)):window.location=location.href});let ei=new Event("hypergen.pushstate"),ea=function(){document.dispatchEvent(ei)},ed=function(e,{partial:t=!1}={}){"loading"!=document.readyState?e():document.addEventListener?document.addEventListener("DOMContentLoaded",e):document.attachEvent("onreadystatechange",function(){"loading"!=document.readyState&&e()}),t&&document.addEventListener("hypergen.pushstate",e)}})();//# sourceMappingURL=hypergen.js.map

//# sourceMappingURL=hypergen.js.map
