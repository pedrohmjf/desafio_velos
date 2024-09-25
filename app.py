from flask import Flask, request, jsonify, render_template
import pdfplumber
from mlx_lm import load, generate
import json

app = Flask(__name__)

# Inicializando o modelo Hugging Face
model, tokenizer = load("mlx-community/Phi-3-mini-4k-instruct-4bit")

# Função para converter o PDF em texto
def pdf_to_text(pdf_file):
    with pdfplumber.open(pdf_file) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
    return text

# Rota para servir a página HTML
@app.route("/")
def index():
    return render_template("index.html")

# Rota para processar o PDF
@app.route("/process_pdf", methods=["POST"])
def process_pdf():
    if "pdf" not in request.files:
        return jsonify({"error": "Nenhum PDF foi enviado."}), 400
    
    pdf_file = request.files["pdf"]
    
    # Converter o PDF para texto
    transcription = pdf_to_text(pdf_file)
    
    # Definir o prompt com a transcrição extraída
    messages = [ {"role": "system", "content": """
              você é uma IA amigável
              """}, 
             {"role": "user", "content": "olá"},]

    input_ids = tokenizer.apply_chat_template(messages, add_generation_prompt=True)
    
    prompt = tokenizer.decode(input_ids)

    # Usar o modelo Hugging Face para gerar a análise
    generated_text = generate(model, tokenizer, prompt=prompt, verbose=True,  max_tokens=512)
    
    print(generated_text)
    # Simulação de como os dados seriam extraídos da resposta
    result = {
        "full_response": generated_text
    }
    
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
