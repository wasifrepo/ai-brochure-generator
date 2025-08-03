import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from openai import OpenAI
import anthropic
import gradio as gr

# Load API keys from .env
load_dotenv(override=True)
openai_api_key = os.getenv("OPENAI_API_KEY")
anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")

openai = OpenAI(api_key=openai_api_key)
claude = anthropic.Anthropic(api_key=anthropic_api_key)

# System message for the assistant
system_message = (
    "You are an assistant that analyzes the contents of a company website landing page "
    "and creates a short brochure about the company for prospective customers, investors, and recruits. "
    "Respond in markdown."
)

# Streaming response from OpenAI GPT
def stream_gpt(prompt):
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": prompt}
    ]
    stream = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        stream=True
    )
    result = ""
    for chunk in stream:
        result += chunk.choices[0].delta.content or ""
        yield result

# Streaming response from Anthropic Claude
def stream_claude(prompt):
    response = ""
    result = claude.messages.stream(
        model="claude-3-haiku-20240307",
        max_tokens=1000,
        temperature=0.7,
        system=system_message,
        messages=[{"role": "user", "content": prompt}]
    )
    with result as stream:
        for text in stream.text_stream:
            response += text or ""
            yield response

# Class to scrape and parse website contents
class Website:
    def __init__(self, url):
        self.url = url
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, "html.parser")
            self.title = soup.title.string if soup.title else "No title found"
            for tag in soup.body(["script", "style", "img", "input"]):
                tag.decompose()
            self.text = soup.body.get_text(separator="\n", strip=True)
        except Exception as e:
            self.title = "Unable to load page"
            self.text = str(e)

    def get_contents(self):
        return f"Webpage Title:\n{self.title}\nWebpage Contents:\n{self.text}\n\n"

# Main function to generate brochure
def stream_brochure(company_name, url, model):
    yield ""
    prompt = f"Please generate a company brochure for {company_name}. Here is their landing page:\n"
    prompt += Website(url).get_contents()
    if model == "GPT":
        yield from stream_gpt(prompt)
    elif model == "Claude":
        yield from stream_claude(prompt)
    else:
        yield "Invalid model selected."

# Gradio UI
view = gr.Interface(
    fn=stream_brochure,
    inputs=[
        gr.Textbox(label="Company name:"),
        gr.Textbox(label="Landing page URL including http:// or https://"),
        gr.Dropdown(["GPT", "Claude"], label="Select model")
    ],
    outputs=[gr.Markdown(label="Brochure:")],
    flagging_mode="never"
)

if __name__ == "__main__":
    view.launch()