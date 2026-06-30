import json
import os

LOG_FILE = "audit_log.json"


def _initialize_log():
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w") as file:
            json.dump([], file, indent=4)


def write_log(entry):
    _initialize_log()

    with open(LOG_FILE, "r") as file:
        logs = json.load(file)

    logs.append(entry)

    with open(LOG_FILE, "w") as file:
        json.dump(logs, file, indent=4)


def get_log():
    _initialize_log()

    with open(LOG_FILE, "r") as file:
        return json.load(file)


def submit_appeal(content_id, creator_reasoning):
    """
    Update a submission to 'under_review'
    and store the creator's appeal.
    """

    _initialize_log()

    with open(LOG_FILE, "r") as file:
        logs = json.load(file)

    found = False

    for entry in logs:
        if entry["content_id"] == content_id:
            entry["status"] = "under_review"
            entry["appeal_reasoning"] = creator_reasoning
            found = True
            break

    with open(LOG_FILE, "w") as file:
        json.dump(logs, file, indent=4)

    return found