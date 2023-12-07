"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[13786],{13786:function(t,e,a){var i,r,o,n,s=a(88962),l=a(99312),d=a(68990),c=a(81043),u=a(40039),h=a(33368),p=a(71650),f=a(82390),m=a(69205),v=a(70906),y=a(91808),k=a(34541),g=a(47838),b=(a(97393),a(76843),a(46349),a(70320),a(46798),a(9849),a(50289),a(94167),a(36513),a(22859),a(91989),a(68144)),_=a(95260),Z=(a(51467),a(51358),a(47084),a(5239),a(98490),function(){var t=(0,c.Z)((0,l.Z)().mark((function t(e){var i,r,o,n;return(0,l.Z)().wrap((function(t){for(;;)switch(t.prev=t.next){case 0:if(e.parentNode){t.next=2;break}throw new Error("Cannot setup Leaflet map on disconnected element");case 2:return t.next=4,Promise.all([a.e(96055),a.e(92557)]).then(a.t.bind(a,70208,23));case 4:return(i=t.sent.default).Icon.Default.imagePath="/static/images/leaflet/images/",r=i.map(e),(o=document.createElement("link")).setAttribute("href","/static/images/leaflet/leaflet.css"),o.setAttribute("rel","stylesheet"),e.parentNode.appendChild(o),r.setView([52.3731339,4.8903147],13),n=M(i).addTo(r),t.abrupt("return",[r,i,n]);case 14:case"end":return t.stop()}}),t)})));return function(e){return t.apply(this,arguments)}}()),M=function(t){return t.tileLayer("https://basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}".concat(t.Browser.retina?"@2x.png":".png"),{attribution:'&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>, &copy; <a href="https://carto.com/attributions">CARTO</a>',subdomains:"abcd",minZoom:0,maxZoom:20})},w=a(22311),x=a(91741),L=a(44281),z=(a(10983),a(47501)),C=a(47181),E=(0,y.Z)(null,(function(t,e){var a=function(e){(0,m.Z)(i,e);var a=(0,v.Z)(i);function i(){var e;(0,p.Z)(this,i);for(var r=arguments.length,o=new Array(r),n=0;n<r;n++)o[n]=arguments[n];return e=a.call.apply(a,[this].concat(o)),t((0,f.Z)(e)),e}return(0,h.Z)(i)}(e);return{F:a,d:[{kind:"field",decorators:[(0,_.Cb)({attribute:"entity-id"})],key:"entityId",value:void 0},{kind:"field",decorators:[(0,_.Cb)({attribute:"entity-name"})],key:"entityName",value:void 0},{kind:"field",decorators:[(0,_.Cb)({attribute:"entity-picture"})],key:"entityPicture",value:void 0},{kind:"field",decorators:[(0,_.Cb)({attribute:"entity-color"})],key:"entityColor",value:void 0},{kind:"method",key:"render",value:function(){return(0,b.dy)(i||(i=(0,s.Z)([' <div class="marker ','" style="','" @click="','"> '," </div> "])),this.entityPicture?"picture":"",(0,z.V)({"border-color":this.entityColor}),this._badgeTap,this.entityPicture?(0,b.dy)(r||(r=(0,s.Z)(['<div class="entity-picture" style="','"></div>'])),(0,z.V)({"background-image":"url(".concat(this.entityPicture,")")})):this.entityName)}},{kind:"method",key:"_badgeTap",value:function(t){t.stopPropagation(),this.entityId&&(0,C.B)(this,"hass-more-info",{entityId:this.entityId})}},{kind:"get",static:!0,key:"styles",value:function(){return(0,b.iv)(o||(o=(0,s.Z)([".marker{display:flex;justify-content:center;align-items:center;box-sizing:border-box;width:48px;height:48px;font-size:var(--ha-marker-font-size, 1.5em);border-radius:50%;border:1px solid var(--ha-marker-color,var(--primary-color));color:var(--primary-text-color);background-color:var(--card-background-color)}.marker.picture{overflow:hidden}.entity-picture{background-size:cover;height:100%;width:100%}"])))}}]}}),b.oi);customElements.define("ha-entity-marker",E);var P=function(t){return"string"==typeof t?t:t.entity_id};(0,y.Z)([(0,_.Mo)("ha-map")],(function(t,e){var a,i,r=function(e){(0,m.Z)(i,e);var a=(0,v.Z)(i);function i(){var e;(0,p.Z)(this,i);for(var r=arguments.length,o=new Array(r),n=0;n<r;n++)o[n]=arguments[n];return e=a.call.apply(a,[this].concat(o)),t((0,f.Z)(e)),e}return(0,h.Z)(i)}(e);return{F:r,d:[{kind:"field",decorators:[(0,_.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,_.Cb)({attribute:!1})],key:"entities",value:void 0},{kind:"field",decorators:[(0,_.Cb)({attribute:!1})],key:"paths",value:void 0},{kind:"field",decorators:[(0,_.Cb)({attribute:!1})],key:"layers",value:void 0},{kind:"field",decorators:[(0,_.Cb)({type:Boolean})],key:"autoFit",value:function(){return!1}},{kind:"field",decorators:[(0,_.Cb)({type:Boolean})],key:"renderPassive",value:function(){return!1}},{kind:"field",decorators:[(0,_.Cb)({type:Boolean})],key:"interactiveZones",value:function(){return!1}},{kind:"field",decorators:[(0,_.Cb)({type:Boolean})],key:"fitZones",value:void 0},{kind:"field",decorators:[(0,_.Cb)({type:Boolean})],key:"darkMode",value:void 0},{kind:"field",decorators:[(0,_.Cb)({type:Number})],key:"zoom",value:function(){return 14}},{kind:"field",decorators:[(0,_.SB)()],key:"_loaded",value:function(){return!1}},{kind:"field",key:"leafletMap",value:void 0},{kind:"field",key:"Leaflet",value:void 0},{kind:"field",key:"_resizeObserver",value:void 0},{kind:"field",key:"_mapItems",value:function(){return[]}},{kind:"field",key:"_mapFocusItems",value:function(){return[]}},{kind:"field",key:"_mapZones",value:function(){return[]}},{kind:"field",key:"_mapPaths",value:function(){return[]}},{kind:"method",key:"connectedCallback",value:function(){(0,k.Z)((0,g.Z)(r.prototype),"connectedCallback",this).call(this),this._loadMap(),this._attachObserver()}},{kind:"method",key:"disconnectedCallback",value:function(){(0,k.Z)((0,g.Z)(r.prototype),"disconnectedCallback",this).call(this),this.leafletMap&&(this.leafletMap.remove(),this.leafletMap=void 0,this.Leaflet=void 0),this._loaded=!1,this._resizeObserver&&this._resizeObserver.unobserve(this)}},{kind:"method",key:"update",value:function(t){var e,a;if((0,k.Z)((0,g.Z)(r.prototype),"update",this).call(this,t),this._loaded){var i=!1,o=t.get("hass");if(t.has("_loaded")||t.has("entities"))this._drawEntities(),i=!0;else if(this._loaded&&o&&this.entities){var n,s=(0,u.Z)(this.entities);try{for(s.s();!(n=s.n()).done;){var l=n.value;if(o.states[P(l)]!==this.hass.states[P(l)]){this._drawEntities(),i=!0;break}}}catch(d){s.e(d)}finally{s.f()}}(t.has("_loaded")||t.has("paths"))&&this._drawPaths(),(t.has("_loaded")||t.has("layers"))&&(this._drawLayers(t.get("layers")),i=!0),(t.has("_loaded")||this.autoFit&&i)&&this.fitMap(),t.has("zoom")&&this.leafletMap.setZoom(this.zoom),(t.has("darkMode")||t.has("hass")&&(!o||(null===(e=o.themes)||void 0===e?void 0:e.darkMode)!==(null===(a=this.hass.themes)||void 0===a?void 0:a.darkMode)))&&this._updateMapStyle()}}},{kind:"method",key:"_updateMapStyle",value:function(){var t,e,a,i=null!==(t=null!==(e=this.darkMode)&&void 0!==e?e:this.hass.themes.darkMode)&&void 0!==t&&t,r=null!==(a=this.darkMode)&&void 0!==a&&a,o=this.shadowRoot.getElementById("map");o.classList.toggle("dark",i),o.classList.toggle("forced-dark",r)}},{kind:"method",key:"_loadMap",value:(i=(0,c.Z)((0,l.Z)().mark((function t(){var e,a,i;return(0,l.Z)().wrap((function(t){for(;;)switch(t.prev=t.next){case 0:return(e=this.shadowRoot.getElementById("map"))||((e=document.createElement("div")).id="map",this.shadowRoot.append(e)),t.next=4,Z(e);case 4:a=t.sent,i=(0,d.Z)(a,2),this.leafletMap=i[0],this.Leaflet=i[1],this._updateMapStyle(),this._loaded=!0;case 10:case"end":return t.stop()}}),t,this)}))),function(){return i.apply(this,arguments)})},{kind:"method",key:"fitMap",value:function(t){var e,a,i;if(this.leafletMap&&this.Leaflet&&this.hass)if(this._mapFocusItems.length||null!==(e=this.layers)&&void 0!==e&&e.length){var r,o=this.Leaflet.latLngBounds(this._mapFocusItems?this._mapFocusItems.map((function(t){return t.getLatLng()})):[]);if(this.fitZones)null===(r=this._mapZones)||void 0===r||r.forEach((function(t){o.extend("getBounds"in t?t.getBounds():t.getLatLng())}));null===(a=this.layers)||void 0===a||a.forEach((function(t){o.extend("getBounds"in t?t.getBounds():t.getLatLng())})),o=o.pad(null!==(i=null==t?void 0:t.pad)&&void 0!==i?i:.5),this.leafletMap.fitBounds(o,{maxZoom:(null==t?void 0:t.zoom)||this.zoom})}else this.leafletMap.setView(new this.Leaflet.LatLng(this.hass.config.latitude,this.hass.config.longitude),(null==t?void 0:t.zoom)||this.zoom)}},{kind:"method",key:"fitBounds",value:function(t,e){var a;if(this.leafletMap&&this.Leaflet&&this.hass){var i=this.Leaflet.latLngBounds(t).pad(null!==(a=null==e?void 0:e.pad)&&void 0!==a?a:.5);this.leafletMap.fitBounds(i,{maxZoom:(null==e?void 0:e.zoom)||this.zoom})}}},{kind:"method",key:"_drawLayers",value:function(t){if(t&&t.forEach((function(t){return t.remove()})),this.layers){var e=this.leafletMap;this.layers.forEach((function(t){e.addLayer(t)}))}}},{kind:"method",key:"_drawPaths",value:function(){var t=this,e=this.hass,a=this.leafletMap,i=this.Leaflet;if(e&&a&&i&&(this._mapPaths.length&&(this._mapPaths.forEach((function(t){return t.remove()})),this._mapPaths=[]),this.paths)){var r=getComputedStyle(this).getPropertyValue("--dark-primary-color");this.paths.forEach((function(e){var o,n;e.gradualOpacity&&(o=e.gradualOpacity/(e.points.length-2),n=1-e.gradualOpacity);for(var s=0;s<e.points.length-1;s++){var l=e.gradualOpacity?n+s*o:void 0;t._mapPaths.push(i.circleMarker(e.points[s].point,{radius:3,color:e.color||r,opacity:l,fillOpacity:l,interactive:!0}).bindTooltip(e.points[s].tooltip,{direction:"top"})),t._mapPaths.push(i.polyline([e.points[s].point,e.points[s+1].point],{color:e.color||r,opacity:l,interactive:!1}))}var d=e.points.length-1;if(d>=0){var c=e.gradualOpacity?n+d*o:void 0;t._mapPaths.push(i.circleMarker(e.points[d].point,{radius:3,color:e.color||r,opacity:c,fillOpacity:c,interactive:!0}).bindTooltip(e.points[d].tooltip,{direction:"top"}))}t._mapPaths.forEach((function(t){return a.addLayer(t)}))}))}}},{kind:"method",key:"_drawEntities",value:function(){var t,e=this.hass,a=this.leafletMap,i=this.Leaflet;if(e&&a&&i&&(this._mapItems.length&&(this._mapItems.forEach((function(t){return t.remove()})),this._mapItems=[],this._mapFocusItems=[]),this._mapZones.length&&(this._mapZones.forEach((function(t){return t.remove()})),this._mapZones=[]),this.entities)){var r,o=getComputedStyle(this),n=o.getPropertyValue("--accent-color"),s=o.getPropertyValue("--secondary-text-color"),l=o.getPropertyValue("--dark-primary-color"),d=(null!==(t=this.darkMode)&&void 0!==t?t:this.hass.themes.darkMode)?"dark":"light",c=(0,u.Z)(this.entities);try{for(c.s();!(r=c.n()).done;){var h=r.value,p=e.states[P(h)];if(p){var f="string"!=typeof h?h.name:void 0,m=null!=f?f:(0,x.C)(p),v=p.attributes,y=v.latitude,k=v.longitude,g=v.passive,b=v.icon,_=v.radius,Z=v.entity_picture,M=v.gps_accuracy;if(y&&k)if("zone"!==(0,w.N)(p)){var L="string"!=typeof h&&"state"===h.label_mode?this.hass.formatEntityState(p):null!=f?f:m.split(" ").map((function(t){return t[0]})).join("").substr(0,3),z=i.marker([y,k],{icon:i.divIcon({html:'\n              <ha-entity-marker\n                entity-id="'.concat(P(h),'"\n                entity-name="').concat(L,'"\n                entity-picture="').concat(Z?this.hass.hassUrl(Z):"",'"\n                ').concat("string"!=typeof h?'entity-color="'.concat(h.color,'"'):"","\n              ></ha-entity-marker>\n            "),iconSize:[48,48],className:""}),title:m});this._mapItems.push(z),"string"!=typeof h&&!1===h.focus||this._mapFocusItems.push(z),M&&this._mapItems.push(i.circle([y,k],{interactive:!1,color:l,radius:M}))}else{if(g&&!this.renderPassive)continue;var C="";if(b){var E=document.createElement("ha-icon");E.setAttribute("icon",b),C=E.outerHTML}else{var I=document.createElement("span");I.innerHTML=m,C=I.outerHTML}this._mapZones.push(i.marker([y,k],{icon:i.divIcon({html:C,iconSize:[24,24],className:d}),interactive:this.interactiveZones,title:m})),this._mapZones.push(i.circle([y,k],{interactive:!1,color:g?s:n,radius:_}))}}}}catch(B){c.e(B)}finally{c.f()}this._mapItems.forEach((function(t){return a.addLayer(t)})),this._mapZones.forEach((function(t){return a.addLayer(t)}))}}},{kind:"method",key:"_attachObserver",value:(a=(0,c.Z)((0,l.Z)().mark((function t(){var e=this;return(0,l.Z)().wrap((function(t){for(;;)switch(t.prev=t.next){case 0:if(this._resizeObserver){t.next=4;break}return t.next=3,(0,L.j)();case 3:this._resizeObserver=new ResizeObserver((function(){var t;null===(t=e.leafletMap)||void 0===t||t.invalidateSize({debounceMoveend:!0})}));case 4:this._resizeObserver.observe(this);case 5:case"end":return t.stop()}}),t,this)}))),function(){return a.apply(this,arguments)})},{kind:"get",static:!0,key:"styles",value:function(){return(0,b.iv)(n||(n=(0,s.Z)([":host{display:block;height:300px}#map{height:100%}#map.dark{background:#090909}#map.forced-dark{--map-filter:invert(0.9) hue-rotate(170deg) brightness(1.5) contrast(1.2) saturate(0.3)}#map:active{cursor:grabbing;cursor:-moz-grabbing;cursor:-webkit-grabbing}.light{color:#000}.dark{color:#fff}.leaflet-tile-pane{filter:var(--map-filter)}.dark .leaflet-bar a{background-color:var(--card-background-color,#1c1c1c);color:#fff}.leaflet-marker-draggable{cursor:move!important}.leaflet-edit-resize{border-radius:50%;cursor:nesw-resize!important}.named-icon{display:flex;align-items:center;justify-content:center;flex-direction:column;text-align:center;color:var(--primary-text-color)}.leaflet-pane{z-index:0!important}.leaflet-bottom,.leaflet-control,.leaflet-top{z-index:1!important}.leaflet-tooltip{padding:8px;font-size:90%;background:rgba(80,80,80,.9)!important;color:#fff!important;border-radius:4px;box-shadow:none!important}"])))}}]}}),b.fl)}}]);
//# sourceMappingURL=13786.XfN4gTWR7-A.js.map