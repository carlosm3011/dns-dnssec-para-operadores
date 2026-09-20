#!/usr/bin/env python3
"""Build 03-Zonas-BIND.pptx from the lacnic46.pptx template."""
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
s1.shapes.title.text_frame.paragraphs[0].runs[0].text = "Módulo 3: Zonas autoritativas con BIND"
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
    "Instalar BIND 9 y entender el layout de configuración en Ubuntu",
    "Configurar y depurar rndc",
    "Crear una zona autoritativa primaria",
    "Verificar con dig/drill",
    "Configurar una zona secundaria (AXFR/IXFR)",
    "Consideraciones de seguridad",
    "NS en la zona padre",
], size=17, space_after=12)

# ---------------------------------------------------------------------------
# Slide 3 -- TITLE_ONLY: Instalación
# ---------------------------------------------------------------------------
s3 = prs.slides.add_slide(layouts["TITLE_ONLY"])
set_title(s3, "Instalando BIND 9 en Ubuntu")
add_code_block(s3, Inches(0.4), Inches(1.15), Inches(9.2), Inches(3.6), [
    "$ sudo apt update",
    "$ sudo apt install bind9 bind9utils bind9-dnsutils",
    "",
    "$ named -v",
    "BIND 9.18.28 (Extended Support Version) <id:...>",
    "",
    "$ systemctl status bind9",
    "● bind9.service - BIND Domain Name Server",
    "     Active: active (running)",
], size=13)

# ---------------------------------------------------------------------------
# Slide 4 -- TITLE_AND_BODY: los tres paquetes + AppArmor
# ---------------------------------------------------------------------------
s4 = prs.slides.add_slide(layouts["TITLE_AND_BODY"])
set_title(s4, "Los tres paquetes")
body4 = get_placeholder(s4, idx=1)
set_body_bullets(body4, [
    "bind9 — el propio servidor (named)",
    "bind9utils — rndc, named-checkzone, named-checkconf, dnssec-*",
    "bind9-dnsutils — dig, nslookup, delv",
    "BIND corre bajo AppArmor: restringe qué directorios puede tocar named (por defecto /etc/bind, /var/cache/bind, /var/lib/bind)",
], size=17, space_after=13)

# ---------------------------------------------------------------------------
# Slide 5 -- TITLE_ONLY + table: layout de configuración
# ---------------------------------------------------------------------------
s5 = prs.slides.add_slide(layouts["TITLE_ONLY"])
set_title(s5, "Layout de configuración en Ubuntu")
add_multiline_textbox(s5, Inches(0.4), Inches(1.1), Inches(9.2), Inches(0.5), [
    "Todo bajo /etc/bind/:",
], size=14, bold=True)
add_table(s5, Inches(0.4), Inches(1.6), Inches(9.2), Inches(2.6), [
    ("Archivo", "Contenido"),
    ("named.conf", "Solo tres include hacia los archivos de abajo — no se edita"),
    ("named.conf.options", "Opciones globales: recursión, listen-on, forwarders"),
    ("named.conf.local", "Donde se declaran las zonas propias (este módulo)"),
    ("named.conf.default-zones", "Zonas que Ubuntu preconfigura: localhost, root.hints"),
], col_widths=[Inches(2.8), Inches(6.4)], size=13, header_size=14, first_col_bold=True,
    mono_cols={0})

# ---------------------------------------------------------------------------
# Slide 6 -- TITLE_AND_BODY: datos vs configuración
# ---------------------------------------------------------------------------
s6 = prs.slides.add_slide(layouts["TITLE_AND_BODY"])
set_title(s6, "Los datos viven aparte de la configuración")
body6 = get_placeholder(s6, idx=1)
set_body_bullets(body6, [
    "/var/cache/bind/ — directorio de trabajo por defecto: archivos de zona, journals (.jnl), zonas transferidas",
    "/etc/bind/rndc.key — clave que usa rndc para autenticarse contra el servidor",
], size=18, space_after=14)

# ---------------------------------------------------------------------------
# Slide 7 -- MAIN_POINT: rndc suele fallar primero
# ---------------------------------------------------------------------------
s7 = prs.slides.add_slide(layouts["MAIN_POINT"])
set_title(s7, "rndc es, en la práctica,\nde lo primero que falla en una instalación nueva.")

# ---------------------------------------------------------------------------
# Slide 8 -- TITLE_AND_BODY: 3 causas comunes
# ---------------------------------------------------------------------------
s8 = prs.slides.add_slide(layouts["TITLE_AND_BODY"])
set_title(s8, "rndc reload falla: tres causas comunes")
body8 = get_placeholder(s8, idx=1)
set_body_bullets(body8, [
    "1. Falta de permisos para leer la clave",
    ("El caso más común. Solución: sudo rndc reload, o sumar el usuario al grupo bind", 1),
    "2. Reloj desincronizado",
    ("rndc firma con timestamp; un desfase grande invalida la firma. Revisar timedatectl", 1),
    "3. Clave de named.conf desactualizada",
    ("Alguien regeneró rndc.key o editó controls/key y quedó desincronizado", 1),
], size=15, space_after=8)
for i in (0, 2, 4):
    body8.text_frame.paragraphs[i].runs[0].font.bold = True
    body8.text_frame.paragraphs[i].runs[0].font.color.rgb = RED

# ---------------------------------------------------------------------------
# Slide 9 -- TITLE_ONLY: habilitar rndc remoto
# ---------------------------------------------------------------------------
s9 = prs.slides.add_slide(layouts["TITLE_ONLY"])
set_title(s9, "Habilitar rndc desde otra máquina")
add_code_block(s9, Inches(0.4), Inches(1.1), Inches(9.2), Inches(1.7), [
    "# En named.conf.options del servidor a controlar:",
    "controls {",
    "    inet 192.0.2.2 port 953",
    "        allow { 203.0.113.10; } keys { \"rndc-key\"; };",
    "};",
], size=13)
add_multiline_textbox(s9, Inches(0.4), Inches(3.0), Inches(9.2), Inches(1.2), [
    "En la máquina que corre rndc hace falta además un /etc/bind/rndc.conf",
    "(Ubuntu no lo genera por defecto) con la misma clave que rndc.key.",
], size=14, color=GRAY)

# ---------------------------------------------------------------------------
# Slide 10 -- TITLE_ONLY: named.conf.local, declarar la zona
# ---------------------------------------------------------------------------
s10 = prs.slides.add_slide(layouts["TITLE_ONLY"])
set_title(s10, "Crear una zona autoritativa primaria")
add_code_block(s10, Inches(0.4), Inches(1.2), Inches(9.2), Inches(1.5), [
    "# /etc/bind/named.conf.local",
    "zone \"example.com\" {",
    "    type primary;",
    "    file \"/etc/bind/db.example.com\";",
    "};",
], size=14)
add_multiline_textbox(s10, Inches(0.4), Inches(2.95), Inches(9.2), Inches(0.6), [
    "\"master\" en versiones/documentación viejas de BIND — mismo significado que \"primary\".",
], size=13, color=GRAY, italic=True)

# ---------------------------------------------------------------------------
# Slide 11 -- TITLE_ONLY: archivo de zona
# ---------------------------------------------------------------------------
s11 = prs.slides.add_slide(layouts["TITLE_ONLY"])
set_title(s11, "/etc/bind/db.example.com")
add_code_block(s11, Inches(0.4), Inches(1.1), Inches(9.2), Inches(4.0), [
    "$TTL 3600",
    "example.com.     IN  SOA  ns1.example.com. admin.example.com. (",
    "                          2026080401 ; serial",
    "                          3600 3600 600 1209600 )",
    "example.com.     IN  NS   ns1.example.com.",
    "example.com.     IN  NS   ns2.example.com.",
    "ns1.example.com. IN  A    192.0.2.1",
    "ns2.example.com. IN  A    192.0.2.2",
    "example.com.     IN  A    93.184.216.34",
    "www.example.com. IN  CNAME example.com.",
], size=13)

# ---------------------------------------------------------------------------
# Slide 12 -- TITLE_ONLY: validar, recargar, verificar
# ---------------------------------------------------------------------------
s12 = prs.slides.add_slide(layouts["TITLE_ONLY"])
set_title(s12, "Validar, recargar, verificar")
add_code_block(s12, Inches(0.4), Inches(1.1), Inches(9.2), Inches(3.9), [
    "$ named-checkzone example.com /etc/bind/db.example.com",
    "zone example.com/IN: loaded serial 2026080401",
    "OK",
    "",
    "$ sudo rndc reload",
    "zone reload successful",
    "",
    "$ dig @127.0.0.1 example.com A +short",
    "93.184.216.34",
], size=13)

# ---------------------------------------------------------------------------
# Slide 13 -- TITLE_AND_BODY: por qué un secundario
# ---------------------------------------------------------------------------
s13 = prs.slides.add_slide(layouts["TITLE_AND_BODY"])
set_title(s13, "Por qué usar un secundario")
body13 = get_placeholder(s13, idx=1)
set_body_bullets(body13, [
    "Un único servidor autoritativo es un punto único de falla",
    "RFC 2182: al menos dos servidores autoritativos, en redes y ubicaciones distintas",
    "Beneficio adicional: menor latencia y carga de consultas repartida",
], size=18, space_after=14)

# ---------------------------------------------------------------------------
# Slide 14 -- TITLE_AND_TWO_COLUMNS: polling vs NOTIFY
# ---------------------------------------------------------------------------
s14 = prs.slides.add_slide(layouts["TITLE_AND_TWO_COLUMNS"])
set_title(s14, "Cómo se mantienen sincronizados")
col1 = get_placeholder(s14, idx=1)
col2 = get_placeholder(s14, idx=2)
set_body_bullets(col1, [
    "Polling por SOA",
    ("Cada refresh segundos, el secundario pregunta el serial del primario", 1),
], size=16, space_after=12, bullet_first=False)
col1.text_frame.paragraphs[0].runs[0].font.bold = True
col1.text_frame.paragraphs[0].runs[0].font.color.rgb = RED
set_body_bullets(col2, [
    "NOTIFY",
    ("El primario avisa proactivamente al cambiar el serial — propagación en segundos", 1),
], size=16, space_after=12, bullet_first=False)
col2.text_frame.paragraphs[0].runs[0].font.bold = True
col2.text_frame.paragraphs[0].runs[0].font.color.rgb = RED

# ---------------------------------------------------------------------------
# Slide 15 -- TITLE_ONLY: flujo AXFR/IXFR (diagram)
# ---------------------------------------------------------------------------
s15 = prs.slides.add_slide(layouts["TITLE_ONLY"])
set_title(s15, "AXFR/IXFR: el flujo de sincronización")
steps = [
    "1. Cambia un registro,\nsube el serial",
    "2. NOTIFY al\nsecundario",
    "3. Secundario\nconsulta SOA",
    "4. IXFR (con journal)\no AXFR (sin él)",
    "5. Secundario\nactualiza su copia",
]
bw = Inches(1.68)
bh = Inches(1.4)
gap = Inches(0.15)
x0 = Inches(0.4)
by = Inches(1.9)
for i, s in enumerate(steps):
    x = x0 + i * (bw + gap)
    fill = RED if i < 4 else DARK
    add_box(s15, x, by, bw, bh, s, fill=fill, size=11)
    if i < 4:
        add_arrow(s15, x + bw, by + bh // 2, x + bw + gap, by + bh // 2)
add_multiline_textbox(s15, Inches(0.4), Inches(3.7), Inches(9.2), Inches(1.0), [
    "AXFR = transferencia completa de la zona, por TCP (empieza y termina con el SOA).",
    "IXFR = variante incremental, solo los cambios desde el último serial conocido.",
], size=14, color=GRAY)

# ---------------------------------------------------------------------------
# Slide 16 -- TITLE_ONLY: config del secundario
# ---------------------------------------------------------------------------
s16 = prs.slides.add_slide(layouts["TITLE_ONLY"])
set_title(s16, "Configurar la zona secundaria")
add_code_block(s16, Inches(0.4), Inches(1.15), Inches(9.2), Inches(1.7), [
    "# named.conf.local del SECUNDARIO",
    "zone \"example.com\" {",
    "    type secondary;",
    "    primaries { 192.0.2.1; };",
    "    file \"/var/cache/bind/example.com.secondary\";",
    "};",
], size=13)
add_multiline_textbox(s16, Inches(0.4), Inches(3.05), Inches(9.2), Inches(1.4), [
    "Los NS tienen que reflejar la topología real: NS ns1 y NS ns2 declarados tanto",
    "en el archivo de zona como en la zona padre. Si el padre delega solo a ns1,",
    "ns2 puede estar sincronizado y ser igualmente irrelevante — nadie lo consulta.",
], size=13, color=GRAY)

# ---------------------------------------------------------------------------
# Slide 17 -- TITLE_ONLY: habilitar transferencias de forma segura
# ---------------------------------------------------------------------------
s17 = prs.slides.add_slide(layouts["TITLE_ONLY"])
set_title(s17, "Permitir AXFR/IXFR de forma segura")
add_code_block(s17, Inches(0.4), Inches(1.1), Inches(9.2), Inches(2.3), [
    "# En el PRIMARIO",
    "zone \"example.com\" {",
    "    type primary;",
    "    file \"/etc/bind/db.example.com\";",
    "    allow-transfer { key transfer-key; };",
    "    also-notify { 192.0.2.2; };",
    "    notify yes;",
    "};",
], size=13)
add_multiline_textbox(s17, Inches(0.4), Inches(3.6), Inches(9.2), Inches(1.0), [
    "Restringir solo por IP se puede falsificar. TSIG (tsig-keygen transfer-key)",
    "autentica de verdad con una clave simétrica compartida entre ambos servidores.",
], size=13, color=GRAY)

# ---------------------------------------------------------------------------
# Slide 18 -- TITLE_ONLY + table: consideraciones de seguridad
# ---------------------------------------------------------------------------
s18 = prs.slides.add_slide(layouts["TITLE_ONLY"])
set_title(s18, "Consideraciones de seguridad")
add_table(s18, Inches(0.4), Inches(1.3), Inches(9.2), Inches(2.9), [
    ("Práctica", "Por qué"),
    ("recursion no", "Un autoritativo no debe resolver para terceros — evita open resolvers"),
    ("additional-from-cache/auth no", "Evita filtrar datos de terceros en respuestas autoritativas"),
    ("allow-transfer { none; } global\n+ excepción por zona", "Sin esto, cualquiera puede descargar la zona completa con dig axfr"),
], col_widths=[Inches(3.4), Inches(5.8)], size=13, header_size=14, first_col_bold=True,
    mono_cols={0})

# ---------------------------------------------------------------------------
# Slide 19 -- TITLE_AND_BODY: NS en la zona padre
# ---------------------------------------------------------------------------
s19 = prs.slides.add_slide(layouts["TITLE_AND_BODY"])
set_title(s19, "NS en la zona padre")
body19 = get_placeholder(s19, idx=1)
set_body_bullets(body19, [
    "Glue records: si el NS vive dentro de la zona que delega (ns1.example.com), el padre debe publicar también su A/AAAA — si no, hay referencia circular",
    "Coherencia de delegación: el set de NS del padre y el de la propia zona deben coincidir, o la delegación queda \"lame\"",
    "Los cambios de NS en el padre tardan en propagar — planificar con margen",
], size=17, space_after=14)

# ---------------------------------------------------------------------------
# Slide 20 -- TITLE_ONLY + table: Resumen
# ---------------------------------------------------------------------------
s20 = prs.slides.add_slide(layouts["TITLE_ONLY"])
set_title(s20, "Resumen")
add_table(s20, Inches(0.4), Inches(1.05), Inches(9.2), Inches(4.0), [
    ("Concepto", "Qué logra"),
    ("rndc.key + grupo bind", "Autentica el control local de named"),
    ("controls + rndc.conf", "Habilita y autentica el control remoto de named"),
    ("type primary / secondary", "Distingue quién tiene la copia autoritativa original"),
    ("allow-transfer + TSIG", "Restringe y autentica quién puede copiar la zona"),
    ("also-notify / notify yes", "El secundario se entera de cambios sin esperar el refresh"),
    ("recursion no", "Evita que el autoritativo actúe como resolver abierto"),
], col_widths=[Inches(3.0), Inches(6.2)], size=12, header_size=13, first_col_bold=True,
    mono_cols={0})

# ---------------------------------------------------------------------------
# Slide 21 -- TITLE_AND_BODY: cierre + siguiente módulo
# ---------------------------------------------------------------------------
s21 = prs.slides.add_slide(layouts["TITLE_AND_BODY"])
set_title(s21, "Antes de firmar")
body21 = get_placeholder(s21, idx=1)
set_body_bullets(body21, [
    "Un primario aloja el archivo de zona original; uno o más secundarios mantienen una copia sincronizada por AXFR/IXFR",
    "Todo lo configurado acá es texto plano, sin firmar — nada impide modificar una respuesta en tránsito",
    "Siguiente: Módulo 4 — firmar esta misma zona con KASP y publicar el DS en el padre",
], size=18, space_after=16)

# ---------------------------------------------------------------------------
# Move the closing "¡Gracias!" slide to the end
# ---------------------------------------------------------------------------
move_slide_to_end(prs, 2)

prs.save("03-Zonas-BIND-wip.pptx")
print("Module 3 done. Slide count:", len(prs.slides))
