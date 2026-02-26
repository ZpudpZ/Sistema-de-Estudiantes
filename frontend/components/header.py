import streamlit as st
import os

def load_css():
    css_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'styles.css')
    if os.path.exists(css_path):
        with open(css_path) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def render_header():
    col_logo, col_text = st.columns([1, 6])
    with col_logo:
        st.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSaDNyWHvTBumE9ArQGi6z4hmAfCfN61pJa6WjNWX2MqOFh79937u-v_Rrlzh-MzlheACdDFHqCwvAhLQBYN1BLHcc9YEsZYJBRv07BU4Y&s=10", width=130)

    with col_text:
        st.markdown("""
        <div style='color: #002d57; font-family: "Segoe UI", Tahoma, sans-serif;'>
            <h1 style='margin-bottom: 0px; font-size: 1.9rem; font-weight: 700;'>UNIVERSIDAD NACIONAL DEL ALTIPLANO</h1>
            <h3 style='margin-top: 5px; font-weight: 300; color: #444; letter-spacing: 0.5px;'>Oficina de Tecnologías de la Información (OTI)</h3>
        </div>
        <hr style="border: 0; height: 2px; background-image: linear-gradient(to right, #800000, #002d57, transparent); margin-top: 10px;">
        """, unsafe_allow_html=True)

def section_title(text, icon_url):
    st.markdown(f"""
        <div style="display: flex; align-items: center; gap: 15px; margin-bottom: 25px; padding-top: 10px; border-bottom: 1px solid #f0f2f6;">
            <img src="{icon_url}" width="28" style="filter: brightness(0.5);"/>
            <h2 style="margin: 0; color: #002d57; font-size: 1.4rem; font-weight: 600;">{text}</h2>
        </div>
    """, unsafe_allow_html=True)