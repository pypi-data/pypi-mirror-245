"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[22115],{55642:function(e,t,n){n.d(t,{h:function(){return u}});var a=n(68990),i=n(71650),r=n(33368),o=n(69205),l=n(70906),c=(n(51467),n(46798),n(9849),n(50289),n(94167),n(82073),n(68144)),s=n(57835),u=(0,s.XM)(function(e){(0,o.Z)(n,e);var t=(0,l.Z)(n);function n(e){var a;if((0,i.Z)(this,n),(a=t.call(this,e))._element=void 0,e.type!==s.pX.CHILD)throw new Error("dynamicElementDirective can only be used in content bindings");return a}return(0,r.Z)(n,[{key:"update",value:function(e,t){var n=this,i=(0,a.Z)(t,2),r=i[0],o=i[1];return this._element&&this._element.localName===r?(o&&Object.entries(o).forEach((function(e){var t=(0,a.Z)(e,2),i=t[0],r=t[1];n._element[i]=r})),c.Jb):this.render(r,o)}},{key:"render",value:function(e,t){var n=this;return this._element=document.createElement(e),t&&Object.entries(t).forEach((function(e){var t=(0,a.Z)(e,2),i=t[0],r=t[1];n._element[i]=r})),this._element}}]),n}(s.Xe))},97345:function(e,t,n){n.r(t),n.d(t,{HuiGaugeCardEditor:function(){return Z}});var a,i=n(88962),r=n(53709),o=n(33368),l=n(71650),c=n(82390),s=n(69205),u=n(70906),d=n(91808),m=(n(97393),n(85717),n(22859),n(68144)),h=n(95260),v=n(14516),y=n(93088),f=n(47181),g=(n(68331),n(98346)),_=n(43283),p=(0,y.Ry)({from:(0,y.Rx)(),color:(0,y.Z_)(),label:(0,y.jt)((0,y.Z_)())}),b=(0,y.f0)(g.I,(0,y.Ry)({name:(0,y.jt)((0,y.Z_)()),entity:(0,y.jt)((0,y.Z_)()),unit:(0,y.jt)((0,y.Z_)()),min:(0,y.jt)((0,y.Rx)()),max:(0,y.jt)((0,y.Rx)()),severity:(0,y.jt)((0,y.Ry)()),theme:(0,y.jt)((0,y.Z_)()),needle:(0,y.jt)((0,y.O7)()),segments:(0,y.jt)((0,y.IX)(p))})),Z=(0,d.Z)([(0,h.Mo)("hui-gauge-card-editor")],(function(e,t){var n=function(t){(0,s.Z)(a,t);var n=(0,u.Z)(a);function a(){var t;(0,l.Z)(this,a);for(var i=arguments.length,r=new Array(i),o=0;o<i;o++)r[o]=arguments[o];return t=n.call.apply(n,[this].concat(r)),e((0,c.Z)(t)),t}return(0,o.Z)(a)}(t);return{F:n,d:[{kind:"field",decorators:[(0,h.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,h.SB)()],key:"_config",value:void 0},{kind:"method",key:"setConfig",value:function(e){(0,y.hu)(e,b),this._config=e}},{kind:"field",key:"_schema",value:function(){return(0,v.Z)((function(e){return[{name:"entity",selector:{entity:{domain:["counter","input_number","number","sensor"]}}},{name:"",type:"grid",schema:[{name:"name",selector:{text:{}}},{name:"unit",selector:{text:{}}}]},{name:"theme",selector:{theme:{}}},{name:"",type:"grid",schema:[{name:"min",default:_.DEFAULT_MIN,selector:{number:{mode:"box",step:"any"}}},{name:"max",default:_.DEFAULT_MAX,selector:{number:{mode:"box",step:"any"}}}]},{name:"",type:"grid",schema:[{name:"needle",selector:{boolean:{}}},{name:"show_severity",selector:{boolean:{}}}]}].concat((0,r.Z)(e?[{name:"severity",type:"grid",schema:[{name:"green",selector:{number:{mode:"box",step:"any"}}},{name:"yellow",selector:{number:{mode:"box",step:"any"}}},{name:"red",selector:{number:{mode:"box",step:"any"}}}]}]:[]))}))}},{kind:"method",key:"render",value:function(){if(!this.hass||!this._config)return m.Ld;var e=this._schema(void 0!==this._config.severity),t=Object.assign({show_severity:void 0!==this._config.severity},this._config);return(0,m.dy)(a||(a=(0,i.Z)([' <ha-form .hass="','" .data="','" .schema="','" .computeLabel="','" @value-changed="','"></ha-form> '])),this.hass,t,e,this._computeLabelCallback,this._valueChanged)}},{kind:"method",key:"_valueChanged",value:function(e){var t,n,a,i=e.detail.value;i.show_severity?i=Object.assign(Object.assign({},i),{},{severity:{green:i.green||(null===(t=i.severity)||void 0===t?void 0:t.green)||0,yellow:i.yellow||(null===(n=i.severity)||void 0===n?void 0:n.yellow)||0,red:i.red||(null===(a=i.severity)||void 0===a?void 0:a.red)||0}}):!i.show_severity&&i.severity&&delete i.severity;delete i.show_severity,delete i.green,delete i.yellow,delete i.red,(0,f.B)(this,"config-changed",{config:i})}},{kind:"field",key:"_computeLabelCallback",value:function(){var e=this;return function(t){switch(t.name){case"name":return e.hass.localize("ui.panel.lovelace.editor.card.generic.name");case"entity":return"".concat(e.hass.localize("ui.panel.lovelace.editor.card.generic.entity")," (").concat(e.hass.localize("ui.panel.lovelace.editor.card.config.required"),")");case"max":return e.hass.localize("ui.panel.lovelace.editor.card.generic.maximum");case"min":return e.hass.localize("ui.panel.lovelace.editor.card.generic.minimum");case"show_severity":return e.hass.localize("ui.panel.lovelace.editor.card.gauge.severity.define");case"needle":return e.hass.localize("ui.panel.lovelace.editor.card.gauge.needle_gauge");case"theme":return"".concat(e.hass.localize("ui.panel.lovelace.editor.card.generic.theme")," (").concat(e.hass.localize("ui.panel.lovelace.editor.card.config.optional"),")");case"unit":return e.hass.localize("ui.panel.lovelace.editor.card.generic.unit");default:return e.hass.localize("ui.panel.lovelace.editor.card.gauge.severity.".concat(t.name))}}}}]}}),m.oi)},98346:function(e,t,n){n.d(t,{I:function(){return i}});var a=n(93088),i=(0,a.Ry)({type:(0,a.Z_)(),view_layout:(0,a.Yj)()})}}]);
//# sourceMappingURL=22115.6ILWje2xAfw.js.map