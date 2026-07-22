import streamlit as st
import plotly.express as px
import plotly.graph_objects as go


CHART_COLORS = ["#2DD4BF", "#F5A524", "#8B7CF6", "#FB7185", "#5EB3E4", "#34D399"]


def load_css(path="static/style.css"):
    with open(path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def render_kpi_card(icon, label, value, accent="#2DD4BF"):
    st.markdown(
        f"""
        <div class="kpi-card" style="--kpi-accent:{accent}">
            <div class="kpi-icon">{icon}</div>
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def _theme_figure(fig, height=360):
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", color="#EAF0F7", size=13),
        margin=dict(l=10, r=10, t=10, b=10),
        height=height,
        showlegend=False,
        hoverlabel=dict(
            bgcolor="#182338",
            font_color="#EAF0F7",
            font_family="Inter, sans-serif",
            bordercolor="#223049"
        ),
    )
    fig.update_xaxes(showgrid=False, color="#8798AE", linecolor="#223049")
    fig.update_yaxes(showgrid=True, gridcolor="#182338", color="#8798AE", zeroline=False)
    return fig


def bar_chart(series, horizontal=False, single_color=None):
    df = series.reset_index()
    df.columns = ["label", "value"]

    if single_color:
        colors = [single_color] * len(df)
    else:
        colors = [CHART_COLORS[i % len(CHART_COLORS)] for i in range(len(df))]

    if horizontal:
        fig = px.bar(df, x="value", y="label", orientation="h", text="value")
    else:
        fig = px.bar(df, x="label", y="value", text="value")

    fig.update_traces(
        marker_color=colors,
        marker_line_width=0,
        texttemplate="%{text:,.0f}",
        textposition="outside"
    )

    fig = _theme_figure(fig)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


def line_chart(series):
    df = series.reset_index()
    df.columns = ["label", "value"]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["label"], y=df["value"],
        mode="lines+markers",
        line=dict(color="#2DD4BF", width=3, shape="spline"),
        marker=dict(size=6, color="#2DD4BF"),
        fill="tozeroy",
        fillcolor="rgba(45,212,191,0.12)"
    ))

    fig = _theme_figure(fig)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


def scatter_chart(df, x, y):
    fig = px.scatter(df, x=x, y=y)
    fig.update_traces(marker=dict(size=8, color="#8B7CF6", opacity=0.75, line=dict(width=0)))

    fig = _theme_figure(fig)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})