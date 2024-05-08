import streamlit as st
import datetime
from dateutil.relativedelta import *
import pandas as pd
import numpy as np
from io import BytesIO
from fpdf import FPDF

####__MIS FUNCIONES
####__MIS FUNCIONES
from scripts import funciones as f
from scripts import generador_excel as excel
from scripts import generador_pdf as pdf

st.markdown("# :hospital: :orange[Lectura de los Dosímetros] :desktop_computer:")
st.sidebar.header("Lectura de Dosímetros en Winrem")


st.markdown("#### Subir el Historial de LECTURAS de la unidad/institución"
                                  ":green_book:")

archivo_excel2 = st.file_uploader("",
                                 type=['xlsx',"xls"],key="dosis")

if archivo_excel2 is not None:

    df2, sheet2=f.lectura_dosis(archivo_excel2)
    name2 = list(df2.columns)
    name2=[ k for k in name2 if k.startswith("LECTURA")]

    st.write(df2)


    fecha_canje2=st.selectbox("Seleccione el período de LECTURA de los dosímetros:",
                name2,
                key="fecha_canje2"
                )

    st.markdown("#### Subir el Historial de los Dosímetros:green_book:")
    archivo_excel3 = st.file_uploader(''
                                    ,type=['xlsx',"xls"],key="dosimetros")

    if archivo_excel3 is not None:

        df3,_=f.lectura_dosimetros(archivo_excel3)
        st.write(df3)

        st.markdown("#### Subir el archivo WINREM .asc del equipo 💻:")
        archivo_asc=st.file_uploader("", 
                                     type=["asc"], key="asc")

        if archivo_asc: 
            df1=f.lectura_asc(archivo_asc)
            st.write(df1)
            

            df2=f.procesar_archivos(df1,df2,df3,fecha_canje2 )
            st.write(df2)

            n_reporte=st.text_input("N° de Reporte",placeholder="00000")
            title_hospital="ibarra"
            hospital_completo= "HOSPITAL DEL NORTE LOS CEIBOS GUAYAQUIL"
            RUC="0960245668855"
            f1,f2=f.fechas_seleccion()

            col1, col2=st.columns(2)

            with col1:
                file_pdf=pdf.df_to_pdf(df2,fecha_canje2, n_reporte,title_hospital,
                                        hospital_completo,RUC,f1,f2)
                file_pdf.output('borrador.pdf')

                with open("borrador.pdf", "rb") as f:
                    st.download_button(f"Descargar reporte Pdf {sheet2}", f, 
                                       f"{title_hospital}_{n_reporte}.pdf")

            with col2:
                wb =excel.excel_reporte_lectura_dosis(df2)
                excel_file = excel.descargar_excel(wb)
                st.download_button(
                    label=f"Descargar reporte de lectura de dosis {sheet2} en Excel",
                    data=excel_file,
                    file_name=f"HISTORIAL_DE_DOSIS_{sheet2}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )