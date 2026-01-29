#!/bin/bash

# Script para compilar el informe LaTeX actualizado
# Uso: ./compile_report.sh

echo "🔄 Compilando revisión sistemática de literatura..."

# Compilar el documento de revisión sistemática
pdflatex articulo_plantilla.tex
echo "📚 Procesando referencias bibliográficas..."
bibtex articulo_plantilla
pdflatex articulo_plantilla.tex
pdflatex articulo_plantilla.tex

# Limpiar archivos temporales
echo "🧹 Limpiando archivos temporales..."
rm -f *.aux *.log *.toc *.out *.bbl *.blg *.fdb_latexmk *.fls

echo "✅ Compilación completada: articulo_plantilla.pdf"

# Mostrar información del archivo generado
if [ -f articulo_plantilla.pdf ]; then
    echo "📄 Documento generado:"
    ls -lh articulo_plantilla.pdf
    echo "📊 Número de páginas: $(pdfinfo articulo_plantilla.pdf 2>/dev/null | grep Pages | awk '{print $2}')"
fi

# Abrir el PDF si el sistema lo permite
if command -v xdg-open &> /dev/null; then
    echo "📖 Abriendo PDF..."
    xdg-open articulo_plantilla.pdf &
elif command -v open &> /dev/null; then
    echo "📖 Abriendo PDF..."
    open articulo_plantilla.pdf &
fi