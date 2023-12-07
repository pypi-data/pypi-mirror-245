"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[16938],{73826:function(a,t,e){e.d(t,{f:function(){return h}});var l=e(40039),c=e(33368),s=e(71650),d=e(82390),r=e(69205),o=e(70906),_=e(91808),n=e(34541),i=e(47838),u=(e(97393),e(46798),e(47084),e(51358),e(98490),e(40271),e(60163),e(9849),e(13526),e(95260)),h=function(a){var t=(0,_.Z)(null,(function(a,t){var e=function(t){(0,r.Z)(l,t);var e=(0,o.Z)(l);function l(){var t;(0,s.Z)(this,l);for(var c=arguments.length,r=new Array(c),o=0;o<c;o++)r[o]=arguments[o];return t=e.call.apply(e,[this].concat(r)),a((0,d.Z)(t)),t}return(0,c.Z)(l)}(t);return{F:e,d:[{kind:"field",decorators:[(0,u.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",key:"hassSubscribeRequiredHostProps",value:void 0},{kind:"field",key:"__unsubs",value:void 0},{kind:"method",key:"connectedCallback",value:function(){(0,n.Z)((0,i.Z)(e.prototype),"connectedCallback",this).call(this),this.__checkSubscribed()}},{kind:"method",key:"disconnectedCallback",value:function(){if((0,n.Z)((0,i.Z)(e.prototype),"disconnectedCallback",this).call(this),this.__unsubs){for(;this.__unsubs.length;){var a=this.__unsubs.pop();a instanceof Promise?a.then((function(a){return a()})):a()}this.__unsubs=void 0}}},{kind:"method",key:"updated",value:function(a){if((0,n.Z)((0,i.Z)(e.prototype),"updated",this).call(this,a),a.has("hass"))this.__checkSubscribed();else if(this.hassSubscribeRequiredHostProps){var t,c=(0,l.Z)(a.keys());try{for(c.s();!(t=c.n()).done;){var s=t.value;if(this.hassSubscribeRequiredHostProps.includes(s))return void this.__checkSubscribed()}}catch(d){c.e(d)}finally{c.f()}}}},{kind:"method",key:"hassSubscribe",value:function(){return[]}},{kind:"method",key:"__checkSubscribed",value:function(){var a,t=this;void 0!==this.__unsubs||!this.isConnected||void 0===this.hass||null!==(a=this.hassSubscribeRequiredHostProps)&&void 0!==a&&a.some((function(a){return void 0===t[a]}))||(this.__unsubs=this.hassSubscribe())}}]}}),a);return t}},16938:function(a,t,e){e.r(t),e.d(t,{HuiEnergySourcesTableCard:function(){return Ca}});var l,c,s,d,r,o,_,n,i,u,h,m,b,y,f,g,v,p,k,Z,w,C,K,j,S,W,V,z,P,x,M,F,R,H,q,B,E,A,U,J,L,N,O,T,$,D,G,I,Q,X,Y,aa,ta,ea,la,ca,sa,da=e(88962),ra=e(33368),oa=e(71650),_a=e(82390),na=e(69205),ia=e(70906),ua=e(91808),ha=(e(97393),e(11451),e(46798),e(9849),e(13526),e(46349),e(70320),e(87438),e(22890),e(40521)),ma=e(68144),ba=e(95260),ya=e(47501),fa=e(15838),ga=e(89525),va=e(18457),pa=(e(22098),e(55424)),ka=e(38014),Za=e(73826),wa=e(53658),Ca=(0,ua.Z)([(0,ba.Mo)("hui-energy-sources-table-card")],(function(a,t){var e=function(t){(0,na.Z)(l,t);var e=(0,ia.Z)(l);function l(){var t;(0,oa.Z)(this,l);for(var c=arguments.length,s=new Array(c),d=0;d<c;d++)s[d]=arguments[d];return t=e.call.apply(e,[this].concat(s)),a((0,_a.Z)(t)),t}return(0,ra.Z)(l)}(t);return{F:e,d:[{kind:"field",decorators:[(0,ba.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,ba.SB)()],key:"_config",value:void 0},{kind:"field",decorators:[(0,ba.SB)()],key:"_data",value:void 0},{kind:"field",key:"hassSubscribeRequiredHostProps",value:function(){return["_config"]}},{kind:"method",key:"hassSubscribe",value:function(){var a,t=this;return[(0,pa.UB)(this.hass,{key:null===(a=this._config)||void 0===a?void 0:a.collection_key}).subscribe((function(a){t._data=a}))]}},{kind:"method",key:"getCardSize",value:function(){return 3}},{kind:"method",key:"setConfig",value:function(a){this._config=a}},{kind:"method",key:"shouldUpdate",value:function(a){return(0,wa.SN)(this,a)||a.size>1||!a.has("hass")}},{kind:"method",key:"_getColor",value:function(a,t,e,l){var c=a.getPropertyValue(t+"-"+l).trim();if(0===c.length){var s=l>0?this.hass.themes.darkMode?(0,ga.C)((0,fa.Rw)((0,fa.wK)(e)),l):(0,ga.W)((0,fa.Rw)((0,fa.wK)(e)),l):void 0;c=s?(0,fa.CO)((0,fa.p3)(s)):e}return c}},{kind:"method",key:"render",value:function(){var a,t,e,sa,ra,oa,_a,na,ia,ua=this;if(!this.hass||!this._config)return ma.Ld;if(!this._data)return(0,ma.dy)(l||(l=(0,da.Z)(["",""])),this.hass.localize("ui.panel.lovelace.cards.energy.loading"));var ha=0,ba=0,fa=0,ga=0,Za=0,wa=0,Ca=0,Ka=0,ja=!1,Sa=!1,Wa=!1,Va=0,za=0,Pa=0,xa=0,Ma=0,Fa=0,Ra=0,Ha=0,qa=(0,pa.Jj)(this._data.prefs),Ba="--energy-grid-return-color",Ea="--energy-grid-consumption-color",Aa="--energy-battery-in-color",Ua="--energy-battery-out-color",Ja="--energy-solar-color",La="--energy-gas-color",Na="--energy-water-color",Oa=getComputedStyle(this),Ta=Oa.getPropertyValue(Ja).trim(),$a=Oa.getPropertyValue(Ua).trim(),Da=Oa.getPropertyValue(Aa).trim(),Ga=Oa.getPropertyValue(Ba).trim(),Ia=Oa.getPropertyValue(Ea).trim(),Qa=Oa.getPropertyValue(La).trim(),Xa=Oa.getPropertyValue(Na).trim(),Ya=(null===(a=qa.grid)||void 0===a?void 0:a[0].flow_from.some((function(a){return a.stat_cost||a.entity_energy_price||a.number_energy_price})))||(null===(t=qa.grid)||void 0===t?void 0:t[0].flow_to.some((function(a){return a.stat_compensation||a.entity_energy_price||a.number_energy_price})))||(null===(e=qa.gas)||void 0===e?void 0:e.some((function(a){return a.stat_cost||a.entity_energy_price||a.number_energy_price})))||(null===(sa=qa.water)||void 0===sa?void 0:sa.some((function(a){return a.stat_cost||a.entity_energy_price||a.number_energy_price}))),at=(0,pa.vE)(this.hass,this._data.prefs,this._data.statsMetadata)||"",tt=(0,pa.b)(this.hass)||"m³",et=void 0!==this._data.statsCompare;return(0,ma.dy)(c||(c=(0,da.Z)([" <ha-card> ",' <div class="mdc-data-table"> <div class="mdc-data-table__table-container"> <table class="mdc-data-table__table" aria-label="Energy sources"> <thead> <tr class="mdc-data-table__header-row"> <th class="mdc-data-table__header-cell"></th> <th class="mdc-data-table__header-cell" role="columnheader" scope="col"> '," </th> ",' <th class="mdc-data-table__header-cell mdc-data-table__header-cell--numeric" role="columnheader" scope="col"> '," </th> ",' </tr> </thead> <tbody class="mdc-data-table__content"> '," "," "," "," "," "," "," "," "," "," "," </tbody> </table> </div> </div> </ha-card>"])),this._config.title?(0,ma.dy)(s||(s=(0,da.Z)(['<h1 class="card-header">',"</h1>"])),this._config.title):"",this.hass.localize("ui.panel.lovelace.cards.energy.energy_sources_table.source"),et?(0,ma.dy)(d||(d=(0,da.Z)(['<th class="mdc-data-table__header-cell mdc-data-table__header-cell--numeric" role="columnheader" scope="col"> '," </th> ",""])),this.hass.localize("ui.panel.lovelace.cards.energy.energy_sources_table.previous_energy"),Ya?(0,ma.dy)(r||(r=(0,da.Z)(['<th class="mdc-data-table__header-cell mdc-data-table__header-cell--numeric" role="columnheader" scope="col"> '," </th>"])),this.hass.localize("ui.panel.lovelace.cards.energy.energy_sources_table.previous_cost")):""):"",this.hass.localize("ui.panel.lovelace.cards.energy.energy_sources_table.energy"),Ya?(0,ma.dy)(o||(o=(0,da.Z)([' <th class="mdc-data-table__header-cell mdc-data-table__header-cell--numeric" role="columnheader" scope="col"> '," </th>"])),this.hass.localize("ui.panel.lovelace.cards.energy.energy_sources_table.cost")):"",null===(ra=qa.solar)||void 0===ra?void 0:ra.map((function(a,t){var e,l=(0,ka.Kj)(ua._data.stats[a.stat_energy_from])||0;fa+=l;var c=et&&(0,ka.Kj)(ua._data.statsCompare[a.stat_energy_from])||0;Pa+=c;var s=ua._getColor(Oa,Ja,Ta,t);return(0,ma.dy)(_||(_=(0,da.Z)(['<tr class="mdc-data-table__row"> <td class="mdc-data-table__cell cell-bullet"> <div class="bullet" style="','"></div> </td> <th class="mdc-data-table__cell" scope="row"> '," </th> ",' <td class="mdc-data-table__cell mdc-data-table__cell--numeric"> '," kWh </td> "," </tr>"])),(0,ya.V)({borderColor:s,backgroundColor:s+"7F"}),(0,ka.Kd)(ua.hass,a.stat_energy_from,null===(e=ua._data)||void 0===e?void 0:e.statsMetadata[a.stat_energy_from]),et?(0,ma.dy)(n||(n=(0,da.Z)(['<td class="mdc-data-table__cell mdc-data-table__cell--numeric"> '," kWh </td> ",""])),(0,va.uf)(c,ua.hass.locale),Ya?(0,ma.dy)(i||(i=(0,da.Z)(['<td class="mdc-data-table__cell"></td>']))):""):"",(0,va.uf)(l,ua.hass.locale),Ya?(0,ma.dy)(u||(u=(0,da.Z)(['<td class="mdc-data-table__cell"></td>']))):"")})),qa.solar?(0,ma.dy)(h||(h=(0,da.Z)(['<tr class="mdc-data-table__row total"> <td class="mdc-data-table__cell"></td> <th class="mdc-data-table__cell" scope="row"> '," </th> ",' <td class="mdc-data-table__cell mdc-data-table__cell--numeric"> '," kWh </td> "," </tr>"])),this.hass.localize("ui.panel.lovelace.cards.energy.energy_sources_table.solar_total"),et?(0,ma.dy)(m||(m=(0,da.Z)(['<td class="mdc-data-table__cell mdc-data-table__cell--numeric"> '," kWh </td> ",""])),(0,va.uf)(Pa,this.hass.locale),Ya?(0,ma.dy)(b||(b=(0,da.Z)(['<td class="mdc-data-table__cell"></td>']))):""):"",(0,va.uf)(fa,this.hass.locale),Ya?(0,ma.dy)(y||(y=(0,da.Z)(['<td class="mdc-data-table__cell"></td>']))):""):"",null===(oa=qa.battery)||void 0===oa?void 0:oa.map((function(a,t){var e,l,c=(0,ka.Kj)(ua._data.stats[a.stat_energy_from])||0,s=(0,ka.Kj)(ua._data.stats[a.stat_energy_to])||0;ga+=c-s;var d=et&&(0,ka.Kj)(ua._data.statsCompare[a.stat_energy_from])||0,r=et&&(0,ka.Kj)(ua._data.statsCompare[a.stat_energy_to])||0;xa+=d-r;var o=ua._getColor(Oa,Ua,$a,t),_=ua._getColor(Oa,Aa,Da,t);return(0,ma.dy)(f||(f=(0,da.Z)(['<tr class="mdc-data-table__row"> <td class="mdc-data-table__cell cell-bullet"> <div class="bullet" style="','"></div> </td> <th class="mdc-data-table__cell" scope="row"> '," </th> ",' <td class="mdc-data-table__cell mdc-data-table__cell--numeric"> '," kWh </td> ",' </tr> <tr class="mdc-data-table__row"> <td class="mdc-data-table__cell cell-bullet"> <div class="bullet" style="','"></div> </td> <th class="mdc-data-table__cell" scope="row"> '," </th> ",' <td class="mdc-data-table__cell mdc-data-table__cell--numeric"> '," kWh </td> "," </tr>"])),(0,ya.V)({borderColor:o,backgroundColor:o+"7F"}),(0,ka.Kd)(ua.hass,a.stat_energy_from,null===(e=ua._data)||void 0===e?void 0:e.statsMetadata[a.stat_energy_from]),et?(0,ma.dy)(g||(g=(0,da.Z)(['<td class="mdc-data-table__cell mdc-data-table__cell--numeric"> '," kWh </td> ",""])),(0,va.uf)(d,ua.hass.locale),Ya?(0,ma.dy)(v||(v=(0,da.Z)(['<td class="mdc-data-table__cell"></td>']))):""):"",(0,va.uf)(c,ua.hass.locale),Ya?(0,ma.dy)(p||(p=(0,da.Z)(['<td class="mdc-data-table__cell"></td>']))):"",(0,ya.V)({borderColor:_,backgroundColor:_+"7F"}),(0,ka.Kd)(ua.hass,a.stat_energy_to,null===(l=ua._data)||void 0===l?void 0:l.statsMetadata[a.stat_energy_to]),et?(0,ma.dy)(k||(k=(0,da.Z)(['<td class="mdc-data-table__cell mdc-data-table__cell--numeric"> '," kWh </td> ",""])),(0,va.uf)(-1*r,ua.hass.locale),Ya?(0,ma.dy)(Z||(Z=(0,da.Z)(['<td class="mdc-data-table__cell"></td>']))):""):"",(0,va.uf)(-1*s,ua.hass.locale),Ya?(0,ma.dy)(w||(w=(0,da.Z)(['<td class="mdc-data-table__cell"></td>']))):"")})),qa.battery?(0,ma.dy)(C||(C=(0,da.Z)(['<tr class="mdc-data-table__row total"> <td class="mdc-data-table__cell"></td> <th class="mdc-data-table__cell" scope="row"> '," </th> ",' <td class="mdc-data-table__cell mdc-data-table__cell--numeric"> '," kWh </td> "," </tr>"])),this.hass.localize("ui.panel.lovelace.cards.energy.energy_sources_table.battery_total"),et?(0,ma.dy)(K||(K=(0,da.Z)([' <td class="mdc-data-table__cell mdc-data-table__cell--numeric"> '," kWh </td> ",""])),(0,va.uf)(xa,this.hass.locale),Ya?(0,ma.dy)(j||(j=(0,da.Z)(['<td class="mdc-data-table__cell"></td>']))):""):"",(0,va.uf)(ga,this.hass.locale),Ya?(0,ma.dy)(S||(S=(0,da.Z)(['<td class="mdc-data-table__cell"></td>']))):""):"",null===(_a=qa.grid)||void 0===_a?void 0:_a.map((function(a){return(0,ma.dy)(W||(W=(0,da.Z)([""," ",""])),a.flow_from.map((function(a,t){var e,l=(0,ka.Kj)(ua._data.stats[a.stat_energy_from])||0;ha+=l;var c=et&&(0,ka.Kj)(ua._data.statsCompare[a.stat_energy_from])||0;Va+=c;var s=a.stat_cost||ua._data.info.cost_sensors[a.stat_energy_from],d=s?(0,ka.Kj)(ua._data.stats[s])||0:null;null!==d&&(ja=!0,ba+=d);var r=et&&s?(0,ka.Kj)(ua._data.statsCompare[s])||0:null;null!==r&&(za+=r);var o=ua._getColor(Oa,Ea,Ia,t);return(0,ma.dy)(V||(V=(0,da.Z)(['<tr class="mdc-data-table__row"> <td class="mdc-data-table__cell cell-bullet"> <div class="bullet" style="','"></div> </td> <th class="mdc-data-table__cell" scope="row"> '," </th> ",' <td class="mdc-data-table__cell mdc-data-table__cell--numeric"> '," kWh </td> "," </tr>"])),(0,ya.V)({borderColor:o,backgroundColor:o+"7F"}),(0,ka.Kd)(ua.hass,a.stat_energy_from,null===(e=ua._data)||void 0===e?void 0:e.statsMetadata[a.stat_energy_from]),et?(0,ma.dy)(z||(z=(0,da.Z)(['<td class="mdc-data-table__cell mdc-data-table__cell--numeric"> '," kWh </td> ",""])),(0,va.uf)(c,ua.hass.locale),Ya?(0,ma.dy)(P||(P=(0,da.Z)(['<td class="mdc-data-table__cell mdc-data-table__cell--numeric"> '," </td>"])),null!==r?(0,va.uf)(r,ua.hass.locale,{style:"currency",currency:ua.hass.config.currency}):""):""):"",(0,va.uf)(l,ua.hass.locale),Ya?(0,ma.dy)(x||(x=(0,da.Z)([' <td class="mdc-data-table__cell mdc-data-table__cell--numeric"> '," </td>"])),null!==d?(0,va.uf)(d,ua.hass.locale,{style:"currency",currency:ua.hass.config.currency}):""):"")})),a.flow_to.map((function(a,t){var e,l=-1*((0,ka.Kj)(ua._data.stats[a.stat_energy_to])||0);ha+=l;var c=a.stat_compensation||ua._data.info.cost_sensors[a.stat_energy_to],s=c?-1*((0,ka.Kj)(ua._data.stats[c])||0):null;null!==s&&(ja=!0,ba+=s);var d=-1*(et&&(0,ka.Kj)(ua._data.statsCompare[a.stat_energy_to])||0);Va+=d;var r=et&&c?-1*((0,ka.Kj)(ua._data.statsCompare[c])||0):null;null!==r&&(za+=r);var o=ua._getColor(Oa,Ba,Ga,t);return(0,ma.dy)(M||(M=(0,da.Z)(['<tr class="mdc-data-table__row"> <td class="mdc-data-table__cell cell-bullet"> <div class="bullet" style="','"></div> </td> <th class="mdc-data-table__cell" scope="row"> '," </th> ",' <td class="mdc-data-table__cell mdc-data-table__cell--numeric"> '," kWh </td> "," </tr>"])),(0,ya.V)({borderColor:o,backgroundColor:o+"7F"}),(0,ka.Kd)(ua.hass,a.stat_energy_to,null===(e=ua._data)||void 0===e?void 0:e.statsMetadata[a.stat_energy_to]),et?(0,ma.dy)(F||(F=(0,da.Z)(['<td class="mdc-data-table__cell mdc-data-table__cell--numeric"> '," kWh </td> ",""])),(0,va.uf)(d,ua.hass.locale),Ya?(0,ma.dy)(R||(R=(0,da.Z)(['<td class="mdc-data-table__cell mdc-data-table__cell--numeric"> '," </td>"])),null!==r?(0,va.uf)(r,ua.hass.locale,{style:"currency",currency:ua.hass.config.currency}):""):""):"",(0,va.uf)(l,ua.hass.locale),Ya?(0,ma.dy)(H||(H=(0,da.Z)([' <td class="mdc-data-table__cell mdc-data-table__cell--numeric"> '," </td>"])),null!==s?(0,va.uf)(s,ua.hass.locale,{style:"currency",currency:ua.hass.config.currency}):""):"")})))})),qa.grid?(0,ma.dy)(q||(q=(0,da.Z)([' <tr class="mdc-data-table__row total"> <td class="mdc-data-table__cell"></td> <th class="mdc-data-table__cell" scope="row"> '," </th> ",' <td class="mdc-data-table__cell mdc-data-table__cell--numeric"> '," kWh </td> "," </tr>"])),this.hass.localize("ui.panel.lovelace.cards.energy.energy_sources_table.grid_total"),et?(0,ma.dy)(B||(B=(0,da.Z)(['<td class="mdc-data-table__cell mdc-data-table__cell--numeric"> '," kWh </td> ",""])),(0,va.uf)(Va,this.hass.locale),Ya?(0,ma.dy)(E||(E=(0,da.Z)(['<td class="mdc-data-table__cell mdc-data-table__cell--numeric"> '," </td>"])),ja?(0,va.uf)(za,this.hass.locale,{style:"currency",currency:this.hass.config.currency}):""):""):"",(0,va.uf)(ha,this.hass.locale),Ya?(0,ma.dy)(A||(A=(0,da.Z)(['<td class="mdc-data-table__cell mdc-data-table__cell--numeric"> '," </td>"])),ja?(0,va.uf)(ba,this.hass.locale,{style:"currency",currency:this.hass.config.currency}):""):""):"",null===(na=qa.gas)||void 0===na?void 0:na.map((function(a,t){var e,l=(0,ka.Kj)(ua._data.stats[a.stat_energy_from])||0;Za+=l;var c=et&&(0,ka.Kj)(ua._data.statsCompare[a.stat_energy_from])||0;Ma+=c;var s=a.stat_cost||ua._data.info.cost_sensors[a.stat_energy_from],d=s?(0,ka.Kj)(ua._data.stats[s])||0:null;null!==d&&(Sa=!0,wa+=d);var r=et&&s?(0,ka.Kj)(ua._data.statsCompare[s])||0:null;null!==r&&(Fa+=r);var o=ua._getColor(Oa,La,Qa,t);return(0,ma.dy)(U||(U=(0,da.Z)(['<tr class="mdc-data-table__row"> <td class="mdc-data-table__cell cell-bullet"> <div class="bullet" style="','"></div> </td> <th class="mdc-data-table__cell" scope="row"> '," </th> ",' <td class="mdc-data-table__cell mdc-data-table__cell--numeric"> '," "," </td> "," </tr>"])),(0,ya.V)({borderColor:o,backgroundColor:o+"7F"}),(0,ka.Kd)(ua.hass,a.stat_energy_from,null===(e=ua._data)||void 0===e?void 0:e.statsMetadata[a.stat_energy_from]),et?(0,ma.dy)(J||(J=(0,da.Z)([' <td class="mdc-data-table__cell mdc-data-table__cell--numeric"> '," "," </td> ",""])),(0,va.uf)(c,ua.hass.locale),at,Ya?(0,ma.dy)(L||(L=(0,da.Z)(['<td class="mdc-data-table__cell mdc-data-table__cell--numeric"> '," </td>"])),null!==r?(0,va.uf)(r,ua.hass.locale,{style:"currency",currency:ua.hass.config.currency}):""):""):"",(0,va.uf)(l,ua.hass.locale),at,Ya?(0,ma.dy)(N||(N=(0,da.Z)(['<td class="mdc-data-table__cell mdc-data-table__cell--numeric"> '," </td>"])),null!==d?(0,va.uf)(d,ua.hass.locale,{style:"currency",currency:ua.hass.config.currency}):""):"")})),qa.gas?(0,ma.dy)(O||(O=(0,da.Z)(['<tr class="mdc-data-table__row total"> <td class="mdc-data-table__cell"></td> <th class="mdc-data-table__cell" scope="row"> '," </th> ",' <td class="mdc-data-table__cell mdc-data-table__cell--numeric"> '," "," </td> "," </tr>"])),this.hass.localize("ui.panel.lovelace.cards.energy.energy_sources_table.gas_total"),et?(0,ma.dy)(T||(T=(0,da.Z)(['<td class="mdc-data-table__cell mdc-data-table__cell--numeric"> '," "," </td> ",""])),(0,va.uf)(Ma,this.hass.locale),at,Ya?(0,ma.dy)($||($=(0,da.Z)(['<td class="mdc-data-table__cell mdc-data-table__cell--numeric"> '," </td>"])),Sa?(0,va.uf)(Fa,this.hass.locale,{style:"currency",currency:this.hass.config.currency}):""):""):"",(0,va.uf)(Za,this.hass.locale),at,Ya?(0,ma.dy)(D||(D=(0,da.Z)(['<td class="mdc-data-table__cell mdc-data-table__cell--numeric"> '," </td>"])),Sa?(0,va.uf)(wa,this.hass.locale,{style:"currency",currency:this.hass.config.currency}):""):""):"",null===(ia=qa.water)||void 0===ia?void 0:ia.map((function(a,t){var e,l=(0,ka.Kj)(ua._data.stats[a.stat_energy_from])||0;Ca+=l;var c=et&&(0,ka.Kj)(ua._data.statsCompare[a.stat_energy_from])||0;Ra+=c;var s=a.stat_cost||ua._data.info.cost_sensors[a.stat_energy_from],d=s?(0,ka.Kj)(ua._data.stats[s])||0:null;null!==d&&(Wa=!0,Ka+=d);var r=et&&s?(0,ka.Kj)(ua._data.statsCompare[s])||0:null;null!==r&&(Ha+=r);var o=ua._getColor(Oa,Na,Xa,t);return(0,ma.dy)(G||(G=(0,da.Z)(['<tr class="mdc-data-table__row"> <td class="mdc-data-table__cell cell-bullet"> <div class="bullet" style="','"></div> </td> <th class="mdc-data-table__cell" scope="row"> '," </th> ",' <td class="mdc-data-table__cell mdc-data-table__cell--numeric"> '," "," </td> "," </tr>"])),(0,ya.V)({borderColor:o,backgroundColor:o+"7F"}),(0,ka.Kd)(ua.hass,a.stat_energy_from,null===(e=ua._data)||void 0===e?void 0:e.statsMetadata[a.stat_energy_from]),et?(0,ma.dy)(I||(I=(0,da.Z)([' <td class="mdc-data-table__cell mdc-data-table__cell--numeric"> '," "," </td> ",""])),(0,va.uf)(c,ua.hass.locale),tt,Ya?(0,ma.dy)(Q||(Q=(0,da.Z)(['<td class="mdc-data-table__cell mdc-data-table__cell--numeric"> '," </td>"])),null!==r?(0,va.uf)(r,ua.hass.locale,{style:"currency",currency:ua.hass.config.currency}):""):""):"",(0,va.uf)(l,ua.hass.locale),tt,Ya?(0,ma.dy)(X||(X=(0,da.Z)(['<td class="mdc-data-table__cell mdc-data-table__cell--numeric"> '," </td>"])),null!==d?(0,va.uf)(d,ua.hass.locale,{style:"currency",currency:ua.hass.config.currency}):""):"")})),qa.water?(0,ma.dy)(Y||(Y=(0,da.Z)(['<tr class="mdc-data-table__row total"> <td class="mdc-data-table__cell"></td> <th class="mdc-data-table__cell" scope="row"> '," </th> ",' <td class="mdc-data-table__cell mdc-data-table__cell--numeric"> '," "," </td> "," </tr>"])),this.hass.localize("ui.panel.lovelace.cards.energy.energy_sources_table.water_total"),et?(0,ma.dy)(aa||(aa=(0,da.Z)(['<td class="mdc-data-table__cell mdc-data-table__cell--numeric"> '," "," </td> ",""])),(0,va.uf)(Ra,this.hass.locale),tt,Ya?(0,ma.dy)(ta||(ta=(0,da.Z)(['<td class="mdc-data-table__cell mdc-data-table__cell--numeric"> '," </td>"])),Wa?(0,va.uf)(Ha,this.hass.locale,{style:"currency",currency:this.hass.config.currency}):""):""):"",(0,va.uf)(Ca,this.hass.locale),tt,Ya?(0,ma.dy)(ea||(ea=(0,da.Z)(['<td class="mdc-data-table__cell mdc-data-table__cell--numeric"> '," </td>"])),Wa?(0,va.uf)(Ka,this.hass.locale,{style:"currency",currency:this.hass.config.currency}):""):""):"",[Sa,Wa,ja].filter(Boolean).length>1?(0,ma.dy)(la||(la=(0,da.Z)(['<tr class="mdc-data-table__row total"> <td class="mdc-data-table__cell"></td> <th class="mdc-data-table__cell" scope="row"> '," </th> ",' <td class="mdc-data-table__cell"></td> <td class="mdc-data-table__cell mdc-data-table__cell--numeric"> '," </td> </tr>"])),this.hass.localize("ui.panel.lovelace.cards.energy.energy_sources_table.total_costs"),et?(0,ma.dy)(ca||(ca=(0,da.Z)(['<td class="mdc-data-table__cell"></td> <td class="mdc-data-table__cell mdc-data-table__cell--numeric"> '," </td>"])),(0,va.uf)(Fa+za+Ha,this.hass.locale,{style:"currency",currency:this.hass.config.currency})):"",(0,va.uf)(wa+ba+Ka,this.hass.locale,{style:"currency",currency:this.hass.config.currency})):"")}},{kind:"get",static:!0,key:"styles",value:function(){return(0,ma.iv)(sa||(sa=(0,da.Z)([""," .mdc-data-table{width:100%;border:0}.mdc-data-table__cell,.mdc-data-table__header-cell{color:var(--primary-text-color);border-bottom-color:var(--divider-color);text-align:var(--float-start)}.mdc-data-table__row:not(.mdc-data-table__row--selected):hover{background-color:rgba(var(--rgb-primary-text-color),.04)}.total{--mdc-typography-body2-font-weight:500}.total .mdc-data-table__cell{border-top:1px solid var(--divider-color)}ha-card{height:100%;overflow:hidden}.card-header{padding-bottom:0}.content{padding:16px}.has-header{padding-top:0}.cell-bullet{width:32px;padding-right:0;padding-inline-end:0;padding-inline-start:16px;direction:var(--direction)}.bullet{border-width:1px;border-style:solid;border-radius:4px;height:16px;width:32px}.mdc-data-table__cell--numeric{direction:ltr}"])),(0,ma.$m)(ha))}}]}}),(0,Za.f)(ma.oi))}}]);
//# sourceMappingURL=16938.IJOO2jIVZbA.js.map