# Introducción

Este es un breve curso de DNS y DNSSEC orientado a operadores de redes pequeños y medianos, incluyendo ISPs, IXPs, operadores de TLDs pequeños y universidades entre otros.

El curso asume que el lector:

- Está familiarizado con la operación de servidores basados en Unix, en particular Linux Ubuntu. 
- Domina los conceptos de alta disponibilidad, sockets, servicios en Unix.
- Esta familiarizado con los conceptos más básicos de DNS. Si bien el texto que sigue intenta ser explicativo de todos los conceptos, no es un curso de DNS básico.
- Está familiarizado con los conceptos de cifrado, cifrado de clave pública y algoritmo de hash. Si bien se incluyen pequeñas explicaciones sobre estas ideas son mas bien a título de recordatorio y este texto no es un curso de criptografía.

El espíritu detrás de este texto es el promover la experimentación. No hay ninguna cantidad de lectura que pueda suplir el experimentar el funcionamiento del DNS de manera directa. El uso de máquinas virtuales y containers hace mucho más accesible el poder experimentar con todos los elementos de una instalación realista de DNS.


Carlos Martinez, carlos@lacnic.net.

Montevideo, 7 de agosto de 2026.

# Temario

## 1. Introducción a DNSSEC
- ¿Qué es DNS y por qué necesita seguridad adicional?
- Ataques que DNSSEC mitiga: cache poisoning, spoofing, ataques on-path
- Qué problemas NO resuelve DNSSEC (confidencialidad, DDoS, etc.)
- Cadena de confianza: de la raíz a la zona hoja
- Conceptos clave: firma, clave pública/privada, validación

## 2. Los registros de DNSSEC
- RRSIG: firma de un conjunto de registros (RRset)
- DNSKEY: clave pública de la zona (ZSK y KSK)
- DS: enlace de confianza hacia el padre (delegation signer)
- NSEC: prueba de no-existencia (denegación autenticada)
- Mención breve de NSEC3 (hashing de nombres, cuándo se usa) — sin profundizar
- RRSIG sobre cada tipo de registro, incluyendo sobre NSEC/NSEC3

## 3. Zonas autoritativas con BIND
- Instalando BIND 9 en Ubuntu 
- Repaso del layout de la configuracion de bind9 en Ubuntu
- Crear una zona autoritativa primaria
- Verificar el funcionamiento con dig/drill 
- Configurar una zona autoritativa secundaria
	- permitir axfr/ixfr de forma segura y controlada
- Consideraciones de seguridad
	- prevenir la recursion no deseada
	- prevenir las respuestas tomadas de cache no deseadas
	- prevenir las transferencias de zona no deseadas
- Comentarios sobre configurar los registros NS en la zona padre

## 4. Firmando una zona con BIND y KASP
- Repaso de conceptos: KSK vs ZSK, por qué existe el rollover (panorama general, sin mecánica interna — eso va en el módulo 7)
- Introducción a KASP (Key and Signing Policy) en BIND
- Migrar el primario del módulo 3 a firmado inline (zona pasa a ser dinámica/gestionada por named)
- Configuración de una dnssec-policy en named.conf (algoritmo ECDSAP256SHA256, NSEC — consistente con el módulo 2; NSEC3 queda para el módulo 7)
- Firmado automático de zona (inline-signing / auto-dnssec)
- Verificación de la firma: dig, delv, dnssec-verify
- Publicación del DS en el padre (registrador / TLD)
- Mención de que KASP gestiona los rollovers automáticamente — detalle completo en el módulo 7

## 5. Monitoreo y troubleshooting
- ¿Cuales son los problemas mas comunes que nos pueden surgir con una zona firmada?
- Que parametros monitorear de una zona firmada, cada cuanto tiempo 
- Herramientas comunes para monitorear una zona firmada
- Diagnostico de problemas
- Resolución de problemas más comunes

## 6. Arquitectura con hidden signer
- Motivación: separar la firma de la publicación
- Ventajas: superficie de ataque reducida, aislamiento de claves privadas, disponibilidad
- Componentes: hidden master/signer, servidores públicos secundarios
- Flujo: zona sin firmar → hidden signer → zona firmada → servidores públicos (AXFR/IXFR)
- Implementación con BIND: hidden signer configurado con KASP + notify/also-notify hacia los públicos, servidores públicos como secundarios ocultando el hidden signer
- Buenas prácticas: control de acceso, monitoreo de expiración de firmas, backups de claves

## 7. DNSSEC avanzado
- NSEC3: hashing de nombres, iteraciones (RFC 9276: iterations=0, sin salt), opt-out — cuándo y por qué preferirlo sobre NSEC
- Mecánica completa de rollovers gestionados por KASP: línea de tiempo de una clave (generada → publicada → activa → retirada → eliminada) y la máquina de estados por tipo de registro que la sostiene (hidden → rumoured → omnipresent → unretentive, para DNSKEY/DS/RRSIG); estrategia pre-publish (ZSK, doble DNSKEY) vs. double-KSK (KSK, doble firma sobre el DNSKEY RRset + doble DS durante la transición con el padre)
- Inspeccionar y operar rollovers en vivo: dnssec-settime, rndc dnssec -status / -rollover / -checkds
- Algorithm rollover: cuándo migrar de algoritmo y cómo dnssec-policy gestiona la firma dual durante la transición
- CDS/CDNSKEY: publicación automática para simplificar (donde el registrador lo soporte) la sincronización del DS con el padre
- Multi-signer (RFC 8901, Model 2): motivación, soporte en BIND vía dnssec-policy, coordinación de DNSKEY/DS entre proveedores independientes
