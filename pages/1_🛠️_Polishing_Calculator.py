import streamlit as st
import math
from datetime import datetime

from packages.email_sender import EmailSender as emsender
from pretty_html_table import build_table


import pandas as pd

st.set_page_config(
    page_title="佑能科技-拋光計算機",
    page_icon="🌟",
)


def gen_email_content(df):
    table = build_table(df, 'grey_light')
    email_content = """
    您的拋光計算結果如下:
    """ + table + """
    """
    return email_content

if "results_table" not in st.session_state:
    st.session_state.results_table = pd.DataFrame( columns=['拋光前重量 (g)', '拋光後重量 (g)','晶圓厚度 (μm)'])
    
if "wafer_before" not in st.session_state:
    st.session_state.wafer_before = 0.0
    
if "wafer_after" not in st.session_state:
    st.session_state.wafer_after = 0.0
    
def calculate_wafer_thickness(weight_before, weight_after, wafer_diameter):
    density = 2330000  # g/m^3
    weight_difference = weight_before - weight_after
    wafer_thickness = weight_difference / (density * math.pi * (wafer_diameter ** 2)) *1000000
    return wafer_thickness

st.title("拋光計算機")


weight_before = st.number_input("拋光前重量 (g)",key="weight_before", step=0.01)
weight_after = st.number_input("拋光後重量 (g)",key="weight_after", step=0.01)
wafer_diameter = st.selectbox("選擇晶圓尺寸", ["6 英吋", "8 英吋", "12 英吋"])

def submit():
    st.session_state.wafer_before = st.session_state.weight_before
    st.session_state.weight_before = 0.0
    st.session_state.wafer_after = st.session_state.weight_after
    st.session_state.weight_after = 0.0
    
    
df = st.session_state.results_table
if st.button("計算", on_click=submit,type="primary"):
    before = st.session_state.wafer_before
    after = st.session_state.wafer_after
    
    if before < after:
        st.error("拋光前重量不可比拋光後重量大")
        st.stop()
        
    if before and after:
        wafer_diameter_inch = float(wafer_diameter.split()[0]) / 2
        wafer_diameter_mm = wafer_diameter_inch * 25.4 / 1000
        result = calculate_wafer_thickness(before, after, wafer_diameter_mm)
        st.success(f"晶圓厚度: {result:.6f} μm")
        df.loc[len(df)] = [before, after, result]
        
    else:
        st.error("請輸入拋光前後的重量")

col1, col2 = st.columns(2)

with col1:
    st.dataframe(df,hide_index=True)
    if st.button("清除"):
        df = pd.DataFrame( columns=['拋光前重量 (g)', '拋光後重量 (g)','晶圓厚度 (μm)'])
        st.session_state.results_table = df
        st.experimental_rerun()

with col2:
    email = st.text_input("郵件地址", placeholder="email")
    if st.button("發送結果"):
        date_str = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        
        email = emsender("佑能拋光測試結果, 日期:" + date_str, 
                            email)
        email.send(gen_email_content(df))


st.session_state.results_table = df