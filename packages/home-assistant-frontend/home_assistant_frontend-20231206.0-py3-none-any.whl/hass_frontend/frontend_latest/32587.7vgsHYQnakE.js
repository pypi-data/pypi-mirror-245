export const id=32587;export const ids=[32587];export const modules={32587:(e,t,i)=>{i.r(t),i.d(t,{HuiButtonsHeaderFooter:()=>c});var o=i(17463),r=i(68144),n=i(83448),s=i(79932),d=i(58831),a=i(90271);i(42109);let c=(0,o.Z)([(0,s.Mo)("hui-buttons-header-footer")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"method",static:!0,key:"getStubConfig",value:function(){return{entities:[]}}},{kind:"field",decorators:[(0,s.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,s.Cb)()],key:"type",value:void 0},{kind:"field",decorators:[(0,s.SB)()],key:"_configEntities",value:void 0},{kind:"method",key:"getCardSize",value:function(){return 3}},{kind:"method",key:"setConfig",value:function(e){this._configEntities=(0,a.A)(e.entities).map((e=>{const t={tap_action:{action:"toggle"},hold_action:{action:"more-info"},...e};return"scene"===(0,d.M)(e.entity)&&(t.tap_action={action:"call-service",service:"scene.turn_on",target:{entity_id:t.entity}}),t}))}},{kind:"method",key:"render",value:function(){return r.dy` ${"footer"===this.type?r.dy`<li class="divider footer" role="separator"></li>`:""} <hui-buttons-base .hass="${this.hass}" .configEntities="${this._configEntities}" class="${(0,n.$)({footer:"footer"===this.type,header:"header"===this.type})}"></hui-buttons-base> ${"header"===this.type?r.dy`<li class="divider header" role="separator"></li>`:""} `}},{kind:"field",static:!0,key:"styles",value:()=>r.iv`.divider{height:0;margin:16px 0;list-style-type:none;border:none;border-bottom-width:1px;border-bottom-style:solid;border-bottom-color:var(--divider-color)}.divider.header{margin-top:0}hui-buttons-base.footer{--padding-bottom:16px}hui-buttons-base.header{--padding-top:16px}`}]}}),r.oi)}};
//# sourceMappingURL=32587.7vgsHYQnakE.js.map