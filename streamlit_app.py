import streamlit as st

# Conexión segura desde secrets.toml
cnx = st.connection("snowflake", type="snowflake")
session = cnx.session()

# Test 1: ¿Conexión funciona?
st.write("✅ Conectado a Snowflake.")

# Test 2: ¿Podemos hacer una consulta básica?
try:
    result = session.sql("SELECT CURRENT_USER(), CURRENT_ROLE(), CURRENT_DATABASE(), CURRENT_SCHEMA()").collect()
    st.write("🔎 Sesión activa:", result)
except Exception as e:
    st.error(f"❌ Error al consultar Snowflake: {e}")
try:
    frutas = session.table("smoothies.public.fruit_options").select("FRUIT_NAME").collect()
    st.write("🥭 Frutas disponibles:", frutas)
except Exception as e:
    st.error(f"❌ Error al acceder a la tabla fruit_options: {e}")
