export const id=13327;export const ids=[13327];export const modules={55642:(e,t,i)=>{i.d(t,{h:()=>a});var n=i(68144),d=i(57835);const a=(0,d.XM)(class extends d.Xe{constructor(e){if(super(e),this._element=void 0,e.type!==d.pX.CHILD)throw new Error("dynamicElementDirective can only be used in content bindings")}update(e,[t,i]){return this._element&&this._element.localName===t?(i&&Object.entries(i).forEach((([e,t])=>{this._element[e]=t})),n.Jb):this.render(t,i)}render(e,t){return this._element=document.createElement(e),t&&Object.entries(t).forEach((([e,t])=>{this._element[e]=t})),this._element}})},35703:(e,t,i)=>{var n=i(17463),d=i(68144),a=i(79932),l=i(14516),r=i(47181),o=i(84627);i(74535);(0,n.Z)([(0,a.Mo)("ha-entities-picker")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,a.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,a.Cb)({type:Array})],key:"value",value:void 0},{kind:"field",decorators:[(0,a.Cb)({type:Boolean})],key:"disabled",value:void 0},{kind:"field",decorators:[(0,a.Cb)({type:Boolean})],key:"required",value:void 0},{kind:"field",decorators:[(0,a.Cb)()],key:"helper",value:void 0},{kind:"field",decorators:[(0,a.Cb)({type:Array,attribute:"include-domains"})],key:"includeDomains",value:void 0},{kind:"field",decorators:[(0,a.Cb)({type:Array,attribute:"exclude-domains"})],key:"excludeDomains",value:void 0},{kind:"field",decorators:[(0,a.Cb)({type:Array,attribute:"include-device-classes"})],key:"includeDeviceClasses",value:void 0},{kind:"field",decorators:[(0,a.Cb)({type:Array,attribute:"include-unit-of-measurement"})],key:"includeUnitOfMeasurement",value:void 0},{kind:"field",decorators:[(0,a.Cb)({type:Array,attribute:"include-entities"})],key:"includeEntities",value:void 0},{kind:"field",decorators:[(0,a.Cb)({type:Array,attribute:"exclude-entities"})],key:"excludeEntities",value:void 0},{kind:"field",decorators:[(0,a.Cb)({attribute:"picked-entity-label"})],key:"pickedEntityLabel",value:void 0},{kind:"field",decorators:[(0,a.Cb)({attribute:"pick-entity-label"})],key:"pickEntityLabel",value:void 0},{kind:"field",decorators:[(0,a.Cb)()],key:"entityFilter",value:void 0},{kind:"method",key:"render",value:function(){if(!this.hass)return d.Ld;const e=this._currentEntities;return d.dy` ${e.map((e=>d.dy` <div> <ha-entity-picker allow-custom-entity .curValue="${e}" .hass="${this.hass}" .includeDomains="${this.includeDomains}" .excludeDomains="${this.excludeDomains}" .includeEntities="${this.includeEntities}" .excludeEntities="${this.excludeEntities}" .includeDeviceClasses="${this.includeDeviceClasses}" .includeUnitOfMeasurement="${this.includeUnitOfMeasurement}" .entityFilter="${this._getEntityFilter(this.value,this.entityFilter)}" .value="${e}" .label="${this.pickedEntityLabel}" .disabled="${this.disabled}" @value-changed="${this._entityChanged}"></ha-entity-picker> </div> `))} <div> <ha-entity-picker allow-custom-entity .hass="${this.hass}" .includeDomains="${this.includeDomains}" .excludeDomains="${this.excludeDomains}" .includeEntities="${this.includeEntities}" .excludeEntities="${this.excludeEntities}" .includeDeviceClasses="${this.includeDeviceClasses}" .includeUnitOfMeasurement="${this.includeUnitOfMeasurement}" .entityFilter="${this._getEntityFilter(this.value,this.entityFilter)}" .label="${this.pickEntityLabel}" .helper="${this.helper}" .disabled="${this.disabled}" .required="${this.required&&!e.length}" @value-changed="${this._addEntity}"></ha-entity-picker> </div> `}},{kind:"field",key:"_getEntityFilter",value:()=>(0,l.Z)(((e,t)=>i=>(!e||!e.includes(i.entity_id))&&(!t||t(i))))},{kind:"get",key:"_currentEntities",value:function(){return this.value||[]}},{kind:"method",key:"_updateEntities",value:async function(e){this.value=e,(0,r.B)(this,"value-changed",{value:e})}},{kind:"method",key:"_entityChanged",value:function(e){e.stopPropagation();const t=e.currentTarget.curValue,i=e.detail.value;if(i===t||void 0!==i&&!(0,o.T)(i))return;const n=this._currentEntities;i&&!n.includes(i)?this._updateEntities(n.map((e=>e===t?i:e))):this._updateEntities(n.filter((e=>e!==t)))}},{kind:"method",key:"_addEntity",value:async function(e){e.stopPropagation();const t=e.detail.value;if(!t)return;if(e.currentTarget.value="",!t)return;const i=this._currentEntities;i.includes(t)||this._updateEntities([...i,t])}},{kind:"field",static:!0,key:"styles",value:()=>d.iv`div{margin-top:8px}`}]}}),d.oi)},73366:(e,t,i)=>{i.d(t,{M:()=>c});var n=i(17463),d=i(34541),a=i(47838),l=i(61092),r=i(96762),o=i(68144),s=i(79932);let c=(0,n.Z)([(0,s.Mo)("ha-list-item")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"method",key:"renderRipple",value:function(){return this.noninteractive?"":(0,d.Z)((0,a.Z)(i.prototype),"renderRipple",this).call(this)}},{kind:"get",static:!0,key:"styles",value:function(){return[r.W,o.iv`:host{padding-left:var(--mdc-list-side-padding-left,var(--mdc-list-side-padding,20px));padding-right:var(--mdc-list-side-padding-right,var(--mdc-list-side-padding,20px))}:host([graphic=avatar]:not([twoLine])),:host([graphic=icon]:not([twoLine])){height:48px}span.material-icons:first-of-type{margin-inline-start:0px!important;margin-inline-end:var(--mdc-list-item-graphic-margin,16px)!important;direction:var(--direction)}span.material-icons:last-of-type{margin-inline-start:auto!important;margin-inline-end:0px!important;direction:var(--direction)}.mdc-deprecated-list-item__meta{display:var(--mdc-list-item-meta-display);align-items:center}:host([multiline-secondary]){height:auto}:host([multiline-secondary]) .mdc-deprecated-list-item__text{padding:8px 0}:host([multiline-secondary]) .mdc-deprecated-list-item__secondary-text{text-overflow:initial;white-space:normal;overflow:auto;display:inline-block;margin-top:10px}:host([multiline-secondary]) .mdc-deprecated-list-item__primary-text{margin-top:10px}:host([multiline-secondary]) .mdc-deprecated-list-item__secondary-text::before{display:none}:host([multiline-secondary]) .mdc-deprecated-list-item__primary-text::before{display:none}:host([disabled]){color:var(--disabled-text-color)}:host([noninteractive]){pointer-events:unset}`]}}]}}),l.K)},3555:(e,t,i)=>{var n=i(17463),d=i(34541),a=i(47838),l=i(42977),r=i(31338),o=i(68144),s=i(79932),c=i(30418);(0,n.Z)([(0,s.Mo)("ha-textfield")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,s.Cb)({type:Boolean})],key:"invalid",value:void 0},{kind:"field",decorators:[(0,s.Cb)({attribute:"error-message"})],key:"errorMessage",value:void 0},{kind:"field",decorators:[(0,s.Cb)({type:Boolean})],key:"icon",value:void 0},{kind:"field",decorators:[(0,s.Cb)({type:Boolean})],key:"iconTrailing",value:void 0},{kind:"field",decorators:[(0,s.Cb)()],key:"autocomplete",value:void 0},{kind:"field",decorators:[(0,s.Cb)()],key:"autocorrect",value:void 0},{kind:"field",decorators:[(0,s.Cb)({attribute:"input-spellcheck"})],key:"inputSpellcheck",value:void 0},{kind:"field",decorators:[(0,s.IO)("input")],key:"formElement",value:void 0},{kind:"method",key:"updated",value:function(e){(0,d.Z)((0,a.Z)(i.prototype),"updated",this).call(this,e),(e.has("invalid")&&(this.invalid||void 0!==e.get("invalid"))||e.has("errorMessage"))&&(this.setCustomValidity(this.invalid?this.errorMessage||"Invalid":""),this.reportValidity()),e.has("autocomplete")&&(this.autocomplete?this.formElement.setAttribute("autocomplete",this.autocomplete):this.formElement.removeAttribute("autocomplete")),e.has("autocorrect")&&(this.autocorrect?this.formElement.setAttribute("autocorrect",this.autocorrect):this.formElement.removeAttribute("autocorrect")),e.has("inputSpellcheck")&&(this.inputSpellcheck?this.formElement.setAttribute("spellcheck",this.inputSpellcheck):this.formElement.removeAttribute("spellcheck"))}},{kind:"method",key:"renderIcon",value:function(e,t=!1){const i=t?"trailing":"leading";return o.dy` <span class="mdc-text-field__icon mdc-text-field__icon--${i}" tabindex="${t?1:-1}"> <slot name="${i}Icon"></slot> </span> `}},{kind:"field",static:!0,key:"styles",value:()=>[r.W,o.iv`.mdc-text-field__input{width:var(--ha-textfield-input-width,100%)}.mdc-text-field:not(.mdc-text-field--with-leading-icon){padding:var(--text-field-padding,0px 16px)}.mdc-text-field__affix--suffix{padding-left:var(--text-field-suffix-padding-left,12px);padding-right:var(--text-field-suffix-padding-right,0px);padding-inline-start:var(--text-field-suffix-padding-left,12px);padding-inline-end:var(--text-field-suffix-padding-right,0px);direction:var(--direction)}.mdc-text-field--with-leading-icon{padding-inline-start:var(--text-field-suffix-padding-left,0px);padding-inline-end:var(--text-field-suffix-padding-right,16px);direction:var(--direction)}.mdc-text-field--with-leading-icon.mdc-text-field--with-trailing-icon{padding-left:var(--text-field-suffix-padding-left,0px);padding-right:var(--text-field-suffix-padding-right,0px);padding-inline-start:var(--text-field-suffix-padding-left,0px);padding-inline-end:var(--text-field-suffix-padding-right,0px)}.mdc-text-field:not(.mdc-text-field--disabled) .mdc-text-field__affix--suffix{color:var(--secondary-text-color)}.mdc-text-field__icon{color:var(--secondary-text-color)}.mdc-text-field__icon--leading{margin-inline-start:16px;margin-inline-end:8px;direction:var(--direction)}.mdc-text-field__icon--trailing{padding:var(--textfield-icon-trailing-padding,12px)}.mdc-floating-label:not(.mdc-floating-label--float-above){text-overflow:ellipsis;width:inherit;padding-right:30px;padding-inline-end:30px;padding-inline-start:initial;box-sizing:border-box;direction:var(--direction)}input{text-align:var(--text-field-text-align,start)}::-ms-reveal{display:none}:host([no-spinner]) input::-webkit-inner-spin-button,:host([no-spinner]) input::-webkit-outer-spin-button{-webkit-appearance:none;margin:0}:host([no-spinner]) input[type=number]{-moz-appearance:textfield}.mdc-text-field__ripple{overflow:hidden}.mdc-text-field{overflow:var(--text-field-overflow)}.mdc-floating-label{inset-inline-start:16px!important;inset-inline-end:initial!important;transform-origin:var(--float-start);direction:var(--direction);text-align:var(--float-start)}.mdc-text-field--with-leading-icon.mdc-text-field--filled .mdc-floating-label{max-width:calc(100% - 48px - var(--text-field-suffix-padding-left,0px));inset-inline-start:calc(48px + var(--text-field-suffix-padding-left,0px))!important;inset-inline-end:initial!important;direction:var(--direction)}.mdc-text-field__input[type=number]{direction:var(--direction)}.mdc-text-field__affix--prefix{padding-right:var(--text-field-prefix-padding-right,2px)}.mdc-text-field:not(.mdc-text-field--disabled) .mdc-text-field__affix--prefix{color:var(--mdc-text-field-label-ink-color)}`,"rtl"===c.E.document.dir?o.iv`.mdc-floating-label,.mdc-text-field--with-leading-icon,.mdc-text-field--with-leading-icon.mdc-text-field--filled .mdc-floating-label,.mdc-text-field__affix--suffix,.mdc-text-field__icon--leading,.mdc-text-field__input[type=number]{direction:rtl}`:o.iv``]}]}}),l.P)},74237:(e,t,i)=>{i.a(e,(async(e,n)=>{try{i.r(t),i.d(t,{HuiLogbookCardEditor:()=>m});var d=i(17463),a=i(68144),l=i(79932),r=i(38768),o=i(47181),s=(i(35703),i(68331),i(57266)),c=i(98346),u=i(8436),h=e([u]);u=(h.then?(await h)():h)[0];const p=(0,r.f0)(c.I,(0,r.Ry)({entities:(0,r.jt)((0,r.IX)((0,r.Z_)())),title:(0,r.jt)((0,r.Z_)()),hours_to_show:(0,r.jt)((0,r.Rx)()),theme:(0,r.jt)((0,r.Z_)())})),f=[{name:"title",selector:{text:{}}},{name:"",type:"grid",schema:[{name:"theme",selector:{theme:{}}},{name:"hours_to_show",default:u.DEFAULT_HOURS_TO_SHOW,selector:{number:{mode:"box",min:1}}}]}];let m=(0,d.Z)([(0,l.Mo)("hui-logbook-card-editor")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,l.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,l.SB)()],key:"_config",value:void 0},{kind:"method",key:"setConfig",value:function(e){(0,r.hu)(e,p),this._config=e}},{kind:"get",key:"_entities",value:function(){return this._config.entities||[]}},{kind:"method",key:"render",value:function(){return this.hass&&this._config?a.dy` <ha-form .hass="${this.hass}" .data="${this._config}" .schema="${f}" .computeLabel="${this._computeLabelCallback}" @value-changed="${this._valueChanged}"></ha-form> <h3> ${`${this.hass.localize("ui.panel.lovelace.editor.card.generic.entities")} (${this.hass.localize("ui.panel.lovelace.editor.card.config.required")})`} </h3> <ha-entities-picker .hass="${this.hass}" .value="${this._entities}" .entityFilter="${s.MY}" @value-changed="${this._entitiesChanged}"> </ha-entities-picker> `:a.Ld}},{kind:"method",key:"_entitiesChanged",value:function(e){this._config={...this._config,entities:e.detail.value},(0,o.B)(this,"config-changed",{config:this._config})}},{kind:"method",key:"_valueChanged",value:function(e){(0,o.B)(this,"config-changed",{config:e.detail.value})}},{kind:"field",key:"_computeLabelCallback",value(){return e=>"theme"===e.name?`${this.hass.localize("ui.panel.lovelace.editor.card.generic.theme")} (${this.hass.localize("ui.panel.lovelace.editor.card.config.optional")})`:this.hass.localize(`ui.panel.lovelace.editor.card.generic.${e.name}`)}}]}}),a.oi);n()}catch(e){n(e)}}))},98346:(e,t,i)=>{i.d(t,{I:()=>d});var n=i(38768);const d=(0,n.Ry)({type:(0,n.Z_)(),view_layout:(0,n.Yj)()})}};
//# sourceMappingURL=13327.OrSXY9gF9FQ.js.map