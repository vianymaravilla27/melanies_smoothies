import streamlit as st
# from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import requests
import pandas as pd
cnx = st.connection("snowflake", type="snowflake")
session = cnx.session()

# Título e instrucciones
st.title("🥤 Customize Your Smoothie!")
st.write("Choose the fruits you want in your custom Smoothie!")

# Campo para ingresar el "nombre" del smoothie
name_on_order = st.text_input("Name on Smoothie:")
st.write(f"The name on your Smoothie will be: {name_on_order}")

# Conexión a Snowpark (dentro de Snowflake Native App/Streamlit)
# session = get_active_session()

# Consulta la tabla 'fruit_options' para obtener la lista de FRUIT_NAME
# y conviértela en una lista de strings (indispensable para el multiselect)
fruit_rows = session.table("smoothies.public.fruit_options") \
                    .select(col('FRUIT_NAME')) \
                    .collect()
fruit_list = [row['FRUIT_NAME'] for row in fruit_rows]

# Muestra un multiselect con la lista de frutas
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    fruit_list  # Aquí le pasamos la lista nativa de strings
    , max_selections = 5
)

# Botón para enviar el pedido
if st.button("Submit Order"):
    if not name_on_order:
        st.warning("Please enter a name for your Smoothie!")
    elif not ingredients_list:
        st.warning("Please select at least one ingredient.")
    else:
        # Construye un string con los ingredientes
        ingredients_string = ", ".join(ingredients_list)

        # Prepara la sentencia INSERT (ajusta si tus columnas difieren)
        insert_stmt = f"""
            INSERT INTO smoothies.public.orders(INGREDIENTS, NAME_ON_ORDER)
            VALUES ('{ingredients_string}', '{name_on_order}')
        """

        # Ejecuta el INSERT
        session.sql(insert_stmt).collect()

        # Muestra el mensaje de éxito
        st.success("Your Smoothie is ordered!", icon="✅")


my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
#st.dataframe(data=my_dataframe, use_container_width = True)
#st.stop

pd_df=my_dataframe.to_pandas()
st.dataframe(pd_df)
st.stop()

ingredients_list = st.multiselect(
  'Choose up to 5 ingredients:'
  , my_dataframe
  , max_selections = 5
)

if ingredients_list:
  ingredients_string = ''

  for fruit_chosen in ingredients_list:
    ingredients_string += fruit_chosen + ' '

    search_on = pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
    #st.write('The search value for', fruit_chosen, 'is', search_on,'.')
    st.subheader(fruit_chosen + 'Nutrition Information')
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + search_on)
    fv_df = st.dataframe(data=fruityvice_response.json(),use_container_width = True)




