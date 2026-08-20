import streamlit as st

EMISSION_FACTOR = 0.82  # kg CO2 per kWh (India)

st.set_page_config(page_title="IoT Carbon Footprint Calculator")

st.title("🌱 IoT Device Carbon Footprint Calculator")
st.write("Select a device, power category, and usage hours.")

device = st.selectbox(
    "Select IoT Device",
    ["Smart Light Bulb", "Fan", "Refrigerator"]
)

power_options = {
    "Smart Light Bulb": [5, 9, 10, 15],
    "Fan": [50, 60, 75, 90],
    "Refrigerator": [100, 150, 200, 250]
}

power = st.selectbox("Select Power (Watts)", power_options[device])

if device == "Refrigerator":
    hours = st.slider("Compressor Running Hours per Day", 1, 24, 8)
else:
    hours = st.slider("Hours Used per Day", 1, 24, 5)

def get_recommendations(device, power, hours, daily_co2, monthly_co2):
    recs = []

    # 1) Intensity label based on monthly CO2
    if monthly_co2 < 2:
        label = "Low"
        headline = "✅ Your emissions are low."
    elif monthly_co2 < 8:
        label = "Medium"
        headline = "⚠️ Your emissions are moderate."
    else:
        label = "High"
        headline = "🚨 Your emissions are high."

    # 2) General tips (based on label)
    if label == "Low":
        recs += [
            "Keep using timers/automation to avoid unnecessary usage.",
            "Turn the device off when not needed."
        ]
    elif label == "Medium":
        recs += [
            "Reduce usage by 1–2 hours/day if possible.",
            "Use scheduling (timer) and motion/occupancy automation."
        ]
    else:  # High
        recs += [
            "Try cutting usage by 2–4 hours/day (big impact).",
            "Choose a lower watt option or more efficient model.",
            "Enable automation (schedules, eco mode, occupancy control)."
        ]

    # 3) Device-specific tips
    if device == "Smart Light Bulb":
        recs += [
            "Use motion sensors in corridors/bathrooms.",
            "Prefer lower watt bulbs or use dimming during nighttime."
        ]
    elif device == "Fan":
        recs += [
            "Use a BLDC fan (typically more energy efficient).",
            "Clean fan blades regularly to maintain efficiency.",
            "Use a higher speed only when needed."
        ]
    elif device == "Refrigerator":
        recs += [
            "Set temperature to efficient levels (avoid extra-cold settings).",
            "Ensure door seals are tight and avoid frequent opening.",
            "Keep ventilation space behind the fridge; clean condenser coils."
        ]

    # 4) “What if” quick saving suggestion
    # (estimate saving if user reduces 1 hour/day)
    saved_energy = (power / 1000) * 1
    saved_monthly = saved_energy * EMISSION_FACTOR * 30
    recs.append(f"Reducing usage by **1 hour/day** can save about **{saved_monthly:.2f} kg CO₂/month**.")

    return headline, recs

if st.button("Calculate"):
    energy = (power / 1000) * hours
    daily_co2 = energy * EMISSION_FACTOR
    monthly_co2 = daily_co2 * 30

    st.success("✅ Calculation Successful")

    st.write(f"**Device:** {device}")
    st.write(f"**Power:** {power} W")
    st.write(f"**Usage:** {hours} hours/day")
    st.write(f"**Energy Used:** {energy:.3f} kWh/day")
    st.write(f"**Daily CO₂ Emission:** {daily_co2:.3f} kg")
    st.write(f"**Monthly CO₂ Emission:** {monthly_co2:.2f} kg")

    # ✅ Recommendations section
    st.subheader("💡 Recommendations")
    headline, recs = get_recommendations(device, power, hours, daily_co2, monthly_co2)
    st.info(headline)
    for r in recs:
        st.write("•", r)
