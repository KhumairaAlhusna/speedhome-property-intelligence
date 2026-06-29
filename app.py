import streamlit as st
import plotly.express as px

from scraper_v2 import get_html
from scraper_v2 import parse_properties

from analytics import calculate_statistics

from utils import (
    dataframe_to_csv,
    dataframe_to_excel,
    create_summary_table
)

st.set_page_config(
    page_title="SPEEDHOME Property Price Intelligence",
    page_icon="🏠",
    layout="wide"
)

st.title("🏠 SPEEDHOME Property Price Intelligence")
st.caption("Property Analytics Dashboard")

# ==========================
# Sidebar
# ==========================

st.sidebar.header("Search Property")

search = st.sidebar.text_input(
    "Area",
    value="Mont Kiara"
)

url = st.sidebar.text_input(
    "SPEEDHOME URL (Optional)",
    value=""
)

search_button = st.sidebar.button(
    "🔍 Search",
    width="stretch"
)

st.sidebar.markdown("---")

st.sidebar.info(
    "Masukkan nama area atau URL SPEEDHOME."
)

# ==========================
# Main
# ==========================

if search_button:

    with st.spinner("Scraping SPEEDHOME..."):

        html = get_html(
            search=search,
            url=url if url else None
        )

        df = parse_properties(html)

        if df.empty:
            st.error("Tidak ada property ditemukan.")
            st.stop()

        stats = calculate_statistics(df)

    st.success(
        f"Berhasil mengambil {stats['count']} property."
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Average",
        f"RM {stats['average']:,.0f}"
    )

    col2.metric(
        "Median",
        f"RM {stats['median']:,.0f}"
    )

    col3.metric(
        "Mode",
        f"RM {stats['mode']:,.0f}"
        if stats["mode"] is not None else "-"
    )

    col4.metric(
        "Fair Price",
        f"RM {stats['fair_price']:,.0f}"
    )

    st.divider()

    # ==========================
    # Price Summary
    # ==========================

    st.subheader("📊 Price Summary")

    summary = create_summary_table(stats)

    st.dataframe(
        summary,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # ==========================
    # Download Data
    # ==========================

    csv_file = dataframe_to_csv(
        stats["data"]
    )

    excel_file = dataframe_to_excel(
        stats["data"]
    )

    download_col1, download_col2 = st.columns(2)

    with download_col1:

        st.download_button(
            label="⬇ Download CSV",
            data=csv_file,
            file_name="speedhome_properties.csv",
            mime="text/csv",
            use_container_width=True
        )

    with download_col2:

        st.download_button(
            label="⬇ Download Excel",
            data=excel_file,
            file_name="speedhome_properties.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )

    st.divider()

    # ==========================
    # Charts
    # ==========================

    st.subheader("📈 Property Analytics")

    tab1, tab2, tab3 = st.tabs(
        [
            "Histogram",
            "Box Plot",
            "Scatter Plot"
        ]
    )

    with tab1:

        fig_hist = px.histogram(
            stats["data"],
            x="Price_Num",
            nbins=20,
            title="Property Price Distribution"
        )

        fig_hist.update_layout(
            xaxis_title="Price (RM)",
            yaxis_title="Number of Properties"
        )

        st.plotly_chart(
            fig_hist,
            use_container_width=True
        )

    with tab2:

        fig_box = px.box(
            stats["data"],
            y="Price_Num",
            title="Price Box Plot"
        )

        fig_box.update_layout(
            yaxis_title="Price (RM)"
        )

        st.plotly_chart(
            fig_box,
            use_container_width=True
        )

    with tab3:

        scatter_df = stats["data"].copy()

        scatter_df = scatter_df.dropna(
            subset=["Size_Num"]
        )

        if not scatter_df.empty:

            fig_scatter = px.scatter(
                scatter_df,
                x="Size_Num",
                y="Price_Num",
                color="Bedroom",
                hover_name="Title",
                hover_data=[
                    "Bathroom",
                    "Parking",
                    "Available"
                ],
                title="Price vs Property Size"
            )

            fig_scatter.update_layout(
                xaxis_title="Size (sq.ft)",
                yaxis_title="Price (RM)"
            )

            st.plotly_chart(
                fig_scatter,
                use_container_width=True
            )

        else:

            st.info("Size data tidak tersedia.")
    st.divider()

    # ==========================
    # Unit Listings
    # ==========================

    st.subheader("🏠 Unit Listings")

    display_df = stats["data"].copy()

    column_order = [
        "Title",
        "Price",
        "Size",
        "Bedroom",
        "Bathroom",
        "Parking",
        "Available",
        "Link"
    ]

    display_df = display_df[
        [
            col for col in column_order
            if col in display_df.columns
        ]
    ]

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )

    st.success("Analysis completed successfully.")