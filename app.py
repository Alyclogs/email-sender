from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

EMAIL_ADDRESS = os.getenv("SENDER_EMAIL")
EMAIL_PASSWORD = os.getenv("SENDER_PASSWORD")

def cargar_plantilla_html(file_name, props: dict[str, str]):
    with open(f"templates/{file_name}.html", "r", encoding="utf-8") as file:
        html = file.read()

    for prop, value in props.items():
        html = html.replace(prop, value)  
    
    return html

def enviar_correo(correo, html_content):
    msg = MIMEMultipart()
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = correo
    msg["Subject"] = "Verificación de correo"

    msg.attach(MIMEText(html_content, "html"))

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, correo, msg.as_string())

@app.route("/verify-email", methods=["POST"])
def send_verify_email():

    try:
        data = request.json
        correo = data.get("correo")
        codigo = data.get("codigo")

        if not correo or not codigo:
            return jsonify({"error": "Faltan datos"}), 400

        html_content = cargar_plantilla_html('verificar-email', {
            "{code}": codigo
        })
        enviar_correo(correo, html_content)

        return jsonify({"mensaje": "Correo enviado"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route("/reset-password", methods=["POST"])
def send_reset_password_email():

    try:
        data = request.json
        nombre = data.get("nombre")
        correo = data.get("correo")
        codigo = data.get("codigo")

        if not nombre or not correo or not codigo:
            return jsonify({"error": "Faltan datos"}), 400

        html_content = cargar_plantilla_html('reestablecer-contrasena', {
            "{name}": nombre,
            "{code}": codigo
        })
        enviar_correo(correo, html_content)

        return jsonify({"mensaje": "Correo enviado"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route("/cita-details", methods=["POST"])
def send_cita_details_email():

    try:
        data = request.json
        nombre = data.get("name")
        correo = data.get("email")
        codigo_cita = data.get("cita_code")
        sede_nombre = data.get("sede_name")
        ubicacion = data.get("address")
        ubicacion_url = data.get("address_url")
        fecha = data.get("date")
        app_link = data.get("app_link")

        if not nombre or not correo or not codigo_cita or not ubicacion or not ubicacion_url or not fecha:
            return jsonify({"error": "Faltan datos"}), 400

        html_content = cargar_plantilla_html('cita-agendada', {
            "{name}": nombre,
            "{cita_code}": codigo_cita,
            "{sede_direccion}": ubicacion,
            "{sede_nombre}": sede_nombre,
            "{sede_direccion_url}": ubicacion_url,
            "{fecha_cita}": fecha,
            "{app_link}": app_link or "http://link-to-app.com"
        })
        enviar_correo(correo, html_content)

        return jsonify({"mensaje": "Correo enviado"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=False, port=5000)
