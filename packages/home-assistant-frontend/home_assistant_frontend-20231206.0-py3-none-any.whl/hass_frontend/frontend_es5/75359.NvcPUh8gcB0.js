"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[75359],{76680:function(t,e,i){function a(t){return void 0===t||Array.isArray(t)?t:[t]}i.d(e,{r:function(){return a}})},55642:function(t,e,i){i.d(e,{h:function(){return c}});var a=i(68990),n=i(71650),o=i(33368),r=i(69205),s=i(70906),l=(i(51467),i(46798),i(9849),i(50289),i(94167),i(82073),i(68144)),d=i(57835),c=(0,d.XM)(function(t){(0,r.Z)(i,t);var e=(0,s.Z)(i);function i(t){var a;if((0,n.Z)(this,i),(a=e.call(this,t))._element=void 0,t.type!==d.pX.CHILD)throw new Error("dynamicElementDirective can only be used in content bindings");return a}return(0,o.Z)(i,[{key:"update",value:function(t,e){var i=this,n=(0,a.Z)(e,2),o=n[0],r=n[1];return this._element&&this._element.localName===o?(r&&Object.entries(r).forEach((function(t){var e=(0,a.Z)(t,2),n=e[0],o=e[1];i._element[n]=o})),l.Jb):this.render(o,r)}},{key:"render",value:function(t,e){var i=this;return this._element=document.createElement(t),e&&Object.entries(e).forEach((function(t){var e=(0,a.Z)(t,2),n=e[0],o=e[1];i._element[n]=o})),this._element}}]),i}(d.Xe))},22311:function(t,e,i){i.d(e,{N:function(){return n}});var a=i(58831),n=function(t){return(0,a.M)(t.entity_id)}},40095:function(t,e,i){i.d(e,{e:function(){return a}});var a=function(t,e){return n(t.attributes,e)},n=function(t,e){return 0!=(t.supported_features&e)}},83447:function(t,e,i){i.d(e,{l:function(){return a}});i(10999),i(52117),i(63789),i(82479),i(94570),i(91989),i(24074),i(46798);var a=function(t){var e,i=arguments.length>1&&void 0!==arguments[1]?arguments[1]:"_",a="àáâäæãåāăąçćčđďèéêëēėęěğǵḧîïíīįìıİłḿñńǹňôöòóœøōõőṕŕřßśšşșťțûüùúūǘůűųẃẍÿýžźż·",n="aaaaaaaaaacccddeeeeeeeegghiiiiiiiilmnnnnoooooooooprrsssssttuuuuuuuuuwxyyzzz".concat(i),o=new RegExp(a.split("").join("|"),"g");return""===t?e="":""===(e=t.toString().toLowerCase().replace(o,(function(t){return n.charAt(a.indexOf(t))})).replace(/(\d),(?=\d)/g,"$1").replace(/[^a-z0-9]+/g,i).replace(new RegExp("(".concat(i,")\\1+"),"g"),"$1").replace(new RegExp("^".concat(i,"+")),"").replace(new RegExp("".concat(i,"+$")),""))&&(e="unknown"),e}},9381:function(t,e,i){var a,n,o,r,s=i(93359),l=i(88962),d=i(33368),c=i(71650),u=i(82390),h=i(69205),v=i(70906),p=i(91808),m=(i(97393),i(68144)),f=i(95260),_=i(83448),g=i(47181),b=(i(10983),i(52039),{info:"M11,9H13V7H11M12,20C7.59,20 4,16.41 4,12C4,7.59 7.59,4 12,4C16.41,4 20,7.59 20,12C20,16.41 16.41,20 12,20M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M11,17H13V11H11V17Z",warning:"M12,2L1,21H23M12,6L19.53,19H4.47M11,10V14H13V10M11,16V18H13V16",error:"M11,15H13V17H11V15M11,7H13V13H11V7M12,2C6.47,2 2,6.5 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M12,20A8,8 0 0,1 4,12A8,8 0 0,1 12,4A8,8 0 0,1 20,12A8,8 0 0,1 12,20Z",success:"M20,12A8,8 0 0,1 12,20A8,8 0 0,1 4,12A8,8 0 0,1 12,4C12.76,4 13.5,4.11 14.2,4.31L15.77,2.74C14.61,2.26 13.34,2 12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12M7.91,10.08L6.5,11.5L11,16L21,6L19.59,4.58L11,13.17L7.91,10.08Z"});(0,p.Z)([(0,f.Mo)("ha-alert")],(function(t,e){var i=function(e){(0,h.Z)(a,e);var i=(0,v.Z)(a);function a(){var e;(0,c.Z)(this,a);for(var n=arguments.length,o=new Array(n),r=0;r<n;r++)o[r]=arguments[r];return e=i.call.apply(i,[this].concat(o)),t((0,u.Z)(e)),e}return(0,d.Z)(a)}(e);return{F:i,d:[{kind:"field",decorators:[(0,f.Cb)()],key:"title",value:function(){return""}},{kind:"field",decorators:[(0,f.Cb)({attribute:"alert-type"})],key:"alertType",value:function(){return"info"}},{kind:"field",decorators:[(0,f.Cb)({type:Boolean})],key:"dismissable",value:function(){return!1}},{kind:"method",key:"render",value:function(){return(0,m.dy)(a||(a=(0,l.Z)([' <div class="issue-type ','" role="alert"> <div class="icon ','"> <slot name="icon"> <ha-svg-icon .path="','"></ha-svg-icon> </slot> </div> <div class="content"> <div class="main-content"> ',' <slot></slot> </div> <div class="action"> <slot name="action"> '," </slot> </div> </div> </div> "])),(0,_.$)((0,s.Z)({},this.alertType,!0)),this.title?"":"no-title",b[this.alertType],this.title?(0,m.dy)(n||(n=(0,l.Z)(['<div class="title">',"</div>"])),this.title):"",this.dismissable?(0,m.dy)(o||(o=(0,l.Z)(['<ha-icon-button @click="','" label="Dismiss alert" .path="','"></ha-icon-button>'])),this._dismiss_clicked,"M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z"):"")}},{kind:"method",key:"_dismiss_clicked",value:function(){(0,g.B)(this,"alert-dismissed-clicked")}},{kind:"field",static:!0,key:"styles",value:function(){return(0,m.iv)(r||(r=(0,l.Z)(['.issue-type{position:relative;padding:8px;display:flex}.issue-type::after{position:absolute;top:0;right:0;bottom:0;left:0;opacity:.12;pointer-events:none;content:"";border-radius:4px}.icon{z-index:1}.icon.no-title{align-self:center}.content{display:flex;justify-content:space-between;align-items:center;width:100%;text-align:var(--float-start)}.action{z-index:1;width:min-content;--mdc-theme-primary:var(--primary-text-color)}.main-content{overflow-wrap:anywhere;word-break:break-word;margin-left:8px;margin-right:0;margin-inline-start:8px;margin-inline-end:0;direction:var(--direction)}.title{margin-top:2px;font-weight:700}.action ha-icon-button,.action mwc-button{--mdc-theme-primary:var(--primary-text-color);--mdc-icon-button-size:36px}.issue-type.info>.icon{color:var(--info-color)}.issue-type.info::after{background-color:var(--info-color)}.issue-type.warning>.icon{color:var(--warning-color)}.issue-type.warning::after{background-color:var(--warning-color)}.issue-type.error>.icon{color:var(--error-color)}.issue-type.error::after{background-color:var(--error-color)}.issue-type.success>.icon{color:var(--success-color)}.issue-type.success::after{background-color:var(--success-color)}'])))}}]}}),m.oi)},34821:function(t,e,i){i.d(e,{i:function(){return k}});var a,n,o,r=i(33368),s=i(71650),l=i(82390),d=i(69205),c=i(70906),u=i(91808),h=i(34541),v=i(47838),p=i(88962),m=(i(97393),i(91989),i(87762)),f=i(91632),_=i(68144),g=i(95260),b=i(74265),y=(i(10983),["button","ha-list-item"]),k=function(t,e){var i;return(0,_.dy)(a||(a=(0,p.Z)([' <div class="header_title">','</div> <ha-icon-button .label="','" .path="','" dialogAction="close" class="header_button"></ha-icon-button> '])),e,null!==(i=null==t?void 0:t.localize("ui.dialogs.generic.close"))&&void 0!==i?i:"Close","M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z")};(0,u.Z)([(0,g.Mo)("ha-dialog")],(function(t,e){var i=function(e){(0,d.Z)(a,e);var i=(0,c.Z)(a);function a(){var e;(0,s.Z)(this,a);for(var n=arguments.length,o=new Array(n),r=0;r<n;r++)o[r]=arguments[r];return e=i.call.apply(i,[this].concat(o)),t((0,l.Z)(e)),e}return(0,r.Z)(a)}(e);return{F:i,d:[{kind:"field",key:b.gA,value:void 0},{kind:"method",key:"scrollToPos",value:function(t,e){var i;null===(i=this.contentElement)||void 0===i||i.scrollTo(t,e)}},{kind:"method",key:"renderHeading",value:function(){return(0,_.dy)(n||(n=(0,p.Z)(['<slot name="heading"> '," </slot>"])),(0,h.Z)((0,v.Z)(i.prototype),"renderHeading",this).call(this))}},{kind:"method",key:"firstUpdated",value:function(){var t;(0,h.Z)((0,v.Z)(i.prototype),"firstUpdated",this).call(this),this.suppressDefaultPressSelector=[this.suppressDefaultPressSelector,y].join(", "),this._updateScrolledAttribute(),null===(t=this.contentElement)||void 0===t||t.addEventListener("scroll",this._onScroll,{passive:!0})}},{kind:"method",key:"disconnectedCallback",value:function(){(0,h.Z)((0,v.Z)(i.prototype),"disconnectedCallback",this).call(this),this.contentElement.removeEventListener("scroll",this._onScroll)}},{kind:"field",key:"_onScroll",value:function(){var t=this;return function(){t._updateScrolledAttribute()}}},{kind:"method",key:"_updateScrolledAttribute",value:function(){this.contentElement&&this.toggleAttribute("scrolled",0!==this.contentElement.scrollTop)}},{kind:"field",static:!0,key:"styles",value:function(){return[f.W,(0,_.iv)(o||(o=(0,p.Z)([":host([scrolled]) ::slotted(ha-dialog-header){border-bottom:1px solid var(--mdc-dialog-scroll-divider-color,rgba(0,0,0,.12))}.mdc-dialog{--mdc-dialog-scroll-divider-color:var(\n          --dialog-scroll-divider-color,\n          var(--divider-color)\n        );z-index:var(--dialog-z-index,8);-webkit-backdrop-filter:var(--dialog-backdrop-filter,none);backdrop-filter:var(--dialog-backdrop-filter,none);--mdc-dialog-box-shadow:var(--dialog-box-shadow, none);--mdc-typography-headline6-font-weight:400;--mdc-typography-headline6-font-size:1.574rem}.mdc-dialog__actions{justify-content:var(--justify-action-buttons,flex-end);padding-bottom:max(env(safe-area-inset-bottom),24px)}.mdc-dialog__actions span:first-child{flex:var(--secondary-action-button-flex,unset)}.mdc-dialog__actions span:nth-child(2){flex:var(--primary-action-button-flex,unset)}.mdc-dialog__container{align-items:var(--vertical-align-dialog,center)}.mdc-dialog__title{padding:24px 24px 0 24px;text-overflow:ellipsis;overflow:hidden}.mdc-dialog__actions{padding:12px 24px 12px 24px}.mdc-dialog__title::before{display:block;height:0px}.mdc-dialog .mdc-dialog__content{position:var(--dialog-content-position,relative);padding:var(--dialog-content-padding,24px)}:host([hideactions]) .mdc-dialog .mdc-dialog__content{padding-bottom:max(var(--dialog-content-padding,24px),env(safe-area-inset-bottom))}.mdc-dialog .mdc-dialog__surface{position:var(--dialog-surface-position,relative);top:var(--dialog-surface-top);margin-top:var(--dialog-surface-margin-top);min-height:var(--mdc-dialog-min-height,auto);border-radius:var(--ha-dialog-border-radius,28px)}:host([flexContent]) .mdc-dialog .mdc-dialog__content{display:flex;flex-direction:column}.header_title{margin-right:32px;margin-inline-end:32px;margin-inline-start:initial;direction:var(--direction)}.header_button{position:absolute;right:16px;top:14px;text-decoration:none;color:inherit;inset-inline-start:initial;inset-inline-end:16px;direction:var(--direction)}.dialog-actions{inset-inline-start:initial!important;inset-inline-end:0px!important;direction:var(--direction)}"])))]}}]}}),m.M)},57630:function(t,e,i){i.r(e),i.d(e,{DialogLovelaceDashboardDetail:function(){return A}});var a,n,o,r,s,l=i(99312),d=i(81043),c=i(53709),u=i(88962),h=i(33368),v=i(71650),p=i(82390),m=i(69205),f=i(70906),_=i(91808),g=(i(97393),i(11451),i(22859),i(63789),i(99397),i(85717),i(40271),i(60163),i(47704),i(68144)),b=i(95260),y=i(14516),k=i(47181),x=i(83447),Z=i(34821),w=(i(68331),i(1887)),L=i(11654),A=(0,_.Z)([(0,b.Mo)("dialog-lovelace-dashboard-detail")],(function(t,e){var i,_,A=function(e){(0,m.Z)(a,e);var i=(0,f.Z)(a);function a(){var e;(0,v.Z)(this,a);for(var n=arguments.length,o=new Array(n),r=0;r<n;r++)o[r]=arguments[r];return e=i.call.apply(i,[this].concat(o)),t((0,p.Z)(e)),e}return(0,h.Z)(a)}(e);return{F:A,d:[{kind:"field",decorators:[(0,b.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,b.SB)()],key:"_params",value:void 0},{kind:"field",decorators:[(0,b.SB)()],key:"_urlPathChanged",value:function(){return!1}},{kind:"field",decorators:[(0,b.SB)()],key:"_data",value:void 0},{kind:"field",decorators:[(0,b.SB)()],key:"_error",value:void 0},{kind:"field",decorators:[(0,b.SB)()],key:"_submitting",value:function(){return!1}},{kind:"method",key:"showDialog",value:function(t){this._params=t,this._error=void 0,this._urlPathChanged=!1,this._params.dashboard?this._data=this._params.dashboard:this._data={show_in_sidebar:!0,icon:void 0,title:"",require_admin:!1,mode:"storage"}}},{kind:"method",key:"closeDialog",value:function(){this._params=void 0,this._data=void 0,(0,k.B)(this,"dialog-closed",{dialog:this.localName})}},{kind:"method",key:"render",value:function(){var t,e;if(!this._params||!this._data)return g.Ld;var i=this.hass.defaultPanel,s=!this._data.title||!this._data.title.trim();return(0,g.dy)(a||(a=(0,u.Z)([' <ha-dialog open @closed="','" scrimClickAction escapeKeyAction .heading="','"> <div> '," </div> ",' <mwc-button slot="primaryAction" @click="','" .disabled="','" dialogInitialFocus> '," </mwc-button> </ha-dialog> "])),this.closeDialog,(0,Z.i)(this.hass,this._params.urlPath?this._data.title||this.hass.localize("ui.panel.config.lovelace.dashboards.detail.edit_dashboard"):this.hass.localize("ui.panel.config.lovelace.dashboards.detail.new_dashboard")),this._params.dashboard&&!this._params.dashboard.id?this.hass.localize("ui.panel.config.lovelace.dashboards.cant_edit_yaml"):"lovelace"===this._params.urlPath?this.hass.localize("ui.panel.config.lovelace.dashboards.cant_edit_default"):(0,g.dy)(n||(n=(0,u.Z)([' <ha-form .schema="','" .data="','" .hass="','" .error="','" .computeLabel="','" @value-changed="','"></ha-form> '])),this._schema(this._params,this.hass.userData),this._data,this.hass,this._error,this._computeLabel,this._valueChanged),this._params.urlPath?(0,g.dy)(o||(o=(0,u.Z)([" ",' <mwc-button slot="secondaryAction" @click="','" .disabled="','"> '," </mwc-button> "])),null!==(t=this._params.dashboard)&&void 0!==t&&t.id?(0,g.dy)(r||(r=(0,u.Z)([' <mwc-button slot="secondaryAction" class="warning" @click="','" .disabled="','"> '," </mwc-button> "])),this._deleteDashboard,this._submitting,this.hass.localize("ui.panel.config.lovelace.dashboards.detail.delete")):"",this._toggleDefault,"lovelace"===this._params.urlPath&&"lovelace"===i,this._params.urlPath===i?this.hass.localize("ui.panel.config.lovelace.dashboards.detail.remove_default"):this.hass.localize("ui.panel.config.lovelace.dashboards.detail.set_default")):"",this._updateDashboard,this._error&&"url_path"in this._error||s||this._submitting,this._params.urlPath?null!==(e=this._params.dashboard)&&void 0!==e&&e.id?this.hass.localize("ui.panel.config.lovelace.dashboards.detail.update"):this.hass.localize("ui.common.close"):this.hass.localize("ui.panel.config.lovelace.dashboards.detail.create"))}},{kind:"field",key:"_schema",value:function(){return(0,y.Z)((function(t,e){return[{name:"title",required:!0,selector:{text:{}}},{name:"icon",required:!0,selector:{icon:{}}}].concat((0,c.Z)(!t.dashboard&&null!=e&&e.showAdvanced?[{name:"url_path",required:!0,selector:{text:{}}}]:[]),[{name:"require_admin",required:!0,selector:{boolean:{}}},{name:"show_in_sidebar",required:!0,selector:{boolean:{}}}])}))}},{kind:"field",key:"_computeLabel",value:function(){var t=this;return function(e){return t.hass.localize("ui.panel.config.lovelace.dashboards.detail.".concat("show_in_sidebar"===e.name?"show_sidebar":"url_path"===e.name?"url":e.name))}}},{kind:"method",key:"_valueChanged",value:function(t){var e,i;this._error=void 0;var a=t.detail.value;a.url_path!==(null===(e=this._data)||void 0===e?void 0:e.url_path)&&(this._urlPathChanged=!0,a.url_path&&"lovelace"!==a.url_path&&/^[a-zA-Z0-9_-]+-[a-zA-Z0-9_-]+$/.test(a.url_path)||(this._error={url_path:this.hass.localize("ui.panel.config.lovelace.dashboards.detail.url_error_msg")})),a.title!==(null===(i=this._data)||void 0===i?void 0:i.title)?(this._data=a,this._fillUrlPath(a.title)):this._data=a}},{kind:"method",key:"_fillUrlPath",value:function(t){var e;if(!(null!==(e=this.hass.userData)&&void 0!==e&&e.showAdvanced&&this._urlPathChanged||!t)){var i=(0,x.l)(t,"-");this._data=Object.assign(Object.assign({},this._data),{},{url_path:i.includes("-")?i:"dashboard-".concat(i)})}}},{kind:"method",key:"_toggleDefault",value:function(){var t,e=null===(t=this._params)||void 0===t?void 0:t.urlPath;e&&(0,w.CM)(this,e===this.hass.defaultPanel?w.te:e)}},{kind:"method",key:"_updateDashboard",value:(_=(0,d.Z)((0,l.Z)().mark((function t(){var e,i,a;return(0,l.Z)().wrap((function(t){for(;;)switch(t.prev=t.next){case 0:if(null===(e=this._params)||void 0===e||!e.urlPath||null!==(i=this._params.dashboard)&&void 0!==i&&i.id||this.closeDialog(),this._submitting=!0,t.prev=2,!this._params.dashboard){t.next=9;break}return a={require_admin:this._data.require_admin,show_in_sidebar:this._data.show_in_sidebar,icon:this._data.icon||void 0,title:this._data.title},t.next=7,this._params.updateDashboard(a);case 7:t.next=11;break;case 9:return t.next=11,this._params.createDashboard(this._data);case 11:this.closeDialog(),t.next=17;break;case 14:t.prev=14,t.t0=t.catch(2),this._error={base:(null===t.t0||void 0===t.t0?void 0:t.t0.message)||"Unknown error"};case 17:return t.prev=17,this._submitting=!1,t.finish(17);case 20:case"end":return t.stop()}}),t,this,[[2,14,17,20]])}))),function(){return _.apply(this,arguments)})},{kind:"method",key:"_deleteDashboard",value:(i=(0,d.Z)((0,l.Z)().mark((function t(){return(0,l.Z)().wrap((function(t){for(;;)switch(t.prev=t.next){case 0:return this._submitting=!0,t.prev=1,t.next=4,this._params.removeDashboard();case 4:if(!t.sent){t.next=6;break}this.closeDialog();case 6:return t.prev=6,this._submitting=!1,t.finish(6);case 9:case"end":return t.stop()}}),t,this,[[1,,6,9]])}))),function(){return i.apply(this,arguments)})},{kind:"get",static:!0,key:"styles",value:function(){return[L.yu,(0,g.iv)(s||(s=(0,u.Z)([""])))]}}]}}),g.oi)}}]);
//# sourceMappingURL=75359.NvcPUh8gcB0.js.map