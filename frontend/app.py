import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Gestión de Estudiantes", layout="wide", page_icon="🎓")

API_URL = "http://web:8000"

st.title("🎓 Sistema de Gestión de Estudiantes")

# Menú de pestañas para organizar mejor
tab1, tab2, tab3 = st.tabs(["📋 Lista de Estudiantes", "➕ Registrar Nuevo", "✏️ Administrar (Editar/Borrar)"])

# --- PESTAÑA 1: LISTAR ---
with tab1:
    st.header("Directorio de Alumnos")
    if st.button("🔄 Actualizar Lista"):
        st.rerun()
    
    try:
        response = requests.get(f"{API_URL}/estudiantes/")
        if response.status_code == 200:
            data = response.json()
            if data:
                df = pd.DataFrame(data)
                # Reordenar columnas y ocultar ID si quieres
                df_view = df[["id", "codigo", "nombres", "apellidos", "email", "semestre", "activo"]]
                st.dataframe(df_view, use_container_width=True, hide_index=True)
            else:
                st.info("No hay estudiantes registrados.")
    except Exception as e:
        st.error(f"Error de conexión: {e}")

# --- PESTAÑA 2: REGISTRAR ---
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
                    "codigo": codigo, "nombres": nombres, "apellidos": apellidos,
                    "email": email, "semestre": semestre
                }
                res = requests.post(f"{API_URL}/estudiantes/", json=payload)
                if res.status_code == 200:
                    st.success("✅ Estudiante registrado exitosamente")
                    st.rerun()
                else:
                    st.error(f"Error: {res.text}")
            else:
                st.warning("⚠️ Todos los campos son obligatorios")

# --- PESTAÑA 3: ADMINISTRAR (EDITAR/BORRAR) ---
with tab3:
    st.header("Modificar o Eliminar")
    st.write("Selecciona un estudiante por su ID para realizar acciones.")
    
    # Buscador simple por ID
    search_id = st.number_input("Buscar por ID del estudiante:", min_value=1, step=1)
    
    if st.button("🔍 Buscar Estudiante"):
        # Guardamos en session_state para no perderlo al recargar
        st.session_state['search_id'] = search_id

    # Si ya buscamos, mostramos las opciones
    if 'search_id' in st.session_state:
        # Intentamos obtener los datos actuales
        try:
            res_get = requests.get(f"{API_URL}/estudiantes/")
            students = res_get.json()
            # Filtramos en Python (idealmente sería un endpoint get_by_id, pero esto funciona)
            found = next((item for item in students if item["id"] == st.session_state['search_id']), None)
            
            if found:
                st.success(f"Estudiante encontrado: {found['nombres']} {found['apellidos']}")
                
                with st.expander("📝 Editar Datos", expanded=True):
                    with st.form("edit_form"):
                        e_codigo = st.text_input("Código", value=found['codigo'])
                        e_nombres = st.text_input("Nombres", value=found['nombres'])
                        e_apellidos = st.text_input("Apellidos", value=found['apellidos'])
                        e_email = st.text_input("Email", value=found['email'])
                        e_semestre = st.number_input("Semestre", 1, 12, value=found['semestre'])
                        
                        if st.form_submit_button("💾 Guardar Cambios"):
                            payload = {
                                "codigo": e_codigo, "nombres": e_nombres, "apellidos": e_apellidos,
                                "email": e_email, "semestre": e_semestre
                            }
                            res_put = requests.put(f"{API_URL}/estudiantes/{found['id']}", json=payload)
                            if res_put.status_code == 200:
                                st.success("Datos actualizados correctamente")
                                st.rerun()
                            else:
                                st.error("Error al actualizar")

                st.divider()
                
                col_del, _ = st.columns([1, 4])
                with col_del:
                    if st.button("🗑️ Eliminar Estudiante", type="primary"):
                        res_del = requests.delete(f"{API_URL}/estudiantes/{found['id']}")
                        if res_del.status_code == 200:
                            st.warning("Estudiante eliminado.")
                            # Limpiamos la búsqueda
                            del st.session_state['search_id']
                            st.rerun()
                        else:
                            st.error("No se pudo eliminar")
            else:
                st.warning("❌ No se encontró ningún estudiante con ese ID.")
        except Exception as e:
            st.error("Error de conexión con la API")