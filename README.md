# Financial Audit Assistant

A web-based application for generating professional audit reports and plans.

## Features

- Company Information Management
- Sector-Specific Audit Planning
- Risk Assessment
- Resource Allocation
- Timeline Management
- PDF Report Generation

## Deployment Instructions

### Local Development

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the application:
   ```bash
   streamlit run app.py
   ```

### Deploy to Streamlit Cloud

1. Create a GitHub repository and push your code
2. Go to [Streamlit Cloud](https://streamlit.io/cloud)
3. Sign in with your GitHub account
4. Click "New app"
5. Select your repository and branch
6. Set the main file path to `app.py`
7. Click "Deploy"

## Project Structure

- `app.py` - Main application file
- `sector_data.py` - Sector-specific audit data
- `pdf_generator.py` - PDF report generation functionality
- `requirements.txt` - Python dependencies
- `setup.sh` - Deployment setup script

## License

MIT License 