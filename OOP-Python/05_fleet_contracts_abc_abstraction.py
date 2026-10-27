# Import ABC (Abstract Base Class) and abstractmethod from Python's built-in `abc` module.
# These tools allow us to create strict "blueprint" classes that enforce rules on child classes.
from abc import ABC, abstractmethod


class ElectricVehicle(ABC):
    """
    An Abstract Base Class (blueprint) representing a generic Electric Vehicle.
    
    By inheriting from `ABC` and using `@abstractmethod`, this class acts as a strict contract:
    1. You CANNOT create an `ElectricVehicle` object directly (e.g., `ElectricVehicle("EV-1", 50)` will fail).
    2. Any child class that inherits from `ElectricVehicle` MUST implement its own working versions 
       of `calculate_range()` and `charging_rate_kw()`.
    """

    def __init__(self, vehicle_id: str, battery_level: int):
        """
        The constructor method (__init__) that sets up the shared attributes for any vehicle.
        Child classes will inherit and use this constructor.
        
        Args:
            vehicle_id (str): The unique identifier for the vehicle (e.g., "VAN-01").
            battery_level (int): The starting battery percentage (e.g., 90).
        """
        self.vehicle_id = vehicle_id        # Stores the vehicle's unique ID
        self.battery_level = battery_level  # Stores the starting battery percentage

    @abstractmethod
    def calculate_range(self) -> float:
        """
        Abstract Method: Acts as a placeholder rule requiring every child class 
        to define how its specific driving range (in kilometers) is calculated.
        
        Returns:
            float: The estimated driving range in kilometers.
        """
        # `pass` is a null statement (do nothing) used here because the parent class 
        # doesn't have a formula—each child class will provide its own!
        pass

    @abstractmethod
    def charging_rate_kw(self) -> int:
        """
        Abstract Method: Acts as a placeholder rule requiring every child class 
        to define its maximum charging power in kilowatts (kW).
        
        Returns:
            int: The maximum charging rate in kW.
        """
        pass


class DeliveryVan(ElectricVehicle):
    """
    A concrete child class (subclass) representing a Delivery Van that inherits from `ElectricVehicle`.
    
    Because it inherits from `ElectricVehicle`, it automatically gets the `__init__` method, 
    and it fulfills the abstract class contract by implementing both `calculate_range()` 
    and `charging_rate_kw()`.
    """

    def calculate_range(self) -> float:
        """
        Implements the required `calculate_range` method for a Delivery Van.
        
        Returns:
            float: The estimated range (assumes 2.2 km per 1% of battery).
        """
        # Multiplies battery percentage by 2.2 (e.g., 90 * 2.2 = 198.0 km)
        return self.battery_level * 2.2

    def charging_rate_kw(self) -> int:
        """
        Implements the required `charging_rate_kw` method for a Delivery Van.
        
        Returns:
            int: The van's maximum charging speed (150 kW).
        """
        return 150


# --- Testing Abstraction and Concrete Child Classes ---

# Create an instance of the concrete child class `DeliveryVan` with ID "VAN-01" and 90% battery.
# (Since `DeliveryVan` didn't define its own `__init__`, it automatically uses `ElectricVehicle.__init__`)
van = DeliveryVan("VAN-01", 90)

# Print the van's ID, calculated range, and charging rate by calling its implemented methods
print(f"{van.vehicle_id}: {van.calculate_range()} km | {van.charging_rate_kw()} kW")