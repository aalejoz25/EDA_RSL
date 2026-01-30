#!/bin/bash

# Script de compilación para artículo MDPI en español
# Versión: 1.0
# Autor: Sistema de compilación LaTeX

# Colores para salida
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # Sin color

# Nombre del archivo principal (sin extensión)
MAIN_FILE="articulo_plantilla_ES"

# Función para imprimir mensajes con color
print_info() {
    echo -e "${BLUE}$1${NC}"
}

print_success() {
    echo -e "${GREEN}$1${NC}"
}

print_warning() {
    echo -e "${YELLOW}$1${NC}"
}

print_error() {
    echo -e "${RED}$1${NC}"
}

# Verificar que el archivo .tex existe
if [ ! -f "${MAIN_FILE}.tex" ]; then
    print_error "❌ Error: No se encuentra el archivo ${MAIN_FILE}.tex"
    exit 1
fi

# Función de limpieza
cleanup() {
    print_info "🧹 Limpiando archivos temporales..."
    rm -f "${MAIN_FILE}.aux" "${MAIN_FILE}.log" "${MAIN_FILE}.out" \
          "${MAIN_FILE}.blg" "${MAIN_FILE}.toc" "${MAIN_FILE}.lof" \
          "${MAIN_FILE}.lot" "${MAIN_FILE}.fls" "${MAIN_FILE}.fdb_latexmk" \
          "${MAIN_FILE}.synctex.gz"
}

# Compilación principal
print_info "🔄 Compilando revisión sistemática de literatura (Español)..."

# Primera pasada de pdflatex
print_info "📝 Primera compilación (pdflatex)..."
pdflatex -interaction=nonstopmode "${MAIN_FILE}.tex" > /dev/null 2>&1
if [ $? -ne 0 ]; then
    print_warning "⚠️  Advertencias en la primera compilación"
fi

# Procesar bibliografía
print_info "📚 Procesando referencias bibliográficas..."
bibtex "${MAIN_FILE}" 2>&1 | tee bibtex.log
if [ $? -ne 0 ]; then
    print_warning "⚠️  Advertencias en el procesamiento de bibliografía"
    cat bibtex.log
fi

# Segunda pasada de pdflatex
print_info "📝 Segunda compilación (pdflatex)..."
pdflatex -interaction=nonstopmode "${MAIN_FILE}.tex" > /dev/null 2>&1
if [ $? -ne 0 ]; then
    print_warning "⚠️  Advertencias en la segunda compilación"
fi

# Tercera pasada de pdflatex (para referencias cruzadas)
print_info "📝 Tercera compilación (pdflatex)..."
pdflatex -interaction=nonstopmode "${MAIN_FILE}.tex" > /dev/null 2>&1
if [ $? -ne 0 ]; then
    print_warning "⚠️  Advertencias en la tercera compilación"
fi

# Limpiar archivos temporales
cleanup
rm -f bibtex.log

# Verificar si se generó el PDF
if [ -f "${MAIN_FILE}.pdf" ]; then
    print_success "✅ Compilación completada: ${MAIN_FILE}.pdf"
    print_info "📄 Documento generado:"
    ls -lh "${MAIN_FILE}.pdf"
else
    print_error "❌ Error: No se generó el archivo PDF"
    exit 1
fi

exit 0
