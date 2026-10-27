# Allows modern type hinting features (like using `list[ElectricVehicle]`) in older Python versions
from __future__ import annotations

# ABC stands for Abstract Base Class. It lets us create "blueprint" classes that cannot be used directly.
from abc import ABC, abstractmethod


def normalize_battery(level: int) -> int:
    """
    Validates a battery level and caps it at a maximum of 100%.
    
    Args:
        level (int): The desired battery percentage.
        
    Returns:
        int: A valid battery percentage between 0 and 100.
    """
    # Check if the input is strictly an integer (note: in Python, `type(level) is not int` also rejects booleans)
    if type(level) is not int:
        raise TypeError("battery_level must be an integer")
    
    # Prevent negative battery percentages
    if level < 0:
        raise ValueError("battery_level cannot be negative")
    
    # `min(100, level)` ensures that if `level` is over 100 (e.g., 120), it gets capped at 100.
    return min(100, level)


def validate_charge(amount: int) -> None:
    """
    Checks if the amount of charge being added is a valid non-negative integer.
    This function returns `None` because it only checks for errors.
    """
    if type(amount) is not int:
        raise TypeError("charge amount must be an integer")
    if amount < 0:
        raise ValueError("charge amount cannot be negative")


class ElectricVehicle(ABC):
    """
    An Abstract Base Class (blueprint) representing a generic Electric Vehicle.
    
    Because it inherits from `ABC` and has `@abstractmethod` decorators, you CANNOT create 
    a generic `ElectricVehicle` directly. You must create a specific child class (like ElectricSedan).
    """

    def __init__(self, vehicle_id: str, model: str, battery_level: int):
        """
        The constructor method that runs automatically when a new vehicle object is created.
        """
        self.vehicle_id = vehicle_id        # Unique ID (e.g., "EV-101")
        self.model = model                  # Model name (e.g., "FleetSedan X")
        # Assigning `self.battery_level` here automatically triggers the `@battery_level.setter` method below!
        self.battery_level = battery_level
    
    @property
    def battery_level(self) -> int:
        """
        A 'getter' method (Encapsulation). 
        Allows outside code to safely read `vehicle.battery_level` while keeping 
        the actual data (`__battery_level`) hidden and protected inside the class.
        """
        # The double underscore `__` makes this attribute private so it cannot be accidentally changed from outside
        return self.__battery_level

    @battery_level.setter
    def battery_level(self, value: int) -> None:
        """
        A 'setter' method (Encapsulation).
        Intercepts any attempt to change `self.battery_level = value` and runs 
        validation rules (`normalize_battery`) before saving it to the private attribute.
        """
        self.__battery_level = normalize_battery(value)

    def charge(self, amount: int, fast_charge: bool = False) -> None:
        """
        Charges the vehicle's battery.
        
        Notice `fast_charge: bool = False`. Having a default value (`= False`) allows you to call 
        this method in two ways: `vehicle.charge(10)` OR `vehicle.charge(10, fast_charge=True)`.
        """
        print(f"[{self.vehicle_id}] Running Parent Class Electric Vehicle Charge Method")
        
        # 1. Validate inputs before changing anything
        validate_charge(amount)
        if type(fast_charge) is not bool:
            raise TypeError("fast_charge must be a bool")
        
        # 2. Update the battery level (this triggers the `@battery_level.setter`, which caps it at 100%)
        self.battery_level = self.battery_level + amount
        
        # 3. Determine charging mode label and power rate
        mode = "FAST" if fast_charge else "STANDARD"
        
        # Illustrative mode rating, not a simulated charging-time calculation.
        # Calls `self.charging_rate_kw()`, which belongs to whichever child class (Sedan, Van, Scooter) is being charged!
        rate = self.charging_rate_kw() if fast_charge else self.charging_rate_kw() / 2
        
        # `:.1f` formats the number to show 1 decimal place (e.g., 60.0)
        print(f"[{self.vehicle_id}] {rate} ({rate:.1f} kW mode) -> Battery: {self.battery_level}%")

    @abstractmethod
    def calculate_range(self) -> float:
        """
        Abstract Method: Every child class (Sedan, Van, Scooter) is FORCED to write 
        its own version of this method to calculate how far it can drive.
        """
        raise NotImplementedError

    @abstractmethod
    def charging_rate_kw(self) -> int:
        """
        Abstract Method: Every child class is FORCED to write its own version 
        of this method to return its maximum charging power in kilowatts (kW).
        """
        raise NotImplementedError


class ElectricSedan(ElectricVehicle):
    """
    A child class representing an Electric Sedan.
    It inherits `__init__`, `battery_level`, and `charge` directly from `ElectricVehicle`.
    """

    def calculate_range(self) -> float:
        """Calculates range: A sedan gets 3.5 km for every 1% of battery."""
        return self.battery_level * 3.5

    def charging_rate_kw(self) -> int:
        """Returns the max charging speed for a sedan (120 kW)."""
        return 120


class DeliveryVan(ElectricVehicle):
    """
    A child class representing a Delivery Van.
    Adds a new attribute (`cargo_weight_kg`) that affects its driving range.
    """

    def __init__(self, vehicle_id: str, model: str, battery_level: int,
                 cargo_weight_kg: int):
        """
        Initializes the Delivery Van. Uses `super().__init__()` to let the parent 
        class handle `vehicle_id`, `model`, and `battery_level`, then sets up `cargo_weight_kg`.
        """
        # Call the parent class (ElectricVehicle) constructor
        super().__init__(vehicle_id, model, battery_level)
        
        # Validate the van-specific cargo weight
        if type(cargo_weight_kg) is not int or cargo_weight_kg < 0:
            raise ValueError("cargo_weight_kg must be a non-negative integer")
        self.cargo_weight_kg = cargo_weight_kg

    def calculate_range(self) -> float:
        """
        Calculates range: Gets 2.5 km per 1% of battery, minus 0.05 km for every kg of cargo.
        `max(0.0, ...)` ensures the calculated range never drops below 0.0 km if the cargo is super heavy.
        """
        return max(0.0, self.battery_level * 2.5 - self.cargo_weight_kg * 0.05)

    def charging_rate_kw(self) -> int:
        """Returns the max charging speed for a delivery van (150 kW)."""
        return 150


class ElectricScooter(ElectricVehicle):
    """
    A child class representing a lightweight Electric Scooter.
    Adds a `helmet_included` attribute.
    """

    def __init__(self, vehicle_id: str, model: str, battery_level: int,
                 helmet_included: bool = True):
        """Initializes the Scooter and checks if a helmet is included."""
        super().__init__(vehicle_id, model, battery_level)
        
        if type(helmet_included) is not bool:
            raise TypeError("helmet_included must be a bool")
        self.helmet_included = helmet_included

    def calculate_range(self) -> float:
        """Calculates range: A small scooter gets 0.8 km for every 1% of battery."""
        return self.battery_level * 0.8

    def charging_rate_kw(self) -> int:
        """Returns the max charging speed for a scooter (3 kW)."""
        return 3


class RepeatedChargeDemo:
    """
    Demonstrates a common beginner pitfall in Python:
    Unlike languages like Java or C++, Python does NOT support traditional 'Method Overloading'
    (defining two methods with the exact same name but different parameters).
    
    If you define `def charge` twice in the same class, the second definition completely 
    erases and replaces the first one! (Instead, use default arguments like `fast_charge: bool = False`).
    """

    # First definition of `charge` (takes 1 argument)
    def charge(self, amount: int) -> str:  # noqa: F811 (tells code linters to ignore the duplicate name warning)
        return f"Standard +{amount}%"

    # Second definition of `charge` (takes 2 arguments) -> THIS OVERWRITES THE FIRST METHOD ABOVE!
    def charge(self, amount: int, fast_charge: bool) -> str:  # noqa: F811
        mode = "FAST" if fast_charge else "STANDARD"
        return f"{mode} +{amount}%"


def main() -> None:
    """
    Main function to test creating vehicles, calculating range, and charging.
    """
    # 1. Create instances (objects) of our three different vehicle child classes
    sedan = ElectricSedan("EV-101", "FleetSedan X", 80)
    van = DeliveryVan("VAN-01", "VoltHauler", 40, cargo_weight_kg=200)
    scooter = ElectricScooter("SCOOT-01", "CityGlide", 80, helmet_included=True)

    # 2. Put all different vehicles into one list (Polymorphism).
    # Even though they are different types, they are all `ElectricVehicle`s!
    fleet: list[ElectricVehicle] = [sedan, van, scooter]
    
    # Loop through each vehicle and call its specific `calculate_range` and `charging_rate_kw` methods
    for vehicle in fleet:
        print(
            f"{vehicle.vehicle_id} ({vehicle.model}) -> "
            f"range: {vehicle.calculate_range():.1f} km | "
            f"max rate: {vehicle.charging_rate_kw()} kW"
        )
    
    # 3. Charge each vehicle using the inherited `charge()` method from the parent class
    van.charge(10)       # Standard charge (since fast_charge defaults to False)
    sedan.charge(20)     # Standard charge (80% + 20% = 100%)
    scooter.charge(10)   # Standard charge (80% + 10% = 90%)
    
    # 4. Demonstrate why defining `def charge` twice in `RepeatedChargeDemo` fails
    try:
        # This will fail because the 1-argument `charge(amount)` was overwritten by the 2-argument `charge(amount, fast_charge)`
        RepeatedChargeDemo().charge(15)  # type: ignore[call-arg]
    except TypeError as exc:
        print(f"Repeated def charge(15) -> TypeError: {exc}")
    
    # 5. Charge the van further (Minimum is 0, Maximum is capped at 100)
    van.charge(15)                      # Uses default: fast_charge=False
    van.charge(15, fast_charge=True)    # Explicitly enables fast charging
    
    # Print the final battery level using the `@property` getter
    print(van.battery_level)


# This standard Python check ensures `main()` only runs if you execute this file directly 
# (and not if you import this file into another Python script).
if __name__ == "__main__":
    main()