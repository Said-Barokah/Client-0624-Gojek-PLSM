mkdir -p ~/.streamlit/
echo "\
[general]\n\
email = \"your-email@domain.com\"\n\
" > ~/.streamlit/credentials.toml
echo "\
[server]\n\
headless = true\n\
port = $PORT\n\
enableCORS = false\n\
\n\
[theme]\n\
primaryColor=\"#F63366\"\n\
backgroundColor=\"#FFFFFF\"\n\
secondaryBackgroundColor=\"#F0F2F6\"\n\
textColor=\"#262730\"\n\
font=\"sans serif\"\n\
\n\
[logger]\n\
level=\"error\"\n\
\n\
[global]\n\
inferArrowTypes = false\n\
" > ~/.streamlit/config.toml
echo "python-3.8.0" >> ~/.streamlit/requirements.txt
