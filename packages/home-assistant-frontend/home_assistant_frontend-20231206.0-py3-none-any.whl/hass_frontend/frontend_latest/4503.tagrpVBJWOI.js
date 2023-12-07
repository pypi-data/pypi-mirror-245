export const id=4503;export const ids=[4503];export const modules={34821:(i,e,t)=>{t.d(e,{i:()=>u});var a=t(17463),o=t(34541),n=t(47838),s=t(87762),l=t(91632),d=t(68144),r=t(79932),c=t(74265);t(10983);const h=["button","ha-list-item"],u=(i,e)=>{var t;return d.dy` <div class="header_title">${e}</div> <ha-icon-button .label="${null!==(t=null==i?void 0:i.localize("ui.dialogs.generic.close"))&&void 0!==t?t:"Close"}" .path="${"M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z"}" dialogAction="close" class="header_button"></ha-icon-button> `};(0,a.Z)([(0,r.Mo)("ha-dialog")],(function(i,e){class t extends e{constructor(...e){super(...e),i(this)}}return{F:t,d:[{kind:"field",key:c.gA,value:void 0},{kind:"method",key:"scrollToPos",value:function(i,e){var t;null===(t=this.contentElement)||void 0===t||t.scrollTo(i,e)}},{kind:"method",key:"renderHeading",value:function(){return d.dy`<slot name="heading"> ${(0,o.Z)((0,n.Z)(t.prototype),"renderHeading",this).call(this)} </slot>`}},{kind:"method",key:"firstUpdated",value:function(){var i;(0,o.Z)((0,n.Z)(t.prototype),"firstUpdated",this).call(this),this.suppressDefaultPressSelector=[this.suppressDefaultPressSelector,h].join(", "),this._updateScrolledAttribute(),null===(i=this.contentElement)||void 0===i||i.addEventListener("scroll",this._onScroll,{passive:!0})}},{kind:"method",key:"disconnectedCallback",value:function(){(0,o.Z)((0,n.Z)(t.prototype),"disconnectedCallback",this).call(this),this.contentElement.removeEventListener("scroll",this._onScroll)}},{kind:"field",key:"_onScroll",value(){return()=>{this._updateScrolledAttribute()}}},{kind:"method",key:"_updateScrolledAttribute",value:function(){this.contentElement&&this.toggleAttribute("scrolled",0!==this.contentElement.scrollTop)}},{kind:"field",static:!0,key:"styles",value:()=>[l.W,d.iv`:host([scrolled]) ::slotted(ha-dialog-header){border-bottom:1px solid var(--mdc-dialog-scroll-divider-color,rgba(0,0,0,.12))}.mdc-dialog{--mdc-dialog-scroll-divider-color:var(
          --dialog-scroll-divider-color,
          var(--divider-color)
        );z-index:var(--dialog-z-index,8);-webkit-backdrop-filter:var(--dialog-backdrop-filter,none);backdrop-filter:var(--dialog-backdrop-filter,none);--mdc-dialog-box-shadow:var(--dialog-box-shadow, none);--mdc-typography-headline6-font-weight:400;--mdc-typography-headline6-font-size:1.574rem}.mdc-dialog__actions{justify-content:var(--justify-action-buttons,flex-end);padding-bottom:max(env(safe-area-inset-bottom),24px)}.mdc-dialog__actions span:first-child{flex:var(--secondary-action-button-flex,unset)}.mdc-dialog__actions span:nth-child(2){flex:var(--primary-action-button-flex,unset)}.mdc-dialog__container{align-items:var(--vertical-align-dialog,center)}.mdc-dialog__title{padding:24px 24px 0 24px;text-overflow:ellipsis;overflow:hidden}.mdc-dialog__actions{padding:12px 24px 12px 24px}.mdc-dialog__title::before{display:block;height:0px}.mdc-dialog .mdc-dialog__content{position:var(--dialog-content-position,relative);padding:var(--dialog-content-padding,24px)}:host([hideactions]) .mdc-dialog .mdc-dialog__content{padding-bottom:max(var(--dialog-content-padding,24px),env(safe-area-inset-bottom))}.mdc-dialog .mdc-dialog__surface{position:var(--dialog-surface-position,relative);top:var(--dialog-surface-top);margin-top:var(--dialog-surface-margin-top);min-height:var(--mdc-dialog-min-height,auto);border-radius:var(--ha-dialog-border-radius,28px)}:host([flexContent]) .mdc-dialog .mdc-dialog__content{display:flex;flex-direction:column}.header_title{margin-right:32px;margin-inline-end:32px;margin-inline-start:initial;direction:var(--direction)}.header_button{position:absolute;right:16px;top:14px;text-decoration:none;color:inherit;inset-inline-start:initial;inset-inline-end:16px;direction:var(--direction)}.dialog-actions{inset-inline-start:initial!important;inset-inline-end:0px!important;direction:var(--direction)}`]}]}}),s.M)},83927:(i,e,t)=>{var a=t(17463),o=t(8485),n=t(92038),s=t(68144),l=t(79932),d=t(47181);(0,a.Z)([(0,l.Mo)("ha-formfield")],(function(i,e){return{F:class extends e{constructor(...e){super(...e),i(this)}},d:[{kind:"method",key:"_labelClick",value:function(){const i=this.input;if(i&&(i.focus(),!i.disabled))switch(i.tagName){case"HA-CHECKBOX":i.checked=!i.checked,(0,d.B)(i,"change");break;case"HA-RADIO":i.checked=!0,(0,d.B)(i,"change");break;default:i.click()}}},{kind:"field",static:!0,key:"styles",value:()=>[n.W,s.iv`:host(:not([alignEnd])) ::slotted(ha-switch){margin-right:10px;margin-inline-end:10px;margin-inline-start:inline}.mdc-form-field>label{direction:var(--direction);margin-inline-start:0;margin-inline-end:auto;padding-inline-start:4px;padding-inline-end:0}`]}]}}),o.a)},73548:(i,e,t)=>{var a=t(17463),o=t(68144),n=t(79932);(0,a.Z)([(0,n.Mo)("ha-label")],(function(i,e){return{F:class extends e{constructor(...e){super(...e),i(this)}},d:[{kind:"method",key:"render",value:function(){return o.dy` <span class="label"> <slot name="icon"></slot> <slot></slot>  </span>`}},{kind:"get",static:!0,key:"styles",value:function(){return[o.iv`:host{--ha-label-text-color:var(--primary-text-color);--ha-label-icon-color:var(--primary-text-color);--ha-label-background-color:rgba(
            var(--rgb-primary-text-color),
            0.15
          )}.label{display:inline-flex;flex-direction:row;align-items:center;font-size:12px;font-weight:500;line-height:16px;letter-spacing:.1px;vertical-align:middle;height:32px;padding:0 16px;border-radius:18px;background-color:var(--ha-label-background-color);color:var(--ha-label-text-color);--mdc-icon-size:18px}::slotted([slot=icon]){margin-right:8px;margin-left:-8px;display:flex;color:var(--ha-label-icon-color)}span{display:inline-flex}`]}}]}}),o.oi)},43709:(i,e,t)=>{var a=t(17463),o=t(34541),n=t(47838),s=t(53464),l=t(4301),d=t(68144),r=t(79932),c=t(62359);(0,a.Z)([(0,r.Mo)("ha-switch")],(function(i,e){class t extends e{constructor(...e){super(...e),i(this)}}return{F:t,d:[{kind:"field",decorators:[(0,r.Cb)({type:Boolean})],key:"haptic",value:()=>!1},{kind:"method",key:"firstUpdated",value:function(){(0,o.Z)((0,n.Z)(t.prototype),"firstUpdated",this).call(this),this.addEventListener("change",(()=>{this.haptic&&(0,c.j)("light")}))}},{kind:"field",static:!0,key:"styles",value:()=>[l.W,d.iv`:host{--mdc-theme-secondary:var(--switch-checked-color)}.mdc-switch.mdc-switch--checked .mdc-switch__thumb{background-color:var(--switch-checked-button-color);border-color:var(--switch-checked-button-color)}.mdc-switch.mdc-switch--checked .mdc-switch__track{background-color:var(--switch-checked-track-color);border-color:var(--switch-checked-track-color)}.mdc-switch:not(.mdc-switch--checked) .mdc-switch__thumb{background-color:var(--switch-unchecked-button-color);border-color:var(--switch-unchecked-button-color)}.mdc-switch:not(.mdc-switch--checked) .mdc-switch__track{background-color:var(--switch-unchecked-track-color);border-color:var(--switch-unchecked-track-color)}`]}]}}),s.H)},4503:(i,e,t)=>{t.r(e);var a=t(17463),o=(t(33829),t(14271),t(68144)),n=t(79932),s=t(87744),l=t(34821),d=(t(83927),t(76865),t(73548),t(52039),t(43709),t(3555),t(65253)),r=t(26765),c=t(11654),h=t(45917);(0,a.Z)([(0,n.Mo)("dialog-user-detail")],(function(i,e){return{F:class extends e{constructor(...e){super(...e),i(this)}},d:[{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.SB)()],key:"_name",value:void 0},{kind:"field",decorators:[(0,n.SB)()],key:"_isAdmin",value:void 0},{kind:"field",decorators:[(0,n.SB)()],key:"_localOnly",value:void 0},{kind:"field",decorators:[(0,n.SB)()],key:"_isActive",value:void 0},{kind:"field",decorators:[(0,n.SB)()],key:"_error",value:void 0},{kind:"field",decorators:[(0,n.SB)()],key:"_params",value:void 0},{kind:"field",decorators:[(0,n.SB)()],key:"_submitting",value:()=>!1},{kind:"method",key:"showDialog",value:async function(i){this._params=i,this._error=void 0,this._name=i.entry.name||"",this._isAdmin=i.entry.group_ids.includes(d.Pb),this._localOnly=i.entry.local_only,this._isActive=i.entry.is_active,await this.updateComplete}},{kind:"method",key:"render",value:function(){var i;if(!this._params)return o.Ld;const e=this._params.entry,t=(0,d.FH)(this.hass,e,!0);return o.dy` <ha-dialog open @closed="${this._close}" scrimClickAction escapeKeyAction .heading="${(0,l.i)(this.hass,e.name)}"> <div> ${this._error?o.dy` <div class="error">${this._error}</div> `:""} <div class="secondary"> ${this.hass.localize("ui.panel.config.users.editor.id")}: ${e.id}<br> ${this.hass.localize("ui.panel.config.users.editor.username")}: ${e.username} </div> ${0===t.length?"":o.dy` <div class="badge-container"> ${t.map((([i,e])=>o.dy` <ha-label> <ha-svg-icon slot="icon" .path="${i}"></ha-svg-icon> ${e} </ha-label> `))} </div> `} <div class="form"> <ha-textfield dialogInitialFocus .value="${this._name}" .disabled="${e.system_generated}" @input="${this._nameChanged}" .label="${this.hass.localize("ui.panel.config.users.editor.name")}"></ha-textfield> <div class="row"> <ha-formfield .label="${this.hass.localize("ui.panel.config.users.editor.local_only")}" .dir="${(0,s.Zu)(this.hass)}"> <ha-switch .disabled="${e.system_generated}" .checked="${this._localOnly}" @change="${this._localOnlyChanged}"> </ha-switch> </ha-formfield> </div> <div class="row"> <ha-formfield .label="${this.hass.localize("ui.panel.config.users.editor.admin")}" .dir="${(0,s.Zu)(this.hass)}"> <ha-switch .disabled="${e.system_generated||e.is_owner}" .checked="${this._isAdmin}" @change="${this._adminChanged}"> </ha-switch> </ha-formfield> </div> ${this._isAdmin?"":o.dy` <br> ${this.hass.localize("ui.panel.config.users.users_privileges_note")} `} <div class="row"> <ha-formfield .label="${this.hass.localize("ui.panel.config.users.editor.active")}" .dir="${(0,s.Zu)(this.hass)}"> <ha-switch .disabled="${e.system_generated||e.is_owner}" .checked="${this._isActive}" @change="${this._activeChanged}"> </ha-switch> </ha-formfield> <ha-help-tooltip .label="${this.hass.localize("ui.panel.config.users.editor.active_tooltip")}"> </ha-help-tooltip> </div> </div> </div> <div slot="secondaryAction"> <mwc-button class="warning" @click="${this._deleteEntry}" .disabled="${this._submitting||e.system_generated||e.is_owner}"> ${this.hass.localize("ui.panel.config.users.editor.delete_user")} </mwc-button> ${e.system_generated?o.dy` <simple-tooltip animation-delay="0" position="right"> ${this.hass.localize("ui.panel.config.users.editor.system_generated_users_not_removable")} </simple-tooltip> `:""} ${!e.system_generated&&null!==(i=this.hass.user)&&void 0!==i&&i.is_owner?o.dy`<mwc-button @click="${this._changePassword}"> ${this.hass.localize("ui.panel.config.users.editor.change_password")} </mwc-button>`:""} </div> <div slot="primaryAction"> <mwc-button @click="${this._updateEntry}" .disabled="${!this._name||this._submitting||e.system_generated}"> ${this.hass.localize("ui.panel.config.users.editor.update_user")} </mwc-button> ${e.system_generated?o.dy` <simple-tooltip animation-delay="0" position="left"> ${this.hass.localize("ui.panel.config.users.editor.system_generated_users_not_editable")} </simple-tooltip> `:""} </div> </ha-dialog> `}},{kind:"method",key:"_nameChanged",value:function(i){this._error=void 0,this._name=i.target.value}},{kind:"method",key:"_adminChanged",value:function(i){this._isAdmin=i.target.checked}},{kind:"method",key:"_localOnlyChanged",value:function(i){this._localOnly=i.target.checked}},{kind:"method",key:"_activeChanged",value:function(i){this._isActive=i.target.checked}},{kind:"method",key:"_updateEntry",value:async function(){this._submitting=!0;try{await this._params.updateEntry({name:this._name.trim(),is_active:this._isActive,group_ids:[this._isAdmin?d.Pb:d.CE],local_only:this._localOnly}),this._close()}catch(i){this._error=(null==i?void 0:i.message)||"Unknown error"}finally{this._submitting=!1}}},{kind:"method",key:"_deleteEntry",value:async function(){this._submitting=!0;try{await this._params.removeEntry()&&(this._params=void 0)}finally{this._submitting=!1}}},{kind:"method",key:"_changePassword",value:async function(){var i;(null===(i=this._params)||void 0===i?void 0:i.entry.credentials.find((i=>"homeassistant"===i.type)))?(0,h.o)(this,{userId:this._params.entry.id}):(0,r.showAlertDialog)(this,{title:"No Home Assistant credentials found."})}},{kind:"method",key:"_close",value:function(){this._params=void 0}},{kind:"get",static:!0,key:"styles",value:function(){return[c.yu,o.iv`ha-dialog{--mdc-dialog-max-width:500px}.form{padding-top:16px}.secondary{color:var(--secondary-text-color)}ha-textfield{display:block}.badge-container{margin-top:4px}.badge-container>*{margin:4px 4px 4px 0}.state{background-color:rgba(var(--rgb-primary-text-color),.15);border-radius:16px;padding:4px 8px;margin-top:8px;display:inline-block}.state:not(:first-child){margin-left:8px}.row{display:flex;padding:8px 0}ha-help-tooltip{margin-left:4px;position:relative}`]}}]}}),o.oi)},45917:(i,e,t)=>{t.d(e,{o:()=>n});var a=t(47181);const o=()=>Promise.all([t.e(68331),t.e(39285)]).then(t.bind(t,52431)),n=(i,e)=>{(0,a.B)(i,"show-dialog",{dialogTag:"dialog-admin-change-password",dialogImport:o,dialogParams:e})}}};
//# sourceMappingURL=4503.tagrpVBJWOI.js.map