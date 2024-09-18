# import streamlit as st

# # Streamlit app layout
# st.title("GST Calculator")

# # Option to choose if the amount is including or excluding GST
# gst_option = st.radio("Select an option:", ('Excluding GST', 'Including GST'))

# # Slider for the total amount
# amount = st.slider("Total amount", min_value=100, max_value=100000, value=5000, step=100)

# # Dropdown for selecting GST rate
# gst_rate = st.selectbox("Tax slab", (0.25, 1, 3, 5, 12, 18, 28))

# # Calculating GST based on the selection
# if gst_option == 'Excluding GST':
#     gst_amount = (amount * gst_rate) / 100
#     post_gst_amount = amount + gst_amount
# else:
#     gst_amount = amount - (amount * (100 / (100 + gst_rate)))
#     post_gst_amount = amount

# # Displaying the calculated GST and the total amount post-GST
# st.write(f"**Total GST:** ₹{gst_amount:,.0f}")
# st.write(f"**Post-GST amount:** ₹{post_gst_amount:,.0f}")
import streamlit as st
from babel.numbers import format_currency, format_number
import matplotlib.pyplot as plt

# Utility functions
def format_currency_without_fraction(amount, currency_symbol='₹', locale='en_IN'):
    amount_int = int(amount)
    return f"{currency_symbol}{format_number(amount_int, locale=locale)}"

# EMI Calculator Functions
def calculate_emi(principal, rate, tenure):
    monthly_rate = rate / (12 * 100)
    emi = principal * monthly_rate * ((1 + monthly_rate) ** (tenure * 12)) / (((1 + monthly_rate) ** (tenure * 12)) - 1)
    return emi

def calculate_total_interest(principal, emi, tenure):
    total_payment = emi * tenure * 12
    total_interest = total_payment - principal
    return total_interest, total_payment

def plot_emi_pie_chart(principal, total_interest):
    labels = ['Principal Amount', 'Interest Amount']
    sizes = [principal, total_interest]
    colors = ['#AED6F1', '#5DADE2']
    explode = (0.1, 0)
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
    ax.axis('equal')
    return fig

# GST Calculator Functions
def calculate_gst(gst_option, amount, gst_rate):
    if gst_option == 'Excluding GST':
        gst_amount = (amount * gst_rate) / 100
        post_gst_amount = amount + gst_amount
    else:
        gst_amount = amount - (amount * (100 / (100 + gst_rate)))
        post_gst_amount = amount
    return gst_amount, post_gst_amount

# Mutual Fund Calculator Functions
def calculate_returns(principal, rate_of_return, time_period):
    future_value = principal * ((1 + (rate_of_return / 100)) ** time_period)
    est_returns = future_value - principal
    return future_value, est_returns

def plot_mf_pie_chart(total_investment, est_returns):
    labels = ['Invested Amount', 'Estimated Returns']
    sizes = [total_investment, est_returns]
    colors = ['#ADD8E6', '#4169E1']
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    return fig

# SIP Calculator Functions
def calculate_sip(monthly_investment, annual_return_rate, years):
    monthly_return_rate = annual_return_rate / 12 / 100
    num_months = years * 12
    future_value = 0
    for _ in range(num_months):
        future_value = (future_value + monthly_investment) * (1 + monthly_return_rate)
    total_invested = monthly_investment * num_months
    estimated_returns = future_value - total_invested
    return total_invested, estimated_returns, future_value

def plot_sip_pie_chart(total_invested, estimated_returns):
    labels = ['Total Invested', 'Estimated Returns']
    sizes = [total_invested, estimated_returns]
    colors = ['#ff9999', '#66b3ff']
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(sizes, labels=labels, colors=colors, autopct='%1.0f%%', startangle=140)
    ax.axis('equal')
    return fig

# SWP Calculator Functions
def calculate_swp(total_investment, withdrawal_per_month, return_rate, time_period):
    monthly_rate = return_rate / 12 / 100
    total_withdrawal = 0
    current_value = total_investment
    for month in range(int(time_period * 12)):
        current_value += current_value * monthly_rate
        current_value -= withdrawal_per_month
        total_withdrawal += withdrawal_per_month
        if current_value <= 0:
            break
    return current_value, total_withdrawal

# Main Streamlit App
def main():
    st.title("Financial Calculators")
    option = st.sidebar.selectbox("Choose a Calculator", 
                                  ("EMI Calculator", "GST Calculator", "Mutual Fund Calculator", "SIP Calculator", "SWP Calculator"))

    if option == "EMI Calculator":
        st.header("EMI Calculator")
        col1, col2 = st.columns([3, 2])

        with col1:
            principal = st.slider("Loan Amount (₹)", min_value=100000, max_value=10000000, value=1000000, step=50000, format="₹%d")
            monthly_investment = st.number_input("Monthly Investment (₹)", value=0, step=500)
            rate = st.slider("Rate of Interest (p.a.)", min_value=0.1, max_value=20.0, value=1.5, step=0.1, format="%1.1f%%")
            tenure = st.slider("Loan Tenure (Years)", min_value=1, max_value=30, value=4, step=1, format="%d years")
            emi = calculate_emi(principal, rate, tenure)
            total_interest, total_amount = calculate_total_interest(principal, emi, tenure)
            st.write("**EMI Calculator Results:**")
            st.write(f"Monthly EMI: {format_currency_without_fraction(emi)}")
            st.write(f"Principal Amount: {format_currency_without_fraction(principal)}")
            st.write(f"Total Interest: {format_currency_without_fraction(total_interest)}")
            st.write(f"Total Amount: {format_currency_without_fraction(total_amount)}")
        
        with col2:
            st.write("### Pie Chart")
            st.markdown("<br><br>", unsafe_allow_html=True)
            fig = plot_emi_pie_chart(principal, total_interest)
            st.pyplot(fig)

    elif option == "GST Calculator":
        st.header("GST Calculator")
        gst_option = st.radio("Select an option:", ('Excluding GST', 'Including GST'))
        amount = st.slider("Total amount", min_value=100, max_value=100000, value=5000, step=100)
        gst_rate = st.selectbox("Tax slab", (0.25, 1, 3, 5, 12, 18, 28))
        gst_amount, post_gst_amount = calculate_gst(gst_option, amount, gst_rate)
        st.write(f"**Total GST:** ₹{gst_amount:,.0f}")
        st.write(f"**Post-GST amount:** ₹{post_gst_amount:,.0f}")

    elif option == "Mutual Fund Calculator":
        st.header("Mutual Fund Return Calculator")
        col1, col2 = st.columns([3, 2])

        with col1:
            total_investment = st.slider("Total Investment (₹)", min_value=1000, max_value=1000000, value=25000, step=1000, format="₹%d")
            monthly_investment = st.number_input("Monthly Investment (₹)", value=0, step=500)
            expected_return_rate = st.slider("Expected Return Rate (p.a.)", min_value=0.0, max_value=15.0, value=5.4, step=0.1, format="%1.1f%%")
            time_period = st.slider("Time Period (Years)", min_value=1, max_value=30, value=6, format="%d years")
            total_value, est_returns = calculate_returns(total_investment, expected_return_rate, time_period)
            st.write("**Investment Calculator Results:**")
            st.write(f"Invested Amount: {format_currency_without_fraction(total_investment)}")
            st.write(f"Estimated Returns: {format_currency_without_fraction(est_returns)}")
            st.write(f"Total Value: {format_currency_without_fraction(total_value)}")
        
        with col2:
            st.write("### Pie Chart")
            st.markdown("<br><br>", unsafe_allow_html=True)
            fig = plot_mf_pie_chart(total_investment, est_returns)
            st.pyplot(fig)

    elif option == "SIP Calculator":
        st.header("SIP Calculator")
        col1, col2 = st.columns([3, 2])

        with col1:
            monthly_investment = st.slider("SIP Amount (₹)", min_value=500, max_value=100000, value=5000, format="₹%d")
            annual_return_rate = st.slider("Annual Return Rate (%)", min_value=1, max_value=30, value=12, format="%d%%")
            years = st.slider("Investment Period (Years)", min_value=1, max_value=50, value=10, format="%d years")
            st.number_input("Monthly Investment (₹)", value=monthly_investment, step=500)
            total_invested, estimated_returns, future_value = calculate_sip(monthly_investment, annual_return_rate, years)
            st.write("**SIP Calculator Results:**")
            st.write(f"Total Invested Amount: {format_currency_without_fraction(total_invested)}")
            st.write(f"Estimated Returns: {format_currency_without_fraction(estimated_returns)}")
            st.write(f"Total Value: {format_currency_without_fraction(future_value)}")
        
        with col2:
            st.write("### Pie Chart")
            st.markdown("<br><br>", unsafe_allow_html=True)
            fig = plot_sip_pie_chart(total_invested, estimated_returns)
            st.pyplot(fig)

    elif option == "SWP Calculator":
        st.header("SWP (Systematic Withdrawal Plan) Calculator")
        total_investment = st.slider("Total Investment (₹)", min_value=10000, max_value=1000000, value=120000, step=1000, format="₹%d")
        monthly_investment = st.number_input("Monthly Investment (₹)", value=0, step=500)
        withdrawal_per_month = st.slider("Withdrawal per Month (₹)", min_value=1000, max_value=50000, value=2500, step=500, format="₹%d")
        return_rate = st.slider("Expected Return Rate (p.a.)", min_value=0.0, max_value=15.0, value=2.3, step=0.1, format="%1.1f%%")
        time_period = st.slider("Time Period (Years)", min_value=1, max_value=30, value=2, format="%d years")
        final_value, total_withdrawal = calculate_swp(total_investment, withdrawal_per_month, return_rate, time_period)
        st.write(f"### Total Investment: {format_currency_without_fraction(total_investment)}")
        st.write(f"### Total Withdrawal: {format_currency_without_fraction(total_withdrawal)}")
        st.write(f"### Final Value: {format_currency_without_fraction(final_value)}")
        
        if final_value <= 0:
            st.write("### Warning: Your investment may be exhausted before the end of the time period.")

if __name__ == "__main__":
    main()
