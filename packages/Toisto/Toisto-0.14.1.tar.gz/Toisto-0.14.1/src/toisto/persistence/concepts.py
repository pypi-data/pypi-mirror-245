"""Load concepts from concept files and generate quizzes."""

from argparse import ArgumentParser
from pathlib import Path
from typing import NoReturn

from ..metadata import NAME
from ..model.language.concept import Concept, ConceptId, ConceptIds
from ..model.language.concept_factory import create_concept
from .json_file import load_json


class ConceptIdRegistry:
    """Registry to check the uniqueness of concept identifiers across concept files."""

    def __init__(self, argument_parser: ArgumentParser) -> None:
        self.argument_parser = argument_parser
        self.concept_files_by_concept_id: dict[ConceptId, Path] = {}

    def check_concept_ids(self, concept_ids: ConceptIds, concept_file: Path) -> None:
        """Check that the concept ids are unique."""
        for concept_id in concept_ids:
            self._check_concept_id(concept_id, concept_file)

    def _check_concept_id(self, concept_id: ConceptId, concept_file: Path) -> None:
        """Check that the concept id is unique."""
        if concept_id in self.concept_files_by_concept_id:
            other_concept_file = self.concept_files_by_concept_id[concept_id]
            self.argument_parser.error(
                f"{NAME} cannot read concept file {concept_file}: concept identifier '{concept_id}' also occurs in "
                f"concept file {other_concept_file}.\nConcept identifiers must be unique across concept files.\n",
            )

    def register_concept_ids(self, concept_ids: ConceptIds, concept_file: Path) -> None:
        """Register the concept ids."""
        for concept_id in concept_ids:
            self.concept_files_by_concept_id[concept_id] = concept_file


def load_concepts(
    concept_files: list[Path],
    concept_id_registry: ConceptIdRegistry,
    argument_parser: ArgumentParser,
) -> set[Concept] | NoReturn:
    """Load the concepts from the specified concept files and with the specified levels."""
    all_concepts = set()
    for concept_file in concept_files:
        concepts = []
        try:
            for concept_key, concept_value in load_json(concept_file).items():
                concept = create_concept(concept_key, concept_value)
                concepts.append(concept)
        except Exception as reason:  # noqa: BLE001
            argument_parser.error(f"{NAME} cannot read concept file {concept_file}: {reason}.\n")
        concept_ids = tuple(concept.concept_id for concept in concepts)
        concept_id_registry.check_concept_ids(concept_ids, concept_file)
        concept_id_registry.register_concept_ids(concept_ids, concept_file)
        all_concepts |= set(concepts)
    return all_concepts
