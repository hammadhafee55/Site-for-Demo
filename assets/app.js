(function(){var d=document,$=function(s,r){return(r||d).querySelector(s)},$$=function(s,r){return[].slice.call((r||d).querySelectorAll(s))};
var nav=$("#nav"),prog=$("#prog");
function onScroll(){var y=scrollY;nav&&nav.classList.toggle("sc",y>8);if(prog){var h=d.documentElement.scrollHeight-innerHeight;prog.style.transform="scaleX("+(h>0?y/h:0)+")"}}
addEventListener("scroll",onScroll,{passive:true});onScroll();
$("#theme")&&$("#theme").addEventListener("click",function(){var t=d.documentElement.dataset.theme==="dark"?"light":"dark";d.documentElement.dataset.theme=t;try{localStorage.setItem("theme",t)}catch(e){}});
$("#burger")&&$("#burger").addEventListener("click",function(){$("#links").classList.toggle("open")});
$$("#links a").forEach(function(a){a.addEventListener("click",function(){$("#links").classList.remove("open")})});
var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add("in");io.unobserve(e.target)}})},{threshold:.12,rootMargin:"0px 0px -40px 0px"});
$$(".rv").forEach(function(el){io.observe(el)});
// list search + category filter
var q=$("#q"),list=$("#list");
if(q&&list){var items=$$(".card",list),cat="",none=$("#none"),count=$("#count");
function run(){var t=q.value.trim().toLowerCase(),n=0;items.forEach(function(i){var ok=(!t||i.dataset.text.indexOf(t)>-1)&&(!cat||i.dataset.cat===cat);i.hidden=!ok;if(ok){n++;i.classList.add("in")}});none.hidden=n>0;count.textContent=n+" result"+(n===1?"":"s")}
q.addEventListener("input",run);
$$(".chip[data-cat]").forEach(function(c){c.addEventListener("click",function(){$$(".chip[data-cat]").forEach(function(x){x.classList.remove("on")});c.classList.add("on");cat=c.dataset.cat;run()})});
var p=new URLSearchParams(location.search);if(p.get("q"))q.value=p.get("q");
if(p.get("cat")){cat=p.get("cat");$$(".chip[data-cat]").forEach(function(c){c.classList.toggle("on",c.dataset.cat===cat)})}run()}
// TOC scroll spy
var tl=$$(".toc a");if(tl.length){var so=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){tl.forEach(function(a){a.classList.toggle("on",a.getAttribute("href")==="#"+e.target.id)})}})},{rootMargin:"-20% 0px -70% 0px"});$$(".content h2[id]").forEach(function(h){so.observe(h)})}
// copy link
var cp=$("#copy");cp&&cp.addEventListener("click",function(){navigator.clipboard&&navigator.clipboard.writeText(location.href);cp.lastChild.textContent=" Copied!";setTimeout(function(){cp.lastChild.textContent=" Copy link"},1800)});
// Formspree forms
$$("form.ajax").forEach(function(f){f.addEventListener("submit",function(ev){ev.preventDefault();var s=$(".status",f),b=$("button",f);b.disabled=true;s.className="status";s.textContent="Sending...";
fetch(f.action,{method:"POST",body:new FormData(f),headers:{Accept:"application/json"}}).then(function(r){if(!r.ok)throw 0;f.reset();s.className="status ok";s.textContent="Thank you! Your submission was received."}).catch(function(){s.className="status err";s.textContent="Something went wrong. Please try again."}).then(function(){b.disabled=false})})});
})();
