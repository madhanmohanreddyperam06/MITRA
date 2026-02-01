# MITRA - AI Powered College Helpdesk Bot

An intelligent chatbot system for college helpdesk services built with Streamlit frontend and FastAPI backend.

## Features

- 🎓 **Admission Information**: Get details about admission process, eligibility, and requirements
- 📚 **Course Information**: Browse available courses and programs
- 💰 **Fee Structure**: Information about fees, scholarships, and payment options
- 🏠 **Hostel Facilities**: Details about accommodation and hostel services
- 📖 **Library Services**: Library facilities and resources information
- 🏢 **Placement Support**: Career guidance and placement statistics
- 📞 **Contact Information**: Department contacts and office locations

## Technology Stack

- **Frontend**: Streamlit
- **Backend**: FastAPI + Python
- **NLP**: spaCy, NLTK
- **Database**: SQLite
- **Deployment**: Docker (optional)

## Installation

1. **Clone the repository**
   ```bash
   git clone <https://github.com/madhanmohanreddyperam06/MITRA.git>
   cd smart_college_bot
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Download spaCy model**
   ```bash
   python -m spacy download en_core_web_sm
   ```

## Usage

### Running the Backend API

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Start the FastAPI server:
   ```bash
   python main.py
   ```

   The API will be available at `http://localhost:8000`

### Running the Streamlit Frontend

1. Navigate to the streamlit_app directory:
   ```bash
   cd streamlit_app
   ```

2. Start the Streamlit app:
   ```bash
   streamlit run main.py
   ```

   The app will open in your browser at `http://localhost:8501`

## Project Structure

```
smart_college_bot/
├── streamlit_app/              # Frontend application
│   ├── main.py                 # Main Streamlit app
│   ├── components/             # Reusable UI components
│   │   ├── __init__.py
│   │   ├── chat_interface.py   # Chat interface component
│   │   └── sidebar.py          # Sidebar component
│   └── pages/                  # Multi-page app pages
│       ├── 1_Admissions.py     # Admissions information page
│       ├── 2_Courses.py        # Courses information page
│       └── 3_Facilities.py     # Facilities information page
├── backend/                    # Backend API
│   ├── main.py                 # FastAPI main application
│   ├── nlp_pipeline.py         # NLP processing pipeline
│   ├── knowledge_base.py       # Knowledge base management
│   └── response_generator.py   # Response generation logic
├── data/                       # Data storage
│   ├── knowledge_base/         # Knowledge base files
│   └── models/                 # ML model storage
├── config/                     # Configuration files
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## Configuration

The system uses SQLite database for storing knowledge base information. The database is automatically initialized with sample data on first run.

## API Endpoints

- `GET /`: Health check
- `GET /health`: Detailed health status
- `POST /chat`: Main chat endpoint
- `GET /intents`: Available intents

## Customization

### Adding New Intents

1. Update `intent_patterns` in `nlp_pipeline.py`
2. Add corresponding handler in `response_generator.py`
3. Update knowledge base if needed

### Modifying Knowledge Base

Edit the sample data in `knowledge_base.py` or directly modify the SQLite database.

### Customizing UI

Modify components in the `streamlit_app/components/` directory or add new pages in `pages/` directory.

## Development

### Running in Development Mode

Backend with auto-reload:
```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Streamlit with auto-reload:
```bash
cd streamlit_app
streamlit run main.py --server.runOnSave true
```

### Testing

```bash
pytest backend/tests/
```

## Deployment

### Docker Deployment (Optional)

Create `Dockerfile` and `docker-compose.yml` for containerized deployment.

### Cloud Deployment

- **Frontend**: Deploy on Streamlit Community Cloud
- **Backend**: Deploy on Heroku, AWS, or similar platforms

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For support or questions, please contact the development team or create an issue in the repository.
