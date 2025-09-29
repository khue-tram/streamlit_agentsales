import streamlit as st
import os
import csv

# --- Title ---
st.title("📁 Sales CSV Uploader")
st.markdown("Upload your monthly sales file and save it with a standardized name format.")

# --- Inputs ---
uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])
year = st.number_input("Enter Year (YYYY)", min_value=2000, max_value=2100, step=1)
month = st.number_input("Enter Month (MM)", min_value=1, max_value=12, step=1)

# --- Save Logic ---
if st.button("Save File"):
    if uploaded_file and year and month:
        # Format filename
        filename = f"Sales{year}{month:02d}.csv"
        sales_folder = "sales"
        save_path = os.path.join(sales_folder, filename)

        # Ensure folder exists
        os.makedirs(sales_folder, exist_ok=True)

        # Save file (overwrite if exists)
        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.success(f"✅ File saved as `{filename}` in `{sales_folder}` folder.")
        st.info("Existing file for the same month (if any) was overwritten.")
    else:
        st.warning("Please upload a file and enter both year and month.")

# --- Month Name Mapping --- I added this part from Khue_c3p3.py as AI suggested
month_names = {
    "01": "Jan", "02": "Feb", "03": "Mar", "04": "Apr",
    "05": "May", "06": "Jun", "07": "Jul", "08": "Aug",
    "09": "Sep", "10": "Oct", "11": "Nov", "12": "Dec"
}
months = list(month_names.keys()) #list of months with leading zeros

# Initialize summary 
def sales_summary(year):
    summary = {}    
    data_folder = "sales"
       
    # Loop through the files in the sales folder
    if os.path.exists(data_folder):
        for file in os.listdir(data_folder):
            if file.startswith(f"Sales{year}") and file.endswith(".csv"):
                basename, _ = os.path.splitext(file)
                month = basename[-2:]                              
                with open(os.path.join(data_folder, file), mode='r') as f:
                    reader = csv.reader(f)                    
                    for row in reader:
                        day, agent, amount = row
                        amount = float(amount)

                        if agent not in summary:
                            summary[agent] = {month: 0 for month in months}
                        
                        summary[agent][month] += amount               
    else:
        return {}
    return summary

# --- Sales Summary Section ---
st.header("📊 Agent Sales Summary for the Year")

# --- Display Table ---
st.subheader(f"🧮 Sales Totals for {year}")

summary = sales_summary(year)
if summary:    
    months = [f"{i:02d}" for i in range(1, 13)]
    sale = []
    for agent, sales in summary.items():
        row = {"Agent": agent}
        for month in months:
            month_name = month_names[month]
            amount = f"{sales.get(month, 0):,.2f}"
            row[month_name] = amount            
        row["Total"] = f"{sum(sales.values()):,.2f}"
        sale.append(row)
    
    # Calculate and append the grand total row
    total_row = {"Agent": "Total"}
    for month in months:
        month_name = month_names[month]
        total_amount = sum(float(sales.get(month, 0)) for sales in summary.values())
        total_row[month_name] = f"{total_amount:,.2f}"
    total_row["Total"] = f"{sum(float(sales.get(month, 0)) for sales in summary.values() for month in months):,.2f}"
    # the grand total is the sum of all monthly totals across all agents
    sale.append(total_row)

    st.table(sale) #display the table with agent names and sales for each month
else:
    st.info(f"No sales data found for the year {year}.") #if no data found for the given year
    
