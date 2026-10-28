"""
    Episode 7: Dynamic typing, duck typing, and what type hints actually do.

    This runnable module demonstrates three beginner-friendly Python concepts using
    our Electric Vehicle Fleet:
    1. Dynamic typing and name rebinding: runtime types belong to objects, not
    variable names.
    2. Duck typing: the range-report loop looks up attributes and methods directly
    at the point of use without requiring a shared parent class.
    3. Type hints versus explicit validation: annotations guide static tools, while
    runtime checks require explicit code.
"""

# Allow forward-reference type annotations across all supported Python 3.10+ versions.
from __future__ import annotations

# Import ABC and abstractmethod to define the abstract fleet blueprint.
from abc import ABC, abstractmethod


# Validate and cap a battery percentage before storing it on a vehicle.
def normalize_battery(level: int) -> int:
    """Validate that level is a non-negative integer and cap values above 100.

    Raises TypeError if level is not an int (excluding bool), and ValueError
    if level is below 0. Returns an integer percentage between 0 and 100.
    """
    # Explicit runtime check: reject strings, floats, and booleans.
    if type(level) is not int:
        raise TypeError("battery_level must be an integer")
    # Reject negative percentages before storing or updating state.
    if level < 0:
        raise ValueError("battery_level cannot be negative")
    # Cap valid integer percentages at 100%.
    if level > 100:
        return 100
    return level


# Check that a requested charge amount is a non-negative integer.
def validate_charge(amount: int) -> None:
    """Verify that the percentage-point charge amount is a non-negative int.

    Raises TypeError for non-integers and ValueError for negative numbers.
    """
    # Explicit runtime check: reject non-integer charge amounts.
    if type(amount) is not int:
        raise TypeError("charge amount must be an integer")
    # Reject negative charge amounts so charging cannot drain the battery.
    if amount < 0:
        raise ValueError("charge amount cannot be negative")


# Define the abstract blueprint shared by all core fleet vehicles.
class ElectricVehicle(ABC):
    """Abstract base class for core fleet vehicles.

    Stores vehicle_id, model, and a validated battery_level percentage.
    Concrete subclasses must implement calculate_range and charging_rate_kw.
    """

    # Set up the shared attributes on a newly created vehicle instance.
    def __init__(self, vehicle_id: str, model: str, battery_level: int):
        """Initialize the vehicle's ID, model name, and starting battery level."""
        self.vehicle_id = vehicle_id
        self.model = model
        # Assigning to self.battery_level runs the validated property setter below.
        self.battery_level = battery_level

    # Expose battery_level as a readable attribute backed by private storage.
    @property
    def battery_level(self) -> int:
        """Return the current integer battery percentage (0 to 100)."""
        return self.__battery_level

    # Validate every assignment to vehicle.battery_level through normalize_battery.
    @battery_level.setter
    def battery_level(self, value: int) -> None:
        """Validate and store a new integer battery percentage."""
        self.__battery_level = normalize_battery(value)

    # Add percentage points to the battery and display an illustrative status line.
    def charge(self, amount: int, fast_charge: bool = False) -> None:
        """Add percentage points to battery_level and print the mode and new charge.

        Both standard and fast modes add the same percentage points; fast_charge
        selects the full illustrative kW rating instead of half.
        """
        # Verify the requested percentage-point increase before mutating state.
        validate_charge(amount)
        # Ensure fast_charge is an actual boolean value.
        if type(fast_charge) is not bool:
            raise TypeError("fast_charge must be a bool")
        # Update the battery level through the validated property setter.
        self.battery_level = self.battery_level + amount
        # Select the display label and illustrative power rating explicitly.
        if fast_charge:
            mode = "FAST"
            rate = float(self.charging_rate_kw())
        else:
            mode = "STANDARD"
            rate = self.charging_rate_kw() / 2
        # Build the status message first, then display it in the terminal.
        status_message = (
            f"[{self.vehicle_id}] {mode} ({rate:.1f} kW mode) -> "
            f"Battery: {self.battery_level}%"
        )
        print(status_message)

    # Require every concrete fleet subclass to provide its own range formula.
    @abstractmethod
    def calculate_range(self) -> float:
        """Return the illustrative travel range in kilometers."""
        raise NotImplementedError

    # Require every concrete fleet subclass to declare its fast-charge kW rating.
    @abstractmethod
    def charging_rate_kw(self) -> int:
        """Return the illustrative fast-charging power rating in kilowatts."""
        raise NotImplementedError


# Concrete subclass representing our core passenger sedan (EV-101).
class ElectricSedan(ElectricVehicle):
    """Concrete passenger sedan implementing the ElectricVehicle contract."""

    # Compute the sedan's illustrative range at 3.5 km per battery percent.
    def calculate_range(self) -> float:
        """Return illustrative range in km (battery_level * 3.5)."""
        return self.battery_level * 3.5

    # Provide the sedan's illustrative fast-charging rating in kilowatts.
    def charging_rate_kw(self) -> int:
        """Return 120 kW as the illustrative fast-charge rating."""
        return 120


# Concrete subclass representing our cargo delivery van (VAN-01).
class DeliveryVan(ElectricVehicle):
    """Concrete delivery van that accounts for cargo weight in its range formula."""

    # Set up the van's core vehicle fields plus its non-negative cargo weight.
    def __init__(
        self,
        vehicle_id: str,
        model: str,
        battery_level: int,
        cargo_weight_kg: int,
    ):
        """Initialize a delivery van with its cargo weight in kilograms."""
        super().__init__(vehicle_id, model, battery_level)
        # Validate that cargo_weight_kg is a non-negative integer.
        if type(cargo_weight_kg) is not int or cargo_weight_kg < 0:
            raise ValueError("cargo_weight_kg must be a non-negative integer")
        self.cargo_weight_kg = cargo_weight_kg

    # Compute the van's illustrative range with a cargo-weight penalty.
    def calculate_range(self) -> float:
        """Return illustrative range in km, subtracting 0.05 km per kg of cargo."""
        raw_range = self.battery_level * 2.5 - self.cargo_weight_kg * 0.05
        if raw_range < 0.0:
            return 0.0
        return raw_range

    # Provide the van's illustrative fast-charging rating in kilowatts.
    def charging_rate_kw(self) -> int:
        """Return 150 kW as the illustrative fast-charge rating."""
        return 150


# Concrete subclass representing our urban scooter (SCOOT-01).
class ElectricScooter(ElectricVehicle):
    """Concrete electric scooter with an optional helmet flag."""

    # Set up the scooter's core fields and record whether a helmet is included.
    def __init__(
        self,
        vehicle_id: str,
        model: str,
        battery_level: int,
        helmet_included: bool = True,
    ):
        """Initialize an electric scooter and validate its helmet_included flag."""
        super().__init__(vehicle_id, model, battery_level)
        # Validate that helmet_included is a boolean.
        if type(helmet_included) is not bool:
            raise TypeError("helmet_included must be a bool")
        self.helmet_included = helmet_included

    # Compute the scooter's illustrative range at 0.8 km per battery percent.
    def calculate_range(self) -> float:
        """Return illustrative range in km (battery_level * 0.8)."""
        return self.battery_level * 0.8

    # Provide the scooter's illustrative fast-charging rating in kilowatts.
    def charging_rate_kw(self) -> int:
        """Return 3 kW as the illustrative fast-charge rating."""
        return 3


# Standalone partner class outside the ElectricVehicle inheritance tree.
class ChargingDrone:
    """Temporary third-party guest; not an ElectricVehicle subclass.

    Provides matching vehicle_id, model, battery_level, and calculate_range
    attributes and methods so it can participate in duck-typed range reporting.
    """

    # Set up the drone's ID, model name, and validated battery percentage.
    def __init__(self, vehicle_id: str, model: str, battery_level: int):
        """Initialize the partner drone with a validated battery percentage."""
        self.vehicle_id = vehicle_id
        self.model = model
        # Assigning to self.battery_level triggers the property setter below.
        self.battery_level = battery_level

    # Read the drone's battery percentage from private storage.
    @property
    def battery_level(self) -> int:
        """Return the drone's integer battery percentage (0 to 100)."""
        return self.__battery_level

    # Reuse normalize_battery so the drone enforces the same integer policy.
    @battery_level.setter
    def battery_level(self, value: int) -> None:
        """Validate and store the drone's battery percentage."""
        self.__battery_level = normalize_battery(value)

    # Compute the drone's illustrative range at 0.5 km per battery percent.
    def calculate_range(self) -> float:
        """Return illustrative range in km (battery_level * 0.5)."""
        return self.battery_level * 0.5


# Helper with a type hint only—no runtime check is inside this function.
def echo_level(level: int) -> int:
    """Return level unchanged to show that type hints do not validate at runtime."""
    return level


# Run the Episode 7 demonstration of name rebinding, duck typing, and type hints.
def main() -> None:
    """Execute the Episode 7 fleet demonstration and print the 8-line transcript."""
    # Create the three core fleet vehicles starting fresh at 80% battery.
    sedan = ElectricSedan("EV-101", "FleetSedan X", 80)
    van = DeliveryVan("VAN-01", "VoltHauler", 80, cargo_weight_kg=200)
    scooter = ElectricScooter("SCOOT-01", "CityGlide", 80, helmet_included=True)

    # Bind the variable name 'unit' to our DeliveryVan object and display its runtime class name.
    unit: ElectricVehicle = van
    unit_type_name = type(unit).__name__
    first_binding_line = f"unit -> {unit_type_name}"
    print(first_binding_line)

    # Rebind the same variable name 'unit' to our ElectricScooter object; VAN-01 stays unchanged.
    unit = scooter
    unit_type_name = type(unit).__name__
    second_binding_line = f"unit -> {unit_type_name}"
    print(second_binding_line)

    # Create the independent partner drone (not an ElectricVehicle subclass).
    drone = ChargingDrone("DRONE-01", "SkyCharge Mini", 80)

    # Combine the three core fleet vehicles and the temporary guest drone in one list.
    fleet = [sedan, van, scooter, drone]

    # Duck typing: Python looks up .vehicle_id, .model, and .calculate_range() on each object at point of use.
    for vehicle in fleet:
        range_km = vehicle.calculate_range()
        report_line = f"{vehicle.vehicle_id} ({vehicle.model}) range: {range_km:.1f} km"
        print(report_line)

    # Pass a string to echo_level: the : int hint is not enforced by Python at runtime.
    value = echo_level("80")  # type: ignore[arg-type]
    returned_type_name = type(value).__name__
    hint_demo_line = f"Annotation-only demo returned: {returned_type_name}"
    print(hint_demo_line)

    # Attempt to assign a string to sedan.battery_level: explicit code in normalize_battery raises TypeError.
    try:
        sedan.battery_level = "80"  # type: ignore[assignment]
    except TypeError:
        rejection_message = "Fleet validator: string battery rejected"
        print(rejection_message)


if __name__ == "__main__":
    main()
