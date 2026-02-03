import streamlit as st
import requests
import pandas as pd
import time

st.set_page_config(page_title="Gestión de Estudiantes", layout="wide", page_icon="🎓")

API_URL = "http://web:8000"

st.title("👨‍🎓 Sistema de Gestión de Estudiantes")

# Menú de pestañas
tab1, tab2, tab3 = st.tabs(["📋 Lista de Estudiantes", "➕ Registrar Nuevo", "⚙️ Administrar (Editar/Borrar)"])

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
        st.error(f"🔌 Error de conexión con la API: {e}")

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

# Editar/Borrar
with tab3:
    st.header("Modificar o Eliminar")
    st.write("Ingresa el ID de un estudiante para buscarlo y realizar acciones.")

    search_id = st.number_input("Buscar por ID del estudiante:", min_value=1, step=1, key="search_id_input")

    if st.button("🔍 Buscar Estudiante"):
        # Limpiar estado anterior antes de una nueva búsqueda
        if 'student_found' in st.session_state:
            del st.session_state['student_found']

        try:
            # Petición directa al endpoint del estudiante específico
            response = requests.get(f"{API_URL}/estudiantes/{search_id}")

            if response.status_code == 200:
                # Estudiante encontrado (guarda el estado de la sesión)
                st.session_state['student_found'] = response.json()
            elif response.status_code == 404:
                st.warning("🚫 No se encontró ningún estudiante con ese ID.")
            else:
                st.error(f"Error al buscar en la API: {response.status_code} - {response.text}")

        except requests.exceptions.RequestException as e:
            st.error(f"🔌 Error de conexión: {e}")

    if 'student_found' in st.session_state:
        student = st.session_state['student_found']
        st.success(f"Estudiante encontrado: **{student['nombres']} {student['apellidos']}** (ID: {student['id']})")

        # Formulario de Edición
        with st.expander("📝 Editar Datos", expanded=True):
            with st.form("edit_form"):
                e_codigo = st.text_input("Código", value=student['codigo'])
                e_nombres = st.text_input("Nombres", value=student['nombres'])
                e_apellidos = st.text_input("Apellidos", value=student['apellidos'])
                e_email = st.text_input("Email", value=student['email'])
                e_semestre = st.number_input("Semestre", 1, 12, value=student['semestre'])

                if st.form_submit_button("Guardar Cambios", type="primary"):
                    payload = {
                        "codigo": e_codigo,
                        "nombres": e_nombres,
                        "apellidos": e_apellidos,
                        "email": e_email,
                        "semestre": e_semestre
                    }
                    res_put = requests.put(f"{API_URL}/estudiantes/{student['id']}", json=payload)
                    if res_put.status_code == 200:
                        st.success("💾 Datos actualizados correctamente.")
                        # Limpiamos el estado para ocultar el formulario
                        del st.session_state['student_found']
                        time.sleep(2)
                        st.rerun()
                    else:
                        st.error(f"Error al actualizar: {res_put.text}")

        st.divider()

        # Sección de Borrado
        st.subheader("Zona de Peligro")
        col_del, col_void = st.columns([1, 4])
        with col_del:
            if st.button("🗑️ Eliminar Estudiante", type="secondary"):
                res_del = requests.delete(f"{API_URL}/estudiantes/{student['id']}")
                if res_del.status_code == 200:
                    st.warning("Estudiante eliminado.")
                    # Limpiamos el estado para ocultar el formulario
                    del st.session_state['student_found']
                    time.sleep(2)
                    st.rerun()
                else:
                    st.error(f"No se pudo eliminar: {res_del.text}")