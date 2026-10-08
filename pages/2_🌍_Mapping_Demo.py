import streamlit as st
import pandas as pd
import pydeck as pdk

st.set_page_config(page_title="Mapping Demo", page_icon="🌍")
st.markdown("# Mapping Demo")
st.sidebar.header("Mapping Demo")
st.write("""This demo uses `st.pydeck_chart` to show geospatial data.
Choose one or more map layers in the sidebar.""")

@st.cache_data(show_spinner="Loading mapping data...")
def from_data_file(filename):
    url = f"https://raw.githubusercontent.com/streamlit/example-data/master/hello/v1/{filename}"
    return pd.read_json(url)

try:
    all_layers = {
        "Bike Rentals": pdk.Layer(
            "HexagonLayer", data=from_data_file("bike_rental_stats.json"),
            get_position=["lon", "lat"], radius=200, elevation_scale=4,
            elevation_range=[0, 1000], extruded=True,
        ),
        "Bart Stop Exits": pdk.Layer(
            "ScatterplotLayer", data=from_data_file("bart_stop_stats.json"),
            get_position=["lon", "lat"], get_color=[200, 30, 0, 160],
            get_radius="exits", radius_scale=0.05,
        ),
        "Bart Stop Names": pdk.Layer(
            "TextLayer", data=from_data_file("bart_stop_stats.json"),
            get_position=["lon", "lat"], get_color=[0, 0, 0, 200],
            get_text="name", get_size=15, get_alignment_baseline="'bottom'",
        ),
        "Outbound Flow": pdk.Layer(
            "ArcLayer", data=from_data_file("bart_path_stats.json"),
            get_source_position=["lon", "lat"], get_target_position=["lon2", "lat2"],
            get_source_color=[200, 30, 0, 160], get_target_color=[200, 30, 0, 160],
            auto_highlight=True, width_scale=0.0001,
            get_width="outbound", width_min_pixels=3, width_max_pixels=30,
        ),
    }
    st.sidebar.markdown("### Map Layers")
    selected_layers = [
        layer for name, layer in all_layers.items()
        if st.sidebar.checkbox(name, value=True)
    ]
    if selected_layers:
        st.pydeck_chart(pdk.Deck(
            map_style="https://basemaps.cartocdn.com/gl/positron-gl-style/style.json",
            initial_view_state=pdk.ViewState(latitude=37.76, longitude=-122.4, zoom=11, pitch=50),
            layers=selected_layers,
        ))
    else:
        st.warning("Please choose at least one layer above.")
except Exception as exc:
    st.error("This demo requires internet access to load the example mapping data.")
    st.exception(exc)
