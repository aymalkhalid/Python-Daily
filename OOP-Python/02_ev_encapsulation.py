class ElectricVehicle:
    """
    A class representing an Electric Vehicle that uses Encapsulation.
    
    By using a private attribute (`__battery_level`) along with `@property` (getter) 
    and `@battery_level.setter` methods, this class protects the battery level 
    from being set to invalid numbers (like negative values or values over 100%).
    """

    def __init__(self, vehicle_id: str, model: str, battery_level: int):
        """
        The constructor method (__init__) that initializes a new ElectricVehicle object.
        
        Args:
            vehicle_id (str): The unique identifier for the vehicle (e.g., "EV-101").
            model (str): The name/model of the vehicle (e.g., "FleetSedan X").
            battery_level (int): The starting battery percentage (e.g., 80).
        """
        self.vehicle_id = vehicle_id          # Public attribute storing the vehicle's ID
        self.model = model                    # Public attribute storing the vehicle's model name
        
        # Initialize the private attribute (`__` double underscore hides it from outside the class)
        self.__battery_level = 0
        
        # Assigning to `self.battery_level` (without underscores) automatically calls 
        # the `@battery_level.setter` method below to validate the initial value!
        self.battery_level = battery_level  # Routed through setter

    @property
    def battery_level(self) -> int:
        """
        The 'getter' method for `battery_level`.
        
        The `@property` decorator allows external code to read `ev.battery_level` 
        like a normal variable while safely retrieving the hidden `self.__battery_level`.
        
        Returns:
            int: The current protected battery percentage.
        """
        return self.__battery_level

    @battery_level.setter
    def battery_level(self, value: int) -> None:
        """
        The 'setter' method for `battery_level`.
        
        The `@battery_level.setter` decorator intercepts any attempt to assign a value 
        to `self.battery_level` (or `ev.battery_level = ...`). It checks that the value 
        is valid before updating the private `self.__battery_level` attribute.
        
        Args:
            value (int): The new battery level percentage being assigned.
            
        Raises:
            ValueError: If someone tries to set the battery level below 0%.
        """
        # Prevent negative battery values by raising an error
        if value < 0:
            raise ValueError("Battery cannot drop below 0%.")
        
        # `min(value, 100)` compares `value` and `100`, picking the smaller number.
        # If `value` is 130, `min(130, 100)` returns 100, safely capping the battery at 100%!
        self.__battery_level = min(value, 100)

    def charge(self, amount: int) -> None:
        """
        Adds charge to the vehicle's battery if the charge amount is positive.
        
        Args:
            amount (int): The percentage of battery charge to add.
        """
        # Only update the battery if a positive amount of charge is provided
        if amount > 0:
            # `self.battery_level += amount` reads the current level via the `@property` getter,
            # adds `amount` to it, and sends the result into `@battery_level.setter` (capping it at 100).
            self.battery_level += amount


# This block only runs when this Python file is executed directly
if __name__ == "__main__":
    # Create an ElectricVehicle instance starting at 80% battery (validated through the setter)
    ev = ElectricVehicle("EV-101", "FleetSedan X", 80)
    
    # Add 50% charge (80 + 50 = 130, which the setter automatically caps at 100)
    ev.charge(50)
    
    # Read and print the battery level using the `@property` getter
    print(ev.battery_level)  # Safely capped at 100