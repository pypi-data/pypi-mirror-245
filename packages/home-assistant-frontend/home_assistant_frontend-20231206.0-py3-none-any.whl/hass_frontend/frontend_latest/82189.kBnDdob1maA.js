/*! For license information please see 82189.kBnDdob1maA.js.LICENSE.txt */
export const id=82189;export const ids=[82189,31206];export const modules={31206:(e,o,t)=>{t.r(o),t.d(o,{HaCircularProgress:()=>d});var r=t(17463),i=t(34541),a=t(47838),n=(t(34131),t(22129)),l=t(68144),c=t(79932);let d=(0,r.Z)([(0,c.Mo)("ha-circular-progress")],(function(e,o){class t extends o{constructor(...o){super(...o),e(this)}}return{F:t,d:[{kind:"field",decorators:[(0,c.Cb)({attribute:"aria-label",type:String})],key:"ariaLabel",value:()=>"Loading"},{kind:"field",decorators:[(0,c.Cb)()],key:"size",value:()=>"medium"},{kind:"method",key:"updated",value:function(e){if((0,i.Z)((0,a.Z)(t.prototype),"updated",this).call(this,e),e.has("size"))switch(this.size){case"tiny":this.style.setProperty("--md-circular-progress-size","16px");break;case"small":this.style.setProperty("--md-circular-progress-size","28px");break;case"medium":this.style.setProperty("--md-circular-progress-size","48px");break;case"large":this.style.setProperty("--md-circular-progress-size","68px")}}},{kind:"get",static:!0,key:"styles",value:function(){return[...(0,i.Z)((0,a.Z)(t),"styles",this),l.iv`:host{--md-sys-color-primary:var(--primary-color);--md-circular-progress-size:48px}`]}}]}}),n.B)},34821:(e,o,t)=>{t.d(o,{i:()=>h});var r=t(17463),i=t(34541),a=t(47838),n=t(87762),l=t(91632),c=t(68144),d=t(79932),s=t(74265);t(10983);const v=["button","ha-list-item"],h=(e,o)=>{var t;return c.dy` <div class="header_title">${o}</div> <ha-icon-button .label="${null!==(t=null==e?void 0:e.localize("ui.dialogs.generic.close"))&&void 0!==t?t:"Close"}" .path="${"M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z"}" dialogAction="close" class="header_button"></ha-icon-button> `};(0,r.Z)([(0,d.Mo)("ha-dialog")],(function(e,o){class t extends o{constructor(...o){super(...o),e(this)}}return{F:t,d:[{kind:"field",key:s.gA,value:void 0},{kind:"method",key:"scrollToPos",value:function(e,o){var t;null===(t=this.contentElement)||void 0===t||t.scrollTo(e,o)}},{kind:"method",key:"renderHeading",value:function(){return c.dy`<slot name="heading"> ${(0,i.Z)((0,a.Z)(t.prototype),"renderHeading",this).call(this)} </slot>`}},{kind:"method",key:"firstUpdated",value:function(){var e;(0,i.Z)((0,a.Z)(t.prototype),"firstUpdated",this).call(this),this.suppressDefaultPressSelector=[this.suppressDefaultPressSelector,v].join(", "),this._updateScrolledAttribute(),null===(e=this.contentElement)||void 0===e||e.addEventListener("scroll",this._onScroll,{passive:!0})}},{kind:"method",key:"disconnectedCallback",value:function(){(0,i.Z)((0,a.Z)(t.prototype),"disconnectedCallback",this).call(this),this.contentElement.removeEventListener("scroll",this._onScroll)}},{kind:"field",key:"_onScroll",value(){return()=>{this._updateScrolledAttribute()}}},{kind:"method",key:"_updateScrolledAttribute",value:function(){this.contentElement&&this.toggleAttribute("scrolled",0!==this.contentElement.scrollTop)}},{kind:"field",static:!0,key:"styles",value:()=>[l.W,c.iv`:host([scrolled]) ::slotted(ha-dialog-header){border-bottom:1px solid var(--mdc-dialog-scroll-divider-color,rgba(0,0,0,.12))}.mdc-dialog{--mdc-dialog-scroll-divider-color:var(
          --dialog-scroll-divider-color,
          var(--divider-color)
        );z-index:var(--dialog-z-index,8);-webkit-backdrop-filter:var(--dialog-backdrop-filter,none);backdrop-filter:var(--dialog-backdrop-filter,none);--mdc-dialog-box-shadow:var(--dialog-box-shadow, none);--mdc-typography-headline6-font-weight:400;--mdc-typography-headline6-font-size:1.574rem}.mdc-dialog__actions{justify-content:var(--justify-action-buttons,flex-end);padding-bottom:max(env(safe-area-inset-bottom),24px)}.mdc-dialog__actions span:first-child{flex:var(--secondary-action-button-flex,unset)}.mdc-dialog__actions span:nth-child(2){flex:var(--primary-action-button-flex,unset)}.mdc-dialog__container{align-items:var(--vertical-align-dialog,center)}.mdc-dialog__title{padding:24px 24px 0 24px;text-overflow:ellipsis;overflow:hidden}.mdc-dialog__actions{padding:12px 24px 12px 24px}.mdc-dialog__title::before{display:block;height:0px}.mdc-dialog .mdc-dialog__content{position:var(--dialog-content-position,relative);padding:var(--dialog-content-padding,24px)}:host([hideactions]) .mdc-dialog .mdc-dialog__content{padding-bottom:max(var(--dialog-content-padding,24px),env(safe-area-inset-bottom))}.mdc-dialog .mdc-dialog__surface{position:var(--dialog-surface-position,relative);top:var(--dialog-surface-top);margin-top:var(--dialog-surface-margin-top);min-height:var(--mdc-dialog-min-height,auto);border-radius:var(--ha-dialog-border-radius,28px)}:host([flexContent]) .mdc-dialog .mdc-dialog__content{display:flex;flex-direction:column}.header_title{margin-right:32px;margin-inline-end:32px;margin-inline-start:initial;direction:var(--direction)}.header_button{position:absolute;right:16px;top:14px;text-decoration:none;color:inherit;inset-inline-start:initial;inset-inline-end:16px;direction:var(--direction)}.dialog-actions{inset-inline-start:initial!important;inset-inline-end:0px!important;direction:var(--direction)}`]}]}}),n.M)},10983:(e,o,t)=>{t.d(o,{$:()=>l});var r=t(17463),i=(t(20210),t(68144)),a=t(79932),n=t(30153);t(52039);let l=(0,r.Z)([(0,a.Mo)("ha-icon-button")],(function(e,o){return{F:class extends o{constructor(...o){super(...o),e(this)}},d:[{kind:"field",decorators:[(0,a.Cb)({type:Boolean,reflect:!0})],key:"disabled",value:()=>!1},{kind:"field",decorators:[(0,a.Cb)({type:String})],key:"path",value:void 0},{kind:"field",decorators:[(0,a.Cb)({type:String})],key:"label",value:void 0},{kind:"field",decorators:[(0,a.Cb)({type:String,attribute:"aria-haspopup"})],key:"ariaHasPopup",value:void 0},{kind:"field",decorators:[(0,a.Cb)({type:Boolean})],key:"hideTitle",value:()=>!1},{kind:"field",decorators:[(0,a.IO)("mwc-icon-button",!0)],key:"_button",value:void 0},{kind:"method",key:"focus",value:function(){var e;null===(e=this._button)||void 0===e||e.focus()}},{kind:"field",static:!0,key:"shadowRootOptions",value:()=>({mode:"open",delegatesFocus:!0})},{kind:"method",key:"render",value:function(){return i.dy` <mwc-icon-button aria-label="${(0,n.o)(this.label)}" title="${(0,n.o)(this.hideTitle?void 0:this.label)}" aria-haspopup="${(0,n.o)(this.ariaHasPopup)}" .disabled="${this.disabled}"> ${this.path?i.dy`<ha-svg-icon .path="${this.path}"></ha-svg-icon>`:i.dy`<slot></slot>`} </mwc-icon-button> `}},{kind:"get",static:!0,key:"styles",value:function(){return i.iv`:host{display:inline-block;outline:0}:host([disabled]){pointer-events:none}mwc-icon-button{--mdc-theme-on-primary:currentColor;--mdc-theme-text-disabled-on-light:var(--disabled-text-color)}`}}]}}),i.oi)},52039:(e,o,t)=>{t.d(o,{C:()=>n});var r=t(17463),i=t(68144),a=t(79932);let n=(0,r.Z)([(0,a.Mo)("ha-svg-icon")],(function(e,o){return{F:class extends o{constructor(...o){super(...o),e(this)}},d:[{kind:"field",decorators:[(0,a.Cb)()],key:"path",value:void 0},{kind:"field",decorators:[(0,a.Cb)()],key:"secondaryPath",value:void 0},{kind:"field",decorators:[(0,a.Cb)()],key:"viewBox",value:void 0},{kind:"method",key:"render",value:function(){return i.YP` <svg viewBox="${this.viewBox||"0 0 24 24"}" preserveAspectRatio="xMidYMid meet" focusable="false" role="img" aria-hidden="true"> <g> ${this.path?i.YP`<path class="primary-path" d="${this.path}"></path>`:i.Ld} ${this.secondaryPath?i.YP`<path class="secondary-path" d="${this.secondaryPath}"></path>`:i.Ld} </g> </svg>`}},{kind:"get",static:!0,key:"styles",value:function(){return i.iv`:host{display:var(--ha-icon-display,inline-flex);align-items:center;justify-content:center;position:relative;vertical-align:middle;fill:var(--icon-primary-color,currentcolor);width:var(--mdc-icon-size,24px);height:var(--mdc-icon-size,24px)}svg{width:100%;height:100%;pointer-events:none;display:block}path.primary-path{opacity:var(--icon-primary-opactity, 1)}path.secondary-path{fill:var(--icon-secondary-color,currentcolor);opacity:var(--icon-secondary-opactity, .5)}`}}]}}),i.oi)},91502:(e,o,t)=>{t.d(o,{Ex:()=>a,R9:()=>l,_T:()=>d,ab:()=>c,fC:()=>n,gK:()=>s,tB:()=>h,xr:()=>v});var r=t(83849),i=t(57292);const a=e=>{var o;return null===(o=e.auth.external)||void 0===o?void 0:o.config.canCommissionMatter},n=e=>e.auth.external.fireMessage({type:"matter/commission"}),l=(e,o)=>{let t;const a=(0,i.q4)(e.connection,(e=>{if(!t)return void(t=new Set(Object.values(e).filter((e=>e.identifiers.find((e=>"matter"===e[0])))).map((e=>e.id))));const i=Object.values(e).filter((e=>e.identifiers.find((e=>"matter"===e[0]))&&!t.has(e.id)));i.length&&(a(),t=void 0,null==o||o(),(0,r.c)(`/config/devices/device/${i[0].id}`))}));return()=>{a(),t=void 0}},c=e=>{n(e)},d=(e,o)=>e.callWS({type:"matter/commission",code:o}),s=(e,o)=>e.callWS({type:"matter/commission_on_network",pin:o}),v=(e,o,t)=>e.callWS({type:"matter/set_wifi_credentials",network_name:o,password:t}),h=(e,o)=>e.callWS({type:"matter/set_thread",thread_operation_dataset:o})},82189:(e,o,t)=>{t.r(o);var r=t(17463),i=(t(14271),t(68144)),a=t(79932),n=t(47181),l=(t(31206),t(34821)),c=t(91502),d=t(11654);(0,r.Z)([(0,a.Mo)("dialog-matter-add-device")],(function(e,o){return{F:class extends o{constructor(...o){super(...o),e(this)}},d:[{kind:"field",decorators:[(0,a.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,a.SB)()],key:"_open",value:()=>!1},{kind:"field",key:"_unsub",value:void 0},{kind:"method",key:"showDialog",value:function(){this._open=!0,(0,c.Ex)(this.hass)&&(this._unsub=(0,c.R9)(this.hass,(()=>this.closeDialog())),(0,c.ab)(this.hass))}},{kind:"method",key:"closeDialog",value:function(){var e;this._open=!1,null===(e=this._unsub)||void 0===e||e.call(this),this._unsub=void 0,(0,n.B)(this,"dialog-closed",{dialog:this.localName})}},{kind:"method",key:"render",value:function(){return this._open?i.dy` <ha-dialog open @closed="${this.closeDialog}" .heading="${(0,l.i)(this.hass,"Add Matter device")}"> <div> ${(0,c.Ex)(this.hass)?i.dy`<ha-circular-progress size="large" indeterminate></ha-circular-progress>`:this.hass.localize("ui.panel.config.integrations.config_flow.matter_mobile_app")} </div> <mwc-button slot="primaryAction" @click="${this.closeDialog}"> ${this.hass.localize("ui.common.cancel")} </mwc-button> </ha-dialog> `:i.Ld}},{kind:"field",static:!0,key:"styles",value:()=>[d.yu,i.iv`div{display:grid}ha-circular-progress{justify-self:center}`]}]}}),i.oi)},11654:(e,o,t)=>{t.d(o,{$c:()=>l,Qx:()=>a,k1:()=>i,yu:()=>n});var r=t(68144);const i=r.iv`button.link{background:0 0;color:inherit;border:none;padding:0;font:inherit;text-align:left;text-decoration:underline;cursor:pointer;outline:0}`,a=r.iv`:host{font-family:var(--paper-font-body1_-_font-family);-webkit-font-smoothing:var(--paper-font-body1_-_-webkit-font-smoothing);font-size:var(--paper-font-body1_-_font-size);font-weight:var(--paper-font-body1_-_font-weight);line-height:var(--paper-font-body1_-_line-height)}app-header div[sticky]{height:48px}app-toolbar [main-title]{margin-left:20px}h1{font-family:var(--paper-font-headline_-_font-family);-webkit-font-smoothing:var(--paper-font-headline_-_-webkit-font-smoothing);white-space:var(--paper-font-headline_-_white-space);overflow:var(--paper-font-headline_-_overflow);text-overflow:var(--paper-font-headline_-_text-overflow);font-size:var(--paper-font-headline_-_font-size);font-weight:var(--paper-font-headline_-_font-weight);line-height:var(--paper-font-headline_-_line-height)}h2{font-family:var(--paper-font-title_-_font-family);-webkit-font-smoothing:var(--paper-font-title_-_-webkit-font-smoothing);white-space:var(--paper-font-title_-_white-space);overflow:var(--paper-font-title_-_overflow);text-overflow:var(--paper-font-title_-_text-overflow);font-size:var(--paper-font-title_-_font-size);font-weight:var(--paper-font-title_-_font-weight);line-height:var(--paper-font-title_-_line-height)}h3{font-family:var(--paper-font-subhead_-_font-family);-webkit-font-smoothing:var(--paper-font-subhead_-_-webkit-font-smoothing);white-space:var(--paper-font-subhead_-_white-space);overflow:var(--paper-font-subhead_-_overflow);text-overflow:var(--paper-font-subhead_-_text-overflow);font-size:var(--paper-font-subhead_-_font-size);font-weight:var(--paper-font-subhead_-_font-weight);line-height:var(--paper-font-subhead_-_line-height)}a{color:var(--primary-color)}.secondary{color:var(--secondary-text-color)}.error{color:var(--error-color)}.warning{color:var(--error-color)}mwc-button.warning{--mdc-theme-primary:var(--error-color)}${i} .card-actions a{text-decoration:none}.card-actions .warning{--mdc-theme-primary:var(--error-color)}.layout.horizontal,.layout.vertical{display:flex}.layout.inline{display:inline-flex}.layout.horizontal{flex-direction:row}.layout.vertical{flex-direction:column}.layout.wrap{flex-wrap:wrap}.layout.no-wrap{flex-wrap:nowrap}.layout.center,.layout.center-center{align-items:center}.layout.bottom{align-items:flex-end}.layout.center-center,.layout.center-justified{justify-content:center}.flex{flex:1;flex-basis:0.000000001px}.flex-auto{flex:1 1 auto}.flex-none{flex:none}.layout.justified{justify-content:space-between}`,n=r.iv`ha-dialog{--mdc-dialog-min-width:400px;--mdc-dialog-max-width:600px;--mdc-dialog-max-width:min(600px, 95vw);--justify-action-buttons:space-between}ha-dialog .form{color:var(--primary-text-color)}a{color:var(--primary-color)}@media all and (max-width:450px),all and (max-height:500px){ha-dialog{--mdc-dialog-min-width:calc(
        100vw - env(safe-area-inset-right) - env(safe-area-inset-left)
      );--mdc-dialog-max-width:calc(
        100vw - env(safe-area-inset-right) - env(safe-area-inset-left)
      );--mdc-dialog-min-height:100%;--mdc-dialog-max-height:100%;--vertical-align-dialog:flex-end;--ha-dialog-border-radius:0}}ha-button.warning,mwc-button.warning{--mdc-theme-primary:var(--error-color)}.error{color:var(--error-color)}`,l=r.iv`.ha-scrollbar::-webkit-scrollbar{width:.4rem;height:.4rem}.ha-scrollbar::-webkit-scrollbar-thumb{-webkit-border-radius:4px;border-radius:4px;background:var(--scrollbar-thumb-color)}.ha-scrollbar{overflow-y:auto;scrollbar-color:var(--scrollbar-thumb-color) transparent;scrollbar-width:thin}`;r.iv`body{background-color:var(--primary-background-color);color:var(--primary-text-color);height:calc(100vh - 32px);width:100vw}`},22129:(e,o,t)=>{t.d(o,{B:()=>v});var r=t(43204),i=t(79932),a=t(68144),n=t(83448),l=t(92204);class c extends a.oi{constructor(){super(...arguments),this.value=0,this.max=1,this.indeterminate=!1,this.fourColor=!1}render(){const{ariaLabel:e}=this;return a.dy` <div class="progress ${(0,n.$)(this.getRenderClasses())}" role="progressbar" aria-label="${e||a.Ld}" aria-valuemin="0" aria-valuemax="${this.max}" aria-valuenow="${this.indeterminate?a.Ld:this.value}">${this.renderIndicator()}</div> `}getRenderClasses(){return{indeterminate:this.indeterminate,"four-color":this.fourColor}}}(0,l.d)(c),(0,r.__decorate)([(0,i.Cb)({type:Number})],c.prototype,"value",void 0),(0,r.__decorate)([(0,i.Cb)({type:Number})],c.prototype,"max",void 0),(0,r.__decorate)([(0,i.Cb)({type:Boolean})],c.prototype,"indeterminate",void 0),(0,r.__decorate)([(0,i.Cb)({type:Boolean,attribute:"four-color"})],c.prototype,"fourColor",void 0);class d extends c{renderIndicator(){return this.indeterminate?this.renderIndeterminateContainer():this.renderDeterminateContainer()}renderDeterminateContainer(){const e=100*(1-this.value/this.max);return a.dy` <svg viewBox="0 0 4800 4800"> <circle class="track" pathLength="100"></circle> <circle class="active-track" pathLength="100" stroke-dashoffset="${e}"></circle> </svg> `}renderIndeterminateContainer(){return a.dy` <div class="spinner"> <div class="left"> <div class="circle"></div> </div> <div class="right"> <div class="circle"></div> </div> </div>`}}const s=a.iv`:host{--_active-indicator-color:var(--md-circular-progress-active-indicator-color, var(--md-sys-color-primary, #6750a4));--_active-indicator-width:var(--md-circular-progress-active-indicator-width, 10);--_four-color-active-indicator-four-color:var(--md-circular-progress-four-color-active-indicator-four-color, var(--md-sys-color-tertiary-container, #ffd8e4));--_four-color-active-indicator-one-color:var(--md-circular-progress-four-color-active-indicator-one-color, var(--md-sys-color-primary, #6750a4));--_four-color-active-indicator-three-color:var(--md-circular-progress-four-color-active-indicator-three-color, var(--md-sys-color-tertiary, #7d5260));--_four-color-active-indicator-two-color:var(--md-circular-progress-four-color-active-indicator-two-color, var(--md-sys-color-primary-container, #eaddff));--_size:var(--md-circular-progress-size, 48px);display:inline-flex;vertical-align:middle;min-block-size:var(--_size);min-inline-size:var(--_size);position:relative;align-items:center;justify-content:center;contain:strict;content-visibility:auto}.progress{flex:1;align-self:stretch;margin:4px}.active-track,.circle,.left,.progress,.right,.spinner,.track,svg{position:absolute;inset:0}svg{transform:rotate(-90deg)}circle{cx:50%;cy:50%;r:calc(50%*(1 - var(--_active-indicator-width)/ 100));stroke-width:calc(var(--_active-indicator-width)*1%);stroke-dasharray:100;fill:rgba(0,0,0,0)}.active-track{transition:stroke-dashoffset .5s cubic-bezier(0, 0, .2, 1);stroke:var(--_active-indicator-color)}.track{stroke:rgba(0,0,0,0)}.progress.indeterminate{animation:linear infinite linear-rotate;animation-duration:1.568s}.spinner{animation:infinite both rotate-arc;animation-duration:5332ms;animation-timing-function:cubic-bezier(0.4,0,0.2,1)}.left{overflow:hidden;inset:0 50% 0 0}.right{overflow:hidden;inset:0 0 0 50%}.circle{box-sizing:border-box;border-radius:50%;border:solid calc(var(--_active-indicator-width)/ 100*(var(--_size) - 8px));border-color:var(--_active-indicator-color) var(--_active-indicator-color) transparent transparent;animation:expand-arc;animation-iteration-count:infinite;animation-fill-mode:both;animation-duration:1333ms,5332ms;animation-timing-function:cubic-bezier(0.4,0,0.2,1)}.four-color .circle{animation-name:expand-arc,four-color}.left .circle{rotate:135deg;inset:0 -100% 0 0}.right .circle{rotate:100deg;inset:0 0 0 -100%;animation-delay:-.666s,0s}@media(forced-colors:active){.active-track{stroke:CanvasText}.circle{border-color:CanvasText CanvasText Canvas Canvas}}@keyframes expand-arc{0%{transform:rotate(265deg)}50%{transform:rotate(130deg)}100%{transform:rotate(265deg)}}@keyframes rotate-arc{12.5%{transform:rotate(135deg)}25%{transform:rotate(270deg)}37.5%{transform:rotate(405deg)}50%{transform:rotate(540deg)}62.5%{transform:rotate(675deg)}75%{transform:rotate(810deg)}87.5%{transform:rotate(945deg)}100%{transform:rotate(1080deg)}}@keyframes linear-rotate{to{transform:rotate(360deg)}}@keyframes four-color{0%{border-top-color:var(--_four-color-active-indicator-one-color);border-right-color:var(--_four-color-active-indicator-one-color)}15%{border-top-color:var(--_four-color-active-indicator-one-color);border-right-color:var(--_four-color-active-indicator-one-color)}25%{border-top-color:var(--_four-color-active-indicator-two-color);border-right-color:var(--_four-color-active-indicator-two-color)}40%{border-top-color:var(--_four-color-active-indicator-two-color);border-right-color:var(--_four-color-active-indicator-two-color)}50%{border-top-color:var(--_four-color-active-indicator-three-color);border-right-color:var(--_four-color-active-indicator-three-color)}65%{border-top-color:var(--_four-color-active-indicator-three-color);border-right-color:var(--_four-color-active-indicator-three-color)}75%{border-top-color:var(--_four-color-active-indicator-four-color);border-right-color:var(--_four-color-active-indicator-four-color)}90%{border-top-color:var(--_four-color-active-indicator-four-color);border-right-color:var(--_four-color-active-indicator-four-color)}100%{border-top-color:var(--_four-color-active-indicator-one-color);border-right-color:var(--_four-color-active-indicator-one-color)}}`;let v=class extends d{};v.styles=[s],v=(0,r.__decorate)([(0,i.Mo)("md-circular-progress")],v)}};
//# sourceMappingURL=82189.kBnDdob1maA.js.map