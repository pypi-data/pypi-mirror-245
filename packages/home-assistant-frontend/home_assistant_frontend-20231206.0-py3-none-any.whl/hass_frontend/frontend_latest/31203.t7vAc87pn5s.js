export const id=31203;export const ids=[31203];export const modules={91168:(t,e,i)=>{i.d(e,{Z:()=>a});const n=t=>t<10?`0${t}`:t;function a(t){const e=Math.floor(t/3600),i=Math.floor(t%3600/60),a=Math.floor(t%3600%60);return e>0?`${e}:${n(i)}:${n(a)}`:i>0?`${i}:${n(a)}`:a>0?""+a:null}},40958:(t,e,i)=>{i.d(e,{rv:()=>c,eF:()=>s,WH:()=>o,aT:()=>a,mK:()=>l,mZ:()=>r});var n=i(91168);const a=t=>t.callWS({type:"timer/list"}),s=(t,e)=>t.callWS({type:"timer/create",...e}),r=(t,e,i)=>t.callWS({type:"timer/update",timer_id:e,...i}),o=(t,e)=>t.callWS({type:"timer/delete",timer_id:e}),l=t=>{if(!t.attributes.remaining)return;let e=function(t){const e=t.split(":").map(Number);return 3600*e[0]+60*e[1]+e[2]}(t.attributes.remaining);if("active"===t.state){const i=(new Date).getTime(),n=new Date(t.last_changed).getTime();e=Math.max(e-(i-n)/1e3,0)}return e},c=(t,e,i)=>{if(!e)return null;if("idle"===e.state||0===i)return t.formatEntityState(e);let a=(0,n.Z)(i||0);return"paused"===e.state&&(a=`${a} (${t.formatEntityState(e)})`),a}},31203:(t,e,i)=>{i.a(t,(async(t,n)=>{try{i.r(e);var a=i(17463),s=i(34541),r=i(47838),o=i(68144),l=i(79932),c=i(40958),h=i(53658),d=i(91476),u=i(75502),v=t([d]);d=(v.then?(await v)():v)[0];(0,a.Z)([(0,l.Mo)("hui-timer-entity-row")],(function(t,e){class i extends e{constructor(...e){super(...e),t(this)}}return{F:i,d:[{kind:"field",decorators:[(0,l.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,l.SB)()],key:"_config",value:void 0},{kind:"field",decorators:[(0,l.SB)()],key:"_timeRemaining",value:void 0},{kind:"field",key:"_interval",value:void 0},{kind:"method",key:"setConfig",value:function(t){if(!t)throw new Error("Invalid configuration");if(this._config=t,!this.hass)return;const e=this.hass.states[this._config.entity];e?this._startInterval(e):this._clearInterval()}},{kind:"method",key:"disconnectedCallback",value:function(){(0,s.Z)((0,r.Z)(i.prototype),"disconnectedCallback",this).call(this),this._clearInterval()}},{kind:"method",key:"connectedCallback",value:function(){if((0,s.Z)((0,r.Z)(i.prototype),"connectedCallback",this).call(this),this._config&&this._config.entity){var t;const e=null===(t=this.hass)||void 0===t?void 0:t.states[this._config.entity];e&&this._startInterval(e)}}},{kind:"method",key:"render",value:function(){if(!this._config||!this.hass)return o.Ld;const t=this.hass.states[this._config.entity];return t?o.dy` <hui-generic-entity-row .hass="${this.hass}" .config="${this._config}"> <div class="text-content"> ${(0,c.rv)(this.hass,t,this._timeRemaining)} </div> </hui-generic-entity-row> `:o.dy` <hui-warning> ${(0,u.i)(this.hass,this._config.entity)} </hui-warning> `}},{kind:"method",key:"shouldUpdate",value:function(t){return!!t.has("_timeRemaining")||(0,h.G2)(this,t)}},{kind:"method",key:"updated",value:function(t){if((0,s.Z)((0,r.Z)(i.prototype),"updated",this).call(this,t),!this._config||!t.has("hass"))return;const e=this.hass.states[this._config.entity],n=t.get("hass");(n?n.states[this._config.entity]:void 0)!==e?this._startInterval(e):e||this._clearInterval()}},{kind:"method",key:"_clearInterval",value:function(){this._interval&&(window.clearInterval(this._interval),this._interval=void 0)}},{kind:"method",key:"_startInterval",value:function(t){this._clearInterval(),this._calculateRemaining(t),"active"===t.state&&(this._interval=window.setInterval((()=>this._calculateRemaining(t)),1e3))}},{kind:"method",key:"_calculateRemaining",value:function(t){this._timeRemaining=(0,c.mK)(t)}}]}}),o.oi);n()}catch(t){n(t)}}))}};
//# sourceMappingURL=31203.t7vAc87pn5s.js.map