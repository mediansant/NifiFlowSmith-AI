# NiFi NL Builder - Streamlit UI

A modern web interface for transforming natural language descriptions into Apache NiFi flows using CrewAI.

## 🚀 Features

- **Natural Language Processing**: Convert plain English descriptions into NiFi flows
- **Multi-Agent Workflow**: Four specialized agents working together
- **Real-time Configuration**: Adjust NiFi settings and model parameters
- **Execution History**: Track and review previous flow generations
- **Modern UI**: Clean, responsive interface with custom styling
- **Template Management**: Save and reuse flow templates

## 📋 Prerequisites

- Python 3.8+
- Apache NiFi instance running
- OpenAI API key configured
- Required Python packages installed

## 🛠️ Installation

1. **Clone the repository** (if not already done):
   ```bash
   git clone <repository-url>
   cd Nifiautomation
   ```

2. **Install dependencies**:
   ```bash
   uv pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   ```bash
   # Copy the example .env file
   cp .env.example .env
   
   # Edit with your actual values
   OPENAI_API_KEY=your_openai_api_key
   NIFI_URL=https://your-nifi-instance:9090
   NIFI_TOKEN=your_nifi_token  # Optional
   ```

## 🎯 Usage

### Starting the Application

**Option 1: Using the startup script (Recommended)**
```bash
python run_app.py
```

**Option 2: Direct Streamlit command**
```bash
cd streamlit_app
streamlit run app.py
```

**Option 3: From project root**
```bash
streamlit run streamlit_app/app.py
```

3. **Open your browser** and go to `http://localhost:8501`

### Using the Interface

1. **Initialize the Crew**:
   - Click "🔄 Initialize Crew" in the sidebar
   - Wait for the success message

2. **Configure Settings** (optional):
   - Set NiFi URL and token
   - Choose model and temperature
   - Adjust advanced options

3. **Describe Your Flow**:
   - Enter a natural language description
   - Be specific about sources, transformations, and destinations
   - Example: "Create a flow that reads from Kafka topic 'input-data', filters records with status 'active', transforms to JSON, and writes to HDFS"

4. **Generate and Deploy**:
   - Click "🚀 Generate & Deploy Flow"
   - Monitor the progress
   - Review the results

## 🏗️ Architecture

### Agent Workflow

1. **nl_parser**: Extracts structured requirements from natural language
2. **flow_planner**: Matches requirements to existing NiFi templates
3. **flow_builder**: Creates flow definitions using NiFi REST API
4. **cdf_deployer**: Deploys flows to Cloudera Data Flow

### UI Components

- **Sidebar**: Configuration and initialization controls
- **Main Area**: Flow description input and execution
- **Status Panel**: Real-time status and execution history
- **Advanced Options**: Template saving, auto-deployment settings

## 🎨 Customization

### Styling

The UI uses custom CSS (`ui.css`) for a modern look:
- Gradient buttons and backgrounds
- Smooth animations and transitions
- Responsive design for mobile devices
- Custom scrollbars and focus states

### Configuration

Modify `app.py` to:
- Add new model options
- Customize agent parameters
- Extend the UI with additional features
- Integrate with other services

## 🔧 Configuration Options

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key | Required |
| `NIFI_URL` | NiFi instance URL | `https://nifi-dev:9090` |
| `NIFI_TOKEN` | NiFi authentication token | Optional |
| `CDP_SERVICE_CRN` | Cloudera Data Platform service CRN | Required for deployment |
| `CDP_ENV_CRN` | Cloudera Data Platform environment CRN | Required for deployment |

### Model Settings

- **Primary Model**: Choose between GPT-4o, GPT-4o-mini, or GPT-3.5-turbo
- **Temperature**: Control randomness (0.0 = deterministic, 1.0 = creative)
- **Max Tokens**: Limit response length for cost control

## 📊 Monitoring

### Execution History

The app maintains a history of:
- Flow descriptions
- Generation results
- Timestamps
- Success/failure status

### Status Indicators

- **✅ Crew Ready**: Agents initialized successfully
- **⚠️ Crew Not Initialized**: Need to initialize first
- **🔄 Processing**: Flow generation in progress
- **✅ Success**: Flow created and deployed
- **❌ Error**: Generation failed with details

## 🐛 Troubleshooting

### Common Issues

1. **Crew initialization fails**:
   - Check OpenAI API key
   - Verify network connectivity
   - Review error messages in console

2. **NiFi connection issues**:
   - Verify NiFi URL and port
   - Check authentication token
   - Ensure NiFi is running and accessible

3. **Flow generation errors**:
   - Review natural language description
   - Check agent configurations
   - Verify template availability

### Debug Mode

Enable debug logging by setting:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Powered by [CrewAI](https://github.com/joaomdmoura/crewAI)
- Integrated with [Apache NiFi](https://nifi.apache.org/)
- Styled with custom CSS

---

**NiFi NL Builder** - Transform natural language into Apache NiFi flows with ease! 🔄 