# 📄 Artículo de Revisión Sistemática - IA en Agricultura

## 🎯 Descripción General

Este directorio contiene el **artículo académico completo** de la revisión sistemática de literatura sobre aplicaciones de inteligencia artificial, visión por computador y machine learning en agricultura, generado a partir del análisis bibliométrico del notebook Jupyter.

## 📁 Archivos Generados

### Documento Principal
- **`articulo_revision.tex`**: Código fuente LaTeX completo
- **`articulo_revision.pdf`**: Documento final compilado

### Herramientas
- **`compile_report.sh`**: Script para compilación automática

## 📊 Contenido del Artículo

### Estructura de la Revisión Sistemática:



## 🛠️ Compilación

### Opción 1: Script Automático
```bash
./compile_report.sh
```

### Opción 2: Manual
```bash
pdflatex informe_clustering.tex
pdflatex informe_clustering.tex  # Segunda pasada para referencias
```

### Requisitos:
- LaTeX completo (texlive-full recomendado)
- Paquetes: amsmath, booktabs, hyperref, listings, algorithms
