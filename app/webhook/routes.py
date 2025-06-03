from flask import Blueprint, request, jsonify
from app.extensions import mongo
from datetime import datetime
import logging

webhook_bp = Blueprint("webhook", __name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@webhook_bp.route("/webhook", methods=["POST"])
def handle_webhook():
    try:
        event_type = request.headers.get("X-GitHub-Event")
        data = request.json
        
        logger.info(f"Received webhook event: {event_type}")
        
        if not data:
            return jsonify({"error": "No JSON data received"}), 400
        
        if event_type == "ping":
            return jsonify({"message": "Ping received"}), 200
        
        elif event_type == "push":
            # Handle push event
            author = data.get("pusher", {}).get("name", "Unknown")
            ref = data.get("ref", "")
            to_branch = ref.split("/")[-1] if ref else "unknown"
            
            # Insert into MongoDB
            mongo.db.github_events.insert_one({
                "type": "push",
                "author": author,
                "to_branch": to_branch,
                "timestamp": datetime.utcnow()
            })
            
            logger.info(f"Push event stored: {author} -> {to_branch}")
            return jsonify({"message": "Push event stored"}), 200
        
        elif event_type == "pull_request":
            # Handle pull request event
            action = data.get("action", "")
            pr = data.get("pull_request", {})
            
            author = pr.get("user", {}).get("login", "Unknown")
            from_branch = pr.get("head", {}).get("ref", "unknown")
            to_branch = pr.get("base", {}).get("ref", "unknown")
            merged = pr.get("merged", False)
            
            # Check if it's a merge event (closed + merged)
            if action == "closed" and merged:
                mongo.db.github_events.insert_one({
                    "type": "merge",
                    "author": author,
                    "from_branch": from_branch,
                    "to_branch": to_branch,
                    "timestamp": datetime.utcnow()
                })
                logger.info(f"Merge event stored: {author} merged {from_branch} -> {to_branch}")
                return jsonify({"message": "Merge event stored"}), 200
            
            # Regular pull request event
            elif action in ["opened", "synchronize", "reopened"]:
                mongo.db.github_events.insert_one({
                    "type": "pull_request",
                    "action": action,
                    "author": author,
                    "from_branch": from_branch,
                    "to_branch": to_branch,
                    "timestamp": datetime.utcnow()
                })
                logger.info(f"Pull request event stored: {author} {action} PR {from_branch} -> {to_branch}")
                return jsonify({"message": "Pull request event stored"}), 200
            
            else:
                logger.info(f"Ignored pull request action: {action}")
                return jsonify({"message": f"Pull request action '{action}' ignored"}), 200
        
        else:
            logger.warning(f"Unhandled event type: {event_type}")
            return jsonify({"error": f"Unhandled event type: {event_type}"}), 400
    
    except Exception as e:
        logger.error(f"Error processing webhook: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500