import streamlit as st
import pandas as pd
from PIL import Image
import subprocess
import os
import base64
import pickle
def desc_calc():
    bashCommand = "java -Xms2G -Xmx2G -Djava.awt.headless=true -jar ./PaDEL-Descriptor/PaDEL-Descriptor.jar -removesalt -standardizenitro -fingerprints -descriptortypes ./PaDEL-Descriptor/PubchemFingerprinter.xml -dir ./ -file descriptors_output.csv"
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE) # Removed extra indent here
def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="prediction.csv">Download Predictions</a>'
    return href
def build_model(input_data):
  load_model = pickle.load(open('acetylcholinesterase_model.pkl', 'rb'))
  prediction = load_model.predict(input_data) # Removed extra indent here
  st.header('**Prediction output**')
  prediction_output = pd.Series(prediction, name='pIC50')
  molecule_name = pd.Series(load_data[1], name='molecule_name')
  df = pd.concat([molecule_name, prediction_output], axis=1)
  st.write(df)
  st.markdown(filedownload(df), unsafe_allow_html=True)



