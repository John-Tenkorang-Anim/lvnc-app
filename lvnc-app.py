import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import plotly.graph_objects as go
import time
from streamlit_extras.metric_cards import style_metric_cards
import pandas as pd
from PIL import Image

# =============================================
# APP CONFIGURATION
# =============================================
st.set_page_config(
    page_title="CardioScan LVNC Detector",
    page_icon="🫀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional medical UI
st.markdown("""
<style>
    .main {
        background-color: #f8f9fa;
    }
    .sidebar .sidebar-content {
        background-color: #2c3e50;
        color: white;
    }
    h1, h2, h3 {
        color: #2c3e50;
    }
    .stButton>button {
        background-color: #e74c3c;
        color: white;
        border-radius: 8px;
        padding: 10px 24px;
    }
    .stProgress>div>div>div>div {
        background-color: #e74c3c;
    }
    .css-1aumxhk {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# =============================================
# SIDEBAR - DEVICE CONTROL PANEL
# =============================================
with st.sidebar:
    st.image("https://img.icons8.com/color/96/heart-health.png", width=80)
    st.title("CardioScan Pro")
    
    # Device Connection Status
    connection_status = st.selectbox(
        "Device Status",
        ["🔴 Disconnected", "🟢 Connected"],
        index=0
    )
    
    if "🟢 Connected" in connection_status:
        st.success("Hardware connected successfully")
        
        # Device Settings
        st.subheader("Device Settings")
        sensitivity = st.slider("Sensor Sensitivity", 1, 100, 75)
        scan_duration = st.select_slider("Scan Duration", options=[5, 10, 15, 30], value=10)
        
        # Patient Info
        st.subheader("Patient Information")
        patient_id = st.text_input("Patient ID")
        age = st.number_input("Age", 1, 120, 45)
        
    else:
        st.error("Please connect CardioScan hardware")
    
    st.markdown("---")
    st.caption("""
    **Instructions:**
    1. Connect CardioScan device
    2. Position sensor on chest
    3. Start scan (10-15 sec)
    4. Review diagnostics
    """)

# =============================================
# MAIN DASHBOARD
# =============================================
st.title("🫀 LVNC Cardiac Analysis System")
st.caption("Advanced detection of Left Ventricular Noncompaction Cardiomyopathy")

# Three-column layout for metrics
col1, col2, col3 = st.columns(3)
col1.metric("Scan Duration", "10 sec", "Ready")
col2.metric("Signal Quality", "92%", "Excellent")
col3.metric("Last Scan", "2 min ago", "Complete")

# Apply styling to metric cards
style_metric_cards(background_color="#FFFFFF", border_left_color="#e74c3c")

# =============================================
# REAL-TIME VISUALIZATION SECTION
# =============================================
if st.button("▶️ Start Cardiac Scan", use_container_width=True):
    
    # Progress bar
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # Initialize plot containers
    wave_container = st.empty()
    freq_container = st.empty()
    analysis_container = st.empty()
    
    # Simulate real-time data acquisition
    sample_rate = 44100
    duration = 10  # seconds
    samples = int(duration * sample_rate)
    t = np.linspace(0, duration, samples, endpoint=False)
    
    # Generate simulated heart sounds with possible abnormalities
    base_signal = 0.5 * np.sin(2 * np.pi * 25 * t)  # Normal heart sound
    noise = 0.1 * np.random.randn(samples)  # Background noise
    
    # Simulate potential LVNC abnormalities
    if np.random.rand() > 0.6:  # 40% chance of abnormal reading
        abnormality = 0.3 * np.sin(2 * np.pi * 150 * t) * (t > 5)
        abnormality += 0.2 * np.random.randn(samples) * (t > 7)
    else:
        abnormality = np.zeros(samples)
    
    full_signal = base_signal + noise + abnormality
    
    # Create dynamic visualization
    for i in range(100):
        # Update progress
        progress_bar.progress(i + 1)
        status_text.text(f"Scanning... {i+1}% complete")
        
        # Update waveform plot
        chunk_size = int(samples/100)
        display_samples = min((i+1)*chunk_size, samples)
        
        fig_wave = go.Figure()
        fig_wave.add_trace(go.Scatter(
            x=t[:display_samples],
            y=full_signal[:display_samples],
            line=dict(color='#e74c3c', width=2),
            name="Cardiac Signal"
        ))
        fig_wave.update_layout(
            title="Real-time Phonocardiogram",
            xaxis_title="Time (seconds)",
            yaxis_title="Amplitude",
            height=300,
            margin=dict(l=20, r=20, t=40, b=20)
        )
        wave_container.plotly_chart(fig_wave, use_container_width=True)
        
        # Update frequency analysis every 5 steps
        if i % 5 == 0:
            f, Pxx = signal.welch(full_signal[:display_samples], sample_rate, nperseg=1024)
            fig_freq = go.Figure()
            fig_freq.add_trace(go.Scatter(
                x=f,
                y=Pxx,
                line=dict(color='#3498db', width=2),
                name="Power Spectrum"
            ))
            fig_freq.update_layout(
                title="Frequency Spectrum Analysis",
                xaxis_title="Frequency (Hz)",
                yaxis_title="Power",
                height=300,
                xaxis_range=[0, 500],
                margin=dict(l=20, r=20, t=40, b=20)
            )
            freq_container.plotly_chart(fig_freq, use_container_width=True)
        
        time.sleep(0.05)
    
    # After scan completion
    progress_bar.empty()
    status_text.success("✅ Scan Complete - Analyzing Results...")
    
    # =============================================
    # DIAGNOSTIC RESULTS SECTION
    # =============================================
    st.markdown("---")
    st.subheader("📊 Diagnostic Analysis")
    
    # Generate simulated diagnostic metrics
    nc_ratio = np.random.uniform(1.5, 2.8)
    ejection_fraction = np.random.uniform(35, 65)
    trabeculation_score = np.random.uniform(0.4, 0.9)
    
    # Calculate risk score
    risk_score = min(100, int(
        30 * (nc_ratio - 1.5) + 
        25 * (1 - (ejection_fraction/65)) + 
        20 * trabeculation_score + 
        np.random.randint(0, 15)
    ))
    
    # Display metrics in cards
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("NC Ratio", f"{nc_ratio:.2f}", ">2.0 suggests LVNC" if nc_ratio > 2 else "Normal")
    col2.metric("Ejection Fraction", f"{ejection_fraction:.1f}%", "Concern <40%" if ejection_fraction < 40 else "Normal")
    col3.metric("Trabeculation Score", f"{trabeculation_score:.2f}", "High" if trabeculation_score > 0.7 else "Normal")
    col4.metric("LVNC Risk Score", f"{risk_score}/100", "High Risk" if risk_score > 60 else "Moderate" if risk_score > 40 else "Low")
    
    # Risk visualization
    fig_risk = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = risk_score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "LVNC Risk Assessment"},
        gauge = {
            'axis': {'range': [0, 100]},
            'steps': [
                {'range': [0, 40], 'color': "lightgreen"},
                {'range': [40, 60], 'color': "orange"},
                {'range': [60, 100], 'color': "red"}
            ],
            'threshold': {
                'line': {'color': "black", 'width': 4},
                'thickness': 0.75,
                'value': risk_score
            }
        }
    ))
    fig_risk.update_layout(height=300)
    st.plotly_chart(fig_risk, use_container_width=True)
    
    # Recommendations
    if risk_score > 70:
        st.error("""
        **🚨 High Probability of LVNC Detected**
        
        Clinical Recommendations:
        - Urgent cardiology referral
        - Cardiac MRI with contrast
        - 24-hour Holter monitoring
        - Family screening advised
        """)
    elif risk_score > 45:
        st.warning("""
        **⚠️ Moderate Suspicion for LVNC**
        
        Clinical Recommendations:
        - Echocardiogram with contrast
        - ECG and clinical evaluation
        - Consider cardiac MRI if symptoms progress
        """)
    else:
        st.success("""
        **✅ Low Probability of LVNC**
        
        Clinical Recommendations:
        - Routine follow-up if symptomatic
        - Re-evaluate if new symptoms emerge
        """)

# =============================================
# PATIENT HISTORY SECTION (Collapsible)
# =============================================
with st.expander("📋 Patient History & Prior Scans"):
    if '🟢 Connected' in connection_status:
        # Simulated patient data
        history_data = pd.DataFrame({
            "Date": ["2023-06-15", "2023-03-22", "2022-11-10"],
            "NC Ratio": [1.8, 1.7, 1.6],
            "EF (%)": [58, 60, 62],
            "Risk Score": [45, 38, 32],
            "Findings": ["Stable", "Normal variant", "Initial screening"]
        })
        st.dataframe(history_data, hide_index=True, use_container_width=True)
        
        # Trend visualization
        fig_trend = go.Figure()
        fig_trend.add_trace(go.Scatter(
            x=history_data["Date"],
            y=history_data["Risk Score"],
            mode='lines+markers',
            name="Risk Score",
            line=dict(color='#e74c3c', width=3)
        ))
        fig_trend.update_layout(
            title="LVNC Risk Trend Over Time",
            yaxis_title="Risk Score",
            height=300
        )
        st.plotly_chart(fig_trend, use_container_width=True)
    else:
        st.warning("Connect device to access patient history")

# =============================================
# FOOTER & DISCLAIMER
# =============================================
st.markdown("---")
st.caption("""
**CardioScan LVNC Detection System** | For clinical use only  
*This device is intended to assist healthcare professionals in LVNC assessment.  
Final diagnosis requires comprehensive clinical evaluation.*  
© 2023 CardioScan Technologies
""")