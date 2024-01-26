import streamlit as st
import pandas as pd
import plotly.express as px
import math

st.title("Mortgage Calculator")

st.write("### Input Data")
col1, col2 = st.columns(2)
home_value = col1.number_input("Home Value", min_value=0, value=200000)
deposit = col1.number_input("Deposit", min_value=0, value=50000)
interest_rate = col2.number_input("Interest Rate (in %)", min_value=0.0, value=5.5)
loan_term = col2.number_input("Loan Term (in years)", min_value=1, value=30)

# Calculate the repayments
loan_amount = home_value - deposit
monthly_interest_rate = (interest_rate / 100) / 12
number_of_payments = loan_term * 12
monthly_payment = (
    loan_amount
    * (monthly_interest_rate * (1 + monthly_interest_rate) ** number_of_payments)
    / ((1 + monthly_interest_rate) ** number_of_payments - 1)
)

# Display the repayments
total_payments = monthly_payment * number_of_payments
total_interest = total_payments - loan_amount

st.write("### Repayments")
col1, col2, col3 = st.columns(3)
col1.metric(label="Monthly Repayments", value=f"${monthly_payment:,.2f}")
col2.metric(label="Total Repayments", value=f"${total_payments:,.0f}")
col3.metric(label="Total Interest", value=f"${total_interest:,.0f}")

# Data-frame with the payment schedule
schedule = []
remaining_balance = loan_amount

for i in range(1, number_of_payments + 1):
    interest_payment = remaining_balance * monthly_interest_rate
    principal_payment = monthly_payment - interest_payment
    remaining_balance -= principal_payment
    year = math.ceil(i / 12)  
    schedule.append(
        [
            i,
            monthly_payment,
            principal_payment,
            interest_payment,
            remaining_balance,
            year,
        ]
    )

df = pd.DataFrame(
    schedule,
    columns=["Month", "Payment", "Principal", "Interest", "Remaining Balance", "Year"],
)

# Data-frame as  chart
st.write("### Payment Schedule")
payments_df = df[["Year", "Remaining Balance"]].groupby("Year").min()

fig = px.line(payments_df, x=payments_df.index, y="Remaining Balance", title="Remaining Balance Over Time")
st.plotly_chart(fig)

# Interest vs Principal Over Time
fig2 = px.area(df, x="Month", y=["Principal", "Interest"], title="Interest vs Principal Over Time",
               labels={"value": "Amount", "variable": "Type"})
st.plotly_chart(fig2)

# Cumulative Interest Over Time
df['Cumulative Interest'] = df['Interest'].cumsum()
fig3 = px.line(df, x="Month", y="Cumulative Interest", title="Cumulative Interest Over Time")
st.plotly_chart(fig3)

# Monthly Payment Breakdown (selected month)
selected_month = st.selectbox("Select Month for Payment Breakdown", df['Month'], index=0)
selected_payment = df[df['Month'] == selected_month]

# bar chart
payment_data = {
    'Payment Type': ['Principal', 'Interest'],
    'Amount': [selected_payment['Principal'].values[0], selected_payment['Interest'].values[0]]
}

payment_df = pd.DataFrame(payment_data)
fig4 = px.bar(payment_df, x='Payment Type', y='Amount', 
              title=f"Payment Breakdown for Month {selected_month}",
              labels={'y': 'Amount'})
st.plotly_chart(fig4)