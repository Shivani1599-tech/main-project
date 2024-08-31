# -*- coding: utf-8 -*-
"""main

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1xmFVR12HWZ7hgdYWT-Cq0pu7dHr33gw_
"""

!pip install streamlit

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
    output, error = process.communicate()
    os.remove('molecule.smi')

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

from PIL import Image

from PIL import Image
import os

import os

# Get the current working directory
script_dir = os.getcwd()

print("Current directory:", script_dir)

# Install the ipynbname package
!pip install ipynbname

import os
import ipynbname

# Get the full path of the notebook
notebook_path = ipynbname.path()
script_dir = os.path.dirname(notebook_path)

print("Notebook directory:", script_dir)

script_dir = os.path.dirname(os.path.abspath(os.getcwd()))
image_path = os.path.join(script_dir, 'logo.png')

image = Image.open('logo.png')

st.image(image, use_column_width=True)

st.markdown("""
# Bioactivity Prediction App (Acetylcholinesterase)

This app allows you to predict the bioactivity towards inhibting the `Acetylcholinesterase` enzyme. `Acetylcholinesterase` is a drug target for Alzheimer's disease.

**Credits**
- App built in `Python` + `Streamlit` by [Chanin Nantasenamat](https://medium.com/@chanin.nantasenamat) (aka [Data Professor](http://youtube.com/dataprofessor))
- Descriptor calculated using [PaDEL-Descriptor](http://www.yapcwsoft.com/dd/padeldescriptor/) [[Read the Paper]](https://doi.org/10.1002/jcc.21707).
---
""")

# Sidebar
with st.sidebar.header('1. Upload your CSV data'):
    uploaded_file = st.sidebar.file_uploader("Upload your input file", type=['txt'])
    st.sidebar.markdown("""
[Example input file](https://raw.githubusercontent.com/dataprofessor/bioactivity-prediction-app/main/example_acetylcholinesterase.txt)
""")

if st.sidebar.button('Predict'):
    load_data = pd.read_table(uploaded_file, sep=' ', header=None)
    load_data.to_csv('molecule.smi', sep = '\t', header = False, index = False)

    st.header('**Original input data**')
    st.write(load_data)

    with st.spinner("Calculating descriptors..."):
        desc_calc()

    # Read in calculated descriptors and display the dataframe
    st.header('**Calculated molecular descriptors**')
    desc = pd.read_csv('descriptors_output.csv')
    st.write(desc)
    st.write(desc.shape)

    # Read descriptor list used in previously built model
    st.header('**Subset of descriptors from previously built models**')
    Xlist = list(pd.read_csv('descriptor_list.csv').columns)
    desc_subset = desc[Xlist]
    st.write(desc_subset)
    st.write(desc_subset.shape)

    # Apply trained model to make prediction on query compounds
    build_model(desc_subset)
else:
    st.info('Upload input data in the sidebar to start!')

"""Connect CMD to Colab

"""