import streamlit as st
import datetime
from update_database import store_missing_data
from db_sync import push_db_to_github

def show_missing_form(dining_hall, meal, dish_ids):
    """Given some data from the menu table, display form
    to save data to the database.
    """
    st.markdown("### 📝 Submit Missing Items")

    with st.form("missing_form"):
        default_name = st.session_state.get("username", "")
        username = st.text_input("Your name or initials:", value=default_name)
        comment = st.text_area("Any comments or notes (optional):", height=100)
        submit = st.form_submit_button("💾 Save")

        if submit:
            if not username:
                st.warning("Please enter your name or initials.")
                return

            missing_ids = [
                dish_id for dish_id in dish_ids
                if st.session_state.get(f"check_{meal}_{dish_id}", False)
            ]

            if not missing_ids:
                st.info("No items were marked as missing.")
                return

            today = datetime.date.today().isoformat()
            store_missing_data(
                missing_dish_ids=missing_ids,
                date=today,
                dining_hall=dining_hall,
                meal=meal,
                comment=comment,
                username=username
            )
            st.success(f"✅ Saved {len(missing_ids)} missing items. Thanks, {username}!")

            # Need to send our database to Github private repo
            push_db_to_github()