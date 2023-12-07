import streamlit as st
import streamlit_authenticator as stauth
from pathlib import Path
import pickle
import json
from streamlit.source_util import _on_pages_changed, get_pages
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(
    page_title="佑能科技-拋光工具",
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
    # --- USER AUTHENTICATION ---

    names = ["Siri", "Admin"]
    usernames = ["siri", "admin"]

    # load hashed passwords
    file_path = Path(__file__).parent / "hashed_pw.pkl"
    with file_path.open("rb") as file:
        hashed_passwords = pickle.load(file)

    credentials = {"usernames":{}}
    for uname,name,pwd in zip(usernames,names,hashed_passwords):
        user_dict = {"name": name, "password": pwd}
        credentials["usernames"].update({uname: user_dict})
        
    authenticator = stauth.Authenticate(credentials, 'pt-userinfo', 'random_key', cookie_expiry_days=30)

    name, authentication_status, username = authenticator.login("Login", "main")


    if authentication_status == False:
        st.error("Username/password is incorrect")
        clear_all_but_first_page()  # clear all page but show first page

    if authentication_status == None:
        st.warning("Please enter your username and password")
        clear_all_but_first_page()  # clear all page but show first page

    if authentication_status:
        show_all_pages()  # call all page
        # hide_page(DEFAULT_PAGE.replace(".py", ""))  # hide first page
        st.title(f"嗨! {name}👋")
        st.write("")
        st.markdown(
            """
            #### 這是佑能科技的拋光計算機套件    
        """
        )
        st.write("")
        st.write("")
        st.write("")
        authenticator.logout('登出', 'main')
        # switch_page(SECOND_PAGE_NAME)   # switch to second page
        # st.stop()
    
    
if __name__ == "__main__":
    main()