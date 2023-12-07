export const id=61588;export const ids=[61588];export const modules={2315:(o,e,r)=>{var t=r(17463),a=r(68144),i=r(79932),l=r(30418);r(10983);(0,t.Z)([(0,i.Mo)("ha-icon-button-arrow-prev")],(function(o,e){return{F:class extends e{constructor(...e){super(...e),o(this)}},d:[{kind:"field",decorators:[(0,i.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,i.Cb)({type:Boolean})],key:"disabled",value:()=>!1},{kind:"field",decorators:[(0,i.Cb)()],key:"label",value:void 0},{kind:"field",decorators:[(0,i.SB)()],key:"_icon",value:()=>"rtl"===l.E.document.dir?"M4,11V13H16L10.5,18.5L11.92,19.92L19.84,12L11.92,4.08L10.5,5.5L16,11H4Z":"M20,11V13H8L13.5,18.5L12.08,19.92L4.16,12L12.08,4.08L13.5,5.5L8,11H20Z"},{kind:"method",key:"render",value:function(){var o;return a.dy` <ha-icon-button .disabled="${this.disabled}" .label="${this.label||(null===(o=this.hass)||void 0===o?void 0:o.localize("ui.common.back"))||"Back"}" .path="${this._icon}"></ha-icon-button> `}}]}}),a.oi)},10983:(o,e,r)=>{var t=r(17463),a=(r(20210),r(68144)),i=r(79932),l=r(30153);r(52039);(0,t.Z)([(0,i.Mo)("ha-icon-button")],(function(o,e){return{F:class extends e{constructor(...e){super(...e),o(this)}},d:[{kind:"field",decorators:[(0,i.Cb)({type:Boolean,reflect:!0})],key:"disabled",value:()=>!1},{kind:"field",decorators:[(0,i.Cb)({type:String})],key:"path",value:void 0},{kind:"field",decorators:[(0,i.Cb)({type:String})],key:"label",value:void 0},{kind:"field",decorators:[(0,i.Cb)({type:String,attribute:"aria-haspopup"})],key:"ariaHasPopup",value:void 0},{kind:"field",decorators:[(0,i.Cb)({type:Boolean})],key:"hideTitle",value:()=>!1},{kind:"field",decorators:[(0,i.IO)("mwc-icon-button",!0)],key:"_button",value:void 0},{kind:"method",key:"focus",value:function(){var o;null===(o=this._button)||void 0===o||o.focus()}},{kind:"field",static:!0,key:"shadowRootOptions",value:()=>({mode:"open",delegatesFocus:!0})},{kind:"method",key:"render",value:function(){return a.dy` <mwc-icon-button aria-label="${(0,l.o)(this.label)}" title="${(0,l.o)(this.hideTitle?void 0:this.label)}" aria-haspopup="${(0,l.o)(this.ariaHasPopup)}" .disabled="${this.disabled}"> ${this.path?a.dy`<ha-svg-icon .path="${this.path}"></ha-svg-icon>`:a.dy`<slot></slot>`} </mwc-icon-button> `}},{kind:"get",static:!0,key:"styles",value:function(){return a.iv`:host{display:inline-block;outline:0}:host([disabled]){pointer-events:none}mwc-icon-button{--mdc-theme-on-primary:currentColor;--mdc-theme-text-disabled-on-light:var(--disabled-text-color)}`}}]}}),a.oi)},48932:(o,e,r)=>{var t=r(17463),a=r(34541),i=r(47838),l=r(68144),c=r(79932),s=r(47181),n=r(6936);r(10983);(0,t.Z)([(0,c.Mo)("ha-menu-button")],(function(o,e){class r extends e{constructor(...e){super(...e),o(this)}}return{F:r,d:[{kind:"field",decorators:[(0,c.Cb)({type:Boolean})],key:"hassio",value:()=>!1},{kind:"field",decorators:[(0,c.Cb)()],key:"narrow",value:void 0},{kind:"field",decorators:[(0,c.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,c.SB)()],key:"_hasNotifications",value:()=>!1},{kind:"field",decorators:[(0,c.SB)()],key:"_show",value:()=>!1},{kind:"field",key:"_alwaysVisible",value:()=>!1},{kind:"field",key:"_attachNotifOnConnect",value:()=>!1},{kind:"field",key:"_unsubNotifications",value:void 0},{kind:"method",key:"connectedCallback",value:function(){(0,a.Z)((0,i.Z)(r.prototype),"connectedCallback",this).call(this),this._attachNotifOnConnect&&(this._attachNotifOnConnect=!1,this._subscribeNotifications())}},{kind:"method",key:"disconnectedCallback",value:function(){(0,a.Z)((0,i.Z)(r.prototype),"disconnectedCallback",this).call(this),this._unsubNotifications&&(this._attachNotifOnConnect=!0,this._unsubNotifications(),this._unsubNotifications=void 0)}},{kind:"method",key:"render",value:function(){if(!this._show)return l.Ld;const o=this._hasNotifications&&(this.narrow||"always_hidden"===this.hass.dockedSidebar);return l.dy` <ha-icon-button .label="${this.hass.localize("ui.sidebar.sidebar_toggle")}" .path="${"M3,6H21V8H3V6M3,11H21V13H3V11M3,16H21V18H3V16Z"}" @click="${this._toggleMenu}"></ha-icon-button> ${o?l.dy`<div class="dot"></div>`:""} `}},{kind:"method",key:"firstUpdated",value:function(o){(0,a.Z)((0,i.Z)(r.prototype),"firstUpdated",this).call(this,o),this.hassio&&(this._alwaysVisible=(Number(window.parent.frontendVersion)||0)<20190710)}},{kind:"method",key:"willUpdate",value:function(o){if((0,a.Z)((0,i.Z)(r.prototype),"willUpdate",this).call(this,o),!o.has("narrow")&&!o.has("hass"))return;const e=o.has("hass")?o.get("hass"):this.hass,t=(o.has("narrow")?o.get("narrow"):this.narrow)||"always_hidden"===(null==e?void 0:e.dockedSidebar),l=this.narrow||"always_hidden"===this.hass.dockedSidebar;this.hasUpdated&&t===l||(this._show=l||this._alwaysVisible,l?this._subscribeNotifications():this._unsubNotifications&&(this._unsubNotifications(),this._unsubNotifications=void 0))}},{kind:"method",key:"_subscribeNotifications",value:function(){if(this._unsubNotifications)throw new Error("Already subscribed");this._unsubNotifications=(0,n.r)(this.hass.connection,(o=>{this._hasNotifications=o.length>0}))}},{kind:"method",key:"_toggleMenu",value:function(){(0,s.B)(this,"hass-toggle-menu")}},{kind:"get",static:!0,key:"styles",value:function(){return l.iv`:host{position:relative}.dot{pointer-events:none;position:absolute;background-color:var(--accent-color);width:12px;height:12px;top:9px;right:7px;border-radius:50%;border:2px solid var(--app-header-background-color)}`}}]}}),l.oi)},52039:(o,e,r)=>{var t=r(17463),a=r(68144),i=r(79932);(0,t.Z)([(0,i.Mo)("ha-svg-icon")],(function(o,e){return{F:class extends e{constructor(...e){super(...e),o(this)}},d:[{kind:"field",decorators:[(0,i.Cb)()],key:"path",value:void 0},{kind:"field",decorators:[(0,i.Cb)()],key:"secondaryPath",value:void 0},{kind:"field",decorators:[(0,i.Cb)()],key:"viewBox",value:void 0},{kind:"method",key:"render",value:function(){return a.YP` <svg viewBox="${this.viewBox||"0 0 24 24"}" preserveAspectRatio="xMidYMid meet" focusable="false" role="img" aria-hidden="true"> <g> ${this.path?a.YP`<path class="primary-path" d="${this.path}"></path>`:a.Ld} ${this.secondaryPath?a.YP`<path class="secondary-path" d="${this.secondaryPath}"></path>`:a.Ld} </g> </svg>`}},{kind:"get",static:!0,key:"styles",value:function(){return a.iv`:host{display:var(--ha-icon-display,inline-flex);align-items:center;justify-content:center;position:relative;vertical-align:middle;fill:var(--icon-primary-color,currentcolor);width:var(--mdc-icon-size,24px);height:var(--mdc-icon-size,24px)}svg{width:100%;height:100%;pointer-events:none;display:block}path.primary-path{opacity:var(--icon-primary-opactity, 1)}path.secondary-path{fill:var(--icon-secondary-color,currentcolor);opacity:var(--icon-secondary-opactity, .5)}`}}]}}),a.oi)},6936:(o,e,r)=>{r.d(e,{r:()=>t});const t=(o,e)=>{const r=new a,t=o.subscribeMessage((o=>e(r.processMessage(o))),{type:"persistent_notification/subscribe"});return()=>{t.then((o=>null==o?void 0:o()))}};class a{constructor(){this.notifications=void 0,this.notifications={}}processMessage(o){if("removed"===o.type)for(const e of Object.keys(o.notifications))delete this.notifications[e];else this.notifications={...this.notifications,...o.notifications};return Object.values(this.notifications)}}},61588:(o,e,r)=>{r.r(e);var t=r(17463),a=r(34541),i=r(47838),l=(r(14271),r(68144)),c=r(79932);const s={"primary-background-color":"#111111","card-background-color":"#1c1c1c","secondary-background-color":"#282828","clear-background-color":"#111111","primary-text-color":"#e1e1e1","secondary-text-color":"#9b9b9b","disabled-text-color":"#6f6f6f","app-header-text-color":"#e1e1e1","app-header-background-color":"#101e24","switch-unchecked-button-color":"#999999","switch-unchecked-track-color":"#9b9b9b","divider-color":"rgba(225, 225, 225, .12)","outline-color":"rgba(225, 225, 225, .12)","mdc-ripple-color":"#AAAAAA","mdc-linear-progress-buffer-color":"rgba(255, 255, 255, 0.1)","input-idle-line-color":"rgba(255, 255, 255, 0.42)","input-hover-line-color":"rgba(255, 255, 255, 0.87)","input-disabled-line-color":"rgba(255, 255, 255, 0.06)","input-outlined-idle-border-color":"rgba(255, 255, 255, 0.38)","input-outlined-hover-border-color":"rgba(255, 255, 255, 0.87)","input-outlined-disabled-border-color":"rgba(255, 255, 255, 0.06)","input-fill-color":"rgba(255, 255, 255, 0.05)","input-disabled-fill-color":"rgba(255, 255, 255, 0.02)","input-ink-color":"rgba(255, 255, 255, 0.87)","input-label-ink-color":"rgba(255, 255, 255, 0.6)","input-disabled-ink-color":"rgba(255, 255, 255, 0.37)","input-dropdown-icon-color":"rgba(255, 255, 255, 0.54)","codemirror-keyword":"#C792EA","codemirror-operator":"#89DDFF","codemirror-variable":"#f07178","codemirror-variable-2":"#EEFFFF","codemirror-variable-3":"#DECB6B","codemirror-builtin":"#FFCB6B","codemirror-atom":"#F78C6C","codemirror-number":"#FF5370","codemirror-def":"#82AAFF","codemirror-string":"#C3E88D","codemirror-string-2":"#f07178","codemirror-comment":"#545454","codemirror-tag":"#FF5370","codemirror-meta":"#FFCB6B","codemirror-attribute":"#C792EA","codemirror-property":"#C792EA","codemirror-qualifier":"#DECB6B","codemirror-type":"#DECB6B","energy-grid-return-color":"#a280db","map-filter":"invert(.9) hue-rotate(170deg) brightness(1.5) contrast(1.2) saturate(.3)","disabled-color":"#464646"},n={"state-icon-error-color":"var(--error-state-color, var(--error-color))","state-unavailable-color":"var(--state-icon-unavailable-color, var(--disabled-text-color))","sidebar-text-color":"var(--primary-text-color)","sidebar-background-color":"var(--card-background-color)","sidebar-selected-text-color":"var(--primary-color)","sidebar-selected-icon-color":"var(--primary-color)","sidebar-icon-color":"rgba(var(--rgb-primary-text-color), 0.6)","switch-checked-color":"var(--primary-color)","switch-checked-button-color":"var(--switch-checked-color, var(--primary-background-color))","switch-checked-track-color":"var(--switch-checked-color, #000000)","switch-unchecked-button-color":"var(--switch-unchecked-color, var(--primary-background-color))","switch-unchecked-track-color":"var(--switch-unchecked-color, #000000)","slider-color":"var(--primary-color)","slider-secondary-color":"var(--light-primary-color)","slider-track-color":"var(--scrollbar-thumb-color)","label-badge-background-color":"var(--card-background-color)","label-badge-text-color":"rgba(var(--rgb-primary-text-color), 0.8)","paper-listbox-background-color":"var(--card-background-color)","paper-item-icon-color":"var(--state-icon-color)","paper-item-icon-active-color":"var(--state-icon-active-color)","table-header-background-color":"var(--input-fill-color)","table-row-background-color":"var(--primary-background-color)","table-row-alternative-background-color":"var(--secondary-background-color)","data-table-background-color":"var(--card-background-color)","markdown-code-background-color":"var(--primary-background-color)","mdc-theme-primary":"var(--primary-color)","mdc-theme-secondary":"var(--accent-color)","mdc-theme-background":"var(--primary-background-color)","mdc-theme-surface":"var(--card-background-color)","mdc-theme-on-primary":"var(--text-primary-color)","mdc-theme-on-secondary":"var(--text-primary-color)","mdc-theme-on-surface":"var(--primary-text-color)","mdc-theme-text-disabled-on-light":"var(--disabled-text-color)","mdc-theme-text-primary-on-background":"var(--primary-text-color)","mdc-theme-text-secondary-on-background":"var(--secondary-text-color)","mdc-theme-text-hint-on-background":"var(--secondary-text-color)","mdc-theme-text-icon-on-background":"var(--secondary-text-color)","mdc-theme-error":"var(--error-color)","app-header-text-color":"var(--text-primary-color)","app-header-background-color":"var(--primary-color)","mdc-checkbox-unchecked-color":"rgba(var(--rgb-primary-text-color), 0.54)","mdc-checkbox-disabled-color":"var(--disabled-text-color)","mdc-radio-unchecked-color":"rgba(var(--rgb-primary-text-color), 0.54)","mdc-radio-disabled-color":"var(--disabled-text-color)","mdc-tab-text-label-color-default":"var(--primary-text-color)","mdc-button-disabled-ink-color":"var(--disabled-text-color)","mdc-button-outline-color":"var(--outline-color)","mdc-dialog-scroll-divider-color":"var(--divider-color)","mdc-dialog-heading-ink-color":"var(--primary-text-color)","mdc-dialog-content-ink-color":"var(--primary-text-color)","mdc-text-field-idle-line-color":"var(--input-idle-line-color)","mdc-text-field-hover-line-color":"var(--input-hover-line-color)","mdc-text-field-disabled-line-color":"var(--input-disabled-line-color)","mdc-text-field-outlined-idle-border-color":"var(--input-outlined-idle-border-color)","mdc-text-field-outlined-hover-border-color":"var(--input-outlined-hover-border-color)","mdc-text-field-outlined-disabled-border-color":"var(--input-outlined-disabled-border-color)","mdc-text-field-fill-color":"var(--input-fill-color)","mdc-text-field-disabled-fill-color":"var(--input-disabled-fill-color)","mdc-text-field-ink-color":"var(--input-ink-color)","mdc-text-field-label-ink-color":"var(--input-label-ink-color)","mdc-text-field-disabled-ink-color":"var(--input-disabled-ink-color)","mdc-select-idle-line-color":"var(--input-idle-line-color)","mdc-select-hover-line-color":"var(--input-hover-line-color)","mdc-select-outlined-idle-border-color":"var(--input-outlined-idle-border-color)","mdc-select-outlined-hover-border-color":"var(--input-outlined-hover-border-color)","mdc-select-outlined-disabled-border-color":"var(--input-outlined-disabled-border-color)","mdc-select-fill-color":"var(--input-fill-color)","mdc-select-disabled-fill-color":"var(--input-disabled-fill-color)","mdc-select-ink-color":"var(--input-ink-color)","mdc-select-label-ink-color":"var(--input-label-ink-color)","mdc-select-disabled-ink-color":"var(--input-disabled-ink-color)","mdc-select-dropdown-icon-color":"var(--input-dropdown-icon-color)","mdc-select-disabled-dropdown-icon-color":"var(--input-disabled-ink-color)","chip-background-color":"rgba(var(--rgb-primary-text-color), 0.15)","material-body-text-color":"var(--primary-text-color)","material-background-color":"var(--card-background-color)","material-secondary-background-color":"var(--secondary-background-color)","material-secondary-text-color":"var(--secondary-text-color)"},d=o=>{if(6===(o=o.replace("#","")).length)return o;let e="";for(const r of o)e+=r+r;return e},h=o=>{const e=Math.round(Math.min(Math.max(o,0),255)).toString(16);return 1===e.length?`0${e}`:e},u=o=>(o=d(o),[parseInt(o.substring(0,2),16),parseInt(o.substring(2,4),16),parseInt(o.substring(4,6),16)]),b=o=>`#${h(o[0])}${h(o[1])}${h(o[2])}`,p=.95047,v=1.08883,m=.137931034,k=.12841855,y=o=>(o/=255)<=.04045?o/12.92:((o+.055)/1.055)**2.4,f=o=>o>.008856452?o**(1/3):o/k+m,g=o=>255*(o<=.00304?12.92*o:1.055*o**(1/2.4)-.055),x=o=>o>.206896552?o*o*o:k*(o-m),w=o=>{const[e,r,t]=(o=>{let[e,r,t]=o;return e=y(e),r=y(r),t=y(t),[f((.4124564*e+.3575761*r+.1804375*t)/p),f((.2126729*e+.7151522*r+.072175*t)/1),f((.0193339*e+.119192*r+.9503041*t)/v)]})(o),a=116*r-16;return[a<0?0:a,500*(e-r),200*(r-t)]},_=o=>{const[e,r,t]=o;let a=(e+16)/116,i=isNaN(r)?a:a+r/500,l=isNaN(t)?a:a-t/200;a=1*x(a),i=p*x(i),l=v*x(l);return[g(3.2404542*i-1.5371385*a-.4985314*l),g(-.969266*i+1.8760108*a+.041556*l),g(.0556434*i-.2040259*a+1.0572252*l)]},C=(o,e=1)=>[o[0]-18*e,o[1],o[2]],$=o=>{const e=[0,0,0];for(let r=0;r<o.length;r++){const t=o[r]/255;e[r]=t<=.03928?t/12.92:((t+.055)/1.055)**2.4}return.2126*e[0]+.7152*e[1]+.0722*e[2]},N=(o,e)=>{const r=$(o),t=$(e);return r>t?(r+.05)/(t+.05):(t+.05)/(r+.05)};let S={};const M=(o,e,r,t,a)=>{var i,l;const c=r||(a?e.theme:void 0),n=void 0!==(null==t?void 0:t.dark)?t.dark:e.darkMode;let h=c,p={};if(c&&n&&(h=`${h}__dark`,p={...s}),"default"===c){var v;const e=null==t?void 0:t.primaryColor,r=null==t?void 0:t.accentColor;if(n&&e&&(p["app-header-background-color"]=((o,e,r=50)=>{let t="";o=d(o),e=d(e);for(let a=0;a<=5;a+=2){const i=parseInt(o.substr(a,2),16),l=parseInt(e.substr(a,2),16);let c=Math.floor(l+r/100*(i-l)).toString(16);for(;c.length<2;)c="0"+c;t+=c}return`#${t}`})(e,"#121212",8)),e){h=`${h}__primary_${e}`;const o=u(e),r=w(o);p["primary-color"]=e;const t=_(((o,e=1)=>C(o,-e))(r));p["light-primary-color"]=b(t),p["dark-primary-color"]=(o=>{const e=_(o);return b(e)})(C(r)),p["text-primary-color"]=N(o,[33,33,33])<6?"#fff":"#212121",p["text-light-primary-color"]=N(t,[33,33,33])<6?"#fff":"#212121",p["state-icon-color"]=p["dark-primary-color"]}if(r){h=`${h}__accent_${r}`,p["accent-color"]=r;const o=u(r);p["text-accent-color"]=N(o,[33,33,33])<6?"#fff":"#212121"}if((null===(v=o.__themes)||void 0===v?void 0:v.cacheKey)===h)return}if(c&&"default"!==c&&e.themes[c]){const{modes:o,...r}=e.themes[c];p={...p,...r},o&&(p=n?{...p,...o.dark}:{...p,...o.light})}if(!(null!==(i=o.__themes)&&void 0!==i&&i.keys||Object.keys(p).length))return;const m=Object.keys(p).length&&h?S[h]||B(h,p):void 0,k={...null===(l=o.__themes)||void 0===l?void 0:l.keys,...null==m?void 0:m.styles};if(o.__themes={cacheKey:h,keys:null==m?void 0:m.keys},o.updateStyles)o.updateStyles(k);else if(window.ShadyCSS)window.ShadyCSS.styleSubtree(o,k);else for(const e in k)null===e?o.style.removeProperty(e):o.style.setProperty(e,k[e])},B=(o,e)=>{if(!e||!Object.keys(e).length)return;const r={...n,...e},t={},a={};for(const o of Object.keys(r)){const e=`--${o}`,i=String(r[o]);if(t[e]=i,a[e]="",!i.startsWith("#"))continue;const l=`rgb-${o}`;if(void 0===r[l])try{const o=u(i).join(","),e=`--${l}`;t[e]=o,a[e]=""}catch(o){continue}}return S[o]={styles:t,keys:a},{styles:t,keys:a}};(0,t.Z)([(0,c.Mo)("ha-card")],(function(o,e){return{F:class extends e{constructor(...e){super(...e),o(this)}},d:[{kind:"field",decorators:[(0,c.Cb)()],key:"header",value:void 0},{kind:"field",decorators:[(0,c.Cb)({type:Boolean,reflect:!0})],key:"raised",value:()=>!1},{kind:"get",static:!0,key:"styles",value:function(){return l.iv`:host{background:var(--ha-card-background,var(--card-background-color,#fff));box-shadow:var(--ha-card-box-shadow,none);box-sizing:border-box;border-radius:var(--ha-card-border-radius,12px);border-width:var(--ha-card-border-width,1px);border-style:solid;border-color:var(--ha-card-border-color,var(--divider-color,#e0e0e0));color:var(--primary-text-color);display:block;transition:all .3s ease-out;position:relative}:host([raised]){border:none;box-shadow:var(--ha-card-box-shadow,0px 2px 1px -1px rgba(0,0,0,.2),0px 1px 1px 0px rgba(0,0,0,.14),0px 1px 3px 0px rgba(0,0,0,.12))}.card-header,:host ::slotted(.card-header){color:var(--ha-card-header-color,--primary-text-color);font-family:var(--ha-card-header-font-family, inherit);font-size:var(--ha-card-header-font-size, 24px);letter-spacing:-.012em;line-height:48px;padding:12px 16px 16px;display:block;margin-block-start:0px;margin-block-end:0px;font-weight:400}:host ::slotted(.card-content:not(:first-child)),slot:not(:first-child)::slotted(.card-content){padding-top:0px;margin-top:-8px}:host ::slotted(.card-content){padding:16px}:host ::slotted(.card-actions){border-top:1px solid var(--divider-color,#e8e8e8);padding:5px 16px}`}},{kind:"method",key:"render",value:function(){return l.dy` ${this.header?l.dy`<h1 class="card-header">${this.header}</h1>`:l.Ld} <slot></slot> `}}]}}),l.oi);var F=r(11654);const Z=((o,e,r=!0,t=!0)=>{let a,i=0;const l=(...l)=>{const c=()=>{i=!1===r?0:Date.now(),a=void 0,o(...l)},s=Date.now();i||!1!==r||(i=s);const n=e-(s-i);n<=0||n>e?(a&&(clearTimeout(a),a=void 0),i=s,o(...l)):a||!1===t||(a=window.setTimeout(c,n))};return l.cancel=()=>{clearTimeout(a),a=void 0,i=0},l})((o=>{history.replaceState({scrollPosition:o},"")}),300),P=o=>e=>({kind:"method",placement:"prototype",key:e.key,descriptor:{set(o){Z(o),this[`__${String(e.key)}`]=o},get(){var o;return this[`__${String(e.key)}`]||(null===(o=history.state)||void 0===o?void 0:o.scrollPosition)},enumerable:!0,configurable:!0},finisher(r){const t=r.prototype.connectedCallback;r.prototype.connectedCallback=function(){t.call(this);const r=this[e.key];r&&this.updateComplete.then((()=>{const e=this.renderRoot.querySelector(o);e&&setTimeout((()=>{e.scrollTop=r}),0)}))}}});function T(o){const e=o.language||"en";return o.translationMetadata.translations[e]&&o.translationMetadata.translations[e].isRTL||!1}r(2315),r(48932);(0,t.Z)([(0,c.Mo)("hass-subpage")],(function(o,e){class r extends e{constructor(...e){super(...e),o(this)}}return{F:r,d:[{kind:"field",decorators:[(0,c.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,c.Cb)()],key:"header",value:void 0},{kind:"field",decorators:[(0,c.Cb)({type:Boolean,attribute:"main-page"})],key:"mainPage",value:()=>!1},{kind:"field",decorators:[(0,c.Cb)({type:String,attribute:"back-path"})],key:"backPath",value:void 0},{kind:"field",decorators:[(0,c.Cb)()],key:"backCallback",value:void 0},{kind:"field",decorators:[(0,c.Cb)({type:Boolean,reflect:!0})],key:"narrow",value:()=>!1},{kind:"field",decorators:[(0,c.Cb)({type:Boolean})],key:"supervisor",value:()=>!1},{kind:"field",decorators:[P(".content")],key:"_savedScrollPos",value:void 0},{kind:"method",key:"willUpdate",value:function(o){if((0,a.Z)((0,i.Z)(r.prototype),"willUpdate",this).call(this,o),!o.has("hass"))return;const e=o.get("hass");var t,l,c;e&&e.locale===this.hass.locale||(t=this,l="rtl",void 0!==(c=T(this.hass))&&(c=!!c),t.hasAttribute(l)?c||t.removeAttribute(l):!1!==c&&t.setAttribute(l,""))}},{kind:"method",key:"render",value:function(){var o;return l.dy` <div class="toolbar"> ${this.mainPage||null!==(o=history.state)&&void 0!==o&&o.root?l.dy` <ha-menu-button .hassio="${this.supervisor}" .hass="${this.hass}" .narrow="${this.narrow}"></ha-menu-button> `:this.backPath?l.dy` <a href="${this.backPath}"> <ha-icon-button-arrow-prev .hass="${this.hass}"></ha-icon-button-arrow-prev> </a> `:l.dy` <ha-icon-button-arrow-prev .hass="${this.hass}" @click="${this._backTapped}"></ha-icon-button-arrow-prev> `} <div class="main-title"><slot name="header">${this.header}</slot></div> <slot name="toolbar-icon"></slot> </div> <div class="content ha-scrollbar" @scroll="${this._saveScrollPos}"> <slot></slot> </div> <div id="fab"> <slot name="fab"></slot> </div> `}},{kind:"method",decorators:[(0,c.hO)({passive:!0})],key:"_saveScrollPos",value:function(o){this._savedScrollPos=o.target.scrollTop}},{kind:"method",key:"_backTapped",value:function(){this.backCallback?this.backCallback():history.back()}},{kind:"get",static:!0,key:"styles",value:function(){return[F.$c,l.iv`:host{display:block;height:100%;background-color:var(--primary-background-color);overflow:hidden;position:relative}:host([narrow]){width:100%;position:fixed}.toolbar{display:flex;align-items:center;font-size:20px;height:var(--header-height);padding:8px 12px;pointer-events:none;background-color:var(--app-header-background-color);font-weight:400;color:var(--app-header-text-color,#fff);border-bottom:var(--app-header-border-bottom,none);box-sizing:border-box}@media (max-width:599px){.toolbar{padding:4px}}.toolbar a{color:var(--sidebar-text-color);text-decoration:none}::slotted([slot=toolbar-icon]),ha-icon-button-arrow-prev,ha-menu-button{pointer-events:auto;color:var(--sidebar-icon-color)}.main-title{margin:0 0 0 24px;line-height:20px;flex-grow:1}.content{position:relative;width:100%;height:calc(100% - 1px - var(--header-height));overflow-y:auto;overflow:auto;-webkit-overflow-scrolling:touch}#fab{position:absolute;right:calc(16px + env(safe-area-inset-right));bottom:calc(16px + env(safe-area-inset-bottom));z-index:1}:host([narrow]) #fab.tabs{bottom:calc(84px + env(safe-area-inset-bottom))}#fab[is-wide]{bottom:24px;right:24px}:host([rtl]) #fab{right:auto;left:calc(16px + env(safe-area-inset-left))}:host([rtl][is-wide]) #fab{bottom:24px;left:24px;right:auto}`]}}]}}),l.oi),(0,t.Z)([(0,c.Mo)("supervisor-error-screen")],(function(o,e){class r extends e{constructor(...e){super(...e),o(this)}}return{F:r,d:[{kind:"field",decorators:[(0,c.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"method",key:"firstUpdated",value:function(o){(0,a.Z)((0,i.Z)(r.prototype),"firstUpdated",this).call(this,o),this._applyTheme()}},{kind:"method",key:"updated",value:function(o){(0,a.Z)((0,i.Z)(r.prototype),"updated",this).call(this,o);const e=o.get("hass");e&&e.themes!==this.hass.themes&&this._applyTheme()}},{kind:"method",key:"render",value:function(){return l.dy` <hass-subpage .hass="${this.hass}" .header="${this.hass.localize("ui.errors.supervisor.title")}"> <ha-card header="Troubleshooting"> <div class="card-content"> <ol> <li>${this.hass.localize("ui.errors.supervisor.wait")}</li> <li> <a class="supervisor_error-link" href="http://homeassistant.local:4357" target="_blank" rel="noreferrer"> ${this.hass.localize("ui.errors.supervisor.observer")} </a> </li> <li>${this.hass.localize("ui.errors.supervisor.reboot")}</li> <li> <a href="/config/info" target="_parent"> ${this.hass.localize("ui.errors.supervisor.system_health")} </a> </li> <li> <a href="https://www.home-assistant.io/help/" target="_blank" rel="noreferrer"> ${this.hass.localize("ui.errors.supervisor.ask")} </a> </li> </ol> </div> </ha-card> </hass-subpage> `}},{kind:"method",key:"_applyTheme",value:function(){let o,e;var r;((o,e,r,t)=>{const[a,i,l]=o.split(".",3);return Number(a)>e||Number(a)===e&&(void 0===t?Number(i)>=r:Number(i)>r)||void 0!==t&&Number(a)===e&&Number(i)===r&&Number(l)>=t})(this.hass.config.version,0,114)?(o=(null===(r=this.hass.selectedTheme)||void 0===r?void 0:r.theme)||(this.hass.themes.darkMode&&this.hass.themes.default_dark_theme?this.hass.themes.default_dark_theme:this.hass.themes.default_theme),e=this.hass.selectedTheme):o=this.hass.selectedTheme||this.hass.themes.default_theme;M(this.parentElement,this.hass.themes,o,e,!0)}},{kind:"get",static:!0,key:"styles",value:function(){return[F.Qx,l.iv`a{color:var(--mdc-theme-primary)}ha-card{width:600px;margin:auto;padding:8px}@media all and (max-width:500px){ha-card{width:calc(100vw - 32px)}}`]}}]}}),l.oi)}};
//# sourceMappingURL=61588.YfTOeVGu984.js.map