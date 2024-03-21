#importacion de librerias
import streamlit as st
import pandas as pd
import numpy as np
import random
from PIL import Image
#para el modelo
from sklearn.metrics.pairwise import cosine_similarity


#carga de dataframe
businessry = pd.read_csv('review.csv')
df_prueba = businessry.drop_duplicates(subset=['business_id'])

businessy = pd.read_csv('business_full.csv')
df = pd.read_csv('df.csv')
users = pd.read_csv('users.csv')

#carga modelos
df_modelo_entrenamiento = df[[ 'cat_elite',	'cat_limpieza',	'cat_ambiente',	'cat_promociones',	'cat_extra',	'cat_interaccion']]

cosine_sim = cosine_similarity(df_modelo_entrenamiento, df_modelo_entrenamiento)

st.markdown("### Instrucciones de uso:\n\n")
st.write("Ingrese un correo válido")
st.write("En caso de no estar en nuestra base de datos, se le dará una recomendación")
st.write("Ejemplos de correos : jodi90@gmail.com, katie202@gmail.com, maria115@gmail.com")
st.write(" ")
st.write("  ")
st.write("   ")
st.write("   ")
st.write("   ")

def app():

        # Load the image and display it
    col1, col2, col3 = st.columns(3)

    with col1:
     st.image("publicidad.png",width=200)

    with col2:
     st.image("nails1c.png",width=240)

    with col3:
     st.write("")
  

    #st.markdown("<h2 style='text-align: center;'> Podrás encontrar los negocios de uñas que más se adapten a tus preferencias.</h2>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center;'> Nails Recommender 1.0</h2>", unsafe_allow_html=True)


    correo = st.text_input("Coloca tu email, para darte una recomendación", key="query_input")
    boton = st.button("Generar Recomendación")
    if boton:
       if correo.find("@") == -1 or correo.find(".com") == -1 or correo.find(" ") != -1:
          st.write("Coloque un correo válido.")
       else:
          #Correo-busines_id
          #correo='diane1312@gmail.com'
          correo = correo.lower()
          

          businessry_ord=businessry.sort_values(by='review_stars', ascending=False)
          businessry_ord_unic=businessry.drop_duplicates(subset=['business_id'])

          try:
            usuario = users[users['correo']==correo].iloc[0][0]
          except IndexError:
             business_id_recomendado = businessry_ord_unic.iloc[0][1]  


          try:
             df_usuario = businessry_ord[businessry_ord['user_id']==usuario].sort_values(by='review_stars', ascending=False)
          except:
            st.write('No estas en nuestra base de datos, te daremos una recomendación de igual forma.')
            pass   
          
          n = random.randint(0, 100)

          try:
            business_id_recomendado = df_usuario.iloc[0][1]
          except:
             business_id_recomendado = businessry_ord_unic.iloc[n][1]

         
          idx = df[df['business_id'] == business_id_recomendado].index[0]
          sim_scores = list(enumerate(cosine_sim[idx]))
          sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
          sim_scores = sim_scores[2:7]
          business_indices = [i[0] for i in sim_scores]
          lista_business_id=[]
          for i,k in enumerate(business_indices):
                  lista_business_id.append(df.iloc[k][0])
          


          lista_nombre=[]; lista_direccion=[]
 
      
#           #Revisar bien al usar el codigo final, porque los diccionarios no guardan orden
          for i,k in enumerate(lista_business_id):
              if lista_business_id[i] != business_id_recomendado:

                    lista_nombre.append( businessy[businessy['business_id']==lista_business_id[i]].iloc[0][1]) 
                    lista_direccion.append(businessy[businessy['business_id']==lista_business_id[i]].iloc[0][2])  
             
    
          df_print =pd.DataFrame({'Nombre Local':lista_nombre,'Dirección':lista_direccion})
          df_print.index = [index + 1 for index in df_print.index]
          st.table(df_print)
    



    st.markdown("<p style='text-align: center;'> Construido con ❤ por: <a href='https://github.com/jrguignan'> jrguignan </a> | 2024 © Beauty Consulting </p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)

    with col1:
     st.write("")

    with col2:
     st.image("beautyc.png",width=240)

    with col3:
     st.write("")
    

if __name__ == '__main__':
    app()    