import streamlit as st
import pandas as pd
import numpy as np
import math

def main():
    st.title('Covid-19 Aerosol Transmission Estimator')
    st.markdown('Based on version 3.4.19 of [https://tinyurl.com/covid-estimator](https://tinyurl.com/covid-estimator)')
    st.sidebar.markdown('# Parameters')
    st.sidebar.markdown('### Room measurements')
    b13 = st.sidebar.number_input('Length of room (in ft)', value=80)
    b14 = st.sidebar.number_input('Width of room (in ft)', value=50)
    b16 = st.sidebar.number_input('Height of room (in ft)', value=18)
    b28 = st.sidebar.number_input('Air changes per hour', value=3)
    st.sidebar.markdown('### Scenario parameters')
    b24 = st.sidebar.number_input('Duration of event (in min)', value=480)
    b26 = st.sidebar.number_input('Number of repetitions of event', value=26)
    b38 = st.sidebar.number_input('Total number of people present', value=75)
    b39 = st.sidebar.number_input('Infective people', value=1)
    st.sidebar.markdown('### Advanced parameters')
    b47 = st.sidebar.number_input('Breathing rate of susceptibles (m3/hr)', value=0.72)
    b51 = st.sidebar.number_input('Quanta exhalation rate of infected (quanta/hr)', value=10)
    b52 = st.sidebar.number_input('Exhalation mask efficiency (%)', value=50)
    b53 = st.sidebar.number_input('Fraction of people w/ masks', value=100)
    b54 = st.sidebar.number_input('Inhalation mask efficiency', value=30)

    ## Calculations
    ### Calculating room volume
    e13 = b13 * 0.305
    e14 = b14 * 0.305
    e15 = e13 * e14
    e16 = b16 * 0.305
    e17 = e13 * e14 * e16

    e24 = b24/60

    ### Calculating first order loss rate
    b29 = 0.62
    b30 = 0.3
    b31 = 0
    b32 = b28 + b29 + b30 + b31

    ### Calculating ventilation rate per person
    b34 = e17 * (b28 + b31) * 1000 / 3600 / b38

    ### Calculating quanta
    b66 = b51 * (1 - (b52/100) * (b53/100)) * b39
    b67 = b66/b32/e17 * (1-(1/b32/e24) * (1 - math.exp(-1 * b32 * e24)))
    b68 = b67 * b47 * e24 * (1 - (b54/100) * (b53/100))

    b71 = (1 - math.exp(-1 * b68)) * 100

    st.markdown('### Overall Results')
    st.write(f'Probability of infection: {b71}%')

    st.markdown('### Intermediate Results')
    st.write(f'First order loss rate: {b32} h-1')
    st.write(f'Ventilation rate per person: {b34} L/s/person')



if __name__ == "__main__":
    main()