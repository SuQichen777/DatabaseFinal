from .profileRoutes import profile_bp
from .tripRoutes import trip_bp # It is not used in the app, trips_bp is used instead
from .dashboardRoutes import trips_bp, destination_bp, tour_guide_bp, hotel_bp
from .cartRoutes import cart_bp

all_blueprints = [
    profile_bp, trip_bp, trips_bp, destination_bp, tour_guide_bp, hotel_bp, cart_bp
]
