class ElectricVehicle:
    """
    The parent (base) class representing a general Electric Vehicle.
    
    This class provides shared attributes (`vehicle_id`, `model`, `battery_level`) 
    and methods (`charge`) that child classes can inherit and reuse without 
    having to rewrite them.
    """

    def __init__(self, vehicle_id: str, model: str, battery_level: int):
        """
        The constructor method (__init__) that initializes a new ElectricVehicle.
        
        Args:
            vehicle_id (str): The unique identifier for the vehicle (e.g., "VAN-01").
            model (str): The name/model of the vehicle (e.g., "VoltHauler").
            battery_level (int): The starting battery percentage.
        """
        self.vehicle_id = vehicle_id  # Stores the vehicle's unique ID
        self.model = model            # Stores the vehicle's model name
        
        # Clamps (restricts) the starting battery level between 0 and 100:
        # 1. `min(battery_level, 100)` caps the value so it cannot exceed 100.
        # 2. `max(0, ...)` ensures the value cannot be lower than 0 (no negative battery).
        self.battery_level = max(0, min(battery_level, 100))

    def charge(self, amount: int) -> None:
        """
        Charges the vehicle's battery by adding `amount`, capped at a maximum of 100%.
        
        Args:
            amount (int): The percentage of battery charge to add.
        """
        # Adds `amount` to the current battery level, using `min(100, ...)` to prevent going over 100%
        self.battery_level = min(100, self.battery_level + amount)


class DeliveryVan(ElectricVehicle):
    """
    A child (subclass) that inherits from `ElectricVehicle`.
    
    Putting `(ElectricVehicle)` in the class definition means `DeliveryVan` automatically 
    gets `vehicle_id`, `model`, `battery_level`, and the `charge()` method from the parent class, 
    while adding its own cargo-specific features (`cargo_weight_kg` and `load_cargo()`).
    """

    def __init__(self, vehicle_id: str, model: str, battery_level: int, cargo_weight_kg: int):
        """
        Initializes a new DeliveryVan object.
        
        Args:
            vehicle_id (str): The unique identifier for the van.
            model (str): The model name of the van.
            battery_level (int): The starting battery percentage.
            cargo_weight_kg (int): The initial weight of cargo in kilograms.
        """
        # `super().__init__(...)` calls the parent class (`ElectricVehicle`) constructor 
        # so it can set up `vehicle_id`, `model`, and `battery_level` for us.
        super().__init__(vehicle_id, model, battery_level)
        
        # Sets up the new attribute that is specific only to DeliveryVan
        self.cargo_weight_kg = cargo_weight_kg

    def load_cargo(self, weight: int) -> None:
        """
        Adds extra cargo weight to the delivery van.
        
        Args:
            weight (int): The additional cargo weight in kilograms to add.
        """
        # Increases `cargo_weight_kg` by `weight` (shorthand for: self.cargo_weight_kg = self.cargo_weight_kg + weight)
        self.cargo_weight_kg += weight


class ElectricScooter(ElectricVehicle):
    """
    Another child (subclass) that inherits from `ElectricVehicle`.
    
    It reuses the parent class setup for ID, model, and battery, and adds 
    a scooter-specific attribute (`helmet_included`).
    """

    def __init__(self, vehicle_id: str, model: str, battery_level: int, helmet_included: bool):
        """
        Initializes a new ElectricScooter object.
        
        Args:
            vehicle_id (str): The unique identifier for the scooter.
            model (str): The model name of the scooter.
            battery_level (int): The starting battery percentage.
            helmet_included (bool): True if a helmet comes with the scooter, False otherwise.
        """
        # Calls the parent class (`ElectricVehicle`) constructor to handle the shared attributes
        super().__init__(vehicle_id, model, battery_level)
        
        # Sets up the new attribute specific only to ElectricScooter
        self.helmet_included = helmet_included


# --- Testing Inheritance and Child Classes ---

# 1. Create a `DeliveryVan` object with 60% battery and 250kg of starting cargo
van = DeliveryVan("VAN-01", "VoltHauler", 60, cargo_weight_kg=250)
print(f"Init  -> id={van.vehicle_id}, model={van.model}, battery={van.battery_level}%, cargo={van.cargo_weight_kg}kg")

# 2. Call the inherited `charge()` method on `van` (defined in `ElectricVehicle`, used by `DeliveryVan`)
van.charge(30)
print(f"After charge(30) -> battery={van.battery_level}%")

# 3. Call the van's own `load_cargo()` method to add 100kg of cargo (250 + 100 = 350kg)
van.load_cargo(100)
print(f"After load_cargo(100) -> cargo={van.cargo_weight_kg}kg")

# 4. Create an `ElectricScooter` object with 80% battery and a helmet included
scooter = ElectricScooter("SCT-09", "ZipSpark", 80, helmet_included=True)
print(f"Scooter -> id={scooter.vehicle_id}, battery={scooter.battery_level}%, helmet={scooter.helmet_included}")