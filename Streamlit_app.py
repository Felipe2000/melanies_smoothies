# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title("Customize your smoothie Streamlit App")
st.write(
    """Choose the fruits you want in your custom Smoothie!
    """
)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

name_on_order = st.text_input("Name on Smoothie :")
st.write("the name on the smoothie is : ", name_on_order)

ingredients_list = st.multiselect(
    'Choose up to 5 Ingredients',
    my_dataframe,
    max_selections=5
)

if ingredients_list:
    #st.write(ingredients_list)
    #st.text(ingredients_list)

    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

    st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order,order_filled)
                values ('""" + ingredients_string + """','""" + name_on_order + """',false)"""

    st.write(my_insert_stmt)
    
    # st.write(my_insert_stmt)
    time_to_insert = st.button('submit order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('your smoothie is ordered ' + name_on_order, icon='✔️')
