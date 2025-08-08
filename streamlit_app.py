# Streamlit Cloud entry point
import sys
import os

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import and run the dashboard
from dashboard import main

# Always run main() for Streamlit Cloud (no __name__ check needed)
main()