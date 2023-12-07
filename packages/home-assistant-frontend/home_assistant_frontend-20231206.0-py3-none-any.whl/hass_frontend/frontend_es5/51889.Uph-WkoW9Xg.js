"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[51889],{32594:function(e,t,r){r.d(t,{U:function(){return o}});var o=function(e){return e.stopPropagation()}},33753:function(e,t,r){var o,n=r(88962),i=r(53709),a=r(99312),d=r(81043),s=r(33368),l=r(71650),u=r(82390),c=r(69205),h=r(70906),f=r(91808),v=r(34541),p=r(47838),m=(r(97393),r(46798),r(94570),r(51358),r(47084),r(5239),r(98490),r(36513),r(51467),r(46349),r(70320),r(65974),r(76843),r(22859),r(91989),r(68144)),k=r(95260),y=r(14516),_=r(47181),C=r(32594),b=(r(81312),{key:"Mod-s",run:function(e){return(0,_.B)(e.dom,"editor-save"),!0}}),g=function(e){var t=document.createElement("ha-icon");return t.icon=e.label,t};(0,f.Z)([(0,k.Mo)("ha-code-editor")],(function(e,t){var f,Z,M=function(t){(0,c.Z)(o,t);var r=(0,h.Z)(o);function o(){var t;(0,l.Z)(this,o);for(var n=arguments.length,i=new Array(n),a=0;a<n;a++)i[a]=arguments[a];return t=r.call.apply(r,[this].concat(i)),e((0,u.Z)(t)),t}return(0,s.Z)(o)}(t);return{F:M,d:[{kind:"field",key:"codemirror",value:void 0},{kind:"field",decorators:[(0,k.Cb)()],key:"mode",value:function(){return"yaml"}},{kind:"field",key:"hass",value:void 0},{kind:"field",decorators:[(0,k.Cb)({type:Boolean})],key:"autofocus",value:function(){return!1}},{kind:"field",decorators:[(0,k.Cb)({type:Boolean})],key:"readOnly",value:function(){return!1}},{kind:"field",decorators:[(0,k.Cb)({type:Boolean,attribute:"autocomplete-entities"})],key:"autocompleteEntities",value:function(){return!1}},{kind:"field",decorators:[(0,k.Cb)({type:Boolean,attribute:"autocomplete-icons"})],key:"autocompleteIcons",value:function(){return!1}},{kind:"field",decorators:[(0,k.Cb)({type:Boolean})],key:"error",value:function(){return!1}},{kind:"field",decorators:[(0,k.SB)()],key:"_value",value:function(){return""}},{kind:"field",key:"_loadedCodeMirror",value:void 0},{kind:"field",key:"_iconList",value:void 0},{kind:"set",key:"value",value:function(e){this._value=e}},{kind:"get",key:"value",value:function(){return this.codemirror?this.codemirror.state.doc.toString():this._value}},{kind:"get",key:"hasComments",value:function(){if(!this.codemirror||!this._loadedCodeMirror)return!1;var e=this._loadedCodeMirror.highlightingFor(this.codemirror.state,[this._loadedCodeMirror.tags.comment]);return!!this.renderRoot.querySelector("span.".concat(e))}},{kind:"method",key:"connectedCallback",value:function(){(0,v.Z)((0,p.Z)(M.prototype),"connectedCallback",this).call(this),this.hasUpdated&&this.requestUpdate(),this.addEventListener("keydown",C.U),this.codemirror&&!1!==this.autofocus&&this.codemirror.focus()}},{kind:"method",key:"disconnectedCallback",value:function(){var e=this;(0,v.Z)((0,p.Z)(M.prototype),"disconnectedCallback",this).call(this),this.removeEventListener("keydown",C.U),this.updateComplete.then((function(){e.codemirror.destroy(),delete e.codemirror}))}},{kind:"method",key:"scheduleUpdate",value:(Z=(0,d.Z)((0,a.Z)().mark((function e(){var t;return(0,a.Z)().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:if(null===(t=this._loadedCodeMirror)||void 0===t){e.next=4;break}e.next=7;break;case 4:return e.next=6,Promise.all([r.e(96055),r.e(43642),r.e(85030),r.e(92914)]).then(r.bind(r,92914));case 6:this._loadedCodeMirror=e.sent;case 7:(0,v.Z)((0,p.Z)(M.prototype),"scheduleUpdate",this).call(this);case 8:case"end":return e.stop()}}),e,this)}))),function(){return Z.apply(this,arguments)})},{kind:"method",key:"update",value:function(e){if((0,v.Z)((0,p.Z)(M.prototype),"update",this).call(this,e),this.codemirror){var t,r=[];if(e.has("mode")&&r.push({effects:this._loadedCodeMirror.langCompartment.reconfigure(this._mode)}),e.has("readOnly")&&r.push({effects:this._loadedCodeMirror.readonlyCompartment.reconfigure(this._loadedCodeMirror.EditorView.editable.of(!this.readOnly))}),e.has("_value")&&this._value!==this.value&&r.push({changes:{from:0,to:this.codemirror.state.doc.length,insert:this._value}}),r.length>0)(t=this.codemirror).dispatch.apply(t,r);e.has("error")&&this.classList.toggle("error-state",this.error)}else this._createCodeMirror()}},{kind:"get",key:"_mode",value:function(){return this._loadedCodeMirror.langs[this.mode]}},{kind:"method",key:"_createCodeMirror",value:function(){if(!this._loadedCodeMirror)throw new Error("Cannot create editor before CodeMirror is loaded");var e=[this._loadedCodeMirror.lineNumbers(),this._loadedCodeMirror.history(),this._loadedCodeMirror.drawSelection(),this._loadedCodeMirror.EditorState.allowMultipleSelections.of(!0),this._loadedCodeMirror.rectangularSelection(),this._loadedCodeMirror.crosshairCursor(),this._loadedCodeMirror.highlightSelectionMatches(),this._loadedCodeMirror.highlightActiveLine(),this._loadedCodeMirror.keymap.of([].concat((0,i.Z)(this._loadedCodeMirror.defaultKeymap),(0,i.Z)(this._loadedCodeMirror.searchKeymap),(0,i.Z)(this._loadedCodeMirror.historyKeymap),(0,i.Z)(this._loadedCodeMirror.tabKeyBindings),[b])),this._loadedCodeMirror.langCompartment.of(this._mode),this._loadedCodeMirror.haTheme,this._loadedCodeMirror.haSyntaxHighlighting,this._loadedCodeMirror.readonlyCompartment.of(this._loadedCodeMirror.EditorView.editable.of(!this.readOnly)),this._loadedCodeMirror.EditorView.updateListener.of(this._onUpdate)];if(!this.readOnly){var t=[];this.autocompleteEntities&&this.hass&&t.push(this._entityCompletions.bind(this)),this.autocompleteIcons&&t.push(this._mdiCompletions.bind(this)),t.length>0&&e.push(this._loadedCodeMirror.autocompletion({override:t,maxRenderedOptions:10}))}this.codemirror=new this._loadedCodeMirror.EditorView({state:this._loadedCodeMirror.EditorState.create({doc:this._value,extensions:e}),parent:this.renderRoot})}},{kind:"field",key:"_getStates",value:function(){return(0,y.Z)((function(e){return e?Object.keys(e).map((function(t){return{type:"variable",label:t,detail:e[t].attributes.friendly_name,info:"State: ".concat(e[t].state)}})):[]}))}},{kind:"method",key:"_entityCompletions",value:function(e){var t=e.matchBefore(/[a-z_]{3,}\.\w*/);if(!t||t.from===t.to&&!e.explicit)return null;var r=this._getStates(this.hass.states);return r&&r.length?{from:Number(t.from),options:r,validFor:/^[a-z_]{3,}\.\w*$/}:null}},{kind:"field",key:"_getIconItems",value:function(){var e=this;return(0,d.Z)((0,a.Z)().mark((function t(){var o;return(0,a.Z)().wrap((function(t){for(;;)switch(t.prev=t.next){case 0:if(e._iconList){t.next=9;break}t.next=5;break;case 5:return t.next=7,r.e(71639).then(r.t.bind(r,71639,19));case 7:o=t.sent.default;case 8:e._iconList=o.map((function(e){return{type:"variable",label:"mdi:".concat(e.name),detail:e.keywords.join(", "),info:g}}));case 9:return t.abrupt("return",e._iconList);case 10:case"end":return t.stop()}}),t)})))}},{kind:"method",key:"_mdiCompletions",value:(f=(0,d.Z)((0,a.Z)().mark((function e(t){var r,o;return(0,a.Z)().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:if((r=t.matchBefore(/mdi:\S*/))&&(r.from!==r.to||t.explicit)){e.next=3;break}return e.abrupt("return",null);case 3:return e.next=5,this._getIconItems();case 5:return o=e.sent,e.abrupt("return",{from:Number(r.from),options:o,validFor:/^mdi:\S*$/});case 7:case"end":return e.stop()}}),e,this)}))),function(e){return f.apply(this,arguments)})},{kind:"field",key:"_onUpdate",value:function(){var e=this;return function(t){t.docChanged&&(e._value=t.state.doc.toString(),(0,_.B)(e,"value-changed",{value:e._value}))}}},{kind:"get",static:!0,key:"styles",value:function(){return(0,m.iv)(o||(o=(0,n.Z)([":host(.error-state) .cm-gutters{border-color:var(--error-state-color,red)}"])))}}]}}),m.fl)},16235:function(e,t,r){var o,n,i=r(88962),a=r(33368),d=r(71650),s=r(82390),l=r(69205),u=r(70906),c=r(91808),h=(r(97393),r(68144)),f=r(95260);(0,c.Z)([(0,f.Mo)("ha-input-helper-text")],(function(e,t){var r=function(t){(0,l.Z)(o,t);var r=(0,u.Z)(o);function o(){var t;(0,d.Z)(this,o);for(var n=arguments.length,i=new Array(n),a=0;a<n;a++)i[a]=arguments[a];return t=r.call.apply(r,[this].concat(i)),e((0,s.Z)(t)),t}return(0,a.Z)(o)}(t);return{F:r,d:[{kind:"method",key:"render",value:function(){return(0,h.dy)(o||(o=(0,i.Z)(["<slot></slot>"])))}},{kind:"field",static:!0,key:"styles",value:function(){return(0,h.iv)(n||(n=(0,i.Z)([":host{display:block;color:var(--mdc-text-field-label-ink-color,rgba(0,0,0,.6));font-size:.75rem;padding-left:16px;padding-right:16px}"])))}}]}}),h.oi)},56097:function(e,t,r){r.r(t),r.d(t,{HaTemplateSelector:function(){return k}});var o,n,i,a,d=r(88962),s=r(33368),l=r(71650),u=r(82390),c=r(69205),h=r(70906),f=r(91808),v=(r(97393),r(68144)),p=r(95260),m=r(47181),k=(r(33753),r(16235),(0,f.Z)([(0,p.Mo)("ha-selector-template")],(function(e,t){var r=function(t){(0,c.Z)(o,t);var r=(0,h.Z)(o);function o(){var t;(0,l.Z)(this,o);for(var n=arguments.length,i=new Array(n),a=0;a<n;a++)i[a]=arguments[a];return t=r.call.apply(r,[this].concat(i)),e((0,u.Z)(t)),t}return(0,s.Z)(o)}(t);return{F:r,d:[{kind:"field",decorators:[(0,p.Cb)()],key:"hass",value:void 0},{kind:"field",decorators:[(0,p.Cb)()],key:"value",value:void 0},{kind:"field",decorators:[(0,p.Cb)()],key:"label",value:void 0},{kind:"field",decorators:[(0,p.Cb)()],key:"helper",value:void 0},{kind:"field",decorators:[(0,p.Cb)({type:Boolean})],key:"disabled",value:function(){return!1}},{kind:"field",decorators:[(0,p.Cb)({type:Boolean})],key:"required",value:function(){return!0}},{kind:"method",key:"render",value:function(){return(0,v.dy)(o||(o=(0,d.Z)([" ",' <ha-code-editor mode="jinja2" .hass="','" .value="','" .readOnly="','" autofocus autocomplete-entities autocomplete-icons @value-changed="','" dir="ltr"></ha-code-editor> '," "])),this.label?(0,v.dy)(n||(n=(0,d.Z)(["<p>","","</p>"])),this.label,this.required?"*":""):"",this.hass,this.value,this.disabled,this._handleChange,this.helper?(0,v.dy)(i||(i=(0,d.Z)(["<ha-input-helper-text>","</ha-input-helper-text>"])),this.helper):"")}},{kind:"method",key:"_handleChange",value:function(e){var t=e.target.value;this.value!==t&&(0,m.B)(this,"value-changed",{value:t})}},{kind:"get",static:!0,key:"styles",value:function(){return(0,v.iv)(a||(a=(0,d.Z)(["p{margin-top:0}"])))}}]}}),v.oi))},82160:function(e,t,r){r.d(t,{MT:function(){return i},RV:function(){return n},U2:function(){return d},ZH:function(){return l},t8:function(){return s}});var o;r(68990),r(46798),r(47084),r(9849),r(50289),r(94167),r(51358),r(5239),r(98490),r(46349),r(70320),r(36513);function n(e){return new Promise((function(t,r){e.oncomplete=e.onsuccess=function(){return t(e.result)},e.onabort=e.onerror=function(){return r(e.error)}}))}function i(e,t){var r=indexedDB.open(e);r.onupgradeneeded=function(){return r.result.createObjectStore(t)};var o=n(r);return function(e,r){return o.then((function(o){return r(o.transaction(t,e).objectStore(t))}))}}function a(){return o||(o=i("keyval-store","keyval")),o}function d(e){return(arguments.length>1&&void 0!==arguments[1]?arguments[1]:a())("readonly",(function(t){return n(t.get(e))}))}function s(e,t){return(arguments.length>2&&void 0!==arguments[2]?arguments[2]:a())("readwrite",(function(r){return r.put(t,e),n(r.transaction)}))}function l(){return(arguments.length>0&&void 0!==arguments[0]?arguments[0]:a())("readwrite",(function(e){return e.clear(),n(e.transaction)}))}}}]);
//# sourceMappingURL=51889.Uph-WkoW9Xg.js.map