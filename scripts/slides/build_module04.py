#!/usr/bin/env python3
"""Build 04-Firmando-con-BIND-y-KASP.pptx from the lacnic46.pptx template."""
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
s1.shapes.title.text_frame.paragraphs[0].runs[0].text = "Módulo 4: Firmando una zona con BIND y KASP"
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
    "Repaso: KSK vs ZSK, y por qué el rollover",
    "Qué es KASP",
    "Migrar el primario a firmado inline",
    "Configurar una dnssec-policy y firmar",
    "Verificación de la firma",
    "Publicar el DS en el padre",
], size=18, space_after=13)

# ---------------------------------------------------------------------------
# Slide 3 -- TITLE_AND_BODY: repaso KSK/ZSK y por qué el rollover
# ---------------------------------------------------------------------------
s3 = prs.slides.add_slide(layouts["TITLE_AND_BODY"])
set_title(s3, "Repaso: KSK vs ZSK, y por qué el rollover")
body3 = get_placeholder(s3, idx=1)
set_body_bullets(body3, [
    "El DS en el padre apunta al hash de la KSK, no de la ZSK",
    "Rotar la ZSK es interno a la zona — no toca nada en el padre",
    "Rotar la KSK implica actualizar el DS: un paso manual, fuera del control de la zona",
    "Por eso la ZSK rota seguido y la KSK se mantiene estable",
], size=17, space_after=13)

# ---------------------------------------------------------------------------
# Slide 4 -- TITLE_AND_BODY: qué es KASP
# ---------------------------------------------------------------------------
s4 = prs.slides.add_slide(layouts["TITLE_AND_BODY"])
set_title(s4, "Qué es KASP")
body4 = get_placeholder(s4, idx=1)
set_body_bullets(body4, [
    "Key and Signing Policy — automatiza todo el ciclo de vida de claves y firma",
    "Generación, publicación, uso, rotación y retiro, sin dnssec-keygen/dnssec-signzone a mano",
    "Una dnssec-policy es un perfil reutilizable: algoritmo, tiempos de vida, parámetros de firma",
], size=18, space_after=14)

# ---------------------------------------------------------------------------
# Slide 5 -- TITLE_ONLY: migrar a inline-signing (diagram)
# ---------------------------------------------------------------------------
s5 = prs.slides.add_slide(layouts["TITLE_ONLY"])
set_title(s5, "Migrar el primario a firmado inline")
bw = Inches(2.7)
bh = Inches(1.1)
gap = Inches(0.4)
x0 = Inches(0.4)
by = Inches(1.5)
add_box(s5, x0, by, bw, bh, "db.example.com\n(fuente sin firmar,\nla editás vos)", fill=DARK, size=12)
add_arrow(s5, x0 + bw, by + bh // 2, x0 + bw + gap, by + bh // 2)
add_box(s5, x0 + bw + gap, by, bw, bh, "copia firmada\n(gestionada por named)", fill=RED, size=12)
add_arrow(s5, x0 + 2 * bw + gap, by + bh // 2, x0 + 2 * bw + 2 * gap, by + bh // 2)
add_box(s5, x0 + 2 * (bw + gap), by, bw, bh, "Secundario\n(AXFR/IXFR, sin cambios)", fill=DARK, size=12)
add_multiline_textbox(s5, Inches(0.4), Inches(3.0), Inches(9.2), Inches(0.9), [
    "El archivo que editás a mano pasa a ser la fuente sin firmar; named mantiene",
    "por separado la copia firmada, y es esa la que se responde y se transfiere.",
], size=14, color=GRAY)
add_code_block(s5, Inches(0.4), Inches(4.0), Inches(9.2), Inches(1.15), [
    "$ sudo mkdir -p /etc/bind/keys/example.com",
    "$ sudo chown bind:bind /etc/bind/keys/example.com",
], size=12)

# ---------------------------------------------------------------------------
# Slide 6 -- TITLE_ONLY: configurando dnssec-policy
# ---------------------------------------------------------------------------
s6 = prs.slides.add_slide(layouts["TITLE_ONLY"])
set_title(s6, "Configurando una dnssec-policy")
add_code_block(s6, Inches(0.4), Inches(1.1), Inches(9.2), Inches(4.1), [
    "dnssec-policy \"operadores\" {",
    "    keys {",
    "        ksk lifetime unlimited algorithm ecdsap256sha256;",
    "        zsk lifetime P90D algorithm ecdsap256sha256;",
    "    };",
    "    dnskey-ttl PT1H;",
    "    signatures-refresh P5D;",
    "    signatures-validity P2W;",
    "    max-zone-ttl P1D;",
    "    purge-keys P90D;",
    "};",
], size=13)

# ---------------------------------------------------------------------------
# Slide 7 -- TITLE_AND_BODY: notas sobre la política
# ---------------------------------------------------------------------------
s7 = prs.slides.add_slide(layouts["TITLE_AND_BODY"])
set_title(s7, "Notas sobre esta política")
body7 = get_placeholder(s7, idx=1)
set_body_bullets(body7, [
    "ecdsap256sha256 — el mismo algoritmo 13 que vimos en isc.org (módulo 2)",
    "ksk lifetime unlimited — el rollover de KSK se dispara a mano",
    "zsk lifetime P90D — rota cada 90 días sin intervención",
    "Sin nsec3param — la política usa NSEC (NSEC3 se ve en el módulo 7)",
], size=17, space_after=13)

# ---------------------------------------------------------------------------
# Slide 8 -- TITLE_ONLY: la zona en named.conf.local
# ---------------------------------------------------------------------------
s8 = prs.slides.add_slide(layouts["TITLE_ONLY"])
set_title(s8, "La zona: named.conf.local")
add_code_block(s8, Inches(0.4), Inches(1.15), Inches(9.2), Inches(3.0), [
    "zone \"example.com\" {",
    "    type primary;",
    "    file \"/etc/bind/db.example.com\";",
    "    key-directory \"/etc/bind/keys/example.com\";",
    "    dnssec-policy \"operadores\";",
    "    inline-signing yes;",
    "",
    "    allow-transfer { key transfer-key; };",
    "    also-notify { 192.0.2.2; };",
    "    notify yes;",
    "};",
], size=13)
add_multiline_textbox(s8, Inches(0.4), Inches(4.35), Inches(9.2), Inches(0.6), [
    "allow-transfer / also-notify / notify: exactamente lo del módulo 3, sin cambios.",
], size=13, color=GRAY, italic=True)

# ---------------------------------------------------------------------------
# Slide 9 -- TITLE_ONLY: firmado automático
# ---------------------------------------------------------------------------
s9 = prs.slides.add_slide(layouts["TITLE_ONLY"])
set_title(s9, "Firmado automático de zona")
add_code_block(s9, Inches(0.4), Inches(1.1), Inches(9.2), Inches(3.9), [
    "$ named-checkconf",
    "$ sudo rndc reload example.com",
    "zone example.com/IN: reloaded",
    "",
    "$ journalctl -u named --since \"1 min ago\"",
    "... DNSKEY (Kexample.com.+013+41230) is now published",
    "... DNSKEY (Kexample.com.+013+54915) is now published",
    "... zone example.com/IN: signing zone: done",
    "",
    "$ rndc signing -list example.com",
    "Signing with key 013+41230",
    "Signing with key 013+54915",
], size=12)

# ---------------------------------------------------------------------------
# Slide 10 -- TITLE_ONLY: verificación con dig
# ---------------------------------------------------------------------------
s10 = prs.slides.add_slide(layouts["TITLE_ONLY"])
set_title(s10, "Verificación de la firma")
add_code_block(s10, Inches(0.4), Inches(1.1), Inches(9.2), Inches(3.0), [
    "$ dig @127.0.0.1 example.com DNSKEY +dnssec +multiline",
    "example.com. IN DNSKEY 256 3 13 ( ... ) ; ZSK; key id = 41230",
    "example.com. IN DNSKEY 257 3 13 ( ... ) ; KSK; key id = 54915",
    "",
    "$ dig @127.0.0.1 example.com A +dnssec +short",
    "93.184.216.34",
    "A 13 2 3600 20260819 20260805 41230 example.com. ...",
], size=13)
add_multiline_textbox(s10, Inches(0.4), Inches(4.35), Inches(9.2), Inches(0.6), [
    "Mismo patrón que isc.org: la KSK (54915) firma el DNSKEY RRset, la ZSK (41230) firma el resto.",
], size=13, color=GRAY, italic=True)

# ---------------------------------------------------------------------------
# Slide 11 -- MAIN_POINT: delv insecure es esperado
# ---------------------------------------------------------------------------
s11 = prs.slides.add_slide(layouts["MAIN_POINT"])
set_title(s11, "delv dice \"insecure\" — y está bien.\nEl DS todavía no está publicado en el padre.")

# ---------------------------------------------------------------------------
# Slide 12 -- TITLE_ONLY: dnssec-verify
# ---------------------------------------------------------------------------
s12 = prs.slides.add_slide(layouts["TITLE_ONLY"])
set_title(s12, "dnssec-verify: chequear sin depender del padre")
add_code_block(s12, Inches(0.4), Inches(1.15), Inches(9.2), Inches(2.6), [
    "$ dnssec-verify -o example.com /var/cache/bind/example.com.signed",
    "Verifying the zone using the following algorithms: ECDSAP256SHA256.",
    "Zone fully signed:",
    "Algorithm: ECDSAP256SHA256: KSKs: 1 active, 0 stand-by, 0 revoked",
    "                            ZSKs: 1 active, 0 stand-by, 0 revoked",
], size=13)

# ---------------------------------------------------------------------------
# Slide 13 -- TITLE_ONLY: publicar el DS (dsfromkey + flujo)
# ---------------------------------------------------------------------------
s13 = prs.slides.add_slide(layouts["TITLE_ONLY"])
set_title(s13, "Publicación del DS en el padre")
add_code_block(s13, Inches(0.4), Inches(1.1), Inches(9.2), Inches(1.1), [
    "$ dnssec-dsfromkey /etc/bind/keys/example.com/Kexample.com.+013+54915.key",
    "example.com. IN DS 54915 13 2 A94C3B1F... (SHA-256)",
], size=12)
add_multiline_textbox(s13, Inches(0.4), Inches(2.5), Inches(9.2), Inches(2.3), [
    "1.  Confirmar que la zona ya firma correctamente — nunca publicar el DS antes",
    "2.  Cargar el DS en el panel del registrador/TLD",
    "3.  Esperar propagación (TTL del DS + caché de resolvers)",
    "4.  Volver a correr delv — debería pasar de insecure a validado",
], size=15)

# ---------------------------------------------------------------------------
# Slide 14 -- TITLE_ONLY: cadena de confianza cerrada
# ---------------------------------------------------------------------------
s14 = prs.slides.add_slide(layouts["TITLE_ONLY"])
set_title(s14, "La cadena de confianza queda completa")
add_code_block(s14, Inches(0.4), Inches(1.3), Inches(9.2), Inches(1.1), [
    "$ delv @127.0.0.1 example.com A",
    "; fully validated",
    "93.184.216.34",
], size=15)
add_multiline_textbox(s14, Inches(0.4), Inches(2.8), Inches(9.2), Inches(0.7), [
    "Raíz → TLD → example.com, tal como se planteó en el módulo 1.",
], size=15, color=GRAY, italic=True)

# ---------------------------------------------------------------------------
# Slide 15 -- TITLE_AND_TWO_COLUMNS: rollovers panorama general
# ---------------------------------------------------------------------------
s15 = prs.slides.add_slide(layouts["TITLE_AND_TWO_COLUMNS"])
set_title(s15, "Rollovers: panorama general")
col1 = get_placeholder(s15, idx=1)
col2 = get_placeholder(s15, idx=2)
set_body_bullets(col1, [
    "ZSK",
    ("Rota sola cada 90 días, sin paso manual", 1),
    ("Superposición suficiente para que no haya ventana inválida", 1),
], size=16, space_after=10, bullet_first=False)
col1.text_frame.paragraphs[0].runs[0].font.bold = True
col1.text_frame.paragraphs[0].runs[0].font.color.rgb = RED
set_body_bullets(col2, [
    "KSK",
    ("Su rollover implica actualizar el DS en el padre", 1),
    ("Siempre requiere intervención humana", 1),
], size=16, space_after=10, bullet_first=False)
col2.text_frame.paragraphs[0].runs[0].font.bold = True
col2.text_frame.paragraphs[0].runs[0].font.color.rgb = RED

# ---------------------------------------------------------------------------
# Slide 16 -- TITLE_ONLY + table: Resumen
# ---------------------------------------------------------------------------
s16 = prs.slides.add_slide(layouts["TITLE_ONLY"])
set_title(s16, "Resumen")
add_table(s16, Inches(0.4), Inches(1.15), Inches(9.2), Inches(3.4), [
    ("Concepto", "Qué logra"),
    ("dnssec-policy", "Perfil reutilizable: algoritmo, tiempos de vida, parámetros de firma"),
    ("inline-signing yes", "El archivo de zona pasa a ser fuente sin firmar; named guarda la copia firmada aparte"),
    ("dnssec-dsfromkey", "Genera el registro DS a partir de la KSK, para publicar en el padre"),
    ("DS en el padre", "Cierra la cadena de confianza — sin esto, la zona firma pero nadie la valida"),
    ("Rollover ZSK vs KSK", "El de ZSK es automático; el de KSK requiere actualizar el DS a mano"),
], col_widths=[Inches(2.6), Inches(6.6)], size=13, header_size=14, first_col_bold=True,
    mono_cols={0})

# ---------------------------------------------------------------------------
# Slide 17 -- TITLE_AND_BODY: cierre + siguiente módulo
# ---------------------------------------------------------------------------
s17 = prs.slides.add_slide(layouts["TITLE_AND_BODY"])
set_title(s17, "Antes de monitorear")
body17 = get_placeholder(s17, idx=1)
set_body_bullets(body17, [
    "El mismo primario del módulo 3 ahora firma la zona; el secundario sigue funcionando sin cambios",
    "Firmar la zona no alcanza por sí solo — sin el DS en el padre, un validador la sigue viendo insecure",
    "Siguiente: Módulo 5 — qué vigilar en una zona firmada y cómo diagnosticar cuando algo falla",
], size=18, space_after=16)

# ---------------------------------------------------------------------------
# Move the closing "¡Gracias!" slide to the end
# ---------------------------------------------------------------------------
move_slide_to_end(prs, 2)

prs.save("04-Firmando-con-BIND-y-KASP-wip.pptx")
print("Module 4 done. Slide count:", len(prs.slides))
