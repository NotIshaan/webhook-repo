from flask import Blueprint, render_template, jsonify
from app.extensions import mongo
import logging

events_bp = Blueprint("events", __name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@events_bp.route("/")
def index():
    """Serve the main HTML page"""
    return render_template("index.html")

@events_bp.route("/events")
def get_events():
    """API endpoint to get latest GitHub events"""
    try:
        # Fetch latest 20 events, sorted by timestamp (newest first)
        events_cursor = mongo.db.github_events.find(
            {}, 
            {'_id': 0}
        ).sort('timestamp', -1).limit(20)
        
        events_list = list(events_cursor)
        
        # Convert datetime objects to ISO format strings for JSON serialization
        for event in events_list:
            if 'timestamp' in event:
                event['timestamp'] = event['timestamp'].isoformat() + 'Z'
        
        logger.info(f"Retrieved {len(events_list)} events")
        return jsonify(events_list)
    
    except Exception as e:
        logger.error(f"Error fetching events: {str(e)}")
        return jsonify({"error": "Failed to fetch events"}), 500