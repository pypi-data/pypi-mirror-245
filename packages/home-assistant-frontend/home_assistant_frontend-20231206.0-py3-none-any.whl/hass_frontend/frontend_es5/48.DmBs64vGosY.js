"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[48],{32511:function(e,t,n){var r,a=n(88962),i=n(33368),o=n(71650),s=n(82390),l=n(69205),c=n(70906),u=n(91808),d=(n(97393),n(58417)),h=n(39274),f=n(68144),v=n(95260);(0,u.Z)([(0,v.Mo)("ha-checkbox")],(function(e,t){var n=function(t){(0,l.Z)(r,t);var n=(0,c.Z)(r);function r(){var t;(0,o.Z)(this,r);for(var a=arguments.length,i=new Array(a),l=0;l<a;l++)i[l]=arguments[l];return t=n.call.apply(n,[this].concat(i)),e((0,s.Z)(t)),t}return(0,i.Z)(r)}(t);return{F:n,d:[{kind:"field",static:!0,key:"styles",value:function(){return[h.W,(0,f.iv)(r||(r=(0,a.Z)([":host{--mdc-theme-secondary:var(--primary-color)}"])))]}}]}}),d.A)},65189:function(e,t,n){var r,a,i,o=n(88962),s=n(33368),l=n(71650),c=n(82390),u=n(69205),d=n(70906),h=n(91808),f=(n(97393),n(68144)),v=n(95260),m=n(99312),p=n(40039),k=n(81043),b=n(34541),y=n(47838),g=(n(10187),n(32797),n(5239),n(17692),n(86439),n(47181)),w=(n(51358),n(46798),n(98490),n(31528),n(7695),n(44758),n(80354),n(68630),n(93217)),_=function(){var e=(0,k.Z)((0,m.Z)().mark((function e(t,a,i){return(0,m.Z)().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return r||(r=(0,w.Ud)(new Worker(new URL(n.p+n.u(71402),n.b)))),e.abrupt("return",r.renderMarkdown(t,a,i));case 2:case"end":return e.stop()}}),e)})));return function(t,n,r){return e.apply(this,arguments)}}(),Z={Note:"info",Warning:"warning"};(0,h.Z)([(0,v.Mo)("ha-markdown-element")],(function(e,t){var n,r=function(t){(0,u.Z)(r,t);var n=(0,d.Z)(r);function r(){var t;(0,l.Z)(this,r);for(var a=arguments.length,i=new Array(a),o=0;o<a;o++)i[o]=arguments[o];return t=n.call.apply(n,[this].concat(i)),e((0,c.Z)(t)),t}return(0,s.Z)(r)}(t);return{F:r,d:[{kind:"field",decorators:[(0,v.Cb)()],key:"content",value:void 0},{kind:"field",decorators:[(0,v.Cb)({type:Boolean})],key:"allowSvg",value:function(){return!1}},{kind:"field",decorators:[(0,v.Cb)({type:Boolean})],key:"breaks",value:function(){return!1}},{kind:"field",decorators:[(0,v.Cb)({type:Boolean,attribute:"lazy-images"})],key:"lazyImages",value:function(){return!1}},{kind:"method",key:"createRenderRoot",value:function(){return this}},{kind:"method",key:"update",value:function(e){(0,b.Z)((0,y.Z)(r.prototype),"update",this).call(this,e),void 0!==this.content&&this._render()}},{kind:"method",key:"_render",value:(n=(0,k.Z)((0,m.Z)().mark((function e(){var t,n,r,a,i,o,s,l,c,u,d;return(0,m.Z)().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.next=2,_(String(this.content),{breaks:this.breaks,gfm:!0},{allowSvg:this.allowSvg});case 2:for(this.innerHTML=e.sent,this._resize(),t=document.createTreeWalker(this,NodeFilter.SHOW_ELEMENT,null);t.nextNode();)if((n=t.currentNode)instanceof HTMLAnchorElement&&n.host!==document.location.host)n.target="_blank",n.rel="noreferrer noopener";else if(n instanceof HTMLImageElement)this.lazyImages&&(n.loading="lazy"),n.addEventListener("load",this._resize);else if(n instanceof HTMLQuoteElement&&(r=n.firstElementChild,a=null==r?void 0:r.firstElementChild,i=(null==a?void 0:a.textContent)&&Z[a.textContent],"STRONG"===(null==a?void 0:a.nodeName)&&i)){(s=document.createElement("ha-alert")).alertType=i,s.title="#text"===r.childNodes[1].nodeName&&(null===(o=r.childNodes[1].textContent)||void 0===o?void 0:o.trimStart())||"",l=Array.from(r.childNodes),c=(0,p.Z)(l.slice(l.findIndex((function(e){return e instanceof HTMLBRElement}))+1));try{for(c.s();!(u=c.n()).done;)d=u.value,s.appendChild(d)}catch(h){c.e(h)}finally{c.f()}n.firstElementChild.replaceWith(s)}case 6:case"end":return e.stop()}}),e,this)}))),function(){return n.apply(this,arguments)})},{kind:"field",key:"_resize",value:function(){var e=this;return function(){return(0,g.B)(e,"content-resize")}}}]}}),f.fl),n(9381),n(81312),n(52039),(0,h.Z)([(0,v.Mo)("ha-markdown")],(function(e,t){var n=function(t){(0,u.Z)(r,t);var n=(0,d.Z)(r);function r(){var t;(0,l.Z)(this,r);for(var a=arguments.length,i=new Array(a),o=0;o<a;o++)i[o]=arguments[o];return t=n.call.apply(n,[this].concat(i)),e((0,c.Z)(t)),t}return(0,s.Z)(r)}(t);return{F:n,d:[{kind:"field",decorators:[(0,v.Cb)()],key:"content",value:void 0},{kind:"field",decorators:[(0,v.Cb)({type:Boolean})],key:"allowSvg",value:function(){return!1}},{kind:"field",decorators:[(0,v.Cb)({type:Boolean})],key:"breaks",value:function(){return!1}},{kind:"field",decorators:[(0,v.Cb)({type:Boolean,attribute:"lazy-images"})],key:"lazyImages",value:function(){return!1}},{kind:"method",key:"render",value:function(){return this.content?(0,f.dy)(a||(a=(0,o.Z)(['<ha-markdown-element .content="','" .allowSvg="','" .breaks="','" .lazyImages="','"></ha-markdown-element>'])),this.content,this.allowSvg,this.breaks,this.lazyImages):f.Ld}},{kind:"get",static:!0,key:"styles",value:function(){return(0,f.iv)(i||(i=(0,o.Z)([":host{display:block}ha-markdown-element{-ms-user-select:text;-webkit-user-select:text;-moz-user-select:text}ha-markdown-element>:first-child{margin-top:0}ha-markdown-element>:last-child{margin-bottom:0}a{color:var(--primary-color)}img{max-width:100%}code,pre{background-color:var(--markdown-code-background-color,none);border-radius:3px}svg{background-color:var(--markdown-svg-background-color,none);color:var(--markdown-svg-color,none)}code{font-size:85%;padding:.2em .4em}pre code{padding:0}pre{padding:16px;overflow:auto;line-height:1.45;font-family:var(--code-font-family, monospace)}h1,h2,h3,h4,h5,h6{line-height:initial}h2{font-size:1.5em;font-weight:700}"])))}}]}}),f.oi)},48:function(e,t,n){n.r(t);var r,a,i,o,s,l,c,u,d,h,f,v,m,p,k,b=n(88962),y=n(33368),g=n(71650),w=n(82390),_=n(69205),Z=n(70906),O=n(91808),j=(n(97393),n(47704),n(82692),n(68144)),S=n(95260),E=n(49706),C=n(40095),x=(n(9381),n(32511),n(31206),n(34541)),z=n(47838),N=(n(76843),n(34997),n(46798),n(9849),n(12148),n(83448)),A=((0,O.Z)([(0,S.Mo)("ha-faded")],(function(e,t){var n=function(t){(0,_.Z)(r,t);var n=(0,Z.Z)(r);function r(){var t;(0,g.Z)(this,r);for(var a=arguments.length,i=new Array(a),o=0;o<a;o++)i[o]=arguments[o];return t=n.call.apply(n,[this].concat(i)),e((0,w.Z)(t)),t}return(0,y.Z)(r)}(t);return{F:n,d:[{kind:"field",decorators:[(0,S.Cb)({type:Number,attribute:"faded-height"})],key:"fadedHeight",value:function(){return 102}},{kind:"field",decorators:[(0,S.SB)()],key:"_contentShown",value:function(){return!1}},{kind:"method",key:"render",value:function(){return(0,j.dy)(r||(r=(0,b.Z)([' <div class="container ','" style="','" @click="','"> <slot @content-resize="','"></slot> </div> '])),(0,N.$)({faded:!this._contentShown}),this._contentShown?"":"max-height: ".concat(this.fadedHeight,"px"),this._showContent,this._setShowContent)}},{kind:"get",key:"_slottedHeight",value:function(){var e;return(null===(e=this.shadowRoot.querySelector(".container"))||void 0===e?void 0:e.firstElementChild).assignedElements().reduce((function(e,t){return e+t.offsetHeight}),0)||0}},{kind:"method",key:"_setShowContent",value:function(){var e=this._slottedHeight;this._contentShown=0!==e&&e<=this.fadedHeight+50}},{kind:"method",key:"firstUpdated",value:function(e){(0,x.Z)((0,z.Z)(n.prototype),"firstUpdated",this).call(this,e),this._setShowContent()}},{kind:"method",key:"_showContent",value:function(){this._contentShown=!0}},{kind:"get",static:!0,key:"styles",value:function(){return(0,j.iv)(a||(a=(0,b.Z)([".container{display:block;height:auto;cursor:default}.faded{cursor:pointer;-webkit-mask-image:linear-gradient(to bottom,black 25%,transparent 100%);mask-image:linear-gradient(to bottom,black 25%,transparent 100%);overflow-y:hidden}"])))}}]}}),j.oi),n(83927),n(65189),n(56007)),M=n(24833);(0,O.Z)([(0,S.Mo)("more-info-update")],(function(e,t){var n=function(t){(0,_.Z)(r,t);var n=(0,Z.Z)(r);function r(){var t;(0,g.Z)(this,r);for(var a=arguments.length,i=new Array(a),o=0;o<a;o++)i[o]=arguments[o];return t=n.call.apply(n,[this].concat(i)),e((0,w.Z)(t)),t}return(0,y.Z)(r)}(t);return{F:n,d:[{kind:"field",decorators:[(0,S.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,S.Cb)({attribute:!1})],key:"stateObj",value:void 0},{kind:"field",decorators:[(0,S.SB)()],key:"_releaseNotes",value:void 0},{kind:"field",decorators:[(0,S.SB)()],key:"_error",value:void 0},{kind:"method",key:"render",value:function(){var e,t;if(!this.hass||!this.stateObj||(0,A.rk)(this.stateObj.state))return j.Ld;var n=this.stateObj.attributes.latest_version&&this.stateObj.attributes.skipped_version===this.stateObj.attributes.latest_version;return(0,j.dy)(i||(i=(0,b.Z)([" "," <h3>","</h3> ",' <div class="row"> <div class="key"> ',' </div> <div class="value"> ',' </div> </div> <div class="row"> <div class="key"> ',' </div> <div class="value"> '," </div> </div> "," "," ",' <hr> <div class="actions"> '," "," </div> "])),this.stateObj.attributes.in_progress?(0,C.e)(this.stateObj,M.k6)&&"number"==typeof this.stateObj.attributes.in_progress?(0,j.dy)(o||(o=(0,b.Z)(['<mwc-linear-progress .progress="','" buffer=""></mwc-linear-progress>'])),this.stateObj.attributes.in_progress/100):(0,j.dy)(s||(s=(0,b.Z)(["<mwc-linear-progress indeterminate></mwc-linear-progress>"]))):"",this.stateObj.attributes.title,this._error?(0,j.dy)(l||(l=(0,b.Z)(['<ha-alert alert-type="error">',"</ha-alert>"])),this._error):"",this.hass.formatEntityAttributeName(this.stateObj,"installed_version"),null!==(e=this.stateObj.attributes.installed_version)&&void 0!==e?e:this.hass.localize("state.default.unavailable"),this.hass.formatEntityAttributeName(this.stateObj,"latest_version"),null!==(t=this.stateObj.attributes.latest_version)&&void 0!==t?t:this.hass.localize("state.default.unavailable"),this.stateObj.attributes.release_url?(0,j.dy)(c||(c=(0,b.Z)(['<div class="row"> <div class="key"> <a href="','" target="_blank" rel="noreferrer"> '," </a> </div> </div>"])),this.stateObj.attributes.release_url,this.hass.localize("ui.dialogs.more_info_control.update.release_announcement")):"",(0,C.e)(this.stateObj,M.BD)&&!this._error?this._releaseNotes?(0,j.dy)(d||(d=(0,b.Z)(['<hr> <ha-faded> <ha-markdown .content="','"></ha-markdown> </ha-faded> '])),this._releaseNotes):(0,j.dy)(u||(u=(0,b.Z)(['<div class="flex center"> <ha-circular-progress indeterminate></ha-circular-progress> </div>']))):this.stateObj.attributes.release_summary?(0,j.dy)(h||(h=(0,b.Z)(['<hr> <ha-markdown .content="','"></ha-markdown>'])),this.stateObj.attributes.release_summary):"",(0,C.e)(this.stateObj,M.zG)?(0,j.dy)(f||(f=(0,b.Z)(['<hr> <ha-formfield .label="','"> <ha-checkbox checked="checked" .disabled="','"></ha-checkbox> </ha-formfield> '])),this.hass.localize("ui.dialogs.more_info_control.update.create_backup"),(0,M.Sk)(this.stateObj)):"",this.stateObj.attributes.auto_update?"":this.stateObj.state===E.lC&&this.stateObj.attributes.skipped_version?(0,j.dy)(v||(v=(0,b.Z)([' <mwc-button @click="','"> '," </mwc-button> "])),this._handleClearSkipped,this.hass.localize("ui.dialogs.more_info_control.update.clear_skipped")):(0,j.dy)(m||(m=(0,b.Z)([' <mwc-button @click="','" .disabled="','"> '," </mwc-button> "])),this._handleSkip,n||this.stateObj.state===E.lC||(0,M.Sk)(this.stateObj),this.hass.localize("ui.dialogs.more_info_control.update.skip")),(0,C.e)(this.stateObj,M.oF)?(0,j.dy)(p||(p=(0,b.Z)([' <mwc-button @click="','" .disabled="','"> '," </mwc-button> "])),this._handleInstall,this.stateObj.state===E.lC&&!n||(0,M.Sk)(this.stateObj),this.hass.localize("ui.dialogs.more_info_control.update.install")):"")}},{kind:"method",key:"firstUpdated",value:function(){var e=this;(0,C.e)(this.stateObj,M.BD)&&(0,M.UJ)(this.hass,this.stateObj.entity_id).then((function(t){e._releaseNotes=t})).catch((function(t){e._error=t.message}))}},{kind:"get",key:"_shouldCreateBackup",value:function(){var e;if(!(0,C.e)(this.stateObj,M.zG))return null;var t=null===(e=this.shadowRoot)||void 0===e?void 0:e.querySelector("ha-checkbox");return!t||t.checked}},{kind:"method",key:"_handleInstall",value:function(){var e={entity_id:this.stateObj.entity_id};this._shouldCreateBackup&&(e.backup=!0),(0,C.e)(this.stateObj,M.kK)&&this.stateObj.attributes.latest_version&&(e.version=this.stateObj.attributes.latest_version),this.hass.callService("update","install",e)}},{kind:"method",key:"_handleSkip",value:function(){this.hass.callService("update","skip",{entity_id:this.stateObj.entity_id})}},{kind:"method",key:"_handleClearSkipped",value:function(){this.hass.callService("update","clear_skipped",{entity_id:this.stateObj.entity_id})}},{kind:"get",static:!0,key:"styles",value:function(){return(0,j.iv)(k||(k=(0,b.Z)(["hr{border-color:var(--divider-color);border-bottom:none;margin:16px 0}ha-expansion-panel{margin:16px 0}.row{margin:0;display:flex;flex-direction:row;justify-content:space-between}.actions{margin:8px 0 0;display:flex;flex-wrap:wrap;justify-content:center}.actions mwc-button{margin:0 4px 4px}a{color:var(--primary-color)}.flex.center{display:flex;justify-content:center;align-items:center}mwc-linear-progress{margin-bottom:-8px;margin-top:4px}ha-markdown{direction:ltr}"])))}}]}}),j.oi)},79894:function(e,t,n){n(68077)({target:"Number",stat:!0,nonConfigurable:!0,nonWritable:!0},{MAX_SAFE_INTEGER:9007199254740991})},93217:function(e,t,n){n.d(t,{Ud:function(){return b}});var r=n(68990),a=n(93359),i=n(59202),o=n(53709),s=n(40039),l=n(76775),c=(n(58556),n(94738),n(98214),n(46798),n(51467),n(22859),n(85717),n(51358),n(96043),n(5239),n(98490),n(10999),n(52117),n(63789),n(82479),n(94570),n(99397),n(89802),n(46349),n(70320),n(34997),n(9849),n(12148),n(17692),n(47084),n(39685),n(97393),n(91989),n(86576),n(79894),n(76843),Symbol("Comlink.proxy")),u=Symbol("Comlink.endpoint"),d=Symbol("Comlink.releaseProxy"),h=Symbol("Comlink.finalizer"),f=Symbol("Comlink.thrown"),v=function(e){return"object"===(0,l.Z)(e)&&null!==e||"function"==typeof e},m=new Map([["proxy",{canHandle:function(e){return v(e)&&e[c]},serialize:function(e){var t=new MessageChannel,n=t.port1,r=t.port2;return p(e,n),[r,[r]]},deserialize:function(e){return e.start(),b(e)}}],["throw",{canHandle:function(e){return v(e)&&f in e},serialize:function(e){var t=e.value;return[t instanceof Error?{isError:!0,value:{message:t.message,name:t.name,stack:t.stack}}:{isError:!1,value:t},[]]},deserialize:function(e){if(e.isError)throw Object.assign(new Error(e.value.message),e.value);throw e.value}}]]);function p(e){var t=arguments.length>1&&void 0!==arguments[1]?arguments[1]:globalThis,n=arguments.length>2&&void 0!==arguments[2]?arguments[2]:["*"];t.addEventListener("message",(function l(u){if(u&&u.data)if(function(e,t){var n,r=(0,s.Z)(e);try{for(r.s();!(n=r.n()).done;){var a=n.value;if(t===a||"*"===a)return!0;if(a instanceof RegExp&&a.test(t))return!0}}catch(i){r.e(i)}finally{r.f()}return!1}(n,u.origin)){var d,v=Object.assign({path:[]},u.data),m=v.id,b=v.type,y=v.path,g=(u.data.argumentList||[]).map(E);try{var w=y.slice(0,-1).reduce((function(e,t){return e[t]}),e),_=y.reduce((function(e,t){return e[t]}),e);switch(b){case"GET":d=_;break;case"SET":w[y.slice(-1)[0]]=E(u.data.value),d=!0;break;case"APPLY":d=_.apply(w,g);break;case"CONSTRUCT":var Z;d=function(e){return Object.assign(e,(0,a.Z)({},c,!0))}((0,i.Z)(_,(0,o.Z)(g)));break;case"ENDPOINT":var O=new MessageChannel,C=O.port1,x=O.port2;p(e,x),d=function(e,t){return j.set(e,t),e}(C,[C]);break;case"RELEASE":d=void 0;break;default:return}}catch(Z){d=(0,a.Z)({value:Z},f,0)}Promise.resolve(d).catch((function(e){return(0,a.Z)({value:e},f,0)})).then((function(n){var a=S(n),i=(0,r.Z)(a,2),o=i[0],s=i[1];t.postMessage(Object.assign(Object.assign({},o),{id:m}),s),"RELEASE"===b&&(t.removeEventListener("message",l),k(t),h in e&&"function"==typeof e[h]&&e[h]())})).catch((function(e){var n=S((0,a.Z)({value:new TypeError("Unserializable return value")},f,0)),i=(0,r.Z)(n,2),o=i[0],s=i[1];t.postMessage(Object.assign(Object.assign({},o),{id:m}),s)}))}else console.warn("Invalid origin '".concat(u.origin,"' for comlink proxy"))})),t.start&&t.start()}function k(e){(function(e){return"MessagePort"===e.constructor.name})(e)&&e.close()}function b(e,t){return Z(e,[],t)}function y(e){if(e)throw new Error("Proxy has been released and is not useable")}function g(e){return C(e,{type:"RELEASE"}).then((function(){k(e)}))}var w=new WeakMap,_="FinalizationRegistry"in globalThis&&new FinalizationRegistry((function(e){var t=(w.get(e)||0)-1;w.set(e,t),0===t&&g(e)}));function Z(e){var t=arguments.length>1&&void 0!==arguments[1]?arguments[1]:[],n=!1,a=new Proxy(arguments.length>2&&void 0!==arguments[2]?arguments[2]:function(){},{get:function(r,i){if(y(n),i===d)return function(){!function(e){_&&_.unregister(e)}(a),g(e),n=!0};if("then"===i){if(0===t.length)return{then:function(){return a}};var s=C(e,{type:"GET",path:t.map((function(e){return e.toString()}))}).then(E);return s.then.bind(s)}return Z(e,[].concat((0,o.Z)(t),[i]))},set:function(a,i,s){y(n);var l=S(s),c=(0,r.Z)(l,2),u=c[0],d=c[1];return C(e,{type:"SET",path:[].concat((0,o.Z)(t),[i]).map((function(e){return e.toString()})),value:u},d).then(E)},apply:function(a,i,o){y(n);var s=t[t.length-1];if(s===u)return C(e,{type:"ENDPOINT"}).then(E);if("bind"===s)return Z(e,t.slice(0,-1));var l=O(o),c=(0,r.Z)(l,2),d=c[0],h=c[1];return C(e,{type:"APPLY",path:t.map((function(e){return e.toString()})),argumentList:d},h).then(E)},construct:function(a,i){y(n);var o=O(i),s=(0,r.Z)(o,2),l=s[0],c=s[1];return C(e,{type:"CONSTRUCT",path:t.map((function(e){return e.toString()})),argumentList:l},c).then(E)}});return function(e,t){var n=(w.get(t)||0)+1;w.set(t,n),_&&_.register(e,t,e)}(a,e),a}function O(e){var t,n=e.map(S);return[n.map((function(e){return e[0]})),(t=n.map((function(e){return e[1]})),Array.prototype.concat.apply([],t))]}var j=new WeakMap;function S(e){var t,n=(0,s.Z)(m);try{for(n.s();!(t=n.n()).done;){var a=(0,r.Z)(t.value,2),i=a[0],o=a[1];if(o.canHandle(e)){var l=o.serialize(e),c=(0,r.Z)(l,2);return[{type:"HANDLER",name:i,value:c[0]},c[1]]}}}catch(u){n.e(u)}finally{n.f()}return[{type:"RAW",value:e},j.get(e)||[]]}function E(e){switch(e.type){case"HANDLER":return m.get(e.name).deserialize(e.value);case"RAW":return e.value}}function C(e,t,n){return new Promise((function(r){var a=new Array(4).fill(0).map((function(){return Math.floor(Math.random()*Number.MAX_SAFE_INTEGER).toString(16)})).join("-");e.addEventListener("message",(function t(n){n.data&&n.data.id&&n.data.id===a&&(e.removeEventListener("message",t),r(n.data))})),e.start&&e.start(),e.postMessage(Object.assign({id:a},t),n)}))}}}]);
//# sourceMappingURL=48.DmBs64vGosY.js.map