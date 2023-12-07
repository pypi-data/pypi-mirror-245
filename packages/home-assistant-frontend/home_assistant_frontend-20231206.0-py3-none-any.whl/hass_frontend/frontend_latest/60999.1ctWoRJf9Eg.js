export const id=60999;export const ids=[60999];export const modules={60999:(e,i,t)=>{t.r(i),t.d(i,{SideBarView:()=>v});var d=t(17463),o=t(34541),a=t(47838),n=t(68144),l=t(79932),s=t(83448),r=t(47181),c=t(87744),h=t(54324);let v=(0,d.Z)(null,(function(e,i){class d extends i{constructor(...i){super(...i),e(this)}}return{F:d,d:[{kind:"field",decorators:[(0,l.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,l.Cb)({attribute:!1})],key:"lovelace",value:void 0},{kind:"field",decorators:[(0,l.Cb)({type:Number})],key:"index",value:void 0},{kind:"field",decorators:[(0,l.Cb)({type:Boolean})],key:"isStrategy",value:()=>!1},{kind:"field",decorators:[(0,l.Cb)({attribute:!1})],key:"cards",value:()=>[]},{kind:"field",decorators:[(0,l.SB)()],key:"_config",value:void 0},{kind:"field",key:"_mqlListenerRef",value:void 0},{kind:"field",key:"_mql",value:void 0},{kind:"method",key:"connectedCallback",value:function(){(0,o.Z)((0,a.Z)(d.prototype),"connectedCallback",this).call(this),this._mql=window.matchMedia("(min-width: 760px)"),this._mqlListenerRef=this._createCards.bind(this),this._mql.addListener(this._mqlListenerRef)}},{kind:"method",key:"disconnectedCallback",value:function(){var e;(0,o.Z)((0,a.Z)(d.prototype),"disconnectedCallback",this).call(this),null===(e=this._mql)||void 0===e||e.removeListener(this._mqlListenerRef),this._mqlListenerRef=void 0,this._mql=void 0}},{kind:"method",key:"setConfig",value:function(e){this._config=e}},{kind:"method",key:"willUpdate",value:function(e){var i,n,l;if((0,o.Z)((0,a.Z)(d.prototype),"willUpdate",this).call(this,e),null!==(i=this.lovelace)&&void 0!==i&&i.editMode&&t.e(49826).then(t.bind(t,49826)),e.has("cards")&&this._createCards(),!e.has("lovelace")&&!e.has("_config"))return;const s=e.get("lovelace");(!e.has("cards")&&(null==s?void 0:s.config)!==(null===(n=this.lovelace)||void 0===n?void 0:n.config)||s&&(null==s?void 0:s.editMode)!==(null===(l=this.lovelace)||void 0===l?void 0:l.editMode))&&this._createCards()}},{kind:"method",key:"render",value:function(){var e,i;return n.dy` <div class="container ${null!==(e=this.lovelace)&&void 0!==e&&e.editMode?"edit-mode":""}"></div> ${null!==(i=this.lovelace)&&void 0!==i&&i.editMode?n.dy` <ha-fab .label="${this.hass.localize("ui.panel.lovelace.editor.edit_card.add")}" extended @click="${this._addCard}" class="${(0,s.$)({rtl:(0,c.HE)(this.hass)})}"> <ha-svg-icon slot="icon" .path="${"M19,13H13V19H11V13H5V11H11V5H13V11H19V13Z"}"></ha-svg-icon> </ha-fab> `:""} `}},{kind:"method",key:"_addCard",value:function(){(0,r.B)(this,"ll-create-card")}},{kind:"method",key:"_createCards",value:function(){var e;const i=document.createElement("div");let t;if(i.id="main",null!==(e=this._mql)&&void 0!==e&&e.matches?(t=document.createElement("div"),t.id="sidebar"):t=i,this.hasUpdated){const e=this.renderRoot.querySelector("#main"),d=this.renderRoot.querySelector("#sidebar"),o=this.renderRoot.querySelector(".container");e&&o.removeChild(e),d&&o.removeChild(d),o.appendChild(i),o.appendChild(t)}else this.updateComplete.then((()=>{const e=this.renderRoot.querySelector(".container");e.appendChild(i),e.appendChild(t)}));this.cards.forEach(((e,d)=>{var o,a,n;const l=null===(o=this._config)||void 0===o||null===(o=o.cards)||void 0===o?void 0:o[d];let s;if(this.isStrategy||null===(a=this.lovelace)||void 0===a||!a.editMode)e.editMode=!1,s=e;else{var r;s=document.createElement("hui-card-options"),s.hass=this.hass,s.lovelace=this.lovelace,s.path=[this.index,d],e.editMode=!0;const i=document.createElement("ha-icon-button");i.slot="buttons";const t=document.createElement("ha-svg-icon");t.path="sidebar"!==(null==l||null===(r=l.view_layout)||void 0===r?void 0:r.position)?"M4,11V13H16L10.5,18.5L11.92,19.92L19.84,12L11.92,4.08L10.5,5.5L16,11H4Z":"M20,11V13H8L13.5,18.5L12.08,19.92L4.16,12L12.08,4.08L13.5,5.5L8,11H20Z",i.appendChild(t),i.addEventListener("click",(()=>{var e;this.lovelace.saveConfig((0,h.LG)(this.lovelace.config,[this.index,d],{...l,view_layout:{position:"sidebar"!==(null==l||null===(e=l.view_layout)||void 0===e?void 0:e.position)?"sidebar":"main"}}))})),s.appendChild(i),s.appendChild(e)}"sidebar"!==(null==l||null===(n=l.view_layout)||void 0===n?void 0:n.position)?i.appendChild(s):t.appendChild(s)}))}},{kind:"get",static:!0,key:"styles",value:function(){return n.iv`:host{display:block;padding-top:4px}.container{display:flex;justify-content:center;margin-left:4px;margin-right:4px}.container.edit-mode{margin-bottom:72px}#main{max-width:1620px;flex-grow:2}#sidebar{flex-grow:1;flex-shrink:0;max-width:380px}.container>div{min-width:0;box-sizing:border-box}.container>div>:not([hidden]){display:block;margin:var(--masonry-view-card-margin,4px 4px 8px)}@media (max-width:500px){.container>div>*{margin-left:0;margin-right:0}}ha-fab{position:fixed;right:calc(16px + env(safe-area-inset-right));bottom:calc(16px + env(safe-area-inset-bottom));z-index:1}ha-fab.rtl{right:auto;left:calc(16px + env(safe-area-inset-left))}`}}]}}),n.oi);customElements.define("hui-sidebar-view",v)}};
//# sourceMappingURL=60999.1ctWoRJf9Eg.js.map