"""
Script para fazer push de prompts otimizados ao LangSmith Prompt Hub.

Este script:
1. Lê os prompts otimizados de prompts/bug_to_user_story_v2.yml
2. Valida os prompts
3. Faz push PÚBLICO para o LangSmith Hub
4. Adiciona metadados (tags, descrição, técnicas utilizadas)

SIMPLIFICADO: Código mais limpo e direto ao ponto.
"""

import os
import sys
from dotenv import load_dotenv
from langchain import hub
from langsmith import Client
from langchain_core.prompts import ChatPromptTemplate
from utils import load_yaml, check_env_vars, print_section_header

load_dotenv()
def push_prompt_to_langsmith(prompt_name: str, prompt_data: dict) -> bool:
    """
    Faz push do prompt otimizado para o LangSmith Hub (PÚBLICO).

    Args:
        prompt_name: Nome do prompt
        prompt_data: Dados do prompt com campos system_prompt, user_prompt, etc.

    Returns:
        True se sucesso, False caso contrário
    """
    try:
        username = os.getenv("USERNAME_LANGSMITH_HUB")
        if not prompt_data:
            print("❌ Falha ao carregar prompt otimizado.")
            return False

        prompt_template = ChatPromptTemplate.from_messages([
            ("system", prompt_data["system_prompt"]),
            ("human", prompt_data["user_prompt"]),
        ])

        hub.push(
            f"{username}/{prompt_name}",
            prompt_template,
            new_repo_is_public=True,
            tags=prompt_data.get("tags", []),
        )
        print(f"✅ Prompt '{username}/{prompt_name}' publicado com sucesso!")
        return True
    except Exception as e:
        print(f"❌ Erro ao fazer push do prompt: {e}")
        return False

def validate_prompt(prompt_data: dict) -> tuple[bool, list]:
    """
    Valida estrutura básica de um prompt (versão simplificada).

    Args:
        prompt_data: Dados do prompt

    Returns:
        (is_valid, errors) - Tupla com status e lista de erros
    """
    ...
    errors = []

    campos_obrigatorios = ["description", "system_prompt", "user_prompt"]
    for campo in campos_obrigatorios:
        if campo not in prompt_data:
            errors.append(f"Campo obrigatório ausente: '{campo}'")
        elif not prompt_data[campo] or not str(prompt_data[campo]).strip():
            errors.append(f"Campo '{campo}' está vazio")

    if "tags" in prompt_data and not isinstance(prompt_data["tags"], list):
        errors.append("Campo 'tags' deve ser uma lista")

    is_valid = len(errors) == 0
    return is_valid, errors
     


def main():
    """Função principal"""
    raw = load_yaml("prompts/bug_to_user_story_v2.yml")
    if raw is None:
        print("❌ Falha ao carregar prompts/bug_to_user_story_v2.yml")
        return False

    # Suporta YAML com dados no nível raiz ou aninhados sob a chave do prompt
    prompt_data = raw.get("bug_to_user_story_v2", raw)

    is_valid, errors = validate_prompt(prompt_data)
    if not is_valid:
        print("❌ Prompt inválido:")
        for error in errors:
            print(f"  - {error}")
        return False

    print_section_header("Prompt otimizado carregado:")
    push_prompt_to_langsmith("bug_to_user_story_v2", prompt_data)

if __name__ == "__main__":
    main()
    
