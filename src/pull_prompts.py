"""
Script para fazer pull de prompts do LangSmith Prompt Hub.

Este script:
1. Conecta ao LangSmith usando credenciais do .env
2. Faz pull dos prompts do Hub
3. Salva localmente em prompts/bug_to_user_story_v1.yml

SIMPLIFICADO: Usa serialização nativa do LangChain para extrair prompts.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from langchain import hub
from langchain_core.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate
from utils import save_yaml, check_env_vars, print_section_header

load_dotenv()
check_env_vars(["LANGSMITH_API_KEY"])


def extract_prompt_data(prompt_name: str, chat_prompt) -> dict:
    """Extrai system_prompt e user_prompt de um ChatPromptTemplate e monta o dict YAML."""
    system_prompt = ""
    user_prompt = ""

    for msg in chat_prompt.messages:
        if isinstance(msg, SystemMessagePromptTemplate):
            system_prompt = msg.prompt.template
        elif isinstance(msg, HumanMessagePromptTemplate):
            user_prompt = msg.prompt.template

    return {
        prompt_name: {
            "description": f"Prompt para converter relatos de bugs em User Stories",
            "system_prompt": system_prompt,
            "user_prompt": user_prompt,
            "version": "v1",
            "tags": ["bug-analysis", "user-story", "product-management"],
        }
    }


def pull_prompts_from_langsmith():
    prompt_name = "bug_to_user_story_v1"
    output_path = Path("prompts") / f"{prompt_name}.yml"

    chat_prompt = hub.pull(f"leonanluppi/{prompt_name}")

    data = extract_prompt_data(prompt_name, chat_prompt)
    print_section_header(data[prompt_name]["description"])

    ok = save_yaml(data, str(output_path))
    if ok:
        print(f"✅ Prompt salvo em {output_path}")
    else:
        print("❌ Falha ao salvar prompt.")


def main():
    pull_prompts_from_langsmith()


if __name__ == "__main__":
    main()
