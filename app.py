import textwrap
import google.generativeai as genai
import PIL.Image
import streamlit as st

# Function to convert text to markdown


def to_markdown(text):
    text = text.replace('•', '  *')
    return textwrap.indent(text, '> ', predicate=lambda _: True)

# Function to handle responses and errors


def handle_response(response):
    if response and hasattr(response, 'text'):
        return to_markdown(response.text)
    else:
        return "> Sorry, can't help at this moment."


# Securely store your API key (ensure to replace with your method of storing API keys)
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=GOOGLE_API_KEY)

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Go to", ["Home", "Generate Content", "Generate from Image"])

# Home page
if page == "Home":
    st.title("Welcome to AI Content Generator")
    st.write(
        "This app allows you to generate content using Google Generative AI models.")
    st.write("Navigate using the sidebar to generate content, generate from images, or chat with the model.")

# Generate Content page
elif page == "Generate Content":
    st.header("Generate Content")
    model = genai.GenerativeModel('gemini-1.5-pro-latest')
    prompt = st.text_input("Enter your prompt for content generation:",
                           "Tell me about the historical significance of Lumbini and list the best places to visit there.")
    if st.button('Generate Content'):
        try:
            response = model.generate_content(prompt)
            st.markdown(handle_response(response))
        except Exception as e:
            st.markdown("> Sorry, can't help at this moment.")

# Generate from Image page
elif page == "Generate from Image":
    st.header("Generate Content from Image")
    model = genai.GenerativeModel('gemini-1.5-flash')
    uploaded_file = st.file_uploader(
        "Choose an image...", type=["jpg", "png", "jpeg"])
    image_prompt = st.text_input("Enter your prompt for content generation from image:",
                                 "Describe the content and context of this image.")
    if uploaded_file is not None:
        image = PIL.Image.open(uploaded_file)
        st.image(image, caption='Uploaded Image.', use_column_width=True)
        if st.button('Generate Content from Image'):
            try:
                response = model.generate_content([image_prompt, image])
                st.markdown(handle_response(response))
            except Exception as e:
                st.markdown("> Sorry, can't help at this moment.")
        blog_prompt = st.text_input("Enter your prompt for blog post generation from image:",
                                    "Write a detailed blog post based on this image, including a description of the scene, the people involved, and their activities. If the image is of a place, include information about the location and its significance. If the image is of an event, provide details about the event and its impact. If the image is of a famous person, describe the person's background, personality, and achievements in detail. If the image is of an object, explain its purpose, history, and significance. If the image is abstract, interpret its meaning and significance. You can also include your own thoughts, feelings, and reactions to the image. Be creative and imaginative! You can write in any style or genre you like. Be sure to proofread your blog post for spelling, grammar, and punctuation errors before submitting it. Good luck!")
        if st.button('Generate Blog Post from Image'):
            try:
                response = model.generate_content(
                    [blog_prompt, image], stream=True)
                response.resolve()
                st.markdown(handle_response(response))
            except Exception as e:
                st.markdown("> Sorry, can't help at this moment.")

# Display available models
st.sidebar.header("Available Models")
model_list = genai.list_models()
for m in model_list:
    if 'generateContent' in m.supported_generation_methods:
        st.sidebar.write(m.name)
