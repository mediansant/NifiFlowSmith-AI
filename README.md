# 🚀 NiFi NL Builder

**Transform Natural Language into Apache NiFi Flows with AI**

A powerful system that uses CrewAI agents to convert plain English descriptions into fully functional Apache NiFi data flows, with both command-line and web interfaces.

## 📋 Table of Contents

- [Features](#-features)
- [Quick Start](#-quick-start)
- [Architecture](#-architecture)
- [Installation](#-installation)
- [Usage](#-usage)
- [Docker NiFi Setup](#-docker-nifi-setup)
- [Configuration](#-configuration)
- [Troubleshooting](#-troubleshooting)
- [Project Structure](#-project-structure)
- [Contributing](#-contributing)

## ✨ Features

- **🤖 AI-Powered Flow Generation**: Convert natural language to NiFi flows using CrewAI
- **🌐 Web Interface**: Modern Streamlit UI for easy interaction
- **💻 Command Line**: Direct CLI for automation and scripting
- **🐳 Docker Integration**: Local NiFi development environment
- **📊 Real-time Monitoring**: Track flow generation and deployment
- **🔧 Template System**: Reusable flow templates and patterns
- **🔄 Multi-Agent Workflow**: Four specialized AI agents working together

## 🚀 Quick Start

### 1. Prerequisites

- Python 3.8+
- Docker and Docker Compose
- OpenAI API key

### 2. Setup

```bash
# Clone and setup
git clone <repository-url>
cd Nifiautomation

# Install dependencies
uv pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your OpenAI API key
```

### 3. Start NiFi (Docker)

```bash
# Start local NiFi instance
./scripts/start-nifi.sh

# Verify NiFi is running
./scripts/check-nifi.sh
```

### 4. Generate Your First Flow

**Option A: Web Interface**
```bash
python run_app.py
# Open http://localhost:8501
```

**Option B: Command Line**
```bash
python nifi_cli.py deploy "My First Flow" "Read from a file and log the contents"
```

## 🏗️ Architecture

### Multi-Agent System

1. **nl_parser** 🤖: Extracts structured requirements from natural language
2. **flow_planner** 📋: Matches requirements to existing NiFi templates  
3. **flow_builder** 🔧: Creates flow definitions using NiFi REST API
4. **cdf_deployer** 🚀: Deploys flows to Cloudera Data Flow

### Technology Stack

- **CrewAI**: Multi-agent orchestration framework
- **Streamlit**: Web interface
- **Apache NiFi**: Data flow management
- **Docker**: Local development environment
- **OpenAI GPT**: Natural language processing

## 📦 Installation

### Detailed Setup

1. **Environment Setup**
   ```bash
   # Create virtual environment (optional)
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install dependencies
   uv pip install -r requirements.txt
   ```

2. **Configuration**
   ```bash
   # Set up environment variables
   cp .env.example .env
   
   # Edit .env with your settings:
   OPENAI_API_KEY=sk-your-openai-api-key-here
   NIFI_URL=http://localhost:8080
   NIFI_USERNAME=admin
   NIFI_PASSWORD=admin123
   ```

3. **Verify Installation**
   ```bash
   # Test NiFi connection
   python nifi_cli.py list
   
   # Test CrewAI setup
   python -c "from src.nifi_nl_builder.crew import NiFiNLCrew; print('✅ Setup complete')"
   ```

## 🎯 Usage

### Web Interface (Recommended)

```bash
python run_app.py
```

**Features:**
- Natural language input
- Real-time flow generation
- Execution history
- Configuration management
- Template management

### Command Line Interface

```bash
# List existing flows
python nifi_cli.py list

# Deploy from description
python nifi_cli.py deploy "Flow Name" "Description of what the flow should do"

# Deploy from template
python nifi_cli.py template simple_logging

# Show flow details
python nifi_cli.py show <flow-id>

# Start/stop flows
python nifi_cli.py start <flow-id>
python nifi_cli.py stop <flow-id>
```

### Direct API Usage

```bash
# Deploy flow programmatically
python deploy_flow.py "Flow Name" "Description"
```

## 🐳 Docker NiFi Setup

### Quick Start

```bash
# Start NiFi
./scripts/start-nifi.sh

# Check status
./scripts/check-nifi.sh

# Stop NiFi
./scripts/stop-nifi.sh

# Clean all data
./scripts/clean-nifi.sh
```

### Access Points

- **NiFi Web UI**: http://localhost:8080/nifi
- **NiFi REST API**: http://localhost:8080/nifi-api
- **Username**: admin
- **Password**: admin123

### Configuration

The NiFi instance is configured with:
- Single-user authentication (admin/admin123)
- HTTP access (no HTTPS)
- Standalone mode (no clustering)
- Persistent data storage via Docker volumes

### Environment Variables

Update your `.env` file with:
```bash
NIFI_URL=http://localhost:8080
NIFI_USERNAME=admin
NIFI_PASSWORD=admin123
```

### Data Persistence

NiFi data is stored in Docker volumes:
- `nifi_database_repository`: Database files
- `nifi_flowfile_repository`: FlowFile data
- `nifi_content_repository`: Content storage
- `nifi_provenance_repository`: Provenance data
- `nifi_state`: State information
- `nifi_logs`: Log files

To completely reset: `./scripts/clean-nifi.sh`

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key | Required |
| `NIFI_URL` | NiFi instance URL | `http://localhost:8080` |
| `NIFI_USERNAME` | NiFi username | `admin` |
| `NIFI_PASSWORD` | NiFi password | `admin123` |
| `NIFI_TOKEN` | NiFi authentication token | Optional |
| `CDP_SERVICE_CRN` | Cloudera Data Platform service CRN | Required for deployment |
| `CDP_ENV_CRN` | Cloudera Data Platform environment CRN | Required for deployment |

### Model Settings

- **Primary Model**: Choose between GPT-4o, GPT-4o-mini, or GPT-3.5-turbo
- **Temperature**: Control randomness (0.0 = deterministic, 1.0 = creative)
- **Max Tokens**: Limit response length for cost control

## 🐛 Troubleshooting

### Common Issues

1. **NiFi not starting**:
   ```bash
   # Check Docker is running
   docker info
   
   # Check port availability
   lsof -i :8080
   
   # View NiFi logs
   docker logs nifi-local
   ```

2. **CrewAI initialization fails**:
   - Verify OpenAI API key in `.env`
   - Check network connectivity
   - Review error messages in console

3. **Flow generation errors**:
   - Ensure NiFi is running and accessible
   - Check authentication credentials
   - Review natural language description clarity

4. **Permission errors**:
   ```bash
   chmod +x scripts/*.sh
   ```

### Debug Mode

Enable debug logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📁 Project Structure

```
Nifiautomation/
├── 📁 src/                          # Main application source
│   └── 📁 nifi_nl_builder/
│       ├── 📁 config/               # Agent and task configurations
│       ├── 📁 tools/                # NiFi API and CrewAI tools
│       └── crew.py                  # Main CrewAI orchestration
├── 📁 streamlit_app/                # Web interface
│   ├── app.py                       # Main Streamlit application
│   ├── ui.css                       # Custom styling
│   └── README.md                    # UI documentation
├── 📁 templates/                    # NiFi flow templates
├── 📁 scripts/                      # Docker and utility scripts
├── 📁 test-data/                    # Sample data for testing
├── 📁 nifi-conf/                    # NiFi configuration files
├── docker-compose.yml               # Docker services configuration
├── requirements.txt                 # Python dependencies
├── run_app.py                       # Streamlit app launcher
├── deploy_flow.py                   # Direct flow deployment
├── nifi_cli.py                      # Command-line interface
├── .env                             # Environment variables
├── .cursorrules                     # Cursor IDE rules
└── README.md                        # This file
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Test thoroughly
5. Submit a pull request

### Development Setup

```bash
# Install development dependencies
uv pip install -r requirements.txt

# Run tests
python -m pytest tests/

# Format code
black src/ streamlit_app/

# Lint code
flake8 src/ streamlit_app/
```

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Powered by [CrewAI](https://github.com/joaomdmoura/crewAI)
- Integrated with [Apache NiFi](https://nifi.apache.org/)
- Containerized with [Docker](https://www.docker.com/)

---

**🎉 Ready to transform natural language into Apache NiFi flows!**

For detailed documentation, see:
- [Streamlit UI Guide](streamlit_app/README.md)
- [NiFi Setup Guide](NIFI_README.md) 