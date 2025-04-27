from .profileRoutes import profile_bp
from .tripRoutes import trip_bp
from .dashboardRoutes import trips_bp, destination_bp, tour_guide_bp, hotel_bp

all_blueprints = [
    profile_bp, trip_bp, trips_bp, destination_bp, tour_guide_bp, hotel_bp
]
