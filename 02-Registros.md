# 02 - Los registros de DNSSEC

> Nota sobre los ejemplos: `example.com` no está firmado en la vida real, así que para ver registros DNSSEC reales usamos **isc.org** (Internet Systems Consortium, mantenedores de BIND), uno de los dominios pioneros en firmar su zona. Las consultas se hicieron el 10/07/2026 — si las repetís, los valores van a diferir (las firmas y claves rotan).

DNSSEC agrega cuatro tipos de registro nuevos a una zona: **DNSKEY**, **RRSIG**, **DS** y **NSEC**. Cada uno cumple un rol distinto en la cadena de confianza vista en el [módulo 1](01-Introduccion.md).

## DNSKEY — la clave pública de la zona

Contiene la clave pública de la zona. Se publica en la propia zona para que cualquier validador pueda obtenerla.

```
$ dig +dnssec +multiline DNSKEY isc.org

isc.org.  405 IN DNSKEY 256 3 13 (
              1CS+VQcRn4lGTK+b3wDjVO0hFDx4DV7s3Q1Fwxuq9ahd
              255FRny4f4vdZOMMMxpbRH5Zhwoh/706IV0v9JwjlA==
              ) ; ZSK; alg = ECDSAP256SHA256 ; key id = 27566
isc.org.  405 IN DNSKEY 257 3 13 (
              zEoOfseNFDM+E8spu7RR2Ar/GzFqAehe4yapWLiv6McI
              UF6xmI5GcIQ3+uLAizS2cNWHt6EArVj8ogjtrRXwfw==
              ) ; KSK; alg = ECDSAP256SHA256 ; key id = 7250
```

`isc.org` publica **dos** DNSKEY: una ZSK (Zone Signing Key) y una KSK (Key Signing Key). El propio `dig` anota el rol y el `key id` de cada una entre paréntesis — de dónde sale esa distinción y por qué se usan dos claves en vez de una se explica en detalle en el [módulo 4](04-Firmando-con-BIND-y-KASP.md), cuando toque generarlas.

## RRSIG — la firma sobre un RRset

Es la firma digital (la del [módulo 1](01-Introduccion.md)) empaquetada como registro DNS. Cada RRset firmado tiene su propio RRSIG.

```
$ dig +dnssec +multiline A isc.org

isc.org.  300 IN A 151.101.2.217
isc.org.  300 IN A 151.101.66.217
isc.org.  300 IN A 151.101.130.217
isc.org.  300 IN A 151.101.194.217
isc.org.  300 IN RRSIG A 13 2 300 (
              20260719192313 20260705182333 27566 isc.org.
              kh8odndDXlsLHt7vumqWyXTdf/HbiiPfxqPli0Dg6+QZ
              D9nxorNCXuA2E0I807oC8tJ5FzL0wfgbtmUtkDAqyg== )
```

Lo importante del RRSIG, sin entrar en el formato binario completo:

- `13` — algoritmo de firma (se detalla en el módulo 4).
- `20260719192313` / `20260705182333` — vencimiento e inicio de validez de la firma. Fuera de ese rango, la firma es inválida aunque los datos no hayan cambiado.
- `27566` — key id de la DNSKEY que firmó este RRset (coincide con la ZSK que vimos arriba).
- `isc.org.` — nombre de la zona firmante.

Fijate que la KSK (7250) **no** firmó este registro A — lo firmó la ZSK (27566). Si consultás el DNSKEY RRset vas a ver lo contrario:

```
$ dig +dnssec +multiline DNSKEY isc.org | grep RRSIG -A2

isc.org.  405 IN RRSIG DNSKEY 13 2 3600 (
              20260720060847 20260706053216 7250 isc.org.
              ...
```

Ese `7250` es la KSK. Patrón general: **la KSK firma únicamente el DNSKEY RRset; la ZSK firma todo lo demás** (A, SOA, NSEC, etc.). El porqué de esta separación de roles se ve en el módulo 4.

## DS — el enlace hacia el padre

El DS ("Delegation Signer") no vive en la zona misma, sino en la zona **padre**. Es un hash de la KSK, y es lo que permite extender la cadena de confianza de un eslabón al siguiente.

```
$ dig +dnssec +multiline DS isc.org

isc.org.  3600 IN DS 7250 13 2 (
              A30B3F78B6DDE9A4A9A2AD0C805518B4F49EC62E7D3F
              4531D33DE697CDA01CB2 )
isc.org.  3600 IN RRSIG DS 8 2 3600 (
              20260730154208 20260709144208 13950 org.
              ...
```

Notá tres cosas:

- El `7250` inicial es el key id de la KSK de `isc.org` — el DS apunta a esa clave específica.
- El DS de `isc.org` está firmado por la clave `13950`, que pertenece a la zona **`org.`**, no a `isc.org`. Esto es literalmente el eslabón de la cadena: el padre certifica al hijo.
- Un validador calcula el hash de la KSK que recibió de `isc.org` y lo compara contra este DS. Si coinciden, la KSK es de confianza; si no, la validación falla.

## NSEC — negar que algo no existe, de forma autenticada

DNS necesita poder responder "esto no existe" (NXDOMAIN). Sin DNSSEC, esa respuesta negativa no está firmada — un atacante podría falsificarla para ocultar un nombre real. NSEC resuelve esto firmando la **ausencia**.

```
$ dig +dnssec +multiline A doesnotexist.isc.org

;; ->>HEADER<<- opcode: QUERY, status: NXDOMAIN

docs.isc.org.  3600 IN NSEC dommel.isc.org. A RRSIG NSEC
docs.isc.org.  3600 IN RRSIG NSEC 13 3 3600 ( ... )
isc.org.       3600 IN NSEC _acme-challenge.isc.org. A NS SOA MX TXT AAAA ...
isc.org.       3600 IN RRSIG NSEC 13 2 3600 ( ... )
```

Un NSEC dice "no existe ningún nombre entre este registro y el siguiente, en orden alfabético". Acá `docs.isc.org.` apunta a `dommel.isc.org.` — como `doesnotexist.isc.org` cae alfabéticamente entre ambos, y el NSEC (firmado) lo confirma, el resolver puede probar criptográficamente que el nombre no existe, no solo confiar en un NXDOMAIN sin firmar.

El NSEC también lista, al final, qué tipos de registro *sí* existen para ese nombre (`A NS SOA MX TXT ... RRSIG NSEC`) — útil para probar autenticadamente ausencia de un tipo puntual (ej. "este nombre existe pero no tiene AAAA").

**NSEC3** es una variante que usa nombres *hasheados* en vez de nombres en claro, para evitar que alguien recorra el NSEC de la zona y enumere todos los nombres existentes (zone walking). La lógica de fondo es la misma; lo vas a encontrar en zonas grandes o sensibles a enumeración. No entramos en su formato acá.

## Resumen

| Registro | Vive en | Firma/protege |
|---|---|---|
| DNSKEY | La propia zona | Publica las claves públicas (ZSK/KSK) |
| RRSIG | La propia zona | La firma de un RRset puntual |
| DS | La zona padre | El hash de la KSK del hijo — extiende la cadena de confianza |
| NSEC | La propia zona | Prueba autenticada de que un nombre/tipo no existe |

- Todo RRset firmado tiene su RRSIG correspondiente; el DNSKEY RRset lo firma la KSK, el resto lo firma la ZSK.
- El DS es el único registro DNSSEC que no vive en la zona que protege — vive un nivel arriba.
- NSEC (no NSEC3) fue lo que vimos en el ejemplo; ambos resuelven el mismo problema de denegación autenticada.
- Siguiente: [03-Zonas-BIND.md](03-Zonas-BIND.md) — levantar un servidor BIND y publicar una zona autoritativa (sin firmar todavía).
