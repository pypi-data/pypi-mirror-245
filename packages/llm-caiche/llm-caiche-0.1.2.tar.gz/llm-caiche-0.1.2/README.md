# Caiche: Unified Language Model Cache
[![Supported Versions](https://img.shields.io/pypi/pyversions/requests.svg)](https://pypi.org/project/llm-caiche/)

Welcome to **Caiche** – your gateway to efficient and cached language model interactions! 🚀

## What is Caiche?

Caiche is a Unified Language Model Cache designed to streamline your language model queries. Imagine a world where you can ask a question and instantly get a response, thanks to a global vector database that stores and retrieves prompt-response pairs. That's Caiche for you – making your language model interactions faster and cheaper.

## Installation

Installing Caiche is a breeze. Open your terminal and run:

```bash
pip install llm-caiche
```

## Getting Started

Now that you have Caiche installed, let's dive into some quick code snippets to get you started:

```python
from caiche import Caiche

# Replace <OPENAI_API_KEY> with your actual OpenAI API key
cai = Caiche(api_key="<OPENAI_API_KEY>")

# Ask a question and get a response
result = cai.query("What is the capital of Bulgaria?")
```

And just like that, you're ready to unlock the power of cached language model responses!

## Why Caiche?

### 1. **Cheaper Responses**
   Enjoy cost savings as you won't be charged for inference costs when a response is cached.

### 2. **Faster Queries**
   Caiche eliminates the need to wait for language models to generate responses by storing and retrieving previous interactions. Say goodbye to unnecessary delays!

### 3. **Global Database**
   Your prompts and responses are stored globally, allowing you to benefit from a vast database of interactions. Join the Caiche community and contribute to a shared knowledge space.

## What's Next?

At Caiche, we're not just stopping at efficient cached responses. Our vision extends beyond, aiming to redefine the landscape of language model interactions. Here's a glimpse of what's on the horizon:

### **Approximate Cache for Semantically Similar Prompts**
   We're actively working on building an approximate cache that goes beyond storing exact prompt-response pairs. Our goal is to leverage the collected data to lower costs not only for existing prompts but also for prompts that are semantically similar. Imagine getting cost-efficient responses for a range of related queries, making your interactions even more budget-friendly and responsive.

## Community and Contributions

We believe in the power of community collaboration. If you have ideas, improvements, or want to report issues, head over to our [GitHub repository](https://github.com/structuraize/caiche) and let your voice be heard!

## Example Use Cases

1. **Conversational Agents**
   Enhance the user experience of your chatbots and conversational agents by tapping into the Caiche global database.

2. **Research and Development**
   Expedite your language model experimentation process by utilizing stored interactions for quicker testing.

## Contributing

[//]: # (We welcome contributions of all kinds. Whether it's bug fixes, new features, or improvements to the documentation, your input is valuable. Check out our [contribution guidelines]&#40;CONTRIBUTING.md&#41; to get started.)
We will be adding contributing guidelines soon.

## License

Caiche is licensed under the [MIT License](LICENSE). Feel free to explore, modify, and share!

---

Ready to revolutionize your language model interactions? Install Caiche, explore the possibilities, and join us on this exciting journey!

Happy querying! 🚀✨
