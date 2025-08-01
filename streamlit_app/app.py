import streamlit as st
import sys
import os
import yaml
from pathlib import Path

# Add the src directory to the Python path
src_path = str(Path(__file__).parent.parent / "src")
if src_path not in sys.path:
    sys.path.insert(0, src_path)

try:
    from nifi_nl_builder.crew import NiFiNLCrew
except ImportError as e:
    st.error(f"Failed to import NiFiNLCrew: {e}")
    st.error(f"Python path: {sys.path}")
    st.stop()

# Page configuration
st.set_page_config(
    page_title="NiFi NL Builder",
    page_icon="🔄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
def load_css():
    css_path = Path(__file__).parent / "ui.css"
    try:
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning(f"CSS file not found at {css_path}. Using default styling.")
    except Exception as e:
        st.warning(f"Error loading CSS: {e}. Using default styling.")

load_css()

# Initialize session state
if 'crew_manager' not in st.session_state:
    st.session_state.crew_manager = None
if 'execution_history' not in st.session_state:
    st.session_state.execution_history = []

def initialize_crew():
    """Initialize the NiFi NL Builder crew"""
    try:
        if st.session_state.crew_manager is None:
            st.session_state.crew_manager = NiFiNLCrew()
            st.success("Crew initialized successfully!")
        return True
    except FileNotFoundError as e:
        st.error(f"Configuration file not found: {str(e)}")
        st.info("Please ensure agents.yaml and tasks.yaml exist in src/nifi_nl_builder/config/")
        return False
    except yaml.YAMLError as e:
        st.error(f"YAML configuration error: {str(e)}")
        st.info("Please check the format of your YAML configuration files")
        return False
    except Exception as e:
        st.error(f"Failed to initialize crew: {str(e)}")
        st.info("Please check your environment variables and dependencies")
        return False

def main():
    # Header
    st.title("🔄 NiFi NL Builder")
    st.markdown("Transform natural language descriptions into Apache NiFi flows")
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Environment variables
        st.subheader("Environment")
        nifi_url = st.text_input(
            "NiFi URL", 
            value=os.getenv("NIFI_URL", "https://nifi-dev:9090"),
            help="NiFi instance URL"
        )
        nifi_token = st.text_input(
            "NiFi Token", 
            value=os.getenv("NIFI_TOKEN", ""),
            type="password",
            help="Optional authentication token"
        )
        
        # Model settings
        st.subheader("Model Settings")
        model_choice = st.selectbox(
            "Primary Model",
            ["gpt-4o", "gpt-4o-mini", "gpt-3.5-turbo"],
            index=0
        )
        
        temperature = st.slider(
            "Temperature",
            min_value=0.0,
            max_value=1.0,
            value=0.2,
            step=0.1,
            help="Controls randomness in responses"
        )
        
        # Initialize button
        if st.button("🔄 Initialize Crew", type="primary"):
            with st.spinner("Initializing NiFi NL Builder crew..."):
                initialize_crew()
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("📝 Flow Description")
        
        # Text area for natural language description
        description = st.text_area(
            "Describe your NiFi flow in natural language:",
            height=200,
            placeholder="Example: Create a flow that reads from Kafka topic 'input-data', filters records with status 'active', transforms the data to JSON format, and writes to HDFS path '/data/processed'",
            help="Be as detailed as possible about sources, transformations, and destinations"
        )
        
        # Advanced options
        with st.expander("🔧 Advanced Options"):
            col_a, col_b = st.columns(2)
            
            with col_a:
                auto_deploy = st.checkbox("Auto-deploy flow", value=False)
                save_template = st.checkbox("Save as template", value=True)
                
            with col_b:
                flow_name = st.text_input("Flow Name", value="Generated Flow")
                priority = st.selectbox("Priority", ["Low", "Medium", "High"], index=1)
        
        # Execute button
        if st.button("🚀 Generate & Deploy Flow", type="primary", disabled=not description.strip()):
            if not st.session_state.crew_manager:
                st.error("Please initialize the crew first!")
                return
            
            with st.spinner("Processing your request..."):
                try:
                    # Execute the crew
                    result = st.session_state.crew_manager.run(description)
                    
                    # Store in history
                    st.session_state.execution_history.append({
                        "description": description,
                        "result": result,
                        "timestamp": st.session_state.get("timestamp", "Now")
                    })
                    
                    st.success("Flow generated successfully!")
                    
                except Exception as e:
                    st.error(f"Error generating flow: {str(e)}")
    
    with col2:
        st.header("📊 Status")
        
        # Crew status
        if st.session_state.crew_manager:
            st.success("✅ Crew Ready")
        else:
            st.warning("⚠️ Crew Not Initialized")
        
        # Recent executions
        st.subheader("Recent Executions")
        if st.session_state.execution_history:
            for i, execution in enumerate(reversed(st.session_state.execution_history[-5:])):
                with st.expander(f"Execution {len(st.session_state.execution_history) - i}"):
                    st.text_area(
                        "Description",
                        execution["description"],
                        height=100,
                        disabled=True
                    )
                    st.text_area(
                        "Result",
                        str(execution["result"]),
                        height=150,
                        disabled=True
                    )
        else:
            st.info("No executions yet")
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666;'>
            <p>NiFi NL Builder - Transform natural language into Apache NiFi flows</p>
            <p>Built with CrewAI and Streamlit</p>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main() 