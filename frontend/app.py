import streamlit as st
import requests
import pandas as pd
import time

st.set_page_config(page_title="Gestión de Estudiantes", layout="wide", page_icon="🎓")

API_URL = "http://web:8000"

st.title("🎓 Sistema de Gestión de Estudiantes")

# Menú de pestañas
tab1, tab2, tab3 = st.tabs(["📋 Lista de Estudiantes", "➕ Registrar Nuevo", "✏️ Administrar (Editar/Borrar)"])

# Listar
with tab1:
    st.header("Directorio de Alumnos")
    
    col_a, col_b = st.columns([1, 4])
    with col_a:
        if st.button("🔄 Actualizar Lista"):
            st.rerun()
    
    try:
        response = requests.get(f"{API_URL}/estudiantes/")
        if response.status_code == 200:
            data = response.json()
            if data:
                df = pd.DataFrame(data)
                # Reordenar columnas para mejor vista
                df_view = df[["id", "codigo", "nombres", "apellidos", "email", "semestre", "activo"]]
                st.dataframe(df_view, use_container_width=True, hide_index=True)
            else:
                st.info("ℹ️ No hay estudiantes registrados todavía.")
        else:
            st.error(f"Error al obtener datos: {response.status_code}")
            
    except Exception as e:
        st.error(f"🚨 Error de conexión con la API: {e}")

# Registrar
with tab2:
    st.header("Ingresar Nuevo Estudiante")
    with st.form("add_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            codigo = st.text_input("Código de Matrícula")
            nombres = st.text_input("Nombres")
            semestre = st.number_input("Semestre", 1, 12, 1)
        with col2:
            apellidos = st.text_input("Apellidos")
            email = st.text_input("Correo Electrónico")
            
        btn_add = st.form_submit_button("Guardar Estudiante", type="primary")
        
        if btn_add:
            if codigo and nombres and apellidos and email:
                payload = {
                    "codigo": codigo,
                    "nombres": nombres,
                    "apellidos": apellidos,
                    "email": email,
                    "semestre": semestre
                }
                try:
                    res = requests.post(f"{API_URL}/estudiantes/", json=payload)
                    if res.status_code == 200:
                        st.success("✅ Estudiante registrado")
                        time.sleep(2)  
                        st.rerun()
                    else:
                        st.error(f"Error: {res.text}")
                except Exception as e:
                    st.error(f"Error de conexión: {e}")
            else:
                st.warning("⚠️ Todos los campos son obligatorios")

# Editar/Borar
with tab3:
    st.header("Modificar o Eliminar")
    st.write("Selecciona un estudiante por su ID para realizar acciones.")
    
    search_id = st.number_input("Buscar por ID del estudiante:", min_value=1, step=1)
    
    if st.button("🔍 Buscar Estudiante"):
        st.session_state['search_id'] = search_id

    if 'search_id' in st.session_state:
        try:
            res_get = requests.get(f"{API_URL}/estudiantes/")
            if res_get.status_code == 200:
                students = res_get.json()
                found = next((item for item in students if item["id"] == st.session_state['search_id']), None)
                
                if found:
                    st.success(f"Estudiante encontrado: {found['nombres']} {found['apellidos']}")
                    
                    # Edicion
                    with st.expander("📝 Editar Datos", expanded=True):
                        with st.form("edit_form"):
                            e_codigo = st.text_input("Código", value=found['codigo'])
                            e_nombres = st.text_input("Nombres", value=found['nombres'])
                            e_apellidos = st.text_input("Apellidos", value=found['apellidos'])
                            e_email = st.text_input("Email", value=found['email'])
                            e_semestre = st.number_input("Semestre", 1, 12, value=found['semestre'])
                            
                            if st.form_submit_button("Guardar Cambios"):
                                payload = {
                                    "codigo": e_codigo,
                                    "nombres": e_nombres,
                                    "apellidos": e_apellidos,
                                    "email": e_email,
                                    "semestre": e_semestre
                                }
                                res_put = requests.put(f"{API_URL}/estudiantes/{found['id']}", json=payload)
                                if res_put.status_code == 200:
                                    st.success(" Datos actualizados")
                                    time.sleep(2)
                                    st.rerun()
                                else:
                                    st.error(f"Error al actualizar: {res_put.text}")
                    
                    st.divider()
                    
                    # Borrado
                    col_del, col_void = st.columns([1, 4])
                    with col_del:
                        if st.button("🗑️ Eliminar Estudiante", type="primary"):
                            res_del = requests.delete(f"{API_URL}/estudiantes/{found['id']}")
                            if res_del.status_code == 200:
                                st.warning("Estudiante eliminado.")
                                time.sleep(2)
                                del st.session_state['search_id']
                                st.rerun()
                            else:
                                st.error(f"No se pudo eliminar: {res_del.text}")
                else:
                    st.warning(" No se encontró ningún estudiante con ese ID.")
            else:
                st.error("Error al conectar con la base de datos.")
                
        except Exception as e:
            st.error(f"Error de conexión: {e}")