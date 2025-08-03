🧠 AI Brochure Generator

A simple AI-powered tool that creates a professional marketing brochure from any company's website. Just enter the company name and its URL — the app scrapes the landing page and uses either GPT (OpenAI) or Claude (Anthropic) to generate a clean, readable brochure in markdown format.

---

🚀 Features

- 🧠 Choose between GPT or Claude models
- 🌐 Scrapes live content from any company website
- 📝 Outputs a formatted brochure ready for use
- ⚡ Real-time streaming responses
- 🖥️ Clean and minimal Gradio-based UI

---

🛠 Tech Stack

- Python
- Gradio
- OpenAI GPT (via `openai` SDK)
- Claude (via `anthropic` SDK)
- BeautifulSoup for web scraping
- `dotenv` for environment variable handling

---

⚙️ Setup Instructions

1. Clone the repo
git clone https://github.com/wasifrepo/ai-brochure-generator.git
cd ai-brochure-generator

2. Install dependencies
pip install -r requirements.txt

3. Add your API keys
Create a .env file by copying the example:

cp .env.example .env
Then fill in your OpenAI and Anthropic API keys inside .env.

4. Run the app
python app.py


💡 Example Use
Company Name: OpenAI
Website: https://openai.com
Model: GPT or Claude
Output: A short brochure summarizing the company’s mission, services, values, and more — all in markdown format.

