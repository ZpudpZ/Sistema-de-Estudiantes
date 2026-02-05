import streamlit as st
import os

def load_css():
    css_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'styles.css')
    
    with open(css_path) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def render_header():
    col_logo, col_text = st.columns([1, 6])

    with col_logo:
        st.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSaDNyWHvTBumE9ArQGi6z4hmAfCfN61pJa6WjNWX2MqOFh79937u-v_Rrlzh-MzlheACdDFHqCwvAhLQBYN1BLHcc9YEsZYJBRv07BU4Y&s=10", width=150)

    with col_text:
        st.markdown("""
        <div style='color: #003366;'>
            <h1 style='margin-bottom: 0px;'>UNIVERSIDAD NACIONAL DEL ALTIPLANO</h1>
            <h3 style='margin-top: 0px; font-weight: 300; color: #555;'>Sistema Integrado de Gestión Académica</h3>
        </div>
        <hr style="border: 1px solid #b30000; margin-top: 5px;">
        """, unsafe_allow_html=True)

def section_title(text, icon_url):
    st.markdown(f"""
        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 20px;">
            <img src="{icon_url}" width="35"/>
            <h2 style="margin: 0; color: #003366;">{text}</h2>
        </div>
    """, unsafe_allow_html=True)