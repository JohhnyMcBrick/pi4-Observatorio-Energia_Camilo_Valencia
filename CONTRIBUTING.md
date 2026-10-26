# Reglas del equipo

## Ramas
`main` está protegida: nadie hace push directo. Cada tarea se hace en su rama y entra por Pull Request.

- `feature/extract-xm`, `feature/extract-ideam`, `feature/fuente-propia-trm`
- `fix/...` para correcciones · `docs/...` para documentación · `test/...` para pruebas

## Commits
En español, con prefijo: `feat:`, `fix:`, `docs:`, `test:`, `refactor:`. Ejemplo: `feat: extrae temperatura del IDEAM con SoQL`.
Haga commits pequeños y a lo largo de la semana, no todos el último día.

## Pull Requests
1. Abra el PR desde su rama hacia `main` con la plantilla (qué cambió y por qué, cómo se probó).
2. Un compañero lo revisa y aprueba (mínimo 1 aprobación). Nadie aprueba su propio PR.
3. Antes de pedir revisión: `python -m pytest` debe pasar.
4. Se hace *Squash and merge* y se borra la rama.

## Issues y tablero
Cada tarea es un issue asignado a una persona, en el tablero de GitHub Projects (*Por hacer · En progreso · En revisión · Hecho*). El PR cierra su issue con `Closes #N`.

## Datos y secretos
- No se sube `data/bronze/` (está en `.gitignore`); sí `data/sample/`.
- Ninguna clave en el código: use `.env` (ignorado) o GitHub Secrets.

## Bitácora
Cada integrante mantiene `docs/bitacoras/apellido_nombre.md` (use `docs/bitacoras/_plantilla.md`), actualizada cada semana.
