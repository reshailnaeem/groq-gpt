# GroqGPT
A Streamlit app to use all Groq models in a ChatGPT-like interface.

Parts of this project are based on groq_streamlit_demo by tonykipkemboi, available at [https://github.com/tonykipkemboi/ollama_pdf_rag](https://github.com/tonykipkemboi/groq_streamlit_demo).

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [License](#license)

## Features

- A simple Streamlit UI to use all Groq chat models in a ChatGPT-like interface (API key required)
- Configurable options for temperature, top-p, and maximum tokens
- Ability to save chat history as a .txt file

## Usage

Use any Python >= 3.11 version along with the requirements.txt file in the repository. I used 3.12 with the latest versions of all libraries.

```bash
# Installing using repo file
pip install -r requirements.txt
```

First, if you haven't already, create a free account on [GroqCloud](https://console.groq.com/) and generate a [Groq API Key](https://console.groq.com/keys). Set your Groq API Key as an environment variable:

```bash
export GROQ_API_KEY=<YOUR_GROQ_API_KEY>
```

Run the app using:
```bash
streamlit run app.py
```

You can now access the app locally on:
```bash
http://localhost:8501/
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
