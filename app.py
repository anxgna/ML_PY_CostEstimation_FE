import gradio as gr
import httpx
import os
from config import API_BASE_URL

def predict(area, bedrooms, bathrooms, stories, mainroad, guestroom, basement, hotwaterheating, airconditioning):
    payload = {
        "area": area,
        "bedrooms": bedrooms,
        "bathrooms": bathrooms,
        "stories": stories,
        "mainroad": mainroad,
        "guestroom": guestroom,
        "basement": basement,
        "hotwaterheating": hotwaterheating,
        "airconditioning": airconditioning
    }
    try:
        response = httpx.post(f"{API_BASE_URL}/predict", json=payload)
        if response.status_code == 200:
            data = response.json()
            return f"Predicted Price: ${data['predicted_price']:.2f}\nModel Version: {data.get('model_version', 'N/A')}"
        else:
            return f"Error: {response.text}"
    except Exception as e:
        return f"Error connecting to backend: {str(e)}"

def get_history():
    response = httpx.get(f"{API_BASE_URL}/predictions")
    if response.status_code == 200:
        return response.json()
    return []

with gr.Blocks() as demo:
    gr.Markdown("# House Price Estimation")
    with gr.Row():
        with gr.Column():
            area = gr.Number(label="Area (sq ft)", value=0)
            bedrooms = gr.Number(label="Bedrooms", value=0)
            bathrooms = gr.Number(label="Bathrooms", value=0)
            stories = gr.Number(label="Stories", value=1)
            mainroad = gr.Checkbox(label="Main Road")
            guestroom = gr.Checkbox(label="Guest Room")
            basement = gr.Checkbox(label="Basement")
            hotwaterheating = gr.Checkbox(label="Hot Water Heating")
            airconditioning = gr.Checkbox(label="Air Conditioning")
            predict_btn = gr.Button("Predict")
            output = gr.Textbox(label="Result")
            predict_btn.click(fn=predict, inputs=[area, bedrooms, bathrooms, stories, mainroad, guestroom, basement, hotwaterheating, airconditioning], outputs=output)
        with gr.Column():
            history_btn = gr.Button("Show History")
            history_table = gr.Dataframe(headers=["id", "price", "model_version", "created_at"], label="Prediction History")
            history_btn.click(fn=get_history, inputs=None, outputs=history_table)

demo.launch(
    server_name="0.0.0.0", 
    server_port=10000, 
    share=False,
    allowed_paths=["/"]
)

