import json
from crewai.tools import tool

@tool("Retrieve telemetry, coordinates, cargo details, and active route hazards for a specific ship by its ID")
def get_fleet_telemetry(ship_id: str) -> str:
    telemetry = {
        "Voyager-X": {
            "status": "Delayed",
            "coordinates": "24.8607 N, 67.0011 E",
            "cargo_type": "Semiconductors and Electronics",
            "hazard_description": "Severe tropical storm blocking the primary shipping lane in the Arabian Sea",
            "fuel_level": "78%",
            "destination": "Port of Rotterdam"
        },
        "Titan-Liner": {
            "status": "On Schedule",
            "coordinates": "12.0521 N, 43.1492 E",
            "cargo_type": "Automotive Parts",
            "hazard_description": "None",
            "fuel_level": "85%",
            "destination": "Port of Rotterdam"
        }
    }
    ship_data = telemetry.get(ship_id, {})
    return json.dumps(ship_data)

@tool("Retrieve backlog days, alternative berth availability, and daily demurrage fees for a destination port")
def get_port_metrics(port_name: str) -> str:
    ports = {
        "Port of Rotterdam": {
            "backlog_days": 4,
            "alternative_berth_available": True,
            "daily_demurrage_fee_usd": 15000
        },
        "Port of Singapore": {
            "backlog_days": 1,
            "alternative_berth_available": True,
            "daily_demurrage_fee_usd": 12000
        }
    }
    port_data = ports.get(port_name, ports.get("Port of Rotterdam"))
    return json.dumps(port_data)
