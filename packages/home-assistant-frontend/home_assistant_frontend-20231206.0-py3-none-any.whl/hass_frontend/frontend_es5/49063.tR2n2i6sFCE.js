(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[49063],{53725:function(t,e,n){"use strict";n(95905),n(51467),Object.defineProperty(e,"__esModule",{value:!0}),e.default=function(t,e){if(null==t)throw new TypeError("assign requires that input parameter not be null or undefined");for(var n in e)Object.prototype.hasOwnProperty.call(e,n)&&(t[n]=e[n]);return t},t.exports=e.default},20508:function(t,e,n){"use strict";n(95905);var r=n(28847).default;Object.defineProperty(e,"__esModule",{value:!0}),e.default=function(t){return(0,u.default)({},t)};var u=r(n(53725));t.exports=e.default},59699:function(t,e,n){"use strict";n.d(e,{Z:function(){return o}});var r=n(90394),u=n(39244),a=n(23682),i=36e5;function o(t,e){(0,a.Z)(2,arguments);var n=(0,r.Z)(e);return(0,u.Z)(t,n*i)}},39244:function(t,e,n){"use strict";n.d(e,{Z:function(){return i}});var r=n(90394),u=n(34327),a=n(23682);function i(t,e){(0,a.Z)(2,arguments);var n=(0,u.Z)(t).getTime(),i=(0,r.Z)(e);return new Date(n+i)}},57879:function(t,e,n){"use strict";n.d(e,{Z:function(){return a}});var r=n(34327),u=n(23682);function a(t,e){(0,u.Z)(2,arguments);var n=(0,r.Z)(t),a=(0,r.Z)(e),i=n.getTime()-a.getTime();return i<0?-1:i>0?1:i}},38588:function(t,e,n){"use strict";n.d(e,{Z:function(){return o}});n(76843);var r=n(34327),u=n(23682);var a=n(57879),i=n(63390);function o(t,e){(0,u.Z)(2,arguments);var n,o=(0,r.Z)(t),s=(0,r.Z)(e),c=(0,a.Z)(o,s),f=Math.abs(function(t,e){(0,u.Z)(2,arguments);var n=(0,r.Z)(t),a=(0,r.Z)(e);return 12*(n.getFullYear()-a.getFullYear())+(n.getMonth()-a.getMonth())}(o,s));if(f<1)n=0;else{1===o.getMonth()&&o.getDate()>27&&o.setDate(30),o.setMonth(o.getMonth()-c*f);var l=(0,a.Z)(o,s)===-c;(0,i.Z)((0,r.Z)(t))&&1===f&&1===(0,a.Z)(t,s)&&(l=!1),n=c*(f-Number(l))}return 0===n?0:n}},74774:function(t,e,n){"use strict";n.d(e,{Z:function(){return a}});var r=n(34327),u=n(23682);function a(t){return(0,u.Z)(1,arguments),1===(0,r.Z)(t).getDate()}},63390:function(t,e,n){"use strict";n.d(e,{Z:function(){return o}});var r=n(34327),u=n(93752),a=n(1905),i=n(23682);function o(t){(0,i.Z)(1,arguments);var e=(0,r.Z)(t);return(0,u.Z)(e).getTime()===(0,a.Z)(e).getTime()}},7616:function(t,e,n){"use strict";n.r(e),n.d(e,{OriginalStatesViewStrategy:function(){return m}});var r=n(99312),u=n(68990),a=n(81043),i=n(33368),o=n(71650),s=n(82390),c=n(69205),f=n(70906),l=n(91808),Z=(n(97393),n(51358),n(46798),n(47084),n(5239),n(98490),n(40271),n(60163),n(36513),n(28101)),d=n(68144),g=n(95260),p=n(7323),v=n(55424),h=n(47680),m=(0,l.Z)([(0,g.Mo)("original-states-view-strategy")],(function(t,e){var n,l=function(e){(0,c.Z)(r,e);var n=(0,f.Z)(r);function r(){var e;(0,o.Z)(this,r);for(var u=arguments.length,a=new Array(u),i=0;i<u;i++)a[i]=arguments[i];return e=n.call.apply(n,[this].concat(a)),t((0,s.Z)(e)),e}return(0,i.Z)(r)}(e);return{F:l,d:[{kind:"method",static:!0,key:"generate",value:(n=(0,a.Z)((0,r.Z)().mark((function t(e,n){var a,i,o,s,c;return(0,r.Z)().wrap((function(t){for(;;)switch(t.prev=t.next){case 0:if(n.config.state!==Z.UE){t.next=2;break}return t.abrupt("return",{cards:[{type:"starting"}]});case 2:if(!n.config.recovery_mode){t.next=4;break}return t.abrupt("return",{cards:[{type:"recovery-mode"}]});case 4:return t.next=6,Promise.all([n.loadBackendTranslation("title"),(0,p.p)(n,"energy")?(0,v.ZC)(n).catch((function(){})):void 0]);case 6:return a=t.sent,i=(0,u.Z)(a,2),o=i[0],s=i[1],c=(0,h.AP)(n.areas,n.devices,n.entities,n.states,o,s,e.areas,e.hide_entities_without_area,e.hide_energy),n.config.components.includes("geo_location")&&c&&c.cards&&c.cards.push({type:"map",geo_location_sources:["all"]}),0===c.cards.length&&c.cards.push({type:"empty-state"}),t.abrupt("return",c);case 14:case"end":return t.stop()}}),t)}))),function(t,e){return n.apply(this,arguments)})}]}}),d.fl)},28847:function(t){t.exports=function(t){return t&&t.__esModule?t:{default:t}},t.exports.__esModule=!0,t.exports.default=t.exports},23158:function(t,e,n){"use strict";n.d(e,{Z:function(){return a}});var r=n(89273),u=n(36857);function a(t,e,n){var a=(0,u.Z)(t,n),i=(0,r.Z)(e,a,!0),o=new Date(a.getTime()-i),s=new Date(0);return s.setFullYear(o.getUTCFullYear(),o.getUTCMonth(),o.getUTCDate()),s.setHours(o.getUTCHours(),o.getUTCMinutes(),o.getUTCSeconds(),o.getUTCMilliseconds()),s}},25101:function(t,e,n){"use strict";n.d(e,{Z:function(){return s}});n(63789),n(18098);var r=n(20508),u=n(36857),a=n(57944),i=n(89273),o=n(74101);function s(t,e,n){if("string"==typeof t&&!t.match(a.Z)){var s=r(n);return s.timeZone=e,(0,u.Z)(t,s)}var c=(0,u.Z)(t,n),f=(0,o.Z)(c.getFullYear(),c.getMonth(),c.getDate(),c.getHours(),c.getMinutes(),c.getSeconds(),c.getMilliseconds()).getTime(),l=(0,i.Z)(e,new Date(f));return new Date(f+l)}}}]);
//# sourceMappingURL=49063.tR2n2i6sFCE.js.map