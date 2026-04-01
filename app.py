import streamlit as st

# 1. 设置网页的标题和基本配置
st.set_page_config(page_title="坐位胃超声饱胃预警系统", page_icon="🩻", layout="centered")

# 2. 网页头部设计
st.title("🩻 坐位胃部超声：容量定量与饱胃预警系统")
st.markdown("""
**作者**：周智虎 | **单位**：桂林医科大学第二附属医院麻醉科  
*本辅助决策工具基于多中心队列数据推导的多元线性公式开发，仅供围术期气道管理参考。*
---
""")

st.header("📝 1. 请输入患者临床参数")

# 3. 界面排版：分成两列更好看
col1, col2 = st.columns(2)

with col1:
    csa = st.number_input("坐位胃窦横截面积 (CSA, cm²)", min_value=0.0, max_value=25.0, value=3.5, step=0.1)
    age = st.number_input("患者年龄 (Age, 岁)", min_value=18, max_value=120, value=45, step=1)

with col2:
    # 提示医生：体重虽不参与容量计算，但用于计算风险阈值
    weight = st.number_input("患者体重 (Weight, kg)", min_value=30.0, max_value=150.0, value=65.0, step=1.0)
    st.caption("注：体重参数用于换算单位体重容量 (mL/kg) 风险阈值")

st.markdown("---")
st.header("⚙️ 2. 智能评估结果")

# 4. 核心计算与红绿灯逻辑
if st.button("🚀 一键评估误吸风险", use_container_width=True):
    
    # 【核心：植入你的专属博士论文公式！】
    # GV(ml) = 11.27 × 坐位CSA - 0.57 × 年龄 + 12.89
    pred_volume = (11.27 * csa) - (0.57 * age) + 12.89
    
    # 生理学兜底：防止极端数值算出负数容量
    pred_volume = max(0, pred_volume) 
    
    # 计算风险比 (mL/kg)
    risk_ratio = pred_volume / weight
    
    # 5. 结果展示（红绿灯视觉冲击）
    col3, col4 = st.columns(2)
    with col3:
        st.info(f"### 📈 预估胃容量 \n ## **{pred_volume:.1f} mL**")
    with col4:
        st.warning(f"### ⚖️ 单位体重容量 \n ## **{risk_ratio:.2f} mL/kg**")
    
    st.markdown("### 🚦 临床气道管理建议")
    
    # 判断是否超过 1.5 ml/kg 的高危截断值
    if risk_ratio >= 1.5:
        st.error("""
        🚨 **高危饱胃状态 (High Risk)** 
        
        患者预估单位体重胃容量已达到或超出 **1.5 mL/kg** 的高误吸风险阈值。
        
        👉 **决策建议**：强烈建议采取 **快速序贯诱导 (RSI)**、清醒插管，或在条件允许时推迟择期手术及进行胃管抽吸减压！
        """)
    else:
        st.success("""
        ✅ **低误吸风险 (Low Risk)** 
        
        患者预估单位体重胃容量低于 1.5 mL/kg，胃排空情况良好。
        
        👉 **决策建议**：在无其他反流高危因素及禁忌症的情况下，可安全实施 **常规麻醉诱导**。
        """)
        st.balloons() # 庆祝气球动画
