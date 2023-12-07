/*! For license information please see 94985.1ryRK2Pp8lI.js.LICENSE.txt */
export const id=94985;export const ids=[94985];export const modules={76680:(e,t,a)=>{function i(e){return void 0===e||Array.isArray(e)?e:[e]}a.d(t,{r:()=>i})},55642:(e,t,a)=>{a.d(t,{h:()=>n});var i=a(68144),o=a(57835);const n=(0,o.XM)(class extends o.Xe{constructor(e){if(super(e),this._element=void 0,e.type!==o.pX.CHILD)throw new Error("dynamicElementDirective can only be used in content bindings")}update(e,[t,a]){return this._element&&this._element.localName===t?(a&&Object.entries(a).forEach((([e,t])=>{this._element[e]=t})),i.Jb):this.render(t,a)}render(e,t){return this._element=document.createElement(e),t&&Object.entries(t).forEach((([e,t])=>{this._element[e]=t})),this._element}})},22311:(e,t,a)=>{a.d(t,{N:()=>o});var i=a(58831);const o=e=>(0,i.M)(e.entity_id)},40095:(e,t,a)=>{a.d(t,{e:()=>i});const i=(e,t)=>o(e.attributes,t),o=(e,t)=>0!=(e.supported_features&t)},50424:(e,t,a)=>{a.d(t,{n:()=>i});const i=(e,t)=>{const a=new Promise(((t,a)=>{setTimeout((()=>{a(`Timed out in ${e} ms.`)}),e)}));return Promise.race([t,a])}},34821:(e,t,a)=>{a.d(t,{i:()=>f});var i=a(17463),o=a(34541),n=a(47838),s=a(87762),r=a(91632),d=a(68144),c=a(79932),l=a(74265);a(10983);const h=["button","ha-list-item"],f=(e,t)=>{var a;return d.dy` <div class="header_title">${t}</div> <ha-icon-button .label="${null!==(a=null==e?void 0:e.localize("ui.dialogs.generic.close"))&&void 0!==a?a:"Close"}" .path="${"M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z"}" dialogAction="close" class="header_button"></ha-icon-button> `};(0,i.Z)([(0,c.Mo)("ha-dialog")],(function(e,t){class a extends t{constructor(...t){super(...t),e(this)}}return{F:a,d:[{kind:"field",key:l.gA,value:void 0},{kind:"method",key:"scrollToPos",value:function(e,t){var a;null===(a=this.contentElement)||void 0===a||a.scrollTo(e,t)}},{kind:"method",key:"renderHeading",value:function(){return d.dy`<slot name="heading"> ${(0,o.Z)((0,n.Z)(a.prototype),"renderHeading",this).call(this)} </slot>`}},{kind:"method",key:"firstUpdated",value:function(){var e;(0,o.Z)((0,n.Z)(a.prototype),"firstUpdated",this).call(this),this.suppressDefaultPressSelector=[this.suppressDefaultPressSelector,h].join(", "),this._updateScrolledAttribute(),null===(e=this.contentElement)||void 0===e||e.addEventListener("scroll",this._onScroll,{passive:!0})}},{kind:"method",key:"disconnectedCallback",value:function(){(0,o.Z)((0,n.Z)(a.prototype),"disconnectedCallback",this).call(this),this.contentElement.removeEventListener("scroll",this._onScroll)}},{kind:"field",key:"_onScroll",value(){return()=>{this._updateScrolledAttribute()}}},{kind:"method",key:"_updateScrolledAttribute",value:function(){this.contentElement&&this.toggleAttribute("scrolled",0!==this.contentElement.scrollTop)}},{kind:"field",static:!0,key:"styles",value:()=>[r.W,d.iv`:host([scrolled]) ::slotted(ha-dialog-header){border-bottom:1px solid var(--mdc-dialog-scroll-divider-color,rgba(0,0,0,.12))}.mdc-dialog{--mdc-dialog-scroll-divider-color:var(
          --dialog-scroll-divider-color,
          var(--divider-color)
        );z-index:var(--dialog-z-index,8);-webkit-backdrop-filter:var(--dialog-backdrop-filter,none);backdrop-filter:var(--dialog-backdrop-filter,none);--mdc-dialog-box-shadow:var(--dialog-box-shadow, none);--mdc-typography-headline6-font-weight:400;--mdc-typography-headline6-font-size:1.574rem}.mdc-dialog__actions{justify-content:var(--justify-action-buttons,flex-end);padding-bottom:max(env(safe-area-inset-bottom),24px)}.mdc-dialog__actions span:first-child{flex:var(--secondary-action-button-flex,unset)}.mdc-dialog__actions span:nth-child(2){flex:var(--primary-action-button-flex,unset)}.mdc-dialog__container{align-items:var(--vertical-align-dialog,center)}.mdc-dialog__title{padding:24px 24px 0 24px;text-overflow:ellipsis;overflow:hidden}.mdc-dialog__actions{padding:12px 24px 12px 24px}.mdc-dialog__title::before{display:block;height:0px}.mdc-dialog .mdc-dialog__content{position:var(--dialog-content-position,relative);padding:var(--dialog-content-padding,24px)}:host([hideactions]) .mdc-dialog .mdc-dialog__content{padding-bottom:max(var(--dialog-content-padding,24px),env(safe-area-inset-bottom))}.mdc-dialog .mdc-dialog__surface{position:var(--dialog-surface-position,relative);top:var(--dialog-surface-top);margin-top:var(--dialog-surface-margin-top);min-height:var(--mdc-dialog-min-height,auto);border-radius:var(--ha-dialog-border-radius,28px)}:host([flexContent]) .mdc-dialog .mdc-dialog__content{display:flex;flex-direction:column}.header_title{margin-right:32px;margin-inline-end:32px;margin-inline-start:initial;direction:var(--direction)}.header_button{position:absolute;right:16px;top:14px;text-decoration:none;color:inherit;inset-inline-start:initial;inset-inline-end:16px;direction:var(--direction)}.dialog-actions{inset-inline-start:initial!important;inset-inline-end:0px!important;direction:var(--direction)}`]}]}}),s.M)},81312:(e,t,a)=>{var i=a(17463),o=a(34541),n=a(47838),s=a(68144),r=a(79932),d=a(47181),c=a(38346),l=a(49594),h=a(82160),f=a(50424);const u=JSON.parse('{"version":"7.3.67","parts":[{"file":"58ce751bfb601c28addea4dbdfee24226e4e26b1"},{"start":"account-switch-","file":"6fe9065fea10add5c0c6e48354166d037ac50b20"},{"start":"alpha-t-c","file":"d7d106c388bfda2f151cc05b575c6407a2321358"},{"start":"arrow-down-box","file":"07d46da6788757104d63cc6dfd69a5574fa9ea0e"},{"start":"bac","file":"a69c2429be94dc38246377a9f0b8bb0d7208c49a"},{"start":"battery-mi","file":"a4bd09088298857870205aad48d71ef5ecf14162"},{"start":"bo","file":"ea1b8f25379b641ca6ab4a89b3bb012a1898f125"},{"start":"briefcase-d","file":"a488fc5c297ba0d1eab0b7550c859ba5eb332d64"},{"start":"calendar-st","file":"a0916c7eca5a3e1154f040f8e1131481f554470b"},{"start":"car-ou","file":"4530f3f42b83c2fd05d41beb9ed32394dd236b86"},{"start":"cellphone-me","file":"18001e19a5b2dc0aa3829423dbe7a8cfcb3faedf"},{"start":"city-variant-","file":"8cf347559af0ec77cb1a1fbc9cf4f26c71e199a2"},{"start":"cloud-d","file":"aa0ca15dca285dcaf2d68fc1905a5886bff8e737"},{"start":"cog-sync-","file":"12d257426150b4727a785f64ace3cda63ad0837d"},{"start":"cookie-o","file":"e9a86cfd4033dbb9152bc25846a327e0272f8867"},{"start":"currency-tr","file":"5131d4536a8d7f548abb80d0ce20e6b8ef3da456"},{"start":"det","file":"d84e77bed2fec3dded9590d3a223f90a77850404"},{"start":"e","file":"c50a17e014e7dc1dda66612c9f4262e362046942"},{"start":"emoticon-r","file":"fa93bbb9f394ae9dad00dd24d63b2b8abc51eb57"},{"start":"fan-o","file":"fcf07b2bb103855d7881ea7785be0d9356a91169"},{"start":"file-set","file":"9e3206e4b3fc6a9516d852501f2a0f2d87dc38be"},{"start":"flip-t","file":"b732f8191887ed827ee9522c5be6e2b313d41a93"},{"start":"football-h","file":"a2953da9f03edc844d932976096ab3d6bb700b03"},{"start":"gas-station-","file":"5e9382d02a8816f0580987453669f4984e890764"},{"start":"google-s","file":"7fbeae05187b80048f4e6c8b15b417b8b915f31e"},{"start":"head-l","file":"6a014f724c5e039ebab09a43fda1b86b0a6d5b60"},{"start":"home-v","file":"a9431e7dae87b1867647a2f84c24c587aace2901"},{"start":"incognito-o","file":"43bf39792d61eb1233b56e4c27063ba787a6abc3"},{"start":"l","file":"be619036639cbb2a4eeee0ec39f4d180e8b1b61b"},{"start":"lightbulb-night-","file":"341f70f7b271dfb175d02bf888b28d235a4e76c5"},{"start":"map-clock-","file":"5415140032324eb36efbb9ff4a1c1620e1e09cee"},{"start":"microsoft-p","file":"2b3ac173c56a374495f6832c5bba32ae886e6cff"},{"start":"movie-open-plu","file":"a748347ba838db9f493261933486ee2b5ab8edb6"},{"start":"numeric-10-c","file":"137c0b16170d81671cd5515981f45eb52f661fd9"},{"start":"palette-s","file":"5de2e50c3ff206321071caf8d66f586be45bb9eb"},{"start":"phone-bluetooth-","file":"f634d315e85b52f05338ef94afa5e177506646e6"},{"start":"podi","file":"40f323ce90754fd2fe1ae5943ede7eec7cd415d8"},{"start":"puzzle-heart-","file":"96951c0eed3f62d2b9e964426dc5b62c3a9a66f8"},{"start":"relation-only-one-to-zero-or-o","file":"e256296bf39da5bdf1542ade4bbf8c7787d0c771"},{"start":"run","file":"63c07fd3a05a51a8ee8793a9493003ab03a55b26"},{"start":"set-left-","file":"3f22521dc9253cfc8b6d5e27e572a54a947006db"},{"start":"size-xxs","file":"8f8ad2f98fec00bb74b733c7f3104c0bf54451c5"},{"start":"sort-v","file":"504b0477945091d0dec0a1019ea3e84381d94dd5"},{"start":"sticker-ci","file":"c07c3d33aa7ce443bd3d45dffd88627e778b3bc9"},{"start":"sync","file":"6aaa668c62e648ba83547c2a6a966860dcfabfc4"},{"start":"tex","file":"ca7c219223cc867e80ab379ac7315629a2e75538"},{"start":"timer-st","file":"4ca8681e7117bc34e70f0ad97faee59dfd121cae"},{"start":"truck-ou","file":"015c125a80491ef47bab3cd6c3cd481b20ebf9da"},{"start":"view-d","file":"63b32ed0ba333f1070f0f113cbf4581879e43ebc"},{"start":"weather-night-","file":"555b752999d9858994f4eb2e289a8e7144951ec0"},{"start":"wifi-st","file":"20dbfd4ce7231736e91b0360b85a857d47407ba7"}]}'),p=(0,h.MT)("hass-icon-db","mdi-icon-store"),m=["mdi","hass","hassio","hademo"];let b=[];a(52039);const v={},g={};(async()=>{const e=await(0,h.U2)("_version",p);e?e!==u.version&&(await(0,h.ZH)(p),(0,h.t8)("_version",u.version,p)):(0,h.t8)("_version",u.version,p)})();const y=(0,c.D)((()=>(async e=>{const t=Object.keys(e),a=await Promise.all(Object.values(e));p("readwrite",(i=>{a.forEach(((a,o)=>{Object.entries(a).forEach((([e,t])=>{i.put(t,e)})),delete e[t[o]]}))}))})(g)),2e3),k={};(0,i.Z)([(0,r.Mo)("ha-icon")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,r.Cb)()],key:"icon",value:void 0},{kind:"field",decorators:[(0,r.SB)()],key:"_path",value:void 0},{kind:"field",decorators:[(0,r.SB)()],key:"_secondaryPath",value:void 0},{kind:"field",decorators:[(0,r.SB)()],key:"_viewBox",value:void 0},{kind:"field",decorators:[(0,r.SB)()],key:"_legacy",value:()=>!1},{kind:"method",key:"willUpdate",value:function(e){(0,o.Z)((0,n.Z)(i.prototype),"willUpdate",this).call(this,e),e.has("icon")&&(this._path=void 0,this._secondaryPath=void 0,this._viewBox=void 0,this._loadIcon())}},{kind:"method",key:"render",value:function(){return this.icon?this._legacy?s.dy` <iron-icon .icon="${this.icon}"></iron-icon>`:s.dy`<ha-svg-icon .path="${this._path}" .secondaryPath="${this._secondaryPath}" .viewBox="${this._viewBox}"></ha-svg-icon>`:s.Ld}},{kind:"method",key:"_loadIcon",value:async function(){if(!this.icon)return;const e=this.icon,[t,i]=this.icon.split(":",2);let o,n=i;if(!t||!n)return;if(!m.includes(t)){const a=l.g[t];return a?void(a&&"function"==typeof a.getIcon&&this._setCustomPath(a.getIcon(n),e)):void(this._legacy=!0)}if(this._legacy=!1,n in v){const e=v[n];let a;e.newName?(a=`Icon ${t}:${n} was renamed to ${t}:${e.newName}, please change your config, it will be removed in version ${e.removeIn}.`,n=e.newName):a=`Icon ${t}:${n} was removed from MDI, please replace this icon with an other icon in your config, it will be removed in version ${e.removeIn}.`,console.warn(a),(0,d.B)(this,"write_log",{level:"warning",message:a})}if(n in k)return void(this._path=k[n]);if("home-assistant"===n){const t=(await a.e(30008).then(a.bind(a,30008))).mdiHomeAssistant;return this.icon===e&&(this._path=t),void(k[n]=t)}try{o=await(e=>new Promise(((t,a)=>{b.push([e,t,a]),b.length>1||(0,f.n)(1e3,p("readonly",(e=>{for(const[t,a,i]of b)(0,h.RV)(e.get(t)).then((e=>a(e))).catch((e=>i(e)));b=[]}))).catch((e=>{for(const[,,t]of b)t(e);b=[]}))})))(n)}catch(e){o=void 0}if(o)return this.icon===e&&(this._path=o),void(k[n]=o);const s=(e=>{let t;for(const a of u.parts){if(void 0!==a.start&&e<a.start)break;t=a}return t.file})(n);if(s in g)return void this._setPath(g[s],n,e);const r=fetch(`/static/mdi/${s}.json`).then((e=>e.json()));g[s]=r,this._setPath(r,n,e),y()}},{kind:"method",key:"_setCustomPath",value:async function(e,t){const a=await e;this.icon===t&&(this._path=a.path,this._secondaryPath=a.secondaryPath,this._viewBox=a.viewBox)}},{kind:"method",key:"_setPath",value:async function(e,t,a){const i=await e;this.icon===a&&(this._path=i[t]),k[t]=i[t]}},{kind:"get",static:!0,key:"styles",value:function(){return s.iv`:host{fill:currentcolor}`}}]}}),s.oi)},65189:(e,t,a)=>{var i=a(17463),o=a(68144),n=a(79932),s=a(34541),r=a(47838),d=a(47181),c=a(93217);let l;const h={Note:"info",Warning:"warning"};(0,i.Z)([(0,n.Mo)("ha-markdown-element")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,n.Cb)()],key:"content",value:void 0},{kind:"field",decorators:[(0,n.Cb)({type:Boolean})],key:"allowSvg",value:()=>!1},{kind:"field",decorators:[(0,n.Cb)({type:Boolean})],key:"breaks",value:()=>!1},{kind:"field",decorators:[(0,n.Cb)({type:Boolean,attribute:"lazy-images"})],key:"lazyImages",value:()=>!1},{kind:"method",key:"createRenderRoot",value:function(){return this}},{kind:"method",key:"update",value:function(e){(0,s.Z)((0,r.Z)(i.prototype),"update",this).call(this,e),void 0!==this.content&&this._render()}},{kind:"method",key:"_render",value:async function(){this.innerHTML=await(async(e,t,i)=>(l||(l=(0,c.Ud)(new Worker(new URL(a.p+a.u(71402),a.b),{type:"module"}))),l.renderMarkdown(e,t,i)))(String(this.content),{breaks:this.breaks,gfm:!0},{allowSvg:this.allowSvg}),this._resize();const e=document.createTreeWalker(this,NodeFilter.SHOW_ELEMENT,null);for(;e.nextNode();){const a=e.currentNode;if(a instanceof HTMLAnchorElement&&a.host!==document.location.host)a.target="_blank",a.rel="noreferrer noopener";else if(a instanceof HTMLImageElement)this.lazyImages&&(a.loading="lazy"),a.addEventListener("load",this._resize);else if(a instanceof HTMLQuoteElement){const e=a.firstElementChild,i=null==e?void 0:e.firstElementChild,o=(null==i?void 0:i.textContent)&&h[i.textContent];if("STRONG"===(null==i?void 0:i.nodeName)&&o){var t;const i=document.createElement("ha-alert");i.alertType=o,i.title="#text"===e.childNodes[1].nodeName&&(null===(t=e.childNodes[1].textContent)||void 0===t?void 0:t.trimStart())||"";const n=Array.from(e.childNodes);for(const e of n.slice(n.findIndex((e=>e instanceof HTMLBRElement))+1))i.appendChild(e);a.firstElementChild.replaceWith(i)}}}}},{kind:"field",key:"_resize",value(){return()=>(0,d.B)(this,"content-resize")}}]}}),o.fl);a(9381),a(81312),a(52039);(0,i.Z)([(0,n.Mo)("ha-markdown")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,n.Cb)()],key:"content",value:void 0},{kind:"field",decorators:[(0,n.Cb)({type:Boolean})],key:"allowSvg",value:()=>!1},{kind:"field",decorators:[(0,n.Cb)({type:Boolean})],key:"breaks",value:()=>!1},{kind:"field",decorators:[(0,n.Cb)({type:Boolean,attribute:"lazy-images"})],key:"lazyImages",value:()=>!1},{kind:"method",key:"render",value:function(){return this.content?o.dy`<ha-markdown-element .content="${this.content}" .allowSvg="${this.allowSvg}" .breaks="${this.breaks}" .lazyImages="${this.lazyImages}"></ha-markdown-element>`:o.Ld}},{kind:"get",static:!0,key:"styles",value:function(){return o.iv`:host{display:block}ha-markdown-element{-ms-user-select:text;-webkit-user-select:text;-moz-user-select:text}ha-markdown-element>:first-child{margin-top:0}ha-markdown-element>:last-child{margin-bottom:0}a{color:var(--primary-color)}img{max-width:100%}code,pre{background-color:var(--markdown-code-background-color,none);border-radius:3px}svg{background-color:var(--markdown-svg-background-color,none);color:var(--markdown-svg-color,none)}code{font-size:85%;padding:.2em .4em}pre code{padding:0}pre{padding:16px;overflow:auto;line-height:1.45;font-family:var(--code-font-family, monospace)}h1,h2,h3,h4,h5,h6{line-height:initial}h2{font-size:1.5em;font-weight:700}`}}]}}),o.oi)},49594:(e,t,a)=>{a.d(t,{g:()=>s});const i=window;"customIconsets"in i||(i.customIconsets={});const o=i.customIconsets,n=window;"customIcons"in n||(n.customIcons={});const s=new Proxy(n.customIcons,{get:(e,t)=>{var a;return null!==(a=e[t])&&void 0!==a?a:o[t]?{getIcon:o[t]}:void 0}})},3958:(e,t,a)=>{a.r(t);var i=a(17463),o=a(34541),n=a(47838),s=(a(14271),a(68144)),r=a(79932),d=(a(31206),a(34821),a(68331),a(65189),a(22814)),c=a(11654);let l=0;(0,i.Z)([(0,r.Mo)("ha-mfa-module-setup-flow")],(function(e,t){class a extends t{constructor(...t){super(...t),e(this)}}return{F:a,d:[{kind:"field",decorators:[(0,r.Cb)()],key:"hass",value:void 0},{kind:"field",decorators:[(0,r.SB)()],key:"_dialogClosedCallback",value:void 0},{kind:"field",decorators:[(0,r.SB)()],key:"_instance",value:void 0},{kind:"field",decorators:[(0,r.SB)()],key:"_loading",value:()=>!1},{kind:"field",decorators:[(0,r.SB)()],key:"_opened",value:()=>!1},{kind:"field",decorators:[(0,r.SB)()],key:"_stepData",value:()=>({})},{kind:"field",decorators:[(0,r.SB)()],key:"_step",value:void 0},{kind:"field",decorators:[(0,r.SB)()],key:"_errorMessage",value:void 0},{kind:"method",key:"showDialog",value:function({continueFlowId:e,mfaModuleId:t,dialogClosedCallback:a}){this._instance=l++,this._dialogClosedCallback=a,this._opened=!0;const i=e?this.hass.callWS({type:"auth/setup_mfa",flow_id:e}):this.hass.callWS({type:"auth/setup_mfa",mfa_module_id:t}),o=this._instance;i.then((e=>{o===this._instance&&this._processStep(e)}))}},{kind:"method",key:"closeDialog",value:function(){this._step&&this._flowDone(),this._opened=!1}},{kind:"method",key:"render",value:function(){var e,t;return this._opened?s.dy` <ha-dialog open .heading="${this._computeStepTitle()}" @closed="${this.closeDialog}"> <div> ${this._errorMessage?s.dy`<div class="error">${this._errorMessage}</div>`:""} ${this._step?s.dy`${"abort"===this._step.type?s.dy` <ha-markdown allowsvg breaks .content="${this.hass.localize(`component.auth.mfa_setup.${this._step.handler}.abort.${this._step.reason}`)}"></ha-markdown>`:"create_entry"===this._step.type?s.dy`<p> ${this.hass.localize("ui.panel.profile.mfa_setup.step_done",{step:this._step.title})} </p>`:"form"===this._step.type?s.dy`<ha-markdown allowsvg breaks .content="${this.hass.localize(`component.auth.mfa_setup.${this._step.handler}.step.${this._step.step_id}.description`,this._step.description_placeholders)}"></ha-markdown> <ha-form .hass="${this.hass}" .data="${this._stepData}" .schema="${(0,d.oT)(this._step.data_schema)}" .error="${this._step.errors}" .computeLabel="${this._computeLabel}" .computeError="${this._computeError}" @value-changed="${this._stepDataChanged}"></ha-form>`:""}`:s.dy`<div class="init-spinner"> <ha-circular-progress indeterminate></ha-circular-progress> </div>`} </div> ${["abort","create_entry"].includes((null===(e=this._step)||void 0===e?void 0:e.type)||"")?s.dy`<mwc-button slot="primaryAction" @click="${this.closeDialog}">${this.hass.localize("ui.panel.profile.mfa_setup.close")}</mwc-button>`:""} ${"form"===(null===(t=this._step)||void 0===t?void 0:t.type)?s.dy`<mwc-button slot="primaryAction" .disabled="${this._loading}" @click="${this._submitStep}">${this.hass.localize("ui.panel.profile.mfa_setup.submit")}</mwc-button>`:""} </ha-dialog> `:s.Ld}},{kind:"get",static:!0,key:"styles",value:function(){return[c.yu,s.iv`.error{color:red}ha-dialog{max-width:500px}ha-markdown{--markdown-svg-background-color:white;--markdown-svg-color:black;display:block;margin:0 auto}ha-markdown a{color:var(--primary-color)}.init-spinner{padding:10px 100px 34px;text-align:center}.submit-spinner{margin-right:16px}`]}},{kind:"method",key:"firstUpdated",value:function(e){(0,o.Z)((0,n.Z)(a.prototype),"firstUpdated",this).call(this,e),this.hass.loadBackendTranslation("mfa_setup","auth"),this.addEventListener("keypress",(e=>{"Enter"===e.key&&this._submitStep()}))}},{kind:"method",key:"_stepDataChanged",value:function(e){this._stepData=e.detail.value}},{kind:"method",key:"_submitStep",value:function(){this._loading=!0,this._errorMessage=void 0;const e=this._instance;this.hass.callWS({type:"auth/setup_mfa",flow_id:this._step.flow_id,user_input:this._stepData}).then((t=>{e===this._instance&&(this._processStep(t),this._loading=!1)}),(e=>{this._errorMessage=e&&e.body&&e.body.message||"Unknown error occurred",this._loading=!1}))}},{kind:"method",key:"_processStep",value:function(e){e.errors||(e.errors={}),this._step=e,0===Object.keys(e.errors).length&&(this._stepData={})}},{kind:"method",key:"_flowDone",value:function(){const e=Boolean(this._step&&["create_entry","abort"].includes(this._step.type));this._dialogClosedCallback({flowFinished:e}),this._errorMessage=void 0,this._step=void 0,this._stepData={},this._dialogClosedCallback=void 0,this.closeDialog()}},{kind:"method",key:"_computeStepTitle",value:function(){var e,t,a;return"abort"===(null===(e=this._step)||void 0===e?void 0:e.type)?this.hass.localize("ui.panel.profile.mfa_setup.title_aborted"):"create_entry"===(null===(t=this._step)||void 0===t?void 0:t.type)?this.hass.localize("ui.panel.profile.mfa_setup.title_success"):"form"===(null===(a=this._step)||void 0===a?void 0:a.type)?this.hass.localize(`component.auth.mfa_setup.${this._step.handler}.step.${this._step.step_id}.title`):""}},{kind:"field",key:"_computeLabel",value(){return e=>this.hass.localize(`component.auth.mfa_setup.${this._step.handler}.step.${this._step.step_id}.data.${e.name}`)||e.name}},{kind:"field",key:"_computeError",value(){return e=>this.hass.localize(`component.auth.mfa_setup.${this._step.handler}.error.${e}`)||e}}]}}),s.oi)},93217:(e,t,a)=>{a.d(t,{Ud:()=>f});const i=Symbol("Comlink.proxy"),o=Symbol("Comlink.endpoint"),n=Symbol("Comlink.releaseProxy"),s=Symbol("Comlink.finalizer"),r=Symbol("Comlink.thrown"),d=e=>"object"==typeof e&&null!==e||"function"==typeof e,c=new Map([["proxy",{canHandle:e=>d(e)&&e[i],serialize(e){const{port1:t,port2:a}=new MessageChannel;return l(e,t),[a,[a]]},deserialize:e=>(e.start(),f(e))}],["throw",{canHandle:e=>d(e)&&r in e,serialize({value:e}){let t;return t=e instanceof Error?{isError:!0,value:{message:e.message,name:e.name,stack:e.stack}}:{isError:!1,value:e},[t,[]]},deserialize(e){if(e.isError)throw Object.assign(new Error(e.value.message),e.value);throw e.value}}]]);function l(e,t=globalThis,a=["*"]){t.addEventListener("message",(function o(n){if(!n||!n.data)return;if(!function(e,t){for(const a of e){if(t===a||"*"===a)return!0;if(a instanceof RegExp&&a.test(t))return!0}return!1}(a,n.origin))return void console.warn(`Invalid origin '${n.origin}' for comlink proxy`);const{id:d,type:c,path:f}=Object.assign({path:[]},n.data),u=(n.data.argumentList||[]).map(_);let p;try{const t=f.slice(0,-1).reduce(((e,t)=>e[t]),e),a=f.reduce(((e,t)=>e[t]),e);switch(c){case"GET":p=a;break;case"SET":t[f.slice(-1)[0]]=_(n.data.value),p=!0;break;case"APPLY":p=a.apply(t,u);break;case"CONSTRUCT":p=function(e){return Object.assign(e,{[i]:!0})}(new a(...u));break;case"ENDPOINT":{const{port1:t,port2:a}=new MessageChannel;l(e,a),p=function(e,t){return y.set(e,t),e}(t,[t])}break;case"RELEASE":p=void 0;break;default:return}}catch(e){p={value:e,[r]:0}}Promise.resolve(p).catch((e=>({value:e,[r]:0}))).then((a=>{const[i,n]=k(a);t.postMessage(Object.assign(Object.assign({},i),{id:d}),n),"RELEASE"===c&&(t.removeEventListener("message",o),h(t),s in e&&"function"==typeof e[s]&&e[s]())})).catch((e=>{const[a,i]=k({value:new TypeError("Unserializable return value"),[r]:0});t.postMessage(Object.assign(Object.assign({},a),{id:d}),i)}))})),t.start&&t.start()}function h(e){(function(e){return"MessagePort"===e.constructor.name})(e)&&e.close()}function f(e,t){return v(e,[],t)}function u(e){if(e)throw new Error("Proxy has been released and is not useable")}function p(e){return w(e,{type:"RELEASE"}).then((()=>{h(e)}))}const m=new WeakMap,b="FinalizationRegistry"in globalThis&&new FinalizationRegistry((e=>{const t=(m.get(e)||0)-1;m.set(e,t),0===t&&p(e)}));function v(e,t=[],a=function(){}){let i=!1;const s=new Proxy(a,{get(a,o){if(u(i),o===n)return()=>{!function(e){b&&b.unregister(e)}(s),p(e),i=!0};if("then"===o){if(0===t.length)return{then:()=>s};const a=w(e,{type:"GET",path:t.map((e=>e.toString()))}).then(_);return a.then.bind(a)}return v(e,[...t,o])},set(a,o,n){u(i);const[s,r]=k(n);return w(e,{type:"SET",path:[...t,o].map((e=>e.toString())),value:s},r).then(_)},apply(a,n,s){u(i);const r=t[t.length-1];if(r===o)return w(e,{type:"ENDPOINT"}).then(_);if("bind"===r)return v(e,t.slice(0,-1));const[d,c]=g(s);return w(e,{type:"APPLY",path:t.map((e=>e.toString())),argumentList:d},c).then(_)},construct(a,o){u(i);const[n,s]=g(o);return w(e,{type:"CONSTRUCT",path:t.map((e=>e.toString())),argumentList:n},s).then(_)}});return function(e,t){const a=(m.get(t)||0)+1;m.set(t,a),b&&b.register(e,t,e)}(s,e),s}function g(e){const t=e.map(k);return[t.map((e=>e[0])),(a=t.map((e=>e[1])),Array.prototype.concat.apply([],a))];var a}const y=new WeakMap;function k(e){for(const[t,a]of c)if(a.canHandle(e)){const[i,o]=a.serialize(e);return[{type:"HANDLER",name:t,value:i},o]}return[{type:"RAW",value:e},y.get(e)||[]]}function _(e){switch(e.type){case"HANDLER":return c.get(e.name).deserialize(e.value);case"RAW":return e.value}}function w(e,t,a){return new Promise((i=>{const o=new Array(4).fill(0).map((()=>Math.floor(Math.random()*Number.MAX_SAFE_INTEGER).toString(16))).join("-");e.addEventListener("message",(function t(a){a.data&&a.data.id&&a.data.id===o&&(e.removeEventListener("message",t),i(a.data))})),e.start&&e.start(),e.postMessage(Object.assign({id:o},t),a)}))}},82160:(e,t,a)=>{function i(e){return new Promise(((t,a)=>{e.oncomplete=e.onsuccess=()=>t(e.result),e.onabort=e.onerror=()=>a(e.error)}))}function o(e,t){const a=indexedDB.open(e);a.onupgradeneeded=()=>a.result.createObjectStore(t);const o=i(a);return(e,a)=>o.then((i=>a(i.transaction(t,e).objectStore(t))))}let n;function s(){return n||(n=o("keyval-store","keyval")),n}function r(e,t=s()){return t("readonly",(t=>i(t.get(e))))}function d(e,t,a=s()){return a("readwrite",(a=>(a.put(t,e),i(a.transaction))))}function c(e=s()){return e("readwrite",(e=>(e.clear(),i(e.transaction))))}a.d(t,{MT:()=>o,RV:()=>i,U2:()=>r,ZH:()=>c,t8:()=>d})}};
//# sourceMappingURL=94985.1ryRK2Pp8lI.js.map