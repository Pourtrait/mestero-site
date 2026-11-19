"""One privacy/index.html holding all languages (no extra folders).
Reads the per-language pages built by build.py and merges them; shows the visitor's language.
Run after build.py: python3 tools/privacy/single.py  -> writes privacy/index.html"""
import os, re, json
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
LANGS = [('en', 'English'), ('de', 'Deutsch'), ('fr', 'Français'), ('es', 'Español'), ('pt', 'Português'),
         ('it', 'Italiano'), ('nl', 'Nederlands'), ('pl', 'Polski'), ('da', 'Dansk')]
def src(code): return open(os.path.join(ROOT, 'privacy', '' if code == 'en' else code, 'index.html'), encoding='utf-8').read()
en = src('en')
head = en[:en.index('<script>')]                       # doctype, meta, links (English)
head = re.sub(r'<link rel="alternate"[^>]*>\n?', '', head)
style = en[en.index('<style>'):en.index('</style>') + 8]
blocks, titles, homes = [], {}, {}
for code, name in LANGS:
    h = src(code)
    main = h[h.index('<main class="wrap">') + len('<main class="wrap">'):h.index('</main>')]
    foot = h[h.index('<footer>') + 8:h.index('</footer>')]
    titles[code] = re.search(r'<title>(.*?)</title>', h).group(1)
    homes[code] = re.search(r'<a class="home" href="[^"]*">(.*?)</a>', h).group(1)
    if code != 'en':  # ids stay unique: #delete in English, #fr-delete in French
        main = re.sub(r'id="([a-z]+)"', lambda m: 'id="%s-%s"' % (code, m.group(1)), main)
        main = re.sub(r'href="#([a-z]+)"', lambda m: 'href="#%s-%s"' % (code, m.group(1)), main)
    hidden = '' if code == 'en' else ' hidden'
    blocks.append('<div class="lp" data-l="%s" lang="%s"%s>\n<main class="wrap">%s</main>\n<footer>%s</footer>\n</div>' % (code, code, hidden, main, foot))
opts = ''.join('<option value="%s">%s</option>' % (c, n) for c, n in LANGS)
script = """<script>
(function(){
  var K='mestero_privacy_lang', T=%s, H=%s, have=Object.keys(T), pick=null;
  try{pick=localStorage.getItem(K);}catch(e){}
  var q=(location.search.match(/lang=([a-z]+)/i)||[])[1]; if(q&&have.indexOf(q)>=0){pick=q;try{localStorage.setItem(K,q);}catch(e){}}
  if(have.indexOf(pick)<0){pick=null;var l=navigator.languages&&navigator.languages.length?navigator.languages:[navigator.language||'en'];
    for(var i=0;i<l.length&&!pick;i++){var b=String(l[i]).toLowerCase().split('-')[0];if(have.indexOf(b)>=0)pick=b;}}
  pick=pick||'en';
  var sel=document.getElementById('lang');
  function show(c){
    document.querySelectorAll('.lp').forEach(function(d){d.hidden=d.getAttribute('data-l')!==c;});
    document.documentElement.lang=c; document.title=T[c]; sel.value=c;
    document.getElementById('home').textContent=H[c];
  }
  sel.onchange=function(){try{localStorage.setItem(K,sel.value);}catch(e){} show(sel.value); scrollTo(0,0);};
  show(pick);
  // old links like /privacy#delete open the same section in the visitor's language
  var h=location.hash.slice(1);
  if(h&&pick!=='en'&&!/-/.test(h)){var t=document.getElementById(pick+'-'+h);if(t)setTimeout(function(){t.scrollIntoView();},0);}
})();
</script>""" % (json.dumps(titles, ensure_ascii=False), json.dumps(homes, ensure_ascii=False))
header = en[en.index('<header'):en.index('</header>') + 9]
header = re.sub(r'<label class="lang">.*?</label>', '<label class="lang"><span class="sr">Language</span><select id="lang" aria-label="Language">%s</select></label>' % opts, header, flags=re.S)
header = re.sub(r'<a class="home" ', '<a class="home" id="home" ', header)
out = head + style + '\n</head>\n<body>\n' + header + '\n\n' + '\n\n'.join(blocks) + '\n' + script + '\n</body>\n</html>\n'
out = out.replace('<link rel="canonical" href="https://mestero.com/privacy">', '<link rel="canonical" href="https://mestero.com/privacy">')
os.makedirs(os.path.join(ROOT, 'out'), exist_ok=True)
open(os.path.join(ROOT, 'out', 'privacy-index.html'), 'w', encoding='utf-8').write(out)
print(len(out))

# Usage: python3 tools/privacy/build.py (one page per language, kept out of the site) then python3 tools/privacy/single.py (writes out/privacy-index.html = the live privacy/index.html)
