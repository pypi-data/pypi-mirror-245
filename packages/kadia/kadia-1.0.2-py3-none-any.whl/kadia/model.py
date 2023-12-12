import confuse
import torch
from ctransformers import AutoModelForCausalLM
from keybert import KeyBERT
from langchain import OpenAI
from lazy import lazy
from transformers import AutoTokenizer

from .llm_manager import LLMManager
from .prompts.base import BasePrompter


class KadiaModel:
    """
    Utility class that manages all nested AI models required for Kadia to be functional.
    Mainly consists of configs and models instances.
    """

    def __init__(self, config: confuse.Configuration):
        self.config = config

    @lazy
    def keyword_extractor(self):
        if self.config["keyword_extraction"]:
            return KeyBERT()

    @lazy
    def llm_manager(self):
        if self.config["llm"]["model_type"] == "llama":
            return LLMManager(
                llm=AutoModelForCausalLM.from_pretrained(
                    **self.config["llm"]["config"].get(dict)
                ),
                prompter=BasePrompter.prompter_from_type(
                    self.config["llm"]["prompter"]["type"].get(str)
                ),
                config=self.config["llm"]["config"].get(dict),
                max_prompt_chars=self.config["llm"]["max_prompt_chars"].get(int),
            )
        elif self.config["llm"]["model_type"] == "mistral":
            return LLMManager(
                llm=AutoModelForCausalLM.from_pretrained(
                    **self.config["llm"]["config"].get(dict)
                ),
                prompter=BasePrompter.prompter_from_type(
                    self.config["llm"]["prompter"]["type"].get(str)
                ),
                config=self.config["llm"]["config"],
                max_prompt_chars=self.config["llm"]["max_prompt_chars"].get(int),
            )
        elif self.config["llm"]["model_type"] == "openai":
            return LLMManager(
                llm=OpenAI(**self.config["llm"]["config"].get(dict)),
                prompter=BasePrompter.prompter_from_type(
                    self.config["llm"]["prompter"]["type"].get(str)
                ),
                config=self.config["llm"]["config"],
                max_prompt_chars=self.config["llm"]["max_prompt_chars"].get(int),
            )
        elif self.config["llm"]["model_type"].get(str) == "petals":
            from petals import AutoDistributedModelForCausalLM

            return LLMManager(
                llm=AutoDistributedModelForCausalLM.from_pretrained(
                    self.config["llm"]["config"]["model_name"].get(str),
                    torch_dtype=getattr(
                        torch, self.config["llm"]["config"]["torch_dtype"].get(str)
                    ),
                    low_cpu_mem_usage=True,
                ),
                prompter=BasePrompter.prompter_from_type(
                    self.config["llm"]["prompter"]["type"].get(str)
                ),
                config=self.config["llm"]["config"],
                max_prompt_chars=self.config["llm"]["max_prompt_chars"].get(int),
                tokenizer=AutoTokenizer.from_pretrained(
                    self.config["llm"]["config"]["model_name"].get(str)
                ),
            )
