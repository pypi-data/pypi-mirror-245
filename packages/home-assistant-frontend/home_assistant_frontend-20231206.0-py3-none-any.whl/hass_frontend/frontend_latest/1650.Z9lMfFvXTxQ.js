export const id=1650;export const ids=[1650];export const modules={76680:(e,t,i)=>{function a(e){return void 0===e||Array.isArray(e)?e:[e]}i.d(t,{r:()=>a})},55642:(e,t,i)=>{i.d(t,{h:()=>n});var a=i(68144),s=i(57835);const n=(0,s.XM)(class extends s.Xe{constructor(e){if(super(e),this._element=void 0,e.type!==s.pX.CHILD)throw new Error("dynamicElementDirective can only be used in content bindings")}update(e,[t,i]){return this._element&&this._element.localName===t?(i&&Object.entries(i).forEach((([e,t])=>{this._element[e]=t})),a.Jb):this.render(t,i)}render(e,t){return this._element=document.createElement(e),t&&Object.entries(t).forEach((([e,t])=>{this._element[e]=t})),this._element}})},22311:(e,t,i)=>{i.d(t,{N:()=>s});var a=i(58831);const s=e=>(0,a.M)(e.entity_id)},40095:(e,t,i)=>{i.d(t,{e:()=>a});const a=(e,t)=>s(e.attributes,t),s=(e,t)=>0!=(e.supported_features&t)},86977:(e,t,i)=>{i.d(t,{Q:()=>a});const a=e=>!(!e.detail.selected||"property"!==e.detail.source)&&(e.currentTarget.selected=!1,!0)},61878:(e,t,i)=>{var a=i(17463),s=i(68144),n=i(79932);(0,a.Z)([(0,n.Mo)("ha-dialog-header")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"method",key:"render",value:function(){return s.dy` <header class="header"> <div class="header-bar"> <section class="header-navigation-icon"> <slot name="navigationIcon"></slot> </section> <section class="header-title"> <slot name="title"></slot> </section> <section class="header-action-items"> <slot name="actionItems"></slot> </section> </div> <slot></slot> </header> `}},{kind:"get",static:!0,key:"styles",value:function(){return[s.iv`:host{display:block}:host([show-border]){border-bottom:1px solid var(--mdc-dialog-scroll-divider-color,rgba(0,0,0,.12))}.header-bar{display:flex;flex-direction:row;align-items:flex-start;padding:4px;box-sizing:border-box}.header-title{flex:1;font-size:22px;line-height:28px;font-weight:400;padding:10px 4px;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}@media all and (min-width:450px) and (min-height:500px){.header-bar{padding:12px}}.header-navigation-icon{flex:none;min-width:8px;height:100%;display:flex;flex-direction:row}.header-action-items{flex:none;min-width:8px;height:100%;display:flex;flex-direction:row}`]}}]}}),s.oi)},47840:(e,t,i)=>{i.r(t),i.d(t,{DialogVoiceAssistantPipelineDetail:()=>v});var a=i(17463),s=i(68144),n=i(79932),o=i(47181),d=i(32594),l=i(86977),r=i(83849),c=(i(74834),i(61878),i(68331),i(69949)),h=i(11654),u=i(14516);(0,a.Z)([(0,n.Mo)("assist-pipeline-detail-config")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.Cb)()],key:"data",value:void 0},{kind:"field",decorators:[(0,n.Cb)()],key:"supportedLanguages",value:void 0},{kind:"method",key:"focus",value:async function(){var e;await this.updateComplete;const t=null===(e=this.renderRoot)||void 0===e?void 0:e.querySelector("ha-form");null==t||t.focus()}},{kind:"field",key:"_schema",value:()=>(0,u.Z)((e=>[{name:"",type:"grid",schema:[{name:"name",required:!0,selector:{text:{}}},e?{name:"language",required:!0,selector:{language:{languages:e}}}:{name:"",type:"constant"}]}]))},{kind:"field",key:"_computeLabel",value(){return e=>e.name?this.hass.localize(`ui.panel.config.voice_assistants.assistants.pipeline.detail.form.${e.name}`):""}},{kind:"method",key:"render",value:function(){return s.dy` <div class="section"> <div class="intro"> <h3> ${this.hass.localize("ui.panel.config.voice_assistants.assistants.pipeline.detail.steps.config.title")} </h3> <p> ${this.hass.localize("ui.panel.config.voice_assistants.assistants.pipeline.detail.steps.config.description")} </p> </div> <ha-form .schema="${this._schema(this.supportedLanguages)}" .data="${this.data}" .hass="${this.hass}" .computeLabel="${this._computeLabel}"></ha-form> </div> `}},{kind:"get",static:!0,key:"styles",value:function(){return s.iv`.section{border:1px solid var(--divider-color);border-radius:8px;box-sizing:border-box;padding:16px}.intro{margin-bottom:16px}h3{font-weight:400;font-size:22px;line-height:28px;margin-top:0;margin-bottom:4px}p{color:var(--secondary-text-color);font-size:var(--mdc-typography-body2-font-size, .875rem);margin-top:0;margin-bottom:0}`}}]}}),s.oi),(0,a.Z)([(0,n.Mo)("assist-pipeline-detail-conversation")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.Cb)()],key:"data",value:void 0},{kind:"field",decorators:[(0,n.SB)()],key:"_supportedLanguages",value:void 0},{kind:"field",key:"_schema",value:()=>(0,u.Z)(((e,t)=>[{name:"",type:"grid",schema:[{name:"conversation_engine",required:!0,selector:{conversation_agent:{language:e}}},"*"!==t&&null!=t&&t.length?{name:"conversation_language",required:!0,selector:{language:{languages:t,no_sort:!0}}}:{name:"",type:"constant"}]}]))},{kind:"field",key:"_computeLabel",value(){return e=>e.name?this.hass.localize(`ui.panel.config.voice_assistants.assistants.pipeline.detail.form.${e.name}`):""}},{kind:"method",key:"render",value:function(){var e;return s.dy` <div class="section"> <div class="intro"> <h3> ${this.hass.localize("ui.panel.config.voice_assistants.assistants.pipeline.detail.steps.conversation.title")} </h3> <p> ${this.hass.localize("ui.panel.config.voice_assistants.assistants.pipeline.detail.steps.conversation.description")} </p> </div> <ha-form .schema="${this._schema(null===(e=this.data)||void 0===e?void 0:e.language,this._supportedLanguages)}" .data="${this.data}" .hass="${this.hass}" .computeLabel="${this._computeLabel}" @supported-languages-changed="${this._supportedLanguagesChanged}"></ha-form> </div> `}},{kind:"method",key:"_supportedLanguagesChanged",value:function(e){"*"===e.detail.value&&setTimeout((()=>{const e={...this.data};e.conversation_language="*",(0,o.B)(this,"value-changed",{value:e})}),0),this._supportedLanguages=e.detail.value}},{kind:"get",static:!0,key:"styles",value:function(){return s.iv`.section{border:1px solid var(--divider-color);border-radius:8px;box-sizing:border-box;padding:16px}.intro{margin-bottom:16px}h3{font-weight:400;font-size:22px;line-height:28px;margin-top:0;margin-bottom:4px}p{color:var(--secondary-text-color);font-size:var(--mdc-typography-body2-font-size, .875rem);margin-top:0;margin-bottom:0}`}}]}}),s.oi),(0,a.Z)([(0,n.Mo)("assist-pipeline-detail-stt")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.Cb)()],key:"data",value:void 0},{kind:"field",decorators:[(0,n.SB)()],key:"_supportedLanguages",value:void 0},{kind:"field",key:"_schema",value:()=>(0,u.Z)(((e,t)=>[{name:"",type:"grid",schema:[{name:"stt_engine",selector:{stt:{language:e}}},null!=t&&t.length?{name:"stt_language",required:!0,selector:{language:{languages:t,no_sort:!0}}}:{name:"",type:"constant"}]}]))},{kind:"field",key:"_computeLabel",value(){return e=>e.name?this.hass.localize(`ui.panel.config.voice_assistants.assistants.pipeline.detail.form.${e.name}`):""}},{kind:"method",key:"render",value:function(){var e;return s.dy` <div class="section"> <div class="intro"> <h3> ${this.hass.localize("ui.panel.config.voice_assistants.assistants.pipeline.detail.steps.stt.title")} </h3> <p> ${this.hass.localize("ui.panel.config.voice_assistants.assistants.pipeline.detail.steps.stt.description")} </p> </div> <ha-form .schema="${this._schema(null===(e=this.data)||void 0===e?void 0:e.language,this._supportedLanguages)}" .data="${this.data}" .hass="${this.hass}" .computeLabel="${this._computeLabel}" @supported-languages-changed="${this._supportedLanguagesChanged}"></ha-form> </div> `}},{kind:"method",key:"_supportedLanguagesChanged",value:function(e){this._supportedLanguages=e.detail.value}},{kind:"get",static:!0,key:"styles",value:function(){return s.iv`.section{border:1px solid var(--divider-color);border-radius:8px;box-sizing:border-box;padding:16px}.intro{margin-bottom:16px}h3{font-weight:400;font-size:22px;line-height:28px;margin-top:0;margin-bottom:4px}p{color:var(--secondary-text-color);font-size:var(--mdc-typography-body2-font-size, .875rem);margin-top:0;margin-bottom:0}`}}]}}),s.oi);const p=()=>Promise.all([i.e(28597),i.e(5915)]).then(i.bind(i,5915));(0,a.Z)([(0,n.Mo)("assist-pipeline-detail-tts")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.Cb)()],key:"data",value:void 0},{kind:"field",decorators:[(0,n.SB)()],key:"_supportedLanguages",value:void 0},{kind:"field",key:"_schema",value:()=>(0,u.Z)(((e,t)=>[{name:"",type:"grid",schema:[{name:"tts_engine",selector:{tts:{language:e}}},null!=t&&t.length?{name:"tts_language",required:!0,selector:{language:{languages:t,no_sort:!0}}}:{name:"",type:"constant"},{name:"tts_voice",selector:{tts_voice:{}},context:{language:"tts_language",engineId:"tts_engine"},required:!0}]}]))},{kind:"field",key:"_computeLabel",value(){return e=>e.name?this.hass.localize(`ui.panel.config.voice_assistants.assistants.pipeline.detail.form.${e.name}`):""}},{kind:"method",key:"render",value:function(){var e,t;return s.dy` <div class="section"> <div class="content"> <div class="intro"> <h3> ${this.hass.localize("ui.panel.config.voice_assistants.assistants.pipeline.detail.steps.tts.title")} </h3> <p> ${this.hass.localize("ui.panel.config.voice_assistants.assistants.pipeline.detail.steps.tts.description")} </p> </div> <ha-form .schema="${this._schema(null===(e=this.data)||void 0===e?void 0:e.language,this._supportedLanguages)}" .data="${this.data}" .hass="${this.hass}" .computeLabel="${this._computeLabel}" @supported-languages-changed="${this._supportedLanguagesChanged}"></ha-form> </div> ${null!==(t=this.data)&&void 0!==t&&t.tts_engine?s.dy`<div class="footer"> <ha-button .label="${this.hass.localize("ui.panel.config.voice_assistants.assistants.pipeline.detail.try_tts")}" @click="${this._preview}"> </ha-button> </div>`:s.Ld} </div> `}},{kind:"method",key:"_preview",value:async function(){if(!this.data)return;const e=this.data.tts_engine,t=this.data.tts_language||void 0,i=this.data.tts_voice||void 0;var a,s;e&&(a=this,s={engine:e,language:t,voice:i},(0,o.B)(a,"show-dialog",{addHistory:!1,dialogTag:"dialog-tts-try",dialogImport:p,dialogParams:s}))}},{kind:"method",key:"_supportedLanguagesChanged",value:function(e){this._supportedLanguages=e.detail.value}},{kind:"get",static:!0,key:"styles",value:function(){return s.iv`.section{border:1px solid var(--divider-color);border-radius:8px}.content{padding:16px}.intro{margin-bottom:16px}h3{font-weight:400;font-size:22px;line-height:28px;margin-top:0;margin-bottom:4px}p{color:var(--secondary-text-color);font-size:var(--mdc-typography-body2-font-size, .875rem);margin-top:0;margin-bottom:0}.footer{border-top:1px solid var(--divider-color);padding:8px 16px}`}}]}}),s.oi);var g=i(27322);(0,a.Z)([(0,n.Mo)("assist-pipeline-detail-wakeword")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.Cb)()],key:"data",value:void 0},{kind:"field",decorators:[(0,n.SB)()],key:"_wakeWords",value:void 0},{kind:"field",key:"_schema",value:()=>(0,u.Z)((e=>[{name:"",type:"grid",schema:[{name:"wake_word_entity",selector:{entity:{domain:"wake_word"}}},null!=e&&e.length?{name:"wake_word_id",required:!0,selector:{select:{mode:"dropdown",sort:!0,options:e.map((e=>({value:e.id,label:e.name})))}}}:{name:"",type:"constant"}]}]))},{kind:"field",key:"_computeLabel",value(){return e=>e.name?this.hass.localize(`ui.panel.config.voice_assistants.assistants.pipeline.detail.form.${e.name}`):""}},{kind:"method",key:"willUpdate",value:function(e){var t,i,a,s;e.has("data")&&(null===(t=e.get("data"))||void 0===t?void 0:t.wake_word_entity)!==(null===(i=this.data)||void 0===i?void 0:i.wake_word_entity)&&(null!==(a=e.get("data"))&&void 0!==a&&a.wake_word_entity&&null!==(s=this.data)&&void 0!==s&&s.wake_word_id&&(0,o.B)(this,"value-changed",{value:{...this.data,wake_word_id:void 0}}),this._fetchWakeWords())}},{kind:"field",key:"_hasWakeWorkEntities",value:()=>(0,u.Z)((e=>Object.keys(e).some((e=>e.startsWith("wake_word.")))))},{kind:"method",key:"render",value:function(){const e=this._hasWakeWorkEntities(this.hass.states);return s.dy` <div class="section"> <div class="content"> <div class="intro"> <h3> ${this.hass.localize("ui.panel.config.voice_assistants.assistants.pipeline.detail.steps.wakeword.title")} </h3> <p> ${this.hass.localize("ui.panel.config.voice_assistants.assistants.pipeline.detail.steps.wakeword.description")} </p> </div> ${e?s.Ld:s.dy`${this.hass.localize("ui.panel.config.voice_assistants.assistants.pipeline.detail.steps.wakeword.no_wake_words")} <a href="${(0,g.R)(this.hass,"/docs/assist/")}" target="_blank" rel="noreferrer noopener">${this.hass.localize("ui.panel.config.voice_assistants.assistants.pipeline.detail.steps.wakeword.no_wake_words_link")}</a>`} <ha-form .schema="${this._schema(this._wakeWords)}" .data="${this.data}" .hass="${this.hass}" .computeLabel="${this._computeLabel}" .disabled="${!e}"></ha-form> </div> </div> `}},{kind:"method",key:"_fetchWakeWords",value:async function(){var e,t;if(this._wakeWords=void 0,null===(e=this.data)||void 0===e||!e.wake_word_entity)return;const i=this.data.wake_word_entity,a=await(s=this.hass,n=i,s.callWS({type:"wake_word/info",entity_id:n}));var s,n,d;this.data.wake_word_entity===i&&(this._wakeWords=a.wake_words,!this.data||null!==(t=this.data)&&void 0!==t&&t.wake_word_id&&this._wakeWords.some((e=>e.id===this.data.wake_word_id))||(0,o.B)(this,"value-changed",{value:{...this.data,wake_word_id:null===(d=this._wakeWords[0])||void 0===d?void 0:d.id}}))}},{kind:"get",static:!0,key:"styles",value:function(){return s.iv`.section{border:1px solid var(--divider-color);border-radius:8px}.content{padding:16px}.intro{margin-bottom:16px}h3{font-weight:400;font-size:22px;line-height:28px;margin-top:0;margin-bottom:4px}p{color:var(--secondary-text-color);font-size:var(--mdc-typography-body2-font-size, .875rem);margin-top:0;margin-bottom:0}a{color:var(--primary-color)}`}}]}}),s.oi);i(99057);let v=(0,a.Z)([(0,n.Mo)("dialog-voice-assistant-pipeline-detail")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.SB)()],key:"_params",value:void 0},{kind:"field",decorators:[(0,n.SB)()],key:"_data",value:void 0},{kind:"field",decorators:[(0,n.SB)()],key:"_preferred",value:void 0},{kind:"field",decorators:[(0,n.SB)()],key:"_cloudActive",value:void 0},{kind:"field",decorators:[(0,n.SB)()],key:"_error",value:void 0},{kind:"field",decorators:[(0,n.SB)()],key:"_submitting",value:()=>!1},{kind:"field",decorators:[(0,n.SB)()],key:"_supportedLanguages",value:void 0},{kind:"method",key:"showDialog",value:function(e){this._params=e,this._error=void 0,this._cloudActive=this._params.cloudActiveSubscription,this._params.pipeline?(this._data=this._params.pipeline,this._preferred=this._params.preferred):this._data={language:(this.hass.config.language||this.hass.locale.language).substring(0,2),stt_engine:this._cloudActive?"cloud":void 0,tts_engine:this._cloudActive?"cloud":void 0}}},{kind:"method",key:"closeDialog",value:function(){this._params=void 0,this._data=void 0,(0,o.B)(this,"dialog-closed",{dialog:this.localName})}},{kind:"method",key:"firstUpdated",value:function(){this._getSupportedLanguages()}},{kind:"method",key:"_getSupportedLanguages",value:async function(){const{languages:e}=await(0,c.Dy)(this.hass);this._supportedLanguages=e}},{kind:"method",key:"render",value:function(){var e,t,i,a;if(!this._params||!this._data)return s.Ld;const n=null!==(e=this._params.pipeline)&&void 0!==e&&e.id?this._params.pipeline.name:this.hass.localize("ui.panel.config.voice_assistants.assistants.pipeline.detail.add_assistant_title");return s.dy` <ha-dialog open @closed="${this.closeDialog}" scrimClickAction escapeKeyAction .heading="${n}"> <ha-dialog-header slot="heading"> <ha-icon-button slot="navigationIcon" dialogAction="cancel" .label="${this.hass.localize("ui.common.close")}" .path="${"M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z"}"></ha-icon-button> <span slot="title" .title="${n}">${n}</span> ${null!==(t=this._params.pipeline)&&void 0!==t&&t.id?s.dy` <ha-icon-button slot="actionItems" .label="${this.hass.localize("ui.panel.config.voice_assistants.assistants.pipeline.detail.set_as_preferred")}" .path="${this._preferred?"M12,17.27L18.18,21L16.54,13.97L22,9.24L14.81,8.62L12,2L9.19,8.62L2,9.24L7.45,13.97L5.82,21L12,17.27Z":"M12,15.39L8.24,17.66L9.23,13.38L5.91,10.5L10.29,10.13L12,6.09L13.71,10.13L18.09,10.5L14.77,13.38L15.76,17.66M22,9.24L14.81,8.63L12,2L9.19,8.63L2,9.24L7.45,13.97L5.82,21L12,17.27L18.18,21L16.54,13.97L22,9.24Z"}" @click="${this._setPreferred}" .disabled="${Boolean(this._preferred)}"></ha-icon-button> <ha-button-menu corner="BOTTOM_END" menuCorner="END" slot="actionItems" @closed="${d.U}" fixed> <ha-icon-button slot="trigger" .label="${this.hass.localize("ui.common.menu")}" .path="${"M12,16A2,2 0 0,1 14,18A2,2 0 0,1 12,20A2,2 0 0,1 10,18A2,2 0 0,1 12,16M12,10A2,2 0 0,1 14,12A2,2 0 0,1 12,14A2,2 0 0,1 10,12A2,2 0 0,1 12,10M12,4A2,2 0 0,1 14,6A2,2 0 0,1 12,8A2,2 0 0,1 10,6A2,2 0 0,1 12,4Z"}"></ha-icon-button> <ha-list-item graphic="icon" @request-selected="${this._debug}"> ${this.hass.localize("ui.panel.config.voice_assistants.assistants.pipeline.detail.debug")} <ha-svg-icon slot="graphic" .path="${"M14,12H10V10H14M14,16H10V14H14M20,8H17.19C16.74,7.22 16.12,6.55 15.37,6.04L17,4.41L15.59,3L13.42,5.17C12.96,5.06 12.5,5 12,5C11.5,5 11.04,5.06 10.59,5.17L8.41,3L7,4.41L8.62,6.04C7.88,6.55 7.26,7.22 6.81,8H4V10H6.09C6.04,10.33 6,10.66 6,11V12H4V14H6V15C6,15.34 6.04,15.67 6.09,16H4V18H6.81C7.85,19.79 9.78,21 12,21C14.22,21 16.15,19.79 17.19,18H20V16H17.91C17.96,15.67 18,15.34 18,15V14H20V12H18V11C18,10.66 17.96,10.33 17.91,10H20V8Z"}"></ha-svg-icon> </ha-list-item> </ha-button-menu> `:s.Ld} </ha-dialog-header> <div class="content"> ${this._error?s.dy`<ha-alert alert-type="error">${this._error}</ha-alert>`:s.Ld} <assist-pipeline-detail-config .hass="${this.hass}" .data="${this._data}" .supportedLanguages="${this._supportedLanguages}" keys="name,language" @value-changed="${this._valueChanged}" dialogInitialFocus></assist-pipeline-detail-config> <assist-pipeline-detail-conversation .hass="${this.hass}" .data="${this._data}" keys="conversation_engine,conversation_language" @value-changed="${this._valueChanged}"></assist-pipeline-detail-conversation> ${this._cloudActive||"cloud"!==this._data.tts_engine&&"cloud"!==this._data.stt_engine?s.Ld:s.dy` <ha-alert alert-type="warning"> ${this.hass.localize("ui.panel.config.voice_assistants.assistants.pipeline.detail.no_cloud_message")} <a href="/config/cloud" slot="action" @click="${this.closeDialog}"> <ha-button> ${this.hass.localize("ui.panel.config.voice_assistants.assistants.pipeline.detail.no_cloud_action")} </ha-button> </a> </ha-alert> `} <assist-pipeline-detail-stt .hass="${this.hass}" .data="${this._data}" keys="stt_engine,stt_language" @value-changed="${this._valueChanged}"></assist-pipeline-detail-stt> <assist-pipeline-detail-tts .hass="${this.hass}" .data="${this._data}" keys="tts_engine,tts_language,tts_voice" @value-changed="${this._valueChanged}"></assist-pipeline-detail-tts> <assist-pipeline-detail-wakeword .hass="${this.hass}" .data="${this._data}" keys="wake_word_entity,wake_word_id" @value-changed="${this._valueChanged}"></assist-pipeline-detail-wakeword> </div> ${null!==(i=this._params.pipeline)&&void 0!==i&&i.id?s.dy` <ha-button slot="secondaryAction" class="warning" .disabled="${this._preferred||this._submitting}" @click="${this._deletePipeline}"> ${this.hass.localize("ui.common.delete")} </ha-button> `:s.Ld} <ha-button slot="primaryAction" @click="${this._updatePipeline}" .disabled="${this._submitting}" dialogInitialFocus> ${null!==(a=this._params.pipeline)&&void 0!==a&&a.id?this.hass.localize("ui.panel.config.voice_assistants.assistants.pipeline.detail.update_assistant_action"):this.hass.localize("ui.panel.config.voice_assistants.assistants.pipeline.detail.add_assistant_action")} </ha-button> </ha-dialog> `}},{kind:"method",key:"_valueChanged",value:function(e){this._error=void 0;const t={};e.currentTarget.getAttribute("keys").split(",").forEach((i=>{t[i]=e.detail.value[i]})),this._data={...this._data,...t}}},{kind:"method",key:"_updatePipeline",value:async function(){this._submitting=!0;try{var e,t,i,a,s,n,o,d,l;const r=this._data,c={name:r.name,language:r.language,conversation_engine:r.conversation_engine,conversation_language:null!==(e=r.conversation_language)&&void 0!==e?e:null,stt_engine:null!==(t=r.stt_engine)&&void 0!==t?t:null,stt_language:null!==(i=r.stt_language)&&void 0!==i?i:null,tts_engine:null!==(a=r.tts_engine)&&void 0!==a?a:null,tts_language:null!==(s=r.tts_language)&&void 0!==s?s:null,tts_voice:null!==(n=r.tts_voice)&&void 0!==n?n:null,wake_word_entity:null!==(o=r.wake_word_entity)&&void 0!==o?o:null,wake_word_id:null!==(d=r.wake_word_id)&&void 0!==d?d:null};null!==(l=this._params.pipeline)&&void 0!==l&&l.id?await this._params.updatePipeline(c):await this._params.createPipeline(c),this.closeDialog()}catch(e){this._error=(null==e?void 0:e.message)||"Unknown error"}finally{this._submitting=!1}}},{kind:"method",key:"_setPreferred",value:async function(){this._submitting=!0;try{await this._params.setPipelinePreferred(),this._preferred=!0}catch(e){this._error=(null==e?void 0:e.message)||"Unknown error"}finally{this._submitting=!1}}},{kind:"method",key:"_debug",value:function(e){(0,l.Q)(e)&&((0,r.c)(`/config/voice-assistants/debug/${this._params.pipeline.id}`),this.closeDialog())}},{kind:"method",key:"_deletePipeline",value:async function(){this._submitting=!0;try{await this._params.deletePipeline()&&this.closeDialog()}catch(e){this._error=(null==e?void 0:e.message)||"Unknown error"}finally{this._submitting=!1}}},{kind:"get",static:!0,key:"styles",value:function(){return[h.yu,s.iv`.content>:not(:last-child){margin-bottom:16px;display:block}ha-alert{margin-bottom:16px;display:block}a{text-decoration:none}`]}}]}}),s.oi)},82160:(e,t,i)=>{function a(e){return new Promise(((t,i)=>{e.oncomplete=e.onsuccess=()=>t(e.result),e.onabort=e.onerror=()=>i(e.error)}))}function s(e,t){const i=indexedDB.open(e);i.onupgradeneeded=()=>i.result.createObjectStore(t);const s=a(i);return(e,i)=>s.then((a=>i(a.transaction(t,e).objectStore(t))))}let n;function o(){return n||(n=s("keyval-store","keyval")),n}function d(e,t=o()){return t("readonly",(t=>a(t.get(e))))}function l(e,t,i=o()){return i("readwrite",(i=>(i.put(t,e),a(i.transaction))))}function r(e=o()){return e("readwrite",(e=>(e.clear(),a(e.transaction))))}i.d(t,{MT:()=>s,RV:()=>a,U2:()=>d,ZH:()=>r,t8:()=>l})}};
//# sourceMappingURL=1650.Z9lMfFvXTxQ.js.map