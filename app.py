import streamlit as st
import pandas as pd
from api_client import obtener_usuarios_api
from database import crear_tabla, guardar_usuarios, eliminar_datos, consultar_usuarios


st.set_page_config(page_title="API-SQLITE-Claudia Aguilar", page_icon=":guardsman")

crear_tabla()

st.title("API-SQLITE-STREAMLIT")
st.write("Obtener datos de una API y almacenarlos en una BD")

menu=st.sidebar.selectbox(
    "Seleccione una Opcion",
    [
        "Inicio",
        "Consumir API",
        "Ver la base de datos",
        "Buscar los Usuarios",
        "Eliminar los datos"   
    ]
)

if menu == "Inicio":
    st.header("BIENVENIDOS A LA APLICACION")
    st.write("Esta app permite alamcenar datos, consultar, eliminar")
    st.info("Seleccione una opcion del menu lateral para empezar a usar la aplicacion")

elif menu == "Consumir API":
    st.header("Consumir API publica")
    st.write("API Utilizada")
    st.code("https://jsonplaceholder.typicode.com/users")
    
    if st.button("Obtener Usuarios del API"):
        usuarios = obtener_usuarios_api()
        if usuarios:
            guardar_usuarios(usuarios)
            st.success("Usuarios guardados exitosamente")
            st.json(usuarios[0])
        else:
            st.error("No se pudieron obtener los datos del API")

elif menu == "Ver la base de datos":
    st.header("Tabla almacenada en SQLite")
    df = consultar_usuarios()

    if df.empty:
        st.warning("La base de datos está vacía. Primero consuma la API.")
    else:
        st.dataframe(df, use_container_width=True)
        col1, col2, col3 = st.columns(3)
        col1.metric("Total usuarios", len(df))
        col2.metric("Total ciudades", df["ciudad"].nunique())
        col3.metric("Total correos", df["email"].nunique())

elif menu == "Buscar los Usuarios":
    st.header("Buscar usuario en SQLite")

    df = consultar_usuarios()
    if df.empty:
        st.warning("No hay datos guardados.")
    else:
        nombre = st.text_input("Ingrese nombre o usuario a buscar")
        if nombre:
            resultado = df[
                df["nombre"].str.contains(nombre, case=False, na=False) |
                df["usuario"].str.contains(nombre, case=False, na=False)
            ]

            if resultado.empty:
                st.error("No se encontraron coincidencias.")
            else:
                st.success("Resultado encontrado.")
                st.dataframe(resultado, use_container_width=True)

elif menu == "Eliminar los datos":
    st.header("Eliminar registros de SQLite")
    st.warning("Esta acción eliminará todos los datos almacenados.")

    if st.button("Eliminar todos los datos"):
        eliminar_datos()
        st.success("Datos eliminados correctamente.")