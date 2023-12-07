!function(){"use strict";var e=tinymce.util.Tools.resolve("tinymce.PluginManager");const t=e=>t=>t.options.get(e),a=t("insertdatetime_dateformat"),n=t("insertdatetime_timeformat"),r=t("insertdatetime_formats"),s=t("insertdatetime_element"),i="Sun Mon Tue Wed Thu Fri Sat Sun".split(" "),o="Sunday Monday Tuesday Wednesday Thursday Friday Saturday Sunday".split(" "),l="Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split(" "),m="January February March April May June July August September October November December".split(" "),c=(e,t)=>{if((e=""+e).length<t)for(let a=0;a<t-e.length;a++)e="0"+e;return e},d=(e,t,a=new Date)=>(t=(t=(t=(t=(t=(t=(t=(t=(t=(t=(t=(t=(t=(t=(t=t.replace("%D","%m/%d/%Y")).replace("%r","%I:%M:%S %p")).replace("%Y",""+a.getFullYear())).replace("%y",""+a.getYear())).replace("%m",c(a.getMonth()+1,2))).replace("%d",c(a.getDate(),2))).replace("%H",""+c(a.getHours(),2))).replace("%M",""+c(a.getMinutes(),2))).replace("%S",""+c(a.getSeconds(),2))).replace("%I",""+((a.getHours()+11)%12+1))).replace("%p",a.getHours()<12?"AM":"PM")).replace("%B",""+e.translate(m[a.getMonth()]))).replace("%b",""+e.translate(l[a.getMonth()]))).replace("%A",""+e.translate(o[a.getDay()]))).replace("%a",""+e.translate(i[a.getDay()]))).replace("%%","%"),u=(e,t)=>{if(s(e)){const a=d(e,t);let n;n=/%[HMSIp]/.test(t)?d(e,"%Y-%m-%dT%H:%M"):d(e,"%Y-%m-%d");const r=e.dom.getParent(e.selection.getStart(),"time");r?((e,t,a,n)=>{const r=e.dom.create("time",{datetime:a},n);e.dom.replace(r,t),e.selection.select(r,!0),e.selection.collapse(!1)})(e,r,n,a):e.insertContent('<time datetime="'+n+'">'+a+"</time>")}else e.insertContent(d(e,t))};var p=tinymce.util.Tools.resolve("tinymce.util.Tools");const g=e=>t=>{const a=()=>{t.setEnabled(e.selection.isEditable())};return e.on("NodeChange",a),a(),()=>{e.off("NodeChange",a)}};e.add("insertdatetime",(e=>{(e=>{const t=e.options.register;t("insertdatetime_dateformat",{processor:"string",default:e.translate("%Y-%m-%d")}),t("insertdatetime_timeformat",{processor:"string",default:e.translate("%H:%M:%S")}),t("insertdatetime_formats",{processor:"string[]",default:["%H:%M:%S","%Y-%m-%d","%I:%M:%S %p","%D"]}),t("insertdatetime_element",{processor:"boolean",default:!1})})(e),(e=>{e.addCommand("mceInsertDate",((t,n)=>{u(e,null!=n?n:a(e))})),e.addCommand("mceInsertTime",((t,a)=>{u(e,null!=a?a:n(e))}))})(e),(e=>{const t=r(e),a=(e=>{let t=e;return{get:()=>t,set:e=>{t=e}}})((e=>{const t=r(e);return t.length>0?t[0]:n(e)})(e)),s=t=>e.execCommand("mceInsertDate",!1,t);e.ui.registry.addSplitButton("insertdatetime",{icon:"insert-time",tooltip:"Insert date/time",select:e=>e===a.get(),fetch:a=>{a(p.map(t,(t=>({type:"choiceitem",text:d(e,t),value:t}))))},onAction:e=>{s(a.get())},onItemAction:(e,t)=>{a.set(t),s(t)},onSetup:g(e)});const i=e=>()=>{a.set(e),s(e)};e.ui.registry.addNestedMenuItem("insertdatetime",{icon:"insert-time",text:"Date/time",getSubmenuItems:()=>p.map(t,(t=>({type:"menuitem",text:d(e,t),onAction:i(t)}))),onSetup:g(e)})})(e)}))}();