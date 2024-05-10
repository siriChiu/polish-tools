import streamlit as st
from pathlib import Path
import json
from streamlit.source_util import _on_pages_changed, get_pages
from st_pages import Page, show_pages, add_page_title
import hmac

st.set_page_config(
    page_title="佑能科技-工具箱",
    page_icon="🌟",
)

DEFAULT_PAGE = "polishing_main"
SECOND_PAGE_NAME = "Polishing_Calculator"

# all pages request
def get_all_pages():
    default_pages = get_pages(DEFAULT_PAGE)

    pages_path = Path("pages.json")

    if pages_path.exists():
        saved_default_pages = json.loads(pages_path.read_text())
    else:
        saved_default_pages = default_pages.copy()
        pages_path.write_text(json.dumps(default_pages, indent=4))

    return saved_default_pages

# clear all page but not login page
def clear_all_but_first_page():
    current_pages = get_pages(DEFAULT_PAGE)

    if len(current_pages.keys()) == 1:
        return

    get_all_pages()

    # Remove all but the first page
    key, val = list(current_pages.items())[0]
    current_pages.clear()
    current_pages[key] = val

    _on_pages_changed.send()

# show all pages
def show_all_pages():
    current_pages = get_pages(DEFAULT_PAGE)

    saved_pages = get_all_pages()

    # Replace all the missing pages
    for key in saved_pages:
        if key not in current_pages:
            current_pages[key] = saved_pages[key]

    _on_pages_changed.send()

# Hide default page
def hide_page(name: str):
    current_pages = get_pages(DEFAULT_PAGE)

    for key, val in current_pages.items():
        if val["page_name"] == name:
            del current_pages[key]
            _on_pages_changed.send()
            break

# calling only default(login) page  
clear_all_but_first_page()

def main():
        # Optional -- adds the title and icon to the current page
    add_page_title()

    # Specify what pages should be shown in the sidebar, and what their titles and icons
    # should be
    show_pages(
        [
            Page("polishing_main.py", "首頁", "🏠"),
            Page("pages/1_🛠️_Polishing_Calculator.py", "拋光計算機", "🛠️"),
        ]
    )
    
    # --- USER AUTHENTICATION ---
    def check_password():
        """Returns `True` if the user had a correct password."""

        def login_form():
            """Form with widgets to collect user information"""
            with st.form("Credentials"):
                st.text_input("帳號", key="username")
                st.text_input("密碼", type="password", key="password")
                st.form_submit_button("登入", on_click=password_entered)

        def password_entered():
            """Checks whether a password entered by the user is correct."""
            if st.session_state["username"] in st.secrets[
                "passwords"
            ] and hmac.compare_digest(
                st.session_state["password"],
                st.secrets.passwords[st.session_state["username"]],
            ):
                st.session_state["password_correct"] = True
                del st.session_state["password"]  # Don't store the username or password.
                del st.session_state["username"]
            else:
                st.session_state["password_correct"] = False

        # Return True if the username + password is validated.
        if st.session_state.get("password_correct", False):
            return True

        # Show inputs for username + password.
        login_form()
        if "password_correct" in st.session_state:
            st.error("😕 User not known or password incorrect")
        return False

    if not check_password():
        clear_all_but_first_page()  # clear all page but show first page
        st.stop()

    show_all_pages()  # call all page
    # hide_page(DEFAULT_PAGE.replace(".py", ""))  # hide first page
    st.title(f"嗨 歡迎光臨! 👋")
    st.write("")
    st.markdown(
        """
        #### 這是佑能科技的拋光計算機套件    
    """
    )
    st.write("")
    st.write("")
    st.write("")
    
    
if __name__ == "__main__":
    main()