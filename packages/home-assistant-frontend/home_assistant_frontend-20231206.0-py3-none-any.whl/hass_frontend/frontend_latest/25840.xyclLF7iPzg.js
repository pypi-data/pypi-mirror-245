export const id=25840;export const ids=[25840];export const modules={54049:(t,e,a)=>{a.d(e,{$Q:()=>i,Hq:()=>n,py:()=>o});var s=a(66628);const n=!1,i=n?s.N:"A078F6B0",o="urn:x-cast:com.nabucasa.hast"},66628:(t,e,a)=>{a.d(e,{M:()=>n,N:()=>s});const s="5FE44367",n="http://192.168.1.234:8123"},91794:(t,e,a)=>{a.d(e,{Il:()=>o,Ni:()=>i,W_:()=>c});var s=a(54049),n=a(66628);const i=(t,e)=>t.sendMessage({type:"connect",refreshToken:e.data.refresh_token,clientId:e.data.clientId,hassUrl:s.Hq?n.M:e.data.hassUrl}),o=(t,e,a,i)=>t.sendMessage({type:"show_lovelace_view",viewPath:a,urlPath:i||null,hassUrl:s.Hq?n.M:e}),c=(t,e)=>{if(!t.castConnectedToOurHass)return new Promise((a=>{const s=t.addEventListener("connection-changed",(()=>{t.castConnectedToOurHass&&(s(),a())}));i(t,e)}))}},25840:(t,e,a)=>{a.r(e);var s=a(17463),n=a(34541),i=a(47838),o=(a(14271),a(68144)),c=a(79932),d=a(83448),r=a(91794);a(81312);(0,s.Z)([(0,c.Mo)("hui-cast-row")],(function(t,e){class s extends e{constructor(...e){super(...e),t(this)}}return{F:s,d:[{kind:"field",decorators:[(0,c.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,c.SB)()],key:"_config",value:void 0},{kind:"field",decorators:[(0,c.SB)()],key:"_castManager",value:void 0},{kind:"field",decorators:[(0,c.SB)()],key:"_noHTTPS",value:()=>!1},{kind:"method",key:"setConfig",value:function(t){this._config={icon:"mdi:television",name:"Home Assistant Cast",view:0,...t}}},{kind:"method",key:"shouldUpdate",value:function(t){return!(1===t.size&&t.has("hass"))}},{kind:"method",key:"render",value:function(){if(!this._config)return o.Ld;const t=this._castManager&&this._castManager.status&&this._config.view===this._castManager.status.lovelacePath&&this._config.dashboard===this._castManager.status.urlPath;return o.dy` <ha-icon .icon="${this._config.icon}"></ha-icon> <div class="flex"> <div class="name">${this._config.name}</div> ${this._noHTTPS?o.dy` Cast requires HTTPS `:void 0===this._castManager?o.Ld:null===this._castManager?o.dy` Cast API unavailable `:"NO_DEVICES_AVAILABLE"===this._castManager.castState?o.dy` No devices found `:o.dy` <div class="controls"> <google-cast-launcher></google-cast-launcher> <mwc-button @click="${this._sendLovelace}" class="${(0,d.$)({inactive:!t})}" .unelevated="${t}" .disabled="${!this._castManager.status}"> SHOW </mwc-button> </div> `} </div> `}},{kind:"method",key:"firstUpdated",value:function(t){(0,n.Z)((0,i.Z)(s.prototype),"firstUpdated",this).call(this,t),"http:"===location.protocol&&"localhost"!==location.hostname&&(this._noHTTPS=!0),a.e(80363).then(a.bind(a,80363)).then((({getCastManager:t})=>t(this.hass.auth).then((t=>{this._castManager=t,t.addEventListener("connection-changed",(()=>{this.requestUpdate()})),t.addEventListener("state-changed",(()=>{this.requestUpdate()}))}),(()=>{this._castManager=null}))))}},{kind:"method",key:"updated",value:function(t){(0,n.Z)((0,i.Z)(s.prototype),"updated",this).call(this,t),this._config&&this._config.hide_if_unavailable&&(this.style.display=this._castManager&&"NO_DEVICES_AVAILABLE"!==this._castManager.castState?"":"none")}},{kind:"method",key:"_sendLovelace",value:async function(){await(0,r.W_)(this._castManager,this.hass.auth),(0,r.Il)(this._castManager,this.hass.auth.data.hassUrl,this._config.view,this._config.dashboard)}},{kind:"get",static:!0,key:"styles",value:function(){return o.iv`:host{display:flex;align-items:center}ha-icon{padding:8px;color:var(--paper-item-icon-color)}.flex{flex:1;margin-left:16px;display:flex;justify-content:space-between;align-items:center}.name{white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.controls{display:flex;align-items:center}google-cast-launcher{margin-right:.57em;cursor:pointer;display:inline-block;height:24px;width:24px}.inactive{padding:0 4px}`}}]}}),o.oi)}};
//# sourceMappingURL=25840.xyclLF7iPzg.js.map