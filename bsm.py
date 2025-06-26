import streamlit as st
import numpy as np
import matplotlib as plt
from scipy.stats import norm
import math
import streamlit as st
from PIL import Image

# --- Black-Scholes Call Option ---
def black_scholes_call(S, K, T, r, sigma):
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    call_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    return call_price, d1, d2

# --- Black-Scholes Put Option ---
def black_scholes_put(S, K, T, r, sigma):
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    put_price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    return put_price

# --- Option Greeks ---
def calculate_greeks(S, K, T, r, sigma):
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    delta_call = norm.cdf(d1)
    delta_put = norm.cdf(d1) - 1
    gamma = norm.pdf(d1) / (S * sigma * np.sqrt(T))
    vega = S * norm.pdf(d1) * np.sqrt(T) / 100
    theta_call = (-S * norm.pdf(d1) * sigma / (2 * np.sqrt(T)) - r * K * np.exp(-r * T) * norm.cdf(d2)) / 365
    theta_put = (-S * norm.pdf(d1) * sigma / (2 * np.sqrt(T)) + r * K * np.exp(-r * T) * norm.cdf(-d2)) / 365
    rho_call = K * T * np.exp(-r * T) * norm.cdf(d2) / 100
    rho_put = -K * T * np.exp(-r * T) * norm.cdf(-d2) / 100

    return {
        "Delta (Call)": delta_call,
        "Delta (Put)": delta_put,
        "Gamma": gamma,
        "Vega": vega,
        "Theta (Call)": theta_call,
        "Theta (Put)": theta_put,
        "Rho (Call)": rho_call,
        "Rho (Put)": rho_put,
    }

# --- Streamlit UI ---
st.set_page_config(page_title="Black-Scholes Pricing Tool", layout="wide")


# Title
st.title("Black-Scholes Option Pricing Model")

# Subtitle
st.subheader("📈 Formula Overview")

# Display image (ensure the image file is in the same directory)
try:
    image = Image.open("bsm.jpeg")
    st.image(image, caption="Black-Scholes Formula", use_container_width=True)
except FileNotFoundError:
    st.error("Image file 'black_scholes_formula.png' not found. Please add it to the project folder.")



st.sidebar.header("Input Parameters")

S = st.sidebar.number_input("Spot Price (S): Current stock price", value=100.0)
K = st.sidebar.number_input("Strike Price (K): Exercise price", value=100.0)
T = st.sidebar.number_input("Time to Expiry (T in years)", value=1.0)
r = st.sidebar.number_input("Risk-Free Rate (r): Annual interest rate", value=0.05)
sigma = st.sidebar.number_input("Volatility (σ): Annual standard deviation", value=0.2)

if st.button("📊 Calculate Option Prices"):
    call, d1, d2 = black_scholes_call(S, K, T, r, sigma)
    put = black_scholes_put(S, K, T, r, sigma)
    greeks = calculate_greeks(S, K, T, r, sigma)

    st.subheader("🔢 Option Pricing Results")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Call Option Price", f"₹{call:.2f}")
        st.metric("d₁", f"{d1:.4f}")
        st.metric("Φ(d₁)", f"{norm.cdf(d1):.4f}")
    with col2:
        st.metric("Put Option Price", f"₹{put:.2f}")
        st.metric("d₂", f"{d2:.4f}")
        st.metric("Φ(d₂)", f"{norm.cdf(d2):.4f}")

    st.subheader("📐 Greeks")
    for key, val in greeks.items():
        st.write(f"**{key}:** {val:.4f}")

# --- Heatmap Call Option ---
st.subheader("🗺️ Heatmap: Call Option Price vs Strike & Volatility")

K_min = st.slider("Min Strike", 50, 150, 80)
K_max = st.slider("Max Strike", 100, 200, 120)
sigma_min = st.slider("Min Volatility (%)", 1, 100, 10)
sigma_max = st.slider("Max Volatility (%)", 10, 300, 60)

K_vals = np.linspace(K_min, K_max, 50)
sigma_vals = np.linspace(sigma_min / 100, sigma_max / 100, 50)
K_grid, sigma_grid = np.meshgrid(K_vals, sigma_vals)

call_prices, _, _ = black_scholes_call(S, K_grid, T, r, sigma_grid)

fig1, ax1 = plt.subplots(figsize=(10, 6))
heatmap1 = ax1.contourf(K_grid, sigma_grid * 100, call_prices, cmap='plasma')
cbar1 = plt.colorbar(heatmap1)
cbar1.set_label("Call Price (₹)")

ax1.set_xlabel("Strike Price (K)")
ax1.set_ylabel("Volatility (%)")
ax1.set_title("Call Option Price Heatmap")

st.pyplot(fig1)

# --- Heatmap Put Option ---
st.subheader("🗺️ Heatmap: Put Option Price vs Strike & Volatility")

put_prices = black_scholes_put(S, K_grid, T, r, sigma_grid)

fig2, ax2 = plt.subplots(figsize=(10, 6))
heatmap2 = ax2.contourf(K_grid, sigma_grid * 100, put_prices, cmap='viridis')
cbar2 = plt.colorbar(heatmap2)
cbar2.set_label("Put Price (₹)")

ax2.set_xlabel("Strike Price (K)")
ax2.set_ylabel("Volatility (%)")
ax2.set_title("Put Option Price Heatmap")

st.pyplot(fig2)
