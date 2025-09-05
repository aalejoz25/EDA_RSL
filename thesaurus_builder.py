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

    def build_query(self, include_related: bool = False) -> str:
        """Construye la parte de la consulta para este término y sus relaciones"""
        terms = set()
        
        # Añadir el término principal si es preferido o no tiene USE
        if self.is_preferred or not self.use_term:
            terms.add(f'"{self.term}"')
        
        # Añadir término USE si existe
        if self.use_term:
            terms.add(f'"{self.use_term.term}"')
        
        # Añadir términos UF
        terms.update(f'"{t.term}"' for t in self.used_for_terms)
        
        # Añadir términos NT recursivamente
        for nt in self.narrower_terms:
            terms.update(nt.build_query(include_related=False).split(" OR "))
        
        # Opcionalmente añadir términos RT
        if include_related:
            terms.update(f'"{t.term}"' for t in self.related_terms)
        
        # Construir la consulta
        if not terms:
            return f'"{self.term}"'
        
        terms_str = " OR ".join(sorted(terms))
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
    
    def build_search_equation(self, include_related: bool = False) -> str:
        """Construye la ecuación de búsqueda completa"""
        if not self.facets:
            return ""
        
        facet_queries = [facet.build_query(include_related) for facet in self.facets]
        return " AND ".join(f"({query})" for query in facet_queries)

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
