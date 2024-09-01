# Required libraries
import streamlit as st
import pandas as pd
from PIL import Image
import subprocess
import os
import base64
import pickle

# Function to calculate molecular descriptors using PaDEL-Descriptor
def desc_calc():
    # Command to run PaDEL-Descriptor for calculating molecular descriptors
    bashCommand = "java -Xms2G -Xmx2G -Djava.awt.headless=true -jar ./PaDEL-Descriptor/PaDEL-Descriptor.jar -removesalt -standardizenitro -fingerprints -descriptortypes ./PaDEL-Descriptor/PubchemFingerprinter.xml -dir ./ -file descriptors_output.csv"
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    os.remove('molecule.smi')

# Function to download the results as a CSV file
def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="prediction.csv">Download Predictions</a>'
    return href

# Function to build the model and make predictions
def build_model(input_data):
    # Load the pre-trained model
    load_model = pickle.load(open('acetylcholinesterase_model.pkl', 'rb'))
    # Make predictions
    prediction = load_model.predict(input_data)
    st.header('**Prediction output**')
    # Create a DataFrame for predictions
    prediction_output = pd.Series(prediction, name='pIC50')
    molecule_name = pd.Series(load_data[1], name='molecule_name')
    df = pd.concat([molecule_name, prediction_output], axis=1)
    st.write(df)
    st.markdown(filedownload(df), unsafe_allow_html=True)

# Main Streamlit app
st.markdown("""
# Bioactivity Prediction App (Acetylcholinesterase)

This app allows you to predict the bioactivity towards inhibiting the `Acetylcholinesterase` enzyme. `Acetylcholinesterase` is a drug target for Alzheimer's disease.

**Credits**
- App built in `Python` + `Streamlit` by [Chanin Nantasenamat](https://medium.com/@chanin.nantasenamat) (aka [Data Professor](http://youtube.com/dataprofessor))
- Descriptor calculated using [PaDEL-Descriptor](http://www.yapcwsoft.com/dd/padeldescriptor/) [[Read the Paper]](https://doi.org/10.1002/jcc.21707).
---
""")

# Display logo image (if available)
script_dir = os.path.dirname(os.path.abspath(os.getcwd()))
image_path = os.path.join(script_dir, 'logo.png')
if os.path.exists(image_path):
    image = Image.open(image_path)
    st.image(image, use_column_width=True)

# Sidebar for file upload
with st.sidebar.header('1. Upload your CSV data'):
    uploaded_file = st.sidebar.file_uploader("Upload your input file", type=['txt'])
    st.sidebar.markdown("""
[Example input file](https://raw.githubusercontent.com/dataprofessor/bioactivity-prediction-app/main/example_acetylcholinesterase.txt)
""")

# If Predict button is clicked
if st.sidebar.button('Predict'):
    if uploaded_file is not None:
        # Load the input data from the uploaded file
        load_data = pd.read_table(uploaded_file, sep=' ', header=None)
        load_data.to_csv('molecule.smi', sep='\t', header=False, index=False)

        st.header('**Original input data**')
        st.write(load_data)

        # Calculating descriptors
        with st.spinner("Calculating descriptors..."):
            desc_calc()

        # Display calculated descriptors
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
        st.error('Please upload a valid input file!')
else:
    st.info('Upload input data in the sidebar to start!')
