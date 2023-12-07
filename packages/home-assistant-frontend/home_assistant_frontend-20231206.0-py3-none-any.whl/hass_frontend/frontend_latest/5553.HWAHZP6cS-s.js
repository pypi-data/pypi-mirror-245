/*! For license information please see 5553.HWAHZP6cS-s.js.LICENSE.txt */
export const id=5553;export const ids=[5553];export const modules={8485:(e,t,i)=>{i.d(t,{a:()=>m});var o=i(43204),a=i(72774),n={ROOT:"mdc-form-field"},s={LABEL_SELECTOR:".mdc-form-field > label"};const r=function(e){function t(i){var a=e.call(this,(0,o.__assign)((0,o.__assign)({},t.defaultAdapter),i))||this;return a.click=function(){a.handleClick()},a}return(0,o.__extends)(t,e),Object.defineProperty(t,"cssClasses",{get:function(){return n},enumerable:!1,configurable:!0}),Object.defineProperty(t,"strings",{get:function(){return s},enumerable:!1,configurable:!0}),Object.defineProperty(t,"defaultAdapter",{get:function(){return{activateInputRipple:function(){},deactivateInputRipple:function(){},deregisterInteractionHandler:function(){},registerInteractionHandler:function(){}}},enumerable:!1,configurable:!0}),t.prototype.init=function(){this.adapter.registerInteractionHandler("click",this.click)},t.prototype.destroy=function(){this.adapter.deregisterInteractionHandler("click",this.click)},t.prototype.handleClick=function(){var e=this;this.adapter.activateInputRipple(),requestAnimationFrame((function(){e.adapter.deactivateInputRipple()}))},t}(a.K);var l=i(78220),d=i(18601),c=i(14114),h=i(68144),p=i(79932),u=i(83448);class m extends l.H{constructor(){super(...arguments),this.alignEnd=!1,this.spaceBetween=!1,this.nowrap=!1,this.label="",this.mdcFoundationClass=r}createAdapter(){return{registerInteractionHandler:(e,t)=>{this.labelEl.addEventListener(e,t)},deregisterInteractionHandler:(e,t)=>{this.labelEl.removeEventListener(e,t)},activateInputRipple:async()=>{const e=this.input;if(e instanceof d.Wg){const t=await e.ripple;t&&t.startPress()}},deactivateInputRipple:async()=>{const e=this.input;if(e instanceof d.Wg){const t=await e.ripple;t&&t.endPress()}}}}get input(){var e,t;return null!==(t=null===(e=this.slottedInputs)||void 0===e?void 0:e[0])&&void 0!==t?t:null}render(){const e={"mdc-form-field--align-end":this.alignEnd,"mdc-form-field--space-between":this.spaceBetween,"mdc-form-field--nowrap":this.nowrap};return h.dy` <div class="mdc-form-field ${(0,u.$)(e)}"> <slot></slot> <label class="mdc-label" @click="${this._labelClick}">${this.label}</label> </div>`}click(){this._labelClick()}_labelClick(){const e=this.input;e&&(e.focus(),e.click())}}(0,o.__decorate)([(0,p.Cb)({type:Boolean})],m.prototype,"alignEnd",void 0),(0,o.__decorate)([(0,p.Cb)({type:Boolean})],m.prototype,"spaceBetween",void 0),(0,o.__decorate)([(0,p.Cb)({type:Boolean})],m.prototype,"nowrap",void 0),(0,o.__decorate)([(0,p.Cb)({type:String}),(0,c.P)((async function(e){var t;null===(t=this.input)||void 0===t||t.setAttribute("aria-label",e)}))],m.prototype,"label",void 0),(0,o.__decorate)([(0,p.IO)(".mdc-form-field")],m.prototype,"mdcRoot",void 0),(0,o.__decorate)([(0,p.vZ)("",!0,"*")],m.prototype,"slottedInputs",void 0),(0,o.__decorate)([(0,p.IO)("label")],m.prototype,"labelEl",void 0)},92038:(e,t,i)=>{i.d(t,{W:()=>o});const o=i(68144).iv`.mdc-form-field{-moz-osx-font-smoothing:grayscale;-webkit-font-smoothing:antialiased;font-family:Roboto,sans-serif;font-family:var(--mdc-typography-body2-font-family, var(--mdc-typography-font-family, Roboto, sans-serif));font-size:.875rem;font-size:var(--mdc-typography-body2-font-size, .875rem);line-height:1.25rem;line-height:var(--mdc-typography-body2-line-height, 1.25rem);font-weight:400;font-weight:var(--mdc-typography-body2-font-weight,400);letter-spacing:.0178571429em;letter-spacing:var(--mdc-typography-body2-letter-spacing, .0178571429em);text-decoration:inherit;text-decoration:var(--mdc-typography-body2-text-decoration,inherit);text-transform:inherit;text-transform:var(--mdc-typography-body2-text-transform,inherit);color:rgba(0,0,0,.87);color:var(--mdc-theme-text-primary-on-background,rgba(0,0,0,.87));display:inline-flex;align-items:center;vertical-align:middle}.mdc-form-field>label{margin-left:0;margin-right:auto;padding-left:4px;padding-right:0;order:0}.mdc-form-field>label[dir=rtl],[dir=rtl] .mdc-form-field>label{margin-left:auto;margin-right:0}.mdc-form-field>label[dir=rtl],[dir=rtl] .mdc-form-field>label{padding-left:0;padding-right:4px}.mdc-form-field--nowrap>label{text-overflow:ellipsis;overflow:hidden;white-space:nowrap}.mdc-form-field--align-end>label{margin-left:auto;margin-right:0;padding-left:0;padding-right:4px;order:-1}.mdc-form-field--align-end>label[dir=rtl],[dir=rtl] .mdc-form-field--align-end>label{margin-left:0;margin-right:auto}.mdc-form-field--align-end>label[dir=rtl],[dir=rtl] .mdc-form-field--align-end>label{padding-left:4px;padding-right:0}.mdc-form-field--space-between{justify-content:space-between}.mdc-form-field--space-between>label{margin:0}.mdc-form-field--space-between>label[dir=rtl],[dir=rtl] .mdc-form-field--space-between>label{margin:0}:host{display:inline-flex}.mdc-form-field{width:100%}::slotted(*){-moz-osx-font-smoothing:grayscale;-webkit-font-smoothing:antialiased;font-family:Roboto,sans-serif;font-family:var(--mdc-typography-body2-font-family, var(--mdc-typography-font-family, Roboto, sans-serif));font-size:.875rem;font-size:var(--mdc-typography-body2-font-size, .875rem);line-height:1.25rem;line-height:var(--mdc-typography-body2-line-height, 1.25rem);font-weight:400;font-weight:var(--mdc-typography-body2-font-weight,400);letter-spacing:.0178571429em;letter-spacing:var(--mdc-typography-body2-letter-spacing, .0178571429em);text-decoration:inherit;text-decoration:var(--mdc-typography-body2-text-decoration,inherit);text-transform:inherit;text-transform:var(--mdc-typography-body2-text-transform,inherit);color:rgba(0,0,0,.87);color:var(--mdc-theme-text-primary-on-background,rgba(0,0,0,.87))}::slotted(mwc-switch){margin-right:10px}::slotted(mwc-switch[dir=rtl]),[dir=rtl] ::slotted(mwc-switch){margin-left:10px}`},66695:(e,t,i)=>{i.d(t,{V:()=>n});const o=Symbol("selection controller");class a{constructor(){this.selected=null,this.ordered=null,this.set=new Set}}class n{constructor(e){this.sets={},this.focusedSet=null,this.mouseIsDown=!1,this.updating=!1,e.addEventListener("keydown",(e=>{this.keyDownHandler(e)})),e.addEventListener("mousedown",(()=>{this.mousedownHandler()})),e.addEventListener("mouseup",(()=>{this.mouseupHandler()}))}static getController(e){const t=!("global"in e)||"global"in e&&e.global?document:e.getRootNode();let i=t[o];return void 0===i&&(i=new n(t),t[o]=i),i}keyDownHandler(e){const t=e.target;"checked"in t&&this.has(t)&&("ArrowRight"==e.key||"ArrowDown"==e.key?this.selectNext(t):"ArrowLeft"!=e.key&&"ArrowUp"!=e.key||this.selectPrevious(t))}mousedownHandler(){this.mouseIsDown=!0}mouseupHandler(){this.mouseIsDown=!1}has(e){return this.getSet(e.name).set.has(e)}selectPrevious(e){const t=this.getOrdered(e),i=t.indexOf(e),o=t[i-1]||t[t.length-1];return this.select(o),o}selectNext(e){const t=this.getOrdered(e),i=t.indexOf(e),o=t[i+1]||t[0];return this.select(o),o}select(e){e.click()}focus(e){if(this.mouseIsDown)return;const t=this.getSet(e.name),i=this.focusedSet;this.focusedSet=t,i!=t&&t.selected&&t.selected!=e&&t.selected.focus()}isAnySelected(e){const t=this.getSet(e.name);for(const e of t.set)if(e.checked)return!0;return!1}getOrdered(e){const t=this.getSet(e.name);return t.ordered||(t.ordered=Array.from(t.set),t.ordered.sort(((e,t)=>e.compareDocumentPosition(t)==Node.DOCUMENT_POSITION_PRECEDING?1:0))),t.ordered}getSet(e){return this.sets[e]||(this.sets[e]=new a),this.sets[e]}register(e){const t=e.name||e.getAttribute("name")||"",i=this.getSet(t);i.set.add(e),i.ordered=null}unregister(e){const t=this.getSet(e.name);t.set.delete(e),t.ordered=null,t.selected==e&&(t.selected=null)}update(e){if(this.updating)return;this.updating=!0;const t=this.getSet(e.name);if(e.checked){for(const i of t.set)i!=e&&(i.checked=!1);t.selected=e}if(this.isAnySelected(e))for(const e of t.set){if(void 0===e.formElementTabIndex)break;e.formElementTabIndex=e.checked?0:-1}this.updating=!1}}},34821:(e,t,i)=>{i.d(t,{i:()=>p});var o=i(17463),a=i(34541),n=i(47838),s=i(87762),r=i(91632),l=i(68144),d=i(79932),c=i(74265);i(10983);const h=["button","ha-list-item"],p=(e,t)=>{var i;return l.dy` <div class="header_title">${t}</div> <ha-icon-button .label="${null!==(i=null==e?void 0:e.localize("ui.dialogs.generic.close"))&&void 0!==i?i:"Close"}" .path="${"M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z"}" dialogAction="close" class="header_button"></ha-icon-button> `};(0,o.Z)([(0,d.Mo)("ha-dialog")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",key:c.gA,value:void 0},{kind:"method",key:"scrollToPos",value:function(e,t){var i;null===(i=this.contentElement)||void 0===i||i.scrollTo(e,t)}},{kind:"method",key:"renderHeading",value:function(){return l.dy`<slot name="heading"> ${(0,a.Z)((0,n.Z)(i.prototype),"renderHeading",this).call(this)} </slot>`}},{kind:"method",key:"firstUpdated",value:function(){var e;(0,a.Z)((0,n.Z)(i.prototype),"firstUpdated",this).call(this),this.suppressDefaultPressSelector=[this.suppressDefaultPressSelector,h].join(", "),this._updateScrolledAttribute(),null===(e=this.contentElement)||void 0===e||e.addEventListener("scroll",this._onScroll,{passive:!0})}},{kind:"method",key:"disconnectedCallback",value:function(){(0,a.Z)((0,n.Z)(i.prototype),"disconnectedCallback",this).call(this),this.contentElement.removeEventListener("scroll",this._onScroll)}},{kind:"field",key:"_onScroll",value(){return()=>{this._updateScrolledAttribute()}}},{kind:"method",key:"_updateScrolledAttribute",value:function(){this.contentElement&&this.toggleAttribute("scrolled",0!==this.contentElement.scrollTop)}},{kind:"field",static:!0,key:"styles",value:()=>[r.W,l.iv`:host([scrolled]) ::slotted(ha-dialog-header){border-bottom:1px solid var(--mdc-dialog-scroll-divider-color,rgba(0,0,0,.12))}.mdc-dialog{--mdc-dialog-scroll-divider-color:var(
          --dialog-scroll-divider-color,
          var(--divider-color)
        );z-index:var(--dialog-z-index,8);-webkit-backdrop-filter:var(--dialog-backdrop-filter,none);backdrop-filter:var(--dialog-backdrop-filter,none);--mdc-dialog-box-shadow:var(--dialog-box-shadow, none);--mdc-typography-headline6-font-weight:400;--mdc-typography-headline6-font-size:1.574rem}.mdc-dialog__actions{justify-content:var(--justify-action-buttons,flex-end);padding-bottom:max(env(safe-area-inset-bottom),24px)}.mdc-dialog__actions span:first-child{flex:var(--secondary-action-button-flex,unset)}.mdc-dialog__actions span:nth-child(2){flex:var(--primary-action-button-flex,unset)}.mdc-dialog__container{align-items:var(--vertical-align-dialog,center)}.mdc-dialog__title{padding:24px 24px 0 24px;text-overflow:ellipsis;overflow:hidden}.mdc-dialog__actions{padding:12px 24px 12px 24px}.mdc-dialog__title::before{display:block;height:0px}.mdc-dialog .mdc-dialog__content{position:var(--dialog-content-position,relative);padding:var(--dialog-content-padding,24px)}:host([hideactions]) .mdc-dialog .mdc-dialog__content{padding-bottom:max(var(--dialog-content-padding,24px),env(safe-area-inset-bottom))}.mdc-dialog .mdc-dialog__surface{position:var(--dialog-surface-position,relative);top:var(--dialog-surface-top);margin-top:var(--dialog-surface-margin-top);min-height:var(--mdc-dialog-min-height,auto);border-radius:var(--ha-dialog-border-radius,28px)}:host([flexContent]) .mdc-dialog .mdc-dialog__content{display:flex;flex-direction:column}.header_title{margin-right:32px;margin-inline-end:32px;margin-inline-start:initial;direction:var(--direction)}.header_button{position:absolute;right:16px;top:14px;text-decoration:none;color:inherit;inset-inline-start:initial;inset-inline-end:16px;direction:var(--direction)}.dialog-actions{inset-inline-start:initial!important;inset-inline-end:0px!important;direction:var(--direction)}`]}]}}),s.M)},83927:(e,t,i)=>{var o=i(17463),a=i(8485),n=i(92038),s=i(68144),r=i(79932),l=i(47181);(0,o.Z)([(0,r.Mo)("ha-formfield")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"method",key:"_labelClick",value:function(){const e=this.input;if(e&&(e.focus(),!e.disabled))switch(e.tagName){case"HA-CHECKBOX":e.checked=!e.checked,(0,l.B)(e,"change");break;case"HA-RADIO":e.checked=!0,(0,l.B)(e,"change");break;default:e.click()}}},{kind:"field",static:!0,key:"styles",value:()=>[n.W,s.iv`:host(:not([alignEnd])) ::slotted(ha-switch){margin-right:10px;margin-inline-end:10px;margin-inline-start:inline}.mdc-form-field>label{direction:var(--direction);margin-inline-start:0;margin-inline-end:auto;padding-inline-start:4px;padding-inline-end:0}`]}]}}),a.a)},33220:(e,t,i)=>{var o=i(17463),a=i(35433),n=i(44973),s=i(68144),r=i(79932);(0,o.Z)([(0,r.Mo)("ha-radio")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",static:!0,key:"styles",value:()=>[n.W,s.iv`:host{--mdc-theme-secondary:var(--primary-color)}`]}]}}),a.J)},24054:(e,t,i)=>{i.r(t),i.d(t,{DialogStatisticsFixUnitsChanged:()=>d});var o=i(17463),a=(i(14271),i(68144)),n=i(79932),s=i(47181),r=(i(34821),i(83927),i(33220),i(38014)),l=i(11654);let d=(0,o.Z)([(0,n.Mo)("dialog-statistics-fix-units-changed")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.SB)()],key:"_params",value:void 0},{kind:"field",decorators:[(0,n.SB)()],key:"_action",value:void 0},{kind:"method",key:"showDialog",value:function(e){this._params=e,this._action="update"}},{kind:"method",key:"closeDialog",value:function(){this._params=void 0,this._action=void 0,(0,s.B)(this,"dialog-closed",{dialog:this.localName})}},{kind:"method",key:"render",value:function(){return this._params?a.dy` <ha-dialog open @closed="${this.closeDialog}" .heading="${this.hass.localize("ui.panel.developer-tools.tabs.statistics.fix_issue.units_changed.title")}"> <p> ${this.hass.localize("ui.panel.developer-tools.tabs.statistics.fix_issue.units_changed.info_text_1",{current_unit:this._params.issue.data.state_unit,previous_unit:this._params.issue.data.metadata_unit})}<br> ${this.hass.localize("ui.panel.developer-tools.tabs.statistics.fix_issue.units_changed.info_text_2")}<br> ${this.hass.localize("ui.panel.developer-tools.tabs.statistics.fix_issue.units_changed.info_text_3")} </p> <h3> ${this.hass.localize("ui.panel.developer-tools.tabs.statistics.fix_issue.units_changed.how_to_fix")} </h3> <ha-formfield .label="${this.hass.localize("ui.panel.developer-tools.tabs.statistics.fix_issue.units_changed.update",this._params.issue.data)}"> <ha-radio value="update" name="action" .checked="${"update"===this._action}" @change="${this._handleActionChanged}" dialogInitialFocus></ha-radio> </ha-formfield> <ha-formfield .label="${this.hass.localize("ui.panel.developer-tools.tabs.statistics.fix_issue.units_changed.clear")}"> <ha-radio value="clear" name="action" .checked="${"clear"===this._action}" @change="${this._handleActionChanged}"></ha-radio> </ha-formfield> <mwc-button slot="primaryAction" @click="${this._fixIssue}"> ${this.hass.localize("ui.panel.developer-tools.tabs.statistics.fix_issue.fix")} </mwc-button> <mwc-button slot="secondaryAction" @click="${this.closeDialog}"> ${this.hass.localize("ui.common.close")} </mwc-button> </ha-dialog> `:a.Ld}},{kind:"method",key:"_handleActionChanged",value:function(e){this._action=e.target.value}},{kind:"method",key:"_fixIssue",value:async function(){var e;"clear"===this._action?await(0,r.hN)(this.hass,[this._params.issue.data.statistic_id]):"update"===this._action&&await(0,r.Cj)(this.hass,this._params.issue.data.statistic_id,this._params.issue.data.state_unit),null===(e=this._params)||void 0===e||e.fixedCallback(),this.closeDialog()}},{kind:"get",static:!0,key:"styles",value:function(){return[l.Qx,l.yu]}}]}}),a.oi)}};
//# sourceMappingURL=5553.HWAHZP6cS-s.js.map