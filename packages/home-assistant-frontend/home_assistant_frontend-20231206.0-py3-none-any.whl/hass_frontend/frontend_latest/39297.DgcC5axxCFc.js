export const id=39297;export const ids=[39297];export const modules={76680:(e,t,i)=>{function a(e){return void 0===e||Array.isArray(e)?e:[e]}i.d(t,{r:()=>a})},57966:(e,t,i)=>{i.d(t,{z:()=>a});const a=e=>(t,i)=>e.includes(t,i)},39197:(e,t,i)=>{i.d(t,{v:()=>n});var a=i(56007),o=i(58831);function n(e,t){const i=(0,o.M)(e.entity_id),n=void 0!==t?t:null==e?void 0:e.state;if(["button","event","input_button","scene"].includes(i))return n!==a.nZ;if((0,a.rk)(n))return!1;if(n===a.PX&&"alert"!==i)return!1;switch(i){case"alarm_control_panel":return"disarmed"!==n;case"alert":return"idle"!==n;case"cover":return"closed"!==n;case"device_tracker":case"person":return"not_home"!==n;case"lawn_mower":return["mowing","error"].includes(n);case"lock":return"locked"!==n;case"media_player":return"standby"!==n;case"vacuum":return!["idle","docked","paused"].includes(n);case"plant":return"problem"===n;case"group":return["on","home","open","locked","problem"].includes(n);case"timer":return"active"===n;case"camera":return"streaming"===n}return!0}},33762:(e,t,i)=>{var a=i(17463),o=i(68144),n=i(79932),s=i(14516),d=i(76680),r=i(47181),l=i(85415),c=i(38014),u=i(27322),h=(i(77576),i(52039),i(3143),i(40163));(0,a.Z)([(0,n.Mo)("ha-statistic-picker")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.Cb)()],key:"label",value:void 0},{kind:"field",decorators:[(0,n.Cb)()],key:"value",value:void 0},{kind:"field",decorators:[(0,n.Cb)({attribute:"statistic-types"})],key:"statisticTypes",value:void 0},{kind:"field",decorators:[(0,n.Cb)({type:Boolean,attribute:"allow-custom-entity"})],key:"allowCustomEntity",value:void 0},{kind:"field",decorators:[(0,n.Cb)({type:Array})],key:"statisticIds",value:void 0},{kind:"field",decorators:[(0,n.Cb)({type:Boolean})],key:"disabled",value:void 0},{kind:"field",decorators:[(0,n.Cb)({type:Array,attribute:"include-statistics-unit-of-measurement"})],key:"includeStatisticsUnitOfMeasurement",value:void 0},{kind:"field",decorators:[(0,n.Cb)({attribute:"include-unit-class"})],key:"includeUnitClass",value:void 0},{kind:"field",decorators:[(0,n.Cb)({attribute:"include-device-class"})],key:"includeDeviceClass",value:void 0},{kind:"field",decorators:[(0,n.Cb)({type:Boolean,attribute:"entities-only"})],key:"entitiesOnly",value:()=>!1},{kind:"field",decorators:[(0,n.Cb)({type:Array,attribute:"exclude-statistics"})],key:"excludeStatistics",value:void 0},{kind:"field",decorators:[(0,n.Cb)()],key:"helpMissingEntityUrl",value:()=>"/more-info/statistics/"},{kind:"field",decorators:[(0,n.SB)()],key:"_opened",value:void 0},{kind:"field",decorators:[(0,n.IO)("ha-combo-box",!0)],key:"comboBox",value:void 0},{kind:"field",key:"_init",value:()=>!1},{kind:"field",key:"_statistics",value:()=>[]},{kind:"field",decorators:[(0,n.SB)()],key:"_filteredItems",value(){}},{kind:"field",key:"_rowRenderer",value(){return e=>o.dy`<mwc-list-item graphic="avatar" twoline> ${e.state?o.dy`<state-badge slot="graphic" .stateObj="${e.state}"></state-badge>`:""} <span>${e.name}</span> <span slot="secondary">${""===e.id||"__missing"===e.id?o.dy`<a target="_blank" rel="noopener noreferrer" href="${(0,u.R)(this.hass,this.helpMissingEntityUrl)}">${this.hass.localize("ui.components.statistic-picker.learn_more")}</a>`:e.id}</span> </mwc-list-item>`}},{kind:"field",key:"_getStatistics",value(){return(0,s.Z)(((e,t,i,a,o,n)=>{if(!e.length)return[{id:"",name:this.hass.localize("ui.components.statistic-picker.no_statistics"),strings:[]}];if(t){const i=(0,d.r)(t);e=e.filter((e=>i.includes(e.statistics_unit_of_measurement)))}if(i){const t=(0,d.r)(i);e=e.filter((e=>t.includes(e.unit_class)))}if(a){const t=(0,d.r)(a);e=e.filter((e=>{const i=this.hass.states[e.statistic_id];return!i||t.includes(i.attributes.device_class||"")}))}const s=[];return e.forEach((e=>{if(n&&n.includes(e.statistic_id))return;const t=this.hass.states[e.statistic_id];if(!t){if(!o){const t=e.statistic_id,i=(0,c.Kd)(this.hass,e.statistic_id,e);s.push({id:t,name:i,strings:[t,i]})}return}const i=e.statistic_id,a=(0,c.Kd)(this.hass,e.statistic_id,e);s.push({id:i,name:a,state:t,strings:[i,a]})})),s.length?(s.length>1&&s.sort(((e,t)=>(0,l.$)(e.name||"",t.name||"",this.hass.locale.language))),s.push({id:"__missing",name:this.hass.localize("ui.components.statistic-picker.missing_entity"),strings:[]}),s):[{id:"",name:this.hass.localize("ui.components.statistic-picker.no_match"),strings:[]}]}))}},{kind:"method",key:"open",value:function(){var e;null===(e=this.comboBox)||void 0===e||e.open()}},{kind:"method",key:"focus",value:function(){var e;null===(e=this.comboBox)||void 0===e||e.focus()}},{kind:"method",key:"willUpdate",value:function(e){(!this.hasUpdated&&!this.statisticIds||e.has("statisticTypes"))&&this._getStatisticIds(),(!this._init&&this.statisticIds||e.has("_opened")&&this._opened)&&(this._init=!0,this.hasUpdated?this._statistics=this._getStatistics(this.statisticIds,this.includeStatisticsUnitOfMeasurement,this.includeUnitClass,this.includeDeviceClass,this.entitiesOnly,this.excludeStatistics):this.updateComplete.then((()=>{this._statistics=this._getStatistics(this.statisticIds,this.includeStatisticsUnitOfMeasurement,this.includeUnitClass,this.includeDeviceClass,this.entitiesOnly,this.excludeStatistics)})))}},{kind:"method",key:"render",value:function(){var e;return 0===this._statistics.length?o.Ld:o.dy` <ha-combo-box .hass="${this.hass}" .label="${void 0===this.label&&this.hass?this.hass.localize("ui.components.statistic-picker.statistic"):this.label}" .value="${this._value}" .renderer="${this._rowRenderer}" .disabled="${this.disabled}" .allowCustomValue="${this.allowCustomEntity}" .items="${this._statistics}" .filteredItems="${null!==(e=this._filteredItems)&&void 0!==e?e:this._statistics}" item-value-path="id" item-id-path="id" item-label-path="name" @opened-changed="${this._openedChanged}" @value-changed="${this._statisticChanged}" @filter-changed="${this._filterChanged}"></ha-combo-box> `}},{kind:"method",key:"_getStatisticIds",value:async function(){this.statisticIds=await(0,c.uR)(this.hass,this.statisticTypes)}},{kind:"get",key:"_value",value:function(){return this.value||""}},{kind:"method",key:"_statisticChanged",value:function(e){e.stopPropagation();let t=e.detail.value;"__missing"===t&&(t=""),t!==this._value&&this._setValue(t)}},{kind:"method",key:"_openedChanged",value:function(e){this._opened=e.detail.value}},{kind:"method",key:"_filterChanged",value:function(e){const t=e.detail.value.toLowerCase();this._filteredItems=t.length?(0,h.q)(t,this._statistics):void 0}},{kind:"method",key:"_setValue",value:function(e){this.value=e,setTimeout((()=>{(0,r.B)(this,"value-changed",{value:e}),(0,r.B)(this,"change")}),0)}}]}}),o.oi)},32511:(e,t,i)=>{var a=i(17463),o=i(58417),n=i(39274),s=i(68144),d=i(79932);(0,a.Z)([(0,d.Mo)("ha-checkbox")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",static:!0,key:"styles",value:()=>[n.W,s.iv`:host{--mdc-theme-secondary:var(--primary-color)}`]}]}}),o.A)},77576:(e,t,i)=>{var a=i(17463),o=i(34541),n=i(47838),s=i(29530),d=(i(93584),i(53947)),r=i(68144),l=i(79932),c=i(30153),u=i(47181);i(10983),i(73366),i(3555);(0,d.hC)("vaadin-combo-box-item",r.iv`:host{padding:0!important}:host([focused]:not([disabled])){background-color:rgba(var(--rgb-primary-text-color,0,0,0),.12)}:host([selected]:not([disabled])){background-color:transparent;color:var(--mdc-theme-primary);--mdc-ripple-color:var(--mdc-theme-primary);--mdc-theme-text-primary-on-background:var(--mdc-theme-primary)}:host([selected]:not([disabled])):before{background-color:var(--mdc-theme-primary);opacity:.12;content:"";position:absolute;top:0;left:0;width:100%;height:100%}:host([selected][focused]:not([disabled])):before{opacity:.24}:host(:hover:not([disabled])){background-color:transparent}[part=content]{width:100%}[part=checkmark]{display:none}`);(0,a.Z)([(0,l.Mo)("ha-combo-box")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,l.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,l.Cb)()],key:"label",value:void 0},{kind:"field",decorators:[(0,l.Cb)()],key:"value",value:void 0},{kind:"field",decorators:[(0,l.Cb)()],key:"placeholder",value:void 0},{kind:"field",decorators:[(0,l.Cb)()],key:"validationMessage",value:void 0},{kind:"field",decorators:[(0,l.Cb)()],key:"helper",value:void 0},{kind:"field",decorators:[(0,l.Cb)({attribute:"error-message"})],key:"errorMessage",value:void 0},{kind:"field",decorators:[(0,l.Cb)({type:Boolean})],key:"invalid",value:()=>!1},{kind:"field",decorators:[(0,l.Cb)({type:Boolean})],key:"icon",value:()=>!1},{kind:"field",decorators:[(0,l.Cb)({attribute:!1})],key:"items",value:void 0},{kind:"field",decorators:[(0,l.Cb)({attribute:!1})],key:"filteredItems",value:void 0},{kind:"field",decorators:[(0,l.Cb)({attribute:!1})],key:"dataProvider",value:void 0},{kind:"field",decorators:[(0,l.Cb)({attribute:"allow-custom-value",type:Boolean})],key:"allowCustomValue",value:()=>!1},{kind:"field",decorators:[(0,l.Cb)({attribute:"item-value-path"})],key:"itemValuePath",value:()=>"value"},{kind:"field",decorators:[(0,l.Cb)({attribute:"item-label-path"})],key:"itemLabelPath",value:()=>"label"},{kind:"field",decorators:[(0,l.Cb)({attribute:"item-id-path"})],key:"itemIdPath",value:void 0},{kind:"field",decorators:[(0,l.Cb)()],key:"renderer",value:void 0},{kind:"field",decorators:[(0,l.Cb)({type:Boolean})],key:"disabled",value:()=>!1},{kind:"field",decorators:[(0,l.Cb)({type:Boolean})],key:"required",value:()=>!1},{kind:"field",decorators:[(0,l.Cb)({type:Boolean,reflect:!0,attribute:"opened"})],key:"opened",value:void 0},{kind:"field",decorators:[(0,l.IO)("vaadin-combo-box-light",!0)],key:"_comboBox",value:void 0},{kind:"field",decorators:[(0,l.IO)("ha-textfield",!0)],key:"_inputElement",value:void 0},{kind:"field",key:"_overlayMutationObserver",value:void 0},{kind:"field",key:"_bodyMutationObserver",value:void 0},{kind:"method",key:"open",value:async function(){var e;await this.updateComplete,null===(e=this._comboBox)||void 0===e||e.open()}},{kind:"method",key:"focus",value:async function(){var e,t;await this.updateComplete,await(null===(e=this._inputElement)||void 0===e?void 0:e.updateComplete),null===(t=this._inputElement)||void 0===t||t.focus()}},{kind:"method",key:"disconnectedCallback",value:function(){(0,o.Z)((0,n.Z)(i.prototype),"disconnectedCallback",this).call(this),this._overlayMutationObserver&&(this._overlayMutationObserver.disconnect(),this._overlayMutationObserver=void 0),this._bodyMutationObserver&&(this._bodyMutationObserver.disconnect(),this._bodyMutationObserver=void 0)}},{kind:"get",key:"selectedItem",value:function(){return this._comboBox.selectedItem}},{kind:"method",key:"setInputValue",value:function(e){this._comboBox.value=e}},{kind:"method",key:"render",value:function(){var e;return r.dy` <vaadin-combo-box-light .itemValuePath="${this.itemValuePath}" .itemIdPath="${this.itemIdPath}" .itemLabelPath="${this.itemLabelPath}" .items="${this.items}" .value="${this.value||""}" .filteredItems="${this.filteredItems}" .dataProvider="${this.dataProvider}" .allowCustomValue="${this.allowCustomValue}" .disabled="${this.disabled}" .required="${this.required}" ${(0,s.t)(this.renderer||this._defaultRowRenderer)} @opened-changed="${this._openedChanged}" @filter-changed="${this._filterChanged}" @value-changed="${this._valueChanged}" attr-for-value="value"> <ha-textfield label="${(0,c.o)(this.label)}" placeholder="${(0,c.o)(this.placeholder)}" ?disabled="${this.disabled}" ?required="${this.required}" validationMessage="${(0,c.o)(this.validationMessage)}" .errorMessage="${this.errorMessage}" class="input" autocapitalize="none" autocomplete="off" autocorrect="off" input-spellcheck="false" .suffix="${r.dy`<div style="width:28px" role="none presentation"></div>`}" .icon="${this.icon}" .invalid="${this.invalid}" helper="${(0,c.o)(this.helper)}" helperPersistent> <slot name="icon" slot="leadingIcon"></slot> </ha-textfield> ${this.value?r.dy`<ha-svg-icon role="button" tabindex="-1" aria-label="${(0,c.o)(null===(e=this.hass)||void 0===e?void 0:e.localize("ui.common.clear"))}" class="clear-button" .path="${"M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z"}" @click="${this._clearValue}"></ha-svg-icon>`:""} <ha-svg-icon role="button" tabindex="-1" aria-label="${(0,c.o)(this.label)}" aria-expanded="${this.opened?"true":"false"}" class="toggle-button" .path="${this.opened?"M7,15L12,10L17,15H7Z":"M7,10L12,15L17,10H7Z"}" @click="${this._toggleOpen}"></ha-svg-icon> </vaadin-combo-box-light> `}},{kind:"field",key:"_defaultRowRenderer",value(){return e=>r.dy`<ha-list-item> ${this.itemLabelPath?e[this.itemLabelPath]:e} </ha-list-item>`}},{kind:"method",key:"_clearValue",value:function(e){e.stopPropagation(),(0,u.B)(this,"value-changed",{value:void 0})}},{kind:"method",key:"_toggleOpen",value:function(e){var t,i;this.opened?(null===(t=this._comboBox)||void 0===t||t.close(),e.stopPropagation()):null===(i=this._comboBox)||void 0===i||i.inputElement.focus()}},{kind:"method",key:"_openedChanged",value:function(e){e.stopPropagation();const t=e.detail.value;if(setTimeout((()=>{this.opened=t}),0),(0,u.B)(this,"opened-changed",{value:e.detail.value}),t){const e=document.querySelector("vaadin-combo-box-overlay");e&&this._removeInert(e),this._observeBody()}else{var i;null===(i=this._bodyMutationObserver)||void 0===i||i.disconnect(),this._bodyMutationObserver=void 0}}},{kind:"method",key:"_observeBody",value:function(){"MutationObserver"in window&&!this._bodyMutationObserver&&(this._bodyMutationObserver=new MutationObserver((e=>{e.forEach((e=>{e.addedNodes.forEach((e=>{"VAADIN-COMBO-BOX-OVERLAY"===e.nodeName&&this._removeInert(e)})),e.removedNodes.forEach((e=>{var t;"VAADIN-COMBO-BOX-OVERLAY"===e.nodeName&&(null===(t=this._overlayMutationObserver)||void 0===t||t.disconnect(),this._overlayMutationObserver=void 0)}))}))})),this._bodyMutationObserver.observe(document.body,{childList:!0}))}},{kind:"method",key:"_removeInert",value:function(e){var t;if(e.inert)return e.inert=!1,null===(t=this._overlayMutationObserver)||void 0===t||t.disconnect(),void(this._overlayMutationObserver=void 0);"MutationObserver"in window&&!this._overlayMutationObserver&&(this._overlayMutationObserver=new MutationObserver((e=>{e.forEach((e=>{if("inert"===e.attributeName){const i=e.target;var t;if(i.inert)null===(t=this._overlayMutationObserver)||void 0===t||t.disconnect(),this._overlayMutationObserver=void 0,i.inert=!1}}))})),this._overlayMutationObserver.observe(e,{attributes:!0}))}},{kind:"method",key:"_filterChanged",value:function(e){e.stopPropagation(),(0,u.B)(this,"filter-changed",{value:e.detail.value})}},{kind:"method",key:"_valueChanged",value:function(e){e.stopPropagation(),this.allowCustomValue||(this._comboBox._closeOnBlurIsPrevented=!0);const t=e.detail.value;t!==this.value&&(0,u.B)(this,"value-changed",{value:t||void 0})}},{kind:"get",static:!0,key:"styles",value:function(){return r.iv`:host{display:block;width:100%}vaadin-combo-box-light{position:relative;--vaadin-combo-box-overlay-max-height:calc(45vh - 56px)}ha-textfield{width:100%}ha-textfield>ha-icon-button{--mdc-icon-button-size:24px;padding:2px;color:var(--secondary-text-color)}ha-svg-icon{color:var(--input-dropdown-icon-color);position:absolute;cursor:pointer}.toggle-button{right:12px;top:-10px;inset-inline-start:initial;inset-inline-end:12px;direction:var(--direction)}:host([opened]) .toggle-button{color:var(--primary-color)}.clear-button{--mdc-icon-size:20px;top:-7px;right:36px;inset-inline-start:initial;inset-inline-end:36px;direction:var(--direction)}`}}]}}),r.oi)},34821:(e,t,i)=>{i.d(t,{i:()=>h});var a=i(17463),o=i(34541),n=i(47838),s=i(87762),d=i(91632),r=i(68144),l=i(79932),c=i(74265);i(10983);const u=["button","ha-list-item"],h=(e,t)=>{var i;return r.dy` <div class="header_title">${t}</div> <ha-icon-button .label="${null!==(i=null==e?void 0:e.localize("ui.dialogs.generic.close"))&&void 0!==i?i:"Close"}" .path="${"M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z"}" dialogAction="close" class="header_button"></ha-icon-button> `};(0,a.Z)([(0,l.Mo)("ha-dialog")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",key:c.gA,value:void 0},{kind:"method",key:"scrollToPos",value:function(e,t){var i;null===(i=this.contentElement)||void 0===i||i.scrollTo(e,t)}},{kind:"method",key:"renderHeading",value:function(){return r.dy`<slot name="heading"> ${(0,o.Z)((0,n.Z)(i.prototype),"renderHeading",this).call(this)} </slot>`}},{kind:"method",key:"firstUpdated",value:function(){var e;(0,o.Z)((0,n.Z)(i.prototype),"firstUpdated",this).call(this),this.suppressDefaultPressSelector=[this.suppressDefaultPressSelector,u].join(", "),this._updateScrolledAttribute(),null===(e=this.contentElement)||void 0===e||e.addEventListener("scroll",this._onScroll,{passive:!0})}},{kind:"method",key:"disconnectedCallback",value:function(){(0,o.Z)((0,n.Z)(i.prototype),"disconnectedCallback",this).call(this),this.contentElement.removeEventListener("scroll",this._onScroll)}},{kind:"field",key:"_onScroll",value(){return()=>{this._updateScrolledAttribute()}}},{kind:"method",key:"_updateScrolledAttribute",value:function(){this.contentElement&&this.toggleAttribute("scrolled",0!==this.contentElement.scrollTop)}},{kind:"field",static:!0,key:"styles",value:()=>[d.W,r.iv`:host([scrolled]) ::slotted(ha-dialog-header){border-bottom:1px solid var(--mdc-dialog-scroll-divider-color,rgba(0,0,0,.12))}.mdc-dialog{--mdc-dialog-scroll-divider-color:var(
          --dialog-scroll-divider-color,
          var(--divider-color)
        );z-index:var(--dialog-z-index,8);-webkit-backdrop-filter:var(--dialog-backdrop-filter,none);backdrop-filter:var(--dialog-backdrop-filter,none);--mdc-dialog-box-shadow:var(--dialog-box-shadow, none);--mdc-typography-headline6-font-weight:400;--mdc-typography-headline6-font-size:1.574rem}.mdc-dialog__actions{justify-content:var(--justify-action-buttons,flex-end);padding-bottom:max(env(safe-area-inset-bottom),24px)}.mdc-dialog__actions span:first-child{flex:var(--secondary-action-button-flex,unset)}.mdc-dialog__actions span:nth-child(2){flex:var(--primary-action-button-flex,unset)}.mdc-dialog__container{align-items:var(--vertical-align-dialog,center)}.mdc-dialog__title{padding:24px 24px 0 24px;text-overflow:ellipsis;overflow:hidden}.mdc-dialog__actions{padding:12px 24px 12px 24px}.mdc-dialog__title::before{display:block;height:0px}.mdc-dialog .mdc-dialog__content{position:var(--dialog-content-position,relative);padding:var(--dialog-content-padding,24px)}:host([hideactions]) .mdc-dialog .mdc-dialog__content{padding-bottom:max(var(--dialog-content-padding,24px),env(safe-area-inset-bottom))}.mdc-dialog .mdc-dialog__surface{position:var(--dialog-surface-position,relative);top:var(--dialog-surface-top);margin-top:var(--dialog-surface-margin-top);min-height:var(--mdc-dialog-min-height,auto);border-radius:var(--ha-dialog-border-radius,28px)}:host([flexContent]) .mdc-dialog .mdc-dialog__content{display:flex;flex-direction:column}.header_title{margin-right:32px;margin-inline-end:32px;margin-inline-start:initial;direction:var(--direction)}.header_button{position:absolute;right:16px;top:14px;text-decoration:none;color:inherit;inset-inline-start:initial;inset-inline-end:16px;direction:var(--direction)}.dialog-actions{inset-inline-start:initial!important;inset-inline-end:0px!important;direction:var(--direction)}`]}]}}),s.M)},83927:(e,t,i)=>{var a=i(17463),o=i(8485),n=i(92038),s=i(68144),d=i(79932),r=i(47181);(0,a.Z)([(0,d.Mo)("ha-formfield")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"method",key:"_labelClick",value:function(){const e=this.input;if(e&&(e.focus(),!e.disabled))switch(e.tagName){case"HA-CHECKBOX":e.checked=!e.checked,(0,r.B)(e,"change");break;case"HA-RADIO":e.checked=!0,(0,r.B)(e,"change");break;default:e.click()}}},{kind:"field",static:!0,key:"styles",value:()=>[n.W,s.iv`:host(:not([alignEnd])) ::slotted(ha-switch){margin-right:10px;margin-inline-end:10px;margin-inline-start:inline}.mdc-form-field>label{direction:var(--direction);margin-inline-start:0;margin-inline-end:auto;padding-inline-start:4px;padding-inline-end:0}`]}]}}),o.a)},73366:(e,t,i)=>{i.d(t,{M:()=>c});var a=i(17463),o=i(34541),n=i(47838),s=i(61092),d=i(96762),r=i(68144),l=i(79932);let c=(0,a.Z)([(0,l.Mo)("ha-list-item")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"method",key:"renderRipple",value:function(){return this.noninteractive?"":(0,o.Z)((0,n.Z)(i.prototype),"renderRipple",this).call(this)}},{kind:"get",static:!0,key:"styles",value:function(){return[d.W,r.iv`:host{padding-left:var(--mdc-list-side-padding-left,var(--mdc-list-side-padding,20px));padding-right:var(--mdc-list-side-padding-right,var(--mdc-list-side-padding,20px))}:host([graphic=avatar]:not([twoLine])),:host([graphic=icon]:not([twoLine])){height:48px}span.material-icons:first-of-type{margin-inline-start:0px!important;margin-inline-end:var(--mdc-list-item-graphic-margin,16px)!important;direction:var(--direction)}span.material-icons:last-of-type{margin-inline-start:auto!important;margin-inline-end:0px!important;direction:var(--direction)}.mdc-deprecated-list-item__meta{display:var(--mdc-list-item-meta-display);align-items:center}:host([multiline-secondary]){height:auto}:host([multiline-secondary]) .mdc-deprecated-list-item__text{padding:8px 0}:host([multiline-secondary]) .mdc-deprecated-list-item__secondary-text{text-overflow:initial;white-space:normal;overflow:auto;display:inline-block;margin-top:10px}:host([multiline-secondary]) .mdc-deprecated-list-item__primary-text{margin-top:10px}:host([multiline-secondary]) .mdc-deprecated-list-item__secondary-text::before{display:none}:host([multiline-secondary]) .mdc-deprecated-list-item__primary-text::before{display:none}:host([disabled]){color:var(--disabled-text-color)}:host([noninteractive]){pointer-events:unset}`]}}]}}),s.K)},33220:(e,t,i)=>{var a=i(17463),o=i(35433),n=i(44973),s=i(68144),d=i(79932);(0,a.Z)([(0,d.Mo)("ha-radio")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",static:!0,key:"styles",value:()=>[n.W,s.iv`:host{--mdc-theme-secondary:var(--primary-color)}`]}]}}),o.J)},3555:(e,t,i)=>{var a=i(17463),o=i(34541),n=i(47838),s=i(42977),d=i(31338),r=i(68144),l=i(79932),c=i(30418);(0,a.Z)([(0,l.Mo)("ha-textfield")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,l.Cb)({type:Boolean})],key:"invalid",value:void 0},{kind:"field",decorators:[(0,l.Cb)({attribute:"error-message"})],key:"errorMessage",value:void 0},{kind:"field",decorators:[(0,l.Cb)({type:Boolean})],key:"icon",value:void 0},{kind:"field",decorators:[(0,l.Cb)({type:Boolean})],key:"iconTrailing",value:void 0},{kind:"field",decorators:[(0,l.Cb)()],key:"autocomplete",value:void 0},{kind:"field",decorators:[(0,l.Cb)()],key:"autocorrect",value:void 0},{kind:"field",decorators:[(0,l.Cb)({attribute:"input-spellcheck"})],key:"inputSpellcheck",value:void 0},{kind:"field",decorators:[(0,l.IO)("input")],key:"formElement",value:void 0},{kind:"method",key:"updated",value:function(e){(0,o.Z)((0,n.Z)(i.prototype),"updated",this).call(this,e),(e.has("invalid")&&(this.invalid||void 0!==e.get("invalid"))||e.has("errorMessage"))&&(this.setCustomValidity(this.invalid?this.errorMessage||"Invalid":""),this.reportValidity()),e.has("autocomplete")&&(this.autocomplete?this.formElement.setAttribute("autocomplete",this.autocomplete):this.formElement.removeAttribute("autocomplete")),e.has("autocorrect")&&(this.autocorrect?this.formElement.setAttribute("autocorrect",this.autocorrect):this.formElement.removeAttribute("autocorrect")),e.has("inputSpellcheck")&&(this.inputSpellcheck?this.formElement.setAttribute("spellcheck",this.inputSpellcheck):this.formElement.removeAttribute("spellcheck"))}},{kind:"method",key:"renderIcon",value:function(e,t=!1){const i=t?"trailing":"leading";return r.dy` <span class="mdc-text-field__icon mdc-text-field__icon--${i}" tabindex="${t?1:-1}"> <slot name="${i}Icon"></slot> </span> `}},{kind:"field",static:!0,key:"styles",value:()=>[d.W,r.iv`.mdc-text-field__input{width:var(--ha-textfield-input-width,100%)}.mdc-text-field:not(.mdc-text-field--with-leading-icon){padding:var(--text-field-padding,0px 16px)}.mdc-text-field__affix--suffix{padding-left:var(--text-field-suffix-padding-left,12px);padding-right:var(--text-field-suffix-padding-right,0px);padding-inline-start:var(--text-field-suffix-padding-left,12px);padding-inline-end:var(--text-field-suffix-padding-right,0px);direction:var(--direction)}.mdc-text-field--with-leading-icon{padding-inline-start:var(--text-field-suffix-padding-left,0px);padding-inline-end:var(--text-field-suffix-padding-right,16px);direction:var(--direction)}.mdc-text-field--with-leading-icon.mdc-text-field--with-trailing-icon{padding-left:var(--text-field-suffix-padding-left,0px);padding-right:var(--text-field-suffix-padding-right,0px);padding-inline-start:var(--text-field-suffix-padding-left,0px);padding-inline-end:var(--text-field-suffix-padding-right,0px)}.mdc-text-field:not(.mdc-text-field--disabled) .mdc-text-field__affix--suffix{color:var(--secondary-text-color)}.mdc-text-field__icon{color:var(--secondary-text-color)}.mdc-text-field__icon--leading{margin-inline-start:16px;margin-inline-end:8px;direction:var(--direction)}.mdc-text-field__icon--trailing{padding:var(--textfield-icon-trailing-padding,12px)}.mdc-floating-label:not(.mdc-floating-label--float-above){text-overflow:ellipsis;width:inherit;padding-right:30px;padding-inline-end:30px;padding-inline-start:initial;box-sizing:border-box;direction:var(--direction)}input{text-align:var(--text-field-text-align,start)}::-ms-reveal{display:none}:host([no-spinner]) input::-webkit-inner-spin-button,:host([no-spinner]) input::-webkit-outer-spin-button{-webkit-appearance:none;margin:0}:host([no-spinner]) input[type=number]{-moz-appearance:textfield}.mdc-text-field__ripple{overflow:hidden}.mdc-text-field{overflow:var(--text-field-overflow)}.mdc-floating-label{inset-inline-start:16px!important;inset-inline-end:initial!important;transform-origin:var(--float-start);direction:var(--direction);text-align:var(--float-start)}.mdc-text-field--with-leading-icon.mdc-text-field--filled .mdc-floating-label{max-width:calc(100% - 48px - var(--text-field-suffix-padding-left,0px));inset-inline-start:calc(48px + var(--text-field-suffix-padding-left,0px))!important;inset-inline-end:initial!important;direction:var(--direction)}.mdc-text-field__input[type=number]{direction:var(--direction)}.mdc-text-field__affix--prefix{padding-right:var(--text-field-prefix-padding-right,2px)}.mdc-text-field:not(.mdc-text-field--disabled) .mdc-text-field__affix--prefix{color:var(--mdc-text-field-label-ink-color)}`,"rtl"===c.E.document.dir?r.iv`.mdc-floating-label,.mdc-text-field--with-leading-icon,.mdc-text-field--with-leading-icon.mdc-text-field--filled .mdc-floating-label,.mdc-text-field__affix--suffix,.mdc-text-field__icon--leading,.mdc-text-field__input[type=number]{direction:rtl}`:r.iv``]}]}}),s.P)},22814:(e,t,i)=>{i.d(t,{Cp:()=>s,TZ:()=>d,W2:()=>n,YY:()=>r,iI:()=>o,oT:()=>a});const a=e=>e.map((e=>{if("string"!==e.type)return e;switch(e.name){case"username":return{...e,autocomplete:"username"};case"password":return{...e,autocomplete:"current-password"};case"code":return{...e,autocomplete:"one-time-code"};default:return e}})),o=(e,t)=>e.callWS({type:"auth/sign_path",path:t}),n=async(e,t,i,a)=>e.callWS({type:"config/auth_provider/homeassistant/create",user_id:t,username:i,password:a}),s=(e,t,i)=>e.callWS({type:"config/auth_provider/homeassistant/change_password",current_password:t,new_password:i}),d=(e,t,i)=>e.callWS({type:"config/auth_provider/homeassistant/admin_change_password",user_id:t,password:i}),r=e=>e.callWS({type:"auth/delete_all_refresh_tokens"})},56007:(e,t,i)=>{i.d(t,{PX:()=>s,V_:()=>d,lz:()=>n,nZ:()=>o,rk:()=>l});var a=i(57966);const o="unavailable",n="unknown",s="off",d=[o,n],r=[o,n,s],l=(0,a.z)(d);(0,a.z)(r)},87651:(e,t,i)=>{i.a(e,(async(e,a)=>{try{i.r(t),i.d(t,{DialogEnergySolarSettings:()=>g});var o=i(17463),n=(i(14271),i(68144)),s=i(79932),d=i(47181),r=(i(33762),i(32511),i(34821),i(83927),i(33220),i(81582)),l=i(55424),c=i(41499),u=i(2852),h=i(11654),v=i(11254),p=e([l]);l=(p.then?(await p)():p)[0];const f="M11.45,2V5.55L15,3.77L11.45,2M10.45,8L8,10.46L11.75,11.71L10.45,8M2,11.45L3.77,15L5.55,11.45H2M10,2H2V10C2.57,10.17 3.17,10.25 3.77,10.25C7.35,10.26 10.26,7.35 10.27,3.75C10.26,3.16 10.17,2.57 10,2M17,22V16H14L19,7V13H22L17,22Z",m=["energy"];let g=(0,o.Z)([(0,s.Mo)("dialog-energy-solar-settings")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,s.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,s.SB)()],key:"_params",value:void 0},{kind:"field",decorators:[(0,s.SB)()],key:"_source",value:void 0},{kind:"field",decorators:[(0,s.SB)()],key:"_configEntries",value:void 0},{kind:"field",decorators:[(0,s.SB)()],key:"_forecast",value:void 0},{kind:"field",decorators:[(0,s.SB)()],key:"_energy_units",value:void 0},{kind:"field",decorators:[(0,s.SB)()],key:"_error",value:void 0},{kind:"field",key:"_excludeList",value:void 0},{kind:"method",key:"showDialog",value:async function(e){this._params=e,this._fetchSolarForecastConfigEntries(),this._source=e.source?{...e.source}:(0,l.rl)(),this._forecast=null!==this._source.config_entry_solar_forecast,this._energy_units=(await(0,c.J9)(this.hass,"energy")).units,this._excludeList=this._params.solar_sources.map((e=>e.stat_energy_from)).filter((e=>{var t;return e!==(null===(t=this._source)||void 0===t?void 0:t.stat_energy_from)}))}},{kind:"method",key:"closeDialog",value:function(){this._params=void 0,this._source=void 0,this._error=void 0,this._excludeList=void 0,(0,d.B)(this,"dialog-closed",{dialog:this.localName})}},{kind:"method",key:"render",value:function(){var e,t;if(!this._params||!this._source)return n.Ld;const i=(null===(e=this._energy_units)||void 0===e?void 0:e.join(", "))||"";return n.dy` <ha-dialog open .heading="${n.dy`<ha-svg-icon .path="${f}" style="--mdc-icon-size:32px"></ha-svg-icon> ${this.hass.localize("ui.panel.config.energy.solar.dialog.header")}`}" @closed="${this.closeDialog}"> ${this._error?n.dy`<p class="error">${this._error}</p>`:""} <div> ${this.hass.localize("ui.panel.config.energy.solar.dialog.entity_para",{unit:i})} </div> <ha-statistic-picker .hass="${this.hass}" .helpMissingEntityUrl="${l.kJ}" .includeUnitClass="${m}" .value="${this._source.stat_energy_from}" .label="${this.hass.localize("ui.panel.config.energy.solar.dialog.solar_production_energy")}" .excludeStatistics="${this._excludeList}" @value-changed="${this._statisticChanged}" dialogInitialFocus></ha-statistic-picker> <h3> ${this.hass.localize("ui.panel.config.energy.solar.dialog.solar_production_forecast")} </h3> <p> ${this.hass.localize("ui.panel.config.energy.solar.dialog.solar_production_forecast_description")} </p> <ha-formfield label="${this.hass.localize("ui.panel.config.energy.solar.dialog.dont_forecast_production")}"> <ha-radio value="false" name="forecast" .checked="${!this._forecast}" @change="${this._handleForecastChanged}"></ha-radio> </ha-formfield> <ha-formfield label="${this.hass.localize("ui.panel.config.energy.solar.dialog.forecast_production")}"> <ha-radio value="true" name="forecast" .checked="${this._forecast}" @change="${this._handleForecastChanged}"></ha-radio> </ha-formfield> ${this._forecast?n.dy`<div class="forecast-options"> ${null===(t=this._configEntries)||void 0===t?void 0:t.map((e=>{var t,i;return n.dy`<ha-formfield .label="${n.dy`<div style="display:flex;align-items:center"> <img alt="" crossorigin="anonymous" referrerpolicy="no-referrer" style="height:24px;margin-right:16px" src="${(0,v.X1)({domain:e.domain,type:"icon",darkOptimized:null===(t=this.hass.themes)||void 0===t?void 0:t.darkMode})}">${e.title} </div>`}"> <ha-checkbox .entry="${e}" @change="${this._forecastCheckChanged}" .checked="${null===(i=this._source)||void 0===i||null===(i=i.config_entry_solar_forecast)||void 0===i?void 0:i.includes(e.entry_id)}"> </ha-checkbox> </ha-formfield>`}))} <mwc-button @click="${this._addForecast}"> ${this.hass.localize("ui.panel.config.energy.solar.dialog.add_forecast")} </mwc-button> </div>`:""} <mwc-button @click="${this.closeDialog}" slot="secondaryAction"> ${this.hass.localize("ui.common.cancel")} </mwc-button> <mwc-button @click="${this._save}" .disabled="${!this._source.stat_energy_from}" slot="primaryAction"> ${this.hass.localize("ui.common.save")} </mwc-button> </ha-dialog> `}},{kind:"method",key:"_fetchSolarForecastConfigEntries",value:async function(){const e=this._params.info.solar_forecast_domains;this._configEntries=0===e.length?[]:1===e.length?await(0,r.pB)(this.hass,{type:["service"],domain:e[0]}):(await(0,r.pB)(this.hass,{type:["service"]})).filter((t=>e.includes(t.domain)))}},{kind:"method",key:"_handleForecastChanged",value:function(e){const t=e.currentTarget;this._forecast="true"===t.value}},{kind:"method",key:"_forecastCheckChanged",value:function(e){const t=e.currentTarget,i=t.entry;t.checked?(null===this._source.config_entry_solar_forecast&&(this._source.config_entry_solar_forecast=[]),this._source.config_entry_solar_forecast.push(i.entry_id)):this._source.config_entry_solar_forecast.splice(this._source.config_entry_solar_forecast.indexOf(i.entry_id),1)}},{kind:"method",key:"_addForecast",value:function(){(0,u.t)(this,{startFlowHandler:"forecast_solar",dialogClosedCallback:e=>{e.entryId&&(null===this._source.config_entry_solar_forecast&&(this._source.config_entry_solar_forecast=[]),this._source.config_entry_solar_forecast.push(e.entryId),this._fetchSolarForecastConfigEntries())}})}},{kind:"method",key:"_statisticChanged",value:function(e){this._source={...this._source,stat_energy_from:e.detail.value}}},{kind:"method",key:"_save",value:async function(){try{this._forecast||(this._source.config_entry_solar_forecast=null),await this._params.saveCallback(this._source),this.closeDialog()}catch(e){this._error=e.message}}},{kind:"get",static:!0,key:"styles",value:function(){return[h.Qx,h.yu,n.iv`ha-dialog{--mdc-dialog-max-width:430px}img{height:24px;margin-right:16px}ha-formfield{display:block}ha-statistic-picker{width:100%}.forecast-options{padding-left:32px}.forecast-options mwc-button{padding-left:8px}`]}}]}}),n.oi);a()}catch(e){a(e)}}))}};
//# sourceMappingURL=39297.DgcC5axxCFc.js.map