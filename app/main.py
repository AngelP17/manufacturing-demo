import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta

# Page configuration
st.set_page_config(
    page_title="Manufacturing Infrastructure Demo",
    page_icon="🏭",
    layout="wide"
)

# Generate demo data
def generate_machine_data():
    now = datetime.now()
    dates = pd.date_range(end=now, periods=100, freq='1H')
    machines = ['Machine 1', 'Machine 2', 'Machine 3', 'Machine 4']
    
    data = []
    for machine in machines:
        base_efficiency = np.random.uniform(85, 95)
        for date in dates:
            efficiency = base_efficiency + np.random.normal(0, 2)
            data.append({
                'timestamp': date,
                'machine': machine,
                'efficiency': min(100, max(0, efficiency)),
                'temperature': np.random.uniform(60, 75),
                'pressure': np.random.uniform(95, 105),
                'status': np.random.choice(['Active', 'Active', 'Active', 'Maintenance'])
            })
    return pd.DataFrame(data)

def generate_production_data():
    now = datetime.now()
    dates = pd.date_range(end=now, periods=24, freq='1H')
    return pd.DataFrame({
        'timestamp': dates,
        'production_rate': np.random.uniform(85, 98, size=24),
        'quality_score': np.random.uniform(90, 100, size=24),
        'defect_rate': np.random.uniform(0.1, 2.0, size=24)
    })

# Cache the demo data
@st.cache_data
def load_demo_data():
    return {
        'machine_data': generate_machine_data(),
        'production_data': generate_production_data()
    }

# Main application
def main():
    # Sidebar
    st.sidebar.title('Navigation')
    page = st.sidebar.selectbox(
        'Select Page',
        ['Dashboard', 'Machine Monitoring', 'Production Analytics', 'System Settings']
    )

    # Load data
    data = load_demo_data()
    machine_data = data['machine_data']
    production_data = data['production_data']

    if page == 'Dashboard':
        st.title('Manufacturing System Dashboard')
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            active_machines = machine_data[
                machine_data['status'] == 'Active'
            ]['machine'].nunique()
            total_machines = machine_data['machine'].nunique()
            st.metric(
                "Active Machines",
                f"{active_machines}/{total_machines}",
                f"{active_machines/total_machines:.0%}"
            )

        with col2:
            avg_efficiency = machine_data['efficiency'].mean()
            st.metric(
                "Average Efficiency",
                f"{avg_efficiency:.1f}%",
                "1.2%"
            )

        with col3:
            avg_temp = machine_data['temperature'].mean()
            st.metric(
                "Average Temperature",
                f"{avg_temp:.1f}°C",
                "-0.5°C"
            )

        with col4:
            quality_score = production_data['quality_score'].iloc[-1]
            st.metric(
                "Quality Score",
                f"{quality_score:.1f}%",
                "0.8%"
            )

        # Efficiency Chart
        st.subheader('Machine Efficiency Trends')
        fig_efficiency = px.line(
            machine_data,
            x='timestamp',
            y='efficiency',
            color='machine',
            title='Machine Efficiency Over Time'
        )
        st.plotly_chart(fig_efficiency, use_container_width=True)

        # Production Rate and Quality
        st.subheader('Production Metrics')
        fig_production = px.line(
            production_data,
            x='timestamp',
            y=['production_rate', 'quality_score'],
            title='Production Rate and Quality Score'
        )
        st.plotly_chart(fig_production, use_container_width=True)

    elif page == 'Machine Monitoring':
        st.title('Machine Monitoring')
        
        # Machine selector
        selected_machine = st.selectbox(
            'Select Machine',
            machine_data['machine'].unique()
        )

        # Filter data for selected machine
        machine_metrics = machine_data[machine_data['machine'] == selected_machine].iloc[-1]
        
        # Machine status and metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Status", machine_metrics['status'])
        with col2:
            st.metric("Temperature", f"{machine_metrics['temperature']:.1f}°C")
        with col3:
            st.metric("Pressure", f"{machine_metrics['pressure']:.1f} PSI")

        # Machine details charts
        machine_history = machine_data[machine_data['machine'] == selected_machine]
        
        # Temperature trend
        st.subheader('Temperature Trend')
        fig_temp = px.line(
            machine_history,
            x='timestamp',
            y='temperature',
            title=f'{selected_machine} Temperature History'
        )
        st.plotly_chart(fig_temp, use_container_width=True)

    elif page == 'Production Analytics':
        st.title('Production Analytics')
        
        # Production overview
        latest_metrics = production_data.iloc[-1]
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(
                "Production Rate",
                f"{latest_metrics['production_rate']:.1f}/hr",
                "2.1%"
            )
        with col2:
            st.metric(
                "Quality Score",
                f"{latest_metrics['quality_score']:.1f}%",
                "0.8%"
            )
        with col3:
            st.metric(
                "Defect Rate",
                f"{latest_metrics['defect_rate']:.2f}%",
                "-0.1%"
            )

        # Production trends
        st.subheader('Production Trends')
        fig_trends = px.line(
            production_data,
            x='timestamp',
            y=['production_rate', 'quality_score', 'defect_rate'],
            title='Production Metrics Over Time'
        )
        st.plotly_chart(fig_trends, use_container_width=True)

    elif page == 'System Settings':
        st.title('System Settings')
        
        st.subheader('Alert Configuration')
        col1, col2 = st.columns(2)
        with col1:
            st.number_input('Temperature Alert Threshold (°C)', value=80.0)
            st.number_input('Pressure Alert Threshold (PSI)', value=110.0)
        with col2:
            st.number_input('Efficiency Alert Threshold (%)', value=85.0)
            st.number_input('Quality Score Alert Threshold (%)', value=90.0)
        
        st.button('Save Settings')

        st.subheader('System Maintenance')
        st.checkbox('Enable Automatic Updates')
        st.checkbox('Enable Performance Monitoring')
        st.checkbox('Enable Error Reporting')
        
        if st.button('Run System Diagnostics'):
            with st.spinner('Running diagnostics...'):
                # Simulate diagnostic run
                import time
                time.sleep(2)
                st.success('System diagnostics completed successfully!')

if __name__ == "__main__":
    main()