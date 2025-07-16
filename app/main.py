import streamlit as st


# Start Streamlit app
def main():
    """Main function to run the Streamlit app."""
    st.set_page_config(
        page_title="Test App",
        layout="wide"
    )

    st.markdown('<br><br><br><br><br><br><br>',
                unsafe_allow_html=True)
    st.markdown(
        '<h1 style="font-size: 100px; text-align: center; color: #FFFFFF;">'
        'Hello</h1>',
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()