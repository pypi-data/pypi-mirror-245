(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[67794],{67794:function(t,e,r){var n,o,i;t=r.nmd(t);var a,u=r(3355).default;r(95905),r(94738),r(98214),r(46798),r(94418),r(38644),r(53737),r(17692),r(51467),r(47084),r(87438),r(9849),r(22890),r(42155),r(54299),r(63789),r(46349),r(70320),r(27392),r(94570),r(36513),r(56308),r(41353),r(4160),r(51358),r(5239),r(98490),r(31528),r(7695),r(44758),r(80354),r(68630),r(57778),r(24829),r(84498),r(83868),r(75544),r(33435),r(66657),r(53608),r(42313),r(48112),r(87323),r(39588),r(31871),r(87753),r(91843),r(9979),r(34497),r(39912),r(76751),r(44988),r(32369),r(39832),r(83327),r(47475),r(94010),r(64085),r(56399),r(16149),r(39891),r(20459),r(89664),r(92478),r(60731),r(51964),r(93330),r(76843),r(34997),r(12148),r(37313),r(50289),r(94167),r(85717),r(20254),r(65974),r(22859),window,a=function(){return function(t){var e={};function r(n){if(e[n])return e[n].exports;var o=e[n]={i:n,l:!1,exports:{}};return t[n].call(o.exports,o,o.exports,r),o.l=!0,o.exports}return r.m=t,r.c=e,r.d=function(t,e,n){r.o(t,e)||Object.defineProperty(t,e,{enumerable:!0,get:n})},r.r=function(t){"undefined"!=typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(t,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(t,"__esModule",{value:!0})},r.t=function(t,e){if(1&e&&(t=r(t)),8&e)return t;if(4&e&&"object"===u(t)&&t&&t.__esModule)return t;var n=Object.create(null);if(r.r(n),Object.defineProperty(n,"default",{enumerable:!0,value:t}),2&e&&"string"!=typeof t)for(var o in t)r.d(n,o,function(e){return t[e]}.bind(null,o));return n},r.n=function(t){var e=t&&t.__esModule?function(){return t.default}:function(){return t};return r.d(e,"a",e),e},r.o=function(t,e){return Object.prototype.hasOwnProperty.call(t,e)},r.p="",r(r.s=10)}([function(t,e,r){"use strict";Object.defineProperty(e,"__esModule",{value:!0}),e.assignDeep=e.mapValues=void 0,e.mapValues=function(t,e){var r={};for(var n in t)if(t.hasOwnProperty(n)){var o=t[n];r[n]=e(o)}return r},e.assignDeep=function t(e){for(var r=[],n=1;n<arguments.length;n++)r[n-1]=arguments[n];return r.forEach((function(r){if(r)for(var n in r)if(r.hasOwnProperty(n)){var o=r[n];Array.isArray(o)?e[n]=o.slice(0):"object"===u(o)?(e[n]||(e[n]={}),t(e[n],o)):e[n]=o}})),e}},function(t,e,r){"use strict";var n=this&&this.__importDefault||function(t){return t&&t.__esModule?t:{default:t}};Object.defineProperty(e,"__esModule",{value:!0});var o=r(7),i=n(r(8)),a=r(0),u=function(){function t(e,r){this._src=e,this.opts=a.assignDeep({},t.DefaultOpts,r)}return t.use=function(t){this._pipeline=t},t.from=function(t){return new i.default(t)},Object.defineProperty(t.prototype,"result",{get:function(){return this._result},enumerable:!1,configurable:!0}),t.prototype._process=function(e,r){this.opts.quantizer,e.scaleDown(this.opts);var n=o.buildProcessOptions(this.opts,r);return t._pipeline.process(e.getImageData(),n)},t.prototype.palette=function(){return this.swatches()},t.prototype.swatches=function(){throw new Error("Method deprecated. Use `Vibrant.result.palettes[name]` instead")},t.prototype.getPalette=function(){var t=this,e=arguments[0],r="string"==typeof e?e:"default",n="string"==typeof e?arguments[1]:e,o=new this.opts.ImageClass;return o.load(this._src).then((function(e){return t._process(e,{generators:[r]})})).then((function(e){return t._result=e,e.palettes[r]})).then((function(t){return o.remove(),n&&n(void 0,t),t})).catch((function(t){return o.remove(),n&&n(t),Promise.reject(t)}))},t.prototype.getPalettes=function(){var t=this,e=arguments[0],r=arguments[1],n=Array.isArray(e)?e:["*"],o=Array.isArray(e)?r:e,i=new this.opts.ImageClass;return i.load(this._src).then((function(e){return t._process(e,{generators:n})})).then((function(e){return t._result=e,e.palettes})).then((function(t){return i.remove(),o&&o(void 0,t),t})).catch((function(t){return i.remove(),o&&o(t),Promise.reject(t)}))},t.DefaultOpts={colorCount:64,quality:5,filters:[]},t}();e.default=u},function(t,e,r){"use strict";Object.defineProperty(e,"__esModule",{value:!0}),e.applyFilters=e.ImageBase=void 0;var n=function(){function t(){}return t.prototype.scaleDown=function(t){var e=this.getWidth(),r=this.getHeight(),n=1;if(t.maxDimension>0){var o=Math.max(e,r);o>t.maxDimension&&(n=t.maxDimension/o)}else n=1/t.quality;n<1&&this.resize(e*n,r*n,n)},t}();e.ImageBase=n,e.applyFilters=function(t,e){if(e.length>0)for(var r=t.data,n=r.length/4,o=void 0,i=void 0,a=void 0,u=void 0,s=void 0,c=0;c<n;c++){i=r[0+(o=4*c)],a=r[o+1],u=r[o+2],s=r[o+3];for(var f=0;f<e.length;f++)if(!e[f](i,a,u,s)){r[o+3]=0;break}}return t}},function(t,e,r){"use strict";Object.defineProperty(e,"__esModule",{value:!0}),e.Swatch=void 0;var n=r(4),o=function(){function t(t,e){this._rgb=t,this._population=e}return t.applyFilters=function(t,e){return e.length>0?t.filter((function(t){for(var r=t.r,n=t.g,o=t.b,i=0;i<e.length;i++)if(!e[i](r,n,o,255))return!1;return!0})):t},t.clone=function(e){return new t(e._rgb,e._population)},Object.defineProperty(t.prototype,"r",{get:function(){return this._rgb[0]},enumerable:!1,configurable:!0}),Object.defineProperty(t.prototype,"g",{get:function(){return this._rgb[1]},enumerable:!1,configurable:!0}),Object.defineProperty(t.prototype,"b",{get:function(){return this._rgb[2]},enumerable:!1,configurable:!0}),Object.defineProperty(t.prototype,"rgb",{get:function(){return this._rgb},enumerable:!1,configurable:!0}),Object.defineProperty(t.prototype,"hsl",{get:function(){if(!this._hsl){var t=this._rgb,e=t[0],r=t[1],o=t[2];this._hsl=n.rgbToHsl(e,r,o)}return this._hsl},enumerable:!1,configurable:!0}),Object.defineProperty(t.prototype,"hex",{get:function(){if(!this._hex){var t=this._rgb,e=t[0],r=t[1],o=t[2];this._hex=n.rgbToHex(e,r,o)}return this._hex},enumerable:!1,configurable:!0}),Object.defineProperty(t.prototype,"population",{get:function(){return this._population},enumerable:!1,configurable:!0}),t.prototype.toJSON=function(){return{rgb:this.rgb,population:this.population}},t.prototype.getRgb=function(){return this._rgb},t.prototype.getHsl=function(){return this.hsl},t.prototype.getPopulation=function(){return this._population},t.prototype.getHex=function(){return this.hex},t.prototype.getYiq=function(){if(!this._yiq){var t=this._rgb;this._yiq=(299*t[0]+587*t[1]+114*t[2])/1e3}return this._yiq},Object.defineProperty(t.prototype,"titleTextColor",{get:function(){return this._titleTextColor&&(this._titleTextColor=this.getYiq()<200?"#fff":"#000"),this._titleTextColor},enumerable:!1,configurable:!0}),Object.defineProperty(t.prototype,"bodyTextColor",{get:function(){return this._bodyTextColor&&(this._bodyTextColor=this.getYiq()<150?"#fff":"#000"),this._bodyTextColor},enumerable:!1,configurable:!0}),t.prototype.getTitleTextColor=function(){return this.titleTextColor},t.prototype.getBodyTextColor=function(){return this.bodyTextColor},t}();e.Swatch=o},function(t,e,r){"use strict";function n(t){var e=/^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(t);if(!e)throw new RangeError("'"+t+"' is not a valid hex color");return[e[1],e[2],e[3]].map((function(t){return parseInt(t,16)}))}function o(t,e,r){return e/=255,r/=255,t=(t/=255)>.04045?Math.pow((t+.005)/1.055,2.4):t/12.92,e=e>.04045?Math.pow((e+.005)/1.055,2.4):e/12.92,r=r>.04045?Math.pow((r+.005)/1.055,2.4):r/12.92,[.4124*(t*=100)+.3576*(e*=100)+.1805*(r*=100),.2126*t+.7152*e+.0722*r,.0193*t+.1192*e+.9505*r]}function i(t,e,r){return e/=100,r/=108.883,t=(t/=95.047)>.008856?Math.pow(t,1/3):7.787*t+16/116,[116*(e=e>.008856?Math.pow(e,1/3):7.787*e+16/116)-16,500*(t-e),200*(e-(r=r>.008856?Math.pow(r,1/3):7.787*r+16/116))]}function a(t,e,r){var n=o(t,e,r);return i(n[0],n[1],n[2])}function u(t,e){var r=t[0],n=t[1],o=t[2],i=e[0],a=e[1],u=e[2],s=r-i,c=n-a,f=o-u,l=Math.sqrt(n*n+o*o),h=i-r,p=Math.sqrt(a*a+u*u)-l,g=Math.sqrt(s*s+c*c+f*f),d=Math.sqrt(g)>Math.sqrt(Math.abs(h))+Math.sqrt(Math.abs(p))?Math.sqrt(g*g-h*h-p*p):0;return h/=1,p/=1*(1+.045*l),d/=1*(1+.015*l),Math.sqrt(h*h+p*p+d*d)}function s(t,e){return u(a.apply(void 0,t),a.apply(void 0,e))}Object.defineProperty(e,"__esModule",{value:!0}),e.getColorDiffStatus=e.hexDiff=e.rgbDiff=e.deltaE94=e.rgbToCIELab=e.xyzToCIELab=e.rgbToXyz=e.hslToRgb=e.rgbToHsl=e.rgbToHex=e.hexToRgb=e.DELTAE94_DIFF_STATUS=void 0,e.DELTAE94_DIFF_STATUS={NA:0,PERFECT:1,CLOSE:2,GOOD:10,SIMILAR:50},e.hexToRgb=n,e.rgbToHex=function(t,e,r){return"#"+((1<<24)+(t<<16)+(e<<8)+r).toString(16).slice(1,7)},e.rgbToHsl=function(t,e,r){t/=255,e/=255,r/=255;var n=Math.max(t,e,r),o=Math.min(t,e,r),i=0,a=0,u=(n+o)/2;if(n!==o){var s=n-o;switch(a=u>.5?s/(2-n-o):s/(n+o),n){case t:i=(e-r)/s+(e<r?6:0);break;case e:i=(r-t)/s+2;break;case r:i=(t-e)/s+4}i/=6}return[i,a,u]},e.hslToRgb=function(t,e,r){var n,o,i;function a(t,e,r){return r<0&&(r+=1),r>1&&(r-=1),r<1/6?t+6*(e-t)*r:r<.5?e:r<2/3?t+(e-t)*(2/3-r)*6:t}if(0===e)n=o=i=r;else{var u=r<.5?r*(1+e):r+e-r*e,s=2*r-u;n=a(s,u,t+1/3),o=a(s,u,t),i=a(s,u,t-1/3)}return[255*n,255*o,255*i]},e.rgbToXyz=o,e.xyzToCIELab=i,e.rgbToCIELab=a,e.deltaE94=u,e.rgbDiff=s,e.hexDiff=function(t,e){return s(n(t),n(e))},e.getColorDiffStatus=function(t){return t<e.DELTAE94_DIFF_STATUS.NA?"N/A":t<=e.DELTAE94_DIFF_STATUS.PERFECT?"Perfect":t<=e.DELTAE94_DIFF_STATUS.CLOSE?"Close":t<=e.DELTAE94_DIFF_STATUS.GOOD?"Good":t<e.DELTAE94_DIFF_STATUS.SIMILAR?"Similar":"Wrong"}},function(t,e,r){"use strict";var n=this&&this.__importDefault||function(t){return t&&t.__esModule?t:{default:t}},o=n(r(6)),i=n(r(9));o.default.DefaultOpts.ImageClass=i.default,t.exports=o.default},function(t,e,r){"use strict";var n=this&&this.__importDefault||function(t){return t&&t.__esModule?t:{default:t}};Object.defineProperty(e,"__esModule",{value:!0});var o=n(r(1));o.default.DefaultOpts.quantizer="mmcq",o.default.DefaultOpts.generators=["default"],o.default.DefaultOpts.filters=["default"],e.default=o.default},function(t,e,r){"use strict";Object.defineProperty(e,"__esModule",{value:!0}),e.buildProcessOptions=void 0;var n=r(0);e.buildProcessOptions=function(t,e){var r=t.colorCount,o=t.quantizer,i=t.generators,a=t.filters,u={colorCount:r},s="string"==typeof o?{name:o,options:{}}:o;return s.options=n.assignDeep({},u,s.options),n.assignDeep({},{quantizer:s,generators:i,filters:a},e)}},function(t,e,r){"use strict";var n=this&&this.__importDefault||function(t){return t&&t.__esModule?t:{default:t}};Object.defineProperty(e,"__esModule",{value:!0});var o=n(r(1)),i=r(0),a=function(){function t(t,e){void 0===e&&(e={}),this._src=t,this._opts=i.assignDeep({},o.default.DefaultOpts,e)}return t.prototype.maxColorCount=function(t){return this._opts.colorCount=t,this},t.prototype.maxDimension=function(t){return this._opts.maxDimension=t,this},t.prototype.addFilter=function(t){return this._opts.filters?this._opts.filters.push(t):this._opts.filters=[t],this},t.prototype.removeFilter=function(t){if(this._opts.filters){var e=this._opts.filters.indexOf(t);e>0&&this._opts.filters.splice(e)}return this},t.prototype.clearFilters=function(){return this._opts.filters=[],this},t.prototype.quality=function(t){return this._opts.quality=t,this},t.prototype.useImageClass=function(t){return this._opts.ImageClass=t,this},t.prototype.useGenerator=function(t,e){return this._opts.generators||(this._opts.generators=[]),this._opts.generators.push(e?{name:t,options:e}:t),this},t.prototype.useQuantizer=function(t,e){return this._opts.quantizer=e?{name:t,options:e}:t,this},t.prototype.build=function(){return new o.default(this._src,this._opts)},t.prototype.getPalette=function(t){return this.build().getPalette(t)},t.prototype.getSwatches=function(t){return this.build().getPalette(t)},t}();e.default=a},function(t,e,r){"use strict";var n,o=this&&this.__extends||(n=function(t,e){return n=Object.setPrototypeOf||{__proto__:[]}instanceof Array&&function(t,e){t.__proto__=e}||function(t,e){for(var r in e)e.hasOwnProperty(r)&&(t[r]=e[r])},n(t,e)},function(t,e){function r(){this.constructor=t}n(t,e),t.prototype=null===e?Object.create(e):(r.prototype=e.prototype,new r)});Object.defineProperty(e,"__esModule",{value:!0});var i=function(t){function e(){return null!==t&&t.apply(this,arguments)||this}return o(e,t),e.prototype._initCanvas=function(){var t=this.image,e=this._canvas=document.createElement("canvas"),r=e.getContext("2d");if(!r)throw new ReferenceError("Failed to create canvas context");this._context=r,e.className="@vibrant/canvas",e.style.display="none",this._width=e.width=t.width,this._height=e.height=t.height,r.drawImage(t,0,0),document.body.appendChild(e)},e.prototype.load=function(t){var e,r,n,o,i,a,u,s=this;if("string"==typeof t)e=document.createElement("img"),r=t,(u=new URL(r,location.href)).protocol===location.protocol&&u.host===location.host&&u.port===location.port||(n=window.location.href,o=r,i=new URL(n),a=new URL(o),i.protocol===a.protocol&&i.hostname===a.hostname&&i.port===a.port)||(e.crossOrigin="anonymous"),e.src=r;else{if(!(t instanceof HTMLImageElement))return Promise.reject(new Error("Cannot load buffer as an image in browser"));e=t,r=t.src}return this.image=e,new Promise((function(t,n){var o=function(){s._initCanvas(),t(s)};e.complete?o():(e.onload=o,e.onerror=function(t){return n(new Error("Fail to load image: "+r))})}))},e.prototype.clear=function(){this._context.clearRect(0,0,this._width,this._height)},e.prototype.update=function(t){this._context.putImageData(t,0,0)},e.prototype.getWidth=function(){return this._width},e.prototype.getHeight=function(){return this._height},e.prototype.resize=function(t,e,r){var n=this,o=n._canvas,i=n._context,a=n.image;this._width=o.width=t,this._height=o.height=e,i.scale(r,r),i.drawImage(a,0,0)},e.prototype.getPixelCount=function(){return this._width*this._height},e.prototype.getImageData=function(){return this._context.getImageData(0,0,this._width,this._height)},e.prototype.remove=function(){this._canvas&&this._canvas.parentNode&&this._canvas.parentNode.removeChild(this._canvas)},e}(r(2).ImageBase);e.default=i},function(t,e,r){"use strict";var n=this&&this.__importDefault||function(t){return t&&t.__esModule?t:{default:t}},o=r(5),i=n(r(11));o.use(i.default),t.exports=o},function(t,e,r){"use strict";var n=this&&this.__importDefault||function(t){return t&&t.__esModule?t:{default:t}};Object.defineProperty(e,"__esModule",{value:!0});var o=n(r(12)),i=n(r(16)),a=(new(r(17).BasicPipeline)).filter.register("default",(function(t,e,r,n){return n>=125&&!(t>250&&e>250&&r>250)})).quantizer.register("mmcq",o.default).generator.register("default",i.default);e.default=a},function(t,e,r){"use strict";var n=this&&this.__importDefault||function(t){return t&&t.__esModule?t:{default:t}};Object.defineProperty(e,"__esModule",{value:!0});var o=r(3),i=n(r(13)),a=n(r(15));function u(t,e){for(var r=t.size();t.size()<e;){var n=t.pop();if(!(n&&n.count()>0))break;var o=n.split(),i=o[0],a=o[1];if(t.push(i),a&&a.count()>0&&t.push(a),t.size()===r)break;r=t.size()}}e.default=function(t,e){if(0===t.length||e.colorCount<2||e.colorCount>256)throw new Error("Wrong MMCQ parameters");var r=i.default.build(t),n=(r.histogram.colorCount,new a.default((function(t,e){return t.count()-e.count()})));n.push(r),u(n,.75*e.colorCount);var s=new a.default((function(t,e){return t.count()*t.volume()-e.count()*e.volume()}));return s.contents=n.contents,u(s,e.colorCount-s.size()),function(t){for(var e=[];t.size();){var r=t.pop(),n=r.avg();n[0],n[1],n[2],e.push(new o.Swatch(n,r.count()))}return e}(s)}},function(t,e,r){"use strict";var n=this&&this.__importDefault||function(t){return t&&t.__esModule?t:{default:t}};Object.defineProperty(e,"__esModule",{value:!0});var o=n(r(14)),i=function(){function t(t,e,r,n,o,i,a){this.histogram=a,this._volume=-1,this._count=-1,this.dimension={r1:t,r2:e,g1:r,g2:n,b1:o,b2:i}}return t.build=function(e){var r=new o.default(e,{sigBits:5});return new t(r.rmin,r.rmax,r.gmin,r.gmax,r.bmin,r.bmax,r)},t.prototype.invalidate=function(){this._volume=this._count=-1,this._avg=null},t.prototype.volume=function(){if(this._volume<0){var t=this.dimension,e=t.r1,r=t.r2,n=t.g1,o=t.g2,i=t.b1,a=t.b2;this._volume=(r-e+1)*(o-n+1)*(a-i+1)}return this._volume},t.prototype.count=function(){if(this._count<0){for(var t=this.histogram,e=t.hist,r=t.getColorIndex,n=this.dimension,o=n.r1,i=n.r2,a=n.g1,u=n.g2,s=n.b1,c=n.b2,f=0,l=o;l<=i;l++)for(var h=a;h<=u;h++)for(var p=s;p<=c;p++)f+=e[r(l,h,p)];this._count=f}return this._count},t.prototype.clone=function(){var e=this.histogram,r=this.dimension;return new t(r.r1,r.r2,r.g1,r.g2,r.b1,r.b2,e)},t.prototype.avg=function(){if(!this._avg){var t=this.histogram,e=t.hist,r=t.getColorIndex,n=this.dimension,o=n.r1,i=n.r2,a=n.g1,u=n.g2,s=n.b1,c=n.b2,f=0,l=void 0,h=void 0,p=void 0;l=h=p=0;for(var g=o;g<=i;g++)for(var d=a;d<=u;d++)for(var m=s;m<=c;m++){var b=e[r(g,d,m)];f+=b,l+=b*(g+.5)*8,h+=b*(d+.5)*8,p+=b*(m+.5)*8}this._avg=f?[~~(l/f),~~(h/f),~~(p/f)]:[~~(8*(o+i+1)/2),~~(8*(a+u+1)/2),~~(8*(s+c+1)/2)]}return this._avg},t.prototype.contains=function(t){var e=t[0],r=t[1],n=t[2],o=this.dimension,i=o.r1,a=o.r2,u=o.g1,s=o.g2,c=o.b1,f=o.b2;return r>>=3,n>>=3,(e>>=3)>=i&&e<=a&&r>=u&&r<=s&&n>=c&&n<=f},t.prototype.split=function(){var t=this.histogram,e=t.hist,r=t.getColorIndex,n=this.dimension,o=n.r1,i=n.r2,a=n.g1,u=n.g2,s=n.b1,c=n.b2,f=this.count();if(!f)return[];if(1===f)return[this.clone()];var l,h,p=i-o+1,g=u-a+1,d=c-s+1,m=Math.max(p,g,d),b=null;l=h=0;var _=null;if(m===p){_="r",b=new Uint32Array(i+1);for(var v=o;v<=i;v++){l=0;for(var y=a;y<=u;y++)for(var w=s;w<=c;w++)l+=e[r(v,y,w)];h+=l,b[v]=h}}else if(m===g)for(_="g",b=new Uint32Array(u+1),y=a;y<=u;y++){for(l=0,v=o;v<=i;v++)for(w=s;w<=c;w++)l+=e[r(v,y,w)];h+=l,b[y]=h}else for(_="b",b=new Uint32Array(c+1),w=s;w<=c;w++){for(l=0,v=o;v<=i;v++)for(y=a;y<=u;y++)l+=e[r(v,y,w)];h+=l,b[w]=h}for(var M=-1,x=new Uint32Array(b.length),D=0;D<b.length;D++){var L=b[D];M<0&&L>h/2&&(M=D),x[D]=h-L}var S=this;return function(t){var e=t+"1",r=t+"2",n=S.dimension[e],o=S.dimension[r],i=S.clone(),a=S.clone(),u=M-n,s=o-M;for(u<=s?(o=Math.min(o-1,~~(M+s/2)),o=Math.max(0,o)):(o=Math.max(n,~~(M-1-u/2)),o=Math.min(S.dimension[r],o));!b[o];)o++;for(var c=x[o];!c&&b[o-1];)c=x[--o];return i.dimension[r]=o,a.dimension[e]=o+1,[i,a]}(_)},t}();e.default=i},function(t,e,r){"use strict";Object.defineProperty(e,"__esModule",{value:!0});var n=function(){function t(t,e){this.pixels=t,this.opts=e;var r=e.sigBits,n=function(t,e,n){return(t<<2*r)+(e<<r)+n};this.getColorIndex=n;var o,i,a,u,s,c,f,l,h,p=8-r,g=new Uint32Array(1<<3*r);o=a=s=0,i=u=c=Number.MAX_VALUE;for(var d=t.length/4,m=0;m<d;){var b=4*m;m++,f=t[b+0],l=t[b+1],h=t[b+2],0!==t[b+3]&&(g[n(f>>=p,l>>=p,h>>=p)]+=1,f>o&&(o=f),f<i&&(i=f),l>a&&(a=l),l<u&&(u=l),h>s&&(s=h),h<c&&(c=h))}this._colorCount=g.reduce((function(t,e){return e>0?t+1:t}),0),this.hist=g,this.rmax=o,this.rmin=i,this.gmax=a,this.gmin=u,this.bmax=s,this.bmin=c}return Object.defineProperty(t.prototype,"colorCount",{get:function(){return this._colorCount},enumerable:!1,configurable:!0}),t}();e.default=n},function(t,e,r){"use strict";Object.defineProperty(e,"__esModule",{value:!0});var n=function(){function t(t){this._comparator=t,this.contents=[],this._sorted=!1}return t.prototype._sort=function(){this._sorted||(this.contents.sort(this._comparator),this._sorted=!0)},t.prototype.push=function(t){this.contents.push(t),this._sorted=!1},t.prototype.peek=function(t){return this._sort(),t="number"==typeof t?t:this.contents.length-1,this.contents[t]},t.prototype.pop=function(){return this._sort(),this.contents.pop()},t.prototype.size=function(){return this.contents.length},t.prototype.map=function(t){return this._sort(),this.contents.map(t)},t}();e.default=n},function(t,e,r){"use strict";Object.defineProperty(e,"__esModule",{value:!0});var n=r(3),o=r(4),i={targetDarkLuma:.26,maxDarkLuma:.45,minLightLuma:.55,targetLightLuma:.74,minNormalLuma:.3,targetNormalLuma:.5,maxNormalLuma:.7,targetMutesSaturation:.3,maxMutesSaturation:.4,targetVibrantSaturation:1,minVibrantSaturation:.35,weightSaturation:3,weightLuma:6.5,weightPopulation:.5};function a(t,e,r,n,o,i,a,u,s,c){var f=null,l=0;return e.forEach((function(e){var h=e.hsl,p=h[1],g=h[2];if(p>=u&&p<=s&&g>=o&&g<=i&&!function(t,e){return t.Vibrant===e||t.DarkVibrant===e||t.LightVibrant===e||t.Muted===e||t.DarkMuted===e||t.LightMuted===e}(t,e)){var d=function(t,e,r,n,o,i,a){function u(t,e){return 1-Math.abs(t-e)}return function(){for(var t=[],e=0;e<arguments.length;e++)t[e]=arguments[e];for(var r=0,n=0,o=0;o<t.length;o+=2){var i=t[o],a=t[o+1];r+=i*a,n+=a}return r/n}(u(t,e),a.weightSaturation,u(r,n),a.weightLuma,o/i,a.weightPopulation)}(p,a,g,n,e.population,r,c);(null===f||d>l)&&(f=e,l=d)}})),f}e.default=function(t,e){e=Object.assign({},i,e);var r=function(t){var e=0;return t.forEach((function(t){e=Math.max(e,t.population)})),e}(t),u=function(t,e,r){var n={Vibrant:null,DarkVibrant:null,LightVibrant:null,Muted:null,DarkMuted:null,LightMuted:null};return n.Vibrant=a(n,t,e,r.targetNormalLuma,r.minNormalLuma,r.maxNormalLuma,r.targetVibrantSaturation,r.minVibrantSaturation,1,r),n.LightVibrant=a(n,t,e,r.targetLightLuma,r.minLightLuma,1,r.targetVibrantSaturation,r.minVibrantSaturation,1,r),n.DarkVibrant=a(n,t,e,r.targetDarkLuma,0,r.maxDarkLuma,r.targetVibrantSaturation,r.minVibrantSaturation,1,r),n.Muted=a(n,t,e,r.targetNormalLuma,r.minNormalLuma,r.maxNormalLuma,r.targetMutesSaturation,0,r.maxMutesSaturation,r),n.LightMuted=a(n,t,e,r.targetLightLuma,r.minLightLuma,1,r.targetMutesSaturation,0,r.maxMutesSaturation,r),n.DarkMuted=a(n,t,e,r.targetDarkLuma,0,r.maxDarkLuma,r.targetMutesSaturation,0,r.maxMutesSaturation,r),n}(t,r,e);return function(t,e,r){if(!t.Vibrant&&!t.DarkVibrant&&!t.LightVibrant){if(!t.DarkVibrant&&t.DarkMuted){var i=t.DarkMuted.hsl,a=i[0],u=i[1],s=i[2];s=r.targetDarkLuma,t.DarkVibrant=new n.Swatch(o.hslToRgb(a,u,s),0)}if(!t.LightVibrant&&t.LightMuted){var c=t.LightMuted.hsl;a=c[0],u=c[1],s=c[2],s=r.targetDarkLuma,t.DarkVibrant=new n.Swatch(o.hslToRgb(a,u,s),0)}}if(!t.Vibrant&&t.DarkVibrant){var f=t.DarkVibrant.hsl;a=f[0],u=f[1],s=f[2],s=r.targetNormalLuma,t.Vibrant=new n.Swatch(o.hslToRgb(a,u,s),0)}else if(!t.Vibrant&&t.LightVibrant){var l=t.LightVibrant.hsl;a=l[0],u=l[1],s=l[2],s=r.targetNormalLuma,t.Vibrant=new n.Swatch(o.hslToRgb(a,u,s),0)}if(!t.DarkVibrant&&t.Vibrant){var h=t.Vibrant.hsl;a=h[0],u=h[1],s=h[2],s=r.targetDarkLuma,t.DarkVibrant=new n.Swatch(o.hslToRgb(a,u,s),0)}if(!t.LightVibrant&&t.Vibrant){var p=t.Vibrant.hsl;a=p[0],u=p[1],s=p[2],s=r.targetLightLuma,t.LightVibrant=new n.Swatch(o.hslToRgb(a,u,s),0)}if(!t.Muted&&t.Vibrant){var g=t.Vibrant.hsl;a=g[0],u=g[1],s=g[2],s=r.targetMutesSaturation,t.Muted=new n.Swatch(o.hslToRgb(a,u,s),0)}if(!t.DarkMuted&&t.DarkVibrant){var d=t.DarkVibrant.hsl;a=d[0],u=d[1],s=d[2],s=r.targetMutesSaturation,t.DarkMuted=new n.Swatch(o.hslToRgb(a,u,s),0)}if(!t.LightMuted&&t.LightVibrant){var m=t.LightVibrant.hsl;a=m[0],u=m[1],s=m[2],s=r.targetMutesSaturation,t.LightMuted=new n.Swatch(o.hslToRgb(a,u,s),0)}}(u,0,e),u}},function(t,e,r){"use strict";var n=this&&this.__awaiter||function(t,e,r,n){return new(r||(r=Promise))((function(o,i){function a(t){try{s(n.next(t))}catch(e){i(e)}}function u(t){try{s(n.throw(t))}catch(e){i(e)}}function s(t){var e;t.done?o(t.value):(e=t.value,e instanceof r?e:new r((function(t){t(e)}))).then(a,u)}s((n=n.apply(t,e||[])).next())}))},o=this&&this.__generator||function(t,e){var r,n,o,i,a={label:0,sent:function(){if(1&o[0])throw o[1];return o[1]},trys:[],ops:[]};return i={next:u(0),throw:u(1),return:u(2)},"function"==typeof Symbol&&(i[Symbol.iterator]=function(){return this}),i;function u(i){return function(u){return function(i){if(r)throw new TypeError("Generator is already executing.");for(;a;)try{if(r=1,n&&(o=2&i[0]?n.return:i[0]?n.throw||((o=n.return)&&o.call(n),0):n.next)&&!(o=o.call(n,i[1])).done)return o;switch(n=0,o&&(i=[2&i[0],o.value]),i[0]){case 0:case 1:o=i;break;case 4:return a.label++,{value:i[1],done:!1};case 5:a.label++,n=i[1],i=[0];continue;case 7:i=a.ops.pop(),a.trys.pop();continue;default:if(!((o=(o=a.trys).length>0&&o[o.length-1])||6!==i[0]&&2!==i[0])){a=0;continue}if(3===i[0]&&(!o||i[1]>o[0]&&i[1]<o[3])){a.label=i[1];break}if(6===i[0]&&a.label<o[1]){a.label=o[1],o=i;break}if(o&&a.label<o[2]){a.label=o[2],a.ops.push(i);break}o[2]&&a.ops.pop(),a.trys.pop();continue}i=e.call(t,a)}catch(u){i=[6,u],n=0}finally{r=o=0}if(5&i[0])throw i[1];return{value:i[0]?i[1]:void 0,done:!0}}([i,u])}}};Object.defineProperty(e,"__esModule",{value:!0}),e.BasicPipeline=e.Stage=void 0;var i=r(2),a=function(){function t(t){this.pipeline=t,this._map={}}return t.prototype.names=function(){return Object.keys(this._map)},t.prototype.has=function(t){return!!this._map[t]},t.prototype.get=function(t){return this._map[t]},t.prototype.register=function(t,e){return this._map[t]=e,this.pipeline},t}();e.Stage=a;var u=function(){function t(){this.filter=new a(this),this.quantizer=new a(this),this.generator=new a(this)}return t.prototype._buildProcessTasks=function(t){var e=this,r=t.filters,n=t.quantizer,o=t.generators;return 1===o.length&&"*"===o[0]&&(o=this.generator.names()),{filters:r.map((function(t){return i(e.filter,t)})),quantizer:i(this.quantizer,n),generators:o.map((function(t){return i(e.generator,t)}))};function i(t,e){var r,n;return"string"==typeof e?r=e:(r=e.name,n=e.options),{name:r,fn:t.get(r),options:n}}},t.prototype.process=function(t,e){return n(this,void 0,void 0,(function(){var r,n,i,a,u,s,c;return o(this,(function(o){switch(o.label){case 0:return r=this._buildProcessTasks(e),n=r.filters,i=r.quantizer,a=r.generators,[4,this._filterColors(n,t)];case 1:return u=o.sent(),[4,this._generateColors(i,u)];case 2:return s=o.sent(),[4,this._generatePalettes(a,s)];case 3:return c=o.sent(),[2,{colors:s,palettes:c}]}}))}))},t.prototype._filterColors=function(t,e){return Promise.resolve(i.applyFilters(e,t.map((function(t){return t.fn}))))},t.prototype._generateColors=function(t,e){return Promise.resolve(t.fn(e.data,t.options))},t.prototype._generatePalettes=function(t,e){return n(this,void 0,void 0,(function(){var r;return o(this,(function(n){switch(n.label){case 0:return[4,Promise.all(t.map((function(t){var r=t.fn,n=t.options;return Promise.resolve(r(e,n))})))];case 1:return r=n.sent(),[2,Promise.resolve(r.reduce((function(e,r,n){return e[t[n].name]=r,e}),{}))]}}))}))},t}();e.BasicPipeline=u}])},"object"===u(e)&&"object"===u(t)?t.exports=a():(o=[],void 0===(i="function"==typeof(n=a)?n.apply(e,o):n)||(t.exports=i))},42155:function(t,e,r){"use strict";var n=r(68077),o=r(18431),i=r(19480),a=r(80581);n({target:"Date",proto:!0,arity:1,forced:o((function(){return null!==new Date(NaN).toJSON()||1!==Date.prototype.toJSON.call({toISOString:function(){return 1}})}))},{toJSON:function(t){var e=i(this),r=a(e,"number");return"number"!=typeof r||isFinite(r)?e.toISOString():null}})},84498:function(t,e,r){"use strict";r(78950)("Uint32",(function(t){return function(e,r,n){return t(this,e,r,n)}}))},54299:function(t,e,r){"use strict";var n=r(68077),o=r(43173);n({target:"URL",proto:!0,enumerable:!0},{toJSON:function(){return o(URL.prototype.toString,this)}})}}]);
//# sourceMappingURL=67794.7-_-kJB7Shg.js.map