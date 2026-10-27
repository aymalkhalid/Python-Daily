class ElectricVehicle:
    """
    A basic class (blueprint) representing an Electric Vehicle.
    
    This version demonstrates how classes work without data protection (encapsulation),
    showing how attributes like `battery_level` can be directly modified from outside.
    """

    def __init__(self, vehicle_id: str,
                 model: str, battery_level: int):
        """
        The constructor method (__init__) that runs automatically when a new 
        ElectricVehicle object is created.
        
        Args:
            vehicle_id (str): The unique identifier for the vehicle (e.g., "EV-101").
            model (str): The name/model of the vehicle (e.g., "FleetSedan X").
            battery_level (int): The starting battery percentage (e.g., 60).
        """
        # `self` refers to the specific object being created.
        # These lines save the passed-in values as attributes on the object.
        self.vehicle_id = vehicle_id        # Stores the vehicle's ID
        self.model = model                  # Stores the vehicle's model name
        self.battery_level = battery_level  # Stores the current battery percentage (public and unprotected)

    def charge(self, amount: int) -> None:
        """
        Increases the vehicle's battery level by a given amount and prints a status message.
        `-> None` indicates that this method performs an action (printing/updating) 
        rather than returning a value.
        
        Args:
            amount (int): The percentage of battery charge to add.
        """
        # `+=` is shorthand for: self.battery_level = self.battery_level + amount
        self.battery_level += amount
        
        # Prints a formatted string (f-string) showing the vehicle ID, charge added, and new total.
        # Two adjacent f-strings on separate lines are automatically joined together by Python.
        print(f"[{self.vehicle_id}] Charged +{amount}%."
              f" Battery: {self.battery_level}%")


# --- Creating Objects (Instances) from the Class Blueprint ---

# Create the first ElectricVehicle object named `sedan` with ID "EV-101", model "FleetSedan X", and 60% battery
sedan = ElectricVehicle("EV-101", "FleetSedan X", 60)

# Create a second, separate ElectricVehicle object named `van` with ID "EV-202", model "CargoVan Pro", and 45% battery
van = ElectricVehicle("EV-202", "CargoVan Pro", 45)

# Call the `charge` method on `sedan` to add 25% to its battery (60 + 25 = 85%)
sedan.charge(25)

# Because `battery_level` is a standard public attribute without a `@property` setter to validate it,
# external code can accidentally or intentionally set it to an impossible number like 9000%!
sedan.battery_level = 9000  # Unprotected!