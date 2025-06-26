import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import math

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

# --- Streamlit UI ---
st.set_page_config(page_title="Black-Scholes Pricing Tool", layout="wide")
st.title("📈 Black-Scholes Option Pricing Tool")

st.sidebar.header("Input Parameters")

S = st.sidebar.number_input("Spot Price (S)", value=100.0)
K = st.sidebar.number_input("Strike Price (K)", value=100.0)
T = st.sidebar.number_input("Time to Expiry (T, in years)", value=1.0)
r = st.sidebar.number_input("Risk-Free Rate (r)", value=0.05)
sigma = st.sidebar.number_input("Volatility (σ)", value=0.2)

if st.button("📊 Calculate Option Prices"):
    call, d1, d2 = black_scholes_call(S, K, T, r, sigma)
    put = black_scholes_put(S, K, T, r, sigma)

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

# --- Heatmap ---
st.subheader("🗺️ Heatmap: Call Option Price vs Strike & Volatility")

K_min = st.slider("Min Strike", 50, 150, 80)
K_max = st.slider("Max Strike", 100, 200, 120)
sigma_min = st.slider("Min Volatility (%)", 1, 100, 10)
sigma_max = st.slider("Max Volatility (%)", 10, 300, 60)

K_vals = np.linspace(K_min, K_max, 50)
sigma_vals = np.linspace(sigma_min / 100, sigma_max / 100, 50)
K_grid, sigma_grid = np.meshgrid(K_vals, sigma_vals)

call_prices, _, _ = black_scholes_call(S, K_grid, T, r, sigma_grid)

fig, ax = plt.subplots(figsize=(10, 6))
heatmap = ax.contourf(K_grid, sigma_grid * 100, call_prices, cmap='plasma')
cbar = plt.colorbar(heatmap)
cbar.set_label("Call Price (₹)")

ax.set_xlabel("Strike Price (K)")
ax.set_ylabel("Volatility (%)")
ax.set_title("Call Option Price Heatmap")

st.pyplot(fig)
