import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="DataFrame Demo", page_icon="📊")
st.markdown("# DataFrame Demo")
st.sidebar.header("DataFrame Demo")
st.write("""This demo shows how to display Pandas DataFrames and charts.
Data courtesy of the UN Data Explorer.""")

@st.cache_data(show_spinner="Loading agricultural data...")
def get_un_data():
    url = "https://streamlit-demo-data.s3-us-west-2.amazonaws.com/agri.csv.gz"
    return pd.read_csv(url).set_index("Region")

try:
    df = get_un_data()
    default_countries = [
        c for c in ["China", "United States of America"] if c in df.index
    ]
    countries = st.multiselect("Choose countries", list(df.index), default_countries)
    if not countries:
        st.warning("Please select at least one country.")
    else:
        data = df.loc[countries].copy() / 1_000_000.0
        st.write("### Gross Agricultural Production ($B)")
        st.dataframe(data.sort_index())
        long_data = data.T.reset_index().melt(id_vars=["index"])
        long_data = long_data.rename(columns={
            "index": "year", "value": "Gross Agricultural Product ($B)"
        })
        chart = alt.Chart(long_data).mark_area(opacity=0.4).encode(
            x=alt.X("year:O", title="Year"),
            y=alt.Y("Gross Agricultural Product ($B):Q", stack=None),
            color="Region:N",
            tooltip=["Region:N", "year:O", "Gross Agricultural Product ($B):Q"],
        )
        st.altair_chart(chart, use_container_width=True)
except Exception as exc:
    st.error("This demo requires internet access to load the example agricultural data.")
    st.exception(exc)
