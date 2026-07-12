# Guía de publicación — Pasos genéricos

Pasos reutilizables para publicar cualquier ensayo del ecosistema. Cada ensayo tiene su propio `docs/publicacion_metadata.md` con los datos específicos (título, descripción, categorías, estado por plataforma, enlaces).

## Requisitos previos

### Formatos a tener listos

| Formato | Para qué | Cómo generar |
|---|---|---|
| ePub | Ebooks en todas las plataformas | `ensayo/build_epub.sh` |
| PDF (lectura) | Payhip, venta directa | `ensayo/build_pdf.sh` |
| PDF (KDP 6×9") | Amazon tapa blanda | `ensayo/build_pdf.sh --amazon` |
| Portada ebook | Todas las plataformas | Mínimo 2560×1600px (KDP recomienda) |
| Portada wraparound | Tapa blanda (KDP, D2D print) | Lomo + contraportada. KDP tiene calculadora de lomo. |
| Portada cuadrada | Audiobook (InAudio) | Mínimo 3000×3000px |
| MP3s audiobook | Google Play, Spotify, InAudio | Script `generate_audiobook.py` |

### Cuentas necesarias (crear una vez, reusar para todos los ensayos)

- [Google Play Partner Center](https://play.google.com/books/publish/) — ebook + audiobook
- [Amazon KDP](https://kdp.amazon.com/) — ebook + tapa blanda
- [Draft2Digital](https://www.draft2digital.com/) — Apple Books, Kobo, B&N, bibliotecas, print, InAudio
- [Payhip](https://payhip.com/) — venta directa
- [Spotify for Podcasters](https://podcasters.spotify.com/) — audiobook como podcast

---

## Pasos por plataforma

### 1. Payhip (venta directa) — el más rápido

1. Ir a https://payhip.com/ → Dashboard
2. "Add a new product" → Digital download
3. Subir ePub + PDF como archivos descargables
4. Rellenar: título, descripción corta, portada
5. Fijar precio (recomendado: 9.99 € o PWYW desde 4.99 €)
6. Publicar → obtener enlace de producto
7. **Fee**: 5% por venta (plan gratuito)
8. **Royalty efectivo**: ~95%

### 2. Amazon KDP (ebook)

1. Ir a https://kdp.amazon.com/ → "Create a new Kindle eBook"
2. **Detalles del libro**:
   - Título, subtítulo, autor
   - Descripción (admite HTML básico)
   - Keywords (hasta 7)
   - Categorías BISAC (hasta 3)
3. **Contenido**:
   - Subir ePub
   - Subir portada (mínimo 1000×625px, recomendado 2560×1600)
   - Usar Kindle Previewer para verificar
4. **Precio y distribución**:
   - Fijar entre 2.99–9.99 € para 70% royalty
   - Territorios: todos
   - **NO activar KDP Select** (requiere exclusividad 90 días, incompatible con D2D/Apple/etc.)
5. Publicar → tarda 24-72h

### 3. Amazon KDP (tapa blanda)

1. Desde el ebook en KDP → "Add Paperback" (o crear independiente)
2. **Interior**:
   - Tamaño de recorte: 6×9"
   - Tipo de tinta: B/N
   - Tipo de papel: blanco
   - Subir PDF interior (generado con `build_pdf.sh --amazon`)
   - Verificar que márgenes cumplen mínimos KDP:
     - Gutter (margen interior): ≥ 0.5"
     - Margen exterior/superior/inferior: ≥ 0.25"
3. **Portada**:
   - Subir portada wraparound (portada + lomo + contraportada)
   - KDP ofrece Cover Creator si no tienes wraparound
   - Acabado: **mate**
4. **Precio**: fijar ~12.99 €, verificar que cubre coste impresión (~5 €)
5. **Distribución ampliada**: activar
6. Pedir **prueba de impresión** antes de publicar definitivamente

### 4. Google Play Books (ebook)

1. Ir a https://play.google.com/books/publish/ → Partner Center
2. "Add new book"
3. Subir ePub + portada
4. Rellenar metadata: título, autor, descripción, categorías, idioma
5. Fijar precio (recomendado: 6.99 €)
6. Publicar → tarda 24-72h
7. **Royalty**: ~52%

### 5. Google Play Books (audiobook)

1. En Partner Center → "Add new audiobook"
2. Subir MP3s en orden (00, 01, 02...)
3. **Marcar como narración IA** (obligatorio si se usa TTS)
4. Rellenar metadata (misma que el ebook)
5. Fijar precio
6. Publicar

### 6. Draft2Digital (distribución amplia — ebook)

1. Ir a https://www.draft2digital.com/ → Dashboard
2. "Add New Book"
3. Subir ePub + portada
4. Seleccionar canales de distribución:
   - ☑ Apple Books
   - ☑ Kobo
   - ☑ Barnes & Noble
   - ☑ OverDrive (bibliotecas)
   - ☐ Amazon (ya cubierto directo por KDP — evitar duplicado)
5. Rellenar metadata
6. Fijar precio (recomendado: 7.99 €)
7. Publicar → D2D se lleva **10%** de cada venta
8. Tarda **1-2 semanas** en aparecer en todas las tiendas

### 7. Draft2Digital (print / tapa blanda)

1. En D2D → "Add Print Book"
2. Tamaño: 6×9"
3. Subir PDF interior + portada wraparound
4. Fijar precio (recomendado: mismo que ebook)
5. D2D calcula coste de impresión automáticamente

### 8. Spotify for Podcasters (audiobook como podcast)

1. Ir a https://podcasters.spotify.com/
2. "Create a new podcast"
3. Nombre del podcast = título del ensayo
4. Subir cada capítulo como episodio (**en orden inverso** para que el cap 0/prólogo sea el primero en la lista)
5. Formato de títulos: "Prólogo: [Título]", "Cap 1: [Título]", etc.
6. Descripción del podcast = descripción corta del ensayo
7. Categoría: Society & Culture / Philosophy (o Science según el ensayo)
8. En la descripción de cada episodio, **enlazar a la venta del ebook**
9. **Precio**: gratis (función promocional)
10. Monetización disponible vía Spotify Partner Program a partir de cierto umbral

### 9. InAudio vía D2D (Audible, Apple, Kobo, Everand, bibliotecas)

1. En D2D → sección audiobooks (distribución InAudio)
2. Subir MP3s + metadata + portada cuadrada (3000×3000px mínimo)
3. Fijar retail price ($14.99 USD) y library price ($29.99 USD)
4. InAudio distribuye a:
   - ☑ Audible
   - ☑ Apple Books (audio)
   - ☑ Kobo
   - ☑ Everand
   - ☑ Bibliotecas
   - ☐ Google Play (ya cubierto directo)
   - ☐ Spotify (ya cubierto directo)

### 10. Promoción (tras publicar)

1. Post en web personal
2. Post en LinkedIn: enlazar a plataformas
3. En ambos posts, mencionar que el audiobook está gratis en Spotify
4. Enlace cruzado entre ensayos del ecosistema
5. El repo GitHub público sirve como prueba de transparencia del proceso

---

## Precios recomendados (referencia)

| Plataforma | Precio | Royalty | Notas |
|---|---|---|---|
| Payhip | 9.99 € (o PWYW desde 4.99 €) | ~95% | Venta directa, máximo margen |
| Spotify | Gratis | — | Promocional |
| Amazon KDP (ebook) | 6.99 € | 70% | Requiere rango 2.99–9.99 para 70% |
| Amazon KDP (tapa blanda) | 12.99 € | ~60% (~2.70€) | Depende del coste de impresión |
| Google Play Books | 6.99 € | ~52% | — |
| D2D ebook (Apple, Kobo, B&N) | 7.99 € | ~60% | D2D se lleva 10% |
| D2D print | 7.99 € | ~60% | D2D calcula coste impresión |
| InAudio audiobook | $14.99 USD | Variable | Library price: $29.99 |

---

## Audiobook — Pipeline de generación

### Configuración estándar

- **Voz**: es-ES-Chirp3-HD-Aoede (femenina, Google Cloud TTS)
- **Voz (inglés)**: en-GB-Chirp3-HD-Aoede (femenina, acento británico)
- **Velocidad**: 1.0x
- **Post-procesamiento**: intro (Am7→C arpeggio crossfade) + EQ + loudnorm + outro (descendente)
- **Jingles**: `audiobook/intro_am7_resolve_c.mp3`, `audiobook/outro_am_descend.mp3`

### Capítulos largos

Capítulos que superan ~30 minutos de audio deben dividirse en partes (Parte 1, Parte 2...) para mejor experiencia en todas las plataformas.

### Archivos especiales para InAudio

| Archivo | Función |
|---|---|
| `opening_credits.mp3` | Créditos iniciales |
| `front_matter.mp3` | Nota al lector / materia preliminar |
| `ending_credits.mp3` | Créditos finales |
| `retail_sample.mp3` | Muestra sin jingles (para tiendas) |
| `back_matter.mp3` | Material final |

---

## Orden recomendado de publicación

1. **Payhip** — inmediato, venta directa, máximo royalty
2. **Amazon KDP ebook** — mayor audiencia
3. **Google Play Books ebook** — segundo mercado
4. **Draft2Digital ebook** — distribuye a Apple, Kobo, B&N, bibliotecas
5. **Amazon KDP tapa blanda** — requiere PDF con márgenes + wraparound
6. **D2D print** — requiere wraparound
7. **Spotify audiobook** — requiere MP3s generados
8. **Google Play audiobook** — requiere MP3s generados
9. **InAudio (D2D)** — requiere MP3s + portada cuadrada

---

## Notas

- Cada ensayo mantiene su `docs/publicacion_metadata.md` con datos específicos: título, descripciones, categorías BISAC, estado por plataforma, enlaces de publicación y capítulos del audiobook.
- Esta guía centralizada se referencia desde cada `publicacion_metadata.md` para no duplicar los pasos.
