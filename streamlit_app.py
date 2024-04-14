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
    root=et.fromstring(string_data)
    #flow for worksheets

    datname=''
    calc=''
    caption=''
    columnData=pd.DataFrame(columns=['column','calculation','caption'])
    for a in root:
        for b in a:
            for c in b:
                if c.tag=='column':
                    try:
                        caption=c.attrib['caption']
                    except:
                        caption=''
                    datname=c.attrib['name']
                    for d in c:
                        if d.tag=='calculation':
                            try:
                                calc=d.attrib['formula']
                            except:
                                calc=''
                if datname!='':
                    #datarow=pd.DataFrame(data={'column': [datname], 'calcluation': [calc]})
                    new_index = len(columnData)
                    columnData.loc[new_index] = {'column': datname, 'calculation': calc,'caption':caption}
                    datname=''
                    calc=''
    
    
    #flow for worksheets
    
    sheetname=''
    dataname=''
    worksheetData=pd.DataFrame(columns=['worksheet','column'])
    for a in root:
        for b in a:
            for c in b:
                for d in c:
                    for e in d:
                        for f in e:
                            if b.tag=='worksheet':
                                sheetname=b.attrib['name']
                            if e.tag=='datasource-dependencies' and f.tag=='column':
                                dataname=f.attrib['name']
                            if sheetname!='' and dataname!='':
                                new_index = len(worksheetData)
                                worksheetData.loc[new_index] = {'worksheet': sheetname, 'column': dataname}
                            sheetname=''
                            dataname=''
    
    
    
    #flow for dashboards
    dashboard=''
    worksheet=''
    dashData=pd.DataFrame(columns=['dashboard','worksheet'])
    for a in root:
        for b in a:
            for c in b:
                for d in c:
                    if b.tag=='window' and b.attrib['class']=='dashboard' and d.tag=='viewpoint':
                        dashboard=b.attrib['name']
                        worksheet=d.attrib['name']
                        new_index = len(dashData)
                        dashData.loc[new_index] = {'dashboard': dashboard, 'worksheet': worksheet}
                        dashboard=''
                        worksheet=''
    
    datasource=columnData.merge(worksheetData,on='column',how='left')
    datasource=datasource.merge(dashData, on='worksheet',how='left')
    #st.write(datasource)

    data = datasource['column'].unique().tolist()
    worksheets = datasource['worksheet'].unique().tolist()
    dashboards = datasource['dashboard'].unique().tolist()
    st.sidebar.multiselect('Data',data)
    st.sidebar.multiselect('Worksheets',worksheets)
    st.sidebar.multiselect('Dashboards',dashboards)
