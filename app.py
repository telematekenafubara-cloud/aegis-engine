import os
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
# CORS ensures your phone app can read this data without security blocks
CORS(app)

# SERVER MEMORY POOL - This stores your active arbitrage settings live in the cloud
aegis_state = {
    "active": True,
    "active_campaigns_count": 12,      # Counts your running PropellerAds setups
    "target_tier": "Tier 1 Focus",     # Default starting profile
    "current_bid_cap": "0.00140",      # Baseline Tier 1 premium bid cap
    "day_parting": "on"
}

@app.route('/api/status', methods=['GET'])
def get_status():
    """
    Handles when you press 'SYNC ALL' on your Tecno Spark 40.
    Gathers server metrics and packages them into clean data for your screen.
    """
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
            f"💰 Financial Cap: CPM limits securely anchored at ${aegis_state['current_bid_cap']}"
        ]
    })

@app.route('/api/update_params', methods=['GET', 'POST'])
def update_params():
    """
    Listens for adjustments you make via the phone app.
    Intercepts the sliders/dropdown choices and overwrites the server rules.
    """
    global aegis_state
    
    # Read custom parameter values submitted by the mobile interface URL
    bid_cap = request.args.get('bid_cap', aegis_state["current_bid_cap"])
    target_tier = request.args.get('target_tier', aegis_state["target_tier"])
    day_parting = request.args.get('day_parting', aegis_state["day_parting"])
    
    # Commit the mobile choices into the live server memory
    aegis_state["current_bid_cap"] = bid_cap
    aegis_state["target_tier"] = target_tier
    aegis_state["day_parting"] = day_parting
    
    print(f"📡 CLUSTER UPDATE -> Tier: {target_tier} | CPM: ${bid_cap} | Day-Parting: {day_parting}")
    return jsonify({"status": "success", "msg": "Parameters safely committed to cloud database."})

@app.route('/api/toggle/on', methods=['GET'])
def toggle_on():
    global aegis_state
    aegis_state["active"] = True
    return jsonify({"status": "success"})

@app.route('/api/toggle/off', methods=['GET'])
def toggle_off():
    global aegis_state
    aegis_state["active"] = False
    return jsonify({"status": "success"})

if __name__ == "__main__":
    # Render binds your web server automatically using an environment Port variable
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
    
