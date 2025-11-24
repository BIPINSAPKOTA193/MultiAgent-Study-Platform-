"""Streamlit UI for Multi-Agent Learning Platform"""

import streamlit as st
import os
import tempfile
from pathlib import Path
from typing import Dict, Any, Optional
import json
import random
import html

# Add parent directory to path for imports
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.agents.manager_agent import ManagerAgent
from src.core.messages import ContentType, LearningMode
from src.core.logger import logger
from src.core.memory import load_state


# Page configuration
st.set_page_config(
    page_title="Multi-Agent Learning Platform",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.username = None
