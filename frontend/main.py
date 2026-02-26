import streamlit as st
import requests
import pandas as pd
import time
import re
from components.header import load_css, render_header, section_title

st.set_page_config(
    page_title="Sistema de Gestión Operativa | OTI UNAP",
    layout="wide",
    page_icon="https://oti.unap.edu.pe/recursos/oti-ofic.png"
)

load_css()
render_header()

API_URL = "http://web:8000"

def check_backend_connectivity():
    max_retries = 3
    for i in range(max_retries):
        try:
            response = requests.get(f"{API_URL}/", timeout=2)
            if response.status_code == 200: return True
        except:
            if i < max_retries - 1: time.sleep(2)
    return False

if 'backend_ready' not in st.session_state:
    with st.status("Verificando servicios internos...", expanded=True) as status:
        if check_backend_connectivity():
            st.session_state['backend_ready'] = True
            status.update(label="Conexión establecida con éxito", state="complete", expanded=False)
        else:
            st.error("ERROR DE INFRAESTRUCTURA: El servicio de datos no responde.")
            st.info("Verifique el estado del contenedor backend y la base de datos en AWS.")
            st.stop()

def validar_inputs(codigo, nombres, apellidos, email):
    if not codigo.isdigit() or len(codigo) != 6:
        return False, "El Identificador debe ser numérico y de 6 dígitos."
    patron_texto = r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$"
    if not re.match(patron_texto, nombres.strip()) or not re.match(patron_texto, apellidos.strip()):
        return False, "Los campos de texto no deben contener caracteres especiales o números."
    if not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email):
        return False, "Dirección de correo electrónico no válida."
    return True, ""

# SIDEBAR PROFESIONAL
with st.sidebar:
    st.image("https://oti.unap.edu.pe/recursos/oti-ofic.png", width=140)
    st.markdown("---")
    st.subheader("Panel de Control")
    st.caption("Terminal de Administración")
    st.write("**Servidor:** AWS EC2")
    st.write("**Entorno:** Producción")
    
    # Espaciado para mover el botón al fondo
    for _ in range(12): st.write("")
    
    st.markdown("---")
    if st.button("Restablecer Entorno", use_container_width=True, help="Limpia la caché de sesión actual"):
        st.session_state.clear()
        st.rerun()

tab_view, tab_new, tab_edit = st.tabs([
    "CONSULTA DE REGISTROS", 
    "ALTA DE INFORMACIÓN", 
    "MODIFICACIÓN Y CONTROL"
])

# TAB 1: CONSULTA
with tab_view:
    section_title("Base de Datos Operativa", "https://cdn-icons-png.flaticon.com/512/3135/3135715.png")
    try:
        response = requests.get(f"{API_URL}/estudiantes/", timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data:
                df = pd.DataFrame(data)
                m1, m2, m3 = st.columns(3)
                m1.metric("Registros Totales", len(df))
                m2.metric("Promedio Categoría", f"{df['semestre'].mean():.1f}")
                m3.metric("Sincronización", "Activa")
                
                st.divider()
                df_view = df[["id", "codigo", "nombres", "apellidos", "email", "semestre"]]
                df_view.columns = ["ID", "Código", "Nombres", "Apellidos", "Email", "Nivel"]
                
                st.dataframe(
                    df_view, 
                    use_container_width=True, 
                    hide_index=True,
                    column_config={"Nivel": st.column_config.NumberColumn(format="%d"), "ID": st.column_config.NumberColumn(format="%d")}
                )
            else:
                st.info("No se han detectado registros en el repositorio central.")
    except Exception as e:
        st.error(f"Fallo en consulta: {e}")

# TAB 2: ALTA
with tab_new:
    section_title("Ingreso de Nuevo Expediente", "https://cdn-icons-png.flaticon.com/512/2921/2921222.png")
    with st.form("registro_form", clear_on_submit=True):
        col_a, col_b = st.columns(2)
        with col_a:
            codigo = st.text_input("Identificador Único (6 dígitos)", max_chars=6)
            nombres = st.text_input("Nombres Completos").upper()
            semestre = st.number_input("Nivel Académico / Ciclo", 1, 14, 1)
        with col_b:
            apellidos = st.text_input("Apellidos Completos").upper()
            email = st.text_input("Correo Institucional / Contacto")

        if st.form_submit_button("Procesar e Inscribir", type="primary"):
            valido, err = validar_inputs(codigo, nombres, apellidos, email)
            if valido:
                payload = {"codigo": codigo, "nombres": nombres, "apellidos": apellidos, "email": email, "semestre": semestre}
                try:
                    res = requests.post(f"{API_URL}/estudiantes/", json=payload)
                    if res.status_code == 201:
                        st.success("Operación exitosa: Registro consolidado.")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error(f"Error {res.status_code}: {res.json().get('detail', 'Conflicto de datos')}")
                except Exception as e:
                    st.error(f"Error de comunicación con API: {e}")
            else:
                st.warning(err)

# TAB 3: CONTROL
with tab_edit:
    section_title("Módulo de Administración y Edición", "https://cdn-icons-png.flaticon.com/512/3953/3953226.png")
    
    sc1, sc2 = st.columns([2, 4])
    with sc1:
        search_id = st.text_input("Buscar Identificador", max_chars=6, placeholder="Ingrese Código")
        btn_search = st.button("Localizar Expediente", use_container_width=True)

    if btn_search and search_id:
        try:
            r = requests.get(f"{API_URL}/estudiantes/buscar/{search_id}")
            if r.status_code == 200:
                st.session_state['active_item'] = r.json()
            else:
                st.warning("No se localizó ningún registro con el identificador proporcionado.")
                st.session_state.pop('active_item', None)
        except:
            st.error("Error al conectar con la base de datos.")

    if 'active_item' in st.session_state:
        item = st.session_state['active_item']
        st.markdown("---")
        with st.expander(f"Editor de Registro - Ref: {item['codigo']}", expanded=True):
            with st.form("update_form"):
                u1, u2 = st.columns(2)
                u_nom = u1.text_input("Nombres", value=item['nombres']).upper()
                u_sem = u1.number_input("Nivel", 1, 14, value=item['semestre'])
                u_ape = u2.text_input("Apellidos", value=item['apellidos']).upper()
                u_ema = u2.text_input("Email", value=item['email'])

                if st.form_submit_button("Actualizar Base de Datos"):
                    up_load = {"codigo": item['codigo'], "nombres": u_nom, "apellidos": u_ape, "email": u_ema, "semestre": u_sem}
                    res_up = requests.put(f"{API_URL}/estudiantes/{item['id']}", json=up_load)
                    if res_up.status_code == 200:
                        st.success("Registro actualizado correctamente.")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("Error al procesar actualización.")

        if st.button("ELIMINAR REGISTRO DE FORMA PERMANENTE", type="secondary", use_container_width=True):
            if requests.delete(f"{API_URL}/estudiantes/{item['id']}").status_code == 200:
                st.success("El registro ha sido eliminado físicamente.")
                st.session_state.pop('active_item', None)
                time.sleep(1)
                st.rerun()