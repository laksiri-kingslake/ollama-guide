import gradio as gr
import requests

OLLAMA_MODEL = "laksiri-en-si-translation:latest"

def chat_with_model(message, history):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": OLLAMA_MODEL,
                "prompt": message,
                "stream": False
            },
            timeout=60
        )

        response.raise_for_status()
        
        # result = response.json()
        # return result.get("response", "⚠️ No response from model")

        result = response.json()
        output = result.get("response", "⚠️ No response from model")
        # Decode Unicode escapes if present
        if isinstance(output, str):
            output = output.encode('utf-8').decode('unicode_escape')
        return output

    except requests.exceptions.RequestException as e:
        print("❌ Request error:", e)
        return f"❌ Request error: {str(e)}"
    except Exception as e:
        print("❌ Unexpected error:", e)
        return f"❌ Unexpected error: {str(e)}"

# Launch Gradio interface
gr.ChatInterface(
    fn=chat_with_model,
    title="English to Sinhala Translator",
    description="Type English sentences and get Sinhala translations using your fine-tuned Ollama model",
    chatbot=gr.Chatbot(show_copy_button=True)
).launch()