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
        st.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSaDNyWHvTBumE9ArQGi6z4hmAfCfN61pJa6WjNWX2MqOFh79937u-v_Rrlzh-MzlheACdDFHqCwvAhLQBYN1BLHcc9YEsZYJBRv07BU4Y&s=10", width=150)

    with col_text:
        st.markdown("""
        <div style='color: #003366; font-family: sans-serif;'>
            <h1 style='margin-bottom: 0px; font-size: 2rem;'>UNIVERSIDAD NACIONAL DEL ALTIPLANO</h1>
            <h3 style='margin-top: 5px; font-weight: 400; color: #555;'>Sistema OTI - Versión Automática</h3>
        </div>
        <hr style="border: 1px solid #800000; margin-top: 10px;">
        """, unsafe_allow_html=True)

def section_title(text, icon_url):
    st.markdown(f"""
        <div style="display: flex; align-items: center; gap: 15px; margin-bottom: 25px; padding-top: 10px;">
            <img src="{icon_url}" width="32"/>
            <h2 style="margin: 0; color: #003366; font-size: 1.5rem;">{text}</h2>
        </div>
    """, unsafe_allow_html=True)