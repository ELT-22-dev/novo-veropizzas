"""Gera o bloco "Cardápio completo" do index.html a partir dos dados abaixo.

Uso (na pasta do projeto):  python _ferramentas/gerar_cardapio.py

- Para mudar sabor ou preço: edite as listas abaixo e rode o comando.
- Fotos: salve em assets/cardapio/<nome>.webp (lista em assets/cardapio/LEIA-ME.txt)
  e rode o comando. Sem foto do sabor, usa a da categoria (cat-*.webp); sem nenhuma,
  aparece o espaço reservado. Pizzas salgadas, pizzas doces e esfihas são só lista, sem foto.

Dados copiados de veropizzas.com.br (cardapio-pizzas-e-esfihas.html e batata.html).
"""
import html, os, re, unicodedata
from urllib.parse import quote

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WA = '5511913339448'
FOTOS = 'assets/cardapio'

# ---------------------------------------------------------------- dados
# nome, descrição, grande, broto
SALGADAS = [
 ('Alho e Óleo','alho refogado no azeite e mussarela',44,34),
 ('Alemã','mussarela coberta com bacon e cebola',52,37),
 ('Aliche','mussarela com aliche e tomate',65,45),
 ('Americana','atum, palmito, ervilha, cebola e mussarela',52,37),
 ('Atum I','atum coberto com cebola',46,35),
 ('Atum II','atum, cebola, mussarela e tomate',52,37),
 ('Atum III','atum coberto com catupiry',54,39),
 ('Bacon','mussarela coberta com bacon e azeitona',52,37),
 ('Baiana I','calabresa moída, cebola, ovos, azeitona e pimenta',46,35),
 ('Baiana II','calabresa moída, cebola, mussarela, ovos e azeitona',52,37),
 ('Brasileira','atum, palmito, ovos, ervilha e cebola salpicada de mussarela',52,37),
 ('Brócolis','brócolis ao alho coberto com mussarela e bacon',53,39),
 ('Bauru','presunto, mussarela, tomate e orégano',48,35),
 ('Caipira','frango, catupiry e milho',53,39),
 ('Calabresa','calabresa fatiada e cebola',45,34),
 ('Calábria','mussarela, calabresa fatiada, cebola, alho frito e parmesão',52,37),
 ('Calamu','calabresa fatiada e mussarela',52,37),
 ('Catubresa','calabresa fatiada, cebola e catupiry',52,37),
 ('Catufrango','frango desfiado temperado e catupiry',52,37),
 ('Catulombo','lombo canadense com catupiry',53,39),
 ('Catumilho','milho coberto com catupiry',52,37),
 ('Catupiry','catupiry com rodelas de tomate',52,37),
 ('Champignon','champignon coberto com mussarela',53,39),
 ('Chilena','mussarela, presunto, palmito e ovos',52,37),
 ('Dois Queijos','mussarela e catupiry',47,35),
 ('Escarola','escarola refogada, bacon e mussarela',48,35),
 ('Eduardo','calabresa, bacon, tomate, mussarela e parmesão',53,39),
 ('Francesa','mussarela, presunto, ovos e catupiry',52,37),
 ('Jardineira','presunto, palmito, ervilha e mussarela',52,37),
 ('Lombo','lombo canadense e cebola',50,37),
 ('Margherita','mussarela, tomate, parmesão e manjericão',48,35),
 ('Milho','milho verde e mussarela',52,37),
 ('Moda Vero','mussarela, champignon, palmito e rodelas de tomate',53,39),
 ('Mussarela','mussarela com azeitona',45,34),
 ('Namorados','palmito, catupiry e mussarela',52,37),
 ('Napolitana','mussarela, rodelas de tomate e parmesão',47,35),
 ('Palmito','palmito coberto com mussarela',50,37),
 ('Penha','presunto, cebola, catupiry, palmito, mussarela e bacon',53,39),
 ('Peruana I','atum, cebola, ovos, mussarela e azeitonas',52,37),
 ('Peperone','peperone coberto com mussarela e rodelas de tomate',53,39),
 ('Portuguesa','presunto, cebola, ovos, ervilha e mussarela',54,39),
 ('Prima Vera','palmito, bacon, milho verde e mussarela',52,37),
 ('Quatro Queijos','mussarela, provolone, catupiry e parmesão',54,39),
 ('Romana','mussarela, aliche e rodelas de tomate',49,37),
 ('Romanesca','presunto, champignon, catupiry e parmesão',52,37),
 ('Rúcula','mussarela, rúcula e tomate seco',53,39),
 ('Siciliana','mussarela, bacon, champignon e parmesão',52,37),
 ('Toscana','mussarela e calabresa moída',52,37),
 ('Três Queijos','mussarela, parmesão e catupiry',48,35),
 ('Tropical','calabresa moída e palmito',53,39),
 ('Vegetariana','brócolis, champignon, milho verde, seleta de legumes, palmito, mussarela e tomate',55,39),
]
DOCES = [
 ('Banana','banana, leite condensado e canela',51),
 ('Brigadeiro','chocolate coberto com granulado',51),
 ('Prestígio','chocolate, leite condensado e coco ralado',51),
 ('Romeu e Julieta','mussarela e goiabada',51),
]
ESF_SAL = [('Carne',4.5),('Queijo',4.5),('Calabresa Moída',4),('Calabresa Fatiada',6),('Catupiry',4.5),
 ('Aliche',8),('Atum',6),('Catumilho',6),('Escarola',6),('Caipira',7),('Frango com Catupiry',6),('Bacon',6),
 ('Palmito',6),('Brócolis',6),('Espinafre c/ Mussarela',6),('Calabresa c/ Catupiry',6),('Especial',6),
 ('Carioca',6),('Quatro Queijos',7),('Portuguesa',7),('Napolitana',6),('Margherita',6)]
ESF_DOCE = [('Brigadeiro',6.5),('Banana',6.5),('Romeu e Julieta',6.5)]
PROMOS = [
 ('Promoção 1','10 esfihas','5 Carne + 5 Queijo',38),
 ('Promoção 2','10 esfihas','5 Carne + 5 Calabresa',38),
 ('Promoção 3','15 esfihas','5 Carne + 5 Queijo + 5 Calabresa',54),
 ('Promoção 4','21 esfihas','7 Carne + 7 Queijo + 7 Calabresa',70),
]
BEIRUTES = [
 ('Bauru','presunto, mussarela, tomate e azeitonas',33),
 ('Calabresa','mussarela, catupiry, maionese, cebola e ovos',33),
 ('Frango','mussarela, catupiry, maionese, milho e ovos',34),
 ('Lombo','catupiry, bacon e maionese',35),
]
CALZONES = [('Mussarela',45),('Calabresa com Bacon e Mussarela',51),('Quatro Queijos',54),
 ('Atum e Cebola',46),('Atum com Mussarela',51),('Calzone à sua Escolha',60)]
PASTEIS = [('Carne',10),('Queijo',10),('Catufrango',10)]
# tamanho, nome, preço, acompanhamentos, destaque
BATATAS = [
 ('P', 'Tradicional Vero', 15, ['Ketchup', 'Mostarda', 'Maionese', 'Queijo ralado', 'Cheddar ou Catupiry', 'Bacon ou Calabresa'], ''),
 ('M', 'Suprema Vero', 20, ['Ketchup', 'Mostarda', 'Maionese', 'Queijo ralado', 'Cheddar e Catupiry', 'Bacon e Calabresa'], ''),
 ('G', 'Explosão de Fritas Vero', 30, ['Ketchup', 'Mostarda', 'Maionese', 'Queijo ralado', 'Cheddar', 'Catupiry', 'Bacon', 'Calabresa'], 'MAIS COMPLETA'),
]
TAM = {'P': 'Pequena', 'M': 'Média', 'G': 'Grande'}
BEBIDAS = [('Cerveja', 'gelada'), ('Refrigerante 2 litros', ''), ('Refrigerante lata', '')]

# ---------------------------------------------------------------- helpers
e = html.escape
FOTO_LIST = []

def slug(s):
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode()
    return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')

def foto(prefix, name, cls='mphoto', fb=None):
    """Espaço de foto. Usa a foto do item; se não existir, a foto da categoria (fb);
    se nenhuma existir, mostra o espaço reservado. A checagem é feita aqui, na geração,
    para o site não pedir arquivos que não existem."""
    f = f'{FOTOS}/{prefix}-{slug(name)}.webp'
    cat = f'{FOTOS}/cat-{fb}.webp' if fb else None
    usa = next((x for x in (f, cat) if x and os.path.exists(os.path.join(ROOT, x))), None)
    FOTO_LIST.append((f, 'foto própria' if usa == f else ('usando foto da categoria' if usa else 'SEM FOTO')))
    if not usa:
        return f'<div class="{cls}" aria-hidden="true"></div>'
    return f'<div class="{cls} has-photo" style="background-image:url(\'{usa}\')" aria-hidden="true"></div>'

def wa(msg):
    return f'https://wa.me/{WA}?text=' + quote(msg, safe='')

def brl(v):
    return 'R$ ' + f'{v:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')

def buy(label, price, msg):
    return (f'<a class="buy" target="_blank" rel="noopener" href="{e(wa(msg))}">'
            f'<span>{e(label or "Pedir")}</span><b>{brl(price)}</b></a>')

def ask(msg):
    return (f'<a class="buy buy--ask" target="_blank" rel="noopener" href="{e(wa(msg))}">'
            f'<span>WhatsApp</span><b>Consultar</b></a>')

def item(prefix, name, desc, buys, fb=None, photo=True):
    d = f'<p>{e(desc)}</p>' if desc else ''
    ph = foto(prefix, name, fb=fb) if photo else ''
    return (f'<li class="mitem">{ph}<div class="mitem__txt"><h4>{e(name)}</h4>{d}</div>'
            f'<div class="mitem__buy">{buys}</div></li>')

def ul(items):
    return '<ul class="menu-list">' + ''.join(items) + '</ul>'

panels = []
def panel(key, label, inner, note=''):
    n = f'<p class="menu-note">{note}</p>' if note else ''
    panels.append((key, label, f'<div class="mpanel" id="tab-{key}" role="tabpanel" aria-labelledby="t-{key}" data-panel="{key}">{n}{inner}</div>'))

# ---------------------------------------------------------------- painéis
panel('pizzas', 'Pizzas Salgadas',
  ul(item('pizza', n, d, buy('Grande', g, f'Olá! Quero pedir uma pizza {n} (Grande) - {brl(g)}.') +
                         buy('Broto', b, f'Olá! Quero pedir uma pizza {n} (Broto) - {brl(b)}.'), photo=False) for n, d, g, b in SALGADAS) +
  '<ul class="extras"><li><b>Borda de catupiry</b> GRÁTIS todos os dias</li><li><b>Borda de cheddar</b> R$ 10,00</li><li><b>Cobertura extra</b> R$ 10,00</li></ul>',
  '51 sabores · todas acompanham molho de tomate, orégano e azeitonas · pizzas ½ a ½ cobradas pelo maior valor · '
  '<b>Broto</b> somente de 1 sabor (não fazemos meio a meio nesse tamanho)')
panel('doces', 'Pizzas Doces',
  ul(item('pizza-doce', n, d, buy('Grande', p, f'Olá! Quero pedir uma pizza doce {n} - {brl(p)}.'), photo=False) for n, d, p in DOCES))
panel('esfihas', 'Esfihas',
  '<h4 class="menu-sub">Esfihas salgadas</h4>' +
  ul(item('esfiha', n, '', buy('', p, f'Olá! Quero pedir esfiha de {n} - {brl(p)} cada.'), photo=False) for n, p in ESF_SAL) +
  '<h4 class="menu-sub">Esfihas doces <small>(só fechadas)</small></h4>' +
  ul(item('esfiha-doce', n, '', buy('', p, f'Olá! Quero pedir esfiha doce de {n} - {brl(p)} cada.'), photo=False) for n, p in ESF_DOCE),
  '22 sabores salgados e 3 doces · informe a quantidade de cada sabor no WhatsApp')
panel('promocoes-esfiha', 'Promoções',
  '<ul class="promos">' + ''.join(
    f'<li class="promo">{foto("promo", t, "pphoto", fb="esfiha")}<small>{e(t)}</small><strong>{e(q)}</strong><p>{e(c)}</p>'
    f'<a class="btn btn--gold" target="_blank" rel="noopener" href="{e(wa(f"Olá! Quero a {t} de esfihas ({c}) - {brl(p)}."))}">{brl(p)} · PEDIR</a></li>'
    for t, q, c, p in PROMOS) + '</ul>',
  'Promoções de esfihas válidas de terça a domingo')
panel('beirutes', 'Beirutes',
  ul(item('beirute', n, d, buy('', p, f'Olá! Quero pedir um beirute de {n} - {brl(p)}.'), fb='beirute') for n, d, p in BEIRUTES))
panel('calzones', 'Calzones',
  ul(item('calzone', n, '', buy('', p, f'Olá! Quero pedir um calzone {n} - {brl(p)}.'), fb='calzone') for n, p in CALZONES))
panel('pasteis', 'Pastéis',
  ul(item('pastel', n, '', buy('', p, f'Olá! Quero pedir um pastel de {n} - {brl(p)}.'), photo=False) for n, p in PASTEIS),
  '<b>Novidade!</b> Que tal um pastel frito na hora? Para começar: carne, queijo e catufrango')

bat = []
for tam, nome, preco, acomp, tag in BATATAS:
    badge = f'<em class="bcard__tag">{e(tag)}</em>' if tag else ''
    lis = ''.join(f'<li>{e(a)}</li>' for a in acomp)
    msg = f'Olá! Quero pedir a batata frita {nome} (tamanho {tam}) - {brl(preco)}.'
    bat.append(
      f'<li class="bcard{" bcard--hl" if tag else ""}">{badge}{foto("batata", nome, "bphoto")}'
      f'<div class="bcard__body"><small>TAMANHO {tam} · {TAM[tam].upper()}</small><h4>{e(nome)}</h4>'
      f'<p class="bcard__price">{brl(preco)}</p><p class="bcard__lbl">Acompanhamentos</p><ul class="bcard__acomp">{lis}</ul>'
      f'<a class="btn btn--wine" target="_blank" rel="noopener" href="{e(wa(msg))}"><svg><use href="#i-wa"/></svg>PEDIR {e(TAM[tam].upper())}</a></div></li>')
panel('batatas', 'Batata Frita',
  '<ul class="bcards">' + ''.join(bat) + '</ul>',
  '<b>Novidade!</b> Porções de batata frita para consumo na unidade ou delivery, no conforto da sua casa')

panel('bebidas', 'Bebidas',
  ul(item('bebida', n, d, ask(f'Olá! Quais opções de {n.lower()} vocês têm hoje?')) for n, d in BEBIDAS),
  'Consulte a disponibilidade de bebidas pelo WhatsApp ou no local')

tabs = ''.join(
  f'<button class="tab" type="button" role="tab" id="t-{k}" aria-controls="tab-{k}" '
  f'aria-selected="{"true" if i == 0 else "false"}" data-tab="{k}">{e(l)}</button>'
  for i, (k, l, _) in enumerate(panels))

FULL = f'''    <div class="fullmenu" id="cardapio-completo">
      <h3 class="fullmenu__title">Cardápio completo</h3>
      <div class="tabs" role="tablist" aria-label="Categorias do cardápio">{tabs}</div>
      {''.join(p for _, _, p in panels)}
      <p class="menu-foot">Valores sujeitos a alteração · Toque no preço e finalize o pedido direto no <b>WhatsApp</b> · Pagamento: PIX e cartão de crédito/débito</p>
    </div>'''

# ---------------------------------------------------------------- aplica
p = os.path.join(ROOT, 'index.html')
h = open(p, encoding='utf-8').read()
h, n = re.subn(r'    <div class="fullmenu" id="cardapio-completo">.*?\n    </div>(?=\n  </div>\n</section>)', lambda m: FULL, h, count=1, flags=re.S)
assert n == 1, 'bloco do cardápio não encontrado no index.html'
open(p, 'w', encoding='utf-8').write(h)

os.makedirs(os.path.join(ROOT, FOTOS), exist_ok=True)
with open(os.path.join(ROOT, FOTOS, 'LEIA-ME.txt'), 'w', encoding='utf-8') as f:
    f.write('FOTOS DO CARDÁPIO\n=================\n'
            'Salve a foto nesta pasta com exatamente o nome abaixo (.webp) e rode:\n'
            '    python _ferramentas/gerar_cardapio.py\n'
            'Fotos "cat-*.webp" valem para a categoria inteira (usadas quando o sabor não tem foto própria).\n'
            'Pizzas salgadas, pizzas doces e esfihas não têm foto (lista simples).\n\n')
    f.write('\n'.join(f'{os.path.basename(x):45} {st}' for x, st in FOTO_LIST) + '\n')

print(f'ok: {h.count(chr(34) + "mitem" + chr(34))} itens de lista, {len(BATATAS)} batatas, {len(FOTO_LIST)} espaços de foto')
