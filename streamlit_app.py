# Import python packages
import streamlit as st





# Write directly to the app
st.title(":cup_with_straw: Customize your smoothie :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie!")

from snowflake.snowpark.functions import col


my_dataframe = session.table("smoothies.publitry:
    frutas = session.table("smoothies.public.fruit_options").select("FRUIT_NAME").collect()
    st.write("🥭 Frutas disponibles:", frutas)
except Exception as e:
    st.error(f"❌ Error al acceder a la tabla fruit_options: {e}")
c.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    my_dataframe)

if ingredients_list:
    ingredients_string = ''
    
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ''
    
#st.write(ingredientes_string)
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients)
            values ('""" + ingredients_string + """')"""

    #st.write(my_insert_stmt)

    time_to_insert = st.button('submit order')
    if time_to_insert: 
       session.sql(my_insert_stmt).collect() 
       st.success('¡Tu batido está pedido!', icon="✅")

cnx = st.connection("snowflake")
session = cnx.session()

       

    
    


