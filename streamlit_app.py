import altair as alt
import numpy as np
import pandas as pd
import streamlit as st
from io import StringIO
import xml.etree.ElementTree as et

"""
# Welcome to Streamlit!

Edit `/streamlit_app.py` to customize this app to your heart's desire :heart:.
If you have any questions, checkout our [documentation](https://docs.streamlit.io) and [community
forums](https://discuss.streamlit.io).

In the meantime, below is an example of what you can do with just a few lines of code:
"""





uploaded_file=st.file_uploader("Upload a .twb.", disabled=False, label_visibility="visible")
if uploaded_file is not None:
    stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
    string_data = stringio.read()
    tree=et.parse(string_data)
    root=tree.getroot()
    st.write(string_data)
