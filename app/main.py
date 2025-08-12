import streamlit as st

try:
    from app.World_map import world_map
    from app.World_map import country_map
except:
    from World_map import world_map
    from World_map import country_map


# Start Streamlit app
def main():
    """Main function to run the Streamlit app."""
    st.set_page_config(
        page_title="Test App",
        layout="wide"
    )


# run all functions
def run_main():
    # Run the main function to start the Streamlit app
    main()
    # Run the world map and country map functions
    world_map()
    country_map()


if __name__ == "__main__":
    run_main()
