from typing import Dict, List, Set, Optional
from enum import Enum

class RelationType(Enum):
    BT = "BT"  # Broader Term
    NT = "NT"  # Narrower Term
    RT = "RT"  # Related Term
    UF = "UF"  # Used For
    USE = "USE"  # Use

class ThesaurusTerm:
    def __init__(self, 
                 term: str, 
                 scope_note: str = None,
                 qualifier: str = None,
                 is_preferred: bool = True):
        self.term = term
        self.scope_note = scope_note
        self.qualifier = qualifier
        self.is_preferred = is_preferred
        
        # Relaciones
        self.broader_terms: Set[ThesaurusTerm] = set()
        self.narrower_terms: Set[ThesaurusTerm] = set()
        self.related_terms: Set[ThesaurusTerm] = set()
        self.used_for_terms: Set[ThesaurusTerm] = set()
        self.use_term: Optional[ThesaurusTerm] = None
    
    def add_relation(self, relation_type: RelationType, term: 'ThesaurusTerm'):
        """Añade una relación con otro término"""
        if relation_type == RelationType.BT:
            self.broader_terms.add(term)
            term.narrower_terms.add(self)
        elif relation_type == RelationType.NT:
            self.narrower_terms.add(term)
            term.broader_terms.add(self)
        elif relation_type == RelationType.RT:
            self.related_terms.add(term)
            term.related_terms.add(self)
        elif relation_type == RelationType.UF:
            self.used_for_terms.add(term)
            term.use_term = self
        elif relation_type == RelationType.USE:
            self.use_term = term
            term.used_for_terms.add(self)

    def _get_all_terms(self, terms_set: Set[str], include_related: bool):
        """Método recursivo para recolectar todos los términos en una jerarquía."""
        # Añadir el término principal si es preferido o no tiene USE
        if self.is_preferred or not self.use_term:
            terms_set.add(f'"{self.term}"')
        
        # Añadir término USE si existe
        if self.use_term:
            terms_set.add(f'"{self.use_term.term}"')
        
        # Añadir términos UF (sinónimos)
        for t in self.used_for_terms:
            terms_set.add(f'"{t.term}"')
        
        # Opcionalmente añadir términos RT
        if include_related:
            for t in self.related_terms:
                terms_set.add(f'"{t.term}"')
        
        # Recursión para términos NT
        for nt in self.narrower_terms:
            nt._get_all_terms(terms_set, include_related)

    def build_query(self, include_related: bool = False, for_wos: bool = False) -> str:
        """Construye la parte de la consulta para este término y sus relaciones"""
        terms = set()
        self._get_all_terms(terms, include_related)
        
        # Construir la consulta
        if not terms:
            return f'"{self.term}"'
        
        terms_str = " OR ".join(sorted(list(terms)))
        # Para WoS, evitamos paréntesis extras en grupos pequeños
        if for_wos:
            return terms_str
        return f"({terms_str})" if len(terms) > 1 else terms_str

class ThesaurusBuilder:
    def __init__(self):
        self.facets: List[ThesaurusTerm] = []
        self.all_terms: Dict[str, ThesaurusTerm] = {}
    
    def add_term(self, 
                 term: str, 
                 scope_note: str = None,
                 qualifier: str = None,
                 is_preferred: bool = True) -> ThesaurusTerm:
        """Añade un nuevo término al tesauro"""
        if term in self.all_terms:
            return self.all_terms[term]
        
        new_term = ThesaurusTerm(term, scope_note, qualifier, is_preferred)
        self.all_terms[term] = new_term
        return new_term
    
    def add_facet(self, term: ThesaurusTerm):
        """Añade una faceta principal a la ecuación de búsqueda"""
        self.facets.append(term)

    def print_thesaurus_structure(self, term, level=0, visited=None):
        """Imprime la estructura jerárquica del tesauro.
        
        Args:
            term (ThesaurusTerm): El término a mostrar
            level (int): Nivel de indentación actual
            visited (set): Conjunto de términos ya visitados para evitar ciclos
        """
        if visited is None:
            visited = set()
        
        if term.term in visited:
            return
        visited.add(term.term)
        
        indent = "  " * level
        print(f"{indent}└── {term.term}")
        
        if term.scope_note:
            print(f"{indent}    SN: {term.scope_note}")
        
        if not term.is_preferred:
            print(f"{indent}    USE: {term.use_term.term}")
        
        if term.used_for_terms:
            print(f"{indent}    UF: {', '.join(t.term for t in term.used_for_terms)}")
        
        if term.related_terms:
            print(f"{indent}    RT: {', '.join(t.term for t in term.related_terms)}")
        
        for nt in term.narrower_terms:
            self.print_thesaurus_structure(nt, level + 1, visited)
    
    def build_search_equation(self, include_related: bool = False, database: str = 'generic') -> str:
        """
        Construye la ecuación de búsqueda completa, adaptada a la sintaxis de diferentes bases de datos.
        
        :param include_related: Si es True, incluye términos relacionados (RT).
        :param database: La base de datos de destino. Opciones: 'scopus', 'wos', 'ieee', 'sciencedirect', 'generic'.
        :return: La ecuación de búsqueda formateada.
        """
        if not self.facets:
            return ""
        
        # Construye la consulta para cada faceta
        facet_queries = [f"({facet.build_query(include_related)})" for facet in self.facets]
        
        if database == 'sciencedirect':
            # ScienceDirect tiene un límite de 8 operadores booleanos en total
            max_operators = 8
            num_facets = len(self.facets)
            
            # Necesitamos (num_facets - 1) operadores AND para conectar todas las facetas
            and_operators = num_facets - 1
            # Los operadores OR restantes se distribuyen entre las facetas
            remaining_or_ops = max_operators - and_operators
            # Calculamos cuántos operadores OR podemos usar por faceta
            or_ops_per_facet = remaining_or_ops // num_facets
            
            simplified_facets = []
            
            # Procesar cada faceta
            for facet in self.facets:
                # Recolectar y priorizar términos
                priority_terms = []
                
                # 1. Término principal (más importante)
                if facet.is_preferred:
                    priority_terms.append(f'"{facet.term}"')
                elif facet.use_term:
                    priority_terms.append(f'"{facet.use_term.term}"')
                
                # 2. Términos más específicos importantes (NT)
                def get_important_specific_terms(term, depth=0, max_depth=2):
                    if depth >= max_depth:
                        return
                    for nt in sorted(term.narrower_terms, key=lambda x: x.term):
                        if nt.is_preferred:
                            priority_terms.append(f'"{nt.term}"')
                        get_important_specific_terms(nt, depth + 1, max_depth)
                
                get_important_specific_terms(facet)
                
                # 3. Sinónimos más usados (UF)
                for t in sorted(facet.used_for_terms, key=lambda x: x.term)[:1]:
                    priority_terms.append(f'"{t.term}"')
                
                # 4. Un término relacionado importante si se solicita
                if include_related and facet.related_terms:
                    rt = min(facet.related_terms, key=lambda x: x.term)
                    if rt.is_preferred:
                        priority_terms.append(f'"{rt.term}"')
                
                # Seleccionar términos respetando el límite de operadores OR por faceta
                selected_terms = priority_terms[:or_ops_per_facet + 1]
                
                # Crear la subconsulta para esta faceta
                if len(selected_terms) > 1:
                    simplified_facets.append(f"({' OR '.join(selected_terms)})")
                else:
                    simplified_facets.append(selected_terms[0])
            
            # Unir todas las facetas con AND
            query_body = " AND ".join(simplified_facets)
            return f"TITLE-ABS-KEY({query_body})"
        
        # Une las facetas con AND para formar el cuerpo de la consulta
        query_body = " AND ".join(facet_queries)
        
        # Aplica el formato específico de la base de datos
        if database == 'scopus':
            # Scopus usa una sintaxis similar para buscar en título, resumen y palabras clave
            facet_queries = []
            for facet in self.facets:
                terms = facet.build_query(include_related=include_related)
                # Si hay múltiples términos, ya vendrán con paréntesis del método build_query
                facet_queries.append(terms)
            
            query_body = " AND ".join(facet_queries)
            return f"TITLE-ABS-KEY({query_body})"
            
        elif database == 'ieee':
            # IEEE Xplore prefiere un formato para su "Command Search"
            # Envolvemos cada faceta en ("All Metadata": ...) para la mejor compatibilidad
            ieee_facets = [f'{facet.build_query(include_related)}' for facet in self.facets]
            return " AND ".join(ieee_facets)

        elif database == 'wos':
            # Web of Science usa el campo TS (Topic) para buscar en título, resumen y palabras clave
            facet_queries = []
            for facet in self.facets:
                terms = facet.build_query(include_related=include_related, for_wos=True)
                facet_queries.append(f"({terms})")
            
            query_body = " AND ".join(facet_queries)
            return f"{query_body}"

        else: # 'generic' o cualquier otro valor
            # Formato genérico para Google Scholar o para pegar en campos de búsqueda avanzada
            return query_body

# Ejemplo de uso
if __name__ == "__main__":
    # Crear el constructor
    builder = ThesaurusBuilder()
    
    # Crear términos con notas de alcance y calificadores
    ai = builder.add_term("artificial intelligence", 
                         scope_note="Use for AI and artificial intelligence systems")
    ml = builder.add_term("machine learning",
                         scope_note="Systems that can learn from data")
    dl = builder.add_term("deep learning",
                         scope_note="Neural network-based learning systems")
    
    # Establecer relaciones
    ml.add_relation(RelationType.BT, ai)  # ML es un término más específico que AI
    dl.add_relation(RelationType.NT, ml)  # DL es un término más específico que ML
    
    # Añadir términos no preferidos
    ai_alt = builder.add_term("AI", is_preferred=False)
    ai_alt.add_relation(RelationType.USE, ai)  # AI debe usar "artificial intelligence"
    
    # Crear faceta de calidad
    quality = builder.add_term("fruit quality",
                             scope_note="Quality attributes of fruits")
    
    # Añadir facetas principales
    builder.add_facet(ai)
    builder.add_facet(quality)
    
    # Construir ecuación
    print(builder.build_search_equation())
