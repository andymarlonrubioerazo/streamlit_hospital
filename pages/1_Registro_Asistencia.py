import streamlit as st
import datetime
from dateutil.relativedelta import *
import pandas as pd
import numpy as np
from io import BytesIO

####__MIS FUNCIONES
from scripts import funciones as f
from scripts import generador_excel as excel





meses1={"01":"ENERO", "02": "FEBRERO","03":"MARZO",
       "04": "ABRIL", "05":"MAYO", "06":"JUNIO",
       "07": "JULIO", "08": "AGOSTO", "09": "SEPTIEMBRE",
       "10": "OCTUBRE", "11": "NOVIEMBRE","12":"DICIEMBRE"
      }


meses = {
    "ENERO": "01", "FEBRERO": "02",     "MARZO": "03",
    "ABRIL": "04", "MAYO": "05", "JUNIO": "06", "JULIO": "07",
    "AGOSTO": "08", "SEPTIEMBRE": "09", "OCTUBRE": "10", "NOVIEMBRE": "11",
    "DICIEMBRE": "12"
}


today = datetime.datetime.now()

    
st.markdown("# :hospital: :orange[Registro de Asistencia:] :calendar:")
st.sidebar.header("Registro de Asistencia")
st.write("PAGINA 1 DESARROLLO DE APLICACIONES ")
st.write(today.strftime("%d/%B/%Y"))


