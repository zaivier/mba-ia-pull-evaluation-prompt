"""
Testes automatizados para validação de prompts.
"""
import pytest
import yaml
import sys
from pathlib import Path

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from utils import validate_prompt_structure

PROMPT_FILE_PATH = str(Path(__file__).parent.parent / "prompts" / "bug_to_user_story_v2.yml")

def load_prompts(file_path: str):
    """Carrega prompts do arquivo YAML."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

class TestPrompts:
    def test_prompt_has_system_prompt(self):
        """Verifica se o campo 'system_prompt' existe e não está vazio."""
        raw_data = load_prompts(PROMPT_FILE_PATH)
        prompt_data = next(iter(raw_data.values()))
        system_prompt = prompt_data.get("system_prompt", "")
        assert system_prompt and system_prompt.strip(), "system_prompt deve existir e não estar vazio"

    def test_prompt_has_role_definition(self):
        """Verifica se o prompt define uma persona (ex: "Você é um Product Manager")."""
        raw_data = load_prompts(PROMPT_FILE_PATH)
        prompt_data = next(iter(raw_data.values()))
        system_prompt = prompt_data.get("system_prompt", "").lower()
        role_definition_keywords = ["você é", "you are", "atue como", "act as", "seu papel é", "sua função é"]
        has_role_definition = any(keyword in system_prompt for keyword in role_definition_keywords)
        assert has_role_definition, "system_prompt deve definir uma persona ou papel (ex: 'Você é um...')"

    def test_prompt_mentions_format(self):
        """Verifica se o prompt exige formato Markdown ou User Story padrão."""
        raw_data = load_prompts(PROMPT_FILE_PATH)
        prompt_data = next(iter(raw_data.values()))
        system_prompt = prompt_data.get("system_prompt", "").lower()
        format_keywords = ["markdown", "user story", "formato", "format"]
        has_format_requirement = any(keyword in system_prompt for keyword in format_keywords)
        assert has_format_requirement, "system_prompt deve mencionar Markdown ou User Story como formato exigido"

    def test_prompt_has_few_shot_examples(self):
        """Verifica se o prompt contém exemplos de entrada/saída (técnica Few-shot)."""
        raw_data = load_prompts(PROMPT_FILE_PATH)
        prompt_data = next(iter(raw_data.values()))
        system_prompt = prompt_data.get("system_prompt", "").lower()
        has_input_examples = "input" in system_prompt or "entrada" in system_prompt
        has_output_examples = "output" in system_prompt or "saída" in system_prompt
        assert has_input_examples and has_output_examples, "system_prompt deve conter exemplos de entrada/saída (few-shot)"

    def test_prompt_no_todos(self):
        """Garante que você não esqueceu nenhum `[TODO]` no texto."""
        raw_data = load_prompts(PROMPT_FILE_PATH)
        prompt_data = next(iter(raw_data.values()))
        system_prompt = prompt_data.get("system_prompt", "")
        user_prompt = prompt_data.get("user_prompt", "")
        assert "[TODO]" not in system_prompt, "system_prompt contém [TODO] não resolvido"
        assert "[TODO]" not in user_prompt, "user_prompt contém [TODO] não resolvido"

    def test_minimum_techniques(self):
        """Verifica (através dos metadados do yaml) se pelo menos 2 técnicas foram listadas."""
        raw_data = load_prompts(PROMPT_FILE_PATH)
        prompt_data = next(iter(raw_data.values()))
        techniques_applied = prompt_data.get("techniques_applied", [])
        assert len(techniques_applied) >= 2, f"Mínimo de 2 técnicas requeridas, encontradas: {len(techniques_applied)}"

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])