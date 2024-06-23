import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt
import skfuzzy.control as ctrl
import streamlit as st
import plotly.graph_objects as go
import random


x_income = np.arange(0, 101, 1)
x_history = np.arange(0, 101, 1)
x_age = np.arange(0, 101, 1)

age_young = fuzz.gaussmf(x_age, 20, 10)  
age_middle_aged = fuzz.gaussmf(x_age, 50, 10)  
age_old = fuzz.gaussmf(x_age, 80, 10)

income_low = fuzz.trapmf(x_income, [0, 0,10, 50])
income_medium = fuzz.trimf(x_income, [25, 50, 75])
income_high = fuzz.trapmf(x_income, [50, 90, 100, 100])

history_rarely = fuzz.trimf(x_history, [0, 0, 30])
history_occasionally = fuzz.trimf(x_history, [20, 50, 80])
history_frequently = fuzz.trimf(x_history, [60, 100, 100])

x_likelihood = np.arange(0, 101, 1)

likelihood_low = fuzz.trimf(x_likelihood, [0, 0, 30])
likelihood_medium = fuzz.trimf(x_likelihood, [20, 50, 80])
likelihood_high = fuzz.trimf(x_likelihood, [60, 100, 100])


age = ctrl.Antecedent(x_age, 'age')
income = ctrl.Antecedent(x_income, 'income')
history = ctrl.Antecedent(x_history, 'history')
likelihood = ctrl.Consequent(x_likelihood, 'likelihood')

age['young'] = age_young
age['middle-aged'] = age_middle_aged
age['old'] = age_old

income['low'] = income_low
income['medium'] = income_medium
income['high'] = income_high

history['rarely'] = history_rarely
history['occasionally'] = history_occasionally
history['frequently'] = history_frequently

likelihood['low'] = likelihood_low
likelihood['medium'] = likelihood_medium
likelihood['high'] = likelihood_high

# Define rules
rules = [
    ctrl.Rule(age['young'] & income['low'] & history['rarely'], likelihood['low']),
    ctrl.Rule(age['young'] & income['low'] & history['occasionally'], likelihood['medium']),
    ctrl.Rule(age['young'] & income['low'] & history['frequently'], likelihood['medium']),
    ctrl.Rule(age['young'] & income['medium'] & history['rarely'], likelihood['low']),
    ctrl.Rule(age['young'] & income['medium'] & history['occasionally'], likelihood['medium']),
    ctrl.Rule(age['young'] & income['medium'] & history['frequently'], likelihood['high']),
    ctrl.Rule(age['young'] & income['high'] & history['rarely'], likelihood['medium']),
    ctrl.Rule(age['young'] & income['high'] & history['occasionally'], likelihood['high']),
    ctrl.Rule(age['young'] & income['high'] & history['frequently'], likelihood['high']),
    ctrl.Rule(age['middle-aged'] & income['low'] & history['rarely'], likelihood['low']),
    ctrl.Rule(age['middle-aged'] & income['low'] & history['occasionally'], likelihood['medium']),
    ctrl.Rule(age['middle-aged'] & income['low'] & history['frequently'], likelihood['medium']),
    ctrl.Rule(age['middle-aged'] & income['medium'] & history['rarely'], likelihood['low']),
    ctrl.Rule(age['middle-aged'] & income['medium'] & history['occasionally'], likelihood['medium']),
    ctrl.Rule(age['middle-aged'] & income['medium'] & history['frequently'], likelihood['high']),
    ctrl.Rule(age['middle-aged'] & income['high'] & history['rarely'], likelihood['medium']),
    ctrl.Rule(age['middle-aged'] & income['high'] & history['occasionally'], likelihood['high']),
    ctrl.Rule(age['middle-aged'] & income['high'] & history['frequently'], likelihood['high']),
    ctrl.Rule(age['old'] & income['low'] & history['rarely'], likelihood['low']),
    ##
    ctrl.Rule(age['old'] & income['low'] & history['occasionally'], likelihood['low']),
    ctrl.Rule(age['old'] & income['low'] & history['frequently'], likelihood['medium']),
    ctrl.Rule(age['old'] & income['medium'] & history['rarely'], likelihood['low']),
    ctrl.Rule(age['old'] & income['medium'] & history['occasionally'], likelihood['low']),
    ctrl.Rule(age['old'] & income['medium'] & history['frequently'], likelihood['medium']),
    ctrl.Rule(age['old'] & income['high'] & history['rarely'], likelihood['medium']),
    ctrl.Rule(age['old'] & income['high'] & history['occasionally'], likelihood['high']),
    ##
    ctrl.Rule(age['old'] & income['high'] & history['frequently'], likelihood['high'])
]

likelihood_ctrl = ctrl.ControlSystem(rules)
likelihood_sim = ctrl.ControlSystemSimulation(likelihood_ctrl)

def defuzzification(age_value, income_value, history_value):
    likelihood_sim.input['age'] = age_value
    likelihood_sim.input['income'] = income_value
    likelihood_sim.input['history'] = history_value

    likelihood_sim.defuzzify_method = 'centroid'

    likelihood_sim.compute()

    fuzzy_output = likelihood_sim.output['likelihood']

    # print(f"Age: {age_value}, Income: {income_value}, History: {history_value} -> Likelihood (Fuzzy Output): {fuzzy_output:.2f}")

    return fuzzy_output

def likelihood_to_text(value):
    if value < 40:
        return "low"
    elif 40 <= value <= 60:
        return "medium"
    else:
        return "high"

test_data = [
    {'age': 25, 'income': 70, 'history': 80},
    {'age': 65, 'income': 30, 'history': 20},
    {'age': 40, 'income': 60, 'history': 50},
    {'age': 20, 'income': 20, 'history': 90},
    {'age': 70, 'income': 90, 'history': 70},
]

for data in test_data:
    print(data)
    result = defuzzification(data['age'], data['income'], data['history'])


### user interface

st.set_option('deprecation.showPyplotGlobalUse', False)

st.title('Buying Product Prediction Tool')

st.text('A Fuzzy Expert System for predicting the likelihood of a customer buying a product based on their age, income, and purchase history. ')

st.divider()


st.text('See System Plots:')

col1, col2, col3, col4 = st.columns([1,1,1,1])
   
st.subheader('Input Parameters:')
input_age = st.number_input("Enter your age", value=23)
input_income = st.number_input("Enter your income", value=70)
input_history = st.number_input("Enter your purchase history", value=80)

if st.button('get results'):
    print(input_age)
    print(input_income)
    print(input_history)

    if input_age > 0 and input_age < 101 and input_income > 0 and input_income < 101 and input_history > 0 and input_history < 101:

        st.balloons()
    
        likelihood_results = defuzzification(input_age, input_income, input_history)
        # st.write(likelihood_results)
        st.markdown(f'<div style="color:white; border:2px solid white; padding: 5px; border-radius: 5px;">{likelihood_results}</div>', unsafe_allow_html=True)
        st.divider()
        st.write("Likelihood of a customer buying a product is", likelihood_to_text(likelihood_results))

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x_likelihood, y=likelihood_low, mode='lines', name='Low'))
        fig.add_trace(go.Scatter(x=x_likelihood, y=likelihood_medium, mode='lines', name='Medium'))
        fig.add_trace(go.Scatter(x=x_likelihood, y=likelihood_high, mode='lines', name='High'))
        fig.add_trace(go.Scatter(x=[likelihood_results, likelihood_results], y=[0, 1], mode='lines', line=dict(color='black', dash='dash'), name='Result'))  # Change mode to 'lines'
        fig.update_layout(title='Likelihood of Buying Product', xaxis_title='Likelihood', yaxis_title='Membership')
        st.plotly_chart(fig, use_container_width=True)

        fig, ax = plt.subplots()
        ax.plot(x_likelihood, likelihood_low, 'b', linewidth=1.5, label='Low')
        ax.plot(x_likelihood, likelihood_medium, 'g', linewidth=1.5, label='Medium')
        ax.plot(x_likelihood, likelihood_high, 'r', linewidth=1.5, label='High')
        ax.axvline(likelihood_results, color='k', linestyle='dashed', linewidth=1.5)
        ax.set_title('Likelihood of Buying Product')
        ax.legend()
        st.pyplot(fig)
    
    else:
        if input_age < 0 or input_age > 100 :
            st.error("age must be between 1 and 100")
        
        if input_income < 0 or input_income > 100 :
            st.error("income must be between 1 and 100")
            
        if input_history < 0 or input_history > 100:
            st.error("purchase history must be between 1 and 100")



with col1:    
    if st.button('Age Plot'):
        defuzzification(input_age, input_income, input_history)  
        st.pyplot(fig=age.view(sim=likelihood_sim), clear_figure=True, use_container_width=True)    

with col2:
    if st.button('Income Plot'):
        defuzzification(input_age, input_income, input_history)  
        st.pyplot(fig=income.view(sim=likelihood_sim), clear_figure=True, use_container_width=True)    

with col3:
    if st.button('History Plot'):
        defuzzification(input_age, input_income, input_history)  
        st.pyplot(fig=history.view(sim=likelihood_sim), clear_figure=True, use_container_width=True)    

with col4:
    if st.button('Likelihood Plot'):
        defuzzification(input_age, input_income, input_history)  
        st.pyplot(fig=likelihood.view(sim=likelihood_sim), clear_figure=True, use_container_width=True)


