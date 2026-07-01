# Storyboard — "El desacoplo pendiente: energía en América Latina"
Curso: Data Visualization · "El Dashboard que Convence"

---

## Fase 1 — Pregunta narrativa central

> **¿Qué países de Latinoamérica han avanzado más en electrificación renovable sin sacrificar
> crecimiento económico, y quiénes siguen atados a los combustibles fósiles?**

Esta pregunta combina dos de los ejemplos válidos de la guía (avance vs. crecimiento económico,
y dependencia fósil persistente) porque el dashboard necesita sostener **una tensión de tres actos**:
progreso desigual → ¿el crecimiento lo explica? → quiénes quedan rezagados. Un dashboard con una
sola pregunta muy estrecha no permitía justificar los tres gráficos con la misma fuerza narrativa.

**Validada por:** _(completar con nombre del docente y fecha de validación)_

---

## Justificación de la paleta — Paleta 1: Sostenibilidad

| Color | Hex | Rol | Justificación (obligatoria por rubro) |
|---|---|---|---|
| Verde | `#2a9d8f` (`PRIMARY`) | Dato principal | Es el color de las renovables en los tres gráficos: representa el "progreso" que la historia quiere resaltar, y su asociación cromática con lo ecológico refuerza el tema sin necesidad de leyenda extra. |
| Naranja/rojo | `#e76f51` (`ACCENT`) | Hallazgo clave / rezagados | Se reserva exclusivamente para marcar lo que se aparta de la norma positiva — los países por encima de la mediana de dependencia fósil en el Gráfico 3 — creando contraste inmediato de "alerta" frente al verde de progreso. |
| Gris azulado | `#8d99ae` (`CONTEXT`) | Datos de contexto | Usado para líneas de referencia (mediana regional) y elementos secundarios que dan marco sin competir visualmente con el hallazgo principal. |
| Amarillo mostaza | `#e9c46a` (`ANNOTATION_BG`) | Acento de anotaciones | Fondo de los cuadros de texto narrativo dentro de los gráficos; se eligió por su alto contraste con el verde y el gris, garantizando que la anotación se lea primero sin necesidad de agrandar el texto. |

Máximo de colores activos por vista: 4 (cumple la regla obligatoria) — **pendiente de ajuste en
Gráfico 1**, ver nota de cierre.

---

## Fase 3 — Storyboard: orden y conexión narrativa

### Gráfico 1 (primera posición) — Línea de tiempo: % renovables en generación eléctrica
- **Por qué va primero:** establece el terreno de juego temporal — muestra que la transición
  eléctrica *sí está pasando*, pero de forma desigual. Es el gancho: genera la pregunta "¿por qué
  unos sí y otros no?"
- **Mensaje:** el progreso hacia renovables no es un fenómeno regional uniforme; hay líderes claros.
- **Anotación:** destaca automáticamente al país con mayor incremento en el periodo filtrado
  (dato dinámico, no hardcodeado), respondiendo la mitad de la pregunta central.

### Gráfico 2 (segunda posición) — Dispersión: PBI per cápita vs. % renovables en electricidad
- **Por qué va segundo:** responde la tensión que dejó el Gráfico 1 — ¿el avance depende de ser
  un país rico? El eje X en escala logarítmica y el tamaño de burbuja (población) permiten comparar
  economías de tamaños muy distintos sin distorsión.
- **Mensaje:** crecer económicamente no obliga a renunciar a las renovables — hay países de PBI
  medio-bajo con alta participación renovable, y viceversa.
- **Color como dato:** la escala continua verde→amarillo→naranja sobre la dependencia fósil añade
  una tercera variable sin agregar un cuarto color "activo" fuera de la paleta.

### Gráfico 3 (tercera posición) — Ranking horizontal: dependencia fósil en electricidad
- **Por qué va al final:** cierra la historia nombrando explícitamente a los rezagados, tras haber
  demostrado en los gráficos 1 y 2 que el avance es posible y no depende solo del ingreso. Es el
  "llamado a la acción" para la ONG y sus donantes.
- **Mensaje:** existe una brecha binaria — un grupo por debajo y otro por encima de la mediana
  regional — y la línea de mediana (gris de contexto) hace visible esa brecha sin necesitar tabla.
- **Conexión con el resto:** los países ya vistos como líderes en el Gráfico 1 (ej. Uruguay,
  Costa Rica) deberían aparecer aquí con baja dependencia fósil, cerrando el círculo narrativo.

### Flujo narrativo completo
**Progreso desigual (G1) → ¿lo explica el ingreso? No necesariamente (G2) → estos son quienes
faltan por cerrar la brecha (G3).**

---

## Roles de Fase 2 (documentación complementaria)

- **Rol 4 — Justificación de los tres gráficos:** ver tabla de Fase 3 arriba; cada gráfico
  responde a una etapa distinta de la pregunta narrativa central.
- **Rol 5 — Contexto para anotaciones:** la anotación del Gráfico 1 se calcula dinámicamente
  (mayor incremento en el rango filtrado) en vez de estar fija a un país, cumpliendo con
  "sin hardcodeo de valores numéricos" también en el texto narrativo, no solo en los datos.

---

## Checklist de cumplimiento frente a la guía

| Requisito | Estado |
|---|---|
| Pregunta narrativa validada por escrito | ✅ (este documento) |
| Fase 2: roles 1-3 en código | ✅ |
| Storyboard con orden, mensaje, conexión y paleta justificada | ✅ (este documento) |
| Título narrativo (no descriptivo) | ✅ |
| Tres visualizaciones con jerarquía clara | ✅ |
| Paleta consistente en las 4 vistas | ⚠️ Gráfico 1 usa `Set2` en vez de la paleta — **corregir antes de entregar** |
| Máx. 4 colores activos por vista | ⚠️ depende de la corrección anterior (5 países por defecto en G1) |
| Al menos una anotación narrativa | ✅ (dos: G1 y G2) |
| Sin gráficos de torta | ✅ |
| CSV leído directamente, sin hardcodeo | ✅ |
| Filtro interactivo con propósito narrativo (Fase 8, bonus) | ✅ (slider de años + multiselect de países) |
| Repositorio público en GitHub (`dv-grupo[N]-energia-latam`) | ⏳ Pendiente |
| `app.py` + `requirements.txt` | ⏳ Pendiente |
| Despliegue en Streamlit Community Cloud | ⏳ Pendiente |
| URL pública compartida en el documento del docente | ⏳ Pendiente |
