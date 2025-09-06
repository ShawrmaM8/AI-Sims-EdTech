import streamlit as st
from business.marketing_sim import MarketingSimulator
from business.hr_conflict_sim import HRConflictSimulator
from business.startup_sim import StartupSimulator
from health.pharm_safety_sim import PharmacologySimulator
from health.outbreak_sim import OutbreakSimulator
from health.chronic_care_sim import ChronicCareSimulator
import pandas as pd
import plotly.graph_objects as go
import json, sys, os

sys.path.append(r"C:\Users\muzam\OneDrive\Desktop\PROJECTS\NajmAI\ai_simulations")

st.set_page_config(page_title='AI Simulation Platform', layout='wide')
st.title('AI-Assisted Situation-Crafting Simulations')

# Simulation Selection
simulation_options = {
    'Digital Marketing': MarketingSimulator,
    'HR Conflict Resolution': HRConflictSimulator,
    'Entrepreneurship Startup': StartupSimulator,
    'Pharmacology Safety': PharmacologySimulator,
    'Outbreak Management': OutbreakSimulator,
    'Chronic Care': ChronicCareSimulator
}

selected_sim_name = st.sidebar.selectbox('Select Simulation', list(simulation_options.keys()))
scenario_path = f'data/scenarios/{selected_sim_name.lower().replace(" ","_")}.json'
SimulationClass = simulation_options[selected_sim_name]
sim = SimulationClass(scenario_path)

# User session
user_id = st.sidebar.text_input('User ID', 'test_user')
session_key = f'{selected_sim_name}_{user_id}'

if session_key not in st.session_state:
    st.session_state[session_key] = sim.new_session(user_id)

runtime = st.session_state[session_key]

st.sidebar.markdown(f'### Scenario: {selected_sim_name}')
st.sidebar.caption(f'Description loaded from {scenario_path}')

# Display current metrics
st.subheader('Current Metrics')
metrics = runtime['metrics']
cols = st.columns(len(metrics))
for i, (k, v) in enumerate(metrics.items()):
    display_val = f'{v:.2f}' if isinstance(v, float) else str(v)
    cols[i].metric(k.replace('_',' ').title(), display_val)

st.markdown('---')

# Load decisions
with open(scenario_path) as f:
    scenario_data = json.load(f)
decisions = scenario_data.get('decisions', [])

for decision in decisions:
    st.write(f"**{decision['prompt']}**")
    cols = st.columns(len(decision['options']))
    for i, opt in enumerate(decision['options']):
        if cols[i].button(opt['label'], key=f"{decision['id']}_{opt['id']}"):
            sim.apply_decision(runtime, decision['id'], opt['id'])
            st.success(f"Decision applied: {opt['label']}")

# AI Evaluation / Feedback
st.subheader('AI Advice / Feedback')
eval_report = sim.evaluate_session(runtime)
advice = eval_report.get('advice', {})
if not advice:
    st.write('No immediate advice — metrics within normal ranges.')
else:
    for v in advice.values():
        st.warning(v)

# Metrics Timeline Plot
st.subheader('Metrics Over Time')
df = pd.DataFrame(runtime['metrics_history'])
df['step'] = range(1, len(df)+1)
fig = go.Figure()
for metric in df.columns:
    if metric != 'step':
        fig.add_trace(go.Scatter(x=df['step'], y=df[metric], mode='lines+markers', name=metric))
st.plotly_chart(fig, use_container_width=True)

# Reset Session
if st.button('Reset Simulation'):
    st.session_state[session_key] = sim.new_session(user_id)
    st.experimental_rerun()

st.markdown('---')
st.info('Select different simulations from the sidebar to switch scenarios.')
