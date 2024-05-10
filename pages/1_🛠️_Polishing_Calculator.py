from pyparsing import col
import streamlit as st
import math
import datetime as dt

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

data_cols = ['拋光前重量 (g)', '拋光後重量 (g)','花費時間 (min)','晶圓厚度 (μm)','移除率 (um/min)']

if "results_table" not in st.session_state:
    st.session_state.results_table = pd.DataFrame( columns=data_cols)
    
if "buff_weight_before" not in st.session_state:
    st.session_state.buff_weight_before = None
    
if "buff_weight_after" not in st.session_state:
    st.session_state.buff_weight_after = None
    
if "buf_polished_min" not in st.session_state:
    st.session_state.buf_polished_min = 0
    
if "buf_polished_sec" not in st.session_state:
    st.session_state.buf_polished_sec = 0
    
def calculate_wafer_thickness(input_weight_before, input_weight_after, wafer_diameter):
    density = 2330000  # g/m^3
    weight_difference = input_weight_before - input_weight_after
    wafer_thickness = weight_difference / (density * math.pi * (wafer_diameter ** 2)) *1000000
    return wafer_thickness

st.title("拋光計算機")

st.number_input("拋光前重量 (g)",key="input_weight_before", step=0.001,value=None, placeholder="請輸入拋光前重量")
st.number_input("拋光後重量 (g)",key="input_weight_after", step=0.001,value=None, placeholder="請輸入拋光後重量")
wafer_diameter = st.selectbox("選擇晶圓尺寸", ["6 英吋", "8 英吋", "12 英吋"])


df = st.session_state.results_table


st.write("加工時間 (m\:s)")
col_min,  col_sec, col_calc, col_clear = st.columns([3,3,4,2])
with col_min:
    st.number_input("m",key="time_input_min", step=1,value=None, placeholder="分",min_value=0,max_value=59,label_visibility="collapsed")
with col_sec:
    st.number_input("s",key="time_input_sec", step=1,value=None, placeholder="秒",min_value=0,max_value=59,label_visibility="collapsed")


def submit():
    st.session_state.buff_weight_before = st.session_state.input_weight_before
    st.session_state.buff_weight_after = st.session_state.input_weight_after
    
    st.session_state.buf_polished_min = st.session_state.time_input_min
    st.session_state.buf_polished_sec = st.session_state.time_input_sec
    
    st.session_state.input_weight_before = None
    st.session_state.input_weight_after = None
    st.session_state.time_input_min = None
    st.session_state.time_input_sec = None

with col_calc:
    calc = st.button("計算", on_click=submit,type="primary",use_container_width=True)
with col_clear:
    clear = st.button("清除",use_container_width=True)
    
st.divider()

if calc:
    before = st.session_state.buff_weight_before
    after = st.session_state.buff_weight_after
    
    min = st.session_state.buf_polished_min 
    sec = st.session_state.buf_polished_sec 
    if min is None:
        min = 0
    if sec is None:
        sec = 0
    if min == 0 and sec == 0:
        min = 1
            
    if before is None or after is None:
        st.error("請輸入拋光前後的重量")
        st.stop()
    if before < after:
        st.error("拋光前重量不可比拋光後重量大")
        st.stop()
        
    if before and after:
        wafer_diameter_inch = float(wafer_diameter.split()[0]) / 2
        wafer_diameter_mm = wafer_diameter_inch * 25.4 / 1000
        removed_thickness_um = calculate_wafer_thickness(before, after, wafer_diameter_mm)
        st.success(f"晶圓厚度: {removed_thickness_um:.6f} μm")
        
        remove_rate = ((float(removed_thickness_um)) / (float(min) + float(sec) / 60))
        
        df.loc[len(df)] = [before, after, dt.time(0, min, sec),removed_thickness_um, remove_rate]
        
    else:
        st.error("請輸入拋光前後的重量")

st.markdown("### 結果記錄")
st.dataframe(df,hide_index=True, use_container_width=True)
st.divider()

if clear:
    df = pd.DataFrame( columns=data_cols)
    st.session_state.results_table = df
    st.rerun()

st.markdown("### 記錄發送")
email = st.text_input("郵件地址", placeholder="email")
if st.button("發送結果"):
    date_str = dt.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    
    email = emsender("佑能拋光測試結果, 日期:" + date_str, 
                        email)
    email.send(gen_email_content(df))


st.session_state.results_table = df