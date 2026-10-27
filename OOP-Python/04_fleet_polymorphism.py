class ElectricVehicle:
    """
    The parent (base) class representing a standard Electric Vehicle.
    
    This class establishes the basic attributes (`vehicle_id`, `battery_level`) 
    and provides a default `calculate_range()` method that child classes can 
    either use as-is or override with their own custom formula (Polymorphism).
    """

    def __init__(self, vehicle_id: str, battery_level: int):
        """
        The constructor method (__init__) that initializes a new ElectricVehicle.
        
        Args:
            vehicle_id (str): The unique identifier for the vehicle (e.g., "SEDAN-01").
            battery_level (int): The starting battery percentage (e.g., 80).
        """
        self.vehicle_id = vehicle_id        # Stores the vehicle's unique ID
        self.battery_level = battery_level  # Stores the starting battery percentage

    def calculate_range(self) -> float:
        """
        Calculates the estimated driving range in kilometers for a standard electric vehicle.
        
        Returns:
            float: The estimated range (assumes 3.5 km per 1% of battery).
        """
        # Multiplies battery percentage by 3.5 (e.g., 80 * 3.5 = 280.0 km)
        return self.battery_level * 3.5


class DeliveryVan(ElectricVehicle):
    """
    A child class (subclass) representing a Delivery Van that inherits from `ElectricVehicle`.
    
    It adds a `cargo_weight_kg` attribute and overrides `calculate_range()` 
    because heavy cargo reduces how far the van can drive on a charge.
    """

    def __init__(self, vehicle_id: str, battery_level: int, cargo_weight_kg: int):
        """
        Initializes a new DeliveryVan object.
        
        Args:
            vehicle_id (str): The unique identifier for the van.
            battery_level (int): The starting battery percentage.
            cargo_weight_kg (int): The weight of the cargo in kilograms.
        """
        # `super().__init__(...)` calls the parent class (`ElectricVehicle`) constructor
        # to set up `vehicle_id` and `battery_level`.
        super().__init__(vehicle_id, battery_level)
        
        # Sets up the cargo weight attribute specific to DeliveryVan
        self.cargo_weight_kg = cargo_weight_kg

    def calculate_range(self) -> float:
        """
        Overrides the parent class's `calculate_range()` method (Method Overriding).
        
        Calculates the van's driving range: starts with 2.5 km per 1% of battery, 
        then subtracts 0.05 km for every 1 kg of cargo weight.
        
        Returns:
            float: The estimated driving range in kilometers (never drops below 0.0 km).
        """
        # `max(0.0, ...)` ensures that even if the cargo is extremely heavy, 
        # the range won't return a negative number (it stops at 0.0 km).
        return max(0.0, (self.battery_level * 2.5) - (self.cargo_weight_kg * 0.05))


class ElectricScooter(ElectricVehicle):
    """
    A child class (subclass) representing an Electric Scooter that inherits from `ElectricVehicle`.
    
    Notice it does not define its own `__init__` method! Because it doesn't need any extra 
    attributes, it automatically uses the `__init__` method inherited from `ElectricVehicle`.
    """

    def calculate_range(self) -> float:
        """
        Overrides the parent class's `calculate_range()` method (Method Overriding).
        
        Calculates the scooter's driving range based on its smaller battery capacity.
        
        Returns:
            float: The estimated driving range (assumes 0.8 km per 1% of battery).
        """
        # Multiplies battery percentage by 0.8 (e.g., 80 * 0.8 = 64.0 km)
        return self.battery_level * 0.8


# --- Demonstrating Polymorphism ---

# Create a list (`fleet`) containing three different types of vehicle objects, all at 80% battery
fleet = [
    ElectricVehicle("SEDAN-01", 80),                    # Uses ElectricVehicle.calculate_range()
    DeliveryVan("VAN-01", 80, cargo_weight_kg=400),     # Uses DeliveryVan.calculate_range()
    ElectricScooter("SCOOT-01", 80),                    # Uses ElectricScooter.calculate_range()
]

# Loop through every vehicle object in the `fleet` list.
# Polymorphism in action: We call the exact same method (`vehicle.calculate_range()`) on each object,
# and Python automatically knows which version of the formula to run based on the object's class!
for vehicle in fleet:
    # `:.1f` formats the floating-point range number to display 1 digit after the decimal point
    print(f"{vehicle.vehicle_id} range: {vehicle.calculate_range():.1f} km")