# GitHub Webhook Receiver

This Flask application receives GitHub webhooks and displays repository activity in real-time.

## Features

- Receives GitHub webhooks for Push, Pull Request, and Merge events
- Stores events in MongoDB
- Real-time dashboard that updates every 15 seconds
- Clean, minimal UI design
- Proper error handling and logging

## Setup Instructions

### Prerequisites
- Python 3.7+
- MongoDB running locally on port 27017
- GitHub repository with webhook configured

### Installation

1. Clone this repository:
```bash
git clone <your-repo-url>
cd webhook-repo
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Ensure MongoDB is running:
```bash
# On macOS with Homebrew
brew services start mongodb-community

# On Ubuntu
sudo systemctl start mongod

# Or run directly
mongod
```

4. Run the application:
```bash
python run.py
```

The application will start on `http://localhost:5000`

### GitHub Webhook Configuration

1. Go to your GitHub repository settings
2. Navigate to "Webhooks" section
3. Click "Add webhook"
4. Set Payload URL to: `http://your-server-domain:5000/webhook`
5. Set Content type to: `application/json`
6. Select individual events: `Pushes`, `Pull requests`
7. Ensure webhook is Active
8. Click "Add webhook"

## API Endpoints

- `GET /` - Main dashboard page
- `POST /webhook` - GitHub webhook receiver endpoint
- `GET /events` - JSON API to fetch latest events

## MongoDB Schema

Events are stored in the `github_events` collection with the following structure:

```json
{
  "type": "push|pull_request|merge",
  "author": "string",
  "to_branch": "string",
  "from_branch": "string", // for PR and merge events
  "action": "string", // for PR events
  "timestamp": "ISODate"
}
```

## Event Formats

### Push Event
Format: `{author} pushed to {to_branch} on {timestamp}`
Example: "Travis pushed to staging on April 1st, 2021 - 9:30 PM UTC"

### Pull Request Event
Format: `{author} submitted a pull request from {from_branch} to {to_branch} on {timestamp}`
Example: "Travis submitted a pull request from staging to master on April 1st, 2021 - 9:00 AM UTC"

### Merge Event
Format: `{author} merged branch {from_branch} to {to_branch} on {timestamp}`
Example: "Travis merged branch dev to master on April 2nd, 2021 - 12:00 PM UTC"

## File Structure

```
webhook-repo/
├── app/
│   ├── webhook/
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── __init__.py
│   ├── extensions.py
│   └── routes.py
├── templates/
│   └── index.html
├── requirements.txt
├── README.md
└── run.py
```

## Testing

To test the webhook endpoint locally, you can use ngrok to expose your local server:

```bash
# Install ngrok and expose port 5000
ngrok http 5000

# Use the generated HTTPS URL in your GitHub webhook configuration
# Example: https://abc123.ngrok.io/webhook
```

## Deployment

For production deployment, consider:
- Using environment variables for MongoDB connection
- Setting up proper logging
- Using a WSGI server like Gunicorn
- Setting up HTTPS
- Implementing webhook signature verification for security

## Troubleshooting

1. **MongoDB Connection Issues**: Ensure MongoDB is running and accessible
2. **Webhook Not Receiving Events**: Check GitHub webhook settings and network connectivity
3. **Events Not Displaying**: Check browser console for JavaScript errors and network requests

## License

This project is for assessment purposes.
