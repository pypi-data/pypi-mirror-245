export const id=96339;export const ids=[96339];export const modules={25516:(t,s,e)=>{e.d(s,{i:()=>a});const i=(0,e(8330).P)((t=>{history.replaceState({scrollPosition:t},"")}),300),a=t=>s=>({kind:"method",placement:"prototype",key:s.key,descriptor:{set(t){i(t),this[`__${String(s.key)}`]=t},get(){var t;return this[`__${String(s.key)}`]||(null===(t=history.state)||void 0===t?void 0:t.scrollPosition)},enumerable:!0,configurable:!0},finisher(e){const i=e.prototype.connectedCallback;e.prototype.connectedCallback=function(){i.call(this);const e=this[s.key];e&&this.updateComplete.then((()=>{const s=this.renderRoot.querySelector(t);s&&setTimeout((()=>{s.scrollTop=e}),0)}))}}})},8330:(t,s,e)=>{e.d(s,{P:()=>i});const i=(t,s,e=!0,i=!0)=>{let a,o=0;const l=(...l)=>{const n=()=>{o=!1===e?0:Date.now(),a=void 0,t(...l)},d=Date.now();o||!1!==e||(o=d);const r=s-(d-o);r<=0||r>s?(a&&(clearTimeout(a),a=void 0),o=d,t(...l)):a||!1===i||(a=window.setTimeout(n,r))};return l.cancel=()=>{clearTimeout(a),a=void 0,o=0},l}},73826:(t,s,e)=>{e.d(s,{f:()=>n});var i=e(17463),a=e(34541),o=e(47838),l=e(79932);const n=t=>(0,i.Z)(null,(function(t,s){class e extends s{constructor(...s){super(...s),t(this)}}return{F:e,d:[{kind:"field",decorators:[(0,l.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",key:"hassSubscribeRequiredHostProps",value:void 0},{kind:"field",key:"__unsubs",value:void 0},{kind:"method",key:"connectedCallback",value:function(){(0,a.Z)((0,o.Z)(e.prototype),"connectedCallback",this).call(this),this.__checkSubscribed()}},{kind:"method",key:"disconnectedCallback",value:function(){if((0,a.Z)((0,o.Z)(e.prototype),"disconnectedCallback",this).call(this),this.__unsubs){for(;this.__unsubs.length;){const t=this.__unsubs.pop();t instanceof Promise?t.then((t=>t())):t()}this.__unsubs=void 0}}},{kind:"method",key:"updated",value:function(t){if((0,a.Z)((0,o.Z)(e.prototype),"updated",this).call(this,t),t.has("hass"))this.__checkSubscribed();else if(this.hassSubscribeRequiredHostProps)for(const s of t.keys())if(this.hassSubscribeRequiredHostProps.includes(s))return void this.__checkSubscribed()}},{kind:"method",key:"hassSubscribe",value:function(){return[]}},{kind:"method",key:"__checkSubscribed",value:function(){var t;void 0!==this.__unsubs||!this.isConnected||void 0===this.hass||null!==(t=this.hassSubscribeRequiredHostProps)&&void 0!==t&&t.some((t=>void 0===this[t]))||(this.__unsubs=this.hassSubscribe())}}]}}),t)},4643:(t,s,e)=>{e.r(s);var i=e(17463),a=(e(14271),e(68144)),o=e(79932),l=e(14516),n=e(47181),d=e(91741),r=(e(37168),e(74186)),c=e(38014),u=e(26765),h=e(73826),_=e(11654);const p=()=>Promise.all([e.e(28597),e.e(50529),e.e(3762),e.e(49412),e.e(81866),e.e(92488),e.e(74177),e.e(42059),e.e(68331),e.e(9039),e.e(139)]).then(e.bind(e,211)),b=()=>Promise.all([e.e(28597),e.e(70632),e.e(5553)]).then(e.bind(e,24054));var f=e(87744),v=e(27322);const k={no_state:0,entity_no_longer_recorded:1,entity_not_recorded:1,unsupported_state_class:2,units_changed:3};(0,i.Z)([(0,o.Mo)("developer-tools-statistics")],(function(t,s){return{F:class extends s{constructor(...s){super(...s),t(this)}},d:[{kind:"field",decorators:[(0,o.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,o.Cb)({type:Boolean})],key:"narrow",value:void 0},{kind:"field",decorators:[(0,o.SB)()],key:"_data",value:()=>[]},{kind:"field",key:"_disabledEntities",value:()=>new Set},{kind:"field",key:"_deletedStatistics",value:()=>new Set},{kind:"method",key:"firstUpdated",value:function(){this._validateStatistics()}},{kind:"field",key:"_displayData",value:()=>(0,l.Z)(((t,s)=>t.map((t=>{var e;return{...t,displayName:t.state?(0,d.C)(t.state):t.name||t.statistic_id,issues_string:null===(e=t.issues)||void 0===e?void 0:e.map((t=>s(`ui.panel.developer-tools.tabs.statistics.issues.${t.type}`,t.data)||t.type)).join(" ")}}))))},{kind:"field",key:"_columns",value(){return(0,l.Z)((t=>({displayName:{title:t("ui.panel.developer-tools.tabs.statistics.data_table.name"),sortable:!0,filterable:!0,grows:!0},statistic_id:{title:t("ui.panel.developer-tools.tabs.statistics.data_table.statistic_id"),sortable:!0,filterable:!0,hidden:this.narrow,width:"20%"},statistics_unit_of_measurement:{title:t("ui.panel.developer-tools.tabs.statistics.data_table.statistics_unit"),sortable:!0,filterable:!0,width:"10%",forceLTR:!0},source:{title:t("ui.panel.developer-tools.tabs.statistics.data_table.source"),sortable:!0,filterable:!0,width:"10%"},issues_string:{title:t("ui.panel.developer-tools.tabs.statistics.data_table.issue"),sortable:!0,filterable:!0,direction:"asc",width:"30%",template:s=>{var e;return a.dy`${null!==(e=s.issues_string)&&void 0!==e?e:t("ui.panel.developer-tools.tabs.statistics.no_issue")}`}},fix:{title:"",label:this.hass.localize("ui.panel.developer-tools.tabs.statistics.fix_issue.fix"),template:s=>a.dy`${s.issues?a.dy`<mwc-button @click="${this._fixIssue}" .data="${s.issues}"> ${t("ui.panel.developer-tools.tabs.statistics.fix_issue.fix")} </mwc-button>`:"—"}`,width:"113px"},actions:{title:"",label:t("ui.panel.developer-tools.tabs.statistics.adjust_sum"),type:"icon-button",template:s=>s.has_sum?a.dy` <ha-icon-button .label="${t("ui.panel.developer-tools.tabs.statistics.adjust_sum")}" .path="${"M22,13V22H2V19L22,13M21.68,7.06L16.86,4.46L17.7,7.24L7.58,10.24C6.63,8.95 4.82,8.67 3.53,9.62C2.24,10.57 1.96,12.38 2.91,13.67C3.85,14.97 5.67,15.24 6.96,14.29C7.67,13.78 8.1,12.97 8.14,12.09L18.26,9.09L19.1,11.87L21.68,7.06Z"}" .statistic="${s}" @click="${this._showStatisticsAdjustSumDialog}"></ha-icon-button> `:""}})))}},{kind:"method",key:"render",value:function(){return a.dy` <ha-data-table .hass="${this.hass}" .columns="${this._columns(this.hass.localize)}" .data="${this._displayData(this._data,this.hass.localize)}" noDataText="No statistics" id="statistic_id" clickable @row-click="${this._rowClicked}" .dir="${(0,f.Zu)(this.hass)}"></ha-data-table> `}},{kind:"method",key:"_showStatisticsAdjustSumDialog",value:function(t){var s,e;t.stopPropagation(),s=this,e={statistic:t.currentTarget.statistic},(0,n.B)(s,"show-dialog",{dialogTag:"dialog-statistics-adjust-sum",dialogImport:p,dialogParams:e})}},{kind:"method",key:"_rowClicked",value:function(t){const s=t.detail.id;s in this.hass.states&&(0,n.B)(this,"hass-more-info",{entityId:s})}},{kind:"method",key:"hassSubscribe",value:function(){return[(0,r.LM)(this.hass.connection,(t=>{const s=new Set;for(const e of t)e.disabled_by&&s.add(e.entity_id);s!==this._disabledEntities&&(this._disabledEntities=s,this._validateStatistics())}))]}},{kind:"method",key:"_validateStatistics",value:async function(){const[t,s]=await Promise.all([(0,c.uR)(this.hass),(0,c.h_)(this.hass)]),e=new Set;this._data=t.filter((t=>!this._disabledEntities.has(t.statistic_id)&&!this._deletedStatistics.has(t.statistic_id))).map((t=>(e.add(t.statistic_id),{...t,state:this.hass.states[t.statistic_id],issues:s[t.statistic_id]}))),Object.keys(s).forEach((t=>{e.has(t)||this._disabledEntities.has(t)||this._deletedStatistics.has(t)||this._data.push({statistic_id:t,statistics_unit_of_measurement:"",source:"",state:this.hass.states[t],issues:s[t],has_mean:!1,has_sum:!1,unit_class:null})}))}},{kind:"field",key:"_fixIssue",value(){return t=>{const s=t.currentTarget.data.sort(((t,s)=>{var e,i;return(null!==(e=k[t.type])&&void 0!==e?e:99)-(null!==(i=k[s.type])&&void 0!==i?i:99)}))[0];switch(s.type){case"no_state":(0,u.showConfirmationDialog)(this,{title:this.hass.localize("ui.panel.developer-tools.tabs.statistics.fix_issue.no_state.title"),text:a.dy`${this.hass.localize("ui.panel.developer-tools.tabs.statistics.fix_issue.no_state.info_text_1")}<br><br>${this.hass.localize("ui.panel.developer-tools.tabs.statistics.fix_issue.no_state.info_text_2",{statistic_id:s.data.statistic_id})}`,confirmText:this.hass.localize("ui.common.delete"),confirm:async()=>{await(0,c.hN)(this.hass,[s.data.statistic_id]),this._deletedStatistics.add(s.data.statistic_id),this._validateStatistics()}});break;case"entity_not_recorded":(0,u.showAlertDialog)(this,{title:this.hass.localize("ui.panel.developer-tools.tabs.statistics.fix_issue.entity_not_recorded.title"),text:a.dy`${this.hass.localize("ui.panel.developer-tools.tabs.statistics.fix_issue.entity_not_recorded.info_text_1")}<br><br>${this.hass.localize("ui.panel.developer-tools.tabs.statistics.fix_issue.entity_not_recorded.info_text_2")}<br><br> <a href="${(0,v.R)(this.hass,"/integrations/recorder/#configure-filter")}" target="_blank" rel="noreferrer noopener"> ${this.hass.localize("ui.panel.developer-tools.tabs.statistics.fix_issue.entity_not_recorded.info_text_3_link")}</a>`});break;case"entity_no_longer_recorded":(0,u.showAlertDialog)(this,{title:this.hass.localize("ui.panel.developer-tools.tabs.statistics.fix_issue.entity_no_longer_recorded.title"),text:a.dy`${this.hass.localize("ui.panel.developer-tools.tabs.statistics.fix_issue.entity_no_longer_recorded.info_text_1")} ${this.hass.localize("ui.panel.developer-tools.tabs.statistics.fix_issue.entity_no_longer_recorded.info_text_2")} <a href="${(0,v.R)(this.hass,"/integrations/recorder/#configure-filter")}" target="_blank" rel="noreferrer noopener"> ${this.hass.localize("ui.panel.developer-tools.tabs.statistics.fix_issue.entity_no_longer_recorded.info_text_3_link")}</a>`});break;case"unsupported_state_class":(0,u.showConfirmationDialog)(this,{title:this.hass.localize("ui.panel.developer-tools.tabs.statistics.fix_issue.unsupported_state_class.title"),text:a.dy`${this.hass.localize("ui.panel.developer-tools.tabs.statistics.fix_issue.unsupported_state_class.info_text_1",{state_class:s.data.state_class})}<br><br> ${this.hass.localize("ui.panel.developer-tools.tabs.statistics.fix_issue.unsupported_state_class.info_text_2")} <ul> <li> ${this.hass.localize("ui.panel.developer-tools.tabs.statistics.fix_issue.unsupported_state_class.info_text_3")} </li> <li> ${this.hass.localize("ui.panel.developer-tools.tabs.statistics.fix_issue.unsupported_state_class.info_text_4")} <a href="https://developers.home-assistant.io/docs/core/entity/sensor/#long-term-statistics" target="_blank" rel="noreferrer noopener"> ${this.hass.localize("ui.panel.developer-tools.tabs.statistics.fix_issue.unsupported_state_class.info_text_4_link")}</a> </li> <li> ${this.hass.localize("ui.panel.developer-tools.tabs.statistics.fix_issue.unsupported_state_class.info_text_5")} </li> </ul> ${this.hass.localize("ui.panel.developer-tools.tabs.statistics.fix_issue.unsupported_state_class.info_text_6",{statistic_id:s.data.statistic_id})}`,confirmText:this.hass.localize("ui.common.delete"),confirm:async()=>{await(0,c.hN)(this.hass,[s.data.statistic_id]),this._deletedStatistics.add(s.data.statistic_id),this._validateStatistics()}});break;case"units_changed":e=this,i={issue:s,fixedCallback:()=>{this._validateStatistics()}},(0,n.B)(e,"show-dialog",{dialogTag:"dialog-statistics-fix-units-changed",dialogImport:b,dialogParams:i});break;default:(0,u.showAlertDialog)(this,{title:this.hass.localize("ui.panel.developer-tools.tabs.statistics.fix_issue.no_support.title"),text:this.hass.localize("ui.panel.developer-tools.tabs.statistics.fix_issue.no_support.info_text_1")})}var e,i}}},{kind:"get",static:!0,key:"styles",value:function(){return[_.Qx,a.iv`.content{padding:16px;padding:max(16px,env(safe-area-inset-top)) max(16px,env(safe-area-inset-right)) max(16px,env(safe-area-inset-bottom)) max(16px,env(safe-area-inset-left))}th{padding:0 8px;text-align:left;font-size:var(
            --paper-input-container-shared-input-style_-_font-size
          )}:host([rtl]) th{text-align:right}tr{vertical-align:top;direction:ltr}tr:nth-child(odd){background-color:var(--table-row-background-color,#fff)}tr:nth-child(2n){background-color:var(--table-row-alternative-background-color,#eee)}td{padding:4px;min-width:200px;word-break:break-word}`]}}]}}),(0,h.f)(a.oi))},44281:(t,s,e)=>{e.d(s,{j:()=>i});const i=async()=>{try{new ResizeObserver((()=>{}))}catch(t){window.ResizeObserver=(await e.e(5442).then(e.bind(e,5442))).default}}},27322:(t,s,e)=>{e.d(s,{R:()=>i});const i=(t,s)=>`https://${t.config.version.includes("b")?"rc":t.config.version.includes("dev")?"next":"www"}.home-assistant.io${s}`}};
//# sourceMappingURL=96339.r14FUcaZPzI.js.map