# Weather Predictor

A simple Flask-based weather prediction API service.

## Features

- Simple REST API for weather predictions
- Health check endpoint
- Docker support
- Error handling and logging

## Getting Started

### Prerequisites

- Python 3.10+
- Docker (optional)

### Local Setup

1. Clone the repository
```bash
git clone https://github.com/yourusername/weather-predictor.git
cd weather-predictor
```

2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Run the application
```bash
python app.py
```

The API will be available at `http://localhost:5000`

### Docker Setup

Build and run using Docker:
```bash
docker build -t weather-predictor .
docker run -p 5000:5000 weather-predictor
```

## API Endpoints

### Health Check
```
GET /health
```

Response:
```json
{
  "status": "healthy"
}
```

### Weather Prediction
```
POST /predict
```

Request body:
```json
{
  "city": "London"
}
```

Response:
```json
{
  "city": "London",
  "prediction": "sunny"
}
```

## Possible Weather Conditions

- sunny
- cloudy
- rainy
- stormy
- snowy

## Development

### Project Structure

```
weather-predictor/
├── app.py              # Main Flask application
├── dockerfile          # Docker configuration
├── requirements.txt    # Python dependencies
├── .gitignore         # Git ignore rules
└── README.md          # This file
```

### Future Improvements

- Integrate with real weather data APIs
- Add weather forecasting models
- Implement caching
- Add unit tests
- Multi-city support
- Historical data tracking

## License

MIT

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.