import urllib.parse,os,re,json,glob,shutil,html,datetime,hashlib,math
import yaml,markdown
C=json.load(open('config.json',encoding='utf-8'))
BASE=os.environ.get('SITE_BASE',C['base']).rstrip('/');ORIGIN=C['url'].rstrip('/');NAME=C['name'];FORM=C['formspree']
OUT='dist';TODAY=datetime.date.today().isoformat()
e=lambda s:html.escape(str(s if s is not None else ''),quote=True)
def asset(p):
    p=str(p or '');return BASE+p if p.startswith('/') else p
def load(d):
    r=[]
    for f in sorted(glob.glob(f'content/{d}/*.md')):
        t=open(f,encoding='utf-8').read();m=re.match(r'^---\s*\n(.*?)\n---\s*\n?(.*)$',t,re.S)
        meta=(yaml.safe_load(m.group(1)) if m else {}) or {};meta['body']=m.group(2) if m else t;meta['slug']=os.path.basename(f)[:-3]
        for k in('date','updated'):meta[k]=str(meta.get(k) or TODAY)[:10]
        r.append(meta)
    return r
G=[g for g in load('guides') if not g.get('draft')];G.sort(key=lambda g:g['date'],reverse=True)
B=[b for b in load('businesses') if b.get('published')];B.sort(key=lambda b:b['name'])
MD=lambda s:markdown.markdown(s or '',extensions=['extra','sane_lists'])
IC={'search':'<circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/>','book':'<path d="M4 5a2 2 0 0 1 2-2h13v16H6a2 2 0 0 0-2 2z"/><path d="M4 19V5"/>','shield':'<path d="M12 3 4 6v6c0 5 3.5 8 8 9 4.5-1 8-4 8-9V6z"/><path d="m9 12 2 2 4-4"/>','bolt':'<path d="M13 2 4 14h7l-1 8 9-12h-7z"/>','arrow':'<path d="M5 12h14M13 6l6 6-6 6"/>','building':'<rect x="4" y="3" width="16" height="18" rx="2"/><path d="M9 7h2M13 7h2M9 11h2M13 11h2M9 15h2M13 15h2"/>','mail':'<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/>','phone':'<path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2"/>','globe':'<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18"/>','sun':'<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>','moon':'<path d="M20 14.5A8.5 8.5 0 0 1 9.5 4 8.5 8.5 0 1 0 20 14.5z"/>','pin':'<path d="M12 21s7-6 7-11a7 7 0 0 0-14 0c0 5 7 11 7 11z"/><circle cx="12" cy="10" r="2.5"/>','clock':'<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>','check':'<path d="m5 12 5 5 9-10"/>','file':'<path d="M6 3h8l4 4v14H6z"/><path d="M14 3v5h4M9 13h6M9 17h6"/>','chat':'<path d="M4 5h16v11H9l-5 4z"/>','link':'<path d="M10 14a4 4 0 0 0 5.7 0l3-3a4 4 0 0 0-5.7-5.7l-1 1M14 10a4 4 0 0 0-5.7 0l-3 3a4 4 0 0 0 5.7 5.7l1-1"/>'}
def ic(n,c=''):return f'<svg class="ic {c}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{IC[n]}</svg>'
def hue(s):return int(hashlib.md5(str(s).encode()).hexdigest()[:4],16)%360
ICONS=['book','shield','bolt','building','file','globe']
def cover(cat,img=None,cls=''):
    if img:return f'<div class="cover {cls}"><img src="{e(asset(img))}" alt="" loading="lazy"></div>'
    return f'<div class="cover {cls}" style="--h:{hue(cat)}">{ic(ICONS[hue(cat)%len(ICONS)])}</div>'
def rt(t):return max(1,math.ceil(len(re.sub(r'<[^>]+>',' ',t).split())/200))
def gcard(g,i=0):
    return f'<a class="card gc rv" style="--d:{i*70}ms" href="{BASE}/guides/{g["slug"]}/" data-text="{e((g["title"]+" "+g["category"]+" "+g.get("excerpt","")).lower())}" data-cat="{e(g["category"])}">{cover(g["category"],g.get("cover"))}<div class="cb"><span class="tag">{e(g["category"])}</span><h3>{e(g["title"])}</h3><p>{e(g.get("excerpt",""))}</p><span class="meta">{ic("clock")} {rt(g["body"])} min read <b class="go">{ic("arrow")}</b></span></div></a>'
def avatar(b,c=''):
    return f'<img class="av {c}" src="{e(asset(b["logo"]))}" alt="" loading="lazy">' if b.get('logo') else f'<div class="av {c}" style="--h:{hue(b["category"])}">{e(b["name"][:1].upper())}</div>'
def bcard(b,i=0):
    return f'<a class="card bc rv" style="--d:{i*70}ms" href="{BASE}/businesses/{b["slug"]}/" data-text="{e((b["name"]+" "+b["category"]+" "+str(b.get("city",""))+" "+str(b.get("tagline",""))+" "+str(b.get("products",""))).lower())}" data-cat="{e(b["category"])}"><div class="row">{avatar(b)}<div><h3>{e(b["name"])}</h3><p class="mut">{e(b["category"])}{" &middot; "+e(b["city"]) if b.get("city") else ""}</p></div></div><p>{e(b.get("tagline",""))}</p><span class="meta"><span class="ver">{ic("shield")} Verified</span><b class="go">{ic("arrow")}</b></span></a>'
def form(kind,hidden,fields,btn):
    return f'<form class="ajax form" action="{FORM}" method="POST"><input type="hidden" name="_subject" value="{NAME}: {e(kind)}"><input type="hidden" name="form_type" value="{e(kind)}">{hidden}<input type="text" name="_gotcha" class="hp" tabindex="-1" autocomplete="off">{fields}<button class="btn" type="submit"><span>{btn}</span>{ic("arrow")}</button><p class="status" role="status"></p></form>'
def page(title,desc,body,path,og='website',ld='',noindex=False):
    full=f'{title} | {NAME}' if title!=NAME else f'{NAME} - {C["tagline"]}'
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{e(full)}</title><meta name="description" content="{e(desc)}">
{'<meta name="robots" content="noindex">' if noindex else f'<link rel="canonical" href="{ORIGIN}{BASE}{path}"><meta property="og:title" content="{e(full)}"><meta property="og:description" content="{e(desc)}"><meta property="og:type" content="{og}"><meta name="twitter:card" content="summary">'}{ld}
<script>try{{var t=localStorage.getItem("theme")||(matchMedia("(prefers-color-scheme:dark)").matches?"dark":"light");document.documentElement.dataset.theme=t}}catch(e){{}}</script>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap"><link rel="stylesheet" href="{BASE}/assets/style.css"></head>
<body><div class="progress" id="prog"></div>
<header class="nav" id="nav"><div class="wrap nb"><a class="logo" href="{BASE}/"><span class="mark">{ic("check")}</span>{NAME}</a>
<nav class="links" id="links"><a href="{BASE}/guides/">Guides</a><a href="{BASE}/businesses/">Businesses</a><a href="{BASE}/register/">List your business</a></nav>
<div class="nr"><button class="icon-btn" id="theme" aria-label="Toggle theme"><span class="i-sun">{ic("sun")}</span><span class="i-moon">{ic("moon")}</span></button><a class="btn sm hide-m" href="{BASE}/register/">Register</a><button class="icon-btn burger" id="burger" aria-label="Menu"><span></span><span></span></button></div></div></header>
<main>{body}</main>
<footer><div class="wrap fg"><div><a class="logo" href="{BASE}/"><span class="mark">{ic("check")}</span>{NAME}</a><p>{e(C["tagline"])}</p></div><div><b>Explore</b><a href="{BASE}/guides/">All guides</a><a href="{BASE}/businesses/">Business directory</a></div><div><b>Businesses</b><a href="{BASE}/register/">Register your business</a></div></div>
<p class="wrap small">Information is for guidance only. Always confirm fees and requirements on the official website. &copy; {datetime.date.today().year} {NAME}</p></footer>
<script src="{BASE}/assets/app.js"></script></body></html>'''
def W(p,t):
    os.makedirs(os.path.dirname(f'{OUT}/{p}') or OUT,exist_ok=True);open(f'{OUT}/{p}','w',encoding='utf-8').write(t)
def toolbar(ph,cats):
    ch=''.join(f'<button class="chip" data-cat="{e(c)}">{e(c)}</button>' for c in sorted(cats))
    return f'<div class="toolbar"><label class="sbox">{ic("search")}<input id="q" type="search" placeholder="{ph}" aria-label="Search"></label><div class="chips"><button class="chip on" data-cat="">All</button>{ch}</div></div><p class="mut count" id="count"></p><p class="empty" id="none" hidden>Nothing found. Try another search.</p>'
if os.path.exists(OUT):shutil.rmtree(OUT)
os.makedirs(OUT);shutil.copytree('assets',OUT+'/assets');shutil.copytree('admin',OUT+'/admin')
if os.path.exists('static'):
    for x in os.listdir('static'):
        s=os.path.join('static',x);d=os.path.join(OUT,x);shutil.copytree(s,d) if os.path.isdir(s) else shutil.copy(s,d)
open(OUT+'/.nojekyll','w').close()
gcats=sorted({g['category'] for g in G});bcats=sorted({b['category'] for b in B})
# HOME
cat_tiles=''.join(f'<a class="card ct rv" style="--d:{i*70}ms" href="{BASE}/guides/?cat={urllib.parse.quote(c)}"><div class="cover mini" style="--h:{hue(c)}">{ic(ICONS[hue(c)%len(ICONS)])}</div><div><h3>{e(c)}</h3><p class="mut">{sum(1 for g in G if g["category"]==c)} guides</p></div>{ic("arrow","go")}</a>' for i,c in enumerate(gcats))
steps=[('search','Find your guide','Search the procedure you need, like domicile, NTN or CNIC.'),('file','Follow the steps','Get documents, fees and the official link in one clear page.'),('chat','Or get it done','Contact a verified business and let them handle it.')]
how=''.join(f'<div class="card st rv" style="--d:{i*100}ms"><span class="num">{i+1}</span>{ic(a)}<h3>{b}</h3><p>{c}</p></div>' for i,(a,b,c) in enumerate(steps))
feat=''.join(bcard(b,i) for i,b in enumerate(B[:6])) or '<p class="mut">No businesses published yet.</p>'
home=f'''<section class="hero"><div class="blob b1"></div><div class="blob b2"></div><div class="blob b3"></div><div class="wrap hc">
<span class="pill rv">{ic("bolt")} Guides + verified businesses, one platform</span>
<h1 class="rv" style="--d:80ms">Any procedure explained.<br>Any business <span class="grad">one click away.</span></h1>
<p class="lead rv" style="--d:160ms">Clear step-by-step guides for government and business tasks, plus a directory of verified companies who can do it for you.</p>
<form class="hsearch rv" style="--d:240ms" action="{BASE}/guides/" method="get">{ic("search")}<input name="q" placeholder="Try: domicile certificate, NTN, CNIC renewal..." aria-label="Search guides"><button class="btn">Search</button></form>
<div class="chips hc-chips rv" style="--d:320ms">{''.join(f'<a class="chip" href="{BASE}/guides/?cat={urllib.parse.quote(c)}">{e(c)}</a>' for c in gcats)}</div></div></section>
<section class="wrap sec"><div class="sh rv"><h2>Browse by topic</h2></div><div class="grid g3">{cat_tiles}</div></section>
<section class="wrap sec"><div class="sh rv"><h2>Latest guides</h2><a class="more" href="{BASE}/guides/">View all {ic("arrow")}</a></div><div class="grid">{''.join(gcard(g,i) for i,g in enumerate(G[:6]))}</div></section>
<section class="band"><div class="wrap sec"><div class="sh rv"><h2>How it works</h2></div><div class="grid g3 steps">{how}</div></div></section>
<section class="wrap sec"><div class="sh rv"><h2>Featured businesses</h2><a class="more" href="{BASE}/businesses/">Browse directory {ic("arrow")}</a></div><div class="grid">{feat}</div></section>
<section class="wrap sec"><div class="cta rv"><div><h2>Own a business?</h2><p>Get your own page on {NAME}. Submit your details, our team reviews them, and your profile goes live.</p></div><a class="btn light" href="{BASE}/register/"><span>Register your business</span>{ic("arrow")}</a></div></section>'''
W('index.html',page(NAME,'Step-by-step guides for government and business procedures in Pakistan, and a directory of verified businesses.',home,'/'))
W('guides/index.html',page('Guides & Articles','Browse step-by-step guides for government and business procedures.',f'<section class="wrap sec"><h1 class="rv">Guides &amp; articles</h1>{toolbar("Search guides...",gcats)}<div class="grid list" id="list">{"".join(gcard(g,i%6) for i,g in enumerate(G))}</div></section>','/guides/'))
W('businesses/index.html',page('Business Directory','Browse verified businesses and companies, their products and services.',f'<section class="wrap sec"><h1 class="rv">Business directory</h1>{toolbar("Search businesses, services, city...",bcats)}<div class="grid list" id="list">{"".join(bcard(b,i%6) for i,b in enumerate(B))}</div></section>','/businesses/'))
# GUIDES
for g in G:
    h=MD(g['body']);toc=[]
    def sub(m):
        i=re.sub(r'[^a-z0-9]+','-',re.sub(r'<[^>]+>','',m.group(1)).lower()).strip('-');toc.append((i,re.sub(r'<[^>]+>','',m.group(1))));return f'<h2 id="{i}">{m.group(1)}</h2>'
    h=re.sub(r'<h2>(.*?)</h2>',sub,h)
    tocs=''.join(f'<a href="#{i}">{e(t)}</a>' for i,t in toc)
    rel=[x for x in G if x is not g][:3];bz=''.join(bcard(b) for b in B[:3])
    d=g.get('description') or g.get('excerpt','')
    ld='<script type="application/ld+json">'+json.dumps({'@context':'https://schema.org','@type':'Article','headline':g['title'],'description':d,'datePublished':g['date'],'dateModified':g['updated'],'author':{'@type':'Organization','name':NAME}})+'</script>'
    body=f'''<section class="wrap sec art"><article><nav class="crumbs"><a href="{BASE}/">Home</a> / <a href="{BASE}/guides/">Guides</a> / {e(g["category"])}</nav><span class="tag">{e(g["category"])}</span><h1>{e(g["title"])}</h1>
<p class="meta2">{ic("clock")} {rt(h)} min read &middot; Updated {e(g["updated"])}</p>{cover(g["category"],g.get("cover"),"hero-cover") if g.get("cover") else ""}
<div class="content" id="content">{h}</div><div class="note">{ic("shield")}<p>Requirements and fees change. Confirm details on the official website before you apply.</p></div>
<div class="share"><button class="btn ghost sm" id="copy">{ic("link")} Copy link</button></div></article>
<aside>{f'<div class="card toc"><h4>On this page</h4>{tocs}</div>' if toc else ''}{f'<div class="card hl"><h3>Want this done for you?</h3><p class="mut">Contact a verified business.</p></div>{bz}' if bz else ''}</aside></section>
<section class="wrap sec"><div class="sh"><h2>More guides</h2></div><div class="grid">{''.join(gcard(x,i) for i,x in enumerate(rel))}</div></section>'''
    W(f'guides/{g["slug"]}/index.html',page(g['title'],d,body,f'/guides/{g["slug"]}/','article',ld))
# BUSINESSES
for b in B:
    lines=[l.strip() for l in str(b.get('products','')).splitlines() if l.strip()]
    wa=re.sub(r'\D','',str(b.get('phone','')));btns=''
    if b.get('website'):btns+=f'<a class="btn" href="{e(b["website"])}" target="_blank" rel="noopener nofollow"><span>Visit website</span>{ic("globe")}</a>'
    if b.get('phone'):btns+=f'<a class="btn ghost" href="tel:{wa}">{ic("phone")} Call</a><a class="btn ghost" href="https://wa.me/{wa}" target="_blank" rel="noopener">{ic("chat")} WhatsApp</a>'
    if b.get('email'):btns+=f'<a class="btn ghost" href="mailto:{e(b["email"])}">{ic("mail")} Email</a>'
    if b.get('social'):btns+=f'<a class="btn ghost" href="{e(b["social"])}" target="_blank" rel="noopener nofollow">{ic("link")} Social</a>'
    sec=lambda t,x:f'<h2>{t}</h2>{x}' if x else ''
    ld='<script type="application/ld+json">'+json.dumps({'@context':'https://schema.org','@type':'Organization','name':b['name'],'description':b.get('tagline',''),'url':b.get('website') or None,'telephone':b.get('phone') or None,'email':b.get('email') or None,'address':b.get('address') or None})+'</script>'
    enq=form('Enquiry: '+b['name'],f'<input type="hidden" name="business" value="{e(b["name"])}">','<input name="name" placeholder="Your name" required><input name="phone" placeholder="Phone / WhatsApp" required><textarea name="message" placeholder="How can they help you?" required></textarea>','Send enquiry')
    body=f'''<section class="wrap sec art"><article><nav class="crumbs"><a href="{BASE}/">Home</a> / <a href="{BASE}/businesses/">Businesses</a></nav>
<div class="bhead card">{avatar(b,"lg")}<div><h1>{e(b["name"])}</h1><p class="mut">{e(b["category"])}{" &middot; "+e(b["city"]) if b.get("city") else ""}</p>{f'<p>{e(b["tagline"])}</p>' if b.get("tagline") else ''}<span class="ver">{ic("shield")} Verified</span></div></div>
<div class="content">{sec("About",MD(b["body"]))}{sec("How it works","<p>"+e(b.get("how_it_works","")).replace(chr(10),"<br>")+"</p>" if b.get("how_it_works") else "")}{sec("Products &amp; services","<ul>"+"".join(f"<li>{e(l)}</li>" for l in lines)+"</ul>" if lines else "")}</div></article>
<aside><div class="card"><h3>Contact</h3>{f'<p class="ci">{ic("pin")} {e(b["address"])}</p>' if b.get("address") else ''}{f'<p class="ci">{ic("phone")} {e(b["phone"])}</p>' if b.get("phone") else ''}{f'<p class="ci">{ic("mail")} {e(b["email"])}</p>' if b.get("email") else ''}<div class="stack">{btns}</div></div><div class="card"><h3>Send an enquiry</h3>{enq}</div></aside></section>'''
    W(f'businesses/{b["slug"]}/index.html',page(b['name'],(b.get('tagline') or b['body'])[:155],body,f'/businesses/{b["slug"]}/','website',ld))
# REGISTER
cats_opt=''.join(f'<option>{e(c)}</option>' for c in (bcats or ['Other Services']) if c)
reg_fields=f'''<div class="two"><label>Business / company name *<input name="business_name" required></label><label>Category<select name="category">{cats_opt}<option>Other</option></select></label></div>
<div class="two"><label>City<input name="city"></label><label>Tagline<input name="tagline" placeholder="One line about what you do"></label></div>
<label>Business description *<textarea name="description" required></textarea></label><label>How your business works<textarea name="how_it_works"></textarea></label><label>Products and services<textarea name="products" placeholder="One per line"></textarea></label>
<div class="two"><label>Website<input name="website" placeholder="https://"></label><label>Social media link<input name="social" placeholder="https://"></label></div>
<div class="two"><label>Email *<input type="email" name="email" required></label><label>Phone / WhatsApp<input name="phone"></label></div>
<div class="two"><label>Business address<input name="address"></label><label>Logo link (optional)<input name="logo_url" placeholder="Link to your logo image"></label></div>'''
W('register/index.html',page('Register Your Business','Submit your business to be listed in our verified directory.',f'<section class="wrap sec narrow"><span class="pill">{ic("shield")} Reviewed before publishing</span><h1>Register your business</h1><p class="mut">Submit your details. Our team reviews every submission and publishes approved profiles.</p><div class="card">{form("Business registration","",reg_fields,"Submit for approval")}</div></section>','/register/'))
W('404.html',page('Page not found','',f'<section class="wrap sec narrow tc"><h1>Page not found</h1><p class="mut">The page you are looking for does not exist.</p><a class="btn" href="{BASE}/">Go home</a></section>','/404.html',noindex=True))
urls=['/','/guides/','/businesses/','/register/']+[f'/guides/{g["slug"]}/' for g in G]+[f'/businesses/{b["slug"]}/' for b in B]
W('sitemap.xml','<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join(f'<url><loc>{ORIGIN}{BASE}{u}</loc><lastmod>{TODAY}</lastmod></url>' for u in urls)+'</urlset>')
W('robots.txt',f'User-agent: *\nDisallow: /admin/\nAllow: /\nSitemap: {ORIGIN}{BASE}/sitemap.xml\n')
print(len(urls)+1,'pages built')
