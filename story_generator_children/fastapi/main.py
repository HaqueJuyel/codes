
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import FileResponse
import uuid
import os
from fpdf import FPDF
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI client
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# Initialize FastAPI app
app = FastAPI()

# Pydantic model for request payload
class StoryRequest(BaseModel):
    child_name: str
    favorite_animal: str
    theme: str
    quality: str = "standard"  # standard = gpt-3.5, high = gpt-4

@app.post("/generate-story/")
def generate_story(req: StoryRequest):
    # Prompt to generate story
    prompt = (
        f"Write a magical, illustrated children's story about a child named {req.child_name} "
        f"who has a best friend that is a {req.favorite_animal}. Theme: {req.theme}. "
        "The story should be under 500 words, whimsical, and suitable for ages 3–8."
    )

    # Choose GPT model
    model_name = "gpt-4" if req.quality == "high" else "gpt-3.5-turbo"

    # Generate story with OpenAI
    response = client.chat.completions.create(
        model=model_name,
        messages=[{"role": "user", "content": prompt}]
    )
    story = response.choices[0].message.content.strip()

    # Generate image from OpenAI
    image_prompt = f"A cute, storybook-style illustration of a {req.favorite_animal} in a magical setting"
    image_response = client.images.generate(prompt=image_prompt, n=1, size="512x512")
    image_url = image_response.data[0].url

    # Create output directory for PDFs
    os.makedirs("pdfs", exist_ok=True)
    filename = f"{uuid.uuid4()}.pdf"
    pdf_path = os.path.join("pdfs", filename)

    # Load local font
    font_path = os.path.join("fonts", "DejaVuSans.ttf")
    if not os.path.exists(font_path):
        raise FileNotFoundError("Font file not found! Please place DejaVuSans.ttf inside the 'fonts/' folder.")

    # Create PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font("DejaVu", "", font_path, uni=True)
    pdf.set_font("DejaVu", size=12)
    pdf.multi_cell(0, 10, f"StoryWeaver - A Story for {req.child_name}")
    pdf.ln()
    for line in story.split("\n"):
        pdf.multi_cell(0, 10, line)
    pdf.output(pdf_path)

    # Return response
    return {
        "story": story,
        "image_url": image_url,
        "pdf_url": f"/download-pdf/{filename}"
    }

@app.get("/download-pdf/{filename}")
def download_pdf(filename: str):
    file_path = os.path.join("pdfs", filename)
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type='application/pdf', filename=filename)
    return {"error": "File not found"}
