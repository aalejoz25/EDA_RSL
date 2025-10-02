#!/bin/bash

# Script para compilar el informe LaTeX actualizado
# Uso: ./compile_report.sh

echo "🔄 Compilando revisión sistemática de literatura..."

# Compilar el documento de revisión sistemática
pdflatex articulo_revision.tex
echo "📚 Procesando referencias bibliográficas..."
bibtex articulo_revision
pdflatex articulo_revision.tex
pdflatex articulo_revision.tex

# Limpiar archivos temporales
echo "🧹 Limpiando archivos temporales..."
rm -f *.aux *.log *.toc *.out *.bbl *.blg *.fdb_latexmk *.fls

echo "✅ Compilación completada: articulo_revision.pdf"

# Mostrar información del archivo generado
if [ -f articulo_revision.pdf ]; then
    echo "📄 Documento generado:"
    ls -lh articulo_revision.pdf
    echo "📊 Número de páginas: $(pdfinfo articulo_revision.pdf 2>/dev/null | grep Pages | awk '{print $2}')"
fi

# Abrir el PDF si el sistema lo permite
if command -v xdg-open &> /dev/null; then
    echo "📖 Abriendo PDF..."
    xdg-open articulo_revision.pdf &
elif command -v open &> /dev/null; then
    echo "📖 Abriendo PDF..."
    open articulo_revision.pdf &
fi