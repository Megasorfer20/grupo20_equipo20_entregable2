import webview
import sys
import os
from difflib import get_close_matches
from datetime import datetime
from database.database import create_database, cerrar_db, session
from database.models import Pacientes, Tratamientos, Alergias, Sintomas, Enfermedades, PacientesEnfermedades
from difflib import SequenceMatcher
from datetime import datetime

class API:
    def serialize_paciente(self, paciente):
        return {
            "id": paciente.id,
            "nombre_completo": paciente.nombre_completo,
            "fecha_nacimiento": paciente.fecha_nacimiento.strftime('%Y-%m-%d'),
            "genero": paciente.genero,
            "numero_identificacion": paciente.numero_identificacion,
            "celular_contacto": paciente.celular_contacto,
            "fecha_registro": paciente.fecha_registro.strftime('%Y-%m-%d')
        }
        
    def buscar_paciente(self, query):
        try:
            paciente = session.query(Pacientes).filter_by(numero_identificacion=query).first()
            if paciente:
                return self.serialize_paciente(paciente)

            nombres = session.query(Pacientes.nombre_completo).all()
            nombres = [n[0] for n in nombres]

            matches = get_close_matches(query, nombres, n=1, cutoff=0.6)
            if matches:
                paciente = session.query(Pacientes).filter_by(nombre_completo=matches[0]).first()
                return self.serialize_paciente(paciente)

            return {} 
        except Exception as e:
            return {"error": str(e)}
        
    def add_paciente(self, paciente):
        try:
            paciente['fecha_nacimiento'] = datetime.strptime(paciente['fecha_nacimiento'], '%Y-%m-%d').date()
            paciente['fecha_registro'] = datetime.strptime(paciente['fecha_registro'], '%Y-%m-%d').date()
            nuevo_paciente = Pacientes(**paciente)
            session.add(nuevo_paciente)
            session.commit()
            message = "Paciente agregado correctamente."
            return message
        except Exception as e:
            session.rollback()
            message = f"Error al agregar el paciente: {str(e)}"
            return message
    
    def actualizar_paciente(self, paciente_actualizado):
        try:
            paciente = session.query(Pacientes).get(paciente_actualizado['id'])
            if not paciente:
                return "Paciente no encontrado"

            paciente.nombre_completo = paciente_actualizado['nombre_completo']
            paciente.fecha_nacimiento = datetime.strptime(paciente_actualizado['fecha_nacimiento'], '%Y-%m-%d').date()
            paciente.genero = paciente_actualizado['genero']
            paciente.celular_contacto = paciente_actualizado['celular_contacto']

            session.commit()
            return "Paciente actualizado correctamente"
        except Exception as e:
            session.rollback()
            return f"Error al actualizar paciente: {str(e)}"
        
    def add_tratamiento(self, datos):
        try:
            datos['fecha_registro'] = datetime.strptime(datos['fecha_registro'], '%Y-%m-%d').date()
            nuevo = Tratamientos(**datos)
            session.add(nuevo)
            session.commit()
            return "Tratamiento registrado correctamente."
        except Exception as e:
            session.rollback()
            return f"Error al registrar tratamiento: {str(e)}"
    
    def add_alergia(self, datos):
        try:
            datos['fecha_registro'] = datetime.strptime(datos['fecha_registro'], '%Y-%m-%d').date()
            nueva_alergia = Alergias(**datos)
            session.add(nueva_alergia)
            session.commit()
            return "Alergia registrada correctamente."
        except Exception as e:
            session.rollback()
            return f"Error al registrar alergia: {str(e)}"
    
    def obtener_sintomas(self):
        try:
            sintomas = session.query(Sintomas).all()
            return [{"id": s.id, "sintoma": s.sintoma} for s in sintomas]
        except Exception as e:
            return {"error": str(e)}
        
    def registrar_enfermedad_paciente(self, datos):
        try:
            sintomas_paciente = datos.get("sintomas", [])
            fecha_registro = datetime.strptime(datos['fecha_registro'], '%Y-%m-%d').date()
            paciente_id = datos['paciente_id']

            enfermedades = session.query(Enfermedades).all()
            mejor_match = None
            max_score = 0

            for enf in enfermedades:
                # Comparación por coincidencia de síntomas
                coincidencias = sum(1 for s in sintomas_paciente if s in enf.sintomas)
                score = coincidencias / max(len(enf.sintomas), 1)

                if score > max_score:
                    mejor_match = enf
                    max_score = score

            if mejor_match and max_score >= 1:
                enfermedad_id = mejor_match.id
                recomendacion = mejor_match.recomendacion
                mensaje = f"El paciente tiene {mejor_match.enfermedad}.\nRecomendación: {recomendacion}"
            else:
                enfermedad_id = None
                mensaje = "No tenemos la información para identificar la enfermedad.\nEl paciente debe visitar un médico para un mejor diagnóstico."

            nueva_relacion = PacientesEnfermedades(
                paciente_id=paciente_id,
                enfermedad_id=enfermedad_id,
                sintomas=sintomas_paciente,
                fecha_registro=fecha_registro
            )

            session.add(nueva_relacion)
            session.commit()

            return mensaje

        except Exception as e:
            session.rollback()
            return f"Error al registrar la enfermedad: {str(e)}"
        
    def obtener_enfermedades_paciente(self, paciente_id):
        relaciones = session.query(PacientesEnfermedades).filter_by(paciente_id=paciente_id).all()
        return [{
            "id": r.id,
            "nombre": r.enfermedad_rel.enfermedad if r.enfermedad_rel else None,
            "sintomas": r.sintomas,
            "fecha_registro": r.fecha_registro.isoformat()
        } for r in relaciones]

    def obtener_alergias_paciente(self, paciente_id):
        alergias = session.query(Alergias).filter_by(paciente_id=paciente_id).all()
        return [{
            "id": a.id,
            "alergeno": a.alergeno,
            "sintomas": a.sintomas,
            "fecha_registro": a.fecha_registro.isoformat()
        } for a in alergias]

    def obtener_tratamientos_paciente(self, paciente_id):
        tratamientos = session.query(Tratamientos).filter_by(paciente_id=paciente_id).all()
        return [{
            "id": t.id,
            "medicamentos": t.medicamentos,
            "dosis_medicamentos": t.dosis_medicamentos,
            "fecha_registro": t.fecha_registro.isoformat()
        } for t in tratamientos]


        
    

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
        create_database()
        
        webview.start(debug=True, http_server=True)
        # webview.start( http_server=True)
    finally:
        print("Cerrando la aplicación...")
        cerrar_db()

if __name__ == "__main__":
    main()