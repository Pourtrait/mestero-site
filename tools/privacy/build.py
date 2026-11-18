"""Build the privacy policy pages: privacy/index.html (English) and privacy/<code>/index.html.
Text lives in tools/privacy/<code>.json (a list, same order as en.json). Run: python3 tools/privacy/build.py"""
import json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
# code, folder, picker name, html lang, og locale
LANGS = [
    ('en', '', 'English', 'en', 'en_GB'),
    ('de', 'de', 'Deutsch', 'de', 'de_DE'),
    ('fr', 'fr', 'Français', 'fr', 'fr_FR'),
    ('es', 'es', 'Español', 'es', 'es_ES'),
    ('pt', 'pt', 'Português', 'pt', 'pt_PT'),
    ('it', 'it', 'Italiano', 'it', 'it_IT'),
    ('nl', 'nl', 'Nederlands', 'nl', 'nl_NL'),
    ('pl', 'pl', 'Polski', 'pl', 'pl_PL'),
    ('da', 'da', 'Dansk', 'da', 'da_DK'),
]
URL = 'https://mestero.com/privacy'
IDS = ['who', 'games', 'collect', 'use', 'ads', 'partners', 'legal', 'children', 'retention', 'rights', 'delete', 'transfers', 'security', 'us', 'changes', 'contact']

CSS = open(os.path.join(HERE, 'style.css'), encoding='utf-8').read().strip()

# Picks the page for the visitor's browser language on the first visit; a choice made in the
# picker is remembered and always wins. Search engines and visitors with no match stay on English.
DETECT = """<script>
(function(){
  var K='mestero_privacy_lang', have=%s, here=%s, saved=null;
  try{saved=localStorage.getItem(K);}catch(e){}
  if(location.search.indexOf('lang=')>=0){var q=(location.search.match(/lang=([a-z-]+)/i)||[])[1];if(q){try{localStorage.setItem(K,q);}catch(e){} saved=q;}}
  var pick=saved;
  if(!pick){var l=(navigator.languages&&navigator.languages.length?navigator.languages:[navigator.language||'en']);
    for(var i=0;i<l.length&&!pick;i++){var b=String(l[i]).toLowerCase().split('-')[0];if(have.indexOf(b)>=0)pick=b;}}
  if(pick&&pick!==here&&have.indexOf(pick)>=0){location.replace((pick==='en'?'%s':'%s'+pick+'/')+location.hash);}
})();
</script>"""


def page(code, folder, T, en):
    up = '../' if not folder else '../../'
    base = up + 'privacy/'
    have = [l[0] for l in LANGS]
    lang_html = [l for l in LANGS if l[0] == code][0][3]
    s = lambda i: T[i]
    heads = T[5:21]
    alt = '\n'.join('<link rel="alternate" hreflang="%s" href="%s%s">' % (l[3], URL, '/' + l[1] + '/' if l[1] else '') for l in LANGS)
    alt += '\n<link rel="alternate" hreflang="x-default" href="%s">' % URL
    picker = '<label class="lang"><span class="sr">%s</span><select aria-label="%s" onchange="try{localStorage.setItem(\'mestero_privacy_lang\',this.value)}catch(e){};location.href=this.value===\'en\'?\'%s\':\'%s\'+this.value+\'/\'">%s</select></label>' % (
        T[77], T[77], base, base, ''.join('<option value="%s"%s>%s</option>' % (l[0], ' selected' if l[0] == code else '', l[2]) for l in LANGS))
    note = '' if code == 'en' else '<p class="note">%s</p>\n' % T[76]
    toc = '\n'.join('<li><a href="#%s">%s</a></li>' % (IDS[i], heads[i]) for i in range(16))
    H = lambda i: '<h2 id="%s">%d. %s</h2>' % (IDS[i], i + 1, heads[i])
    ul = lambda a, b: '<ul>\n' + '\n'.join('<li>%s</li>' % T[i] for i in range(a, b)) + '\n</ul>'
    partners = [('Google AdMob', '<a href="https://policies.google.com/technologies/partner-sites" rel="noopener">policies.google.com/technologies/partner-sites</a>'),
                (None, None),
                ('GameAnalytics', '<a href="https://gameanalytics.com/privacy/" rel="noopener">gameanalytics.com/privacy</a>'),
                ('RevenueCat', '<a href="https://www.revenuecat.com/privacy/" rel="noopener">revenuecat.com/privacy</a>'),
                ('Google Firebase', '<a href="https://firebase.google.com/support/privacy" rel="noopener">firebase.google.com/support/privacy</a>'),
                ('Tenjin', '<a href="https://www.tenjin.com/privacy/" rel="noopener">tenjin.com/privacy</a>'),
                (T[57], '<a href="https://policies.google.com/privacy" rel="noopener">policies.google.com/privacy</a>, <a href="https://www.apple.com/legal/privacy/" rel="noopener">apple.com/legal/privacy</a>')]
    purposes = [T[51], T[52], T[53], T[54], T[55], T[56], T[58]]
    names = ['Google AdMob', T[78], 'GameAnalytics', 'RevenueCat', 'Google Firebase', 'Tenjin', T[57]]
    links = [partners[0][1], T[79]] + [l for _, l in partners[2:]]
    rows = ['<tr><td>%s</td><td>%s</td><td>%s</td></tr>' % (names[k], purposes[k], links[k]) for k in range(7)]
    head = T[50].split('|')
    gh = T[23].split('|')
    out = f"""<!doctype html>
<html lang="{lang_html}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{s(0)} | Mestero Games</title>
<meta name="description" content="{s(1)}">
<link rel="canonical" href="{URL}{'/' + folder + '/' if folder else ''}">
{alt}
<link rel="icon" href="{up}assets/favicon.svg" type="image/svg+xml">
<link rel="icon" href="{up}assets/favicon-32.png" sizes="32x32" type="image/png">
{DETECT % (json.dumps(have), json.dumps(code), base, base)}
<style>
{CSS.replace('../assets/', up + 'assets/')}
</style>
</head>
<body>
<header class="site-header">
<div class="nav">
<a href="{up}" aria-label="Mestero Games home"><img src="{up}assets/mestero-wordmark-peek-games-reversed.svg" alt="Mestero Games" width="150" height="42"></a>
<div class="navr">{picker}<a class="home" href="{up}">{s(2)}</a></div>
</div>
</header>

<main class="wrap">
<h1>{s(0)}</h1>
<p class="meta">{s(3)}</p>
{note}
<p>{s(4)}</p>

<div class="toc">
<ol>
{toc}
</ol>
</div>

{H(0)}
<p>{s(21)}</p>

{H(1)}
<p>{s(22)}</p>
<div class="table-box">
<table>
<thead><tr><th>{gh[0]}</th><th>{gh[1]}</th><th>{gh[2]}</th></tr></thead>
<tbody>
<tr><td>Pourtrait</td><td>{s(24)}</td><td>{s(80)}</td></tr>
</tbody>
</table>
</div>
<p>{s(25)}</p>

{H(2)}
<p>{s(26)}</p>
<h3>{s(27)}</h3>
{ul(28, 32)}
<h3>{s(32)}</h3>
{ul(33, 35)}
<h3>{s(35)}</h3>
<p>{s(36)}</p>

{H(3)}
{ul(37, 43)}
<p>{s(43)}</p>

{H(4)}
<p>{s(44)}</p>
{ul(45, 48)}
<p>{s(48)}</p>

{H(5)}
<p>{s(49)}</p>
<div class="table-box">
<table>
<thead><tr><th>{head[0]}</th><th>{head[1]}</th><th>{head[2]}</th></tr></thead>
<tbody>
{chr(10).join(rows)}
</tbody>
</table>
</div>
<p>{s(59)}</p>

{H(6)}
{ul(60, 64)}

{H(7)}
<p>{s(64)}</p>

{H(8)}
<p>{s(65)}</p>

{H(9)}
<p>{s(66)}</p>

{H(10)}
<p>{s(67)}</p>
<ol>
<li>{s(68)}</li>
<li>{s(69)}</li>
</ol>
<p>{s(70)}</p>

{H(11)}
<p>{s(71)}</p>

{H(12)}
<p>{s(72)}</p>

{H(13)}
<p>{s(73)}</p>

{H(14)}
<p>{s(74)}</p>

{H(15)}
<p>{s(75)}</p>
</main>

<footer>
<div class="wrap">{s(81)} <a href="{up}">mestero.com</a></div>
</footer>
</body>
</html>
"""
    d = os.path.join(ROOT, 'privacy', folder) if folder else os.path.join(ROOT, 'privacy')
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, 'index.html'), 'w', encoding='utf-8').write(out)


en = json.load(open(os.path.join(HERE, 'en.json'), encoding='utf-8'))
for code, folder, *_ in LANGS:
    p = os.path.join(HERE, code + '.json')
    if not os.path.exists(p): print('skip', code); continue
    T = json.load(open(p, encoding='utf-8'))
    assert len(T) == len(en), (code, len(T), len(en))
    for i, (a, b) in enumerate(zip(en, T)):  # keep every link and bold in place
        if sorted(re.findall(r'<(\w+)', a)) != sorted(re.findall(r'<(\w+)', b)) or a.count('href') != b.count('href'):
            raise SystemExit(f'{code} line {i}: tags differ')
    page(code, folder, T, en)
    print('built', code)
