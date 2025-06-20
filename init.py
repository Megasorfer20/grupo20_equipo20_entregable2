import webview # type: ignore
import sys
import os
from database.symptoms import diseases, symptoms

sintomas = []

def disease_recomendations(sintomas):
        for disease in diseases:
            if all(symptom in disease["symptoms"] for symptom in sintomas):
                return f"Podría ser {disease['name']}. {disease['recomendations']}"
        return "No puedo determinar la enfermedad. Por favor, consulta a un médico."


class API:
    def verification(self, sintomas):
        message = disease_recomendations(sintomas)
        return message
    
    def get_sintomas(self):
        return symptoms

def main():
    if hasattr(sys, '_MEIPASS'):
        base_path = os.path.join(sys._MEIPASS, 'frontend')
    else:
        base_path = './frontend'
    
    html_path = os.path.join(base_path, 'index.html')
    
    api = API()

    # webview.create_window('Gestor de pacientes', html_path, js_api=api)
    webview.create_window("Dev", "http://localhost:5173", js_api=api)

    try:
        webview.start(debug=True, http_server=True)
        # webview.start( http_server=True)
    finally:
        print("Cerrando la aplicación...")

if __name__ == "__main__":
    main()