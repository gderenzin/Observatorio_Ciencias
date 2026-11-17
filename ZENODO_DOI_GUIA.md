# Guía Rápida: Emisión de DOIs Oficiales para sus Despachos mediante Zenodo (CERN)

Zenodo es el repositorio de ciencia abierta financiado por la Comisión Europea y alojado en los servidores del **CERN** en Ginebra (Suiza). Permite otorgar un **DOI (Digital Object Identifier) permanente, inmutable y oficial** a cualquier repositorio de GitHub de forma 100% gratuita.

Tener DOIs en sus despachos técnicos le permite:
1. Citarlos formalmente en su currículum vitae académico y en el baremo del **CACES/CES**.
2. Aparecer en los índices de **Google Scholar** y bases de datos bibliométricas.
3. Presentar ante el **Dr. Misganu Debella-Gilo (NMBU)** preprints de investigación auditables antes de la defensa de su tesis o publicación de artículos en revistas Q1.

---

### Paso 1: Iniciar Sesión en Zenodo con su cuenta de GitHub
1. Ingrese a: [https://zenodo.org](https://zenodo.org)
2. Haga clic en **Log in** en la esquina superior derecha.
3. Seleccione el botón **Log in with GitHub**.

---

### Paso 2: Habilitar el Repositorio de Ciencias
1. Una vez autenticado, vaya a su perfil y haga clic en **GitHub** en el menú desplegable (o ingrese directamente a `https://zenodo.org/account/settings/github/`).
2. Busque el repositorio del observatorio (por ejemplo: `ciencias-espaciales-geo` u `observatorio-ciencias`).
3. Active el interruptor (toggle) junto al nombre del repositorio para ponerlo en **ON**.

---

### Paso 3: Crear un "Release" en GitHub para Obtener el DOI
Cada vez que suba un nuevo despacho técnico a la carpeta `data/despachos.yaml`:
1. En GitHub, vaya a la pestaña **Releases** en la columna derecha y haga clic en **Create a new release** (o "Draft a new release").
2. En la etiqueta (*tag*), escriba una versión, por ejemplo: `v1.0.0` o `v2026.11`.
3. En el título, coloque el nombre del despacho técnico (ejemplo: *Despacho 01: Diagnóstico de Estrés Hídrico en Montalvo*).
4. Haga clic en **Publish release**.

---

### Resultado Inmediato
En menos de 60 segundos:
- Zenodo archiva una copia inmutable del repositorio.
- Le genera automáticamente un **DOI oficial** con el prefijo `10.5281/zenodo.XXXXXXX`.
- Le proporciona un distintivo (badge SVG) en Markdown para colocar en el `README.md`.
