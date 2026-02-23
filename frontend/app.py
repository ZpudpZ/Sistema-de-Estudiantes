import streamlit as st
import requests
import pandas as pd
import time
import re
from components.header import load_css, render_header, section_title

st.set_page_config(
    page_title="CI/CD Test - CRUD() | UNAP",
    layout="wide",
    page_icon="https://aulavirtual2.unap.edu.pe/images/themes/unap/favicon.ico"
)

load_css()
render_header()

API_URL = "http://web:8000"

def validar_datos_academicos(codigo, nombres, apellidos):
    if not codigo.isdigit():
        return False, "Error de Formato: El Código Universitario debe ser numérico."
    if len(codigo) != 6:
        return False, f"Error de Longitud: El Código debe constar de 6 dígitos exactos (Ingresado: {len(codigo)})."

    patron_texto = r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$"
    
    if not re.match(patron_texto, nombres):
        return False, "Carácter Inválido: El campo Nombres contiene símbolos no permitidos."
    if len(nombres.strip()) < 2:
        return False, "Longitud Insuficiente: El nombre es demasiado corto para ser válido."
        
    if not re.match(patron_texto, apellidos):
        return False, "Carácter Inválido: El campo Apellidos contiene símbolos no permitidos."
    if len(apellidos.strip()) < 2:
        return False, "Longitud Insuficiente: El apellido es demasiado corto para ser válido."

    return True, ""

with st.sidebar:
    st.image("https://oti.unap.edu.pe/recursos/oti-ofic.png", width=150)
    st.markdown("### Oficina de Registros")
    st.info("Rol: **Administrador**")
    st.text("Periodo Lectivo: 2026-I")
    st.divider()
    st.caption("Sistema Test -Crud")
    st.caption("© 2026 UNAP - OTI")

tab_padron, tab_matricula, tab_admin = st.tabs(["PADRÓN DE MATRICULADOS", "NUEVA MATRÍCULA", "ADMINISTRACIÓN ACADÉMICA"])

# REPORTE DE MATRICULADOS
with tab_padron:
    section_title("Reporte General de Estudiantes Matriculados", "https://cdn-icons-png.flaticon.com/512/3135/3135715.png")

    try:
        response = requests.get(f"{API_URL}/estudiantes/")
        if response.status_code == 200:
            data = response.json()
            if data:
                df = pd.DataFrame(data)
                
                total_matriculados = len(df)
                estudiantes_regulares = len(df[df['activo'] == True]) if 'activo' in df.columns else total_matriculados
                ciclo_promedio = int(df['semestre'].mean()) if not df.empty else 0
                
                k1, k2, k3 = st.columns(3)
                k1.metric("Total Matriculados", total_matriculados)
                k2.metric("Estudiantes Regulares", estudiantes_regulares)
                k3.metric("Ciclo Académico Promedio", f"{ciclo_promedio}°")
                
                st.divider()

                df_view = df[["id", "codigo", "nombres", "apellidos", "email", "semestre"]]
                df_view.columns = ["ID Sistema", "Código Universitario", "Nombres", "Apellidos", "Correo Institucional", "Ciclo"]
                
                col_btn, col_refresh = st.columns([2, 8])
                with col_btn:
                    csv = df_view.to_csv(index=False).encode("utf-8-sig")
                    st.download_button(
                        label="Exportar Padrón (CSV)",
                        data=csv,
                        file_name="padron_matriculados_2026_1.csv",
                        mime="text/csv"
                    )
                with col_refresh:
                    if st.button("Actualizar Padrón"):
                        st.rerun()

                st.dataframe(
                    df_view, 
                    use_container_width=True, 
                    hide_index=True,
                    column_config={
                        "Ciclo": st.column_config.NumberColumn(format="%d°"),
                        "ID Sistema": st.column_config.NumberColumn(format="%d"),
                    }
                )
            else:
                st.info("El sistema no presenta registros de matrícula para el periodo actual.")
        else:
            st.error(f"Error de comunicación con el servidor central. Código de estado: {response.status_code}")
    except Exception as e:
        st.error(f"Fallo de conexión con el servicio de base de datos: {e}")

# PROCESO DE MATRÍCULA
with tab_matricula:
    section_title("Proceso de Matrícula - Periodo 2026-I", "https://cdn-icons-png.flaticon.com/512/2921/2921222.png")
    
    with st.container(border=True):
        st.markdown("#### Datos del Postulante")
        with st.form("form_matricula", clear_on_submit=True):
            c1, c2 = st.columns(2)
            with c1:
                codigo = st.text_input("Código Universitario", max_chars=6, help="Ingrese el código de 6 dígitos asignado.")
                nombres = st.text_input("Nombres Completos").upper()
                semestre = st.number_input("Ciclo Académico a Matricular", 1, 12, 1)
            with c2:
                apellidos = st.text_input("Apellidos Completos").upper()
                email = st.text_input("Correo Institucional Asignado")

            st.markdown("<br>", unsafe_allow_html=True)
            col_izq, col_der = st.columns([1, 4])
            with col_izq:
                submit_btn = st.form_submit_button("Procesar Matrícula", type="primary")
            
            if submit_btn:
                es_valido, mensaje_error = validar_datos_academicos(codigo, nombres, apellidos)

                if es_valido:
                    payload = {
                        "codigo": codigo, 
                        "nombres": nombres, 
                        "apellidos": apellidos, 
                        "email": email, 
                        "semestre": semestre
                    }
                    try:
                        with st.spinner("Validando requisitos y registrando en base de datos..."):
                            res = requests.post(f"{API_URL}/estudiantes/", json=payload)
                        
                        if res.status_code == 200:
                            st.success(f"MATRÍCULA EXITOSA: El estudiante {apellidos}, {nombres} ha sido inscrito en el ciclo {semestre}.")
                            time.sleep(1.5)
                            st.rerun()
                        else:
                            st.error(f"Error en el proceso de matrícula: {res.text}")
                    except Exception as e:
                        st.error(f"Error crítico de red: {e}")
                else:
                    st.warning(f"Validación Fallida: {mensaje_error}")

# ADMINISTRACIÓN
with tab_admin:
    section_title("Administración de Registros Académicos", "https://cdn-icons-png.flaticon.com/512/3953/3953226.png")
    
    col_search, _ = st.columns([2, 4])
    with col_search:
        search_code = st.text_input("Buscar Estudiante por Código", max_chars=6)
        if st.button("Consultar Expediente"):
            if not search_code:
                st.warning("Ingrese un Código Universitario válido para iniciar la búsqueda.")
            else:
                try:
                    r = requests.get(f"{API_URL}/estudiantes/buscar/{search_code}")
                    if r.status_code == 200:
                        st.session_state['student_found'] = r.json()
                        st.rerun()
                    elif r.status_code == 404:
                        st.warning("No se encuentra el expediente académico solicitado.")
                        if 'student_found' in st.session_state:
                            del st.session_state['student_found']
                    else:
                        st.error(f"Error interno del servidor: {r.status_code}")
                except Exception as e:
                    st.error(f"Error de conectividad: {e}")

    if 'student_found' in st.session_state:
        stu = st.session_state['student_found']
        st.divider()
        st.info(f"Expediente Académico: **{stu['apellidos']}, {stu['nombres']}**")

        with st.expander("Modificación de Datos Académicos", expanded=True):
            with st.form("edit_form"):
                ec1, ec2 = st.columns(2)
                e_cod = ec1.text_input("Código Universitario (Inmutable)", value=stu['codigo'], disabled=True)
                e_nom = ec1.text_input("Nombres", value=stu['nombres']).upper()
                e_sem = ec1.number_input("Ciclo Académico", value=stu['semestre'])
                e_ape = ec2.text_input("Apellidos", value=stu['apellidos']).upper()
                e_ema = ec2.text_input("Correo Institucional", value=stu['email'])

                if st.form_submit_button("Guardar Cambios en Expediente"):
                    if len(e_nom) < 2 or len(e_ape) < 2:
                        st.warning("Error: Los datos personales no cumplen con la longitud mínima requerida.")
                    else:
                        pay = {"codigo": e_cod, "nombres": e_nom, "apellidos": e_ape, "email": e_ema, "semestre": e_sem}
                        try:
                            requests.put(f"{API_URL}/estudiantes/{stu['id']}", json=pay)
                            st.session_state['student_found'].update(pay)
                            st.success("La actualización del expediente se completó correctamente.")
                            time.sleep(1.5)
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error al intentar guardar: {e}")

        st.markdown("---")
        col_del_1, col_del_2 = st.columns([1, 4])
        with col_del_1:
            if st.button("ANULAR MATRÍCULA"):
                try:
                    requests.delete(f"{API_URL}/estudiantes/{stu['id']}")
                    st.success("La matrícula ha sido anulada y el registro eliminado del sistema.")
                    del st.session_state['student_found']
                    time.sleep(1.5)
                    st.rerun()
                except Exception as e:
                    st.error(f"Error al anular matrícula: {e}")