"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[49082],{25516:function(t,e,i){i.d(e,{i:function(){return o}});var r=(0,i(8330).P)((function(t){history.replaceState({scrollPosition:t},"")}),300),o=function(t){return function(e){return{kind:"method",placement:"prototype",key:e.key,descriptor:{set:function(t){r(t),this["__".concat(String(e.key))]=t},get:function(){var t;return this["__".concat(String(e.key))]||(null===(t=history.state)||void 0===t?void 0:t.scrollPosition)},enumerable:!0,configurable:!0},finisher:function(i){var r=i.prototype.connectedCallback;i.prototype.connectedCallback=function(){var i=this;r.call(this);var o=this[e.key];o&&this.updateComplete.then((function(){var e=i.renderRoot.querySelector(t);e&&setTimeout((function(){e.scrollTop=o}),0)}))}}}}}},86977:function(t,e,i){i.d(e,{Q:function(){return r}});var r=function(t){return!(!t.detail.selected||"property"!==t.detail.source)&&(t.currentTarget.selected=!1,!0)}},15493:function(t,e,i){i.d(e,{Q2:function(){return a},io:function(){return n},j4:function(){return c},ou:function(){return s},pc:function(){return l}});var r=i(68990),o=i(40039),a=(i(51358),i(46798),i(5239),i(98490),i(7695),i(44758),i(80354),i(68630),i(63789),i(35221),i(9849),i(50289),i(94167),i(82073),i(94570),function(){var t,e={},i=new URLSearchParams(location.search),a=(0,o.Z)(i.entries());try{for(a.s();!(t=a.n()).done;){var n=(0,r.Z)(t.value,2),s=n[0],c=n[1];e[s]=c}}catch(l){a.e(l)}finally{a.f()}return e}),n=function(t){return new URLSearchParams(window.location.search).get(t)},s=function(t){var e=new URLSearchParams;return Object.entries(t).forEach((function(t){var i=(0,r.Z)(t,2),o=i[0],a=i[1];e.append(o,a)})),e.toString()},c=function(t){var e=new URLSearchParams(window.location.search);return Object.entries(t).forEach((function(t){var i=(0,r.Z)(t,2),o=i[0],a=i[1];e.set(o,a)})),e.toString()},l=function(t){var e=new URLSearchParams(window.location.search);return e.delete(t),e.toString()}},8330:function(t,e,i){i.d(e,{P:function(){return r}});var r=function(t,e){var i,r=!(arguments.length>2&&void 0!==arguments[2])||arguments[2],o=!(arguments.length>3&&void 0!==arguments[3])||arguments[3],a=0,n=function(){for(var n=arguments.length,s=new Array(n),c=0;c<n;c++)s[c]=arguments[c];var l=Date.now();a||!1!==r||(a=l);var d=e-(l-a);d<=0||d>e?(i&&(clearTimeout(i),i=void 0),a=l,t.apply(void 0,s)):i||!1===o||(i=window.setTimeout((function(){a=!1===r?0:Date.now(),i=void 0,t.apply(void 0,s)}),d))};return n.cancel=function(){clearTimeout(i),i=void 0,a=0},n}},9381:function(t,e,i){var r,o,a,n,s=i(93359),c=i(88962),l=i(33368),d=i(71650),h=i(82390),u=i(69205),p=i(70906),v=i(91808),f=(i(97393),i(68144)),m=i(95260),g=i(83448),y=i(47181),b=(i(10983),i(52039),{info:"M11,9H13V7H11M12,20C7.59,20 4,16.41 4,12C4,7.59 7.59,4 12,4C16.41,4 20,7.59 20,12C20,16.41 16.41,20 12,20M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M11,17H13V11H11V17Z",warning:"M12,2L1,21H23M12,6L19.53,19H4.47M11,10V14H13V10M11,16V18H13V16",error:"M11,15H13V17H11V15M11,7H13V13H11V7M12,2C6.47,2 2,6.5 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M12,20A8,8 0 0,1 4,12A8,8 0 0,1 12,4A8,8 0 0,1 20,12A8,8 0 0,1 12,20Z",success:"M20,12A8,8 0 0,1 12,20A8,8 0 0,1 4,12A8,8 0 0,1 12,4C12.76,4 13.5,4.11 14.2,4.31L15.77,2.74C14.61,2.26 13.34,2 12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12M7.91,10.08L6.5,11.5L11,16L21,6L19.59,4.58L11,13.17L7.91,10.08Z"});(0,v.Z)([(0,m.Mo)("ha-alert")],(function(t,e){var i=function(e){(0,u.Z)(r,e);var i=(0,p.Z)(r);function r(){var e;(0,d.Z)(this,r);for(var o=arguments.length,a=new Array(o),n=0;n<o;n++)a[n]=arguments[n];return e=i.call.apply(i,[this].concat(a)),t((0,h.Z)(e)),e}return(0,l.Z)(r)}(e);return{F:i,d:[{kind:"field",decorators:[(0,m.Cb)()],key:"title",value:function(){return""}},{kind:"field",decorators:[(0,m.Cb)({attribute:"alert-type"})],key:"alertType",value:function(){return"info"}},{kind:"field",decorators:[(0,m.Cb)({type:Boolean})],key:"dismissable",value:function(){return!1}},{kind:"method",key:"render",value:function(){return(0,f.dy)(r||(r=(0,c.Z)([' <div class="issue-type ','" role="alert"> <div class="icon ','"> <slot name="icon"> <ha-svg-icon .path="','"></ha-svg-icon> </slot> </div> <div class="content"> <div class="main-content"> ',' <slot></slot> </div> <div class="action"> <slot name="action"> '," </slot> </div> </div> </div> "])),(0,g.$)((0,s.Z)({},this.alertType,!0)),this.title?"":"no-title",b[this.alertType],this.title?(0,f.dy)(o||(o=(0,c.Z)(['<div class="title">',"</div>"])),this.title):"",this.dismissable?(0,f.dy)(a||(a=(0,c.Z)(['<ha-icon-button @click="','" label="Dismiss alert" .path="','"></ha-icon-button>'])),this._dismiss_clicked,"M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z"):"")}},{kind:"method",key:"_dismiss_clicked",value:function(){(0,y.B)(this,"alert-dismissed-clicked")}},{kind:"field",static:!0,key:"styles",value:function(){return(0,f.iv)(n||(n=(0,c.Z)(['.issue-type{position:relative;padding:8px;display:flex}.issue-type::after{position:absolute;top:0;right:0;bottom:0;left:0;opacity:.12;pointer-events:none;content:"";border-radius:4px}.icon{z-index:1}.icon.no-title{align-self:center}.content{display:flex;justify-content:space-between;align-items:center;width:100%;text-align:var(--float-start)}.action{z-index:1;width:min-content;--mdc-theme-primary:var(--primary-text-color)}.main-content{overflow-wrap:anywhere;word-break:break-word;margin-left:8px;margin-right:0;margin-inline-start:8px;margin-inline-end:0;direction:var(--direction)}.title{margin-top:2px;font-weight:700}.action ha-icon-button,.action mwc-button{--mdc-theme-primary:var(--primary-text-color);--mdc-icon-button-size:36px}.issue-type.info>.icon{color:var(--info-color)}.issue-type.info::after{background-color:var(--info-color)}.issue-type.warning>.icon{color:var(--warning-color)}.issue-type.warning::after{background-color:var(--warning-color)}.issue-type.error>.icon{color:var(--error-color)}.issue-type.error::after{background-color:var(--error-color)}.issue-type.success>.icon{color:var(--success-color)}.issue-type.success::after{background-color:var(--success-color)}'])))}}]}}),f.oi)},22098:function(t,e,i){var r,o,a,n=i(88962),s=i(33368),c=i(71650),l=i(82390),d=i(69205),h=i(70906),u=i(91808),p=(i(97393),i(68144)),v=i(95260);(0,u.Z)([(0,v.Mo)("ha-card")],(function(t,e){var i=function(e){(0,d.Z)(r,e);var i=(0,h.Z)(r);function r(){var e;(0,c.Z)(this,r);for(var o=arguments.length,a=new Array(o),n=0;n<o;n++)a[n]=arguments[n];return e=i.call.apply(i,[this].concat(a)),t((0,l.Z)(e)),e}return(0,s.Z)(r)}(e);return{F:i,d:[{kind:"field",decorators:[(0,v.Cb)()],key:"header",value:void 0},{kind:"field",decorators:[(0,v.Cb)({type:Boolean,reflect:!0})],key:"raised",value:function(){return!1}},{kind:"get",static:!0,key:"styles",value:function(){return(0,p.iv)(r||(r=(0,n.Z)([":host{background:var(--ha-card-background,var(--card-background-color,#fff));box-shadow:var(--ha-card-box-shadow,none);box-sizing:border-box;border-radius:var(--ha-card-border-radius,12px);border-width:var(--ha-card-border-width,1px);border-style:solid;border-color:var(--ha-card-border-color,var(--divider-color,#e0e0e0));color:var(--primary-text-color);display:block;transition:all .3s ease-out;position:relative}:host([raised]){border:none;box-shadow:var(--ha-card-box-shadow,0px 2px 1px -1px rgba(0,0,0,.2),0px 1px 1px 0px rgba(0,0,0,.14),0px 1px 3px 0px rgba(0,0,0,.12))}.card-header,:host ::slotted(.card-header){color:var(--ha-card-header-color,--primary-text-color);font-family:var(--ha-card-header-font-family, inherit);font-size:var(--ha-card-header-font-size, 24px);letter-spacing:-.012em;line-height:48px;padding:12px 16px 16px;display:block;margin-block-start:0px;margin-block-end:0px;font-weight:400}:host ::slotted(.card-content:not(:first-child)),slot:not(:first-child)::slotted(.card-content){padding-top:0px;margin-top:-8px}:host ::slotted(.card-content){padding:16px}:host ::slotted(.card-actions){border-top:1px solid var(--divider-color,#e8e8e8);padding:5px 16px}"])))}},{kind:"method",key:"render",value:function(){return(0,p.dy)(o||(o=(0,n.Z)([" "," <slot></slot> "])),this.header?(0,p.dy)(a||(a=(0,n.Z)(['<h1 class="card-header">',"</h1>"])),this.header):p.Ld)}}]}}),p.oi)},84431:function(t,e,i){var r,o=i(88962),a=i(33368),n=i(71650),s=i(82390),c=i(69205),l=i(70906),d=i(91808),h=(i(97393),i(68144)),u=i(63335),p=i(21270),v=i(96762),f=i(95260);(0,d.Z)([(0,f.Mo)("ha-check-list-item")],(function(t,e){var i=function(e){(0,c.Z)(r,e);var i=(0,l.Z)(r);function r(){var e;(0,n.Z)(this,r);for(var o=arguments.length,a=new Array(o),c=0;c<o;c++)a[c]=arguments[c];return e=i.call.apply(i,[this].concat(a)),t((0,s.Z)(e)),e}return(0,a.Z)(r)}(e);return{F:i,d:[{kind:"field",static:!0,key:"styles",value:function(){return[v.W,p.W,(0,h.iv)(r||(r=(0,o.Z)([":host{--mdc-theme-secondary:var(--primary-color)}:host([graphic=avatar]) .mdc-deprecated-list-item__graphic,:host([graphic=control]) .mdc-deprecated-list-item__graphic,:host([graphic=large]) .mdc-deprecated-list-item__graphic,:host([graphic=medium]) .mdc-deprecated-list-item__graphic{margin-inline-end:var(--mdc-list-item-graphic-margin,16px);margin-inline-start:0px;direction:var(--direction)}"])))]}}]}}),u.F)},2315:function(t,e,i){var r,o=i(88962),a=i(33368),n=i(71650),s=i(82390),c=i(69205),l=i(70906),d=i(91808),h=(i(97393),i(68144)),u=i(95260),p=i(30418);i(10983),(0,d.Z)([(0,u.Mo)("ha-icon-button-arrow-prev")],(function(t,e){var i=function(e){(0,c.Z)(r,e);var i=(0,l.Z)(r);function r(){var e;(0,n.Z)(this,r);for(var o=arguments.length,a=new Array(o),c=0;c<o;c++)a[c]=arguments[c];return e=i.call.apply(i,[this].concat(a)),t((0,s.Z)(e)),e}return(0,a.Z)(r)}(e);return{F:i,d:[{kind:"field",decorators:[(0,u.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,u.Cb)({type:Boolean})],key:"disabled",value:function(){return!1}},{kind:"field",decorators:[(0,u.Cb)()],key:"label",value:void 0},{kind:"field",decorators:[(0,u.SB)()],key:"_icon",value:function(){return"rtl"===p.E.document.dir?"M4,11V13H16L10.5,18.5L11.92,19.92L19.84,12L11.92,4.08L10.5,5.5L16,11H4Z":"M20,11V13H8L13.5,18.5L12.08,19.92L4.16,12L12.08,4.08L13.5,5.5L8,11H20Z"}},{kind:"method",key:"render",value:function(){var t;return(0,h.dy)(r||(r=(0,o.Z)([' <ha-icon-button .disabled="','" .label="','" .path="','"></ha-icon-button> '])),this.disabled,this.label||(null===(t=this.hass)||void 0===t?void 0:t.localize("ui.common.back"))||"Back",this._icon)}}]}}),h.oi)},73366:function(t,e,i){i.d(e,{M:function(){return g}});var r,o=i(88962),a=i(33368),n=i(71650),s=i(82390),c=i(69205),l=i(70906),d=i(91808),h=i(34541),u=i(47838),p=(i(97393),i(61092)),v=i(96762),f=i(68144),m=i(95260),g=(0,d.Z)([(0,m.Mo)("ha-list-item")],(function(t,e){var i=function(e){(0,c.Z)(r,e);var i=(0,l.Z)(r);function r(){var e;(0,n.Z)(this,r);for(var o=arguments.length,a=new Array(o),c=0;c<o;c++)a[c]=arguments[c];return e=i.call.apply(i,[this].concat(a)),t((0,s.Z)(e)),e}return(0,a.Z)(r)}(e);return{F:i,d:[{kind:"method",key:"renderRipple",value:function(){return this.noninteractive?"":(0,h.Z)((0,u.Z)(i.prototype),"renderRipple",this).call(this)}},{kind:"get",static:!0,key:"styles",value:function(){return[v.W,(0,f.iv)(r||(r=(0,o.Z)([":host{padding-left:var(--mdc-list-side-padding-left,var(--mdc-list-side-padding,20px));padding-right:var(--mdc-list-side-padding-right,var(--mdc-list-side-padding,20px))}:host([graphic=avatar]:not([twoLine])),:host([graphic=icon]:not([twoLine])){height:48px}span.material-icons:first-of-type{margin-inline-start:0px!important;margin-inline-end:var(--mdc-list-item-graphic-margin,16px)!important;direction:var(--direction)}span.material-icons:last-of-type{margin-inline-start:auto!important;margin-inline-end:0px!important;direction:var(--direction)}.mdc-deprecated-list-item__meta{display:var(--mdc-list-item-meta-display);align-items:center}:host([multiline-secondary]){height:auto}:host([multiline-secondary]) .mdc-deprecated-list-item__text{padding:8px 0}:host([multiline-secondary]) .mdc-deprecated-list-item__secondary-text{text-overflow:initial;white-space:normal;overflow:auto;display:inline-block;margin-top:10px}:host([multiline-secondary]) .mdc-deprecated-list-item__primary-text{margin-top:10px}:host([multiline-secondary]) .mdc-deprecated-list-item__secondary-text::before{display:none}:host([multiline-secondary]) .mdc-deprecated-list-item__primary-text::before{display:none}:host([disabled]){color:var(--disabled-text-color)}:host([noninteractive]){pointer-events:unset}"])))]}}]}}),p.K)},60010:function(t,e,i){var r,o,a,n,s,c=i(88962),l=i(33368),d=i(71650),h=i(82390),u=i(69205),p=i(70906),v=i(91808),f=i(34541),m=i(47838),g=(i(97393),i(68144)),y=i(95260),b=i(25516),k=i(70518),w=i(87744),x=(i(2315),i(48932),i(11654));(0,v.Z)([(0,y.Mo)("hass-subpage")],(function(t,e){var i=function(e){(0,u.Z)(r,e);var i=(0,p.Z)(r);function r(){var e;(0,d.Z)(this,r);for(var o=arguments.length,a=new Array(o),n=0;n<o;n++)a[n]=arguments[n];return e=i.call.apply(i,[this].concat(a)),t((0,h.Z)(e)),e}return(0,l.Z)(r)}(e);return{F:i,d:[{kind:"field",decorators:[(0,y.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,y.Cb)()],key:"header",value:void 0},{kind:"field",decorators:[(0,y.Cb)({type:Boolean,attribute:"main-page"})],key:"mainPage",value:function(){return!1}},{kind:"field",decorators:[(0,y.Cb)({type:String,attribute:"back-path"})],key:"backPath",value:void 0},{kind:"field",decorators:[(0,y.Cb)()],key:"backCallback",value:void 0},{kind:"field",decorators:[(0,y.Cb)({type:Boolean,reflect:!0})],key:"narrow",value:function(){return!1}},{kind:"field",decorators:[(0,y.Cb)({type:Boolean})],key:"supervisor",value:function(){return!1}},{kind:"field",decorators:[(0,b.i)(".content")],key:"_savedScrollPos",value:void 0},{kind:"method",key:"willUpdate",value:function(t){if((0,f.Z)((0,m.Z)(i.prototype),"willUpdate",this).call(this,t),t.has("hass")){var e=t.get("hass");e&&e.locale===this.hass.locale||(0,k.X)(this,"rtl",(0,w.HE)(this.hass))}}},{kind:"method",key:"render",value:function(){var t;return(0,g.dy)(r||(r=(0,c.Z)([' <div class="toolbar"> ',' <div class="main-title"><slot name="header">','</slot></div> <slot name="toolbar-icon"></slot> </div> <div class="content ha-scrollbar" @scroll="','"> <slot></slot> </div> <div id="fab"> <slot name="fab"></slot> </div> '])),this.mainPage||null!==(t=history.state)&&void 0!==t&&t.root?(0,g.dy)(o||(o=(0,c.Z)([' <ha-menu-button .hassio="','" .hass="','" .narrow="','"></ha-menu-button> '])),this.supervisor,this.hass,this.narrow):this.backPath?(0,g.dy)(a||(a=(0,c.Z)([' <a href="','"> <ha-icon-button-arrow-prev .hass="','"></ha-icon-button-arrow-prev> </a> '])),this.backPath,this.hass):(0,g.dy)(n||(n=(0,c.Z)([' <ha-icon-button-arrow-prev .hass="','" @click="','"></ha-icon-button-arrow-prev> '])),this.hass,this._backTapped),this.header,this._saveScrollPos)}},{kind:"method",decorators:[(0,y.hO)({passive:!0})],key:"_saveScrollPos",value:function(t){this._savedScrollPos=t.target.scrollTop}},{kind:"method",key:"_backTapped",value:function(){this.backCallback?this.backCallback():history.back()}},{kind:"get",static:!0,key:"styles",value:function(){return[x.$c,(0,g.iv)(s||(s=(0,c.Z)([":host{display:block;height:100%;background-color:var(--primary-background-color);overflow:hidden;position:relative}:host([narrow]){width:100%;position:fixed}.toolbar{display:flex;align-items:center;font-size:20px;height:var(--header-height);padding:8px 12px;pointer-events:none;background-color:var(--app-header-background-color);font-weight:400;color:var(--app-header-text-color,#fff);border-bottom:var(--app-header-border-bottom,none);box-sizing:border-box}@media (max-width:599px){.toolbar{padding:4px}}.toolbar a{color:var(--sidebar-text-color);text-decoration:none}::slotted([slot=toolbar-icon]),ha-icon-button-arrow-prev,ha-menu-button{pointer-events:auto;color:var(--sidebar-icon-color)}.main-title{margin:0 0 0 24px;line-height:20px;flex-grow:1}.content{position:relative;width:100%;height:calc(100% - 1px - var(--header-height));overflow-y:auto;overflow:auto;-webkit-overflow-scrolling:touch}#fab{position:absolute;right:calc(16px + env(safe-area-inset-right));bottom:calc(16px + env(safe-area-inset-bottom));z-index:1}:host([narrow]) #fab.tabs{bottom:calc(84px + env(safe-area-inset-bottom))}#fab[is-wide]{bottom:24px;right:24px}:host([rtl]) #fab{right:auto;left:calc(16px + env(safe-area-inset-left))}:host([rtl][is-wide]) #fab{bottom:24px;left:24px;right:auto}"])))]}}]}}),g.oi)},30247:function(t,e,i){i.r(e);var r,o,a,n,s,c=i(88962),l=i(53709),d=i(40039),h=i(33368),u=i(71650),p=i(82390),v=i(69205),f=i(70906),m=i(91808),g=i(34541),y=i(47838),b=(i(97393),i(87438),i(46798),i(9849),i(22890),i(37313),i(51358),i(78399),i(5239),i(56086),i(47884),i(81912),i(64584),i(41483),i(12367),i(9454),i(98490),i(68144)),k=i(95260),w=i(14516),x=i(7323),Z=i(86977),_=i(83849),L=i(15493),A=(i(22098),i(84431),i(45339)),C=(i(60010),i(73826)),M=(i(67432),i(47084),i(47181)),S=function(){return Promise.all([i.e(3298),i.e(28597),i.e(88841)]).then(i.bind(i,88841))},P=function(){return Promise.all([i.e(3298),i.e(28597),i.e(50529),i.e(98770)]).then(i.bind(i,98770))},I=function(t){(0,M.B)(t,"show-dialog",{dialogTag:"dialog-system-information",dialogImport:P,dialogParams:void 0})};(0,m.Z)([(0,k.Mo)("ha-config-repairs-dashboard")],(function(t,e){var i=function(e){(0,v.Z)(r,e);var i=(0,f.Z)(r);function r(){var e;(0,u.Z)(this,r);for(var o=arguments.length,a=new Array(o),n=0;n<o;n++)a[n]=arguments[n];return e=i.call.apply(i,[this].concat(a)),t((0,p.Z)(e)),e}return(0,h.Z)(r)}(e);return{F:i,d:[{kind:"field",decorators:[(0,k.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,k.Cb)({type:Boolean})],key:"narrow",value:void 0},{kind:"field",decorators:[(0,k.SB)()],key:"_repairsIssues",value:function(){return[]}},{kind:"field",decorators:[(0,k.SB)()],key:"_showIgnored",value:function(){return!1}},{kind:"field",key:"_getFilteredIssues",value:function(){return(0,w.Z)((function(t,e){return t?e:e.filter((function(t){return!t.ignored}))}))}},{kind:"method",key:"connectedCallback",value:function(){(0,g.Z)((0,y.Z)(i.prototype),"connectedCallback",this).call(this),"system-health"===(0,L.io)("dialog")&&((0,_.c)("/config/repairs",{replace:!0}),I(this))}},{kind:"method",key:"hassSubscribe",value:function(){var t=this;return[(0,A.$X)(this.hass.connection,(function(e){t._repairsIssues=e.issues.sort((function(t,e){return A.wC[t.severity]-A.wC[e.severity]}));var i,r=new Set,o=(0,d.Z)(t._repairsIssues);try{for(o.s();!(i=o.n()).done;){var a=i.value;r.add(a.domain)}}catch(n){o.e(n)}finally{o.f()}t.hass.loadBackendTranslation("issues",(0,l.Z)(r))}))]}},{kind:"method",key:"render",value:function(){var t=this._getFilteredIssues(this._showIgnored,this._repairsIssues);return(0,b.dy)(r||(r=(0,c.Z)([' <hass-subpage back-path="/config/system" .hass="','" .narrow="','" .header="','"> <div slot="toolbar-icon"> <ha-button-menu multi> <ha-icon-button slot="trigger" .label="','" .path="','"></ha-icon-button> <ha-check-list-item left @request-selected="','" .selected="','"> ',' </ha-check-list-item> <li divider role="separator"></li> ',' <mwc-list-item @request-selected="','"> ',' </mwc-list-item> </ha-button-menu> </div> <div class="content"> <ha-card outlined> <div class="card-content"> '," </div> </ha-card> </div> </hass-subpage> "])),this.hass,this.narrow,this.hass.localize("ui.panel.config.repairs.caption"),this.hass.localize("ui.common.menu"),"M12,16A2,2 0 0,1 14,18A2,2 0 0,1 12,20A2,2 0 0,1 10,18A2,2 0 0,1 12,16M12,10A2,2 0 0,1 14,12A2,2 0 0,1 12,14A2,2 0 0,1 10,12A2,2 0 0,1 12,10M12,4A2,2 0 0,1 14,6A2,2 0 0,1 12,8A2,2 0 0,1 10,6A2,2 0 0,1 12,4Z",this._toggleIgnored,this._showIgnored,this.hass.localize("ui.panel.config.repairs.show_ignored"),(0,x.p)(this.hass,"system_health")||(0,x.p)(this.hass,"hassio")?(0,b.dy)(o||(o=(0,c.Z)([' <mwc-list-item @request-selected="','"> '," </mwc-list-item> "])),this._showSystemInformationDialog,this.hass.localize("ui.panel.config.repairs.system_information")):"",this._showIntegrationStartupDialog,this.hass.localize("ui.panel.config.repairs.integration_startup_time"),t.length?(0,b.dy)(a||(a=(0,c.Z)([' <ha-config-repairs .hass="','" .narrow="','" .repairsIssues="','"></ha-config-repairs> '])),this.hass,this.narrow,t):(0,b.dy)(n||(n=(0,c.Z)([' <div class="no-repairs"> '," </div> "])),this.hass.localize("ui.panel.config.repairs.no_repairs")))}},{kind:"method",key:"_showSystemInformationDialog",value:function(t){(0,Z.Q)(t)&&I(this)}},{kind:"method",key:"_showIntegrationStartupDialog",value:function(t){var e;(0,Z.Q)(t)&&(e=this,(0,M.B)(e,"show-dialog",{dialogTag:"dialog-integration-startup",dialogImport:S,dialogParams:{}}))}},{kind:"method",key:"_toggleIgnored",value:function(t){"property"===t.detail.source&&(this._showIgnored=!this._showIgnored)}},{kind:"field",static:!0,key:"styles",value:function(){return(0,b.iv)(s||(s=(0,c.Z)([".content{padding:28px 20px 0;max-width:1040px;margin:0 auto}ha-card{max-width:600px;margin:0 auto;height:100%;justify-content:space-between;flex-direction:column;display:flex;margin-bottom:max(24px,env(safe-area-inset-bottom))}.card-content{display:flex;justify-content:space-between;flex-direction:column;padding:0}.no-repairs{padding:16px}li[divider]{border-bottom-color:var(--divider-color)}"])))}}]}}),(0,C.f)(b.oi))}}]);
//# sourceMappingURL=49082.IWAuteq55Pk.js.map