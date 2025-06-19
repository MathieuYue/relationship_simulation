class WorldState:
    def __init__(self):
        # Physical environment
        self.locations = {
            "home": {
                "privacy": 0.9,  # 0-1 scale
                "comfort": 0.8,
                "triggers": ["family_photo", "shared_bed"]
            },
            "restaurant": {
                "privacy": 0.4,
                "comfort": 0.6,
                "triggers": ["menu", "other_couples"]
            }
        }

        
        # Temporal Factors
        self.time = {
            "hour": 14,
            "day_type": "weekday",  # weekend/holiday
            "stress_level": 0.5  # Environmental stress
        }