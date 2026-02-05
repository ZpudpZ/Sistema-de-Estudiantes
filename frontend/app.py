import streamlit as st
import requests
import pandas as pd
import time
from components.header import load_css, render_header, section_title

st.set_page_config(
    page_title="SIGA | UNAP",
    # Sistema Integrado de Gestión Académica
    layout="wide",
    page_icon="https://aulavirtual2.unap.edu.pe/images/themes/unap/favicon.ico"
)

load_css()
render_header()

API_URL = "http://web:8000"

# NAVEGACION
tab1, tab2, tab3 = st.tabs(["DIRECTORIO", "INSCRIPCIÓN", "GESTIÓN"])

# LISTADO
with tab1:
    section_title("Listado General de Estudiantes", "https://cdn-icons-png.flaticon.com/512/3135/3135715.png")

    if st.button("Actualizar Tabla"):
        st.rerun()
    
    try:
        response = requests.get(f"{API_URL}/estudiantes/")
        if response.status_code == 200:
            data = response.json()
            if data:
                df = pd.DataFrame(data)
                df_view = df[["id", "codigo", "nombres", "apellidos", "email", "semestre", "activo"]]
                
                df_view.columns = ["ID", "Matrícula", "Nombres", "Apellidos", "Email", "Semestre", "Activo"]
                
                st.dataframe(
                    df_view, 
                    use_container_width=True, 
                    hide_index=True,
                    column_config={
                        "Semestre": st.column_config.NumberColumn(format="%d°"),
                    }
                )
            else:
                st.info("La base de datos se encuentra vacía.")
        else:
            st.error(f"Error de Servidor: {response.status_code}")
    except Exception as e:
        st.error(f"Error de conexión con API: {e}")

# REGISTRO
with tab2:
    section_title("Ficha de Inscripción", "https://cdn-icons-png.flaticon.com/512/2921/2921222.png")
    
    with st.container(border=True):
        with st.form("add_form", clear_on_submit=True):
            c1, c2 = st.columns(2)
            with c1:
                codigo = st.text_input("Código de Matrícula")
                nombres = st.text_input("Nombres")
                semestre = st.number_input("Semestre", 1, 12, 1)
            with c2:
                apellidos = st.text_input("Apellidos")
                email = st.text_input("Correo Institucional")

            st.markdown("<br>", unsafe_allow_html=True)
            if st.form_submit_button("Registrar Postulante"):
                if codigo and nombres and apellidos:
                    payload = {"codigo": codigo, "nombres": nombres, "apellidos": apellidos, "email": email, "semestre": semestre}
                    try:
                        res = requests.post(f"{API_URL}/estudiantes/", json=payload)
                        if res.status_code == 200:
                            st.success("Transacción Exitosa: Estudiante registrado.")
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.error(f"Error: {res.text}")
                    except Exception as e:
                        st.error(f"Error de Red: {e}")
                else:
                    st.warning("Validación: Debe completar los campos obligatorios.")

# GESTIÓN
with tab3:
    section_title("Gestión y Mantenimiento", "https://cdn-icons-png.flaticon.com/512/3953/3953226.png")
    
    col_search, _ = st.columns([2, 4])
    with col_search:
        search_id = st.number_input("ID del Estudiante", min_value=1, step=1)
        if st.button("Consultar Base de Datos"):
            try:
                r = requests.get(f"{API_URL}/estudiantes/{search_id}")
                if r.status_code == 200:
                    st.session_state['student_found'] = r.json()
                else:
                    st.warning("No se encontraron resultados para ese ID.")
            except Exception as e:
                st.error(f"Error: {e}")

    if 'student_found' in st.session_state:
        stu = st.session_state['student_found']
        st.divider()
        st.success(f"Estudiante seleccionado: {stu['apellidos']}, {stu['nombres']}")

        with st.expander("Editar Información Académica", expanded=True):
            with st.form("edit_form"):
                ec1, ec2 = st.columns(2)
                e_cod = ec1.text_input("Código", value=stu['codigo'])
                e_nom = ec1.text_input("Nombres", value=stu['nombres'])
                e_sem = ec1.number_input("Semestre", value=stu['semestre'])
                e_ape = ec2.text_input("Apellidos", value=stu['apellidos'])
                e_ema = ec2.text_input("Email", value=stu['email'])

                if st.form_submit_button("Guardar Cambios"):
                    pay = {"codigo": e_cod, "nombres": e_nom, "apellidos": e_ape, "email": e_ema, "semestre": e_sem}
                    requests.put(f"{API_URL}/estudiantes/{stu['id']}", json=pay)
                    st.success("Datos actualizados correctamente.")
                    time.sleep(1)
                    st.rerun()

        st.markdown("---")
        if st.button("ELIMINAR REGISTRO PERMANENTEMENTE"):
            requests.delete(f"{API_URL}/estudiantes/{stu['id']}")
            st.warning("Registro eliminado del sistema.")
            del st.session_state['student_found']
            time.sleep(1)
            st.rerun()