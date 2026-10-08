import time
import numpy as np
import streamlit as st

st.set_page_config(page_title="Plotting Demo", page_icon="📈")
st.markdown("# Plotting Demo")
st.sidebar.header("Plotting Demo")
st.write("""This demo illustrates plotting and animation with Streamlit.
We're generating random numbers over around five seconds.""")

if st.button("Run animation"):
    progress_bar = st.sidebar.progress(0)
    status_text = st.sidebar.empty()
    data = np.random.randn(1, 1)
    chart = st.empty()
    chart.line_chart(data)
    for i in range(1, 101):
        new_rows = data[-1, :] + np.random.randn(5, 1).cumsum(axis=0)
        data = np.concatenate([data, new_rows])
        status_text.text(f"{i}% Complete")
        chart.line_chart(data)
        progress_bar.progress(i)
        time.sleep(0.05)
    progress_bar.empty()
    status_text.empty()
    st.success("Animation complete!")
else:
    st.info("Click Run animation to view the plotting demo.")
