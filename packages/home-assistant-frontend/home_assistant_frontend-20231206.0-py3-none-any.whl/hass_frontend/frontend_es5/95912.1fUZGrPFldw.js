/*! For license information please see 95912.1fUZGrPFldw.js.LICENSE.txt */
"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[95912],{67625:function(e,t,r){r.d(t,{s:function(){return x}});var o,i,a,n=r(71650),s=r(33368),l=r(34541),d=r(47838),c=r(69205),h=r(70906),u=(r(85717),r(43204)),p=r(96908),v=r(95260),f=r(88962),m=r(78220),_=r(82612),g=r(443),y=r(68144),k=r(83448),b=_.Vq?{passive:!0}:void 0,C=function(e){(0,c.Z)(r,e);var t=(0,h.Z)(r);function r(){var e;return(0,n.Z)(this,r),(e=t.apply(this,arguments)).centerTitle=!1,e.handleTargetScroll=function(){e.mdcFoundation.handleTargetScroll()},e.handleNavigationClick=function(){e.mdcFoundation.handleNavigationClick()},e}return(0,s.Z)(r,[{key:"scrollTarget",get:function(){return this._scrollTarget||window},set:function(e){this.unregisterScrollListener();var t=this.scrollTarget;this._scrollTarget=e,this.updateRootPosition(),this.requestUpdate("scrollTarget",t),this.registerScrollListener()}},{key:"updateRootPosition",value:function(){if(this.mdcRoot){var e=this.scrollTarget===window;this.mdcRoot.style.position=e?"":"absolute"}}},{key:"render",value:function(){var e=(0,y.dy)(o||(o=(0,f.Z)(['<span class="mdc-top-app-bar__title"><slot name="title"></slot></span>'])));return this.centerTitle&&(e=(0,y.dy)(i||(i=(0,f.Z)(['<section class="mdc-top-app-bar__section mdc-top-app-bar__section--align-center">',"</section>"])),e)),(0,y.dy)(a||(a=(0,f.Z)([' <header class="mdc-top-app-bar ','"> <div class="mdc-top-app-bar__row"> <section class="mdc-top-app-bar__section mdc-top-app-bar__section--align-start" id="navigation"> <slot name="navigationIcon" @click="','"></slot> '," </section> ",' <section class="mdc-top-app-bar__section mdc-top-app-bar__section--align-end" id="actions" role="toolbar"> <slot name="actionItems"></slot> </section> </div> </header> <div class="','"> <slot></slot> </div> '])),(0,k.$)(this.barClasses()),this.handleNavigationClick,this.centerTitle?null:e,this.centerTitle?e:null,(0,k.$)(this.contentClasses()))}},{key:"createAdapter",value:function(){var e=this;return Object.assign(Object.assign({},(0,m.q)(this.mdcRoot)),{setStyle:function(t,r){return e.mdcRoot.style.setProperty(t,r)},getTopAppBarHeight:function(){return e.mdcRoot.clientHeight},notifyNavigationIconClicked:function(){e.dispatchEvent(new Event(g.j2.NAVIGATION_EVENT,{bubbles:!0,cancelable:!0}))},getViewportScrollY:function(){return e.scrollTarget instanceof Window?e.scrollTarget.pageYOffset:e.scrollTarget.scrollTop},getTotalActionItems:function(){return e._actionItemsSlot.assignedNodes({flatten:!0}).length}})}},{key:"registerListeners",value:function(){this.registerScrollListener()}},{key:"unregisterListeners",value:function(){this.unregisterScrollListener()}},{key:"registerScrollListener",value:function(){this.scrollTarget.addEventListener("scroll",this.handleTargetScroll,b)}},{key:"unregisterScrollListener",value:function(){this.scrollTarget.removeEventListener("scroll",this.handleTargetScroll)}},{key:"firstUpdated",value:function(){(0,l.Z)((0,d.Z)(r.prototype),"firstUpdated",this).call(this),this.updateRootPosition(),this.registerListeners()}},{key:"disconnectedCallback",value:function(){(0,l.Z)((0,d.Z)(r.prototype),"disconnectedCallback",this).call(this),this.unregisterListeners()}}]),r}(m.H);(0,u.__decorate)([(0,v.IO)(".mdc-top-app-bar")],C.prototype,"mdcRoot",void 0),(0,u.__decorate)([(0,v.IO)('slot[name="actionItems"]')],C.prototype,"_actionItemsSlot",void 0),(0,u.__decorate)([(0,v.Cb)({type:Boolean})],C.prototype,"centerTitle",void 0),(0,u.__decorate)([(0,v.Cb)({type:Object})],C.prototype,"scrollTarget",null);var w=function(e){(0,c.Z)(r,e);var t=(0,h.Z)(r);function r(){var e;return(0,n.Z)(this,r),(e=t.apply(this,arguments)).mdcFoundationClass=p.Z,e.prominent=!1,e.dense=!1,e.handleResize=function(){e.mdcFoundation.handleWindowResize()},e}return(0,s.Z)(r,[{key:"barClasses",value:function(){return{"mdc-top-app-bar--dense":this.dense,"mdc-top-app-bar--prominent":this.prominent,"center-title":this.centerTitle}}},{key:"contentClasses",value:function(){return{"mdc-top-app-bar--fixed-adjust":!this.dense&&!this.prominent,"mdc-top-app-bar--dense-fixed-adjust":this.dense&&!this.prominent,"mdc-top-app-bar--prominent-fixed-adjust":!this.dense&&this.prominent,"mdc-top-app-bar--dense-prominent-fixed-adjust":this.dense&&this.prominent}}},{key:"registerListeners",value:function(){(0,l.Z)((0,d.Z)(r.prototype),"registerListeners",this).call(this),window.addEventListener("resize",this.handleResize,b)}},{key:"unregisterListeners",value:function(){(0,l.Z)((0,d.Z)(r.prototype),"unregisterListeners",this).call(this),window.removeEventListener("resize",this.handleResize)}}]),r}(C);(0,u.__decorate)([(0,v.Cb)({type:Boolean,reflect:!0})],w.prototype,"prominent",void 0),(0,u.__decorate)([(0,v.Cb)({type:Boolean,reflect:!0})],w.prototype,"dense",void 0);var Z=r(43419),x=function(e){(0,c.Z)(r,e);var t=(0,h.Z)(r);function r(){var e;return(0,n.Z)(this,r),(e=t.apply(this,arguments)).mdcFoundationClass=Z.Z,e}return(0,s.Z)(r,[{key:"barClasses",value:function(){return Object.assign(Object.assign({},(0,l.Z)((0,d.Z)(r.prototype),"barClasses",this).call(this)),{"mdc-top-app-bar--fixed":!0})}},{key:"registerListeners",value:function(){this.scrollTarget.addEventListener("scroll",this.handleTargetScroll,b)}},{key:"unregisterListeners",value:function(){this.scrollTarget.removeEventListener("scroll",this.handleTargetScroll)}}]),r}(w)},33753:function(e,t,r){var o,i=r(88962),a=r(53709),n=r(99312),s=r(81043),l=r(33368),d=r(71650),c=r(82390),h=r(69205),u=r(70906),p=r(91808),v=r(34541),f=r(47838),m=(r(97393),r(46798),r(94570),r(51358),r(47084),r(5239),r(98490),r(36513),r(51467),r(46349),r(70320),r(65974),r(76843),r(22859),r(91989),r(68144)),_=r(95260),g=r(14516),y=r(47181),k=r(32594),b=(r(81312),{key:"Mod-s",run:function(e){return(0,y.B)(e.dom,"editor-save"),!0}}),C=function(e){var t=document.createElement("ha-icon");return t.icon=e.label,t};(0,p.Z)([(0,_.Mo)("ha-code-editor")],(function(e,t){var p,w,Z=function(t){(0,h.Z)(o,t);var r=(0,u.Z)(o);function o(){var t;(0,d.Z)(this,o);for(var i=arguments.length,a=new Array(i),n=0;n<i;n++)a[n]=arguments[n];return t=r.call.apply(r,[this].concat(a)),e((0,c.Z)(t)),t}return(0,l.Z)(o)}(t);return{F:Z,d:[{kind:"field",key:"codemirror",value:void 0},{kind:"field",decorators:[(0,_.Cb)()],key:"mode",value:function(){return"yaml"}},{kind:"field",key:"hass",value:void 0},{kind:"field",decorators:[(0,_.Cb)({type:Boolean})],key:"autofocus",value:function(){return!1}},{kind:"field",decorators:[(0,_.Cb)({type:Boolean})],key:"readOnly",value:function(){return!1}},{kind:"field",decorators:[(0,_.Cb)({type:Boolean,attribute:"autocomplete-entities"})],key:"autocompleteEntities",value:function(){return!1}},{kind:"field",decorators:[(0,_.Cb)({type:Boolean,attribute:"autocomplete-icons"})],key:"autocompleteIcons",value:function(){return!1}},{kind:"field",decorators:[(0,_.Cb)({type:Boolean})],key:"error",value:function(){return!1}},{kind:"field",decorators:[(0,_.SB)()],key:"_value",value:function(){return""}},{kind:"field",key:"_loadedCodeMirror",value:void 0},{kind:"field",key:"_iconList",value:void 0},{kind:"set",key:"value",value:function(e){this._value=e}},{kind:"get",key:"value",value:function(){return this.codemirror?this.codemirror.state.doc.toString():this._value}},{kind:"get",key:"hasComments",value:function(){if(!this.codemirror||!this._loadedCodeMirror)return!1;var e=this._loadedCodeMirror.highlightingFor(this.codemirror.state,[this._loadedCodeMirror.tags.comment]);return!!this.renderRoot.querySelector("span.".concat(e))}},{kind:"method",key:"connectedCallback",value:function(){(0,v.Z)((0,f.Z)(Z.prototype),"connectedCallback",this).call(this),this.hasUpdated&&this.requestUpdate(),this.addEventListener("keydown",k.U),this.codemirror&&!1!==this.autofocus&&this.codemirror.focus()}},{kind:"method",key:"disconnectedCallback",value:function(){var e=this;(0,v.Z)((0,f.Z)(Z.prototype),"disconnectedCallback",this).call(this),this.removeEventListener("keydown",k.U),this.updateComplete.then((function(){e.codemirror.destroy(),delete e.codemirror}))}},{kind:"method",key:"scheduleUpdate",value:(w=(0,s.Z)((0,n.Z)().mark((function e(){var t;return(0,n.Z)().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:if(null===(t=this._loadedCodeMirror)||void 0===t){e.next=4;break}e.next=7;break;case 4:return e.next=6,Promise.all([r.e(96055),r.e(43642),r.e(85030),r.e(92914)]).then(r.bind(r,92914));case 6:this._loadedCodeMirror=e.sent;case 7:(0,v.Z)((0,f.Z)(Z.prototype),"scheduleUpdate",this).call(this);case 8:case"end":return e.stop()}}),e,this)}))),function(){return w.apply(this,arguments)})},{kind:"method",key:"update",value:function(e){if((0,v.Z)((0,f.Z)(Z.prototype),"update",this).call(this,e),this.codemirror){var t,r=[];if(e.has("mode")&&r.push({effects:this._loadedCodeMirror.langCompartment.reconfigure(this._mode)}),e.has("readOnly")&&r.push({effects:this._loadedCodeMirror.readonlyCompartment.reconfigure(this._loadedCodeMirror.EditorView.editable.of(!this.readOnly))}),e.has("_value")&&this._value!==this.value&&r.push({changes:{from:0,to:this.codemirror.state.doc.length,insert:this._value}}),r.length>0)(t=this.codemirror).dispatch.apply(t,r);e.has("error")&&this.classList.toggle("error-state",this.error)}else this._createCodeMirror()}},{kind:"get",key:"_mode",value:function(){return this._loadedCodeMirror.langs[this.mode]}},{kind:"method",key:"_createCodeMirror",value:function(){if(!this._loadedCodeMirror)throw new Error("Cannot create editor before CodeMirror is loaded");var e=[this._loadedCodeMirror.lineNumbers(),this._loadedCodeMirror.history(),this._loadedCodeMirror.drawSelection(),this._loadedCodeMirror.EditorState.allowMultipleSelections.of(!0),this._loadedCodeMirror.rectangularSelection(),this._loadedCodeMirror.crosshairCursor(),this._loadedCodeMirror.highlightSelectionMatches(),this._loadedCodeMirror.highlightActiveLine(),this._loadedCodeMirror.keymap.of([].concat((0,a.Z)(this._loadedCodeMirror.defaultKeymap),(0,a.Z)(this._loadedCodeMirror.searchKeymap),(0,a.Z)(this._loadedCodeMirror.historyKeymap),(0,a.Z)(this._loadedCodeMirror.tabKeyBindings),[b])),this._loadedCodeMirror.langCompartment.of(this._mode),this._loadedCodeMirror.haTheme,this._loadedCodeMirror.haSyntaxHighlighting,this._loadedCodeMirror.readonlyCompartment.of(this._loadedCodeMirror.EditorView.editable.of(!this.readOnly)),this._loadedCodeMirror.EditorView.updateListener.of(this._onUpdate)];if(!this.readOnly){var t=[];this.autocompleteEntities&&this.hass&&t.push(this._entityCompletions.bind(this)),this.autocompleteIcons&&t.push(this._mdiCompletions.bind(this)),t.length>0&&e.push(this._loadedCodeMirror.autocompletion({override:t,maxRenderedOptions:10}))}this.codemirror=new this._loadedCodeMirror.EditorView({state:this._loadedCodeMirror.EditorState.create({doc:this._value,extensions:e}),parent:this.renderRoot})}},{kind:"field",key:"_getStates",value:function(){return(0,g.Z)((function(e){return e?Object.keys(e).map((function(t){return{type:"variable",label:t,detail:e[t].attributes.friendly_name,info:"State: ".concat(e[t].state)}})):[]}))}},{kind:"method",key:"_entityCompletions",value:function(e){var t=e.matchBefore(/[a-z_]{3,}\.\w*/);if(!t||t.from===t.to&&!e.explicit)return null;var r=this._getStates(this.hass.states);return r&&r.length?{from:Number(t.from),options:r,validFor:/^[a-z_]{3,}\.\w*$/}:null}},{kind:"field",key:"_getIconItems",value:function(){var e=this;return(0,s.Z)((0,n.Z)().mark((function t(){var o;return(0,n.Z)().wrap((function(t){for(;;)switch(t.prev=t.next){case 0:if(e._iconList){t.next=9;break}t.next=5;break;case 5:return t.next=7,r.e(71639).then(r.t.bind(r,71639,19));case 7:o=t.sent.default;case 8:e._iconList=o.map((function(e){return{type:"variable",label:"mdi:".concat(e.name),detail:e.keywords.join(", "),info:C}}));case 9:return t.abrupt("return",e._iconList);case 10:case"end":return t.stop()}}),t)})))}},{kind:"method",key:"_mdiCompletions",value:(p=(0,s.Z)((0,n.Z)().mark((function e(t){var r,o;return(0,n.Z)().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:if((r=t.matchBefore(/mdi:\S*/))&&(r.from!==r.to||t.explicit)){e.next=3;break}return e.abrupt("return",null);case 3:return e.next=5,this._getIconItems();case 5:return o=e.sent,e.abrupt("return",{from:Number(r.from),options:o,validFor:/^mdi:\S*$/});case 7:case"end":return e.stop()}}),e,this)}))),function(e){return p.apply(this,arguments)})},{kind:"field",key:"_onUpdate",value:function(){var e=this;return function(t){t.docChanged&&(e._value=t.state.doc.toString(),(0,y.B)(e,"value-changed",{value:e._value}))}}},{kind:"get",static:!0,key:"styles",value:function(){return(0,m.iv)(o||(o=(0,i.Z)([":host(.error-state) .cm-gutters{border-color:var(--error-state-color,red)}"])))}}]}}),m.fl)},36226:function(e,t,r){var o,i=r(88962),a=r(33368),n=r(71650),s=r(82390),l=r(69205),d=r(70906),c=r(91808),h=(r(97393),r(67625)),u=r(71711),p=r(68144),v=r(95260);(0,c.Z)([(0,v.Mo)("ha-top-app-bar-fixed")],(function(e,t){var r=function(t){(0,l.Z)(o,t);var r=(0,d.Z)(o);function o(){var t;(0,n.Z)(this,o);for(var i=arguments.length,a=new Array(i),l=0;l<i;l++)a[l]=arguments[l];return t=r.call.apply(r,[this].concat(a)),e((0,s.Z)(t)),t}return(0,a.Z)(o)}(t);return{F:r,d:[{kind:"field",static:!0,key:"styles",value:function(){return[u.W,(0,p.iv)(o||(o=(0,i.Z)([".mdc-top-app-bar__row{height:var(--header-height);border-bottom:var(--app-header-border-bottom)}.mdc-top-app-bar--fixed-adjust{padding-top:var(--header-height)}.mdc-top-app-bar{--mdc-typography-headline6-font-weight:400;color:var(--app-header-text-color,var(--mdc-theme-on-primary,#fff));background-color:var(--app-header-background-color,var(--mdc-theme-primary))}"])))]}}]}}),h.s)},95912:function(e,t,r){r.r(t);var o,i,a=r(99312),n=r(81043),s=r(88962),l=r(33368),d=r(71650),c=r(82390),h=r(69205),u=r(70906),p=r(91808),v=r(34541),f=r(47838),m=(r(97393),r(43642)),_=(r(47704),r(77426)),g=r(68144),y=r(95260),k=r(83448),b=r(93088),C=r(36639),w=(r(31206),r(33753),r(10983),r(26765)),Z=r(11654),x=r(81796),L=(r(36226),r(36877)),M=(0,b.dt)({title:(0,b.jt)((0,b.Z_)()),views:(0,b.IX)((0,b.Ry)())}),S=(0,b.dt)({strategy:(0,b.dt)({type:(0,b.Z_)()})});(0,p.Z)([(0,y.Mo)("hui-editor")],(function(e,t){var r,p,T,E=function(t){(0,h.Z)(o,t);var r=(0,u.Z)(o);function o(){var t;(0,d.Z)(this,o);for(var i=arguments.length,a=new Array(i),n=0;n<i;n++)a[n]=arguments[n];return t=r.call.apply(r,[this].concat(a)),e((0,c.Z)(t)),t}return(0,l.Z)(o)}(t);return{F:E,d:[{kind:"field",decorators:[(0,y.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,y.Cb)({attribute:!1})],key:"lovelace",value:void 0},{kind:"field",decorators:[(0,y.Cb)()],key:"closeEditor",value:void 0},{kind:"field",decorators:[(0,y.SB)()],key:"_saving",value:void 0},{kind:"field",decorators:[(0,y.SB)()],key:"_changed",value:void 0},{kind:"method",key:"render",value:function(){return(0,g.dy)(o||(o=(0,s.Z)([' <ha-top-app-bar-fixed> <ha-icon-button slot="navigationIcon" .path="','" @click="','" .label="','"></ha-icon-button> <div slot="title"> ',' </div> <div slot="actionItems" class="save-button ','"> ',' </div> <mwc-button raised slot="actionItems" @click="','" .disabled="','">','</mwc-button> <div class="content"> <ha-code-editor mode="yaml" autofocus autocomplete-entities autocomplete-icons .hass="','" @value-changed="','" @editor-save="','" dir="ltr"> </ha-code-editor> </div> </ha-top-app-bar-fixed> '])),"M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z",this._closeEditor,this.hass.localize("ui.common.close"),this.hass.localize("ui.panel.lovelace.editor.raw_editor.header"),(0,k.$)({saved:!1===this._saving||!0===this._changed}),this._changed?this.hass.localize("ui.panel.lovelace.editor.raw_editor.unsaved_changes"):this.hass.localize("ui.panel.lovelace.editor.raw_editor.saved"),this._handleSave,!this._changed,this.hass.localize("ui.panel.lovelace.editor.raw_editor.save"),this.hass,this._yamlChanged,this._handleSave)}},{kind:"method",key:"firstUpdated",value:function(e){(0,v.Z)((0,f.Z)(E.prototype),"firstUpdated",this).call(this,e),this.yamlEditor.value=(0,_.dump)(this.lovelace.rawConfig)}},{kind:"method",key:"updated",value:function(e){var t=this,r=e.get("lovelace");!this._saving&&r&&this.lovelace&&r.rawConfig!==this.lovelace.rawConfig&&!(0,C.v)(r.rawConfig,this.lovelace.rawConfig)&&(0,x.C)(this,{message:this.hass.localize("ui.panel.lovelace.editor.raw_editor.lovelace_changed"),action:{action:function(){t.yamlEditor.value=(0,_.dump)(t.lovelace.rawConfig)},text:this.hass.localize("ui.panel.lovelace.editor.raw_editor.reload")},duration:0,dismissable:!1})}},{kind:"get",static:!0,key:"styles",value:function(){return[Z.Qx,(0,g.iv)(i||(i=(0,s.Z)([":host{--code-mirror-height:100%;--app-header-background-color:var(\n            --app-header-edit-background-color,\n            #455a64\n          );--app-header-text-color:var(--app-header-edit-text-color, #fff)}mwc-button[disabled]{background-color:var(--mdc-theme-on-primary);border-radius:4px}.content{height:calc(100vh - var(--header-height))}.comments{font-size:16px}.save-button{opacity:0;font-size:14px;padding:0px 10px}.saved{opacity:1}"])))]}},{kind:"method",key:"_yamlChanged",value:function(){this._changed=(0,m.of)(this.yamlEditor.codemirror.state)>0,this._changed&&!window.onbeforeunload?window.onbeforeunload=function(){return!0}:!this._changed&&window.onbeforeunload&&(window.onbeforeunload=null)}},{kind:"method",key:"_closeEditor",value:(T=(0,n.Z)((0,a.Z)().mark((function e(){return(0,a.Z)().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:if(e.t0=this._changed,!e.t0){e.next=5;break}return e.next=4,(0,w.showConfirmationDialog)(this,{text:this.hass.localize("ui.panel.lovelace.editor.raw_editor.confirm_unsaved_changes"),dismissText:this.hass.localize("ui.common.stay"),confirmText:this.hass.localize("ui.common.leave")});case 4:e.t0=!e.sent;case 5:if(!e.t0){e.next=7;break}return e.abrupt("return");case 7:window.onbeforeunload=null,this.closeEditor&&this.closeEditor();case 9:case"end":return e.stop()}}),e,this)}))),function(){return T.apply(this,arguments)})},{kind:"method",key:"_removeConfig",value:(p=(0,n.Z)((0,a.Z)().mark((function e(){return(0,a.Z)().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.prev=0,e.next=3,this.lovelace.deleteConfig();case 3:e.next=8;break;case 5:e.prev=5,e.t0=e.catch(0),(0,w.showAlertDialog)(this,{text:this.hass.localize("ui.panel.lovelace.editor.raw_editor.error_remove",{error:e.t0})});case 8:window.onbeforeunload=null,this.closeEditor&&this.closeEditor();case 10:case"end":return e.stop()}}),e,this,[[0,5]])}))),function(){return p.apply(this,arguments)})},{kind:"method",key:"_handleSave",value:(r=(0,n.Z)((0,a.Z)().mark((function e(){var t,r,o=this;return(0,a.Z)().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:if(this._saving=!0,t=this.yamlEditor.value){e.next=5;break}return(0,w.showConfirmationDialog)(this,{title:this.hass.localize("ui.panel.lovelace.editor.raw_editor.confirm_remove_config_title"),text:this.hass.localize("ui.panel.lovelace.editor.raw_editor.confirm_remove_config_text"),confirmText:this.hass.localize("ui.common.remove"),dismissText:this.hass.localize("ui.common.cancel"),confirm:function(){return o._removeConfig()}}),e.abrupt("return");case 5:if(!this.yamlEditor.hasComments){e.next=8;break}if(confirm(this.hass.localize("ui.panel.lovelace.editor.raw_editor.confirm_unsaved_comments"))){e.next=8;break}return e.abrupt("return");case 8:e.prev=8,r=(0,_.load)(t),e.next=17;break;case 12:return e.prev=12,e.t0=e.catch(8),(0,w.showAlertDialog)(this,{text:this.hass.localize("ui.panel.lovelace.editor.raw_editor.error_parse_yaml",{error:e.t0})}),this._saving=!1,e.abrupt("return");case 17:e.prev=17,(0,L.Tx)(r)?(0,b.hu)(r,S):(0,b.hu)(r,M),e.next=25;break;case 21:return e.prev=21,e.t1=e.catch(17),(0,w.showAlertDialog)(this,{text:this.hass.localize("ui.panel.lovelace.editor.raw_editor.error_invalid_config",{error:e.t1})}),e.abrupt("return");case 25:return r.resources&&(0,w.showAlertDialog)(this,{text:this.hass.localize("ui.panel.lovelace.editor.raw_editor.resources_moved")}),e.prev=26,e.next=29,this.lovelace.saveConfig(r);case 29:e.next=34;break;case 31:e.prev=31,e.t2=e.catch(26),(0,w.showAlertDialog)(this,{text:this.hass.localize("ui.panel.lovelace.editor.raw_editor.error_save_yaml",{error:e.t2})});case 34:window.onbeforeunload=null,this._changed=!1,this._saving=!1;case 37:case"end":return e.stop()}}),e,this,[[8,12],[17,21],[26,31]])}))),function(){return r.apply(this,arguments)})},{kind:"get",key:"yamlEditor",value:function(){return this.shadowRoot.querySelector("ha-code-editor")}}]}}),g.oi)}}]);
//# sourceMappingURL=95912.1fUZGrPFldw.js.map