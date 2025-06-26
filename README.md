## 📈 Black-Scholes Option Pricing App

This is a **Streamlit-powered web application** that calculates the fair value of European **Call** and **Put** options using the **Black-Scholes-Merton model**. It also visualizes the results and Greeks through **interactive heatmaps**.

---

## 🧠 What It Does

- ✅ Calculates *Call* and *Put* prices using Black-Scholes formula
- ✅ Computes all major **Greeks**: Delta, Gamma, Vega, Theta, and Rho
- ✅ Visualizes how prices change with **strike price** and **volatility**
- ✅ Offers an intuitive interface with user inputs and live plots

---

📊 The Black-Scholes Formula

##Call Option:
Call Price (C) = Spot Price × Φ(d₁) − Strike Price × e^(-r × T) × Φ(d₂)

## Put Option:
Put Price (P) = Strike Price × e^(-r × T) × Φ(-d₂) − Spot Price × Φ(-d₁)

ℹ️ Where the terms mean:
Spot Price (S) – The current market price of the asset

Strike Price (K) – The price at which the option can be exercised

T – Time to expiration (in years)

r – Annual risk-free interest rate (e.g., government bond yield)

σ (sigma) – Volatility of the asset (standard deviation of returns)

Φ(x) – Cumulative distribution function of the standard normal distribution

e – Euler’s number (≈ 2.71828)


---

 🚀 How to Run Locally

1. Clone this repository
git clone https://github.com/yourusername/Black_ScholesPricingModel.git

 cd black-scholes-pricing-model

3. Install dependencies
pip install -r requirements.txt

4. Run the app
streamlit run streamlit_app.py
