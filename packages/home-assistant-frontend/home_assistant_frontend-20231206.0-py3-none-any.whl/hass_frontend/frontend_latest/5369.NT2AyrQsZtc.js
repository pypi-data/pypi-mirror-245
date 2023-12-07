export const id=5369;export const ids=[5369];export const modules={32594:(e,t,i)=>{i.d(t,{U:()=>a});const a=e=>e.stopPropagation()},50424:(e,t,i)=>{i.d(t,{n:()=>a});const a=(e,t)=>{const i=new Promise(((t,i)=>{setTimeout((()=>{i(`Timed out in ${e} ms.`)}),e)}));return Promise.race([t,i])}},9381:(e,t,i)=>{var a=i(17463),o=i(68144),s=i(79932),r=i(83448),n=i(47181);i(10983),i(52039);const l={info:"M11,9H13V7H11M12,20C7.59,20 4,16.41 4,12C4,7.59 7.59,4 12,4C16.41,4 20,7.59 20,12C20,16.41 16.41,20 12,20M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M11,17H13V11H11V17Z",warning:"M12,2L1,21H23M12,6L19.53,19H4.47M11,10V14H13V10M11,16V18H13V16",error:"M11,15H13V17H11V15M11,7H13V13H11V7M12,2C6.47,2 2,6.5 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M12,20A8,8 0 0,1 4,12A8,8 0 0,1 12,4A8,8 0 0,1 20,12A8,8 0 0,1 12,20Z",success:"M20,12A8,8 0 0,1 12,20A8,8 0 0,1 4,12A8,8 0 0,1 12,4C12.76,4 13.5,4.11 14.2,4.31L15.77,2.74C14.61,2.26 13.34,2 12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12M7.91,10.08L6.5,11.5L11,16L21,6L19.59,4.58L11,13.17L7.91,10.08Z"};(0,a.Z)([(0,s.Mo)("ha-alert")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,s.Cb)()],key:"title",value:()=>""},{kind:"field",decorators:[(0,s.Cb)({attribute:"alert-type"})],key:"alertType",value:()=>"info"},{kind:"field",decorators:[(0,s.Cb)({type:Boolean})],key:"dismissable",value:()=>!1},{kind:"method",key:"render",value:function(){return o.dy` <div class="issue-type ${(0,r.$)({[this.alertType]:!0})}" role="alert"> <div class="icon ${this.title?"":"no-title"}"> <slot name="icon"> <ha-svg-icon .path="${l[this.alertType]}"></ha-svg-icon> </slot> </div> <div class="content"> <div class="main-content"> ${this.title?o.dy`<div class="title">${this.title}</div>`:""} <slot></slot> </div> <div class="action"> <slot name="action"> ${this.dismissable?o.dy`<ha-icon-button @click="${this._dismiss_clicked}" label="Dismiss alert" .path="${"M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z"}"></ha-icon-button>`:""} </slot> </div> </div> </div> `}},{kind:"method",key:"_dismiss_clicked",value:function(){(0,n.B)(this,"alert-dismissed-clicked")}},{kind:"field",static:!0,key:"styles",value:()=>o.iv`.issue-type{position:relative;padding:8px;display:flex}.issue-type::after{position:absolute;top:0;right:0;bottom:0;left:0;opacity:.12;pointer-events:none;content:"";border-radius:4px}.icon{z-index:1}.icon.no-title{align-self:center}.content{display:flex;justify-content:space-between;align-items:center;width:100%;text-align:var(--float-start)}.action{z-index:1;width:min-content;--mdc-theme-primary:var(--primary-text-color)}.main-content{overflow-wrap:anywhere;word-break:break-word;margin-left:8px;margin-right:0;margin-inline-start:8px;margin-inline-end:0;direction:var(--direction)}.title{margin-top:2px;font-weight:700}.action ha-icon-button,.action mwc-button{--mdc-theme-primary:var(--primary-text-color);--mdc-icon-button-size:36px}.issue-type.info>.icon{color:var(--info-color)}.issue-type.info::after{background-color:var(--info-color)}.issue-type.warning>.icon{color:var(--warning-color)}.issue-type.warning::after{background-color:var(--warning-color)}.issue-type.error>.icon{color:var(--error-color)}.issue-type.error::after{background-color:var(--error-color)}.issue-type.success>.icon{color:var(--success-color)}.issue-type.success::after{background-color:var(--success-color)}`}]}}),o.oi)},31206:(e,t,i)=>{i.r(t),i.d(t,{HaCircularProgress:()=>d});var a=i(17463),o=i(34541),s=i(47838),r=(i(34131),i(22129)),n=i(68144),l=i(79932);let d=(0,a.Z)([(0,l.Mo)("ha-circular-progress")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,l.Cb)({attribute:"aria-label",type:String})],key:"ariaLabel",value:()=>"Loading"},{kind:"field",decorators:[(0,l.Cb)()],key:"size",value:()=>"medium"},{kind:"method",key:"updated",value:function(e){if((0,o.Z)((0,s.Z)(i.prototype),"updated",this).call(this,e),e.has("size"))switch(this.size){case"tiny":this.style.setProperty("--md-circular-progress-size","16px");break;case"small":this.style.setProperty("--md-circular-progress-size","28px");break;case"medium":this.style.setProperty("--md-circular-progress-size","48px");break;case"large":this.style.setProperty("--md-circular-progress-size","68px")}}},{kind:"get",static:!0,key:"styles",value:function(){return[...(0,o.Z)((0,s.Z)(i),"styles",this),n.iv`:host{--md-sys-color-primary:var(--primary-color);--md-circular-progress-size:48px}`]}}]}}),r.B)},33753:(e,t,i)=>{var a=i(17463),o=i(34541),s=i(47838),r=i(68144),n=i(79932),l=i(14516),d=i(47181),c=i(32594);i(81312);const h={key:"Mod-s",run:e=>((0,d.B)(e.dom,"editor-save"),!0)},u=e=>{const t=document.createElement("ha-icon");return t.icon=e.label,t};(0,a.Z)([(0,n.Mo)("ha-code-editor")],(function(e,t){class a extends t{constructor(...t){super(...t),e(this)}}return{F:a,d:[{kind:"field",key:"codemirror",value:void 0},{kind:"field",decorators:[(0,n.Cb)()],key:"mode",value:()=>"yaml"},{kind:"field",key:"hass",value:void 0},{kind:"field",decorators:[(0,n.Cb)({type:Boolean})],key:"autofocus",value:()=>!1},{kind:"field",decorators:[(0,n.Cb)({type:Boolean})],key:"readOnly",value:()=>!1},{kind:"field",decorators:[(0,n.Cb)({type:Boolean,attribute:"autocomplete-entities"})],key:"autocompleteEntities",value:()=>!1},{kind:"field",decorators:[(0,n.Cb)({type:Boolean,attribute:"autocomplete-icons"})],key:"autocompleteIcons",value:()=>!1},{kind:"field",decorators:[(0,n.Cb)({type:Boolean})],key:"error",value:()=>!1},{kind:"field",decorators:[(0,n.SB)()],key:"_value",value:()=>""},{kind:"field",key:"_loadedCodeMirror",value:void 0},{kind:"field",key:"_iconList",value:void 0},{kind:"set",key:"value",value:function(e){this._value=e}},{kind:"get",key:"value",value:function(){return this.codemirror?this.codemirror.state.doc.toString():this._value}},{kind:"get",key:"hasComments",value:function(){if(!this.codemirror||!this._loadedCodeMirror)return!1;const e=this._loadedCodeMirror.highlightingFor(this.codemirror.state,[this._loadedCodeMirror.tags.comment]);return!!this.renderRoot.querySelector(`span.${e}`)}},{kind:"method",key:"connectedCallback",value:function(){(0,o.Z)((0,s.Z)(a.prototype),"connectedCallback",this).call(this),this.hasUpdated&&this.requestUpdate(),this.addEventListener("keydown",c.U),this.codemirror&&!1!==this.autofocus&&this.codemirror.focus()}},{kind:"method",key:"disconnectedCallback",value:function(){(0,o.Z)((0,s.Z)(a.prototype),"disconnectedCallback",this).call(this),this.removeEventListener("keydown",c.U),this.updateComplete.then((()=>{this.codemirror.destroy(),delete this.codemirror}))}},{kind:"method",key:"scheduleUpdate",value:async function(){var e;null!==(e=this._loadedCodeMirror)&&void 0!==e||(this._loadedCodeMirror=await Promise.all([i.e(43642),i.e(74561),i.e(92914)]).then(i.bind(i,92914))),(0,o.Z)((0,s.Z)(a.prototype),"scheduleUpdate",this).call(this)}},{kind:"method",key:"update",value:function(e){if((0,o.Z)((0,s.Z)(a.prototype),"update",this).call(this,e),!this.codemirror)return void this._createCodeMirror();const t=[];e.has("mode")&&t.push({effects:this._loadedCodeMirror.langCompartment.reconfigure(this._mode)}),e.has("readOnly")&&t.push({effects:this._loadedCodeMirror.readonlyCompartment.reconfigure(this._loadedCodeMirror.EditorView.editable.of(!this.readOnly))}),e.has("_value")&&this._value!==this.value&&t.push({changes:{from:0,to:this.codemirror.state.doc.length,insert:this._value}}),t.length>0&&this.codemirror.dispatch(...t),e.has("error")&&this.classList.toggle("error-state",this.error)}},{kind:"get",key:"_mode",value:function(){return this._loadedCodeMirror.langs[this.mode]}},{kind:"method",key:"_createCodeMirror",value:function(){if(!this._loadedCodeMirror)throw new Error("Cannot create editor before CodeMirror is loaded");const e=[this._loadedCodeMirror.lineNumbers(),this._loadedCodeMirror.history(),this._loadedCodeMirror.drawSelection(),this._loadedCodeMirror.EditorState.allowMultipleSelections.of(!0),this._loadedCodeMirror.rectangularSelection(),this._loadedCodeMirror.crosshairCursor(),this._loadedCodeMirror.highlightSelectionMatches(),this._loadedCodeMirror.highlightActiveLine(),this._loadedCodeMirror.keymap.of([...this._loadedCodeMirror.defaultKeymap,...this._loadedCodeMirror.searchKeymap,...this._loadedCodeMirror.historyKeymap,...this._loadedCodeMirror.tabKeyBindings,h]),this._loadedCodeMirror.langCompartment.of(this._mode),this._loadedCodeMirror.haTheme,this._loadedCodeMirror.haSyntaxHighlighting,this._loadedCodeMirror.readonlyCompartment.of(this._loadedCodeMirror.EditorView.editable.of(!this.readOnly)),this._loadedCodeMirror.EditorView.updateListener.of(this._onUpdate)];if(!this.readOnly){const t=[];this.autocompleteEntities&&this.hass&&t.push(this._entityCompletions.bind(this)),this.autocompleteIcons&&t.push(this._mdiCompletions.bind(this)),t.length>0&&e.push(this._loadedCodeMirror.autocompletion({override:t,maxRenderedOptions:10}))}this.codemirror=new this._loadedCodeMirror.EditorView({state:this._loadedCodeMirror.EditorState.create({doc:this._value,extensions:e}),parent:this.renderRoot})}},{kind:"field",key:"_getStates",value:()=>(0,l.Z)((e=>{if(!e)return[];return Object.keys(e).map((t=>({type:"variable",label:t,detail:e[t].attributes.friendly_name,info:`State: ${e[t].state}`})))}))},{kind:"method",key:"_entityCompletions",value:function(e){const t=e.matchBefore(/[a-z_]{3,}\.\w*/);if(!t||t.from===t.to&&!e.explicit)return null;const i=this._getStates(this.hass.states);return i&&i.length?{from:Number(t.from),options:i,validFor:/^[a-z_]{3,}\.\w*$/}:null}},{kind:"field",key:"_getIconItems",value(){return async()=>{if(!this._iconList){let e;e=(await i.e(71639).then(i.t.bind(i,71639,19))).default,this._iconList=e.map((e=>({type:"variable",label:`mdi:${e.name}`,detail:e.keywords.join(", "),info:u})))}return this._iconList}}},{kind:"method",key:"_mdiCompletions",value:async function(e){const t=e.matchBefore(/mdi:\S*/);if(!t||t.from===t.to&&!e.explicit)return null;const i=await this._getIconItems();return{from:Number(t.from),options:i,validFor:/^mdi:\S*$/}}},{kind:"field",key:"_onUpdate",value(){return e=>{e.docChanged&&(this._value=e.state.doc.toString(),(0,d.B)(this,"value-changed",{value:this._value}))}}},{kind:"get",static:!0,key:"styles",value:function(){return r.iv`:host(.error-state) .cm-gutters{border-color:var(--error-state-color,red)}`}}]}}),r.fl)},81312:(e,t,i)=>{var a=i(17463),o=i(34541),s=i(47838),r=i(68144),n=i(79932),l=i(47181),d=i(38346),c=i(49594),h=i(82160),u=i(50424);const f=JSON.parse('{"version":"7.3.67","parts":[{"file":"58ce751bfb601c28addea4dbdfee24226e4e26b1"},{"start":"account-switch-","file":"6fe9065fea10add5c0c6e48354166d037ac50b20"},{"start":"alpha-t-c","file":"d7d106c388bfda2f151cc05b575c6407a2321358"},{"start":"arrow-down-box","file":"07d46da6788757104d63cc6dfd69a5574fa9ea0e"},{"start":"bac","file":"a69c2429be94dc38246377a9f0b8bb0d7208c49a"},{"start":"battery-mi","file":"a4bd09088298857870205aad48d71ef5ecf14162"},{"start":"bo","file":"ea1b8f25379b641ca6ab4a89b3bb012a1898f125"},{"start":"briefcase-d","file":"a488fc5c297ba0d1eab0b7550c859ba5eb332d64"},{"start":"calendar-st","file":"a0916c7eca5a3e1154f040f8e1131481f554470b"},{"start":"car-ou","file":"4530f3f42b83c2fd05d41beb9ed32394dd236b86"},{"start":"cellphone-me","file":"18001e19a5b2dc0aa3829423dbe7a8cfcb3faedf"},{"start":"city-variant-","file":"8cf347559af0ec77cb1a1fbc9cf4f26c71e199a2"},{"start":"cloud-d","file":"aa0ca15dca285dcaf2d68fc1905a5886bff8e737"},{"start":"cog-sync-","file":"12d257426150b4727a785f64ace3cda63ad0837d"},{"start":"cookie-o","file":"e9a86cfd4033dbb9152bc25846a327e0272f8867"},{"start":"currency-tr","file":"5131d4536a8d7f548abb80d0ce20e6b8ef3da456"},{"start":"det","file":"d84e77bed2fec3dded9590d3a223f90a77850404"},{"start":"e","file":"c50a17e014e7dc1dda66612c9f4262e362046942"},{"start":"emoticon-r","file":"fa93bbb9f394ae9dad00dd24d63b2b8abc51eb57"},{"start":"fan-o","file":"fcf07b2bb103855d7881ea7785be0d9356a91169"},{"start":"file-set","file":"9e3206e4b3fc6a9516d852501f2a0f2d87dc38be"},{"start":"flip-t","file":"b732f8191887ed827ee9522c5be6e2b313d41a93"},{"start":"football-h","file":"a2953da9f03edc844d932976096ab3d6bb700b03"},{"start":"gas-station-","file":"5e9382d02a8816f0580987453669f4984e890764"},{"start":"google-s","file":"7fbeae05187b80048f4e6c8b15b417b8b915f31e"},{"start":"head-l","file":"6a014f724c5e039ebab09a43fda1b86b0a6d5b60"},{"start":"home-v","file":"a9431e7dae87b1867647a2f84c24c587aace2901"},{"start":"incognito-o","file":"43bf39792d61eb1233b56e4c27063ba787a6abc3"},{"start":"l","file":"be619036639cbb2a4eeee0ec39f4d180e8b1b61b"},{"start":"lightbulb-night-","file":"341f70f7b271dfb175d02bf888b28d235a4e76c5"},{"start":"map-clock-","file":"5415140032324eb36efbb9ff4a1c1620e1e09cee"},{"start":"microsoft-p","file":"2b3ac173c56a374495f6832c5bba32ae886e6cff"},{"start":"movie-open-plu","file":"a748347ba838db9f493261933486ee2b5ab8edb6"},{"start":"numeric-10-c","file":"137c0b16170d81671cd5515981f45eb52f661fd9"},{"start":"palette-s","file":"5de2e50c3ff206321071caf8d66f586be45bb9eb"},{"start":"phone-bluetooth-","file":"f634d315e85b52f05338ef94afa5e177506646e6"},{"start":"podi","file":"40f323ce90754fd2fe1ae5943ede7eec7cd415d8"},{"start":"puzzle-heart-","file":"96951c0eed3f62d2b9e964426dc5b62c3a9a66f8"},{"start":"relation-only-one-to-zero-or-o","file":"e256296bf39da5bdf1542ade4bbf8c7787d0c771"},{"start":"run","file":"63c07fd3a05a51a8ee8793a9493003ab03a55b26"},{"start":"set-left-","file":"3f22521dc9253cfc8b6d5e27e572a54a947006db"},{"start":"size-xxs","file":"8f8ad2f98fec00bb74b733c7f3104c0bf54451c5"},{"start":"sort-v","file":"504b0477945091d0dec0a1019ea3e84381d94dd5"},{"start":"sticker-ci","file":"c07c3d33aa7ce443bd3d45dffd88627e778b3bc9"},{"start":"sync","file":"6aaa668c62e648ba83547c2a6a966860dcfabfc4"},{"start":"tex","file":"ca7c219223cc867e80ab379ac7315629a2e75538"},{"start":"timer-st","file":"4ca8681e7117bc34e70f0ad97faee59dfd121cae"},{"start":"truck-ou","file":"015c125a80491ef47bab3cd6c3cd481b20ebf9da"},{"start":"view-d","file":"63b32ed0ba333f1070f0f113cbf4581879e43ebc"},{"start":"weather-night-","file":"555b752999d9858994f4eb2e289a8e7144951ec0"},{"start":"wifi-st","file":"20dbfd4ce7231736e91b0360b85a857d47407ba7"}]}'),p=(0,h.MT)("hass-icon-db","mdi-icon-store"),m=["mdi","hass","hassio","hademo"];let b=[];i(52039);const v={},y={};(async()=>{const e=await(0,h.U2)("_version",p);e?e!==f.version&&(await(0,h.ZH)(p),(0,h.t8)("_version",f.version,p)):(0,h.t8)("_version",f.version,p)})();const _=(0,d.D)((()=>(async e=>{const t=Object.keys(e),i=await Promise.all(Object.values(e));p("readwrite",(a=>{i.forEach(((i,o)=>{Object.entries(i).forEach((([e,t])=>{a.put(t,e)})),delete e[t[o]]}))}))})(y)),2e3),k={};(0,a.Z)([(0,n.Mo)("ha-icon")],(function(e,t){class a extends t{constructor(...t){super(...t),e(this)}}return{F:a,d:[{kind:"field",decorators:[(0,n.Cb)()],key:"icon",value:void 0},{kind:"field",decorators:[(0,n.SB)()],key:"_path",value:void 0},{kind:"field",decorators:[(0,n.SB)()],key:"_secondaryPath",value:void 0},{kind:"field",decorators:[(0,n.SB)()],key:"_viewBox",value:void 0},{kind:"field",decorators:[(0,n.SB)()],key:"_legacy",value:()=>!1},{kind:"method",key:"willUpdate",value:function(e){(0,o.Z)((0,s.Z)(a.prototype),"willUpdate",this).call(this,e),e.has("icon")&&(this._path=void 0,this._secondaryPath=void 0,this._viewBox=void 0,this._loadIcon())}},{kind:"method",key:"render",value:function(){return this.icon?this._legacy?r.dy` <iron-icon .icon="${this.icon}"></iron-icon>`:r.dy`<ha-svg-icon .path="${this._path}" .secondaryPath="${this._secondaryPath}" .viewBox="${this._viewBox}"></ha-svg-icon>`:r.Ld}},{kind:"method",key:"_loadIcon",value:async function(){if(!this.icon)return;const e=this.icon,[t,a]=this.icon.split(":",2);let o,s=a;if(!t||!s)return;if(!m.includes(t)){const i=c.g[t];return i?void(i&&"function"==typeof i.getIcon&&this._setCustomPath(i.getIcon(s),e)):void(this._legacy=!0)}if(this._legacy=!1,s in v){const e=v[s];let i;e.newName?(i=`Icon ${t}:${s} was renamed to ${t}:${e.newName}, please change your config, it will be removed in version ${e.removeIn}.`,s=e.newName):i=`Icon ${t}:${s} was removed from MDI, please replace this icon with an other icon in your config, it will be removed in version ${e.removeIn}.`,console.warn(i),(0,l.B)(this,"write_log",{level:"warning",message:i})}if(s in k)return void(this._path=k[s]);if("home-assistant"===s){const t=(await i.e(30008).then(i.bind(i,30008))).mdiHomeAssistant;return this.icon===e&&(this._path=t),void(k[s]=t)}try{o=await(e=>new Promise(((t,i)=>{b.push([e,t,i]),b.length>1||(0,u.n)(1e3,p("readonly",(e=>{for(const[t,i,a]of b)(0,h.RV)(e.get(t)).then((e=>i(e))).catch((e=>a(e)));b=[]}))).catch((e=>{for(const[,,t]of b)t(e);b=[]}))})))(s)}catch(e){o=void 0}if(o)return this.icon===e&&(this._path=o),void(k[s]=o);const r=(e=>{let t;for(const i of f.parts){if(void 0!==i.start&&e<i.start)break;t=i}return t.file})(s);if(r in y)return void this._setPath(y[r],s,e);const n=fetch(`/static/mdi/${r}.json`).then((e=>e.json()));y[r]=n,this._setPath(n,s,e),_()}},{kind:"method",key:"_setCustomPath",value:async function(e,t){const i=await e;this.icon===t&&(this._path=i.path,this._secondaryPath=i.secondaryPath,this._viewBox=i.viewBox)}},{kind:"method",key:"_setPath",value:async function(e,t,i){const a=await e;this.icon===i&&(this._path=a[t]),k[t]=a[t]}},{kind:"get",static:!0,key:"styles",value:function(){return r.iv`:host{fill:currentcolor}`}}]}}),r.oi)},49594:(e,t,i)=>{i.d(t,{g:()=>r});const a=window;"customIconsets"in a||(a.customIconsets={});const o=a.customIconsets,s=window;"customIcons"in s||(s.customIcons={});const r=new Proxy(s.customIcons,{get:(e,t)=>{var i;return null!==(i=e[t])&&void 0!==i?i:o[t]?{getIcon:o[t]}:void 0}})},17324:(e,t,i)=>{i.d(t,{N:()=>a,Z:()=>o});const a=(e,t,i)=>e.subscribeMessage((e=>t(e)),{type:"render_template",...i}),o=(e,t,i,a,o)=>e.connection.subscribeMessage(o,{type:"template/start_preview",flow_id:t,flow_type:i,user_input:a})},5369:(e,t,i)=>{i.r(t);var a=i(17463),o=i(34541),s=i(47838),r=(i(14271),i(68144)),n=i(79932),l=i(83448),d=i(38346),c=(i(9381),i(31206),i(33753),i(17324)),h=i(26765),u=i(11654),f=i(27322);const p='{## Imitate available variables: ##}\n{% set my_test_json = {\n  "temperature": 25,\n  "unit": "°C"\n} %}\n\nThe temperature is {{ my_test_json.temperature }} {{ my_test_json.unit }}.\n\n{% if is_state("sun.sun", "above_horizon") -%}\n  The sun rose {{ relative_time(states.sun.sun.last_changed) }} ago.\n{%- else -%}\n  The sun will rise at {{ as_timestamp(state_attr("sun.sun", "next_rising")) | timestamp_local }}.\n{%- endif %}\n\nFor loop example getting entity values in the weather domain:\n\n{% for state in states.weather -%}\n  {%- if loop.first %}The {% elif loop.last %} and the {% else %}, the {% endif -%}\n  {{ state.name | lower }} is {{state.state_with_unit}}\n{%- endfor %}.';(0,a.Z)([(0,n.Mo)("developer-tools-template")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,n.Cb)()],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.Cb)()],key:"narrow",value:void 0},{kind:"field",decorators:[(0,n.SB)()],key:"_error",value:void 0},{kind:"field",decorators:[(0,n.SB)()],key:"_errorLevel",value:void 0},{kind:"field",decorators:[(0,n.SB)()],key:"_rendering",value:()=>!1},{kind:"field",decorators:[(0,n.SB)()],key:"_templateResult",value:void 0},{kind:"field",decorators:[(0,n.SB)()],key:"_unsubRenderTemplate",value:void 0},{kind:"field",key:"_template",value:()=>""},{kind:"field",key:"_inited",value:()=>!1},{kind:"method",key:"connectedCallback",value:function(){(0,o.Z)((0,s.Z)(i.prototype),"connectedCallback",this).call(this),this._template&&!this._unsubRenderTemplate&&this._subscribeTemplate()}},{kind:"method",key:"disconnectedCallback",value:function(){(0,o.Z)((0,s.Z)(i.prototype),"disconnectedCallback",this).call(this),this._unsubscribeTemplate()}},{kind:"method",key:"firstUpdated",value:function(){localStorage&&localStorage["panel-dev-template-template"]?this._template=localStorage["panel-dev-template-template"]:this._template=p,this._subscribeTemplate(),this._inited=!0}},{kind:"method",key:"render",value:function(){var e,t,i;const a=typeof(null===(e=this._templateResult)||void 0===e?void 0:e.result),o="object"===a?Array.isArray(null===(t=this._templateResult)||void 0===t?void 0:t.result)?"list":"dict":a;return r.dy` <div class="content ${(0,l.$)({layout:!this.narrow,horizontal:!this.narrow})}"> <div class="edit-pane"> <p> ${this.hass.localize("ui.panel.developer-tools.tabs.templates.description")} </p> <ul> <li> <a href="https://jinja.palletsprojects.com/en/latest/templates/" target="_blank" rel="noreferrer">${this.hass.localize("ui.panel.developer-tools.tabs.templates.jinja_documentation")} </a> </li> <li> <a href="${(0,f.R)(this.hass,"/docs/configuration/templating/")}" target="_blank" rel="noreferrer"> ${this.hass.localize("ui.panel.developer-tools.tabs.templates.template_extensions")}</a> </li> </ul> <p> ${this.hass.localize("ui.panel.developer-tools.tabs.templates.editor")} </p> <ha-code-editor mode="jinja2" .hass="${this.hass}" .value="${this._template}" .error="${this._error}" autofocus autocomplete-entities autocomplete-icons @value-changed="${this._templateChanged}" dir="ltr"></ha-code-editor> <mwc-button @click="${this._restoreDemo}"> ${this.hass.localize("ui.panel.developer-tools.tabs.templates.reset")} </mwc-button> <mwc-button @click="${this._clear}"> ${this.hass.localize("ui.common.clear")} </mwc-button> </div> <div class="render-pane"> ${this._rendering?r.dy`<ha-circular-progress class="render-spinner" indeterminate size="small"></ha-circular-progress>`:""} ${this._error?r.dy`<ha-alert alert-type="${(null===(i=this._errorLevel)||void 0===i?void 0:i.toLowerCase())||"error"}">${this._error}</ha-alert>`:r.Ld} ${this._templateResult?r.dy`${this.hass.localize("ui.panel.developer-tools.tabs.templates.result_type")}: ${o} <pre class="rendered ${(0,l.$)({[o]:o})}">${"object"===a?JSON.stringify(this._templateResult.result,null,2):this._templateResult.result}</pre> ${this._templateResult.listeners.time?r.dy` <p> ${this.hass.localize("ui.panel.developer-tools.tabs.templates.time")} </p> `:""} ${this._templateResult.listeners?this._templateResult.listeners.all?r.dy` <p class="all_listeners"> ${this.hass.localize("ui.panel.developer-tools.tabs.templates.all_listeners")} </p> `:this._templateResult.listeners.domains.length||this._templateResult.listeners.entities.length?r.dy` <p> ${this.hass.localize("ui.panel.developer-tools.tabs.templates.listeners")} </p> <ul> ${this._templateResult.listeners.domains.sort().map((e=>r.dy` <li> <b>${this.hass.localize("ui.panel.developer-tools.tabs.templates.domain")}</b>: ${e} </li> `))} ${this._templateResult.listeners.entities.sort().map((e=>r.dy` <li> <b>${this.hass.localize("ui.panel.developer-tools.tabs.templates.entity")}</b>: ${e} </li> `))} </ul> `:this._templateResult.listeners.time?r.Ld:r.dy`<span class="all_listeners"> ${this.hass.localize("ui.panel.developer-tools.tabs.templates.no_listeners")} </span>`:r.Ld}`:r.Ld} </div> </div> `}},{kind:"get",static:!0,key:"styles",value:function(){return[u.Qx,r.iv`:host{-ms-user-select:initial;-webkit-user-select:initial;-moz-user-select:initial}.content{padding:16px;padding:max(16px,env(safe-area-inset-top)) max(16px,env(safe-area-inset-right)) max(16px,env(safe-area-inset-bottom)) max(16px,env(safe-area-inset-left))}.edit-pane{margin-right:16px;margin-inline-start:initial;margin-inline-end:16px;direction:var(--direction)}.edit-pane a{color:var(--primary-color)}.horizontal .edit-pane{max-width:50%}.render-pane{position:relative;max-width:50%;flex:1}.render-spinner{position:absolute;top:8px;right:8px}ha-alert{margin-bottom:8px;display:block}.rendered{@apply --paper-font-code1;clear:both;white-space:pre-wrap;background-color:var(--secondary-background-color);padding:8px;direction:ltr}.all_listeners{color:var(--warning-color)}@media all and (max-width:870px){.render-pane{max-width:100%}}`]}},{kind:"field",key:"_debounceRender",value(){return(0,d.D)((()=>{this._subscribeTemplate(),this._storeTemplate()}),500,!1)}},{kind:"method",key:"_templateChanged",value:function(e){this._template=e.detail.value,this._error&&(this._error=void 0,this._errorLevel=void 0),this._debounceRender()}},{kind:"method",key:"_subscribeTemplate",value:async function(){this._rendering=!0,await this._unsubscribeTemplate(),this._error=void 0,this._errorLevel=void 0,this._templateResult=void 0;try{this._unsubRenderTemplate=(0,c.N)(this.hass.connection,(e=>{"error"in e?"ERROR"!==e.level&&"ERROR"===this._errorLevel||(this._error=e.error,this._errorLevel=e.level):this._templateResult=e}),{template:this._template,timeout:3,report_errors:!0}),await this._unsubRenderTemplate}catch(e){this._error="Unknown error",this._errorLevel=void 0,e.message&&(this._error=e.message,this._errorLevel=void 0,this._templateResult=void 0),this._unsubRenderTemplate=void 0}finally{this._rendering=!1}}},{kind:"method",key:"_unsubscribeTemplate",value:async function(){if(this._unsubRenderTemplate)try{(await this._unsubRenderTemplate)(),this._unsubRenderTemplate=void 0}catch(e){if("not_found"!==e.code)throw e}}},{kind:"method",key:"_storeTemplate",value:function(){this._inited&&(localStorage["panel-dev-template-template"]=this._template)}},{kind:"method",key:"_restoreDemo",value:async function(){await(0,h.showConfirmationDialog)(this,{text:this.hass.localize("ui.panel.developer-tools.tabs.templates.confirm_reset"),warning:!0})&&(this._template=p,this._subscribeTemplate(),delete localStorage["panel-dev-template-template"])}},{kind:"method",key:"_clear",value:async function(){await(0,h.showConfirmationDialog)(this,{text:this.hass.localize("ui.panel.developer-tools.tabs.templates.confirm_clear"),warning:!0})&&(this._unsubscribeTemplate(),this._template="",this._templateResult={result:"",listeners:{all:!1,entities:[],domains:[],time:!1}})}}]}}),r.oi)},27322:(e,t,i)=>{i.d(t,{R:()=>a});const a=(e,t)=>`https://${e.config.version.includes("b")?"rc":e.config.version.includes("dev")?"next":"www"}.home-assistant.io${t}`}};
//# sourceMappingURL=5369.NT2AyrQsZtc.js.map