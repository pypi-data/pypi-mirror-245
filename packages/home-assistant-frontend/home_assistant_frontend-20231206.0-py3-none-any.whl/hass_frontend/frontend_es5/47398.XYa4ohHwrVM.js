"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[47398],{54736:function(e,r,t){var n,o,a=t(88962),i=t(33368),c=t(71650),s=t(82390),l=t(69205),d=t(70906),u=t(91808),h=(t(97393),t(63789),t(46798),t(9849),t(50289),t(94167),t(27392),t(68144)),p=t(95260);(0,u.Z)([(0,p.Mo)("ha-ansi-to-html")],(function(e,r){var t=function(r){(0,l.Z)(n,r);var t=(0,d.Z)(n);function n(){var r;(0,c.Z)(this,n);for(var o=arguments.length,a=new Array(o),i=0;i<o;i++)a[i]=arguments[i];return r=t.call.apply(t,[this].concat(a)),e((0,s.Z)(r)),r}return(0,i.Z)(n)}(r);return{F:t,d:[{kind:"field",decorators:[(0,p.Cb)()],key:"content",value:void 0},{kind:"method",key:"render",value:function(){return(0,h.dy)(n||(n=(0,a.Z)(["",""])),this._parseTextToColoredPre(this.content))}},{kind:"get",static:!0,key:"styles",value:function(){return(0,h.iv)(o||(o=(0,a.Z)(["pre{overflow-x:auto;white-space:pre-wrap;overflow-wrap:break-word}.bold{font-weight:700}.italic{font-style:italic}.underline{text-decoration:underline}.strikethrough{text-decoration:line-through}.underline.strikethrough{text-decoration:underline line-through}.fg-red{color:var(--error-color)}.fg-green{color:var(--success-color)}.fg-yellow{color:var(--warning-color)}.fg-blue{color:var(--info-color)}.fg-magenta{color:#762671}.fg-cyan{color:#2cb5e9}.fg-white{color:#ccc}.bg-black{background-color:#000}.bg-red{background-color:var(--error-color)}.bg-green{background-color:var(--success-color)}.bg-yellow{background-color:var(--warning-color)}.bg-blue{background-color:var(--info-color)}.bg-magenta{background-color:#762671}.bg-cyan{background-color:#2cb5e9}.bg-white{background-color:#ccc}"])))}},{kind:"method",key:"_parseTextToColoredPre",value:function(e){for(var r,t=document.createElement("pre"),n=/\033(?:\[(.*?)[@-~]|\].*?(?:\007|\033\\))/g,o=0,a={bold:!1,italic:!1,underline:!1,strikethrough:!1,foregroundColor:null,backgroundColor:null},i=function(e){var r=document.createElement("span");a.bold&&r.classList.add("bold"),a.italic&&r.classList.add("italic"),a.underline&&r.classList.add("underline"),a.strikethrough&&r.classList.add("strikethrough"),null!==a.foregroundColor&&r.classList.add("fg-".concat(a.foregroundColor)),null!==a.backgroundColor&&r.classList.add("bg-".concat(a.backgroundColor)),r.appendChild(document.createTextNode(e)),t.appendChild(r)};null!==(r=n.exec(e));){var c=r.index;i(e.substring(o,c)),o=c+r[0].length,void 0!==r[1]&&r[1].split(";").forEach((function(e){switch(parseInt(e,10)){case 0:a.bold=!1,a.italic=!1,a.underline=!1,a.strikethrough=!1,a.foregroundColor=null,a.backgroundColor=null;break;case 1:a.bold=!0;break;case 3:a.italic=!0;break;case 4:a.underline=!0;break;case 9:a.strikethrough=!0;break;case 22:a.bold=!1;break;case 23:a.italic=!1;break;case 24:a.underline=!1;break;case 29:a.strikethrough=!1;break;case 30:case 39:a.foregroundColor=null;break;case 31:a.foregroundColor="red";break;case 32:a.foregroundColor="green";break;case 33:a.foregroundColor="yellow";break;case 34:a.foregroundColor="blue";break;case 35:a.foregroundColor="magenta";break;case 36:a.foregroundColor="cyan";break;case 37:a.foregroundColor="white";break;case 40:a.backgroundColor="black";break;case 41:a.backgroundColor="red";break;case 42:a.backgroundColor="green";break;case 43:a.backgroundColor="yellow";break;case 44:a.backgroundColor="blue";break;case 45:a.backgroundColor="magenta";break;case 46:a.backgroundColor="cyan";break;case 47:a.backgroundColor="white";break;case 49:a.backgroundColor=null}}))}return i(e.substring(o)),t}}]}}),h.oi)},86630:function(e,r,t){var n,o,a,i,c=t(99312),s=t(81043),l=t(88962),d=t(33368),u=t(71650),h=t(82390),p=t(69205),f=t(70906),g=t(91808),v=t(34541),k=t(47838),b=(t(97393),t(49412)),y=t(3762),m=t(68144),w=t(95260),_=t(38346),Z=t(96151);t(10983),(0,g.Z)([(0,w.Mo)("ha-select")],(function(e,r){var t=function(r){(0,p.Z)(n,r);var t=(0,f.Z)(n);function n(){var r;(0,u.Z)(this,n);for(var o=arguments.length,a=new Array(o),i=0;i<o;i++)a[i]=arguments[i];return r=t.call.apply(t,[this].concat(a)),e((0,h.Z)(r)),r}return(0,d.Z)(n)}(r);return{F:t,d:[{kind:"field",decorators:[(0,w.Cb)({type:Boolean})],key:"icon",value:void 0},{kind:"field",decorators:[(0,w.Cb)({type:Boolean,reflect:!0})],key:"clearable",value:void 0},{kind:"method",key:"render",value:function(){return(0,m.dy)(n||(n=(0,l.Z)([" "," "," "])),(0,v.Z)((0,k.Z)(t.prototype),"render",this).call(this),this.clearable&&!this.required&&!this.disabled&&this.value?(0,m.dy)(o||(o=(0,l.Z)(['<ha-icon-button label="clear" @click="','" .path="','"></ha-icon-button>'])),this._clearValue,"M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z"):m.Ld)}},{kind:"method",key:"renderLeadingIcon",value:function(){return this.icon?(0,m.dy)(a||(a=(0,l.Z)(['<span class="mdc-select__icon"><slot name="icon"></slot></span>']))):m.Ld}},{kind:"method",key:"connectedCallback",value:function(){(0,v.Z)((0,k.Z)(t.prototype),"connectedCallback",this).call(this),window.addEventListener("translations-updated",this._translationsUpdated)}},{kind:"method",key:"disconnectedCallback",value:function(){(0,v.Z)((0,k.Z)(t.prototype),"disconnectedCallback",this).call(this),window.removeEventListener("translations-updated",this._translationsUpdated)}},{kind:"method",key:"_clearValue",value:function(){!this.disabled&&this.value&&(this.valueSetDirectly=!0,this.select(-1),this.mdcFoundation.handleChange())}},{kind:"field",key:"_translationsUpdated",value:function(){var e=this;return(0,_.D)((0,s.Z)((0,c.Z)().mark((function r(){return(0,c.Z)().wrap((function(r){for(;;)switch(r.prev=r.next){case 0:return r.next=2,(0,Z.y)();case 2:e.layoutOptions();case 3:case"end":return r.stop()}}),r)}))),500)}},{kind:"field",static:!0,key:"styles",value:function(){return[y.W,(0,m.iv)(i||(i=(0,l.Z)([":host([clearable]){position:relative}.mdc-select:not(.mdc-select--disabled) .mdc-select__icon{color:var(--secondary-text-color)}.mdc-select__anchor{width:var(--ha-select-min-width,200px)}.mdc-select--filled .mdc-select__anchor{height:var(--ha-select-height,56px)}.mdc-select--filled .mdc-floating-label{inset-inline-start:12px;inset-inline-end:initial;direction:var(--direction)}.mdc-select--filled.mdc-select--with-leading-icon .mdc-floating-label{inset-inline-start:48px;inset-inline-end:initial;direction:var(--direction)}.mdc-select .mdc-select__anchor{padding-inline-start:12px;padding-inline-end:0px;direction:var(--direction)}.mdc-select__anchor .mdc-floating-label--float-above{transform-origin:var(--float-start)}.mdc-select__selected-text-container{padding-inline-end:var(--select-selected-text-padding-end,0px)}:host([clearable]) .mdc-select__selected-text-container{padding-inline-end:var(--select-selected-text-padding-end,12px)}ha-icon-button{position:absolute;top:10px;right:28px;--mdc-icon-button-size:36px;--mdc-icon-size:20px;color:var(--secondary-text-color);inset-inline-start:initial;inset-inline-end:28px;direction:var(--direction)}"])))]}}]}}),b.K)},17515:function(e,r,t){t.d(r,{G:function(){return n},l:function(){return o}});var n=function(e){return e.callApi("GET","error_log")},o="/api/error_log"},69810:function(e,r,t){t.d(r,{CP:function(){return h},Lm:function(){return p},NC:function(){return f},gM:function(){return g},jP:function(){return v},lC:function(){return u}});var n,o,a,i,c=t(99312),s=t(81043),l=(t(40271),t(60163),t(63864)),d=t(41682),u=32143==t.j?(n=(0,s.Z)((0,c.Z)().mark((function e(r){return(0,c.Z)().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:if(!(0,l.I)(r.config.version,2021,2,4)){e.next=4;break}return e.next=3,r.callWS({type:"supervisor/api",endpoint:"/supervisor/reload",method:"post"});case 3:return e.abrupt("return");case 4:return e.next=6,r.callApi("POST","hassio/supervisor/reload");case 6:case"end":return e.stop()}}),e)}))),function(e){return n.apply(this,arguments)}):null,h=32143==t.j?(o=(0,s.Z)((0,c.Z)().mark((function e(r){return(0,c.Z)().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:if(!(0,l.I)(r.config.version,2021,2,4)){e.next=2;break}return e.abrupt("return",r.callWS({type:"supervisor/api",endpoint:"/supervisor/info",method:"get"}));case 2:return e.t0=d.rY,e.next=5,r.callApi("GET","hassio/supervisor/info");case 5:return e.t1=e.sent,e.abrupt("return",(0,e.t0)(e.t1));case 7:case"end":return e.stop()}}),e)}))),function(e){return o.apply(this,arguments)}):null,p=32143==t.j?(a=(0,s.Z)((0,c.Z)().mark((function e(r){return(0,c.Z)().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:if(!(0,l.I)(r.config.version,2021,2,4)){e.next=2;break}return e.abrupt("return",r.callWS({type:"supervisor/api",endpoint:"/info",method:"get"}));case 2:return e.t0=d.rY,e.next=5,r.callApi("GET","hassio/info");case 5:return e.t1=e.sent,e.abrupt("return",(0,e.t0)(e.t1));case 7:case"end":return e.stop()}}),e)}))),function(e){return a.apply(this,arguments)}):null,f=function(){var e=(0,s.Z)((0,c.Z)().mark((function e(r,t){return(0,c.Z)().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.abrupt("return",r.callApi("GET","hassio/".concat(t.includes("_")?"addons/".concat(t):t,"/logs")));case 1:case"end":return e.stop()}}),e)})));return function(r,t){return e.apply(this,arguments)}}(),g=function(e){return"/api/hassio/".concat(e.includes("_")?"addons/".concat(e):e,"/logs")},v=32143==t.j?(i=(0,s.Z)((0,c.Z)().mark((function e(r,t){return(0,c.Z)().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:if(!(0,l.I)(r.config.version,2021,2,4)){e.next=4;break}return e.next=3,r.callWS({type:"supervisor/api",endpoint:"/supervisor/options",method:"post",data:t});case 3:return e.abrupt("return");case 4:return e.next=6,r.callApi("POST","hassio/supervisor/options",t);case 6:case"end":return e.stop()}}),e)}))),function(e,r){return i.apply(this,arguments)}):null},47398:function(e,r,t){var n,o,a,i,c,s,l,d,u,h,p=t(99312),f=t(81043),g=t(88962),v=t(33368),k=t(71650),b=t(82390),y=t(69205),m=t(70906),w=t(91808),_=t(34541),Z=t(47838),x=(t(97393),t(63789),t(24074),t(87438),t(46798),t(9849),t(22890),t(91989),t(40271),t(60163),t(46349),t(70320),t(47704),t(44577),t(68144)),C=t(95260),L=t(7323),T=(t(9381),t(54736),t(22098),t(10983),t(86630),t(52039),t(22814)),M=t(17515),A=t(41682),H=t(69810),S=t(38346),z=t(25936),E="M5,20H19V18H5M19,9H15V3H9V9H5L12,16L19,9Z";(0,w.Z)([(0,C.Mo)("error-log-card")],(function(e,r){var t,w,I,F=function(r){(0,y.Z)(n,r);var t=(0,m.Z)(n);function n(){var r;(0,k.Z)(this,n);for(var o=arguments.length,a=new Array(o),i=0;i<o;i++)a[i]=arguments[i];return r=t.call.apply(t,[this].concat(a)),e((0,b.Z)(r)),r}return(0,v.Z)(n)}(r);return{F:F,d:[{kind:"field",decorators:[(0,C.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,C.Cb)()],key:"filter",value:function(){return""}},{kind:"field",decorators:[(0,C.Cb)()],key:"header",value:void 0},{kind:"field",decorators:[(0,C.Cb)()],key:"provider",value:void 0},{kind:"field",decorators:[(0,C.Cb)({type:Boolean,attribute:!0})],key:"show",value:function(){return!1}},{kind:"field",decorators:[(0,C.SB)()],key:"_isLogLoaded",value:function(){return!1}},{kind:"field",decorators:[(0,C.SB)()],key:"_logHTML",value:void 0},{kind:"field",decorators:[(0,C.SB)()],key:"_error",value:void 0},{kind:"method",key:"render",value:function(){return(0,x.dy)(n||(n=(0,g.Z)([' <div class="error-log-intro"> '," "," "," </div> "])),this._error?(0,x.dy)(o||(o=(0,g.Z)(['<ha-alert alert-type="error">',"</ha-alert>"])),this._error):"",this._logHTML?(0,x.dy)(a||(a=(0,g.Z)([' <ha-card outlined> <div class="header"> <h1 class="card-header"> ',' </h1> <div> <ha-icon-button .path="','" @click="','" .label="','"></ha-icon-button> <ha-icon-button .path="','" @click="','" .label="','"></ha-icon-button> </div> </div> <div class="card-content error-log">',"</div> </ha-card> "])),this.header||this.hass.localize("ui.panel.config.logs.show_full_logs"),"M17.65,6.35C16.2,4.9 14.21,4 12,4A8,8 0 0,0 4,12A8,8 0 0,0 12,20C15.73,20 18.84,17.45 19.73,14H17.65C16.83,16.33 14.61,18 12,18A6,6 0 0,1 6,12A6,6 0 0,1 12,6C13.66,6 15.14,6.69 16.22,7.78L13,11H20V4L17.65,6.35Z",this._refresh,this.hass.localize("ui.common.refresh"),E,this._downloadFullLog,this.hass.localize("ui.panel.config.logs.download_full_log"),this._logHTML):"",this._logHTML?"":(0,x.dy)(i||(i=(0,g.Z)([' <mwc-button outlined @click="','"> <ha-svg-icon .path="','"></ha-svg-icon> ',' </mwc-button> <mwc-button raised @click="','"> '," </mwc-button> "])),this._downloadFullLog,E,this.hass.localize("ui.panel.config.logs.download_full_log"),this._refreshLogs,this.hass.localize("ui.panel.config.logs.load_logs")))}},{kind:"field",key:"_debounceSearch",value:function(){var e=this;return(0,S.D)((function(){return e._isLogLoaded?e._refreshLogs():e._debounceSearch()}),150,!1)}},{kind:"method",key:"firstUpdated",value:function(e){var r;(0,_.Z)((0,Z.Z)(F.prototype),"firstUpdated",this).call(this,e),(null!==(r=this.hass)&&void 0!==r&&r.config.recovery_mode||this.show)&&(this.hass.loadFragmentTranslation("config"),this._refreshLogs())}},{kind:"method",key:"updated",value:function(e){(0,_.Z)((0,Z.Z)(F.prototype),"updated",this).call(this,e),e.has("provider")&&(this._logHTML=void 0),e.has("show")&&this.show||e.has("provider")&&this.show?this._refreshLogs():e.has("filter")&&this._debounceSearch()}},{kind:"method",key:"_refresh",value:(I=(0,f.Z)((0,p.Z)().mark((function e(r){var t;return(0,p.Z)().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return(t=r.currentTarget).progress=!0,e.next=4,this._refreshLogs();case 4:t.progress=!1;case 5:case"end":return e.stop()}}),e,this)}))),function(e){return I.apply(this,arguments)})},{kind:"method",key:"_downloadFullLog",value:(w=(0,f.Z)((0,p.Z)().mark((function e(){var r,t,n,o;return(0,p.Z)().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return r=(new Date).toISOString().replace(/:/g,"-"),t="core"!==this.provider?(0,H.gM)(this.provider):M.l,n="core"!==this.provider?"".concat(this.provider,"_").concat(r,".log"):"home-assistant_".concat(r,".log"),e.next=5,(0,T.iI)(this.hass,t);case 5:o=e.sent,(0,z.N)(o.path,n);case 7:case"end":return e.stop()}}),e,this)}))),function(){return w.apply(this,arguments)})},{kind:"method",key:"_refreshLogs",value:(t=(0,f.Z)((0,p.Z)().mark((function e(){var r,t,n=this;return(0,p.Z)().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:if(this._logHTML=this.hass.localize("ui.panel.config.logs.loading_log"),"core"===this.provider||!(0,L.p)(this.hass,"hassio")){e.next=21;break}return e.prev=2,e.next=5,(0,H.NC)(this.hass,this.provider);case 5:if(r=e.sent,this.filter&&(r=r.split("\n").filter((function(e){return e.toLowerCase().includes(n.filter.toLowerCase())})).join("\n")),r){e.next=10;break}return this._logHTML=this.hass.localize("ui.panel.config.logs.no_errors"),e.abrupt("return");case 10:return this._logHTML=(0,x.dy)(c||(c=(0,g.Z)(['<ha-ansi-to-html .content="','"> </ha-ansi-to-html>'])),r),this._isLogLoaded=!0,e.abrupt("return");case 15:return e.prev=15,e.t0=e.catch(2),this._error=this.hass.localize("ui.panel.config.logs.failed_get_logs",{provider:this.provider,error:(0,A.js)(e.t0)}),e.abrupt("return");case 19:e.next=24;break;case 21:return e.next=23,(0,M.G)(this.hass);case 23:r=e.sent;case 24:this._isLogLoaded=!0,t=r&&r.split("\n"),this._logHTML=t?(this.filter?t.filter((function(e){return n.filter?e.toLowerCase().includes(n.filter.toLowerCase()):e})):t).map((function(e){return e.includes("INFO")?(0,x.dy)(s||(s=(0,g.Z)(['<div class="info">',"</div>"])),e):e.includes("WARNING")?(0,x.dy)(l||(l=(0,g.Z)(['<div class="warning">',"</div>"])),e):e.includes("ERROR")||e.includes("FATAL")||e.includes("CRITICAL")?(0,x.dy)(d||(d=(0,g.Z)(['<div class="error">',"</div>"])),e):(0,x.dy)(u||(u=(0,g.Z)(["<div>","</div>"])),e)})):this.hass.localize("ui.panel.config.logs.no_errors");case 27:case"end":return e.stop()}}),e,this,[[2,15]])}))),function(){return t.apply(this,arguments)})},{kind:"field",static:!0,key:"styles",value:function(){return(0,x.iv)(h||(h=(0,g.Z)([".error-log-intro{text-align:center;margin:16px}ha-card{padding-top:16px}.header{display:flex;justify-content:space-between;padding:0 16px}.card-header{color:var(--ha-card-header-color,--primary-text-color);font-family:var(--ha-card-header-font-family, inherit);font-size:var(--ha-card-header-font-size, 24px);letter-spacing:-.012em;line-height:48px;display:block;margin-block-start:0px;margin-block-end:0px;font-weight:400}ha-select{display:block;max-width:500px;width:100%}ha-icon-button{float:right}.error-log{font-family:var(--code-font-family, monospace);clear:both;text-align:left;padding-top:12px}.error-log>div{overflow:auto;overflow-wrap:break-word}.error-log>div:hover{background-color:var(--secondary-background-color)}.error{color:var(--error-color)}.warning{color:var(--warning-color)}mwc-button{direction:var(--direction)}"])))}}]}}),x.oi)},25936:function(e,r,t){t.d(r,{N:function(){return n}});var n=function(e){var r=arguments.length>1&&void 0!==arguments[1]?arguments[1]:"",t=document.createElement("a");t.target="_blank",t.href=e,t.download=r,document.body.appendChild(t),t.dispatchEvent(new MouseEvent("click")),document.body.removeChild(t)}}}]);
//# sourceMappingURL=47398.XYa4ohHwrVM.js.map