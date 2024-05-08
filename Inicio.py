import streamlit as st

st.set_page_config(
    page_title="Hello",
    page_icon="💻"
)


st.write("# Bienvenido al sistema 👋")

st.sidebar.success("Seleccione una opción de arriba")

st.markdown("""
            
    CARATULA DE BIENVENIDA

            """ 
            )


# Show different content based on the user's email address.
