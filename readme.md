# Entregable 1 - Gestion enfermedades

## Introducción

El gestor de enfermedades es una aplicación para investigar que enfermedad tienes en base a tus sintomas de forma sencilla y eficiente. Este repositorio contiene el código fuente del proyecto, así como las instrucciones necesarias para ejecutar la aplicación tanto desde un ejecutable como desde el código fuente.

---

## Requisitos

### Ejecución desde el ejecutable

- Sistema operativo Windows.

### Ejecución desde el código fuente

- Python 3.8 o superior.
- Sistema operativo Windows.

---

## Instrucciones de Ejecución

### Ejecución desde el ejecutable

1. **Desde el directorio dist:**

   - Abre el directorio **`/dist`**.
   - Haz doble clic sobre el archivo **"Gestor Enfermedades.exe"**.

### Ejecución desde el código fuente

#### Configuración inicial

1. Abre el directorio raíz del proyecto.
2. Ejecuta el archivo **`setup_env_windows.bat`** (preferiblemente como administrador) ubicado en la carpeta raíz. Este script realiza las siguientes tareas:
   - Comprueba si Python está instalado.
   - Crea un entorno virtual llamado **`gestor-enfermedades-env`** (si no existe).
   - Activa el entorno virtual.
   - Verifica si el archivo `requirements.txt` existe.
   - Instala las dependencias necesarias especificadas en `requirements.txt`.
   El contenido del script es el siguiente:
   ```batch
   @echo off
   :: Script para activar el entorno virtual y instalar dependencias

   :: Comprueba si Python está instalado
   python --version >nul 2>&1
   if %errorlevel% neq 0 (
       echo Python no está instalado. Por favor, instálalo antes de continuar.
       exit /b
   )

   :: Crea un entorno virtual si no existe
   if not exist "gestor-enfermedades-env" (
       echo Creando el entorno virtual...
       python -m venv task-manager-env
   )

   :: Activa el entorno virtual
   call task-manager-env\Scripts\activate.bat

   :: Comprueba si requirements.txt existe
   if not exist "requirements.txt" (
       echo No se encontró el archivo requirements.txt.
       echo Crea el archivo con las dependencias necesarias y vuelve a ejecutar el script.
       exit /b
   )

   :: Instala las dependencias
   python -m ensurepip
   python -m pip install --upgrade pip
   pip install --upgrade pip
   pip install -r requirements.txt

   :: Confirma que las dependencias fueron instaladas
   echo Dependencias instaladas correctamente.

   echo El entorno está listo. Para desactivarlo, usa el comando "deactivate".
   exit
   ```

#### Ejecución del proyecto

1. Una vez completada la configuración, activa el entorno virtual (si no lo está):
   ```bash
   gestor-enfermedades-env\Scripts\activate.bat
   ```
2. Ejecuta el siguiente comando para iniciar la aplicación:
   ```bash
   python -m init
   ```
3. La aplicación estará disponible para su uso.

---

## Notas Importantes

- **Compatibilidad:** Este proyecto ha sido diseñado y probado en sistemas Windows.
- **Dependencias:** Todas las dependencias necesarias se encuentran listadas en el archivo `requirements.txt`.
- **Entorno virtual:** El uso del entorno virtual garantiza que las dependencias no interfieran con otras aplicaciones o proyectos en tu sistema.

---