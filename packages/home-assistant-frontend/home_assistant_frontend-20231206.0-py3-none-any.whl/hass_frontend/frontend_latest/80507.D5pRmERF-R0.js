export const id=80507;export const ids=[80507];export const modules={55642:(e,t,s)=>{s.d(t,{h:()=>a});var i=s(68144),o=s(57835);const a=(0,o.XM)(class extends o.Xe{constructor(e){if(super(e),this._element=void 0,e.type!==o.pX.CHILD)throw new Error("dynamicElementDirective can only be used in content bindings")}update(e,[t,s]){return this._element&&this._element.localName===t?(s&&Object.entries(s).forEach((([e,t])=>{this._element[e]=t})),i.Jb):this.render(t,s)}render(e,t){return this._element=document.createElement(e),t&&Object.entries(t).forEach((([e,t])=>{this._element[e]=t})),this._element}})},15136:(e,t,s)=>{s.r(t),s.d(t,{HuiClimatePresetModesCardFeatureEditor:()=>r});var i=s(17463),o=s(68144),a=s(79932),n=s(14516),l=s(47181);s(68331);let r=(0,i.Z)([(0,a.Mo)("hui-climate-preset-modes-card-feature-editor")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,a.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,a.Cb)({attribute:!1})],key:"context",value:void 0},{kind:"field",decorators:[(0,a.SB)()],key:"_config",value:void 0},{kind:"method",key:"setConfig",value:function(e){this._config=e}},{kind:"field",key:"_schema",value:()=>(0,n.Z)(((e,t,s)=>{var i;return[{name:"style",selector:{select:{multiple:!1,mode:"list",options:["dropdown","icons"].map((t=>({value:t,label:e(`ui.panel.lovelace.editor.features.types.climate-preset-modes.style_list.${t}`)})))}}},{name:"preset_modes",selector:{select:{multiple:!0,mode:"list",options:(null==s||null===(i=s.attributes.preset_modes)||void 0===i?void 0:i.map((e=>({value:e,label:t(s,"preset_mode",e)}))))||[]}}}]}))},{kind:"method",key:"render",value:function(){var e,t;if(!this.hass||!this._config)return o.Ld;const s=null!==(e=this.context)&&void 0!==e&&e.entity_id?this.hass.states[null===(t=this.context)||void 0===t?void 0:t.entity_id]:void 0,i={style:"dropdown",preset_modes:[],...this._config},a=this._schema(this.hass.localize,this.hass.formatEntityAttributeValue,s);return o.dy` <ha-form .hass="${this.hass}" .data="${i}" .schema="${a}" .computeLabel="${this._computeLabelCallback}" @value-changed="${this._valueChanged}"></ha-form> `}},{kind:"method",key:"_valueChanged",value:function(e){(0,l.B)(this,"config-changed",{config:e.detail.value})}},{kind:"field",key:"_computeLabelCallback",value(){return e=>{switch(e.name){case"style":case"preset_modes":return this.hass.localize(`ui.panel.lovelace.editor.features.types.climate-preset-modes.${e.name}`);default:return""}}}}]}}),o.oi)}};
//# sourceMappingURL=80507.D5pRmERF-R0.js.map