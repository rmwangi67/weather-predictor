KENYAN_COUNTIES = [
    {"name": "Baringo", "latitude": 0.5000, "longitude": 35.9667},
    {"name": "Bomet", "latitude": -0.7687, "longitude": 35.4394},
    {"name": "Bungoma", "latitude": 0.5658, "longitude": 34.5580},
    {"name": "Busia", "latitude": 0.4556, "longitude": 34.1024},
    {"name": "Elgeyo-Marakwet", "latitude": 0.5091, "longitude": 35.4390},
    {"name": "Embu", "latitude": -0.5323, "longitude": 37.4578},
    {"name": "Garissa", "latitude": -0.4545, "longitude": 39.6454},
    {"name": "Homa Bay", "latitude": -0.5300, "longitude": 34.4604},
    {"name": "Isiolo", "latitude": 0.3547, "longitude": 37.5827},
    {"name": "Kajiado", "latitude": -1.9310, "longitude": 36.7817},
    {"name": "Kakamega", "latitude": 0.2822, "longitude": 34.7519},
    {"name": "Kericho", "latitude": -0.3675, "longitude": 35.2833},
    {"name": "Kiambu", "latitude": -1.0453, "longitude": 36.6562},
    {"name": "Kilifi", "latitude": -3.6333, "longitude": 39.8500},
    {"name": "Kirinyaga", "latitude": -0.6822, "longitude": 37.2758},
    {"name": "Kisii", "latitude": -0.6858, "longitude": 34.7728},
    {"name": "Kisumu", "latitude": -0.0917, "longitude": 34.7680},
    {"name": "Kitui", "latitude": -1.3667, "longitude": 38.0167},
    {"name": "Kwale", "latitude": -4.4567, "longitude": 39.4440},
    {"name": "Laikipia", "latitude": 0.4000, "longitude": 36.8500},
    {"name": "Lamu", "latitude": -2.2719, "longitude": 40.9097},
    {"name": "Machakos", "latitude": -1.5177, "longitude": 37.2633},
    {"name": "Makueni", "latitude": -1.7878, "longitude": 37.7315},
    {"name": "Mandera", "latitude": 3.9372, "longitude": 41.8642},
    {"name": "Marsabit", "latitude": 2.3300, "longitude": 37.9897},
    {"name": "Meru", "latitude": 0.0469, "longitude": 37.6493},
    {"name": "Migori", "latitude": -1.0658, "longitude": 34.4737},
    {"name": "Mombasa", "latitude": -4.0435, "longitude": 39.6682},
    {"name": "Murang'a", "latitude": -0.7115, "longitude": 37.1510},
    {"name": "Nairobi", "latitude": -1.2921, "longitude": 36.8219},
    {"name": "Nakuru", "latitude": -0.3031, "longitude": 36.0800},
    {"name": "Nandi", "latitude": 0.1000, "longitude": 35.1000},
    {"name": "Narok", "latitude": -1.0878, "longitude": 35.8250},
    {"name": "Nyamira", "latitude": -0.5667, "longitude": 34.9500},
    {"name": "Nyandarua", "latitude": -0.4244, "longitude": 36.2431},
    {"name": "Nyeri", "latitude": -0.4258, "longitude": 36.9473},
    {"name": "Samburu", "latitude": 0.5833, "longitude": 37.5167},
    {"name": "Siaya", "latitude": 0.0620, "longitude": 34.2865},
    {"name": "Taita-Taveta", "latitude": -3.3963, "longitude": 38.3563},
    {"name": "Tana River", "latitude": -1.4524, "longitude": 39.7890},
    {"name": "Tharaka-Nithi", "latitude": 0.3000, "longitude": 37.7500},
    {"name": "Trans Nzoia", "latitude": 1.0000, "longitude": 35.0000},
    {"name": "Turkana", "latitude": 3.9833, "longitude": 35.5667},
    {"name": "Uasin Gishu", "latitude": 0.5167, "longitude": 35.2667},
    {"name": "Vihiga", "latitude": 0.0900, "longitude": 34.7400},
    {"name": "Wajir", "latitude": 1.7484, "longitude": 40.0575},
    {"name": "West Pokot", "latitude": 1.2333, "longitude": 35.0667},
]

def get_county_by_name(name):
    """Find a county by name (case-insensitive)."""
    if not name:
        return None
    normalized = name.strip().lower()
    for county in KENYAN_COUNTIES:
        if county["name"].lower() == normalized:
            return county
    return None