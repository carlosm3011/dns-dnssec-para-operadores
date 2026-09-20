#!/usr/bin/env python3
"""Build 07-DNSSEC-Avanzado.pptx from the lacnic46.pptx template."""
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from deck_helpers import (
    load_deck, get_placeholder, set_title, set_body_bullets, add_textbox,
    add_multiline_textbox, add_box, add_arrow, add_code_block, add_table,
    move_slide_to_end, RED, DARK, GRAY, LIGHTGRAY, WHITE, FONT, MONO,
)

prs, layouts = load_deck("lacnic46.pptx")

# ---------------------------------------------------------------------------
# Slide 1 (existing) -- Title
# ---------------------------------------------------------------------------
s1 = prs.slides[0]
s1.shapes.title.text_frame.paragraphs[0].runs[0].text = "Módulo 7: DNSSEC avanzado"
sub_ph = get_placeholder(s1, idx=1)
sub_ph.text_frame.paragraphs[0].text = ""
run = sub_ph.text_frame.paragraphs[0].add_run()
run.text = "Curso de DNS y DNSSEC para Operadores  —  Carlos Martinez"
run.font.size = Pt(18)
run.font.name = FONT

# ---------------------------------------------------------------------------
# Slide 2 (existing) -- Agenda
# ---------------------------------------------------------------------------
s2 = prs.slides[1]
set_title(s2, "Agenda del módulo")
body2 = get_placeholder(s2, idx=1)
set_body_bullets(body2, [
    "NSEC3 en profundidad",
    "Mecánica completa de rollovers",
    "Inspeccionar y operar rollovers en vivo",
    "Algorithm rollover",
    "CDS/CDNSKEY",
    "Multi-signer (RFC 8901, Model 2)",
], size=18, space_after=13)

# ---------------------------------------------------------------------------
# Slide 3 -- TITLE_AND_BODY: NSEC3, qué resuelve
# ---------------------------------------------------------------------------
s3 = prs.slides.add_slide(layouts["TITLE_AND_BODY"])
set_title(s3, "NSEC3 en profundidad")
body3 = get_placeholder(s3, idx=1)
set_body_bullets(body3, [
    "Existe para evitar zone walking — recorrer los NSEC de una zona y reconstruir todos los nombres",
    "Resuelve el mismo problema que NSEC (probar que un nombre no existe)",
    "En vez de encadenar nombres en texto plano, encadena sus hashes",
], size=18, space_after=15)

# ---------------------------------------------------------------------------
# Slide 4 -- TITLE_ONLY + table: nsec3param
# ---------------------------------------------------------------------------
s4 = prs.slides.add_slide(layouts["TITLE_ONLY"])
set_title(s4, "nsec3param: iterations, salt, opt-out")
add_table(s4, Inches(0.3), Inches(1.1), Inches(9.4), Inches(3.6), [
    ("Parámetro", "RFC 9276 recomienda", "Por qué"),
    ("iterations", "0", "Más iteraciones = costo de CPU para firmar y validar, con beneficio marginal"),
    ("salt-length", "0 (sin salt)", "No protege contra un atacante que ya puede consultar la zona"),
    ("optout", "no (salvo muchas delegaciones sin firmar)", "example.com no tiene delegaciones propias"),
], col_widths=[Inches(1.8), Inches(2.6), Inches(5.0)], size=12, header_size=13,
    first_col_bold=True, mono_cols={0})

# ---------------------------------------------------------------------------
# Slide 5 -- TITLE_ONLY: dnssec-policy con nsec3param
# ---------------------------------------------------------------------------
s5 = prs.slides.add_slide(layouts["TITLE_ONLY"])
set_title(s5, "Agregar NSEC3 a la política")
add_code_block(s5, Inches(0.4), Inches(1.1), Inches(9.2), Inches(3.5), [
    "dnssec-policy \"operadores\" {",
    "    keys { ... };",
    "    dnskey-ttl PT1H;",
    "    signatures-refresh P5D;",
    "    signatures-validity P2W;",
    "",
    "    nsec3param iterations 0 optout no salt-length 0;",
    "};",
], size=14)
add_multiline_textbox(s5, Inches(0.4), Inches(4.75), Inches(9.2), Inches(0.6), [
    "La ausencia de nsec3param en el módulo 4 implicaba NSEC — esto es lo único que cambia.",
], size=13, color=GRAY, italic=True)

# ---------------------------------------------------------------------------
# Slide 6 -- TITLE_ONLY: verificación NSEC3
# ---------------------------------------------------------------------------
s6 = prs.slides.add_slide(layouts["TITLE_ONLY"])
set_title(s6, "Verificación")
add_code_block(s6, Inches(0.4), Inches(1.1), Inches(9.2), Inches(3.4), [
    "$ dig @192.0.2.1 example.com NSEC3PARAM +dnssec +short",
    "1 0 0 -",
    "",
    "$ dig @192.0.2.1 nope.example.com A +dnssec",
    "b4c4z1n8...  3600 IN NSEC3 1 0 0 - ( c9d7e5f3... A RRSIG )",
], size=13)
add_multiline_textbox(s6, Inches(0.4), Inches(4.65), Inches(9.2), Inches(0.7), [
    "1 0 0 - = hash SHA-1, 0 flags, 0 iteraciones, salt vacío — exactamente lo que pide RFC 9276.",
], size=13, color=GRAY, italic=True)

# ---------------------------------------------------------------------------
# Slide 7 -- SECTION_TITLE_AND_DESCRIPTION: mecánica de rollovers
# ---------------------------------------------------------------------------
s7 = prs.slides.add_slide(layouts["SECTION_TITLE_AND_DESCRIPTION"])
set_title(s7, "Mecánica completa de rollovers")
sub7 = get_placeholder(s7, idx=1)
r = sub7.text_frame.paragraphs[0].add_run()
r.text = "Cómo es el proceso por dentro"
r.font.size = Pt(18)
r.font.name = FONT
body7 = get_placeholder(s7, idx=2)
set_body_bullets(body7, ["La línea de tiempo de una clave", "La máquina de estados de cada registro"], size=17)

# ---------------------------------------------------------------------------
# Slide 8 -- TITLE_AND_TWO_COLUMNS: dos capas
# ---------------------------------------------------------------------------
s8 = prs.slides.add_slide(layouts["TITLE_AND_TWO_COLUMNS"])
set_title(s8, "Dos capas, no una")
col1 = get_placeholder(s8, idx=1)
col2 = get_placeholder(s8, idx=2)
set_body_bullets(col1, [
    "Capa 1: la clave",
    ("Cuándo se generó, publicó, empezó a firmar, se retiró", 1),
    ("Se ve con dnssec-settime", 1),
], size=15, space_after=10, bullet_first=False)
col1.text_frame.paragraphs[0].runs[0].font.bold = True
col1.text_frame.paragraphs[0].runs[0].font.color.rgb = RED
set_body_bullets(col2, [
    "Capa 2: cada registro",
    ("DNSKEY, DS y RRSIG avanzan de forma independiente", 1),
    ("Es la que determina cuándo KASP da el siguiente paso", 1),
], size=15, space_after=10, bullet_first=False)
col2.text_frame.paragraphs[0].runs[0].font.bold = True
col2.text_frame.paragraphs[0].runs[0].font.color.rgb = RED

# ---------------------------------------------------------------------------
# Slide 9 -- TITLE_ONLY: la máquina de estados (diagram)
# ---------------------------------------------------------------------------
s9 = prs.slides.add_slide(layouts["TITLE_ONLY"])
set_title(s9, "La máquina de estados de un registro")
states = ["hidden\n(no publicado)", "rumoured\n(algunos cachés)", "omnipresent\n(todos los validadores)", "unretentive\n(se retiró)"]
bw = Inches(2.15)
bh = Inches(1.2)
gap = Inches(0.25)
x0 = Inches(0.4)
by = Inches(1.7)
for i, s in enumerate(states):
    x = x0 + i * (bw + gap)
    fill = RED if i == 2 else DARK
    add_box(s9, x, by, bw, bh, s, fill=fill, size=12)
    if i < 3:
        add_arrow(s9, x + bw, by + bh // 2, x + bw + gap, by + bh // 2)
add_multiline_textbox(s9, Inches(0.4), Inches(3.25), Inches(9.2), Inches(0.5), [
    "unretentive → vuelve a hidden una vez que expira de todos los cachés",
], size=13, color=GRAY, italic=True)
add_multiline_textbox(s9, Inches(0.4), Inches(4.0), Inches(9.2), Inches(1.0), [
    "Cada transición espera a que el estado anterior llegue a omnipresent (u hidden) antes de",
    "seguir — no alcanza con que pasen los días de la política.",
], size=14)

# ---------------------------------------------------------------------------
# Slide 10 -- TITLE_AND_BODY: ZSK pre-publish
# ---------------------------------------------------------------------------
s10 = prs.slides.add_slide(layouts["TITLE_AND_BODY"])
set_title(s10, "ZSK: estrategia pre-publish")
body10 = get_placeholder(s10, idx=1)
set_body_bullets(body10, [
    "1. Se publica el DNSKEY sucesor, todavía sin firmar nada",
    "2. Se espera a que llegue a omnipresent (TTL + publish-safety)",
    "3. named firma con la ZSK nueva; las RRSIG viejas quedan unretentive",
    "4. Al llegar a hidden, se borran del disco (purge-keys)",
], size=17, space_after=11)
add_multiline_textbox(s10, Inches(0.4), Inches(4.6), Inches(9.2), Inches(0.6), [
    "Sin depender del padre — KASP lo hace de punta a punta, sin intervención.",
], size=13, color=GRAY, italic=True)

# ---------------------------------------------------------------------------
# Slide 11 -- TITLE_AND_BODY: KSK double-KSK
# ---------------------------------------------------------------------------
s11 = prs.slides.add_slide(layouts["TITLE_AND_BODY"])
set_title(s11, "KSK: estrategia double-KSK")
body11 = get_placeholder(s11, idx=1)
set_body_bullets(body11, [
    "1. Se publica la KSK sucesora y enseguida firma el DNSKEY RRset junto con la vieja — doble firma real",
    "2. Al llegar a omnipresent, se sube el DS nuevo al padre — doble DS conviviendo",
    "3. Al confirmar que el DS viejo se retiró (-checkds), la KSK vieja pasa a unretentive",
], size=16, space_after=12)

# ---------------------------------------------------------------------------
# Slide 12 -- TITLE_ONLY: dnssec-settime
# ---------------------------------------------------------------------------
s12 = prs.slides.add_slide(layouts["TITLE_ONLY"])
set_title(s12, "dnssec-settime: la línea de tiempo")
add_code_block(s12, Inches(0.4), Inches(1.1), Inches(9.2), Inches(2.6), [
    "$ dnssec-settime -p all Kexample.com.+013+41230.key",
    "Created:    Wed Aug  5 09:12:00 2026",
    "Publish:    Wed Aug  5 09:12:00 2026",
    "Activate:   Wed Aug  5 10:12:00 2026",
    "Inactive:   Mon Nov  2 09:12:00 2026",
], size=13)
add_multiline_textbox(s12, Inches(0.4), Inches(4.0), Inches(9.2), Inches(0.6), [
    "Esto es la capa 1 — cuándo pasa cada cosa.",
], size=14, color=GRAY)

# ---------------------------------------------------------------------------
# Slide 13 -- TITLE_ONLY: el archivo .state
# ---------------------------------------------------------------------------
s13 = prs.slides.add_slide(layouts["TITLE_ONLY"])
set_title(s13, "El archivo .state: la capa 2")
add_code_block(s13, Inches(0.4), Inches(1.1), Inches(9.2), Inches(3.5), [
    "$ cat Kexample.com.+013+41230.state",
    "KSK: no",
    "ZSK: yes",
    "DNSKEYState: omnipresent",
    "ZRRSIGState: omnipresent",
    "GoalState: omnipresent",
], size=14)
add_multiline_textbox(s13, Inches(0.4), Inches(4.75), Inches(9.2), Inches(0.6), [
    "Justo lo esperado de una ZSK activa y estable — no hay rollover en curso.",
], size=13, color=GRAY, italic=True)

# ---------------------------------------------------------------------------
# Slide 14 -- TITLE_ONLY: rndc dnssec -status
# ---------------------------------------------------------------------------
s14 = prs.slides.add_slide(layouts["TITLE_ONLY"])
set_title(s14, "rndc dnssec -status: la vista operativa")
add_code_block(s14, Inches(0.4), Inches(1.1), Inches(9.2), Inches(4.0), [
    "$ sudo rndc dnssec -status example.com",
    "key: 41230 (ECDSAP256SHA256), ZSK",
    "  Key will retire on Mon Nov  2 09:12:00 2026",
    "  - goal: hidden   - dnskey: omnipresent   - zone rrsig: omnipresent",
    "",
    "key: 54915 (ECDSAP256SHA256), KSK",
    "  No rollover scheduled",
    "  - goal: omnipresent   - dnskey: omnipresent   - ds: omnipresent",
], size=13)

# ---------------------------------------------------------------------------
# Slide 15 -- TITLE_ONLY: forzar y confirmar a mano
# ---------------------------------------------------------------------------
s15 = prs.slides.add_slide(layouts["TITLE_ONLY"])
set_title(s15, "Forzar y confirmar un rollover a mano")
add_code_block(s15, Inches(0.4), Inches(1.15), Inches(9.2), Inches(2.6), [
    "# fuera de calendario — ej. sospecha de compromiso",
    "$ sudo rndc dnssec -rollover -key 41230 example.com",
    "",
    "# la parte que KASP no puede resolver solo",
    "$ sudo rndc dnssec -checkds -key 12345 published example.com",
    "$ sudo rndc dnssec -checkds -key 54915 withdrawn example.com",
], size=13)

# ---------------------------------------------------------------------------
# Slide 16 -- TITLE_AND_BODY: algorithm rollover, qué dispara
# ---------------------------------------------------------------------------
s16 = prs.slides.add_slide(layouts["TITLE_AND_BODY"])
set_title(s16, "Algorithm rollover")
body16 = get_placeholder(s16, idx=1)
set_body_bullets(body16, [
    "Cambia el algoritmo mismo, no solo las claves — ej. dejar atrás RSASHA256",
    "KASP genera KSK y ZSK nuevas en el algoritmo nuevo — conviven con las viejas",
    "La zona queda firmada con los dos algoritmos en simultáneo durante la transición",
    "El DS en el padre pasa por su propio período doble (mismo mecanismo double-KSK)",
], size=16, space_after=11)

# ---------------------------------------------------------------------------
# Slide 17 -- TITLE_ONLY: firma dual en dnssec-verify
# ---------------------------------------------------------------------------
s17 = prs.slides.add_slide(layouts["TITLE_ONLY"])
set_title(s17, "Firma dual, en dnssec-verify")
add_code_block(s17, Inches(0.4), Inches(1.15), Inches(9.2), Inches(2.6), [
    "$ dnssec-verify -o example.com /var/cache/bind/example.com.signed",
    "Verifying using: RSASHA256, ECDSAP256SHA256.",
    "Zone fully signed:",
    "Algorithm: RSASHA256:        KSKs: 1 active  ZSKs: 1 active",
    "Algorithm: ECDSAP256SHA256:  KSKs: 1 active  ZSKs: 1 active",
], size=13)
add_multiline_textbox(s17, Inches(0.4), Inches(4.05), Inches(9.2), Inches(0.8), [
    "Recién cuando el algoritmo viejo llega a hidden, KASP lo retira — la zona",
    "queda firmada únicamente con el nuevo.",
], size=14, color=GRAY)

# ---------------------------------------------------------------------------
# Slide 18 -- TITLE_AND_BODY: CDS/CDNSKEY
# ---------------------------------------------------------------------------
s18 = prs.slides.add_slide(layouts["TITLE_AND_BODY"])
set_title(s18, "CDS/CDNSKEY")
body18 = get_placeholder(s18, idx=1)
set_body_bullets(body18, [
    "Publicar el DS a mano (módulo 4) es un paso manual — CDS/CDNSKEY lo automatizan",
    "La zona hija publica en sí misma el contenido que el DS debería tener",
    "El padre (o el registrador) los consulta y actualiza el DS solo",
    "Limitación real: no todos los registradores/TLD hacen polling de CDS/CDNSKEY",
], size=16, space_after=11)

# ---------------------------------------------------------------------------
# Slide 19 -- TITLE_ONLY: activar y verificar CDS/CDNSKEY
# ---------------------------------------------------------------------------
s19 = prs.slides.add_slide(layouts["TITLE_ONLY"])
set_title(s19, "Activar y verificar")
add_code_block(s19, Inches(0.4), Inches(1.15), Inches(9.2), Inches(1.3), [
    "dnssec-policy \"operadores\" {",
    "    cdnskey yes;",
    "    cds-digest-types { \"SHA-256\"; };",
    "};",
], size=13)
add_code_block(s19, Inches(0.4), Inches(2.75), Inches(9.2), Inches(1.3), [
    "$ dig @192.0.2.1 example.com CDS +short",
    "54915 13 2 A94C3B1F...",
    "$ dig @192.0.2.1 example.com CDNSKEY +short",
    "257 3 13 ...base64...",
], size=13)

# ---------------------------------------------------------------------------
# Slide 20 -- TITLE_AND_BODY: multi-signer
# ---------------------------------------------------------------------------
s20 = prs.slides.add_slide(layouts["TITLE_AND_BODY"])
set_title(s20, "Multi-signer (RFC 8901, Model 2)")
body20 = get_placeholder(s20, idx=1)
set_body_bullets(body20, [
    "Dos o más proveedores DNS independientes, cada uno con su propio hidden signer y claves",
    "Cada proveedor incluye en su DNSKEY RRset las claves públicas de los demás",
    "El DS en el padre lista las KSK activas de todos los proveedores a la vez",
    "Lo difícil no es firmar — es coordinar el DNSKEY combinado en cada rollover",
], size=16, space_after=11)

# ---------------------------------------------------------------------------
# Slide 21 -- TITLE_ONLY + table: Resumen
# ---------------------------------------------------------------------------
s21 = prs.slides.add_slide(layouts["TITLE_ONLY"])
set_title(s21, "Resumen")
add_table(s21, Inches(0.3), Inches(1.0), Inches(9.4), Inches(4.1), [
    ("Concepto", "Qué logra"),
    ("nsec3param iterations 0 optout no salt-length 0", "NSEC3 según RFC 9276 — evita zone walking sin costo extra"),
    ("Estados hidden/rumoured/omnipresent/unretentive", "Determina cuándo KASP avanza un rollover"),
    ("Pre-publish (ZSK) vs. double-KSK (KSK)", "ZSK duplica el DNSKEY; KSK firma doble y duplica el DS"),
    ("rndc dnssec -status/-rollover/-checkds", "Ver, forzar y confirmar un rollover"),
    ("Algorithm rollover", "Transición con firma dual, misma máquina de estados"),
    ("cdnskey yes + cds-digest-types", "La zona publica lo que el DS debería ser"),
    ("Multi-signer (RFC 8901 Model 2)", "Redundancia entre proveedores DNS independientes"),
], col_widths=[Inches(3.6), Inches(5.8)], size=10.5, header_size=12, first_col_bold=True,
    mono_cols={0})

# ---------------------------------------------------------------------------
# Slide 22 -- MAIN_POINT: cierre del curso
# ---------------------------------------------------------------------------
s22 = prs.slides.add_slide(layouts["MAIN_POINT"])
set_title(s22, "De por qué existe DNSSEC a operarlo\nen producción — los 7 módulos, cerrados.")

# ---------------------------------------------------------------------------
# Move the closing "¡Gracias!" slide to the end
# ---------------------------------------------------------------------------
move_slide_to_end(prs, 2)

prs.save("07-DNSSEC-Avanzado-wip.pptx")
print("Module 7 done. Slide count:", len(prs.slides))
