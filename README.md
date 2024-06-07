# AI Content Generator

This Streamlit app allows users to generate content using Google Generative AI models. Users can enter text prompts to generate content, upload images to generate descriptions or blog posts, and interact with the model using a user-friendly interface.

## Features
1. **Generate Text Content**: Enter a text prompt to generate content based on the prompt.
2. **Generate Content from Images**: Upload an image and provide a text prompt to generate content describing the image.
3. **Generate Blog Posts from Images**: Upload an image and provide a detailed prompt to generate a comprehensive blog post based on the image.
4. **View Available Models**: Display a list of available AI models that support content generation.

## Requirements
- Python 3.6 or higher
- Streamlit
- Google Generative AI Python client library
- PIL (Python Imaging Library)

## Setup Instructions
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/kuxall/BlogGemini
   cd ai-content-generator
   ```

2. **Install the Required Libraries**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up Google API Key**:
- Store your Google API key securely. For Streamlit, you can add your API key in a .streamlit/secrets.toml file:
	```bash
	[default]
	GOOGLE_API_KEY = "your_google_api_key"
	```
4. **Run the App**:
   ```bash
   streamlit run app.py
   ```
