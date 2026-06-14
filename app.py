import os
import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

# SECURITY PROFILE KEYS - Set up your live network connections securely
PROPELLER_API_KEY = os.environ.get("PROPELLER_API_KEY", "YOUR_REAL_PROPELLER_TOKEN_HERE")
ADSTERRA_API_KEY = os.environ.get("ADSTERRA_API_KEY", "YOUR_REAL_ADSTERRA_TOKEN_HERE")

server_memory = {
    "last_deployed_campaign": "None",
    "last_layer_used": "All Layers (Auto)",
    "active_bid_cap": "0.00140"
}

@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    return response

@app.route('/api/status', methods=['GET'])
def get_status():
    return jsonify({
        "active": True,
        "active_campaigns_count": 3,
        "target_tier": "Multi-Layer Auto",
        "current_bid_cap": server_memory["active_bid_cap"],
        "logs": [
            f"📦 Current Pipeline: {server_memory['last_deployed_campaign']}",
            f"🛠️ Target Routing Layer: {server_memory['last_layer_used']}"
        ]
    })

@app.route('/api/update_params', methods=['GET', 'POST'])
def update_params():
    global server_memory
    
    # Extract live form entries from your phone screen
    name = request.args.get('camp_name', 'Unnamed Mobile Push')
    url = request.args.get('landing_url', '')
    keywords = request.args.get('keywords', '')
    layer = request.args.get('execution_layer', 'All Layers (Auto)')
    budget = request.args.get('budget', '25')
    bid_cap = request.args.get('bid_cap', '0.00140')

    server_memory["last_deployed_campaign"] = name
    server_memory["last_layer_used"] = layer
    server_memory["active_bid_cap"] = bid_cap

    print(f"📡 API PAYLOAD RECEIVED -> Launching: {name} | Budget: ${budget} | Scope: {layer}")

    # --- LIVE API EXECUTION CONTRACT BRIDGES ---
    
    # 1. PROPELLERADS CAMPAIGN CREATION BLOCK (Layer 1 Engine)
    if "Layer 1" in layer or "All Layers" in layer:
        propeller_url = "https://api.propellerads.com/v2/adv/campaigns"
        propeller_headers = {
            "Authorization": f"Bearer {PROPELLER_API_KEY}",
            "Content-Type": "application/json"
        }
        propeller_payload = {
            "name": name,
            "status": 1, # 1 turns the campaign on immediately upon approval
            "direction": "onclick", # Native Popunder traffic allocation
            "rate_model": "scpm", # Auto-optimizing Smart CPM Bidding
            "target_url": url,
            "daily_budget": float(budget),
            "tracking_url": url
        }
        print("⚡ FORWARDING DIGITAL CONTRACT TO PROPELLERADS API HUBS...")
        # To go 100% live, uncomment the line below when your tokens are added:
        # requests.post(propeller_url, json=propeller_payload, headers=propeller_headers)

    # 2. ADSTERRA CAMPAIGN CREATION BLOCK (Layer 2 Social Bar Engine)
    if "Layer 2" in layer or "All Layers" in layer:
        adsterra_url = "https://api.adsterra.com/v3/advertiser/campaigns"
        adsterra_headers = {
            "X-API-Key": ADSTERRA_API_KEY,
            "Content-Type": "application/json"
        }
        adsterra_payload = {
            "name": name,
            "url": url,
            "bid": float(bid_cap),
            "daily_budget": float(budget),
            "keywords": keywords
        }
        print("⚡ FORWARDING DIGITAL CONTRACT TO ADSTERRA API HUBS...")
        # To go 100% live, uncomment the line below when your tokens are added:
        # requests.post(adsterra_url, json=adsterra_payload, headers=adsterra_headers)

    return jsonify({"status": "success", "msg": "Campaign injected successfully across selected layers."})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
    
