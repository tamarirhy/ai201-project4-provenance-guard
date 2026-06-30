from flask import Flask, request, jsonify
from uuid import uuid4
from datetime import datetime, timezone

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from detector import analyze_text
from stylometry import analyze_stylometry
from burstiness import analyze_burstiness
from confidence import calculate_confidence
from labels import get_transparency_label
from audit import write_log, get_log, submit_appeal

app = Flask(__name__)

# -------------------------
# Rate Limiter
# -------------------------
limiter = Limiter(
    key_func=get_remote_address,
    app=app,
    default_limits=[],
    storage_uri="memory://",
)


@app.route("/")
def home():
    return jsonify({
        "message": "Welcome to Provenance Guard!",
        "status": "API is running"
    })


@app.route("/submit", methods=["POST"])
@limiter.limit("10 per minute;100 per day")
def submit():

    data = request.get_json()

    if not data:
        return jsonify({"error": "Request must contain JSON."}), 400

    text = data.get("text")
    creator_id = data.get("creator_id")

    if not text or not creator_id:
        return jsonify({
            "error": "Both 'text' and 'creator_id' are required."
        }), 400

    content_id = str(uuid4())

    # Signal 1
    llm_result = analyze_text(text)
    llm_score = llm_result["score"]
    attribution = llm_result["attribution"]

    # Signal 2
    style_result = analyze_stylometry(text)
    stylometry_score = style_result["score"]

    # Signal 3
    burstiness_result = analyze_burstiness(text)
    burstiness_score = burstiness_result["score"]

    # Combined confidence
    confidence = calculate_confidence(
    llm_score,
    stylometry_score,
    burstiness_score
)

    # Transparency label
    label = get_transparency_label(confidence)

    log_entry = {
        "content_id": content_id,
        "creator_id": creator_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "attribution": attribution,
        "confidence": confidence,
        "llm_score": llm_score,
        "stylometry_score": stylometry_score,
        "burstiness_score": burstiness_score,
        "status": "classified"
    }

    write_log(log_entry)

    return jsonify({
        "content_id": content_id,
        "attribution": attribution,
        "confidence": confidence,
        "label": label,
        "signals": {
            "llm_score": llm_score,
            "stylometry_score": stylometry_score
        }
    })


@app.route("/appeal", methods=["POST"])
def appeal():

    data = request.get_json()

    if not data:
        return jsonify({"error": "Request must contain JSON."}), 400

    content_id = data.get("content_id")
    creator_reasoning = data.get("creator_reasoning")

    if not content_id or not creator_reasoning:
        return jsonify({
            "error": "content_id and creator_reasoning are required."
        }), 400

    updated = submit_appeal(
        content_id,
        creator_reasoning
    )

    if not updated:
        return jsonify({
            "error": "Content ID not found."
        }), 404

    return jsonify({
        "message": "Appeal submitted successfully.",
        "content_id": content_id,
        "status": "under_review"
    })


@app.route("/log", methods=["GET"])
def log():
    return jsonify({
        "entries": get_log()
    })


if __name__ == "__main__":
    app.run(debug=True)