import pandas as pd
import time
from datetime import datetime
import tkinter as tk
from tkinter import filedialog, messagebox
import streamlit as st
import numpy as np
from datetime import datetime, timedelta


meses={"01":"ENERO", "02": "FEBRERO","03":"MARZO",
       "04": "ABRIL", "05":"MAYO", "06":"JUNIO",
       "07": "JULIO", "08": "AGOSTO", "09": "SEPTIEMBRE",
       "10": "OCTUBRE", "11": "NOVIEMBRE","12":"DICIEMBRE"
      }

def input_dosimetros(df3,fecha,df,new_column): 
    if "my_dosimetro" not in st.session_state: # "my_dosimetro almaceno la variable en el sistema"
        st.session_state.my_dosimetro = ""
        st.session_state.text1 = ""
        
    if "df" in st.session_state: 
        df=st.session_state.df

    def submit():
        st.session_state.my_dosimetro = st.session_state.w1
        st.session_state.w1 = ""

    st.text_input("Ingrese el código del dosímetro:", key="w1", on_change=submit) #identifico el widget con el nombre "w1" de la key

    text0 = st.session_state.my_dosimetro
    
    for k3 in df3.index.to_list():
        if text0==df3.loc[k3, fecha]:
            text0=df3.loc[k3, [fecha,"CEDULA", "NOMBRES Y APELLIDOS"]]
            st.write(text0)

            for k in df.index.to_list():
                if text0["CEDULA"]==df.loc[k, "CEDULA"]:
                    df.loc[k, new_column]="X"
                    st.session_state.df=df
                    break
            break

    text1=st.session_state.text1    
    st.write(text1)
    st.session_state.text1=text0

    idx=list(df.index)[:-1]
    xn=df.loc[idx,new_column].count()
    st.write(f"Canjeados: {xn}") 

    return df

def registro_asistencia(archivo_excel):
    df=pd.ExcelFile(archivo_excel)
    sheet_names = list(df.sheet_names)

    sheet=st.selectbox("Selecciona la unidad o institución",
                    sheet_names,
                    key="sheet_names"
                    )
    df=pd.read_excel(archivo_excel,sheet_name=sheet,dtype=str)
    title=df.columns[0]
    title
    
    name=df.loc[2].to_list()
    df.columns=name

    df=df.loc[3:].reset_index(drop=True)

    today = datetime.now()
    mes=today.strftime("%m")
    new_column=f"CANJE {meses[mes]} {today.year}"
    df[new_column]=np.NaN

    return df, title, new_column

def historial_asistencia(archivo_excel):
    df=pd.ExcelFile(archivo_excel)
    sheet_names = list(df.sheet_names)

    sheet=st.selectbox("Selecciona la unidad o institución",
                    sheet_names,
                    key="sheet_names"
                    )
    df=pd.read_excel(archivo_excel,sheet_name=sheet,dtype=str)
    title=df.columns[0]
    title
    
    name=df.loc[2].to_list()
    df.columns=name

    df=df.loc[3:].reset_index(drop=True)

    today = datetime.now()
    mes=today.strftime("%m")
    new_column=f"CANJE {meses[mes]} {today.year}"
    df[new_column]=np.NaN

    return df, title, new_column



def redefino_unit(df1):
    for k in range(len(df1[28])):
        if df1.loc[k,28]=='uSv': 
            df1.loc[k,28]='mSv' 
            df1.loc[k,21]=df1.loc[k,21]/1000
            df1.loc[k,24]=df1.loc[k,24]/1000
    return df1

def lectura_asc(archivo_asc): ###LECTURA DE LOS DOSIMETROS EN WINREMS 
    ######______LECTURA DE LOS ARCHIVOS .ASC DE LA MAQUINA
    df1 = pd.read_csv(archivo_asc, header=None) ###LEO EL DOCUMENTO
    
    df1=df1.drop (df1.columns[0:11], axis='columns' ) ###ELIMINO LAS PRIMERAS 10 COLUMNAS, PARECE QUE NO HACE NADA
    df1=df1.drop (df1[[14,15]], axis='columns' ) ###ELIMINO LA COLUMNA 14 Y 15, PARECE QUE NO HACE NADA
    
    # df1=df1.loc[4:]  ### ELIMINO LAS CUATRO PRIMERAS FILAS  QUE CORRESPONDE A LA VERFICICACIÓN DEL EQUIPO
    df1[28]=df1[28].apply(lambda x: x.replace('"',""))
    df1[28]=df1[28].apply(lambda x: x.replace(' ',""))
    
    df1=df1.drop(df1[df1[28]=="nC"].index) ###Elimino las filas que tenga "nC" porque corresponde a medicion del equipo
   
    df1=df1.reset_index(drop=True)
    
    df1=redefino_unit(df1)
    
    i_iv=[16,17,18,25,26,27]
    for col in  i_iv:
        for j in df1[col].unique(): 
            if j!=0: print("ALERTA EN LA COLUMNA I ó IV hay valores que no deberían estar") 
    
    df1=df1.drop (df1[i_iv], axis='columns' ) ###ELIMINO LAS COLUMNA DE I Y IV DESPUES DE VERIFICAR QUE 
                                                ### NO EXISTAN PROBLEMAS
    df1=df1[[11,12,13,21,20,19,24,23,22,28]] ### ORDENO LOS VALROES DE II Y III DE ORDEN DESCENDENTE A IZQUIERDA A DERECHA
    
    name=["fecha", "hora","Dosimeter_ID",
          "TLD_0.007","ECC_II","RCF_II",
          "TLD_0.10","ECC_III","RCF_III",
          "units"]
    df1.columns=name ###DEFINO EL NOMBRE DE CADA COLUMNA 
    df1["Dosimeter_ID"]="00"+df1["Dosimeter_ID"].astype(str)
    df1["fecha"]=df1["fecha"].astype(str)

    return df1

def lectura_dosis(archivo_excel):  ####LECTURA DEL HISTORIAL DE DOSIS DE LOS PACIENTES 

     ######_____LECTURA DEL ARCHIVO EXCEL DE LAS PERSONAS 
    df2=pd.ExcelFile(archivo_excel)
    sheet_names2 = list(df2.sheet_names)
    sheet2=st.selectbox("Selecciona el AÑO de trabajo",
                    sheet_names2,
                    key="sheet_names2"
                    )
    df2=pd.read_excel(archivo_excel,sheet_name=sheet2,dtype=str)
    name=df2.loc[2]

    name2=[]
    for k in name:
        words=k.split()
        sentences=""
        for k1 in words:
            sentences=sentences+k1+" "
        sentences=sentences[:-1]
        name2.append(sentences)
    
        
    df2=df2.loc[3:]
    df2.columns=name2
    df2=df2.dropna(subset=["UNIDAD U HOSPITAL","CEDULA","NOMBRES Y APELLIDOS"])
    df2=df2.reset_index(drop=True)

     
    return df2, sheet2

def lectura_dosimetros(archivo_excel_dosimetro): ######_____LECTURA DEL HISTORIAL DE LOS DOSIMETROS DE LAS PERSONAS 
   
    df3=pd.ExcelFile(archivo_excel_dosimetro)
    sheet_names3 = list(df3.sheet_names)
    sheet3=st.selectbox("Seleccione el AÑO de trabajo",
                sheet_names3,
                key="sheet3"
                )


    df3=pd.read_excel(archivo_excel_dosimetro,sheet_name=sheet3,dtype=str)
    name=list(df3.loc[2])

    name3=[]
    for k in name:
        words=k.split()
        sentences=" ".join(words)            
        name3.append(sentences)

    df3=df3.loc[3:]
    df3.columns=name3
    df3=df3.dropna(subset=["UNIDAD U HOSPITAL","CEDULA","NOMBRES Y APELLIDOS"])
    df3=df3.reset_index(drop=True)

    return df3,sheet3


def procesar_archivos(df1,df2,df3,fecha_canje2 ):

    name3 = list(df3.columns)
    
    fecha2=fecha_canje2.split()
    fecha2[0]="DOSIMETRO"
    dosim_usado=" ".join(fecha2) 

    column_lecturas = df2.columns[df2.columns.str.contains("LECTURA") ].to_list()
    column_dosis=df2.columns[df2.columns.str.contains("TOTAL") ].to_list()
    for k in column_lecturas: 
            df2[k]= df2[k].astype(float)
    ###########   FIN EXTRACCION DE INFORMACION
    
    
    for k1 in df1["Dosimeter_ID"].index:
        for k3 in df3[dosim_usado].index:

            if df1.loc[k1,"Dosimeter_ID"]==df3.loc[k3,dosim_usado]: 
                
                for k2 in df2["CEDULA"].index:
                    if df3.loc[k3,"CEDULA"]==df2.loc[k2,"CEDULA"]:
                        df2.loc[k2,fecha_canje2]=df1.loc[k1,"TLD_0.007"].round(3)
                        df2.loc[k2,"CODIGO DE DOSIMETRO"]=df3.loc[k3,dosim_usado]
                        break 
                break 
                
    for k1 in range(len(df2)):
        dosis=0.0
        for k in column_lecturas: 
            if df2.loc[k1,k]>=0.100: dosis+=df2.loc[k1,k] 
        df2.loc[k1,column_dosis]=dosis 
    return df2

def fechas_seleccion():
    today=datetime.now()
    fi=today-timedelta(days=2*30)
    ff=today#+timedelta(days=4*30)

    d=st.date_input(
        "Selecciona las fechas exactas de las lecturas",
        (fi,ff),
        format="DD/MM/YYYY"
    )


    try:
        f1,f2=d[0].strftime('%d/%m/%Y'),d[1].strftime('%d/%m/%Y')
        x1=f"{d[0].strftime("%d")}/{meses[d[0].strftime("%m")]}/{d[0].strftime("%Y")}"
        x2=f"{d[1].strftime("%d")}/{meses[d[1].strftime("%m")]}/{d[1].strftime("%Y")}"
        
    except:
        f1=fi
        f2=ff
        x1=""
        x2=""

    st.write(x1,x2)
    return f1,f2        
   
    

