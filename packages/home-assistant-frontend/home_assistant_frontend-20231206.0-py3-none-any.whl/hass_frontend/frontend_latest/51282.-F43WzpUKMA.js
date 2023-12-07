/*! For license information please see 51282.-F43WzpUKMA.js.LICENSE.txt */
export const id=51282;export const ids=[51282];export const modules={65189:(e,t,n)=>{var o=n(17463),r=n(68144),i=n(79932),a=n(34541),s=n(47838),l=n(47181),d=n(93217);let c;const u={Note:"info",Warning:"warning"};(0,o.Z)([(0,i.Mo)("ha-markdown-element")],(function(e,t){class o extends t{constructor(...t){super(...t),e(this)}}return{F:o,d:[{kind:"field",decorators:[(0,i.Cb)()],key:"content",value:void 0},{kind:"field",decorators:[(0,i.Cb)({type:Boolean})],key:"allowSvg",value:()=>!1},{kind:"field",decorators:[(0,i.Cb)({type:Boolean})],key:"breaks",value:()=>!1},{kind:"field",decorators:[(0,i.Cb)({type:Boolean,attribute:"lazy-images"})],key:"lazyImages",value:()=>!1},{kind:"method",key:"createRenderRoot",value:function(){return this}},{kind:"method",key:"update",value:function(e){(0,a.Z)((0,s.Z)(o.prototype),"update",this).call(this,e),void 0!==this.content&&this._render()}},{kind:"method",key:"_render",value:async function(){this.innerHTML=await(async(e,t,o)=>(c||(c=(0,d.Ud)(new Worker(new URL(n.p+n.u(71402),n.b),{type:"module"}))),c.renderMarkdown(e,t,o)))(String(this.content),{breaks:this.breaks,gfm:!0},{allowSvg:this.allowSvg}),this._resize();const e=document.createTreeWalker(this,NodeFilter.SHOW_ELEMENT,null);for(;e.nextNode();){const n=e.currentNode;if(n instanceof HTMLAnchorElement&&n.host!==document.location.host)n.target="_blank",n.rel="noreferrer noopener";else if(n instanceof HTMLImageElement)this.lazyImages&&(n.loading="lazy"),n.addEventListener("load",this._resize);else if(n instanceof HTMLQuoteElement){const e=n.firstElementChild,o=null==e?void 0:e.firstElementChild,r=(null==o?void 0:o.textContent)&&u[o.textContent];if("STRONG"===(null==o?void 0:o.nodeName)&&r){var t;const o=document.createElement("ha-alert");o.alertType=r,o.title="#text"===e.childNodes[1].nodeName&&(null===(t=e.childNodes[1].textContent)||void 0===t?void 0:t.trimStart())||"";const i=Array.from(e.childNodes);for(const e of i.slice(i.findIndex((e=>e instanceof HTMLBRElement))+1))o.appendChild(e);n.firstElementChild.replaceWith(o)}}}}},{kind:"field",key:"_resize",value(){return()=>(0,l.B)(this,"content-resize")}}]}}),r.fl);n(9381),n(81312),n(52039);(0,o.Z)([(0,i.Mo)("ha-markdown")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,i.Cb)()],key:"content",value:void 0},{kind:"field",decorators:[(0,i.Cb)({type:Boolean})],key:"allowSvg",value:()=>!1},{kind:"field",decorators:[(0,i.Cb)({type:Boolean})],key:"breaks",value:()=>!1},{kind:"field",decorators:[(0,i.Cb)({type:Boolean,attribute:"lazy-images"})],key:"lazyImages",value:()=>!1},{kind:"method",key:"render",value:function(){return this.content?r.dy`<ha-markdown-element .content="${this.content}" .allowSvg="${this.allowSvg}" .breaks="${this.breaks}" .lazyImages="${this.lazyImages}"></ha-markdown-element>`:r.Ld}},{kind:"get",static:!0,key:"styles",value:function(){return r.iv`:host{display:block}ha-markdown-element{-ms-user-select:text;-webkit-user-select:text;-moz-user-select:text}ha-markdown-element>:first-child{margin-top:0}ha-markdown-element>:last-child{margin-bottom:0}a{color:var(--primary-color)}img{max-width:100%}code,pre{background-color:var(--markdown-code-background-color,none);border-radius:3px}svg{background-color:var(--markdown-svg-background-color,none);color:var(--markdown-svg-color,none)}code{font-size:85%;padding:.2em .4em}pre code{padding:0}pre{padding:16px;overflow:auto;line-height:1.45;font-family:var(--code-font-family, monospace)}h1,h2,h3,h4,h5,h6{line-height:initial}h2{font-size:1.5em;font-weight:700}`}}]}}),r.oi)},17324:(e,t,n)=>{n.d(t,{N:()=>o,Z:()=>r});const o=(e,t,n)=>e.subscribeMessage((e=>t(e)),{type:"render_template",...n}),r=(e,t,n,o,r)=>e.connection.subscribeMessage(r,{type:"template/start_preview",flow_id:t,flow_type:n,user_input:o})},51282:(e,t,n)=>{n.r(t),n.d(t,{HuiMarkdownCard:()=>u});var o=n(17463),r=n(34541),i=n(47838),a=n(68144),s=n(79932),l=n(83448),d=n(62877),c=(n(22098),n(65189),n(9381),n(17324));let u=(0,o.Z)([(0,s.Mo)("hui-markdown-card")],(function(e,t){class o extends t{constructor(...t){super(...t),e(this)}}return{F:o,d:[{kind:"method",static:!0,key:"getConfigElement",value:async function(){return await Promise.all([n.e(68331),n.e(26156)]).then(n.bind(n,54102)),document.createElement("hui-markdown-card-editor")}},{kind:"method",static:!0,key:"getStubConfig",value:function(){return{type:"markdown",content:"The **Markdown** card allows you to write any text. You can style it **bold**, *italicized*, ~strikethrough~ etc. You can do images, links, and more.\n\nFor more information see the [Markdown Cheatsheet](https://commonmark.org/help)."}}},{kind:"field",decorators:[(0,s.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,s.Cb)({type:Boolean})],key:"editMode",value:void 0},{kind:"field",decorators:[(0,s.SB)()],key:"_config",value:void 0},{kind:"field",decorators:[(0,s.SB)()],key:"_error",value:void 0},{kind:"field",decorators:[(0,s.SB)()],key:"_errorLevel",value:void 0},{kind:"field",decorators:[(0,s.SB)()],key:"_templateResult",value:void 0},{kind:"field",key:"_unsubRenderTemplate",value:void 0},{kind:"method",key:"getCardSize",value:function(){return void 0===this._config?3:void 0===this._config.card_size?Math.round(this._config.content.split("\n").length/2)+(this._config.title?1:0):this._config.card_size}},{kind:"method",key:"setConfig",value:function(e){var t;if(!e.content)throw new Error("Content required");(null===(t=this._config)||void 0===t?void 0:t.content)!==e.content&&this._tryDisconnect(),this._config=e}},{kind:"method",key:"connectedCallback",value:function(){(0,r.Z)((0,i.Z)(o.prototype),"connectedCallback",this).call(this),this._tryConnect()}},{kind:"method",key:"disconnectedCallback",value:function(){(0,r.Z)((0,i.Z)(o.prototype),"disconnectedCallback",this).call(this),this._tryDisconnect()}},{kind:"method",key:"render",value:function(){var e,t;return this._config?a.dy` ${this._error?a.dy`<ha-alert alert-type="${(null===(e=this._errorLevel)||void 0===e?void 0:e.toLowerCase())||"error"}">${this._error}</ha-alert>`:a.Ld} <ha-card .header="${this._config.title}"> <ha-markdown breaks class="${(0,l.$)({"no-header":!this._config.title})}" .content="${null===(t=this._templateResult)||void 0===t?void 0:t.result}"></ha-markdown> </ha-card> `:a.Ld}},{kind:"method",key:"updated",value:function(e){if((0,r.Z)((0,i.Z)(o.prototype),"updated",this).call(this,e),!this._config||!this.hass)return;e.has("_config")&&this._tryConnect();const t=e.get("hass"),n=e.get("_config");t&&n&&t.themes===this.hass.themes&&n.theme===this._config.theme||(0,d.R)(this,this.hass.themes,this._config.theme)}},{kind:"method",key:"_tryConnect",value:async function(){if(void 0===this._unsubRenderTemplate&&this.hass&&this._config){this._error=void 0,this._errorLevel=void 0;try{this._unsubRenderTemplate=(0,c.N)(this.hass.connection,(e=>{"error"in e?"ERROR"!==e.level&&"ERROR"===this._errorLevel||(this._error=e.error,this._errorLevel=e.level):this._templateResult=e}),{template:this._config.content,entity_ids:this._config.entity_id,variables:{config:this._config,user:this.hass.user.name},strict:!0,report_errors:this.editMode}),await this._unsubRenderTemplate}catch(e){this.editMode&&(this._error=e.message,this._errorLevel=void 0),this._templateResult={result:this._config.content,listeners:{all:!1,domains:[],entities:[],time:!1}},this._unsubRenderTemplate=void 0}}}},{kind:"method",key:"_tryDisconnect",value:async function(){this._unsubRenderTemplate&&(this._unsubRenderTemplate.then((e=>e())).catch((()=>{})),this._unsubRenderTemplate=void 0,this._error=void 0,this._errorLevel=void 0)}},{kind:"get",static:!0,key:"styles",value:function(){return a.iv`ha-card{height:100%}ha-alert{margin-bottom:8px}ha-markdown{padding:0 16px 16px;word-wrap:break-word}ha-markdown.no-header{padding-top:16px}`}}]}}),a.oi)},93217:(e,t,n)=>{n.d(t,{Ud:()=>h});const o=Symbol("Comlink.proxy"),r=Symbol("Comlink.endpoint"),i=Symbol("Comlink.releaseProxy"),a=Symbol("Comlink.finalizer"),s=Symbol("Comlink.thrown"),l=e=>"object"==typeof e&&null!==e||"function"==typeof e,d=new Map([["proxy",{canHandle:e=>l(e)&&e[o],serialize(e){const{port1:t,port2:n}=new MessageChannel;return c(e,t),[n,[n]]},deserialize:e=>(e.start(),h(e))}],["throw",{canHandle:e=>l(e)&&s in e,serialize({value:e}){let t;return t=e instanceof Error?{isError:!0,value:{message:e.message,name:e.name,stack:e.stack}}:{isError:!1,value:e},[t,[]]},deserialize(e){if(e.isError)throw Object.assign(new Error(e.value.message),e.value);throw e.value}}]]);function c(e,t=globalThis,n=["*"]){t.addEventListener("message",(function r(i){if(!i||!i.data)return;if(!function(e,t){for(const n of e){if(t===n||"*"===n)return!0;if(n instanceof RegExp&&n.test(t))return!0}return!1}(n,i.origin))return void console.warn(`Invalid origin '${i.origin}' for comlink proxy`);const{id:l,type:d,path:h}=Object.assign({path:[]},i.data),m=(i.data.argumentList||[]).map(_);let f;try{const t=h.slice(0,-1).reduce(((e,t)=>e[t]),e),n=h.reduce(((e,t)=>e[t]),e);switch(d){case"GET":f=n;break;case"SET":t[h.slice(-1)[0]]=_(i.data.value),f=!0;break;case"APPLY":f=n.apply(t,m);break;case"CONSTRUCT":f=function(e){return Object.assign(e,{[o]:!0})}(new n(...m));break;case"ENDPOINT":{const{port1:t,port2:n}=new MessageChannel;c(e,n),f=function(e,t){return y.set(e,t),e}(t,[t])}break;case"RELEASE":f=void 0;break;default:return}}catch(e){f={value:e,[s]:0}}Promise.resolve(f).catch((e=>({value:e,[s]:0}))).then((n=>{const[o,i]=b(n);t.postMessage(Object.assign(Object.assign({},o),{id:l}),i),"RELEASE"===d&&(t.removeEventListener("message",r),u(t),a in e&&"function"==typeof e[a]&&e[a]())})).catch((e=>{const[n,o]=b({value:new TypeError("Unserializable return value"),[s]:0});t.postMessage(Object.assign(Object.assign({},n),{id:l}),o)}))})),t.start&&t.start()}function u(e){(function(e){return"MessagePort"===e.constructor.name})(e)&&e.close()}function h(e,t){return k(e,[],t)}function m(e){if(e)throw new Error("Proxy has been released and is not useable")}function f(e){return w(e,{type:"RELEASE"}).then((()=>{u(e)}))}const p=new WeakMap,g="FinalizationRegistry"in globalThis&&new FinalizationRegistry((e=>{const t=(p.get(e)||0)-1;p.set(e,t),0===t&&f(e)}));function k(e,t=[],n=function(){}){let o=!1;const a=new Proxy(n,{get(n,r){if(m(o),r===i)return()=>{!function(e){g&&g.unregister(e)}(a),f(e),o=!0};if("then"===r){if(0===t.length)return{then:()=>a};const n=w(e,{type:"GET",path:t.map((e=>e.toString()))}).then(_);return n.then.bind(n)}return k(e,[...t,r])},set(n,r,i){m(o);const[a,s]=b(i);return w(e,{type:"SET",path:[...t,r].map((e=>e.toString())),value:a},s).then(_)},apply(n,i,a){m(o);const s=t[t.length-1];if(s===r)return w(e,{type:"ENDPOINT"}).then(_);if("bind"===s)return k(e,t.slice(0,-1));const[l,d]=v(a);return w(e,{type:"APPLY",path:t.map((e=>e.toString())),argumentList:l},d).then(_)},construct(n,r){m(o);const[i,a]=v(r);return w(e,{type:"CONSTRUCT",path:t.map((e=>e.toString())),argumentList:i},a).then(_)}});return function(e,t){const n=(p.get(t)||0)+1;p.set(t,n),g&&g.register(e,t,e)}(a,e),a}function v(e){const t=e.map(b);return[t.map((e=>e[0])),(n=t.map((e=>e[1])),Array.prototype.concat.apply([],n))];var n}const y=new WeakMap;function b(e){for(const[t,n]of d)if(n.canHandle(e)){const[o,r]=n.serialize(e);return[{type:"HANDLER",name:t,value:o},r]}return[{type:"RAW",value:e},y.get(e)||[]]}function _(e){switch(e.type){case"HANDLER":return d.get(e.name).deserialize(e.value);case"RAW":return e.value}}function w(e,t,n){return new Promise((o=>{const r=new Array(4).fill(0).map((()=>Math.floor(Math.random()*Number.MAX_SAFE_INTEGER).toString(16))).join("-");e.addEventListener("message",(function t(n){n.data&&n.data.id&&n.data.id===r&&(e.removeEventListener("message",t),o(n.data))})),e.start&&e.start(),e.postMessage(Object.assign({id:r},t),n)}))}}};
//# sourceMappingURL=51282.-F43WzpUKMA.js.map