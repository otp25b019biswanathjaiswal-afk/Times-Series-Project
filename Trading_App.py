import streamlit as st

st.set_page_config(
    page_title = "Agri Trading Analyzer App",
    page_icon = "heavy_dollar_sign:",
    layout = "wide"
)

st.title("Trading Guide App :bar_chart:")

st.header("We provide the greatest platform for you to collect all information prior to investing in stocks.")

st.image("Gramdev Tech App.jpeg")

st.markdown("## We provide the following services:")

st.markdown("#### :one: Stock Information")
st.write("Through this page, you can see all information about stocks.")

st.markdown("#### :two: Stock Prediction")
st.write("You can explore predicted closing price for next 30 days based on historical stock data and adavanced forcasting models. Use this tool to gain valuable insights into market trends and make informed investment decisions")

st.markdown("#### :three: CAPM Return")
st.write("Discover how the Capital Asset Procing Model(CAPM) calculates the expected return of differen stocks asset based risk and market performance.")

st.markdown("#### :four: CAPM Beta")
st.write("Calcualated Beta and Expected Return for Individual Stocks.")
