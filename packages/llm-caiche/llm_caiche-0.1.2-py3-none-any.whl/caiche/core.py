from caiche.enums import LLMEnum
import requests


class Caiche:
    def __init__(
            self,
            api_key: str,
            model_type: LLMEnum = LLMEnum.OPENAI_GPT_3_5_TURBO):
        self.model_type = model_type
        self.api_key = api_key
        self.error = None

        if self.model_type in [
            LLMEnum.CLAUDE,
            LLMEnum.LLAMA_13B,
            LLMEnum.LLAMA_70B,
        ]:
            self.error = (
                f"The support for the model "
                + self.model_type.value[1]
                + " will be available in the next versions."
            )

    def query(self, prompt: str, disable_cache: bool = False):
        if self.error is not None:
            return {"error": self.error}

        body = {
            "prompt": prompt,
            "openai_api_key": self.api_key,
            "model_type": self.model_type.value[1],
        }

        if not disable_cache:
            body["use_cache"] = True

        response = requests.post(
            "https://tvtzp4kpbtsfuh7tdjtuv36bhe0fnkyt.lambda-url.eu-north-1.on.aws/",
            json=body,
        )

        try:
            return response.json()
        except Exception:
            return {
                "status": 500,
                "error": (
                    "Wrong response format. Please, contact support or add PR."
                ),
            }
