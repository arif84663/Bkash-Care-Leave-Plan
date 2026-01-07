import streamlit as st
import pandas as pd
from datetime import date

# অ্যাপের টাইটেল
st.set_page_config(page_title="Employee Leave Portal", layout="wide")
st.title("💼 এমপ্লয়ী ম্যানেজমেন্ট ও লিভ সিস্টেম")

# ডামি ডাটাবেজ (বাস্তবে এটি CSV বা SQL ডাটাবেজে থাকবে)
if 'employees' not in st.session_state:
    st.session_state.employees = {
        "E001": {"name": "আরিফ রহমান", "post": "ম্যানেজার", "leaves_left": 15},
        "E002": {"name": "সারা ইসলাম", "post": "ডেভেলপার", "leaves_left": 12}
    }

if 'leave_requests' not in st.session_state:
    st.session_state.leave_requests = []

# সাইডবার মেনু
menu = ["প্রোফাইল দেখা", "ছুটির আবেদন", "অ্যাডমিন প্যানেল"]
choice = st.sidebar.selectbox("মেনু সিলেক্ট করুন", menu)

# ১. প্রোফাইল সেকশন
if choice == "প্রোফাইল দেখা":
    st.subheader("আপনার তথ্য যাচাই করুন")
    emp_id = st.text_input("আপনার এমপ্লয়ী আইডি দিন (যেমন: E001)")
    if emp_id in st.session_state.employees:
        user = st.session_state.employees[emp_id]
        st.write(f"**নাম:** {user['name']}")
        st.write(f"**পদবী:** {user['post']}")
        st.write(f"**অবশিষ্ট ছুটি:** {user['leaves_left']} দিন")
    elif emp_id:
        st.error("আইডি পাওয়া যায়নি!")

# ২. ছুটির আবেদন সেকশন
elif choice == "ছুটির আবেদন":
    st.subheader("ছুটির জন্য আবেদন ফর্ম")
    with st.form("leave_form"):
        emp_id = st.text_input("এমপ্লয়ী আইডি")
        leave_type = st.selectbox("ছুটির ধরন", ["অসুস্থতা (Sick)", "ব্যক্তিগত (Casual)", "অন্যান্য"])
        start_date = st.date_input("কবে থেকে", date.today())
        end_date = st.date_input("কবে পর্যন্ত", date.today())
        reason = st.text_area("কারণ লিখুন")
        
        submitted = st.form_submit_button("আবেদন জমা দিন")
        if submitted:
            if emp_id in st.session_state.employees:
                st.session_state.leave_requests.append({
                    "ID": emp_id, "Type": leave_type, 
                    "Start": start_date, "End": end_date, "Status": "Pending"
                })
                st.success("আপনার আবেদনটি সফলভাবে জমা হয়েছে!")
            else:
                st.error("সঠিক আইডি দিন!")

# ৩. অ্যাডমিন প্যানেল
elif choice == "অ্যাডমিন প্যানেল":
    st.subheader("আবেদনসমূহ পর্যালোচনা (Admin Only)")
    if st.session_state.leave_requests:
        df = pd.DataFrame(st.session_state.leave_requests)
        st.table(df)
    else:
        st.info("কোনো আবেদন জমা পড়েনি।"
