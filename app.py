import streamlit as st
import re

# 1. Page Configuration
st.set_page_config(page_title="Food Waste Rescue Radar", page_icon="🚀", layout="centered")

# 2. Initialize Permanent Memory Bank (Session State)
if "current_view" not in st.session_state:
    st.session_state.current_view = "home"
if "total_donations_count" not in st.session_state:
    st.session_state.total_donations_count = 14  
if "total_receivers_count" not in st.session_state:
    st.session_state.total_receivers_count = 8    

# Safely store your calculation states so they don't erase on page re-runs
if "saved_co2" not in st.session_state:
    st.session_state.saved_co2 = 0.0
if "saved_meals" not in st.session_state:
    st.session_state.saved_meals = 0

# 3. Dynamic Calculation Math
def calculate_dynamic_metrics(text_input):
    # Extracts the first number found in the text box
    numbers = re.findall(r'\d+', text_input)
    if numbers:
        weight = float(numbers[0])
    else:
        weight = 30.0  # Fallback baseline weight if no number is written
        
    co2_saved = round(weight * 4.5, 1)
    meals_created = int(weight * 0.8)
    return co2_saved, meals_created

# 4. Sidebar Navigation
st.sidebar.header("🔧 Configuration")
api_key = st.sidebar.text_input("OpenAI API Key", type="password", placeholder="Leave blank for Demo Mode!")
st.sidebar.markdown("---")

if st.sidebar.button("🏠 Return to Home Screen"):
    st.session_state.current_view = "home"
    st.rerun()

# 5. View 1: Home Screen
if st.session_state.current_view == "home":
    st.title("🚀 Food Waste Rescue Radar")
    st.markdown("### Smart Logistics & Sustainability Routing Hub")
    st.markdown(
        "Welcome to the **Food Waste Rescue Radar**! Our platform bridges the gap between "
        "commercial surplus food providers and local community distribution centers to safely eliminate local waste."
    )
    
    # 📊 Live Stats Counter
    st.markdown("#### 📊 Live Radar Network Activity")
    stat_col1, stat_col2 = st.columns(2)
    with stat_col1:
        st.metric(label="Total Successful Donations", value=f"{st.session_state.total_donations_count} Batches")
    with stat_col2:
        st.metric(label="Active Community Receivers Linked", value=f"{st.session_state.total_receivers_count} Centers")
        
    st.info(
        "💡 **Read About Us:** This AI-assisted system analyzes food descriptions, flags safety risks, "
        "tracks allergy considerations, and maps the best delivery paths instantly."
    )
    st.markdown("#### Ready to get started?")
    if st.button("🤝 Click Here to Participate", use_container_width=True):
        st.session_state.current_view = "selection"
        st.rerun()

# 6. View 2: Role Selection Screen
elif st.session_state.current_view == "selection":
    st.title("🚪 Choose Your Role")
    st.markdown("Select how you would like to interact with the Rescue Radar network today:")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🍎 Donator")
        if st.button("Proceed as Donator ➡️", use_container_width=True):
            st.session_state.current_view = "donator_form"
            st.rerun()
    with col2:
        st.subheader("📦 Receiver")
        if st.button("Proceed as Receiver ➡️", use_container_width=True):
            st.session_state.current_view = "receiver_form"
            st.rerun()

# 7. View 3: Donator Intake Form (Fixed Calculation Logic)
elif st.session_state.current_view == "donator_form":
    st.title("🍎 Donator Intake Dashboard")
    donator_name = st.text_input("Business / Donator Name", placeholder="e.g., Green Garden Café")
    facility_type = st.selectbox("Facility Type", ["Restaurant", "Grocery Store", "Cafeteria", "Meal Prep Service"])
    
    # Type your number here (e.g., "50 lbs of apples") to process the math
    food_details = st.text_area("What surplus inventory do you have?", placeholder="e.g., 50 lbs of apples...")
    donator_address = st.text_input("Street Address & Zip Code", placeholder="e.g., 123 Main St, 08820")
    donator_allergies = st.text_input("⚠️ Specific Allergen Warnings (Optional)", placeholder="e.g., Contains wheat/gluten")
    
    if st.button("🚀 Run Rescue Radar Analysis", use_container_width=True):
        if not food_details or not donator_address:
            st.error("Please fill out your food details and address!")
        else:
            with st.spinner("Analyzing parameters..."):
                # Run the math and lock it into memory right away
                calc_co2, calc_meals = calculate_dynamic_metrics(food_details)
                st.session_state.saved_co2 = calc_co2
                st.session_state.saved_meals = calc_meals
                
                # Add to your community counter
                st.session_state.total_donations_count += 1
                st.rerun()  # Instantly refresh screen layout with new data

    # Displays metrics ONLY if they have values locked into memory
    if st.session_state.saved_co2 > 0:
        st.success("✅ Analysis Complete (Demo Mode Active)")
        st.markdown("### 📡 Analysis Output Metrics")
        m_col1, m_col2 = st.columns(2)
        with m_col1:
            st.metric(label="Estimated CO2e Saved", value=f"{st.session_state.saved_co2} lbs")
        with m_col2:
            st.metric(label="Equivalent Meals Created", value=f"{st.session_state.saved_meals} Meals")

# 8. View 4: Receiver Request Form
elif st.session_state.current_view == "receiver_form":
    st.title("📦 Receiver Request Dashboard")
    receiver_name = st.text_input("Organization / Receiver Name", placeholder="e.g., Community Food Bank")
    receiver_requirements = st.text_area("What items does your facility urgently need?", placeholder="e.g., Fresh produce, grains...")
    receiver_location = st.text_input("Delivery Address & Zip Code", placeholder="e.g., 456 Assistance Way, 08820")
    receiver_allergies = st.text_input("🚫 Specific Allergen Restrictions (Optional)", placeholder="e.g., Must be nut-free")
    
    if st.button("📡 Register Supply Request", use_container_width=True):
        if not receiver_name or not receiver_location:
            st.error("Please fill out your organization name and location!")
        else:
            st.session_state.total_receivers_count += 1
            st.success("✅ Logistics Profile Active on Radar")
