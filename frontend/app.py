import streamlit as st
import requests
import pandas as pd

# Configuración de la página
st.set_page_config(page_title="Gestión de Estudiantes", layout="wide")

# URL del Backend (Nombre del servicio en Docker:puerto)
# Ojo: Cuando el navegador del usuario (tu laptop) entra, usa localhost.
# Pero Streamlit corre en el servidor. Usaremos el nombre de la red interna de Docker.
API_URL = "http://web:8000" 

st.title("🎓 Sistema de Gestión de Estudiantes")

# --- BARRA LATERAL PARA AGREGAR ---
with st.sidebar:
    st.header("Nuevo Estudiante")
    with st.form("add_student_form"):
        codigo = st.text_input("Código")
        nombres = st.text_input("Nombres")
        apellidos = st.text_input("Apellidos")
        email = st.text_input("Email")
        semestre = st.number_input("Semestre", min_value=1, max_value=12, step=1)
        
        submitted = st.form_submit_button("Registrar")
        
        if submitted:
            student_data = {
                "codigo": codigo,
                "nombres": nombres,
                "apellidos": apellidos,
                "email": email,
                "semestre": semestre
            }
            try:
                # Petición POST a tu API
                response = requests.post(f"{API_URL}/estudiantes/", json=student_data)
                if response.status_code == 200:
                    st.success("¡Estudiante registrado exitosamente!")
                else:
                    st.error(f"Error: {response.json().get('detail', 'Desconocido')}")
            except Exception as e:
                st.error(f"No se pudo conectar con el API: {e}")

# --- ÁREA PRINCIPAL: LISTADO ---
st.subheader("Lista de Estudiantes")

if st.button("🔄 Actualizar Lista"):
    st.rerun()

try:
    # Petición GET a tu API
    response = requests.get(f"{API_URL}/estudiantes/")
    if response.status_code == 200:
        students = response.json()
        if students:
            # Convertimos JSON a DataFrame para que se vea bonito
            df = pd.DataFrame(students)
            # Seleccionamos y renombramos columnas para la vista
            df_display = df[['codigo', 'nombres', 'apellidos', 'email', 'semestre', 'activo']]
            st.dataframe(df_display, use_container_width=True)
        else:
            st.info("No hay estudiantes registrados aún.")
    else:
        st.error("Error al obtener la lista.")
except Exception as e:
    st.warning(f"No se pudo conectar con el Backend. ¿Está encendido? Error: {e}")