"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[67901],{69470:function(e,t,n){n.d(t,{$y:function(){return o},fs:function(){return a},j:function(){return i}});n(46798),n(47084);var r=function(e,t,n){return new Promise((function(r,i){var a=document.createElement(e),o="src",l="body";switch(a.onload=function(){return r(t)},a.onerror=function(){return i(t)},e){case"script":a.async=!0,n&&(a.type=n);break;case"link":a.type="text/css",a.rel="stylesheet",o="href",l="head"}a[o]=t,document[l].appendChild(a)}))},i=function(e){return r("link",e)},a=function(e){return r("script",e)},o=function(e){return r("script",e,"module")}},67901:function(e,t,n){n.r(t),n.d(t,{HaPanelCustom:function(){return w}});var r=n(40039),i=n(33368),a=n(71650),o=n(82390),l=n(69205),s=n(70906),u=n(91808),c=n(34541),d=n(47838),h=(n(97393),n(51358),n(46798),n(98490),n(40271),n(60163),n(22859),n(11451),n(68144)),f=n(95260),p=n(83849),m=n(36639),v=(n(47084),n(69470)),k={},y=function(e){return e.html_url?{type:"html",url:e.html_url}:e.module_url&&e.js_url?{type:"js",url:e.js_url}:e.module_url?{type:"module",url:e.module_url}:{type:"js",url:e.js_url}},_=(n(9849),n(50289),n(94167),n(65974),function(e,t){"setProperties"in e?e.setProperties(t):Object.keys(t).forEach((function(n){e[n]=t[n]}))}),w=(0,u.Z)(null,(function(e,t){var n=function(t){(0,l.Z)(r,t);var n=(0,s.Z)(r);function r(){var t;(0,a.Z)(this,r);for(var i=arguments.length,l=new Array(i),s=0;s<i;s++)l[s]=arguments[s];return t=n.call.apply(n,[this].concat(l)),e((0,o.Z)(t)),t}return(0,i.Z)(r)}(t);return{F:n,d:[{kind:"field",decorators:[(0,f.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,f.Cb)()],key:"narrow",value:void 0},{kind:"field",decorators:[(0,f.Cb)()],key:"route",value:void 0},{kind:"field",decorators:[(0,f.Cb)()],key:"panel",value:void 0},{kind:"field",key:"_setProperties",value:void 0},{kind:"method",key:"createRenderRoot",value:function(){return this}},{kind:"field",key:"navigate",value:function(){return function(e,t){return(0,p.c)(e,t)}}},{kind:"method",key:"registerIframe",value:function(e,t){e(this.panel,{hass:this.hass,narrow:this.narrow,route:this.route}),this._setProperties=t}},{kind:"method",key:"disconnectedCallback",value:function(){(0,c.Z)((0,d.Z)(n.prototype),"disconnectedCallback",this).call(this),this._cleanupPanel()}},{kind:"method",key:"update",value:function(e){if((0,c.Z)((0,d.Z)(n.prototype),"update",this).call(this,e),e.has("panel")){var t=e.get("panel");if(!(0,m.v)(t,this.panel))return t&&this._cleanupPanel(),void this._createPanel(this.panel)}if(this._setProperties){var i,a={},o=(0,r.Z)(e.keys());try{for(o.s();!(i=o.n()).done;){var l=i.value;a[l]=this[l]}}catch(s){o.e(s)}finally{o.f()}this._setProperties(a)}}},{kind:"method",key:"_cleanupPanel",value:function(){for(delete window.customPanel,this._setProperties=void 0;this.lastChild;)this.removeChild(this.lastChild)}},{kind:"method",key:"_createPanel",value:function(e){var t=this,n=e.config._panel_custom,r=y(n),i=document.createElement("a");if(i.href=r.url,n.trust_external||["localhost","127.0.0.1",location.hostname].includes(i.hostname)||confirm("".concat(this.hass.localize("ui.panel.custom.external_panel.question_trust",{name:n.name,link:i.href}),"\n\n           ").concat(this.hass.localize("ui.panel.custom.external_panel.complete_access"),"\n\n           (").concat(this.hass.localize("ui.panel.custom.external_panel.hide_message"),")")))if(n.embed_iframe){var a,o;window.customPanel=this;var l=this.panel.title?'title="'.concat(this.panel.title,'"'):"";this.innerHTML="\n      <style>\n        iframe {\n          border: 0;\n          width: 100%;\n          height: 100%;\n          display: block;\n          background-color: var(--primary-background-color);\n        }\n      </style>\n      <iframe ".concat(l,"></iframe>").trim();var s=this.querySelector("iframe").contentWindow.document;s.open(),s.write("<!doctype html><script src='".concat(window.customPanelJS,"'><\/script>")),s.close()}else(a=n,o=y(a),"js"===o.type?(o.url in k||(k[o.url]=(0,v.fs)(o.url)),k[o.url]):"module"===o.type?(0,v.$y)(o.url):Promise.reject("No valid url found in panel config.")).then((function(){var r=function(e){var t="html_url"in e?"ha-panel-".concat(e.name):e.name;return document.createElement(t)}(n);t._setProperties=function(e){return _(r,e)},_(r,{panel:e,hass:t.hass,narrow:t.narrow,route:t.route}),t.appendChild(r)}),(function(){alert("Unable to load custom panel from ".concat(i.href))}))}}]}}),h.fl);customElements.define("ha-panel-custom",w)}}]);
//# sourceMappingURL=67901.m8IQLVQTyfc.js.map