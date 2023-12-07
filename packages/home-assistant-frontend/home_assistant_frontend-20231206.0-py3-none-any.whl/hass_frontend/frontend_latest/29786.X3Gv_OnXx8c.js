export const id=29786;export const ids=[29786];export const modules={55642:(e,t,a)=>{a.d(t,{h:()=>s});var i=a(68144),n=a(57835);const s=(0,n.XM)(class extends n.Xe{constructor(e){if(super(e),this._element=void 0,e.type!==n.pX.CHILD)throw new Error("dynamicElementDirective can only be used in content bindings")}update(e,[t,a]){return this._element&&this._element.localName===t?(a&&Object.entries(a).forEach((([e,t])=>{this._element[e]=t})),i.Jb):this.render(t,a)}render(e,t){return this._element=document.createElement(e),t&&Object.entries(t).forEach((([e,t])=>{this._element[e]=t})),this._element}})},5083:(e,t,a)=>{a.r(t),a.d(t,{HuiStatisticCardEditor:()=>f});var i=a(17463),n=a(68144),s=a(79932),o=a(14516),r=a(38768),c=a(47181),d=a(36639),l=(a(68331),a(38014)),h=a(61173),_=a(98346);const u=(0,r.f0)(_.I,(0,r.Ry)({entity:(0,r.jt)((0,r.Z_)()),name:(0,r.jt)((0,r.Z_)()),icon:(0,r.jt)((0,r.Z_)()),unit:(0,r.jt)((0,r.Z_)()),stat_type:(0,r.jt)((0,r.Z_)()),period:(0,r.jt)((0,r.Yj)()),theme:(0,r.jt)((0,r.Z_)()),footer:(0,r.jt)(h.ds)})),m=["mean","min","max","change"],y={mean:"mean",min:"min",max:"max",change:"sum"},p={today:{calendar:{period:"day"}},yesterday:{calendar:{period:"day",offset:-1}},this_week:{calendar:{period:"week"}},last_week:{calendar:{period:"week",offset:-1}},this_month:{calendar:{period:"month"}},last_month:{calendar:{period:"month",offset:-1}},this_year:{calendar:{period:"year"}},last_year:{calendar:{period:"year",offset:-1}}};let f=(0,i.Z)([(0,s.Mo)("hui-statistic-card-editor")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,s.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,s.SB)()],key:"_config",value:void 0},{kind:"field",decorators:[(0,s.SB)()],key:"_metadata",value:void 0},{kind:"method",key:"setConfig",value:function(e){(0,r.hu)(e,u),this._config=e,this._fetchMetadata()}},{kind:"method",key:"firstUpdated",value:function(){this._fetchMetadata().then((()=>{var e,t,a;null!==(e=this._config)&&void 0!==e&&e.stat_type||null===(t=this._config)||void 0===t||!t.entity||(0,c.B)(this,"config-changed",{config:{...this._config,stat_type:null!==(a=this._metadata)&&void 0!==a&&a.has_sum?"change":"mean"}})}))}},{kind:"field",key:"_data",value:()=>(0,o.Z)((e=>{if(!e||!e.period)return e;for(const[t,a]of Object.entries(p))if((0,d.v)(a,e.period))return{...e,period:t};return e}))},{kind:"field",key:"_schema",value:()=>(0,o.Z)(((e,t,a)=>[{name:"entity",required:!0,selector:{statistic:{}}},{name:"stat_type",required:!0,selector:{select:{multiple:!1,options:m.map((e=>({value:e,label:t(`ui.panel.lovelace.editor.card.statistic.stat_type_labels.${e}`),disabled:!a||!(0,l.Z0)(a,y[e])})))}}},{name:"period",required:!0,selector:e&&Object.keys(p).includes(e)?{select:{multiple:!1,options:Object.keys(p).map((e=>({value:e,label:t(`ui.panel.lovelace.editor.card.statistic.periods.${e}`)||e})))}}:{object:{}}},{type:"grid",name:"",schema:[{name:"name",selector:{text:{}}},{name:"icon",selector:{icon:{}},context:{icon_entity:"entity"}},{name:"unit",selector:{text:{}}},{name:"theme",selector:{theme:{}}}]}]))},{kind:"method",key:"render",value:function(){if(!this.hass||!this._config)return n.Ld;const e=this._data(this._config),t=this._schema("string"==typeof e.period?e.period:void 0,this.hass.localize,this._metadata);return n.dy` <ha-form .hass="${this.hass}" .data="${e}" .schema="${t}" .computeLabel="${this._computeLabelCallback}" @value-changed="${this._valueChanged}"></ha-form> `}},{kind:"method",key:"_fetchMetadata",value:async function(){this.hass&&this._config&&(this._metadata=(await(0,l.Py)(this.hass,[this._config.entity]))[0])}},{kind:"method",key:"_valueChanged",value:async function(e){var t;const a={...e.detail.value};if(Object.keys(a).forEach((e=>""===a[e]&&delete a[e])),"string"==typeof a.period){const e=p[a.period];e&&(a.period=e)}if(a.stat_type&&a.entity&&a.entity!==(null===(t=this._metadata)||void 0===t?void 0:t.statistic_id)){var i;const e=null===(i=await(0,l.Py)(this.hass,[a.entity]))||void 0===i?void 0:i[0];e&&!e.has_sum&&"change"===a.stat_type&&(a.stat_type="mean"),e&&!e.has_mean&&"change"!==a.stat_type&&(a.stat_type="change")}if(!a.stat_type&&a.entity){var n;const e=null===(n=await(0,l.Py)(this.hass,[a.entity]))||void 0===n?void 0:n[0];a.stat_type=null!=e&&e.has_sum?"change":"mean"}(0,c.B)(this,"config-changed",{config:a})}},{kind:"field",key:"_computeLabelCallback",value(){return e=>"period"===e.name?this.hass.localize("ui.panel.lovelace.editor.card.statistic.period"):"theme"===e.name?`${this.hass.localize("ui.panel.lovelace.editor.card.generic.theme")} (${this.hass.localize("ui.panel.lovelace.editor.card.config.optional")})`:this.hass.localize(`ui.panel.lovelace.editor.card.generic.${e.name}`)}}]}}),n.oi)},85677:(e,t,a)=>{a.d(t,{C:()=>_});var i=a(38768);const n=(0,i.Ry)({user:(0,i.Z_)()}),s=(0,i.G0)([(0,i.O7)(),(0,i.Ry)({text:(0,i.jt)((0,i.Z_)()),excemptions:(0,i.jt)((0,i.IX)(n))})]),o=(0,i.Ry)({action:(0,i.i0)("url"),url_path:(0,i.Z_)(),confirmation:(0,i.jt)(s)}),r=(0,i.Ry)({action:(0,i.i0)("call-service"),service:(0,i.Z_)(),service_data:(0,i.jt)((0,i.Ry)()),data:(0,i.jt)((0,i.Ry)()),target:(0,i.jt)((0,i.Ry)({entity_id:(0,i.jt)((0,i.G0)([(0,i.Z_)(),(0,i.IX)((0,i.Z_)())])),device_id:(0,i.jt)((0,i.G0)([(0,i.Z_)(),(0,i.IX)((0,i.Z_)())])),area_id:(0,i.jt)((0,i.G0)([(0,i.Z_)(),(0,i.IX)((0,i.Z_)())]))})),confirmation:(0,i.jt)(s)}),c=(0,i.Ry)({action:(0,i.i0)("navigate"),navigation_path:(0,i.Z_)(),navigation_replace:(0,i.jt)((0,i.O7)()),confirmation:(0,i.jt)(s)}),d=(0,i.dt)({action:(0,i.i0)("assist"),pipeline_id:(0,i.jt)((0,i.Z_)()),start_listening:(0,i.jt)((0,i.O7)())}),l=(0,i.dt)({action:(0,i.i0)("fire-dom-event")}),h=(0,i.Ry)({action:(0,i.kE)(["none","toggle","more-info","call-service","url","navigate","assist"]),confirmation:(0,i.jt)(s)}),_=(0,i.D8)((e=>{if(e&&"object"==typeof e&&"action"in e)switch(e.action){case"call-service":return r;case"fire-dom-event":return l;case"navigate":return c;case"url":return o;case"assist":return d}return h}))},98346:(e,t,a)=>{a.d(t,{I:()=>n});var i=a(38768);const n=(0,i.Ry)({type:(0,i.Z_)(),view_layout:(0,i.Yj)()})},53939:(e,t,a)=>{a.d(t,{k:()=>s});var i=a(38768),n=a(85677);const s=(0,i.Ry)({entity:(0,i.Z_)(),name:(0,i.jt)((0,i.Z_)()),icon:(0,i.jt)((0,i.Z_)()),image:(0,i.jt)((0,i.Z_)()),show_name:(0,i.jt)((0,i.O7)()),show_icon:(0,i.jt)((0,i.O7)()),tap_action:(0,i.jt)(n.C),hold_action:(0,i.jt)(n.C),double_tap_action:(0,i.jt)(n.C)})},61173:(e,t,a)=>{a.d(t,{ds:()=>d,gg:()=>c});var i=a(38768),n=a(85677),s=a(53939);const o=(0,i.Ry)({type:(0,i.Z_)(),image:(0,i.Z_)(),tap_action:(0,i.jt)(n.C),hold_action:(0,i.jt)(n.C),double_tap_action:(0,i.jt)(n.C),alt_text:(0,i.jt)((0,i.Z_)())}),r=(0,i.Ry)({type:(0,i.Z_)(),entities:(0,i.IX)(s.k)}),c=(0,i.Ry)({type:(0,i.Z_)(),entity:(0,i.Z_)(),detail:(0,i.jt)((0,i.Rx)()),hours_to_show:(0,i.jt)((0,i.Rx)())}),d=(0,i.D8)((e=>{if(e&&"object"==typeof e&&"type"in e)switch(e.type){case"buttons":return r;case"graph":return c;case"picture":return o}return(0,i.G0)([r,c,o])}))}};
//# sourceMappingURL=29786.X3Gv_OnXx8c.js.map