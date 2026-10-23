# SafeHer — Women’s Safety & Route Awareness

SafeHer is a women’s safety-focused web application designed to help users explore routes between locations, with a vision of making urban travel more informed and safety-aware.

The project combines a React frontend with a FastAPI backend to retrieve route information and display route details through a simple user interface.

> **Important safety notice:** SafeHer currently retrieves driving-route information. Routes have not been independently assessed or verified for personal safety. The application should not be treated as a guarantee of safety or as a substitute for emergency services.

## Features

- **Route Search:** Enter an origin and destination to retrieve route information.
- **Route Details:** View available route information, including distance and estimated duration.
- **Backend Integration:** Communicates with a FastAPI backend through HTTP requests.
- **Responsive User Interface:** A modern interface built with React and Vite.
- **Cloud Deployment:** Frontend hosted on Vercel and backend hosted on Render.
- **Future-Oriented Design:** A foundation for integrating verified safety information and safety-aware route recommendations.

## Tech Stack

### Frontend
- React
- Vite
- JavaScript
- CSS

### Backend
- Python
- FastAPI
- REST API
- Uvicorn

### Deployment
- Vercel — Frontend hosting
- Render — Backend hosting
- GitHub — Version control

## Live Demo

- **Frontend:** [SafeHer Web App](https://safeher-frontend.vercel.app/)
- **Backend API:** [SafeHer FastAPI Backend](https://safeher-backend-5467.onrender.com)
- **API Documentation:** [Interactive Swagger UI](https://safeher-backend-5467.onrender.com/docs)

*Note: The frontend URL assumes the default Vercel project domain. Replace it with your actual production domain if it differs.*

## How It Works

1. The user enters a starting location and destination.
2. The frontend validates the input.
3. The application sends a request to the FastAPI backend.
4. The backend retrieves available route information.
5. The frontend displays the returned route details.

## Architecture

```text
User
  |
  v
React + Vite Frontend
  |
  | HTTP GET /route
  v
FastAPI Backend
  |
  v
Route Information
  |
  v
Results Displayed in SafeHer
```

## Getting Started

### Prerequisites

Install the following:

- Node.js and npm
- Python 3.10 or later
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/yehovahacademy/SafeHer---Frontend.git
cd SafeHer---Frontend
```

### 2. Install Dependencies

```bash
npm install
```

### 3. Configure Environment Variables

Create a `.env` file in the frontend project root:

```env
VITE_API_BASE_URL=https://safeher-backend-5467.onrender.com
```

Use your own backend URL if running the backend locally.

**Security note:** Vite exposes variables prefixed with `VITE_` to browser code. Only use this prefix for public configuration, never for passwords, private API keys, or other secrets.

### 4. Start the Development Server

```bash
npm run dev
```

Open the local URL printed by Vite, usually `http://localhost:5173`.

### 5. Build for Production

```bash
npm run build
```

To preview the production build locally:

```bash
npm run preview
```

## API Reference

### Get Routes

**Endpoint:** `GET /route`

Example request:

```http
GET /route?origin=Churchgate&destination=CSMT&transport_mode=driving
```

Example response structure:

```json
{
  "origin": "Churchgate",
  "destination": "CSMT",
  "transport_mode": "driving",
  "routes": [
    {
      "route_id": 1,
      "distance_km": 2.37,
      "duration_minutes": 3.4,
      "geometry": {
        "type": "LineString",
        "coordinates": []
      },
      "safety_status": "Not assessed"
    }
  ],
  "notice": "These are driving routes, not verified safe walking routes."
}
```

The example is illustrative; actual routes and values depend on the backend response.

## Current Limitations

- Route safety is not currently verified.
- Retrieved driving routes may not be suitable for walking.
- Distance and duration estimates may differ from actual travel conditions.
- The application does not guarantee protection from crime or other hazards.
- Route coverage and accuracy depend on the backend's routing data and services.

## Future Enhancements

- Integrate verified public safety datasets and incident reports where legally and ethically appropriate.
- Develop safety-aware route scoring with transparent criteria and data-quality indicators.
- Add walking and public transport routing where supported.
- Explore lighting, operating businesses, public transport access, and emergency-service proximity as potential route factors.
- Introduce emergency-contact workflows and optional location sharing with appropriate consent.
- Expand support for major Indian cities, including Mumbai, Bengaluru, and Kolkata.
- Improve accessibility, mobile usability, and automated testing.

## Contributing

Contributions, feedback, and ideas are welcome. To propose an improvement:

1. Fork the repository.
2. Create a feature branch.
3. Make and test your changes.
4. Submit a pull request describing the improvement.

## Disclaimer

SafeHer is a developing software project intended to support route awareness. It does not certify routes as safe, predict all possible dangers, or replace emergency services. Users should exercise their own judgment and consult reliable local information when making travel decisions.

## Author

**Joshua Joseph**

BSc Information Technology | Python & Web Development | AI/ML Enthusiast

GitHub: [@yehovahacademy](https://github.com/yehovahacademy)

---

*Built with the goal of making everyday travel more informed and safety-aware.*
