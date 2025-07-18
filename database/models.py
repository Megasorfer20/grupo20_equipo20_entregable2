from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, Text, ForeignKey, DateTime
from sqlalchemy.types import TypeDecorator
from sqlalchemy.orm import relationship

import json

Base = declarative_base()


class JSONEncodedList(TypeDecorator):
    impl = Text

    def process_bind_param(self, value, dialect):
        if value is None:
            return "[]"
        return json.dumps(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return []
        return json.loads(value)

class Pacientes(Base):
    __tablename__ = 'pacientes'

    id = Column(Integer, primary_key=True)
    nombre_completo = Column(String)
    apellidos = Column(String)
    fecha_nacimiento = Column(Date)
    genero = Column(String)
    numero_identificacion = Column(Integer)
    celular_contacto = Column(Integer)
    fecha_registro = Column(DateTime)
    
    # Relaciones
    enfermedades = relationship("PacientesEnfermedades", back_populates="paciente", cascade="all, delete-orphan")
    tratamientos = relationship("Tratamientos", back_populates="paciente", cascade="all, delete-orphan")
    alergias = relationship("Alergias", back_populates="paciente", cascade="all, delete-orphan")
    
class Enfermedades(Base):
    __tablename__ = 'enfermedades'

    id = Column(Integer, primary_key=True)
    enfermedad = Column(String)
    recomendacion = Column(String)
    sintomas = Column(JSONEncodedList)
    
    # Relaciones
    pacientes_asociados = relationship("PacientesEnfermedades", back_populates="enfermedad_rel")
    
class PacientesEnfermedades(Base):
    __tablename__ = 'pacientes_enfermedades'

    id = Column(Integer, primary_key=True)
    paciente_id = Column(Integer, ForeignKey('pacientes.id'))
    enfermedad_id = Column(Integer, ForeignKey('enfermedades.id'), nullable=True)
    sintomas = Column(JSONEncodedList)
    fecha_registro = Column(DateTime)
    
    # Relaciones reversas
    paciente = relationship("Pacientes", back_populates="enfermedades")
    enfermedad_rel = relationship("Enfermedades", back_populates="pacientes_asociados")
    
class Sintomas(Base):
    __tablename__ = 'sintomas'

    id = Column(Integer, primary_key=True)
    sintoma = Column(String)

class Tratamientos(Base):
    __tablename__ = 'tratamientos'

    id = Column(Integer, primary_key=True)
    paciente_id = Column(Integer, ForeignKey('pacientes.id'))
    medicamentos = Column(JSONEncodedList)
    dosis_medicamentos = Column(JSONEncodedList)
    fecha_registro = Column(DateTime)
    
    paciente = relationship("Pacientes", back_populates="tratamientos")

class Alergias(Base):
    __tablename__ = 'alergias'

    id = Column(Integer, primary_key=True)
    paciente_id = Column(Integer, ForeignKey('pacientes.id'))
    alergeno = Column(String)
    sintomas = Column(JSONEncodedList)
    fecha_registro = Column(DateTime)
    
    paciente = relationship("Pacientes", back_populates="alergias")

