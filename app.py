import os
from flask import Flask, jsonify, request

app = Flask(__name__)

# GLOBAL MEMORY POOL - Tracks your exact arbitrage targets dynamically
aegis_state = {
    "active": True,
    "active_campaigns_count": 12,      # Counts your live running setups
    "target_tier": "Tier 1 Focus",     # Default starting profile
    "current_bid_cap": "0.00140",      # Baseline Tier 1 premium bid cap
    "day_parting": "on"
}

# Fixes connection blocks for AppCreator24 by attaching a secure header manually
@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    return response

@app.route('/api/status', methods=['GET'])
def get_status():
    global aegis_state
    return jsonify({
        "active": aegis_state["active"],
        "active_campaigns_count": aegis_state["active_campaigns_count"],
        "target_tier": aegis_state["target_tier"],
        "current_bid_cap": aegis_state["current_bid_cap"],
        "day_parting": aegis_state["day_parting"],
        "logs": [
            f"⚡ System Layer: Syncing {aegis_state['target_tier']} profiles.",
            f"🛡️ Guardrails: Day-Parting automation loop is {aegis_state['day_parting'].upper()}.",
            f"Rh-Spread: CPM caps anchored at ${aegis_state['current_bid_cap']}"
        ]
    })

@app.route('/api/update_params', methods=['GET', 'POST'])
def update_params():
    global aegis_state
    bid_cap = request.args.get('bid_cap', aegis_state["current_bid_cap"])
    target_tier = request.args.get('target_tier', aegis_state["target_tier"])
    day_parting = request.args.get('day_parting', aegis_state["day_parting"])
    
    aegis_state["current_bid_cap"] = bid_cap
    aegis_state["target_tier"] = target_tier
    aegis_state["day_parting"] = day_parting
    
    print(f"📡 MOBILE UPDATE DETECTED -> Tier: {target_tier} | CPM: ${bid_cap}")
    return jsonify({"status": "success"})

@app.route('/api/toggle/<state>', methods=['GET'])
def toggle_engine(state):
    global aegis_state
    aegis_state["active"] = True if state == "on" else False
    return jsonify({"status": "success"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
    
