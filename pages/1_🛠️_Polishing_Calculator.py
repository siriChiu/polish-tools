import streamlit as st
import math

st.set_page_config(
    page_title="佑能科技-拋光研磨計算機",
    page_icon="🌟",
)

def calculate_wafer_thickness(weight_before, weight_after, wafer_diameter):
    density = 2330000  # g/m^3
    weight_difference = weight_before - weight_after
    wafer_thickness = weight_difference / (density * math.pi * (wafer_diameter ** 2)) *1000000
    return wafer_thickness

st.title("拋光研磨計算機")


weight_before = st.number_input("拋光前重量 (g)", step=0.01, value=53.55)
weight_after = st.number_input("拋光後重量 (g)", step=0.01, value=53.26)
wafer_diameter = st.selectbox("選擇晶圓尺寸", ["6 英吋", "8 英吋", "12 英吋"])

if st.button("計算"):
    if weight_before and weight_after:
        wafer_diameter_inch = float(wafer_diameter.split()[0]) / 2
        wafer_diameter_mm = wafer_diameter_inch * 25.4 / 1000
        result = calculate_wafer_thickness(weight_before, weight_after, wafer_diameter_mm)
        st.success(f"晶圓厚度: {result:.6f} μm")
    else:
        st.error("請輸入拋光前後的重量")
