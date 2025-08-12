import runpy
from unittest.mock import patch, MagicMock
import pytest
import app.main as main_module
from unittest.mock import patch
import app.main as main_module

def test_main():
    """Test that main() runs without raising exceptions."""
    with patch("streamlit.set_page_config") as mock_config:
        main_module.main()
        mock_config.assert_called_once_with(
            page_title="Test App",
            layout="wide"
        )


def test_run_all():
    with patch.object(main_module, "main") as mock_main, \
         patch.object(main_module, "world_map") as mock_world_map, \
         patch.object(main_module, "country_map") as mock_country_map:

        main_module.run_main()

        mock_main.assert_called_once()
        mock_world_map.assert_called_once()
        mock_country_map.assert_called_once()