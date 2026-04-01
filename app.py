import streamlit as st

st.set_page_config(page_title="坐位胃超声饱胃预警系统", page_icon="🩻")

st.title("🩻 坐位胃部超声：容量预测与饱胃预警系统")
st.markdown("**作者**：XXX博士 | **单位**：XX大学XX医院麻醉科")
st.markdown("---")

csa = st.number_input("坐位胃窦横截面积 (CSA, cm²)", min_value=0.0, value=3.5, step=0.1)
weight = st.number_input("患者体重 (Weight, kg)", min_value=30.0, value=65.0, step=1.0)
diabetes = st.selectbox("是否合并糖尿病?", ["无", "有"])

if st.button("🚀 一键评估误吸风险"):
    diab_value = 10 if diabetes == "有" else 0
    # 这里记得换成你真实的公式！
    pred_volume = (25.4 * csa) + (1.2 * weight) + diab_value - 15.6
    pred_volume = max(0, pred_volume) 
    risk_ratio = pred_volume / weight
    
    st.info(f"**预估胃绝对容量**： **{pred_volume:.1f} mL**")
    st.warning(f"**单位体重胃容量**： **{risk_ratio:.2f} mL/kg**")
    
    if risk_ratio >= 1.5:
        st.error("🚨 **高危饱胃状态 (High Risk)** \n\n 患者胃容量已超出安全阈值。强烈建议采取快速序贯诱导 (RSI)。")
    else:
        st.success("✅ **低误吸风险 (Low Risk)** \n\n 胃排空情况良好，可安全实施常规麻醉诱导。")
        st.balloons()
