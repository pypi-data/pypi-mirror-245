from enum import Enum


class LLMEnum(Enum):
    OPENAI_GPT_4_32K = ("open_ai", "gpt-4-32k")
    OPENAI_GPT_4 = ("open_ai", "gpt_4")
    OPENAI_GPT_3_5_TURBO = ("open_ai", "gpt-3.5-turbo")
    OPENAI_GPT_3_5_TURBO_16K = ("open_ai", "gpt-3.5-turbo-16k")
    CLAUDE = ("claude", "claude")
    LLAMA_13B = ("llama", "llama_13b")
    LLAMA_70B = ("llama", "llama_70b")
    MISTRAL_7B = ("mistral", "mistral_7b")
