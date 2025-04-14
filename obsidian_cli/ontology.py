from typing import Dict, List

class Ontology:
    def __init__(self, relationships: Dict[str, Dict[str, List[str]]]):
        self.parent_relations = relationships.get("parent", {})
        self.sibling_relations = relationships.get("sibling", {})

    def get_parents(self, child_type: str) -> List[str]:
        """Retourne les types de parents valides pour un type donné."""
        return [parent for parent, children in self.parent_relations.items() if child_type in children]

    def get_children(self, parent_type: str) -> List[str]:
        """Retourne les types d'enfants valides pour un type donné."""
        return self.parent_relations.get(parent_type, [])

    def get_siblings(self, note_type: str) -> List[str]:
        """Retourne les types de notes acceptant ce type en lien de fratrie."""
        return [main_type for main_type, siblings in self.sibling_relations.items() if note_type in siblings]

    def is_valid_parent(self, parent_type: str, child_type: str) -> bool:
        return child_type in self.parent_relations.get(parent_type, [])

    def is_valid_sibling(self, type1: str, type2: str) -> bool:
        return type2 in self.sibling_relations.get(type1, []) or type1 in self.sibling_relations.get(type2, [])
