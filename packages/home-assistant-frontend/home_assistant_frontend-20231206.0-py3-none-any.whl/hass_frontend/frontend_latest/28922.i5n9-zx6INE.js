/*! For license information please see 28922.i5n9-zx6INE.js.LICENSE.txt */
export const id=28922;export const ids=[28922,31206];export const modules={31206:(t,e,r)=>{r.r(e),r.d(e,{HaCircularProgress:()=>l});var i=r(17463),o=r(34541),s=r(47838),a=(r(34131),r(22129)),n=r(68144),c=r(79932);let l=(0,i.Z)([(0,c.Mo)("ha-circular-progress")],(function(t,e){class r extends e{constructor(...e){super(...e),t(this)}}return{F:r,d:[{kind:"field",decorators:[(0,c.Cb)({attribute:"aria-label",type:String})],key:"ariaLabel",value:()=>"Loading"},{kind:"field",decorators:[(0,c.Cb)()],key:"size",value:()=>"medium"},{kind:"method",key:"updated",value:function(t){if((0,o.Z)((0,s.Z)(r.prototype),"updated",this).call(this,t),t.has("size"))switch(this.size){case"tiny":this.style.setProperty("--md-circular-progress-size","16px");break;case"small":this.style.setProperty("--md-circular-progress-size","28px");break;case"medium":this.style.setProperty("--md-circular-progress-size","48px");break;case"large":this.style.setProperty("--md-circular-progress-size","68px")}}},{kind:"get",static:!0,key:"styles",value:function(){return[...(0,o.Z)((0,s.Z)(r),"styles",this),n.iv`:host{--md-sys-color-primary:var(--primary-color);--md-circular-progress-size:48px}`]}}]}}),a.B)},66335:(t,e,r)=>{r.d(e,{H:()=>i});const i=5},58763:(t,e,r)=>{r.a(t,(async(t,i)=>{try{r.d(e,{Nu:()=>x,Vk:()=>h,xS:()=>f,xj:()=>C});var o=r(58831),s=r(29171),a=r(91741),n=t([s]);s=(n.then?(await n)():n)[0];const c=["climate","humidifier","water_heater"],l=["climate","humidifier","input_datetime","thermostat","water_heater","person","device_tracker"],d=["temperature","current_temperature","target_temp_low","target_temp_high","hvac_action","humidity","mode","action","current_humidity"],u=(t,e)=>!t.states[e]||l.includes((0,o.M)(e)),h=(t,e,r,i,o)=>{const s={type:"history/stream",entity_ids:o,start_time:r.toISOString(),end_time:i.toISOString(),minimal_response:!0,no_attributes:!o.some((e=>u(t,e)))},a=new v(t);return t.connection.subscribeMessage((t=>e(a.processMessage(t))),s)};class v{constructor(t,e){this.hass=void 0,this.hoursToShow=void 0,this.combinedHistory=void 0,this.hass=t,this.hoursToShow=e,this.combinedHistory={}}processMessage(t){if(!this.combinedHistory||!Object.keys(this.combinedHistory).length)return this.combinedHistory=t.states,this.combinedHistory;if(!Object.keys(t.states).length)return this.combinedHistory;const e=this.hoursToShow?((new Date).getTime()-3600*this.hoursToShow*1e3)/1e3:void 0,r={};for(const t of Object.keys(this.combinedHistory))r[t]=[];for(const e of Object.keys(t.states))r[e]=[];for(const i of Object.keys(r)){if(i in this.combinedHistory&&i in t.states){const e=this.combinedHistory[i],o=e[e.length-1];r[i]=e.concat(t.states[i]),t.states[i][0].lu<o.lu&&(r[i]=r[i].sort(((t,e)=>t.lu-e.lu)))}else i in this.combinedHistory?r[i]=this.combinedHistory[i]:r[i]=t.states[i];if(e&&i in this.combinedHistory){const t=r[i].filter((t=>t.lu<e));if(!t.length)continue;if(r[i]=r[i].filter((t=>t.lu>=e)),r[i].length&&r[i][0].lu===e)continue;const o=t[t.length-1];o.lu=e,r[i].unshift(o)}}return this.combinedHistory=r,this.combinedHistory}}const f=(t,e,r,i,o=!0,s=!0,a)=>{const n={type:"history/stream",entity_ids:i,start_time:new Date((new Date).getTime()-3600*r*1e3).toISOString(),minimal_response:o,significant_changes_only:s,no_attributes:null!=a?a:!i.some((e=>u(t,e)))},c=new v(t,r);return t.connection.subscribeMessage((t=>e(c.processMessage(t))),n)},m=(t,e)=>t.state===e.state&&(!t.attributes||!e.attributes||d.every((r=>t.attributes[r]===e.attributes[r]))),_=(t,e,r,i,o,n,c)=>{const l=[],d=n[0];for(const a of n){if(l.length>0&&a.s===l[l.length-1].state)continue;const n={};null!=c&&c.attributes.device_class&&(n.device_class=null==c?void 0:c.attributes.device_class),l.push({state_localize:(0,s.c)(t,e,r,i[o],o,{...a.a||d.a,...n},a.s),state:a.s,last_changed:1e3*(a.lc?a.lc:a.lu)})}return{name:(0,a.a)(o,(null==c?void 0:c.attributes)||d.a),entity_id:o,data:l}},g=(t,e,r,i)=>{const s=[];return Object.keys(r).forEach((t=>{const e=r[t],n=e[0],l=(0,o.M)(t),u=[];for(const t of e){let e;if(c.includes(l)){e={state:t.s,last_changed:1e3*t.lu,attributes:{}};for(const r of d)r in t.a&&(e.attributes[r]=t.a[r])}else e={state:t.s,last_changed:1e3*(t.lc?t.lc:t.lu),attributes:{}};u.length>1&&m(e,u[u.length-1])&&m(e,u[u.length-2])||u.push(e)}const h=t in i?i[t].attributes:"friendly_name"in n.a?n.a:void 0;s.push({domain:l,name:(0,a.a)(t,h||{}),entity_id:t,states:u})})),{unit:t,device_class:e,identifier:Object.keys(r).join(""),data:s}},b=["counter","input_number","number"],p=t=>b.includes(t),y=t=>"unit_of_measurement"in t||"state_class"in t,k=(t,e)=>null!=t.attributes.device_class&&e.includes(t.attributes.device_class),w=" ",x=(t,e,r,i,s=!1)=>{const a={},n=[];if(!e)return{line:[],timeline:[]};Object.keys(e).forEach((c=>{var l;const d=e[c];if(0===d.length)return;const u=(0,o.M)(c),h=c in t.states?t.states[c]:void 0,v=h||p(u)?void 0:d.find((t=>t.a&&y(t.a)));let f;f=p(u)||null!=h&&y(h.attributes)||null!=h&&"sensor"===u&&k(h,i)||null!=v?(null==h?void 0:h.attributes.unit_of_measurement)||(null==v?void 0:v.a.unit_of_measurement)||w:{zone:r("ui.dialogs.more_info_control.zone.graph_unit"),climate:t.config.unit_system.temperature,humidifier:"%",water_heater:t.config.unit_system.temperature}[u];const m=null===(l=(null==h?void 0:h.attributes)||(null==v?void 0:v.a))||void 0===l?void 0:l.device_class,g=C(f,m,s);f?g&&g in a&&c in a[g]?a[g][c].push(...d):g&&(g in a||(a[g]={}),a[g][c]=d):n.push(_(r,t.locale,t.config,t.entities,c,d,h))}));return{line:Object.keys(a).map((e=>{const r=e.split("_"),i=r[0],o=r[1]||void 0;return g(i,o,a[e],t.states)})),timeline:n}},C=(t,e,r)=>r?`${t}_${e||""}`:t;i()}catch(t){i(t)}}))},4309:(t,e,r)=>{r.d(e,{g:()=>n});var i=r(66335);const o=t=>t.reduce(((t,e)=>t+parseFloat(e.state)),0)/t.length,s=t=>parseFloat(t[t.length-1].state)||0,a=(t,e,r,a,n)=>{t.forEach((t=>{t.state=Number(t.state)})),t=t.filter((t=>!Number.isNaN(t.state)));const c=void 0!==(null==n?void 0:n.min)?n.min:Math.min(...t.map((t=>t.state))),l=void 0!==(null==n?void 0:n.max)?n.max:Math.max(...t.map((t=>t.state))),d=(new Date).getTime(),u=(t,r,i)=>{const o=d-new Date(r.last_changed).getTime();let s=Math.abs(o/36e5-e);return i?(s=60*(s-Math.floor(s)),s=Number((10*Math.round(s/10)).toString()[0])):s=Math.floor(s),t[s]||(t[s]=[]),t[s].push(r),t};if(t=t.reduce(((t,e)=>u(t,e,!1)),[]),a>1&&(t=t.map((t=>t.reduce(((t,e)=>u(t,e,!0)),[])))),t.length)return((t,e,r,a,n,c)=>{const l=[];let d=(c-n)/80;d=0!==d?d:80;let u=r/(e-(1===a?1:0));u=isFinite(u)?u:r;const h=t.filter(Boolean)[0];let v=[o(h),s(h)];const f=(t,e,r=0,a=1)=>{if(a>1&&t)return t.forEach(((t,r)=>f(t,e,r,a-1)));const c=u*(e+r/6);t&&(v=[o(t),s(t)]);const h=80+i.H/2-((t?v[0]:v[1])-n)/d;return l.push([c,h])};for(let e=0;e<t.length;e+=1)f(t[e],e,0,a);return 1===l.length&&(l[1]=[r,l[0][1]]),l.push([r,l[l.length-1][1]]),l})(t,e,r,a,c,l)},n=(t,e,r,i,o)=>{if(!t)return;const s=t.map((t=>({state:Number(t.s),last_changed:1e3*t.lu})));return a(s,e,r,i,o)}},63629:(t,e,r)=>{var i=r(17463),o=r(68144),s=r(79932),a=r(66335);(0,i.Z)([(0,s.Mo)("hui-graph-base")],(function(t,e){return{F:class extends e{constructor(...e){super(...e),t(this)}},d:[{kind:"field",decorators:[(0,s.Cb)()],key:"coordinates",value:void 0},{kind:"field",decorators:[(0,s.SB)()],key:"_path",value:void 0},{kind:"method",key:"render",value:function(){return o.dy` ${this._path?o.YP`<svg width="100%" height="100%" viewBox="0 0 500 100"> <g> <mask id="fill"> <path class="fill" fill="white" d="${this._path} L 500, 100 L 0, 100 z"/> </mask> <rect height="100%" width="100%" id="fill-rect" fill="var(--accent-color)" mask="url(#fill)"></rect> <mask id="line"> <path fill="none" stroke="var(--accent-color)" stroke-width="${a.H}" stroke-linecap="round" stroke-linejoin="round" d="${this._path}"></path> </mask> <rect height="100%" width="100%" id="rect" fill="var(--accent-color)" mask="url(#line)"></rect> </g> </svg>`:o.YP`<svg width="100%" height="100%" viewBox="0 0 500 100"></svg>`} `}},{kind:"method",key:"willUpdate",value:function(t){this.coordinates&&t.has("coordinates")&&(this._path=(t=>{if(!t.length)return"";let e,r,i="",o=t.filter(Boolean)[0];i+=`M ${o[0]},${o[1]}`;for(const l of t)e=l,s=o[0],a=o[1],n=e[0],c=e[1],r=[(s-n)/2+n,(a-c)/2+c],i+=` ${r[0]},${r[1]}`,i+=` Q${e[0]},${e[1]}`,o=e;var s,a,n,c;return i+=` ${e[0]},${e[1]}`,i})(this.coordinates))}},{kind:"get",static:!0,key:"styles",value:function(){return o.iv`:host{display:flex;width:100%}.fill{opacity:.1}`}}]}}),o.oi)},28922:(t,e,r)=>{r.a(t,(async(t,i)=>{try{r.r(e),r.d(e,{HuiGraphHeaderFooter:()=>b});var o=r(17463),s=r(34541),a=r(47838),n=r(68144),c=r(79932),l=r(7323),d=r(58831),u=(r(31206),r(58763)),h=r(15688),v=r(4309),f=(r(63629),t([u]));u=(f.then?(await f)():f)[0];const m=6e4,_=60*m,g=["counter","input_number","number","sensor"];let b=(0,o.Z)([(0,c.Mo)("hui-graph-header-footer")],(function(t,e){class i extends e{constructor(...e){super(...e),t(this)}}return{F:i,d:[{kind:"method",static:!0,key:"getConfigElement",value:async function(){return await Promise.all([r.e(42850),r.e(78133),r.e(50731),r.e(40163),r.e(74535),r.e(60040)]).then(r.bind(r,87071)),document.createElement("hui-graph-footer-editor")}},{kind:"method",static:!0,key:"getStubConfig",value:function(t,e,r){return{type:"graph",entity:(0,h.j)(t,1,e,r,g,(t=>!isNaN(Number(t.state))&&!!t.attributes.unit_of_measurement))[0]||""}}},{kind:"field",decorators:[(0,c.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,c.Cb)()],key:"type",value:void 0},{kind:"field",decorators:[(0,c.Cb)()],key:"_config",value:void 0},{kind:"field",decorators:[(0,c.SB)()],key:"_coordinates",value:void 0},{kind:"field",key:"_error",value:void 0},{kind:"field",key:"_interval",value:void 0},{kind:"field",key:"_subscribed",value:void 0},{kind:"method",key:"getCardSize",value:function(){return 3}},{kind:"method",key:"setConfig",value:function(t){if(null==t||!t.entity||!g.includes((0,d.M)(t.entity)))throw new Error("Specify an entity from within the sensor domain");const e={detail:1,hours_to_show:24,...t};e.hours_to_show=Number(e.hours_to_show),e.detail=1===e.detail||2===e.detail?e.detail:1,this._config=e}},{kind:"method",key:"render",value:function(){return this._config&&this.hass?this._error?n.dy`<div class="errors">${this._error}</div>`:this._coordinates?this._coordinates.length?n.dy` <hui-graph-base .coordinates="${this._coordinates}"></hui-graph-base> `:n.dy` <div class="container"> <div class="info">No state history found.</div> </div> `:n.dy` <div class="container"> <ha-circular-progress indeterminate size="small"></ha-circular-progress> </div> `:n.Ld}},{kind:"method",key:"connectedCallback",value:function(){(0,s.Z)((0,a.Z)(i.prototype),"connectedCallback",this).call(this),this.hasUpdated&&this._config&&this._subscribeHistory()}},{kind:"method",key:"disconnectedCallback",value:function(){(0,s.Z)((0,a.Z)(i.prototype),"disconnectedCallback",this).call(this),this._unsubscribeHistory()}},{kind:"method",key:"_subscribeHistory",value:function(){(0,l.p)(this.hass,"history")&&!this._subscribed&&this._config&&(this._subscribed=(0,u.xS)(this.hass,(t=>{this._subscribed&&this._config&&(this._coordinates=(0,v.g)(t[this._config.entity],this._config.hours_to_show,500,this._config.detail,this._config.limits)||[])}),this._config.hours_to_show,[this._config.entity]).catch((t=>{this._subscribed=void 0,this._error=t})),this._setRedrawTimer())}},{kind:"method",key:"_redrawGraph",value:function(){this._coordinates&&(this._coordinates=[...this._coordinates])}},{kind:"method",key:"_setRedrawTimer",value:function(){clearInterval(this._interval),this._interval=window.setInterval((()=>this._redrawGraph()),this._config.hours_to_show>24?_:m)}},{kind:"method",key:"_unsubscribeHistory",value:function(){clearInterval(this._interval),this._subscribed&&(this._subscribed.then((t=>null==t?void 0:t())),this._subscribed=void 0)}},{kind:"method",key:"updated",value:function(t){if(!this._config||!this.hass||!t.has("_config"))return;const e=t.get("_config");e&&this._subscribed&&e.entity===this._config.entity||(this._unsubscribeHistory(),this._subscribeHistory())}},{kind:"get",static:!0,key:"styles",value:function(){return n.iv`ha-circular-progress{position:absolute;top:calc(50% - 14px)}.container{display:flex;justify-content:center;position:relative;padding-bottom:20%}.info{position:absolute;top:calc(50% - 16px);color:var(--secondary-text-color)}`}}]}}),n.oi);i()}catch(t){i(t)}}))},22129:(t,e,r)=>{r.d(e,{B:()=>u});var i=r(43204),o=r(79932),s=r(68144),a=r(83448),n=r(92204);class c extends s.oi{constructor(){super(...arguments),this.value=0,this.max=1,this.indeterminate=!1,this.fourColor=!1}render(){const{ariaLabel:t}=this;return s.dy` <div class="progress ${(0,a.$)(this.getRenderClasses())}" role="progressbar" aria-label="${t||s.Ld}" aria-valuemin="0" aria-valuemax="${this.max}" aria-valuenow="${this.indeterminate?s.Ld:this.value}">${this.renderIndicator()}</div> `}getRenderClasses(){return{indeterminate:this.indeterminate,"four-color":this.fourColor}}}(0,n.d)(c),(0,i.__decorate)([(0,o.Cb)({type:Number})],c.prototype,"value",void 0),(0,i.__decorate)([(0,o.Cb)({type:Number})],c.prototype,"max",void 0),(0,i.__decorate)([(0,o.Cb)({type:Boolean})],c.prototype,"indeterminate",void 0),(0,i.__decorate)([(0,o.Cb)({type:Boolean,attribute:"four-color"})],c.prototype,"fourColor",void 0);class l extends c{renderIndicator(){return this.indeterminate?this.renderIndeterminateContainer():this.renderDeterminateContainer()}renderDeterminateContainer(){const t=100*(1-this.value/this.max);return s.dy` <svg viewBox="0 0 4800 4800"> <circle class="track" pathLength="100"></circle> <circle class="active-track" pathLength="100" stroke-dashoffset="${t}"></circle> </svg> `}renderIndeterminateContainer(){return s.dy` <div class="spinner"> <div class="left"> <div class="circle"></div> </div> <div class="right"> <div class="circle"></div> </div> </div>`}}const d=s.iv`:host{--_active-indicator-color:var(--md-circular-progress-active-indicator-color, var(--md-sys-color-primary, #6750a4));--_active-indicator-width:var(--md-circular-progress-active-indicator-width, 10);--_four-color-active-indicator-four-color:var(--md-circular-progress-four-color-active-indicator-four-color, var(--md-sys-color-tertiary-container, #ffd8e4));--_four-color-active-indicator-one-color:var(--md-circular-progress-four-color-active-indicator-one-color, var(--md-sys-color-primary, #6750a4));--_four-color-active-indicator-three-color:var(--md-circular-progress-four-color-active-indicator-three-color, var(--md-sys-color-tertiary, #7d5260));--_four-color-active-indicator-two-color:var(--md-circular-progress-four-color-active-indicator-two-color, var(--md-sys-color-primary-container, #eaddff));--_size:var(--md-circular-progress-size, 48px);display:inline-flex;vertical-align:middle;min-block-size:var(--_size);min-inline-size:var(--_size);position:relative;align-items:center;justify-content:center;contain:strict;content-visibility:auto}.progress{flex:1;align-self:stretch;margin:4px}.active-track,.circle,.left,.progress,.right,.spinner,.track,svg{position:absolute;inset:0}svg{transform:rotate(-90deg)}circle{cx:50%;cy:50%;r:calc(50%*(1 - var(--_active-indicator-width)/ 100));stroke-width:calc(var(--_active-indicator-width)*1%);stroke-dasharray:100;fill:rgba(0,0,0,0)}.active-track{transition:stroke-dashoffset .5s cubic-bezier(0, 0, .2, 1);stroke:var(--_active-indicator-color)}.track{stroke:rgba(0,0,0,0)}.progress.indeterminate{animation:linear infinite linear-rotate;animation-duration:1.568s}.spinner{animation:infinite both rotate-arc;animation-duration:5332ms;animation-timing-function:cubic-bezier(0.4,0,0.2,1)}.left{overflow:hidden;inset:0 50% 0 0}.right{overflow:hidden;inset:0 0 0 50%}.circle{box-sizing:border-box;border-radius:50%;border:solid calc(var(--_active-indicator-width)/ 100*(var(--_size) - 8px));border-color:var(--_active-indicator-color) var(--_active-indicator-color) transparent transparent;animation:expand-arc;animation-iteration-count:infinite;animation-fill-mode:both;animation-duration:1333ms,5332ms;animation-timing-function:cubic-bezier(0.4,0,0.2,1)}.four-color .circle{animation-name:expand-arc,four-color}.left .circle{rotate:135deg;inset:0 -100% 0 0}.right .circle{rotate:100deg;inset:0 0 0 -100%;animation-delay:-.666s,0s}@media(forced-colors:active){.active-track{stroke:CanvasText}.circle{border-color:CanvasText CanvasText Canvas Canvas}}@keyframes expand-arc{0%{transform:rotate(265deg)}50%{transform:rotate(130deg)}100%{transform:rotate(265deg)}}@keyframes rotate-arc{12.5%{transform:rotate(135deg)}25%{transform:rotate(270deg)}37.5%{transform:rotate(405deg)}50%{transform:rotate(540deg)}62.5%{transform:rotate(675deg)}75%{transform:rotate(810deg)}87.5%{transform:rotate(945deg)}100%{transform:rotate(1080deg)}}@keyframes linear-rotate{to{transform:rotate(360deg)}}@keyframes four-color{0%{border-top-color:var(--_four-color-active-indicator-one-color);border-right-color:var(--_four-color-active-indicator-one-color)}15%{border-top-color:var(--_four-color-active-indicator-one-color);border-right-color:var(--_four-color-active-indicator-one-color)}25%{border-top-color:var(--_four-color-active-indicator-two-color);border-right-color:var(--_four-color-active-indicator-two-color)}40%{border-top-color:var(--_four-color-active-indicator-two-color);border-right-color:var(--_four-color-active-indicator-two-color)}50%{border-top-color:var(--_four-color-active-indicator-three-color);border-right-color:var(--_four-color-active-indicator-three-color)}65%{border-top-color:var(--_four-color-active-indicator-three-color);border-right-color:var(--_four-color-active-indicator-three-color)}75%{border-top-color:var(--_four-color-active-indicator-four-color);border-right-color:var(--_four-color-active-indicator-four-color)}90%{border-top-color:var(--_four-color-active-indicator-four-color);border-right-color:var(--_four-color-active-indicator-four-color)}100%{border-top-color:var(--_four-color-active-indicator-one-color);border-right-color:var(--_four-color-active-indicator-one-color)}}`;let u=class extends l{};u.styles=[d],u=(0,i.__decorate)([(0,o.Mo)("md-circular-progress")],u)}};
//# sourceMappingURL=28922.i5n9-zx6INE.js.map