#!/usr/bin/env python3
"""
NateOS Web Management API
Provides REST endpoints for configuring all networking functions
"""
import json
import os
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

# Get the directory where this file is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")

app = Flask(__name__, static_folder=STATIC_DIR)
CORS(app)  # Enable CORS for frontend

# Serve the main HTML page
@app.route("/")
@app.route("/static/index.html")
def index():
    """Serve the main web GUI"""
    return send_from_directory(STATIC_DIR, "index.html")

# In-memory config store (will be replaced with Redis/datastore later)
CONFIG_STORE = {
    "interfaces": {},
    "vlans": {},
    "stp": {"enabled": False, "mode": "rstp", "priority": 32768},
    "lacp": {},
    "lldp": {"enabled": False},
    "igmp_snooping": {"enabled": False},
    "static_routes": [],
    "ospf": {"enabled": False, "areas": {}},
    "bgp": {"enabled": False, "asn": 0, "neighbors": {}},
    "vrp": {},
    "qos": {},
    "acl": [],
    "span": {},
    "system": {"hostname": "nateos-switch", "domain": "local"},
    "aaa": {"auth_method": "local"},
}


@app.route("/api/health", methods=["GET"])
def health():
    """Health check endpoint"""
    return jsonify({"status": "ok", "service": "nateos-web-api"})


@app.route("/api/config", methods=["GET"])
def get_config():
    """Get entire configuration"""
    return jsonify(CONFIG_STORE)


@app.route("/api/config/<section>", methods=["GET"])
def get_config_section(section):
    """Get specific configuration section"""
    if section in CONFIG_STORE:
        return jsonify(CONFIG_STORE[section])
    return jsonify({"error": f"Section '{section}' not found"}), 404


@app.route("/api/config/<section>", methods=["POST", "PUT"])
def update_config_section(section):
    """Update configuration section"""
    if section not in CONFIG_STORE:
        return jsonify({"error": f"Section '{section}' not found"}), 404
    
    data = request.get_json()
    if isinstance(CONFIG_STORE[section], dict):
        CONFIG_STORE[section].update(data)
    elif isinstance(CONFIG_STORE[section], list):
        CONFIG_STORE[section] = data
    else:
        CONFIG_STORE[section] = data
    
    return jsonify({"status": "updated", section: CONFIG_STORE[section]})


# L2 Configuration Endpoints
@app.route("/api/l2/interfaces", methods=["GET"])
def get_interfaces():
    """Get all interfaces"""
    return jsonify(CONFIG_STORE["interfaces"])


@app.route("/api/l2/interfaces/<interface>", methods=["GET", "PUT", "POST"])
def interface_config(interface):
    """Configure interface (VLAN membership, mode, etc.)"""
    if request.method == "GET":
        return jsonify(CONFIG_STORE["interfaces"].get(interface, {}))
    
    data = request.get_json()
    if interface not in CONFIG_STORE["interfaces"]:
        CONFIG_STORE["interfaces"][interface] = {}
    CONFIG_STORE["interfaces"][interface].update(data)
    return jsonify({"status": "updated", "interface": interface, "config": CONFIG_STORE["interfaces"][interface]})


@app.route("/api/l2/vlans", methods=["GET", "POST"])
def vlans():
    """Get or create VLANs"""
    if request.method == "GET":
        return jsonify(CONFIG_STORE["vlans"])
    
    data = request.get_json()
    vlan_id = data.get("vlan_id")
    if vlan_id:
        CONFIG_STORE["vlans"][str(vlan_id)] = data
        return jsonify({"status": "created", "vlan": CONFIG_STORE["vlans"][str(vlan_id)]})
    return jsonify({"error": "vlan_id required"}), 400


@app.route("/api/l2/vlans/<vlan_id>", methods=["DELETE"])
def delete_vlan(vlan_id):
    """Delete VLAN"""
    if vlan_id in CONFIG_STORE["vlans"]:
        del CONFIG_STORE["vlans"][vlan_id]
        return jsonify({"status": "deleted", "vlan_id": vlan_id})
    return jsonify({"error": "VLAN not found"}), 404


@app.route("/api/l2/stp", methods=["GET", "PUT"])
def stp_config():
    """Configure Spanning Tree Protocol"""
    if request.method == "GET":
        return jsonify(CONFIG_STORE["stp"])
    
    data = request.get_json()
    CONFIG_STORE["stp"].update(data)
    return jsonify({"status": "updated", "stp": CONFIG_STORE["stp"]})


@app.route("/api/l2/lacp", methods=["GET", "PUT"])
def lacp_config():
    """Configure LACP"""
    if request.method == "GET":
        return jsonify(CONFIG_STORE["lacp"])
    
    data = request.get_json()
    CONFIG_STORE["lacp"].update(data)
    return jsonify({"status": "updated", "lacp": CONFIG_STORE["lacp"]})


@app.route("/api/l2/lldp", methods=["GET", "PUT"])
def lldp_config():
    """Configure LLDP"""
    if request.method == "GET":
        return jsonify(CONFIG_STORE["lldp"])
    
    data = request.get_json()
    CONFIG_STORE["lldp"].update(data)
    return jsonify({"status": "updated", "lldp": CONFIG_STORE["lldp"]})


@app.route("/api/l2/igmp-snooping", methods=["GET", "PUT"])
def igmp_snooping_config():
    """Configure IGMP snooping"""
    if request.method == "GET":
        return jsonify(CONFIG_STORE["igmp_snooping"])
    
    data = request.get_json()
    CONFIG_STORE["igmp_snooping"].update(data)
    return jsonify({"status": "updated", "igmp_snooping": CONFIG_STORE["igmp_snooping"]})


# L3 Configuration Endpoints
@app.route("/api/l3/static-routes", methods=["GET", "POST"])
def static_routes():
    """Get or add static routes"""
    if request.method == "GET":
        return jsonify(CONFIG_STORE["static_routes"])
    
    data = request.get_json()
    CONFIG_STORE["static_routes"].append(data)
    return jsonify({"status": "added", "route": data})


@app.route("/api/l3/static-routes/<int:index>", methods=["DELETE"])
def delete_static_route(index):
    """Delete static route by index"""
    if 0 <= index < len(CONFIG_STORE["static_routes"]):
        route = CONFIG_STORE["static_routes"].pop(index)
        return jsonify({"status": "deleted", "route": route})
    return jsonify({"error": "Route not found"}), 404


@app.route("/api/l3/ospf", methods=["GET", "PUT"])
def ospf_config():
    """Configure OSPF"""
    if request.method == "GET":
        return jsonify(CONFIG_STORE["ospf"])
    
    data = request.get_json()
    CONFIG_STORE["ospf"].update(data)
    return jsonify({"status": "updated", "ospf": CONFIG_STORE["ospf"]})


@app.route("/api/l3/bgp", methods=["GET", "PUT"])
def bgp_config():
    """Configure BGP"""
    if request.method == "GET":
        return jsonify(CONFIG_STORE["bgp"])
    
    data = request.get_json()
    CONFIG_STORE["bgp"].update(data)
    return jsonify({"status": "updated", "bgp": CONFIG_STORE["bgp"]})


@app.route("/api/l3/vrrp", methods=["GET", "PUT"])
def vrrp_config():
    """Configure VRRP"""
    if request.method == "GET":
        return jsonify(CONFIG_STORE["vrp"])
    
    data = request.get_json()
    CONFIG_STORE["vrp"].update(data)
    return jsonify({"status": "updated", "vrrp": CONFIG_STORE["vrp"]})


# Management Endpoints
@app.route("/api/mgmt/qos", methods=["GET", "PUT"])
def qos_config():
    """Configure QoS"""
    if request.method == "GET":
        return jsonify(CONFIG_STORE["qos"])
    
    data = request.get_json()
    CONFIG_STORE["qos"].update(data)
    return jsonify({"status": "updated", "qos": CONFIG_STORE["qos"]})


@app.route("/api/mgmt/acl", methods=["GET", "POST"])
def acl_config():
    """Get or add ACL rules"""
    if request.method == "GET":
        return jsonify(CONFIG_STORE["acl"])
    
    data = request.get_json()
    CONFIG_STORE["acl"].append(data)
    return jsonify({"status": "added", "acl": data})


@app.route("/api/mgmt/span", methods=["GET", "PUT"])
def span_config():
    """Configure SPAN/port mirroring"""
    if request.method == "GET":
        return jsonify(CONFIG_STORE["span"])
    
    data = request.get_json()
    CONFIG_STORE["span"].update(data)
    return jsonify({"status": "updated", "span": CONFIG_STORE["span"]})


@app.route("/api/mgmt/system", methods=["GET", "PUT"])
def system_config():
    """Configure system settings"""
    if request.method == "GET":
        return jsonify(CONFIG_STORE["system"])
    
    data = request.get_json()
    CONFIG_STORE["system"].update(data)
    return jsonify({"status": "updated", "system": CONFIG_STORE["system"]})


@app.route("/api/mgmt/aaa", methods=["GET", "PUT"])
def aaa_config():
    """Configure AAA (Authentication, Authorization, Accounting)"""
    if request.method == "GET":
        return jsonify(CONFIG_STORE["aaa"])
    
    data = request.get_json()
    CONFIG_STORE["aaa"].update(data)
    return jsonify({"status": "updated", "aaa": CONFIG_STORE["aaa"]})


# Serve static files (CSS, JS)
@app.route("/static/<path:filename>")
def static_files(filename):
    """Serve static files"""
    return send_from_directory(STATIC_DIR, filename)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    print(f"[NateOS Web GUI] Starting server on http://0.0.0.0:{port}")
    print(f"[NateOS Web GUI] Access the GUI at: http://localhost:{port}/")
    app.run(host="0.0.0.0", port=port, debug=True)

