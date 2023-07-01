import streamlit as st
import pandas as pd

def authent(username, password):
    df_user = pd.read_csv('data/user.csv')
    if username == df_user['nama'][0] and password ==str(df_user['password'][0]):
        return True
    return False
def main():

    st.sidebar.subheader('Login Menu')

    st.title("Web Analisis Tingkat Kepuasan Pelanggan")
    username = st.sidebar.text_input("User Name")
    password = st.sidebar.text_input("Password",type='password')
    if st.sidebar.checkbox("Login") :
        # create_usertable()
        # hashed_pswd = make_hashes(password)

        result = authent(username,password)
        if result:
            st.success("Logged In as {}".format(username))
            import home
            home.app()
        else:
            st.warning("Incorrect Username/Password")
            

if __name__ == '__main__':
	main()