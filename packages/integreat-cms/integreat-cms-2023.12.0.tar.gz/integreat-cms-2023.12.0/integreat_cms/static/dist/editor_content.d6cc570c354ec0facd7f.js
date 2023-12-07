/*! For license information please see editor_content.d6cc570c354ec0facd7f.js.LICENSE.txt */
!function(){var t={38571:function(t,e){"use strict";Object.defineProperty(e,"__esModule",{value:!0}),e.getCookie=void 0;e.getCookie=function(t){for(var e="".concat(t,"="),n=decodeURIComponent(document.cookie).split(";"),r=0;r<n.length;r++){for(var o=n[r];" "===o.charAt(0);)o=o.substring(1);if(0===o.indexOf(e))return o.substring(e.length,o.length)}return""}},28035:function(t,e,n){"use strict";e.getCsrfToken=void 0;var r=n(38571);e.getCsrfToken=function(){return(0,r.getCookie)("csrftoken")}},82026:function(){var t,e,n,r,o,i,a;t=tinymce.util.Tools.resolve("tinymce.PluginManager"),e=tinymce.util.Tools.resolve("tinymce.Env"),n=function(t,e){var n=e<0?0:e;if(3===t.nodeType){var r=t.data.length;n>r&&(n=r)}return n},r=function(t,e,r){1!==e.nodeType||e.hasChildNodes()?t.setStart(e,n(e,r)):t.setStartBefore(e)},o=function(t,e,r){1!==e.nodeType||e.hasChildNodes()?t.setEnd(e,n(e,r)):t.setEndAfter(e)},i=function(t,e,n){var i,a,u,c,l,f,s,d=function(t){return t.getParam("autolink_pattern",/^(https?:\/\/|ssh:\/\/|ftp:\/\/|file:\/|www\.|(?:mailto:)?[A-Z0-9._%+-]+@(?!.*@))(.+)$/i)}(t),h=function(t){return t.getParam("default_link_target",!1)}(t);if("A"!==t.selection.getNode().tagName){var p=t.selection.getRng().cloneRange();if(p.startOffset<5){if(!(l=p.endContainer.previousSibling)){if(!p.endContainer.firstChild||!p.endContainer.firstChild.nextSibling)return;l=p.endContainer.firstChild.nextSibling}if(f=l.length,r(p,l,f),o(p,l,f),p.endOffset<5)return;i=p.endOffset,a=l}else{if(3!==(a=p.endContainer).nodeType&&a.firstChild){for(;3!==a.nodeType&&a.firstChild;)a=a.firstChild;3===a.nodeType&&(r(p,a,0),o(p,a,a.nodeValue.length))}i=1===p.endOffset?2:p.endOffset-1-e}var y=i;do{r(p,a,i>=2?i-2:0),o(p,a,i>=1?i-1:0),i-=1,s=p.toString()}while(" "!==s&&""!==s&&160!==s.charCodeAt(0)&&i-2>=0&&s!==n);!function(t,e){return t===e||" "===t||160===t.charCodeAt(0)}(p.toString(),n)?0===p.startOffset?(r(p,a,0),o(p,a,y)):(r(p,a,i),o(p,a,y)):(r(p,a,i),o(p,a,y),i+=1),"."===(c=p.toString()).charAt(c.length-1)&&o(p,a,y-1);var m=(c=p.toString().trim()).match(d),g=c.match("(0[0-9/]{6,20})"),v=function(t){return t.getParam("link_default_protocol","http","string")}(t);m?("www."===m[1]?m[1]="".concat(v,"://www."):/@$/.test(m[1])&&!/^mailto:/.test(m[1])&&(m[1]="mailto:".concat(m[1])),u=t.selection.getBookmark(),t.selection.setRng(p),t.execCommand("createlink",!1,m[1]+m[2]),!1!==h&&t.dom.setAttrib(t.selection.getNode(),"target",h),t.selection.moveToBookmark(u),t.nodeChanged()):g&&(g[1]="tel:".concat(g[1]),u=t.selection.getBookmark(),t.selection.setRng(p),t.execCommand("createlink",!1,g[1]),!1!==h&&t.dom.setAttrib(t.selection.getNode(),"target",h),t.selection.moveToBookmark(u),t.nodeChanged())}},a=function(t){var n;return t.on("keydown",(function(e){if(13===e.keyCode)return function(t){i(t,-1,"")}(t)})),e.browser.isIE()?(t.on("focus",(function(){if(!n){n=!0;try{t.execCommand("AutoUrlDetect",!1,!0)}catch(t){}}})),""):(t.on("keypress",(function(e){if(41===e.keyCode)return function(t){i(t,-1,"(")}(t)})),t.on("keyup",(function(e){if(32===e.keyCode)return function(t){i(t,0,"")}(t)})),"")},t.add("autolink_tel",(function(t){a(t)}))},70089:function(t,e,n){"use strict";n.r(e);var r,o,i,a,u=n(28035);function c(t){return c="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(t){return typeof t}:function(t){return t&&"function"==typeof Symbol&&t.constructor===Symbol&&t!==Symbol.prototype?"symbol":typeof t},c(t)}function l(t,e){return function(t){if(Array.isArray(t))return t}(t)||function(t,e){var n=null==t?null:"undefined"!=typeof Symbol&&t[Symbol.iterator]||t["@@iterator"];if(null!=n){var r,o,i,a,u=[],c=!0,l=!1;try{if(i=(n=n.call(t)).next,0===e){if(Object(n)!==n)return;c=!1}else for(;!(c=(r=i.call(n)).done)&&(u.push(r.value),u.length!==e);c=!0);}catch(t){l=!0,o=t}finally{try{if(!c&&null!=n.return&&(a=n.return(),Object(a)!==a))return}finally{if(l)throw o}}return u}}(t,e)||f(t,e)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()}function f(t,e){if(t){if("string"==typeof t)return s(t,e);var n=Object.prototype.toString.call(t).slice(8,-1);return"Object"===n&&t.constructor&&(n=t.constructor.name),"Map"===n||"Set"===n?Array.from(t):"Arguments"===n||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)?s(t,e):void 0}}function s(t,e){(null==e||e>t.length)&&(e=t.length);for(var n=0,r=new Array(e);n<e;n++)r[n]=t[n];return r}function d(){d=function(){return e};var t,e={},n=Object.prototype,r=n.hasOwnProperty,o=Object.defineProperty||function(t,e,n){t[e]=n.value},i="function"==typeof Symbol?Symbol:{},a=i.iterator||"@@iterator",u=i.asyncIterator||"@@asyncIterator",l=i.toStringTag||"@@toStringTag";function f(t,e,n){return Object.defineProperty(t,e,{value:n,enumerable:!0,configurable:!0,writable:!0}),t[e]}try{f({},"")}catch(t){f=function(t,e,n){return t[e]=n}}function s(t,e,n,r){var i=e&&e.prototype instanceof b?e:b,a=Object.create(i.prototype),u=new P(r||[]);return o(a,"_invoke",{value:E(t,n,u)}),a}function h(t,e,n){try{return{type:"normal",arg:t.call(e,n)}}catch(t){return{type:"throw",arg:t}}}e.wrap=s;var p="suspendedStart",y="suspendedYield",m="executing",g="completed",v={};function b(){}function x(){}function w(){}var k={};f(k,a,(function(){return this}));var S=Object.getPrototypeOf,O=S&&S(S(N([])));O&&O!==n&&r.call(O,a)&&(k=O);var A=w.prototype=b.prototype=Object.create(k);function C(t){["next","throw","return"].forEach((function(e){f(t,e,(function(t){return this._invoke(e,t)}))}))}function j(t,e){function n(o,i,a,u){var l=h(t[o],t,i);if("throw"!==l.type){var f=l.arg,s=f.value;return s&&"object"==c(s)&&r.call(s,"__await")?e.resolve(s.__await).then((function(t){n("next",t,a,u)}),(function(t){n("throw",t,a,u)})):e.resolve(s).then((function(t){f.value=t,a(f)}),(function(t){return n("throw",t,a,u)}))}u(l.arg)}var i;o(this,"_invoke",{value:function(t,r){function o(){return new e((function(e,o){n(t,r,e,o)}))}return i=i?i.then(o,o):o()}})}function E(e,n,r){var o=p;return function(i,a){if(o===m)throw new Error("Generator is already running");if(o===g){if("throw"===i)throw a;return{value:t,done:!0}}for(r.method=i,r.arg=a;;){var u=r.delegate;if(u){var c=_(u,r);if(c){if(c===v)continue;return c}}if("next"===r.method)r.sent=r._sent=r.arg;else if("throw"===r.method){if(o===p)throw o=g,r.arg;r.dispatchException(r.arg)}else"return"===r.method&&r.abrupt("return",r.arg);o=m;var l=h(e,n,r);if("normal"===l.type){if(o=r.done?g:y,l.arg===v)continue;return{value:l.arg,done:r.done}}"throw"===l.type&&(o=g,r.method="throw",r.arg=l.arg)}}}function _(e,n){var r=n.method,o=e.iterator[r];if(o===t)return n.delegate=null,"throw"===r&&e.iterator.return&&(n.method="return",n.arg=t,_(e,n),"throw"===n.method)||"return"!==r&&(n.method="throw",n.arg=new TypeError("The iterator does not provide a '"+r+"' method")),v;var i=h(o,e.iterator,n.arg);if("throw"===i.type)return n.method="throw",n.arg=i.arg,n.delegate=null,v;var a=i.arg;return a?a.done?(n[e.resultName]=a.value,n.next=e.nextLoc,"return"!==n.method&&(n.method="next",n.arg=t),n.delegate=null,v):a:(n.method="throw",n.arg=new TypeError("iterator result is not an object"),n.delegate=null,v)}function L(t){var e={tryLoc:t[0]};1 in t&&(e.catchLoc=t[1]),2 in t&&(e.finallyLoc=t[2],e.afterLoc=t[3]),this.tryEntries.push(e)}function T(t){var e=t.completion||{};e.type="normal",delete e.arg,t.completion=e}function P(t){this.tryEntries=[{tryLoc:"root"}],t.forEach(L,this),this.reset(!0)}function N(e){if(e||""===e){var n=e[a];if(n)return n.call(e);if("function"==typeof e.next)return e;if(!isNaN(e.length)){var o=-1,i=function n(){for(;++o<e.length;)if(r.call(e,o))return n.value=e[o],n.done=!1,n;return n.value=t,n.done=!0,n};return i.next=i}}throw new TypeError(c(e)+" is not iterable")}return x.prototype=w,o(A,"constructor",{value:w,configurable:!0}),o(w,"constructor",{value:x,configurable:!0}),x.displayName=f(w,l,"GeneratorFunction"),e.isGeneratorFunction=function(t){var e="function"==typeof t&&t.constructor;return!!e&&(e===x||"GeneratorFunction"===(e.displayName||e.name))},e.mark=function(t){return Object.setPrototypeOf?Object.setPrototypeOf(t,w):(t.__proto__=w,f(t,l,"GeneratorFunction")),t.prototype=Object.create(A),t},e.awrap=function(t){return{__await:t}},C(j.prototype),f(j.prototype,u,(function(){return this})),e.AsyncIterator=j,e.async=function(t,n,r,o,i){void 0===i&&(i=Promise);var a=new j(s(t,n,r,o),i);return e.isGeneratorFunction(n)?a:a.next().then((function(t){return t.done?t.value:a.next()}))},C(A),f(A,l,"Generator"),f(A,a,(function(){return this})),f(A,"toString",(function(){return"[object Generator]"})),e.keys=function(t){var e=Object(t),n=[];for(var r in e)n.push(r);return n.reverse(),function t(){for(;n.length;){var r=n.pop();if(r in e)return t.value=r,t.done=!1,t}return t.done=!0,t}},e.values=N,P.prototype={constructor:P,reset:function(e){if(this.prev=0,this.next=0,this.sent=this._sent=t,this.done=!1,this.delegate=null,this.method="next",this.arg=t,this.tryEntries.forEach(T),!e)for(var n in this)"t"===n.charAt(0)&&r.call(this,n)&&!isNaN(+n.slice(1))&&(this[n]=t)},stop:function(){this.done=!0;var t=this.tryEntries[0].completion;if("throw"===t.type)throw t.arg;return this.rval},dispatchException:function(e){if(this.done)throw e;var n=this;function o(r,o){return u.type="throw",u.arg=e,n.next=r,o&&(n.method="next",n.arg=t),!!o}for(var i=this.tryEntries.length-1;i>=0;--i){var a=this.tryEntries[i],u=a.completion;if("root"===a.tryLoc)return o("end");if(a.tryLoc<=this.prev){var c=r.call(a,"catchLoc"),l=r.call(a,"finallyLoc");if(c&&l){if(this.prev<a.catchLoc)return o(a.catchLoc,!0);if(this.prev<a.finallyLoc)return o(a.finallyLoc)}else if(c){if(this.prev<a.catchLoc)return o(a.catchLoc,!0)}else{if(!l)throw new Error("try statement without catch or finally");if(this.prev<a.finallyLoc)return o(a.finallyLoc)}}}},abrupt:function(t,e){for(var n=this.tryEntries.length-1;n>=0;--n){var o=this.tryEntries[n];if(o.tryLoc<=this.prev&&r.call(o,"finallyLoc")&&this.prev<o.finallyLoc){var i=o;break}}i&&("break"===t||"continue"===t)&&i.tryLoc<=e&&e<=i.finallyLoc&&(i=null);var a=i?i.completion:{};return a.type=t,a.arg=e,i?(this.method="next",this.next=i.finallyLoc,v):this.complete(a)},complete:function(t,e){if("throw"===t.type)throw t.arg;return"break"===t.type||"continue"===t.type?this.next=t.arg:"return"===t.type?(this.rval=this.arg=t.arg,this.method="return",this.next="end"):"normal"===t.type&&e&&(this.next=e),v},finish:function(t){for(var e=this.tryEntries.length-1;e>=0;--e){var n=this.tryEntries[e];if(n.finallyLoc===t)return this.complete(n.completion,n.afterLoc),T(n),v}},catch:function(t){for(var e=this.tryEntries.length-1;e>=0;--e){var n=this.tryEntries[e];if(n.tryLoc===t){var r=n.completion;if("throw"===r.type){var o=r.arg;T(n)}return o}}throw new Error("illegal catch attempt")},delegateYield:function(e,n,r){return this.delegate={iterator:N(e),resultName:n,nextLoc:r},"next"===this.method&&(this.arg=t),v}},e}function h(t,e,n,r,o,i,a){try{var u=t[i](a),c=u.value}catch(t){return void n(t)}u.done?e(c):Promise.resolve(c).then(r,o)}r=document.getElementById("tinymce-config-options"),o=function(){var t,e=(t=d().mark((function t(e,n){var o,i,a;return d().wrap((function(t){for(;;)switch(t.prev=t.next){case 0:return o=r.getAttribute("data-link-ajax-url"),t.next=3,fetch(o,{method:"POST",headers:{"X-CSRFToken":(0,u.getCsrfToken)()},body:JSON.stringify({query_string:e,object_types:["event","page","poi"],archived:!1})});case 3:if(200===(i=t.sent).status){t.next=7;break}return t.abrupt("return",[]);case 7:return t.next=9,i.json();case 9:return a=t.sent,t.abrupt("return",[a.data,n]);case 11:case"end":return t.stop()}}),t)})),function(){var e=this,n=arguments;return new Promise((function(r,o){var i=t.apply(e,n);function a(t){h(i,r,o,a,u,"next",t)}function u(t){h(i,r,o,a,u,"throw",t)}a(void 0)}))});return function(t,n){return e.apply(this,arguments)}}(),i=function(t){return/^[^:/]+[.].+/.test(t)?"https://".concat(t):t},a=function(t,e,n,r){null!==n&&(e.textContent=n),t.dom.setAttribs(e,r),t.selection.select(e)},tinymce.PluginManager.add("custom_link_input",(function(t,e){var n=function(t){return"a"===t.nodeName.toLowerCase()&&t.href},u=function(){for(var e=t.selection.getNode();null!==e;){if(n(e))return e;e=e.parentNode}return null},c=function(){var e=u(),n=e?e.textContent:t.selection.getContent({format:"text"}),c=e?e.getAttribute("href"):"",s=!!e&&e.children.length>0,d="",h=c,p="",y={url:"",text:""},m=0,g={text:r.getAttribute("data-link-no-results-text"),title:"",value:""},v=[g],b="",x={title:r.getAttribute("data-link-dialog-title-text"),body:{type:"panel",items:[{type:"input",name:"url",label:r.getAttribute("data-link-dialog-url-text")},{type:"input",name:"text",label:r.getAttribute("data-link-dialog-text-text"),disabled:s},{type:"label",label:r.getAttribute("data-link-dialog-internal_link-text"),items:[{type:"input",name:"search"},{type:"selectbox",name:"completions",items:v,disabled:!0}]}]},buttons:[{type:"cancel",text:r.getAttribute("data-dialog-cancel-text")},{type:"submit",name:"submit",text:r.getAttribute("data-dialog-submit-text"),primary:!0,disabled:!0}],initialData:{text:n,url:c},onSubmit:function(e){var n=e.getData(),r=n.url,o=s?null:n.text||r;if(""!==n.url.trim()){e.close();var c=i(r),l=u();l?a(t,l,o,{href:c}):t.insertContent("<a href=".concat(c,">").concat(o,"</a>"))}},onChange:function t(e){var n=e.getData(),r=!1;if(p!==n.completions){if(v.length>0){var i=v.find((function(t){return t.value===n.completions}));b=""!==i.value?i.title:""}else b="";""!==n.completions?(r=!0,e.setData({url:n.completions}),n.text&&(y.text===n.text||s)||e.setData({text:b})):e.setData({url:y.url,text:s?"":y.text})}p=n.completions,n=e.getData(),s||r||n.text!==h||e.setData({text:n.url}),h=n.url,n.url!==n.completions&&(y.url=n.url),s||n.text===n.url||n.text===b||(y.text=n.text),(n=e.getData()).url.trim()&&(s||n.text.trim())?e.enable("submit"):e.disable("submit"),n.search!==d&&""!==n.search?(m+=1,o(n.search,m).then((function(r){var o=l(r,2),i=o[0];if(o[1]===m){v.length=0;var a,u=function(t,e){var n="undefined"!=typeof Symbol&&t[Symbol.iterator]||t["@@iterator"];if(!n){if(Array.isArray(t)||(n=f(t))||e&&t&&"number"==typeof t.length){n&&(t=n);var r=0,o=function(){};return{s:o,n:function(){return r>=t.length?{done:!0}:{done:!1,value:t[r++]}},e:function(t){throw t},f:o}}throw new TypeError("Invalid attempt to iterate non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}var i,a=!0,u=!1;return{s:function(){n=n.call(t)},n:function(){var t=n.next();return a=t.done,t},e:function(t){u=!0,i=t},f:function(){try{a||null==n.return||n.return()}finally{if(u)throw i}}}}(i);try{for(u.s();!(a=u.n()).done;){var c=a.value;v.push({text:c.path,title:c.title,value:c.url})}}catch(t){u.e(t)}finally{u.f()}var s=!1;0===v.length&&(s=!0,v.push(g)),e.redial(x),e.setData(n),e.focus("search"),d=n.search,s?e.disable("completions"):e.enable("completions"),t(e)}}))):""===n.search&&""!==d&&(v.length=0,v.push(g),e.redial(x),e.setData(n),e.focus("search"),d=n.search,e.disable("completions"),t(e))}};return t.windowManager.open(x)};return t.addShortcut("Meta+K",r.getAttribute("data-link-menu-text"),c),t.ui.registry.addMenuItem("add_link",{text:r.getAttribute("data-link-menu-text"),icon:"link",shortcut:"Meta+K",onAction:c}),t.ui.registry.addContextForm("link_context_form",{predicate:n,initValue:function(){var t=u();return t?t.href:""},position:"node",commands:[{type:"contextformbutton",icon:"link",tooltip:r.getAttribute("data-update-text"),primary:!0,onSetup:function(e){var n=function(){e.setDisabled(t.readonly)};return t.on("nodechange",n),function(){t.off("nodechange",n)}},onAction:function(e){var n=e.getValue();if(n){var r=i(n),o=u();a(t,o,null,{href:r})}e.hide()}},{type:"contextformbutton",icon:"unlink",tooltip:r.getAttribute("data-link-remove-text"),active:!1,onAction:function(t){var e=u();e&&(e.insertAdjacentHTML("beforebegin",e.innerHTML),e.remove()),t.hide()}},{type:"contextformbutton",icon:"new-tab",tooltip:r.getAttribute("data-link-open-text"),active:!1,onAction:function(){var t=u();t&&window.open(t.getAttribute("href"),"_blank")}}]}),{}}))},82617:function(){function t(e){return t="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(t){return typeof t}:function(t){return t&&"function"==typeof Symbol&&t.constructor===Symbol&&t!==Symbol.prototype?"symbol":typeof t},t(e)}function e(t,e){var n=Object.keys(t);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(t);e&&(r=r.filter((function(e){return Object.getOwnPropertyDescriptor(t,e).enumerable}))),n.push.apply(n,r)}return n}function n(t){for(var n=1;n<arguments.length;n++){var o=null!=arguments[n]?arguments[n]:{};n%2?e(Object(o),!0).forEach((function(e){r(t,e,o[e])})):Object.getOwnPropertyDescriptors?Object.defineProperties(t,Object.getOwnPropertyDescriptors(o)):e(Object(o)).forEach((function(e){Object.defineProperty(t,e,Object.getOwnPropertyDescriptor(o,e))}))}return t}function r(e,n,r){return(n=function(e){var n=function(e,n){if("object"!==t(e)||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var o=r.call(e,n||"default");if("object"!==t(o))return o;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===n?String:Number)(e)}(e,"string");return"symbol"===t(n)?n:String(n)}(n))in e?Object.defineProperty(e,n,{value:r,enumerable:!0,configurable:!0,writable:!0}):e[n]=r,e}tinymce.util.Tools.resolve("tinymce.PluginManager").add("mediacenter",(function(t){!function(t){var e=function(){var e=document.createElement("div");document.body.append(e);var r=JSON.parse(document.getElementById("media_config_data").textContent);window.preactRender(window.preactJSX(window.IntegreatSelectMediaDialog,n(n({},r),{},{cancel:function(){return e.remove()},selectMedia:function(n){if(console.debug("File inserted into content:",n),e.remove(),n.type.startsWith("image/")){var r=document.createElement("a");r.href=n.url;var o=document.createElement("img");o.src=n.url,o.alt=n.altText,r.append(o),t.insertContent(r.outerHTML)}else{var i=document.createElement("a");i.href=n.url,i.innerText=n.name,t.insertContent(i.outerHTML)}}})),e)},r=document.getElementById("tinymce-config-options");t.ui.registry.addButton("openmediacenter",{text:r.getAttribute("data-media-button-translation"),icon:"image",onAction:e}),t.ui.registry.addMenuItem("openmediacenter",{text:r.getAttribute("data-media-item-translation"),icon:"image",onAction:e})}(t)}))},35593:function(t,e,n){"use strict";n.r(e)}},e={};function n(r){var o=e[r];if(void 0!==o)return o.exports;var i=e[r]={exports:{}};return t[r](i,i.exports,n),i.exports}n.r=function(t){"undefined"!=typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(t,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(t,"__esModule",{value:!0})};!function(){"use strict";n(82026),n(70089),n(82617),n(35593)}()}();