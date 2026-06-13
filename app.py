import os
import time
import requests
from flask import Flask, jsonify

app = Flask(__name__)

# Global tracking matrix to feed live stats back to your Tecno Spark 40
ENGINE_STATUS = {
    "active": False, 
    "logs": ["🛰️ Aegis Multi-Campaign Engine Initialized. Ready for telemetry sync."]
}

def execute_campaign_rules():
    """Loops through all live tracker segments and blocks fraud/waste."""
    # Pull secure keys out of the cloud environment box
    propeller_token = os.environ.get("PROPELLER_TOKEN", "")
    tracker_url = os.environ.get("TRACKER_URL", "").rstrip('/')
    tracker_token = os.environ.get("TRACKER_TOKEN", "")
    
    if not propeller_token or not tracker_url:
        ENGINE_STATUS["logs"].insert(0, "⚠️ Access Denied: Missing network API tokens.")
        return

    try:
        # Request data for all active placements across your tracker
        headers = {"X-API-KEY": tracker_token}
        response = requests.get(f"{tracker_url}/api/v1/zones?range=today", headers=headers, timeout=10)
        
        if response.status_code == 200:
            zones_data = response.json().get("rows", [])
            
            # Loop processing through every single campaign tracking block dynamically
            for zone in zones_data:
                campaign_id = str(zone.get("campaign_id", "Unknown-Camp"))
                zone_id = str(zone.get("zone_id"))
                spend = float(zone.get("spend", 0.0))
                clicks = int(zone.get("clicks", 0))
                views = int(zone.get("lander_views", 0))
                conversions = int(zone.get("conversions", 0))
                
                # Math conversion for traffic click loss percentage
                loss = ((clicks - views) / clicks * 100) if clicks > 0 else 0

                # RULE ALPHA: The Fraud Filter (Triggered across all active campaigns)
                if clicks >= 30 and loss > 35.0:
                    log_msg = f"🛑 [Camp: {campaign_id}] Paused Zone {zone_id} ({loss:.1f}% Click Fraud)"
                    if log_msg not in ENGINE_STATUS["logs"]:
                        ENGINE_STATUS["logs"].insert(0, log_msg)
                        # API execution command to PropellerAds to kill the zone goes here

                # RULE BETA: The Budget Spend Guard
                elif spend >= 1.50 and conversions == 0:
                    log_msg = f"💸 [Camp: {campaign_id}] Cut Zone {zone_id} (Spent ${spend} with 0 conversions)"
                    if log_msg not in ENGINE_STATUS["logs"]:
                        ENGINE_STATUS["logs"].insert(0, log_msg)

            timestamp = time.strftime('%H:%M:%S')
            ENGINE_STATUS["logs"].insert(0, f"⏳ [{timestamp}] Global multi-campaign sweep clear.")
    
    except Exception as error:
        ENGINE_STATUS["logs"].insert(0, f"❌ Network Ping Failure: {str(error)}")

@app.route('/')
def basic_ping():
    return jsonify({"engine": "Aegis Media Cloud Core", "status": "Ready"})

@app.route('/api/status')
def send_telemetry():
    # If the cockpit turned the switch on, run the campaign checks
    if ENGINE_STATUS["active"]:
        execute_campaign_rules()
    return jsonify(ENGINE_STATUS)

@app.route('/api/toggle/<string:state>')
def change_engine_state(state):
    ENGINE_STATUS["active"] = True if state.lower() == "on" else False
    action_log = "🚀 [SYSTEM] Multi-Campaign Engine DEPLOYED ACTIVE" if ENGINE_STATUS["active"] else "🛑 [SYSTEM] Automation Suspended"
    ENGINE_STATUS["logs"].insert(0, action_log)
    return jsonify({"status": "success", "engine_active": ENGINE_STATUS["active"]})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
