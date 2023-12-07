"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[53257],{49089:function(e,t,n){var a=n(68077),i=n(72208),r=n(9160),s=n(22933),o=n(73177);a({target:"Iterator",proto:!0,real:!0},{every:function(e){s(this),r(e);var t=o(this),n=0;return!i(t,(function(t,a){if(!e(t,n++))return a()}),{IS_RECORD:!0,INTERRUPTED:!0}).stopped}})},44533:function(e,t,n){n.d(t,{Z:function(){return r}});var a=n(42355),i=n(34953),r=(0,a.rx)({name:"@fullcalendar/daygrid",initialView:"dayGridMonth",views:{dayGrid:{component:i.Nt,dateProfileGeneratorClass:i.XK},dayGridDay:{type:"dayGrid",duration:{days:1}},dayGridWeek:{type:"dayGrid",duration:{weeks:1}},dayGridMonth:{type:"dayGrid",duration:{months:1},fixedWeekCount:!0},dayGridYear:{type:"dayGrid",duration:{years:1}}}})},75069:function(e,t,n){n.d(t,{Z:function(){return D}});var a=n(42355),i=n(40039),r=n(82390),s=n(53709),o=n(71650),l=n(33368),d=n(69205),c=n(70906),u=(n(85717),n(97393),n(36513),n(73092)),f=n(58508),v=function(e){(0,d.Z)(n,e);var t=(0,c.Z)(n);function n(){var e;return(0,o.Z)(this,n),(e=t.apply(this,arguments)).state={textId:(0,u.a5)()},e}return(0,l.Z)(n,[{key:"render",value:function(){var e=this.context,t=e.theme,n=e.dateEnv,a=e.options,i=e.viewApi,r=this.props,o=r.cellId,l=r.dayDate,d=r.todayRange,c=this.state.textId,v=(0,u.a_)(l,d),y=a.listDayFormat?n.format(l,a.listDayFormat):"",g=a.listDaySideFormat?n.format(l,a.listDaySideFormat):"",p=Object.assign({date:n.toDate(l),view:i,textId:c,text:y,sideText:g,navLinkAttrs:(0,u.b0)(this.context,l),sideNavLinkAttrs:(0,u.b0)(this.context,l,"day",!1)},v);return(0,f.az)(u.C,{elTag:"tr",elClasses:["fc-list-day"].concat((0,s.Z)((0,u.aZ)(v,t))),elAttrs:{"data-date":(0,u.bv)(l)},renderProps:p,generatorName:"dayHeaderContent",customGenerator:a.dayHeaderContent,defaultGenerator:h,classNameGenerator:a.dayHeaderClassNames,didMount:a.dayHeaderDidMount,willUnmount:a.dayHeaderWillUnmount},(function(e){return(0,f.az)("th",{scope:"colgroup",colSpan:3,id:o,"aria-labelledby":c},(0,f.az)(e,{elTag:"div",elClasses:["fc-list-day-cushion",t.getClass("tableCellShaded")]}))}))}}]),n}(u.B);function h(e){return(0,f.az)(f.HY,null,e.text&&(0,f.az)("a",Object.assign({id:e.textId,className:"fc-list-day-text"},e.navLinkAttrs),e.text),e.sideText&&(0,f.az)("a",Object.assign({"aria-hidden":!0,className:"fc-list-day-side-text"},e.sideNavLinkAttrs),e.sideText))}var y=(0,u.x)({hour:"numeric",minute:"2-digit",meridiem:"short"}),g=function(e){(0,d.Z)(n,e);var t=(0,c.Z)(n);function n(){return(0,o.Z)(this,n),t.apply(this,arguments)}return(0,l.Z)(n,[{key:"render",value:function(){var e=this.props,t=this.context,n=t.options,a=e.seg,i=e.timeHeaderId,r=e.eventHeaderId,s=e.dateHeaderId,o=n.eventTimeFormat||y;return(0,f.az)(u.cn,Object.assign({},e,{elTag:"tr",elClasses:["fc-list-event",a.eventRange.def.url&&"fc-event-forced-url"],defaultGenerator:function(){return function(e,t){var n=(0,u.bU)(e,t);return(0,f.az)("a",Object.assign({},n),e.eventRange.def.title)}(a,t)},seg:a,timeText:"",disableDragging:!0,disableResizing:!0}),(function(e,n){return(0,f.az)(f.HY,null,function(e,t,n,a,i){var r=n.options;if(!1!==r.displayEventTime){var s,o=e.eventRange.def,l=e.eventRange.instance,d=!1;if(o.allDay?d=!0:(0,u.az)(e.eventRange.range)?e.isStart?s=(0,u.bQ)(e,t,n,null,null,l.range.start,e.end):e.isEnd?s=(0,u.bQ)(e,t,n,null,null,e.start,l.range.end):d=!0:s=(0,u.bQ)(e,t,n),d){var c={text:n.options.allDayText,view:n.viewApi};return(0,f.az)(u.C,{elTag:"td",elClasses:["fc-list-event-time"],elAttrs:{headers:"".concat(a," ").concat(i)},renderProps:c,generatorName:"allDayContent",customGenerator:r.allDayContent,defaultGenerator:p,classNameGenerator:r.allDayClassNames,didMount:r.allDayDidMount,willUnmount:r.allDayWillUnmount})}return(0,f.az)("td",{className:"fc-list-event-time"},s)}return null}(a,o,t,i,s),(0,f.az)("td",{"aria-hidden":!0,className:"fc-list-event-graphic"},(0,f.az)("span",{className:"fc-list-event-dot",style:{borderColor:n.borderColor||n.backgroundColor}})),(0,f.az)(e,{elTag:"td",elClasses:["fc-list-event-title"],elAttrs:{headers:"".concat(r," ").concat(s)}}))}))}}]),n}(u.B);function p(e){return e.text}var m=function(e){(0,d.Z)(n,e);var t=(0,c.Z)(n);function n(){var e;return(0,o.Z)(this,n),(e=t.apply(this,arguments)).computeDateVars=(0,u.z)(x),e.eventStoreToSegs=(0,u.z)(e._eventStoreToSegs),e.state={timeHeaderId:(0,u.a5)(),eventHeaderId:(0,u.a5)(),dateHeaderIdRoot:(0,u.a5)()},e.setRootEl=function(t){t?e.context.registerInteractiveComponent((0,r.Z)(e),{el:t}):e.context.unregisterInteractiveComponent((0,r.Z)(e))},e}return(0,l.Z)(n,[{key:"render",value:function(){var e=this.props,t=this.context,n=this.computeDateVars(e.dateProfile),a=n.dayDates,i=n.dayRanges,r=this.eventStoreToSegs(e.eventStore,e.eventUiBases,i);return(0,f.az)(u.ct,{elRef:this.setRootEl,elClasses:["fc-list",t.theme.getClass("table"),!1!==t.options.stickyHeaderDates?"fc-list-sticky":""],viewSpec:t.viewSpec},(0,f.az)(u.cd,{liquid:!e.isHeightAuto,overflowX:e.isHeightAuto?"visible":"hidden",overflowY:e.isHeightAuto?"visible":"auto"},r.length>0?this.renderSegList(r,a):this.renderEmptyMessage()))}},{key:"renderEmptyMessage",value:function(){var e=this.context,t=e.options,n=e.viewApi,a={text:t.noEventsText,view:n};return(0,f.az)(u.C,{elTag:"div",elClasses:["fc-list-empty"],renderProps:a,generatorName:"noEventsContent",customGenerator:t.noEventsContent,defaultGenerator:b,classNameGenerator:t.noEventsClassNames,didMount:t.noEventsDidMount,willUnmount:t.noEventsWillUnmount},(function(e){return(0,f.az)(e,{elTag:"div",elClasses:["fc-list-empty-cushion"]})}))}},{key:"renderSegList",value:function(e,t){var n=this.context,a=n.theme,r=n.options,s=this.state,o=s.timeHeaderId,l=s.eventHeaderId,d=s.dateHeaderIdRoot,c=function(e){var t,n,a=[];for(t=0;t<e.length;t+=1)(a[(n=e[t]).dayIndex]||(a[n.dayIndex]=[])).push(n);return a}(e);return(0,f.az)(u.ch,{unit:"day"},(function(e,n){for(var s=[],h=0;h<c.length;h+=1){var y=c[h];if(y){var p=(0,u.bv)(t[h]),m=d+"-"+p;s.push((0,f.az)(v,{key:p,cellId:m,dayDate:t[h],todayRange:n})),y=(0,u.bR)(y,r.eventOrder);var b,x=(0,i.Z)(y);try{for(x.s();!(b=x.n()).done;){var k=b.value;s.push((0,f.az)(g,Object.assign({key:p+":"+k.eventRange.instance.instanceId,seg:k,isDragging:!1,isResizing:!1,isDateSelecting:!1,isSelected:!1,timeHeaderId:o,eventHeaderId:l,dateHeaderId:m},(0,u.bS)(k,n,e))))}}catch(C){x.e(C)}finally{x.f()}}}return(0,f.az)("table",{className:"fc-list-table "+a.getClass("table")},(0,f.az)("thead",null,(0,f.az)("tr",null,(0,f.az)("th",{scope:"col",id:o},r.timeHint),(0,f.az)("th",{scope:"col","aria-hidden":!0}),(0,f.az)("th",{scope:"col",id:l},r.eventHint))),(0,f.az)("tbody",null,s))}))}},{key:"_eventStoreToSegs",value:function(e,t,n){return this.eventRangesToSegs((0,u.af)(e,t,this.props.dateProfile.activeRange,this.context.options.nextDayThreshold).fg,n)}},{key:"eventRangesToSegs",value:function(e,t){var n,a=[],r=(0,i.Z)(e);try{for(r.s();!(n=r.n()).done;){var o=n.value;a.push.apply(a,(0,s.Z)(this.eventRangeToSegs(o,t)))}}catch(l){r.e(l)}finally{r.f()}return a}},{key:"eventRangeToSegs",value:function(e,t){var n,a,i,r=this.context.dateEnv,s=this.context.options.nextDayThreshold,o=e.range,l=e.def.allDay,d=[];for(n=0;n<t.length;n+=1)if((a=(0,u.o)(o,t[n]))&&(i={component:this,eventRange:e,start:a.start,end:a.end,isStart:e.isStart&&a.start.valueOf()===o.start.valueOf(),isEnd:e.isEnd&&a.end.valueOf()===o.end.valueOf(),dayIndex:n},d.push(i),!i.isEnd&&!l&&n+1<t.length&&o.end<r.add(t[n+1].start,s))){i.end=o.end,i.isEnd=!0;break}return d}}]),n}(u.be);function b(e){return e.text}function x(e){for(var t=(0,u.q)(e.renderRange.start),n=e.renderRange.end,a=[],i=[];t<n;)a.push(t),i.push({start:t,end:(0,u.t)(t,1)}),t=(0,u.t)(t,1);return{dayDates:a,dayRanges:i}}(0,u.cw)(':root{--fc-list-event-dot-width:10px;--fc-list-event-hover-bg-color:#f5f5f5}.fc-theme-standard .fc-list{border:1px solid var(--fc-border-color)}.fc .fc-list-empty{align-items:center;background-color:var(--fc-neutral-bg-color);display:flex;height:100%;justify-content:center}.fc .fc-list-empty-cushion{margin:5em 0}.fc .fc-list-table{border-style:hidden;width:100%}.fc .fc-list-table tr>*{border-left:0;border-right:0}.fc .fc-list-sticky .fc-list-day>*{background:var(--fc-page-bg-color);position:sticky;top:0}.fc .fc-list-table thead{left:-10000px;position:absolute}.fc .fc-list-table tbody>tr:first-child th{border-top:0}.fc .fc-list-table th{padding:0}.fc .fc-list-day-cushion,.fc .fc-list-table td{padding:8px 14px}.fc .fc-list-day-cushion:after{clear:both;content:"";display:table}.fc-theme-standard .fc-list-day-cushion{background-color:var(--fc-neutral-bg-color)}.fc-direction-ltr .fc-list-day-text,.fc-direction-rtl .fc-list-day-side-text{float:left}.fc-direction-ltr .fc-list-day-side-text,.fc-direction-rtl .fc-list-day-text{float:right}.fc-direction-ltr .fc-list-table .fc-list-event-graphic{padding-right:0}.fc-direction-rtl .fc-list-table .fc-list-event-graphic{padding-left:0}.fc .fc-list-event.fc-event-forced-url{cursor:pointer}.fc .fc-list-event:hover td{background-color:var(--fc-list-event-hover-bg-color)}.fc .fc-list-event-graphic,.fc .fc-list-event-time{white-space:nowrap;width:1px}.fc .fc-list-event-dot{border:calc(var(--fc-list-event-dot-width)/2) solid var(--fc-event-border-color);border-radius:calc(var(--fc-list-event-dot-width)/2);box-sizing:content-box;display:inline-block;height:0;width:0}.fc .fc-list-event-title a{color:inherit;text-decoration:none}.fc .fc-list-event.fc-event-forced-url:hover a{text-decoration:underline}');var k={listDayFormat:C,listDaySideFormat:C,noEventsClassNames:u.n,noEventsContent:u.n,noEventsDidMount:u.n,noEventsWillUnmount:u.n};function C(e){return!1===e?null:(0,u.x)(e)}var D=(0,a.rx)({name:"@fullcalendar/list",optionRefiners:k,views:{list:{component:m,buttonTextKey:"list",listDayFormat:{month:"long",day:"numeric",year:"numeric"}},listDay:{type:"list",duration:{days:1},listDayFormat:{weekday:"long"}},listWeek:{type:"list",duration:{weeks:1},listDayFormat:{weekday:"long"},listDaySideFormat:{month:"long",day:"numeric",year:"numeric"}},listMonth:{type:"list",duration:{month:1},listDaySideFormat:{weekday:"long"}},listYear:{type:"list",duration:{year:1},listDaySideFormat:{weekday:"long"}}}})},10329:function(e,t,n){n.d(t,{Z:function(){return l}});var a=n(99312),i=n(81043),r=n(40039),s=n(71650),o=n(33368),l=(n(51358),n(46798),n(78399),n(5239),n(56086),n(47884),n(81912),n(64584),n(41483),n(12367),n(9454),n(98490),function(){function e(t,n){var a=this,i=n.target,r=n.config,o=n.callback,l=n.skipInitial;(0,s.Z)(this,e),this.t=new Set,this.o=!1,this.i=!1,this.h=t,null!==i&&this.t.add(null!=i?i:t),this.l=r,this.o=null!=l?l:this.o,this.callback=o,window.ResizeObserver?(this.u=new ResizeObserver((function(e){a.handleChanges(e),a.h.requestUpdate()})),t.addController(this)):console.warn("ResizeController error: browser does not support ResizeObserver.")}var t;return(0,o.Z)(e,[{key:"handleChanges",value:function(e){var t;this.value=null===(t=this.callback)||void 0===t?void 0:t.call(this,e,this.u)}},{key:"hostConnected",value:function(){var e,t=(0,r.Z)(this.t);try{for(t.s();!(e=t.n()).done;){var n=e.value;this.observe(n)}}catch(a){t.e(a)}finally{t.f()}}},{key:"hostDisconnected",value:function(){this.disconnect()}},{key:"hostUpdated",value:(t=(0,i.Z)((0,a.Z)().mark((function e(){return(0,a.Z)().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:!this.o&&this.i&&this.handleChanges([]),this.i=!1;case 1:case"end":return e.stop()}}),e,this)}))),function(){return t.apply(this,arguments)})},{key:"observe",value:function(e){this.t.add(e),this.u.observe(e,this.l),this.i=!0,this.h.requestUpdate()}},{key:"unobserve",value:function(e){this.t.delete(e),this.u.unobserve(e)}},{key:"disconnect",value:function(){this.u.disconnect()}}]),e}())}}]);
//# sourceMappingURL=53257.1Rz_z5enDXg.js.map