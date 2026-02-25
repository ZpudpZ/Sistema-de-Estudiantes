import streamlit as st
import requests
import pandas as pd
import time
import re
from components.header import load_css, render_header, section_title

st.set_page_config(
    page_title="Gestión CRUD - simple (OTI) | UNAP",
    layout="wide",
    page_icon="https://aulavirtual2.unap.edu.pe/images/themes/unap/favicon.ico"
)

load_css()
render_header()

API_URL = "http://web:8000"

def check_backend_connectivity():
    max_retries = 5
    for i in range(max_retries):
        try:
            response = requests.get(f"{API_URL}/", timeout=3)
            if response.status_code == 200:
                return True
        except requests.exceptions.ConnectionError:
            if i < max_retries - 1:
                time.sleep(3)
            continue
    return False

if 'backend_ready' not in st.session_state:
    with st.spinner("Estableciendo conexión con el servicio académico..."):
        if check_backend_connectivity():
            st.session_state['backend_ready'] = True
        else:
            st.error("Error Crítico: No se pudo establecer conexión con el Backend (web:8000).")
            st.info("Asegúrese de que el contenedor 'web' esté corriendo y MySQL esté Healthy.")
            st.stop()

def validar_datos_academicos(codigo, nombres, apellidos, email):
    if not codigo.isdigit() or len(codigo) != 6:
        return False, "El Código Universitario debe ser numérico y de 6 dígitos."
    
    patron_texto = r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$"
    if not re.match(patron_texto, nombres.strip()) or not re.match(patron_texto, apellidos.strip()):
        return False, "Nombres y Apellidos solo deben contener letras."
    
    patron_email = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    if not re.match(patron_email, email):
        return False, "El formato del correo institucional es inválido."

    return True, ""

with st.sidebar:
    st.image("https://oti.unap.edu.pe/recursos/oti-ofic.png", width=150)
    st.markdown("### Control de Acceso")
    st.info("Rol: **Administrador OTI**")
    st.divider()
    if st.button("Limpiar Caché de Sesión", use_container_width=True):
        st.session_state.clear()
        st.rerun()

tab_padron, tab_matricula, tab_admin = st.tabs(["PADRÓN DE MATRICULADOS", "NUEVA MATRÍCULA", "ADMINISTRACIÓN ACADÉMICA"])

# TAB 1
with tab_padron:
    section_title("Padrón General de Estudiantes", "https://cdn-icons-png.flaticon.com/512/3135/3135715.png")

    try:
        response = requests.get(f"{API_URL}/estudiantes/", timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data:
                df = pd.DataFrame(data)
                k1, k2, k3 = st.columns(3)
                k1.metric("Total Registrados", len(df))
                k2.metric("Ciclo Promedio", f"{int(df['semestre'].mean())}°")
                k3.metric("Estado de Servicio", "Operativo", delta_color="normal")
                
                st.divider()
                df_view = df[["id", "codigo", "nombres", "apellidos", "email", "semestre"]]
                df_view.columns = ["ID", "Código", "Nombres", "Apellidos", "Email", "Ciclo"]
                
                st.dataframe(
                    df_view, 
                    use_container_width=True, 
                    hide_index=True,
                    column_config={
                        "Ciclo": st.column_config.NumberColumn(format="%d°"),
                        "ID": st.column_config.NumberColumn(format="%d"),
                    }
                )
            else:
                st.info("No existen registros en el sistema.")
        else:
            st.error(f"Error del Servidor ({response.status_code}): No se pudo recuperar el padrón.")
    except Exception as e:
        st.error(f"Error al conectar con el Padrón: {e}")

# TAB 2
with tab_matricula:
    section_title("Registro de Nueva Matrícula", "https://cdn-icons-png.flaticon.com/512/2921/2921222.png")
    
    with st.form("form_matricula", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            codigo = st.text_input("Código Universitario", max_chars=6)
            nombres = st.text_input("Nombres").upper()
            semestre = st.number_input("Ciclo Académico", 1, 14, 1)
        with c2:
            apellidos = st.text_input("Apellidos").upper()
            email = st.text_input("Email Institucional")

        if st.form_submit_button("Confirmar Registro", type="primary"):
            valido, error_msg = validar_datos_academicos(codigo, nombres, apellidos, email)
            
            if valido:
                payload = {"codigo": codigo, "nombres": nombres, "apellidos": apellidos, "email": email, "semestre": semestre}
                try:
                    res = requests.post(f"{API_URL}/estudiantes/", json=payload)
                    if res.status_code == 201:
                        st.success("Estudiante registrado exitosamente en el sistema.")
                        time.sleep(1.2)
                        st.rerun()
                    else:
                        detalle = res.json().get('detail', 'Error desconocido')
                        st.error(f"Error {res.status_code}: {detalle}")
                except Exception as e:
                    st.error(f"Fallo de comunicación: {e}")
            else:
                st.warning(error_msg)

# TAB 3
with tab_admin:
    section_title("Gestión de Expedientes", "https://cdn-icons-png.flaticon.com/512/3953/3953226.png")
    
    col_search, _ = st.columns([3, 5])
    with col_search:
        search_code = st.text_input("Buscar por Código Universitario", max_chars=6)
        buscar = st.button("Consultar Expediente", use_container_width=True)

    if buscar and search_code:
        try:
            r = requests.get(f"{API_URL}/estudiantes/buscar/{search_code}")
            if r.status_code == 200:
                st.session_state['current_student'] = r.json()
            else:
                st.warning("No se encontró ningún estudiante con ese código.")
                st.session_state.pop('current_student', None)
        except Exception as e:
            st.error(f"Error de red: {e}")

    if 'current_student' in st.session_state:
        stu = st.session_state['current_student']
        st.divider()
        
        with st.expander(f"Editar Expediente: {stu['codigo']}", expanded=True):
            with st.form("edit_form"):
                ec1, ec2 = st.columns(2)
                e_nom = ec1.text_input("Nombres", value=stu['nombres']).upper()
                e_sem = ec1.number_input("Ciclo", 1, 14, value=stu['semestre'])
                e_ape = ec2.text_input("Apellidos", value=stu['apellidos']).upper()
                e_ema = ec2.text_input("Email", value=stu['email'])

                if st.form_submit_button("Actualizar Registro"):
                    update_payload = {"codigo": stu['codigo'], "nombres": e_nom, "apellidos": e_ape, "email": e_ema, "semestre": e_sem}
                    res_upd = requests.put(f"{API_URL}/estudiantes/{stu['id']}", json=update_payload)
                    
                    if res_upd.status_code == 200:
                        st.success("Cambios guardados correctamente.")
                        st.session_state['current_student'].update(update_payload)
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error(f"Error al actualizar: {res_upd.text}")

        if st.button("ELIMINAR REGISTRO DEFINITIVAMENTE", type="secondary"):
            res_del = requests.delete(f"{API_URL}/estudiantes/{stu['id']}")
            if res_del.status_code == 200:
                st.success("Registro eliminado del sistema.")
                st.session_state.pop('current_student', None)
                time.sleep(1)
                st.rerun()
            else:
                st.error("No se pudo eliminar el registro.")