import streamlit as st
from World_map import world_map
from World_map import country_map


# Start Streamlit app
def main():
    """Main function to run the Streamlit app."""
    st.set_page_config(
        page_title="Test App",
        layout="wide"
    )


if __name__ == "__main__":
    # Run the main function to start the Streamlit app
    main()
    # Run the world map and country map functions
    world_map()
    country_map()
