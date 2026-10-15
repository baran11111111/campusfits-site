# campusfits.com sayfalarını üretir: index.html (sablon.html'den) ve yasal sayfalar (yasal.json'dan).
# yasal.json uygulamadaki src/app/yasal/[doc].tsx metinlerinden çıkarılır; uygulama ile site aynı metni gösterir.
# Çalıştır: python3 olustur.py
import html, json

ROOT = __file__.rsplit('/', 1)[0]
read = lambda p: open(f'{ROOT}/{p}', encoding='utf-8').read()
write = lambda p, s: open(f'{ROOT}/{p}', 'w', encoding='utf-8').write(s)
esc = html.escape

SUPPORT = 'destek@campusfits.com'

# Sadece kendi dosyaları, Google Fonts ve satır içi stil. Hiç betik yok; form gönderimi ve çerçeveye alınma kapalı.
CSP = ("default-src 'self'; script-src 'none'; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
       "font-src https://fonts.gstatic.com; img-src 'self' data:; connect-src 'none'; object-src 'none'; "
       "base-uri 'self'; form-action 'none'; frame-src 'none'; manifest-src 'self'")
SECURITY_META = (f'<meta http-equiv="Content-Security-Policy" content="{CSP}">\n'
                 '<meta name="referrer" content="strict-origin-when-cross-origin">\n')

FOOTER_LINKS = ('<a href="gizlilik.html">Gizlilik</a><a href="kosullar.html">Kullanım koşulları</a>'
                '<a href="cocuk-guvenligi.html">Çocuk güvenliği</a><a href="destek.html">Destek</a>')

# ───── Ana sayfa ─────
index = read('sablon.html')
uni = json.load(open(f'{ROOT}/universiteler.json', encoding='utf-8'))
names = [u for u in uni if 'Üniversite' in u]
index = index.replace('{{UNIS}}', ''.join(f'<span>{esc(n)}</span>' for n in names))
index = index.replace('{{UNI_COUNT}}', str(len(uni)))
index = index.replace('<meta charset="utf-8">\n', '<meta charset="utf-8">\n' + SECURITY_META, 1)
index = index.replace('<nav aria-label="Alt bağlantılar"><a href="gizlilik.html">Gizlilik</a><a href="kosullar.html">Kullanım koşulları</a><a href="destek.html">Destek</a></nav>',
                      f'<nav aria-label="Alt bağlantılar">{FOOTER_LINKS}</nav>')
write('index.html', index)

# ───── Yasal sayfalar ─────
docs = json.load(open(f'{ROOT}/yasal.json', encoding='utf-8'))

PAGE = '''<!doctype html>
<html lang="tr">
<head>
<meta charset="utf-8">
{security}<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title} · CampusFits</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#0A0A0C">
<link rel="icon" href="img/icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Figtree:wght@400;500;600;700&family=Unbounded:wght@700;800&family=JetBrains+Mono:wght@400&display=swap">
<style>
:root {{ --ink: #F6F6F7; --bg: #0A0A0C; --card: #151518; --muted: #8E8E95; --cream: #F2EEC0; --hair: rgba(255,255,255,0.08);
  --display: "Unbounded", "Arial Black", system-ui, sans-serif; --body: "Figtree", system-ui, -apple-system, "Segoe UI", sans-serif;
  --mono: "JetBrains Mono", ui-monospace, Menlo, monospace; color-scheme: dark; }}
* {{ box-sizing: border-box; }}
body {{ margin: 0; background: var(--bg); color: var(--ink); font-family: var(--body); font-size: 17px; line-height: 1.65; -webkit-font-smoothing: antialiased; }}
a {{ color: var(--cream); }}
:focus-visible {{ outline: 2px solid var(--cream); outline-offset: 3px; border-radius: 6px; }}
.in {{ max-width: 760px; margin: 0 auto; padding-inline: clamp(18px, 5vw, 40px); }}
header {{ border-bottom: 1px solid var(--hair); }}
header .in {{ max-width: 1180px; display: flex; justify-content: space-between; align-items: center; gap: 16px; padding-block: 16px; }}
.logo {{ font-family: var(--display); font-weight: 800; font-size: 22px; letter-spacing: -0.03em; display: inline-flex; align-items: baseline; text-decoration: none; color: var(--ink); }}
.logo .bld {{ width: 0.62em; height: 0.74em; margin: 0 0.06em; flex: none; transform: translateY(0.02em); }}
header nav {{ display: flex; gap: 18px; flex-wrap: wrap; font-size: 15px; }}
header nav a {{ color: var(--muted); text-decoration: none; }}
main {{ padding-block: 56px 80px; }}
.eyebrow {{ font-family: var(--mono); font-size: 12px; letter-spacing: 0.14em; text-transform: uppercase; color: var(--muted); margin: 0; }}
h1 {{ font-family: var(--display); font-weight: 800; font-size: clamp(30px, 5vw, 46px); line-height: 1.05; letter-spacing: -0.03em; margin: 12px 0 0; text-wrap: balance; }}
.intro {{ color: var(--muted); font-size: 18px; margin: 18px 0 0; }}
.note {{ margin: 28px 0 0; padding: 14px 16px; border-radius: 14px; background: var(--card); color: var(--muted); font-size: 15px; }}
h2 {{ font-size: 20px; font-weight: 700; margin: 44px 0 0; letter-spacing: -0.01em; }}
h2 + p, h2 + ul {{ margin-top: 10px; }}
p {{ margin: 10px 0 0; }}
ul {{ margin: 10px 0 0; padding-left: 20px; }}
li {{ margin-top: 6px; }}
.doc + .doc {{ margin-top: 72px; padding-top: 48px; border-top: 1px solid var(--hair); }}
.steps {{ counter-reset: s; list-style: none; padding: 0; }}
.steps li {{ counter-increment: s; display: grid; grid-template-columns: 36px minmax(0, 1fr); gap: 12px; margin-top: 14px; }}
.steps li::before {{ content: counter(s); font-family: var(--mono); font-size: 13px; width: 28px; height: 28px; border-radius: 50%; background: var(--card); display: grid; place-items: center; color: var(--cream); }}
.mail {{ font-family: var(--mono); font-size: 16px; background: var(--card); padding: 3px 10px; border-radius: 8px; user-select: all; }}
footer {{ border-top: 1px solid var(--hair); }}
footer .in {{ max-width: 1180px; display: flex; flex-wrap: wrap; justify-content: space-between; gap: 16px 40px; padding-block: 36px; font-size: 14px; color: var(--muted); }}
footer nav {{ display: flex; gap: 20px; flex-wrap: wrap; }}
footer nav a {{ color: var(--muted); text-decoration: none; }}
@media (max-width: 640px) {{ header nav {{ display: none; }} }}
</style>
</head>
<body>
<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>
<linearGradient id="neon" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#FFD23F"/><stop offset="0.5" stop-color="#FF5F6D"/><stop offset="1" stop-color="#7B5CFF"/></linearGradient>
<symbol id="bina" viewBox="0 0 62 74"><path d="M0 20.7L31 0L62 20.7Z" fill="url(#neon)"/><rect x="2.5" y="22.9" width="57" height="5.9" fill="url(#neon)"/><rect x="6.2" y="31.8" width="7.4" height="31.8" fill="url(#neon)"/><rect x="20.5" y="31.8" width="7.4" height="31.8" fill="url(#neon)"/><rect x="34.7" y="31.8" width="7.4" height="31.8" fill="url(#neon)"/><rect x="48.9" y="31.8" width="7.4" height="31.8" fill="url(#neon)"/><rect x="0" y="65.9" width="62" height="8.1" fill="url(#neon)"/></symbol>
</defs></svg>
<header><div class="in">
  <a class="logo" href="index.html" aria-label="CampusFits ana sayfa">campusf<svg class="bld" viewBox="0 0 62 74" aria-hidden="true"><use href="#bina"/></svg>ts</a>
  <nav aria-label="Sayfalar">{nav}</nav>
</div></header>
<main><div class="in">
{body}
</div></main>
<footer><div class="in"><span>© 2026 CampusFits · Baran Uygun tarafından geliştirildi.</span><nav aria-label="Alt bağlantılar">{nav}</nav></div></footer>
</body>
</html>
'''


def doc_html(key, eyebrow):
    d = docs[key]
    out = [f'<section class="doc" id="{key}">', f'<p class="eyebrow">{esc(eyebrow)}</p>', f'<h1>{esc(d["title"])}</h1>']
    if d.get('intro'):
        out.append(f'<p class="intro">{esc(d["intro"])}</p>')
    for s in d['sections']:
        out.append(f'<h2>{esc(s["h"])}</h2>')
        if len(s['p']) > 1:
            out.append('<ul>' + ''.join(f'<li>{esc(p)}</li>' for p in s['p']) + '</ul>')
        else:
            out.append(f'<p>{esc(s["p"][0])}</p>')
    out.append('</section>')
    return '\n'.join(out)


def page(path, title, desc, body):
    write(path, PAGE.format(security=SECURITY_META, title=esc(title), desc=esc(desc), nav=FOOTER_LINKS, body=body))


TASLAK = '<p class="note">Son güncelleme: Ekim 2026. Sorun ve talepler için <span class="mail">' + SUPPORT + '</span></p>'

page('gizlilik.html', 'Gizlilik', 'CampusFits KVKK aydınlatma metni ve açık rıza metinleri.',
     doc_html('kvkk', 'Gizlilik') + TASLAK + '\n' + doc_html('acik-riza', 'İsteğe bağlı'))
page('kosullar.html', 'Kullanım koşulları', 'CampusFits kullanım koşulları ve topluluk kuralları.',
     doc_html('kosullar', 'Koşullar') + TASLAK + '\n' + doc_html('topluluk', 'Topluluk'))
page('cocuk-guvenligi.html', 'Çocuk güvenliği', 'CampusFits çocuk güvenliği standartları.',
     doc_html('cocuk-guvenligi', 'Güvenlik') + TASLAK)

destek = f'''<section class="doc">
<p class="eyebrow">Destek</p>
<h1>Nasıl yardımcı olabiliriz?</h1>
<p class="intro">Sorun, öneri, şikâyet ya da hesap talebi için bize yaz. Şikâyetleri 24 saat içinde inceliyoruz.</p>
<h2>İletişim</h2>
<p><span class="mail">{SUPPORT}</span></p>
<p>Uygulamanın içinden de yazabilirsin: Ayarlar → Destek.</p>
<h2 id="hesap-silme">Hesabını silmek</h2>
<ol class="steps">
<li>Uygulamada sağ alttaki profil fotoğrafına, ardından Ayarlar'a dokun.</li>
<li>En alttaki "Hesabımı sil"e dokun ve onayla.</li>
<li>Profilin, mesajların, anlıkların, planların ve fotoğrafların silinir. Kanunen saklamamız gereken kayıtlar (ör. şikâyet kayıtları) dışında hiçbir veri kalmaz.</li>
</ol>
<p>Uygulamaya giremiyorsan kayıtlı mail adresinden <span class="mail">{SUPPORT}</span> adresine "Hesabımı silin" diye yaz; hesabını 30 gün içinde sileriz.</p>
<h2>Şikâyet ve güvenlik</h2>
<p>Bir mesajı, anlığı ya da profili uygulamanın içinden şikâyet edebilir ve kişiyi engelleyebilirsin. Acil bir tehlike varsa önce 112'yi ara.</p>
<h2>Sık sorulanlar</h2>
<p>Doğrulama, konum ve anlıklarla ilgili cevaplar <a href="index.html#sss">ana sayfadaki sorular</a> bölümünde.</p>
</section>'''
page('destek.html', 'Destek', 'CampusFits destek, iletişim ve hesap silme.', destek)
print('tamam')
