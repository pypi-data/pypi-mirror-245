"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[70975],{34821:function(i,o,t){t.d(o,{i:function(){return x}});var e,n,a,l=t(33368),r=t(71650),d=t(82390),c=t(69205),s=t(70906),u=t(91808),h=t(34541),p=t(47838),g=t(88962),m=(t(97393),t(91989),t(87762)),f=t(91632),v=t(68144),k=t(95260),_=t(74265),b=(t(10983),["button","ha-list-item"]),x=function(i,o){var t;return(0,v.dy)(e||(e=(0,g.Z)([' <div class="header_title">','</div> <ha-icon-button .label="','" .path="','" dialogAction="close" class="header_button"></ha-icon-button> '])),o,null!==(t=null==i?void 0:i.localize("ui.dialogs.generic.close"))&&void 0!==t?t:"Close","M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z")};(0,u.Z)([(0,k.Mo)("ha-dialog")],(function(i,o){var t=function(o){(0,c.Z)(e,o);var t=(0,s.Z)(e);function e(){var o;(0,r.Z)(this,e);for(var n=arguments.length,a=new Array(n),l=0;l<n;l++)a[l]=arguments[l];return o=t.call.apply(t,[this].concat(a)),i((0,d.Z)(o)),o}return(0,l.Z)(e)}(o);return{F:t,d:[{kind:"field",key:_.gA,value:void 0},{kind:"method",key:"scrollToPos",value:function(i,o){var t;null===(t=this.contentElement)||void 0===t||t.scrollTo(i,o)}},{kind:"method",key:"renderHeading",value:function(){return(0,v.dy)(n||(n=(0,g.Z)(['<slot name="heading"> '," </slot>"])),(0,h.Z)((0,p.Z)(t.prototype),"renderHeading",this).call(this))}},{kind:"method",key:"firstUpdated",value:function(){var i;(0,h.Z)((0,p.Z)(t.prototype),"firstUpdated",this).call(this),this.suppressDefaultPressSelector=[this.suppressDefaultPressSelector,b].join(", "),this._updateScrolledAttribute(),null===(i=this.contentElement)||void 0===i||i.addEventListener("scroll",this._onScroll,{passive:!0})}},{kind:"method",key:"disconnectedCallback",value:function(){(0,h.Z)((0,p.Z)(t.prototype),"disconnectedCallback",this).call(this),this.contentElement.removeEventListener("scroll",this._onScroll)}},{kind:"field",key:"_onScroll",value:function(){var i=this;return function(){i._updateScrolledAttribute()}}},{kind:"method",key:"_updateScrolledAttribute",value:function(){this.contentElement&&this.toggleAttribute("scrolled",0!==this.contentElement.scrollTop)}},{kind:"field",static:!0,key:"styles",value:function(){return[f.W,(0,v.iv)(a||(a=(0,g.Z)([":host([scrolled]) ::slotted(ha-dialog-header){border-bottom:1px solid var(--mdc-dialog-scroll-divider-color,rgba(0,0,0,.12))}.mdc-dialog{--mdc-dialog-scroll-divider-color:var(\n          --dialog-scroll-divider-color,\n          var(--divider-color)\n        );z-index:var(--dialog-z-index,8);-webkit-backdrop-filter:var(--dialog-backdrop-filter,none);backdrop-filter:var(--dialog-backdrop-filter,none);--mdc-dialog-box-shadow:var(--dialog-box-shadow, none);--mdc-typography-headline6-font-weight:400;--mdc-typography-headline6-font-size:1.574rem}.mdc-dialog__actions{justify-content:var(--justify-action-buttons,flex-end);padding-bottom:max(env(safe-area-inset-bottom),24px)}.mdc-dialog__actions span:first-child{flex:var(--secondary-action-button-flex,unset)}.mdc-dialog__actions span:nth-child(2){flex:var(--primary-action-button-flex,unset)}.mdc-dialog__container{align-items:var(--vertical-align-dialog,center)}.mdc-dialog__title{padding:24px 24px 0 24px;text-overflow:ellipsis;overflow:hidden}.mdc-dialog__actions{padding:12px 24px 12px 24px}.mdc-dialog__title::before{display:block;height:0px}.mdc-dialog .mdc-dialog__content{position:var(--dialog-content-position,relative);padding:var(--dialog-content-padding,24px)}:host([hideactions]) .mdc-dialog .mdc-dialog__content{padding-bottom:max(var(--dialog-content-padding,24px),env(safe-area-inset-bottom))}.mdc-dialog .mdc-dialog__surface{position:var(--dialog-surface-position,relative);top:var(--dialog-surface-top);margin-top:var(--dialog-surface-margin-top);min-height:var(--mdc-dialog-min-height,auto);border-radius:var(--ha-dialog-border-radius,28px)}:host([flexContent]) .mdc-dialog .mdc-dialog__content{display:flex;flex-direction:column}.header_title{margin-right:32px;margin-inline-end:32px;margin-inline-start:initial;direction:var(--direction)}.header_button{position:absolute;right:16px;top:14px;text-decoration:none;color:inherit;inset-inline-start:initial;inset-inline-end:16px;direction:var(--direction)}.dialog-actions{inset-inline-start:initial!important;inset-inline-end:0px!important;direction:var(--direction)}"])))]}}]}}),m.M)},70975:function(i,o,t){t.r(o),t.d(o,{DialogManageCloudhook:function(){return z}});var e,n,a,l,r=t(99312),d=t(81043),c=t(88962),s=t(33368),u=t(71650),h=t(82390),p=t(69205),g=t(70906),m=t(91808),f=(t(97393),t(22859),t(47704),t(68144)),v=t(95260),k=t(47181),_=t(50577),b=t(34821),x=(t(3555),t(26765)),y=t(11654),Z=t(27322),w=t(81796),z=(0,m.Z)(null,(function(i,o){var t,m,z=function(o){(0,p.Z)(e,o);var t=(0,g.Z)(e);function e(){var o;(0,u.Z)(this,e);for(var n=arguments.length,a=new Array(n),l=0;l<n;l++)a[l]=arguments[l];return o=t.call.apply(t,[this].concat(a)),i((0,h.Z)(o)),o}return(0,s.Z)(e)}(o);return{F:z,d:[{kind:"field",key:"hass",value:void 0},{kind:"field",decorators:[(0,v.SB)()],key:"_params",value:void 0},{kind:"field",decorators:[(0,v.IO)("ha-textfield")],key:"_input",value:void 0},{kind:"method",key:"showDialog",value:function(i){this._params=i}},{kind:"method",key:"closeDialog",value:function(){this._params=void 0,(0,k.B)(this,"dialog-closed",{dialog:this.localName})}},{kind:"method",key:"render",value:function(){if(!this._params)return f.Ld;var i=this._params,o=i.webhook,t=i.cloudhook,l="automation"===o.domain?(0,Z.R)(this.hass,"/docs/automation/trigger/#webhook-trigger"):(0,Z.R)(this.hass,"/integrations/".concat(o.domain,"/"));return(0,f.dy)(e||(e=(0,c.Z)([' <ha-dialog open hideActions @closed="','" .heading="','"> <div> <p> ',' <br> <a href="','" target="_blank" rel="noreferrer"> ',' <ha-svg-icon .path="','"></ha-svg-icon> </a> </p> <ha-textfield .label="','" .value="','" iconTrailing readOnly="readOnly" @click="','"> <ha-icon-button @click="','" slot="trailingIcon" .path="','"></ha-icon-button> </ha-textfield> </div> <a href="','" target="_blank" rel="noreferrer" slot="secondaryAction"> <mwc-button> ',' </mwc-button> </a> <mwc-button @click="','" slot="primaryAction"> '," </mwc-button> </ha-dialog> "])),this.closeDialog,(0,b.i)(this.hass,this.hass.localize("ui.panel.config.cloud.dialog_cloudhook.webhook_for",{name:o.name})),t.managed?(0,f.dy)(a||(a=(0,c.Z)([" ",' <button class="link" @click="','"> ',"</button>. "])),this.hass.localize("ui.panel.config.cloud.dialog_cloudhook.info_disable_webhook"),this._disableWebhook,this.hass.localize("ui.panel.config.cloud.dialog_cloudhook.link_disable_webhook")):(0,f.dy)(n||(n=(0,c.Z)([" "," "])),this.hass.localize("ui.panel.config.cloud.dialog_cloudhook.managed_by_integration")),l,this.hass.localize("ui.panel.config.cloud.dialog_cloudhook.view_documentation"),"M14,3V5H17.59L7.76,14.83L9.17,16.24L19,6.41V10H21V3M19,19H5V5H12V3H5C3.89,3 3,3.9 3,5V19A2,2 0 0,0 5,21H19A2,2 0 0,0 21,19V12H19V19Z",this.hass.localize("ui.panel.config.cloud.dialog_cloudhook.public_url"),t.cloudhook_url,this.focusInput,this._copyUrl,"M19,21H8V7H19M19,5H8A2,2 0 0,0 6,7V21A2,2 0 0,0 8,23H19A2,2 0 0,0 21,21V7A2,2 0 0,0 19,5M16,1H4A2,2 0 0,0 2,3V17H4V3H16V1Z",l,this.hass.localize("ui.panel.config.cloud.dialog_cloudhook.view_documentation"),this.closeDialog,this.hass.localize("ui.panel.config.cloud.dialog_cloudhook.close"))}},{kind:"method",key:"_disableWebhook",value:(m=(0,d.Z)((0,r.Z)().mark((function i(){return(0,r.Z)().wrap((function(i){for(;;)switch(i.prev=i.next){case 0:return i.next=2,(0,x.showConfirmationDialog)(this,{title:this.hass.localize("ui.panel.config.cloud.dialog_cloudhook.confirm_disable_title"),text:this.hass.localize("ui.panel.config.cloud.dialog_cloudhook.confirm_disable_text",{name:this._params.webhook.name}),dismissText:this.hass.localize("ui.common.cancel"),confirmText:this.hass.localize("ui.common.disable"),destructive:!0});case 2:i.sent&&(this._params.disableHook(),this.closeDialog());case 4:case"end":return i.stop()}}),i,this)}))),function(){return m.apply(this,arguments)})},{kind:"method",key:"focusInput",value:function(i){i.currentTarget.select()}},{kind:"method",key:"_copyUrl",value:(t=(0,d.Z)((0,r.Z)().mark((function i(o){var t,e;return(0,r.Z)().wrap((function(i){for(;;)switch(i.prev=i.next){case 0:if(this.hass){i.next=2;break}return i.abrupt("return");case 2:return o.stopPropagation(),(t=o.target.parentElement).select(),e=this.hass.hassUrl(t.value),i.next=8,(0,_.v)(e);case 8:(0,w.C)(this,{message:this.hass.localize("ui.common.copied_clipboard")});case 9:case"end":return i.stop()}}),i,this)}))),function(i){return t.apply(this,arguments)})},{kind:"get",static:!0,key:"styles",value:function(){return[y.Qx,y.yu,(0,f.iv)(l||(l=(0,c.Z)(["ha-dialog{width:650px}ha-textfield{display:block}ha-textfield>ha-icon-button{--mdc-icon-button-size:24px;--mdc-icon-size:18px}button.link{color:var(--primary-color);text-decoration:none}a{text-decoration:none}a ha-svg-icon{--mdc-icon-size:16px}p{margin-top:0;margin-bottom:16px}"])))]}}]}}),f.oi);customElements.define("dialog-manage-cloudhook",z)},27322:function(i,o,t){t.d(o,{R:function(){return e}});t(97393),t(40271),t(60163);var e=function(i,o){return"https://".concat(i.config.version.includes("b")?"rc":i.config.version.includes("dev")?"next":"www",".home-assistant.io").concat(o)}}}]);
//# sourceMappingURL=70975.86yjheoIpNw.js.map