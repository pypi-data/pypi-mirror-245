export const id=43973;export const ids=[43973];export const modules={43973:(e,t,s)=>{s.r(t),s.d(t,{ExternalAuth:()=>r,createExternalAuth:()=>d});var n=s(10280);class a{constructor(){this.config=void 0,this.commands={},this.msgId=0,this._commandHandler=void 0}async attach(){window.externalBus=e=>this.receiveMessage(e),window.addEventListener("connection-status",(e=>this.fireMessage({type:"connection-status",payload:{event:e.detail}}))),this.config=await this.sendMessage({type:"config/get"})}addCommandHandler(e){this._commandHandler=e}sendMessage(e){const t=++this.msgId;return e.id=t,this._sendExternal(e),new Promise(((e,s)=>{this.commands[t]={resolve:e,reject:s}}))}fireMessage(e){e.id||(e.id=++this.msgId),this._sendExternal(e)}receiveMessage(e){if("command"===e.type){if(!this._commandHandler||!this._commandHandler(e)){let t,s;this._commandHandler?(t="not_ready",s="Command handler not ready"):(t="unknown_command",s=`Unknown command ${e.command}`),console.warn(s,e),this.fireMessage({id:e.id,type:"result",success:!1,error:{code:t,message:s}})}return}const t=this.commands[e.id];t?"result"===e.type&&(e.success?t.resolve(e.result):t.reject(e.error)):console.warn("Received unknown msg ID",e.id)}_sendExternal(e){window.externalApp?window.externalApp.externalBus(JSON.stringify(e)):window.webkit.messageHandlers.externalBus.postMessage(e)}}const i="externalAuthSetToken",o="externalAuthRevokeToken";if(!window.externalApp&&!window.webkit)throw new Error("External auth requires either externalApp or webkit defined on Window object.");class r extends n.gx{constructor(e){super({hassUrl:e,clientId:"",refresh_token:"",access_token:"",expires_in:0,expires:0}),this.external=void 0,this._tokenCallbackPromise=void 0}async refreshAccessToken(e){if(this._tokenCallbackPromise&&!e)try{return void await this._tokenCallbackPromise}catch(e){this._tokenCallbackPromise=void 0}const t={callback:i};e&&(t.force=!0),this._tokenCallbackPromise=new Promise(((e,t)=>{window[i]=(s,n)=>s?e(n):t(n)})),await Promise.resolve(),window.externalApp?window.externalApp.getExternalAuth(JSON.stringify(t)):window.webkit.messageHandlers.getExternalAuth.postMessage(t);const s=await this._tokenCallbackPromise;this.data.access_token=s.access_token,this.data.expires=1e3*s.expires_in+Date.now(),this._tokenCallbackPromise=void 0}async revoke(){const e={callback:o},t=new Promise(((e,t)=>{window[o]=(s,n)=>s?e(n):t(n)}));await Promise.resolve(),window.externalApp?window.externalApp.revokeExternalAuth(JSON.stringify(e)):window.webkit.messageHandlers.revokeExternalAuth.postMessage(e),await t}}const d=async e=>{var t;const s=new r(e);return(null!==(t=window.externalApp)&&void 0!==t&&t.externalBus||window.webkit&&window.webkit.messageHandlers.externalBus)&&(s.external=new a,await s.external.attach()),s}}};
//# sourceMappingURL=43973.rq_WxXnxi8g.js.map