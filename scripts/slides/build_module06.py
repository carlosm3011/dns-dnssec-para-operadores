#!/usr/bin/env python3
"""Build 06-Arquitectura-Hidden-Signer.pptx from the lacnic46.pptx template."""
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
s1.shapes.title.text_frame.paragraphs[0].runs[0].text = "Módulo 6: Arquitectura con hidden signer"
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
    "Motivación: separar la firma de la publicación",
    "Ventajas y componentes de la arquitectura",
    "Migrar example.com a hidden signer",
    "Verificar la migración",
    "Buenas prácticas: acceso, monitoreo, backups",
], size=18, space_after=14)

# ---------------------------------------------------------------------------
# Slide 3 -- TITLE_AND_BODY: motivación
# ---------------------------------------------------------------------------
s3 = prs.slides.add_slide(layouts["TITLE_AND_BODY"])
set_title(s3, "Motivación: separar la firma de la publicación")
body3 = get_placeholder(s3, idx=1)
set_body_bullets(body3, [
    "Hoy el primario hace dos trabajos: sostiene las claves privadas Y responde a cualquiera en internet",
    "Una vulnerabilidad en el servicio DNS público pone en juego el mismo proceso que tiene las claves cargadas",
    "Un hidden signer rompe esa combinación: el que firma no publica nada directamente",
], size=17, space_after=13)

# ---------------------------------------------------------------------------
# Slide 4 -- MAIN_POINT
# ---------------------------------------------------------------------------
s4 = prs.slides.add_slide(layouts["MAIN_POINT"])
set_title(s4, "Solo servidores públicos de confianza\nconsultan al signer — nunca internet.")

# ---------------------------------------------------------------------------
# Slide 5 -- TITLE_AND_BODY: ventajas
# ---------------------------------------------------------------------------
s5 = prs.slides.add_slide(layouts["TITLE_AND_BODY"])
set_title(s5, "Ventajas")
body5 = get_placeholder(s5, idx=1)
set_body_bullets(body5, [
    "Superficie de ataque reducida — el único protocolo expuesto es AXFR/IXFR, a IPs autorizadas",
    "Aislamiento de claves privadas — comprometer un público no expone ninguna KSK/ZSK",
    "Disponibilidad — los públicos se multiplican sin multiplicar el riesgo de exposición de claves",
], size=17, space_after=13)

# ---------------------------------------------------------------------------
# Slide 6 -- TITLE_ONLY: componentes y flujo (diagram)
# ---------------------------------------------------------------------------
s6 = prs.slides.add_slide(layouts["TITLE_ONLY"])
set_title(s6, "Componentes y flujo")
add_box(s6, Inches(0.4), Inches(1.2), Inches(2.7), Inches(1.1),
        "Zona sin firmar\n(editada a mano)", fill=DARK, size=12)
add_arrow(s6, Inches(3.1), Inches(1.75), Inches(3.5), Inches(1.75))
add_box(s6, Inches(3.5), Inches(1.2), Inches(2.9), Inches(1.1),
        "signer.example.com\n192.0.2.1 — hidden\nKSK + ZSK privadas", fill=RED, size=11)
add_arrow(s6, Inches(4.95), Inches(2.3), Inches(2.3), Inches(2.95))
add_arrow(s6, Inches(4.95), Inches(2.3), Inches(7.6), Inches(2.95))
add_box(s6, Inches(0.9), Inches(2.95), Inches(2.9), Inches(0.9),
        "ns2.example.com\n192.0.2.2 — público", fill=DARK, size=11)
add_box(s6, Inches(6.15), Inches(2.95), Inches(2.9), Inches(0.9),
        "ns3.example.com\n192.0.2.3 — público", fill=DARK, size=11)
add_arrow(s6, Inches(2.35), Inches(3.85), Inches(2.35), Inches(4.15))
add_arrow(s6, Inches(7.6), Inches(3.85), Inches(7.6), Inches(4.15))
add_box(s6, Inches(2.7), Inches(4.15), Inches(4.6), Inches(0.85),
        "Resolvers / internet", fill=GRAY, size=13)
add_multiline_textbox(s6, Inches(0.4), Inches(5.1), Inches(9.2), Inches(0.5), [
    "El signer no tiene ninguna flecha hacia internet — esa es la propiedad que construimos.",
], size=13, color=RED, italic=True)

# ---------------------------------------------------------------------------
# Slide 7 -- TITLE_ONLY: archivo de zona
# ---------------------------------------------------------------------------
s7 = prs.slides.add_slide(layouts["TITLE_ONLY"])
set_title(s7, "Archivo de zona: sale ns1, entra ns3")
add_code_block(s7, Inches(0.4), Inches(1.1), Inches(9.2), Inches(3.9), [
    "$TTL 3600",
    "example.com. IN SOA signer.example.com. admin.example.com. (",
    "                    2026080601 ; serial",
    "                    3600 3600 600 1209600 )",
    "example.com.     IN  NS    ns2.example.com.",
    "example.com.     IN  NS    ns3.example.com.",
    "ns2.example.com. IN  A     192.0.2.2",
    "ns3.example.com. IN  A     192.0.2.3",
    "example.com.     IN  A     93.184.216.34",
    "www.example.com. IN  CNAME example.com.",
], size=13)

# ---------------------------------------------------------------------------
# Slide 8 -- TITLE_AND_BODY: dos cambios intencionales
# ---------------------------------------------------------------------------
s8 = prs.slides.add_slide(layouts["TITLE_AND_BODY"])
set_title(s8, "Dos cambios intencionales")
body8 = get_placeholder(s8, idx=1)
set_body_bullets(body8, [
    "El MNAME del SOA (signer.example.com) no aparece en el NS RRset — no es un error, el MNAME no tiene por qué ser público",
    "ns1.example.com desaparece por completo — un NS \"fantasma\" es peor que no tenerlo",
], size=18, space_after=15)

# ---------------------------------------------------------------------------
# Slide 9 -- TITLE_ONLY: el signer, named.conf.local
# ---------------------------------------------------------------------------
s9 = prs.slides.add_slide(layouts["TITLE_ONLY"])
set_title(s9, "El signer: firma, pero no atiende consultas")
add_code_block(s9, Inches(0.4), Inches(1.1), Inches(9.2), Inches(2.5), [
    "zone \"example.com\" {",
    "    type primary;",
    "    dnssec-policy \"operadores\";",
    "    inline-signing yes;",
    "    allow-transfer { key transfer-key; };",
    "    also-notify { 192.0.2.2; 192.0.2.3; };",
    "    notify yes;",
    "};",
], size=13)
add_code_block(s9, Inches(0.4), Inches(3.85), Inches(9.2), Inches(1.15), [
    "# named.conf.options",
    "options { recursion no; allow-recursion { none; }; allow-query { none; }; };",
], size=12)

# ---------------------------------------------------------------------------
# Slide 10 -- MAIN_POINT: allow-query none
# ---------------------------------------------------------------------------
s10 = prs.slides.add_slide(layouts["MAIN_POINT"])
set_title(s10, "allow-query { none; } es lo que realmente\nhace \"hidden\" al signer.")

# ---------------------------------------------------------------------------
# Slide 11 -- TITLE_ONLY: servidores públicos
# ---------------------------------------------------------------------------
s11 = prs.slides.add_slide(layouts["TITLE_ONLY"])
set_title(s11, "Los públicos: ns2 sin cambios, ns3 nuevo")
add_code_block(s11, Inches(0.4), Inches(1.15), Inches(9.2), Inches(1.7), [
    "# ns3 — misma receta del módulo 3",
    "zone \"example.com\" {",
    "    type secondary;",
    "    primaries { 192.0.2.1 key transfer-key; };",
    "    file \"/var/cache/bind/example.com.secondary\";",
    "};",
], size=13)
add_code_block(s11, Inches(0.4), Inches(3.1), Inches(9.2), Inches(0.9), [
    "# endurecimiento nuevo: quién puede gatillar una retransferencia",
    "options { allow-notify { 192.0.2.1; }; };",
], size=13)

# ---------------------------------------------------------------------------
# Slide 12 -- TITLE_AND_BODY: NS y glue en el padre
# ---------------------------------------------------------------------------
s12 = prs.slides.add_slide(layouts["TITLE_AND_BODY"])
set_title(s12, "Actualizar NS y glue en el padre: el orden importa")
body12 = get_placeholder(s12, idx=1)
set_body_bullets(body12, [
    "1. Agregar ns3 (glue + NS) al padre antes de sacar ns1",
    "2. Confirmar que ns2 y ns3 sirven la zona firmada correctamente",
    "3. Recién ahí, quitar ns1 del padre",
    "4. Esperar el TTL del NS/glue viejo antes de dar la migración por terminada",
], size=17, space_after=12)

# ---------------------------------------------------------------------------
# Slide 13 -- TITLE_ONLY: verificar
# ---------------------------------------------------------------------------
s13 = prs.slides.add_slide(layouts["TITLE_ONLY"])
set_title(s13, "Verificar")
add_code_block(s13, Inches(0.4), Inches(1.15), Inches(9.2), Inches(2.6), [
    "$ dig @192.0.2.2 example.com A +dnssec +short    # ns2, firmado",
    "$ dig @192.0.2.3 example.com A +dnssec +short    # ns3, firmado",
    "",
    "$ dig @192.0.2.1 example.com A +short             # el signer",
    ";; connection timed out; no servers could be reached",
], size=13)
add_multiline_textbox(s13, Inches(0.4), Inches(4.05), Inches(9.2), Inches(0.7), [
    "Ese timeout es el resultado esperado — si el signer contesta, allow-query no está funcionando.",
], size=14, color=RED, italic=True)

# ---------------------------------------------------------------------------
# Slide 14 -- TITLE_AND_BODY: buenas prácticas, acceso y monitoreo
# ---------------------------------------------------------------------------
s14 = prs.slides.add_slide(layouts["TITLE_AND_BODY"])
set_title(s14, "Buenas prácticas: acceso y monitoreo")
body14 = get_placeholder(s14, idx=1)
set_body_bullets(body14, [
    "Firewall: negar todo el tráfico entrante al signer salvo desde ns2/ns3 — allow-query no es la única capa",
    "Acceso administrativo (SSH, rndc remoto): red de gestión separada de la de clientes DNS",
    "Monitoreo: todo lo del módulo 5 aplica igual, contra ns2/ns3 — no contra el signer",
], size=17, space_after=13)

# ---------------------------------------------------------------------------
# Slide 15 -- TITLE_AND_BODY: backups de claves
# ---------------------------------------------------------------------------
s15 = prs.slides.add_slide(layouts["TITLE_AND_BODY"])
set_title(s15, "Buenas prácticas: backups de claves")
body15 = get_placeholder(s15, idx=1)
set_body_bullets(body15, [
    "Respaldar también los archivos .state de KASP, no solo las claves — ahí vive el historial del rollover",
    "Cifrado en reposo + al menos una copia fuera del signer",
    "Perder la ZSK es recuperable; perder la KSK sin backup implica repetir la publicación del DS",
    "Probar la restauración, no solo hacerla",
], size=16, space_after=11)

# ---------------------------------------------------------------------------
# Slide 16 -- TITLE_ONLY + table: Resumen
# ---------------------------------------------------------------------------
s16 = prs.slides.add_slide(layouts["TITLE_ONLY"])
set_title(s16, "Resumen")
add_table(s16, Inches(0.3), Inches(1.05), Inches(9.4), Inches(3.9), [
    ("Concepto", "Qué logra"),
    ("allow-query { none; } en el signer", "Su única función de red es firmar y transferir"),
    ("also-notify a ambos públicos", "El signer avisa a los dos servidores públicos"),
    ("allow-notify en los públicos", "Evita un NOTIFY falsificado disparando una retransferencia"),
    ("MNAME del SOA ≠ un NS público", "Normal en hidden-signer — no implica reachability pública"),
    ("Backup del key-directory completo", "Incluye el estado de KASP, no solo las claves"),
], col_widths=[Inches(3.4), Inches(6.0)], size=12, header_size=13, first_col_bold=True)

# ---------------------------------------------------------------------------
# Slide 17 -- TITLE_AND_BODY: cierre + siguiente módulo
# ---------------------------------------------------------------------------
s17 = prs.slides.add_slide(layouts["TITLE_AND_BODY"])
set_title(s17, "Antes de lo avanzado")
body17 = get_placeholder(s17, idx=1)
set_body_bullets(body17, [
    "El signer nunca aparece en el NS RRset ni en el glue del padre — solo ns2 y ns3 lo hacen",
    "La migración es la misma disciplina de coherencia de NS/glue del módulo 3, aplicada a un cambio real",
    "Siguiente: Módulo 7 — NSEC3 y la mecánica completa de rollovers gestionados por KASP",
], size=18, space_after=16)

# ---------------------------------------------------------------------------
# Move the closing "¡Gracias!" slide to the end
# ---------------------------------------------------------------------------
move_slide_to_end(prs, 2)

prs.save("06-Arquitectura-Hidden-Signer-wip.pptx")
print("Module 6 done. Slide count:", len(prs.slides))
