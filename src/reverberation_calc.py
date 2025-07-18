import numpy as np
import warnings

class room:
    """
    Defines a "room" object with properties such as volume, temperature, pressure, relative humidity, and speed of sound.

    Parameters
    ----------
    volume : int or float
        The volume of the room in m$^2$.

    Attributes
    ----------
    volume : int or float
        The volume of the room in m$^2$.
    temperature : int or float
        The temperature of the room in °C (default is 20 °C).
    pressure : int or float
        The pressure of the room in kPa (default is 101.325 kPa).
    rel_humidity : int or float
        The relative humidity of the room in % (default is 50 %).
    height : int or float or None
        The height of the room in m (default is None).
    c : int or float
        The speed of sound in air in m/s, calculated based on temperature and relative humidity.
    """

    def __init__(self, volume):
        """
        Initializes a room object with a specified volume and default values for temperature, pressure, relative humidity, and speed of sound.

        Parameters
        ----------
        volume : int or float 
            The volume of the room in m$^2$.

        Raises
        ------
        TypeError
            If the volume is not a number.
        ValueError
            If the volume is not positive.
        """
        if not isinstance(volume, (int, float)):
            raise TypeError("Volume must be an integer or float.")
        if volume <= 0:
            raise ValueError("Volume must be a positive value.")
        
        self.volume = volume
        self.temperature = 20           # Celsius
        self.pressure = 101.325         # kPa
        self.rel_humidity = 50          # percentage
        self.height = None              # meters
        self.c = self.get_c()           # Speed of sound in air in m/s

    def set_height(self, height):
        """
        Sets the height of the room in m.
        
        Parameters
        ----------
        height : int or float
            The height of the room in m.

        Raises
        -------
        TypeError
            If the height is not a number.
        ValueError
            If the height is not positive.
        """
        if not isinstance(height, (int, float)):
            raise TypeError("Height must be an integer or float.")
        if height <= 0:
            raise ValueError("Height must be a positive value.")
        self.height = height

    def get_height(self):
        """
        Returns the height of the room in m.

        Returns
        -------
        float or None
            The height of the room in m.
        """
        return self.height

    def set_volume(self, volume):
        """
        Sets the volume of the room in m$^2$.
        
        Parameters
        ----------
        volume : int or float
            The volume of the room in m$^2$.

        Raises
        -------
        TypeError
            If the volume is not an integer.
        ValueError
            If the volume is not a positive integer.
        """
        if not isinstance(volume, (int, float)):
            raise TypeError("Volume must be an integer or float.")
        if volume <= 0:
            raise ValueError("Volume must be a positive value.")
        self.volume = volume

    def get_volume(self):
        """
        Returns the volume of the room in m$^2$.

        Returns
        -------
        float
            The volume of the room in m$^2$.
        """
        return self.volume
    
    def set_temperature(self, temperature):
        """
        Sets the temperature of the room in °C.
        
        Parameters
        ----------
        temperature : int or float
            The temperature of the room in °C.

        Raises
        -------
        TypeError
            If the temperature is not a numeric value.
        ValueError
            If the temperature is not above absolute zero (-273.15 °C).
        """
        if not isinstance(temperature, (int, float)):
            raise TypeError("Temperature must be an integer or float.")
        if temperature < -273.15:
            raise ValueError("Temperature must be above absolute zero (-273.15 °C).")
        self.temperature = temperature

    def get_temperature(self):
        """
        Returns the temperature of the room in °C.

        Returns
        -------
        float
            The temperature of the room in °C.
        """
        return self.temperature
    
    def set_pressure(self, pressure):
        """
        Sets the pressure of the room in kPa.

        Parameters
        ----------
        pressure : int or float
            The pressure of the room in kPa.

        Raises
        -------
        TypeError
            If the pressure is not an integer or float.
        ValueError
            If the pressure is not a positive integer.
        """
        if not isinstance(pressure, (int, float)):
            raise TypeError("Pressure must be an integer or float.")
        if pressure <= 0:
            raise ValueError("Pressure must be a positive value.")
        self.pressure = pressure

    def get_pressure(self):
        """
        Returns the pressure of the room in kPa.

        Returns
        -------
        float
            The pressure of the room in kPA.
        """
        return self.pressure
    
    def set_rel_humidity(self, rel_humidity):
        """
        Sets the relative humidity of the room in %.

        Parameters
        ----------
        rel_humidity : int or float
            The relative humidity of the room in %.

        Raises
        -------
        TypeError
            If the relative humidity is not an integer or float.
        ValueError
            If the relative humidity is not in the range of 0 % - 100 %.
        """
        if not isinstance(rel_humidity, (int, float)):
            raise TypeError("Relative humidity must be an integer or float.")
        if rel_humidity < 0 or rel_humidity > 100:
            raise ValueError("Relative humidity must be between 0 and 100 %.")
        self.rel_humidity = rel_humidity

    def get_rel_humidity(self):
        """
        Returns the relative humidity of the room in %.

        Returns
        -------
        float
            The relative humidity of the room in %.
        """
        return self.rel_humidity
    
    def get_c(self):
        """
        Calculates and returns the speed of sound in air based on the current temperature and relative humidity according to DIN EN ISO 354.

        Returns
        -------
        float
            The speed of sound in air in m/s.
        """
        self.c = (331.6 + 0.6 * self.get_temperature())# * (1 + (self.get_rel_humidity() / 100)) ** 0.5 # automatisch ausgefüllt, kp wieso
        return self.c



class air_damp:
    """
    Defines an "air_damp" object that calculates the sound absorption coefficient $m$ in 1/m of air based on frequency, temperature, humidity, and pressure according to DIN EN ISO 354, based on $alpha$ from ISO 9613-1.

    Parameters
    ----------
    frequency : list
        A list of frequencies in Hz for which the sound absorption coefficient is calculated.

    Attributes
    ----------
    pressure : int or float, optional
        The pressure in kPa (default is 101.325 kPa).
    ref_pressure : int or float, optional
        The reference pressure in kPa (default is 101.325 kPa).
    rel_humidity : int or float, optional
        The relative humidity in % (default is 50 %).
    abs_humidity : int or float, optional
        The absolute humidity as molar concentration of water vapour in air in % according to ISO 9613-1 Annex B.
    temperature : int or float, optional
        The temperature in Celsius (default is 20°C).
    ref_temperature : int or float, optional
        The reference temperature in Kelvin (default is 293.15 °K, which is 20 °C).
    alpha : list
        A list of sound absorption coefficients in dB/m, calculated based on the frequency, temperature, humidity and pressure.
    m : list
        A list of sound absorption coefficients in 1/m, calculated from alpha.
    """

    def __init__(self, frequency):
        """
        Initializes an air_damp object with a specified frequency and default values for pressure, relative humidity, temperature, and reference temperature.
        
        Parameters
        ----------
        frequency : list of int or float
            A list of frequencies in Hz for which the sound absorption coefficient is calculated.

        Raises
        -------
        TypeError
            If the frequency is not a list.
        ValueError
            If the frequency is not a list or if it contains non-numeric values.
        ValueError
            If the frequency list is empty.
        ValueError
            If the frequency list contains negative values.
        """
        if not isinstance(frequency, list):
            raise TypeError("Frequency must be a list.")
        if not all(isinstance(f, (int, float)) for f in frequency):
            raise ValueError("Frequency must be a list of numeric values.")
        if len(frequency) == 0:
            raise ValueError("Frequency list cannot be empty.")
        if any(f < 0 for f in frequency):
            raise ValueError("Frequency values must be non-negative.")

        self.frequency = frequency
        self.pressure = 101.325
        self.ref_pressure = 101.325
        self.rel_humidity = 50          # percentage
        self.temperature = 20           # Celsius
        self.ref_temperature = 293.15   # Kelvin
        self.calculate_abs_humidity()
        self.coefficient = self.calculate_coefficient()
    
    def set_frequency(self, frequency):
        """
        Sets the frequency in Hz for which the sound absorption coefficient is calculated.

        Parameters
        ----------
        frequency : list of int or float
            A list of frequencies in Hz.

        Raises
        -------
        TypeError
            If the frequency is not a list.
        ValueError
            If the frequency is not a list or if it contains non-numeric values.
        ValueError
            If the frequency list is empty.
        ValueError
            If the frequency list contains negative values.
        """
        if not isinstance(frequency, list):
            raise TypeError("Frequency must be a list.")
        if not all(isinstance(f, (int, float)) for f in frequency):
            raise ValueError("Frequency must be a list of numeric values.")
        if len(frequency) == 0:
            raise ValueError("Frequency list cannot be empty.")
        if any(f < 0 for f in frequency):
            raise ValueError("Frequency values must be non-negative.")

        self.frequency = frequency    

    def set_pressure(self, pressure):
        """
        Sets the pressure in kPa for the sound absorption coefficient calculation.

        Parameters
        ----------
        pressure : int or float
            The pressure in kPa.

        Raises
        -------
        TypeError
            If the pressure is not a numeric value.
        ValueError
            If the pressure is not a positive numeric value.
        """
        if not isinstance(pressure, (int, float)):
            raise TypeError("Pressure must be an integer or float.")
        if pressure <= 0:
            raise ValueError("Pressure must be a positive value.")
        self.pressure = pressure
    
    def set_temperature(self, temperature):
        """
        Sets the temperature in Celsius for the sound absorption coefficient calculation.

        Parameters
        ----------
        temperature : int or float
            The temperature in °C.

        Raises
        -------
        TypeError
            If the temperature is not a numeric value.
        ValueError
            If the temperature is not above absolute zero (-273.15 °C).
        """
        if not isinstance(temperature, (int, float)):
            raise TypeError("Temperature must be an integer or float.")
        if temperature < -273.15:
            raise ValueError("Temperature must be above absolute zero (-273.15 °C).")
        self.temperature = temperature + 273.15

    def get_temperature(self):
        """
        Returns the temperature in °C.

        Returns
        -------
        float
            The temperature in °C.
        """
        return self.temperature - 273.15
    
    def set_rel_humidity(self, rel_humidity):
        """
        Sets the relative humidity in % for the sound absorption coefficient calculation.

        Parameters
        ----------
        rel_humidity : int or float
            The relative humidity in %.

        Raises
        -------
        TypeError
            If the relative humidity is not an integer or float.
        ValueError
            If the relative humidity is not in the range of 0 % - 100 %.
        """
        if not isinstance(rel_humidity, (int, float)):
            raise TypeError("Relative humidity must be an integer or float.")  
        if rel_humidity < 0 or rel_humidity > 100:
            raise ValueError("Relative humidity must be between 0 and 100 %.")
        self.rel_humidity = rel_humidity
        self.calculate_abs_humidity()
    
    def calculate_abs_humidity(self):
        """
        Calculates the absolute humidity based on the relative humidity, pressure, and temperature.
        The absolute humidity is calculated as the molar concentration of water vapor in air according to ISO 9613-1 Annex B.
        """
        self.abs_humidity = (self.rel_humidity * 10**(-6.8346 * ((273.16 / (self.temperature))**1.261) + 4.6151)) / (self.pressure / 101.325)

    def set_ref_pressure(self, ref_pressure):
        """
        Sets the reference pressure in kPa for the sound absorption coefficient calculation.

        Parameters
        ----------
        ref_pressure : int or float
            The reference pressure in kPa.

        Raises
        -------
        TypeError
            If the reference pressure is not a numeric value.
        ValueError
            If the reference pressure is not a positive numeric value.
        """
        if not isinstance(ref_pressure, (int, float)):
            raise TypeError("Reference pressure must be an integer or float.")
        if ref_pressure <= 0:
            raise ValueError("Reference pressure must be a positive value.")
        self.ref_pressure = ref_pressure

    def calculate_coefficient(self):
        """
        Calculates the sound absorption coefficient $m$ in 1/m and $alpha$ in dB/m of air based on frequency, temperature, humidity and pressure according to DIN EN ISO 354, based on $alpha$ from ISO 9613-1.
        
        Returns
        -------
        list
            The sound absorption coefficient $m$ in 1/m.
        
        Raises
        -------
        ValueError
            If temperature, relative humidity or pressure is not set before calculating the coefficient.
        """
        if not hasattr(self, 'temperature'):
            raise ValueError("Temperature must be set before calculating coefficient.") 
        if not hasattr(self, 'rel_humidity'):
            raise ValueError("Relative humidity must be set before calculating coefficient.")
        if not hasattr(self, 'pressure'):
            raise ValueError("Pressure must be set before calculating coefficient.")
        else:
            alpha = np.zeros(len(self.frequency))
            f_rO = (self.pressure/self.ref_pressure)*(24.0+4.04*(10.0**4.0)*self.abs_humidity*((0.02+self.abs_humidity)/(0.391+self.abs_humidity)))
            f_rN = (self.pressure/self.ref_pressure)*((self.temperature/self.ref_temperature)**(-(1.0/2.0)))*(9.0+280.0*self.abs_humidity*np.exp(-4.170*(((self.temperature/self.ref_temperature)**(-(1.0/3.0)))-1.0)))
            for i, f in enumerate(self.frequency):
                alpha[i] = 8.686*(f**2.0)*((1.84*(10.0**(-11.0))*((self.pressure/self.ref_pressure)**(-1.0))*((self.temperature/self.ref_temperature)**(1.0/2.0)))+
                                 ((self.temperature/self.ref_temperature)**(-5.0/2.0))*
                                 (0.01275*np.exp(-2239.1/self.temperature)*((f_rO+((f**2.0)/f_rO))**(-1.0))+
                                  0.1068*np.exp(-3352.0/self.temperature)*((f_rN+((f**2.0)/f_rN))**(-1.0))))# dB/m

            m = (alpha*1000)/4350
            self.alpha = alpha
            self.m = m
            return m
    

        
class material:
    """
    Defines a "material" object with properties such as name, absorption coefficient (and price).

    Attributes
    ----------
    name : str
        The name of the material.
    absorption_coefficient : list
        The absorption coefficient of the material at different frequencies.
    price : int or float, optional
        The price of the material as €/m$^2$ (default is None).
    """

    def __init__(self, name, absorption_coefficient):
        """
        Initializes a material object with a specified name and absorption coefficient.

        Parameters
        ----------
        name : str
            The name of the material.
        absorption_coefficient : list of float
            A list of absorption coefficients at different frequencies.

        Raises
        -------
        TypeError
            If the name is not a string or if the absorption coefficient is not a list.
        ValueError
            If the absorption coefficient is not a list or if it contains non-numeric values.
        ValueError
            If the absorption coefficient list is empty.
        ValueError
            If the absorption coefficient list contains negative values.
        ValueError
            If the absorption coefficient list does not contain exactly 8 values for the frequency bands 63, 125, 250, 500, 1000, 2000, 4000, and 8000 Hz.
        """
        if not isinstance(name, str):
            raise TypeError("Name must be a string.")
        if not isinstance(absorption_coefficient, list):
            raise TypeError("Absorption coefficient must be a list.")
        if not all(isinstance(ac, (int, float)) for ac in absorption_coefficient):
            raise ValueError("Absorption coefficient must be a list of numeric values.")
        if len(absorption_coefficient) == 0:
            raise ValueError("Absorption coefficient list cannot be empty.")
        if any(ac < 0 for ac in absorption_coefficient):
            raise ValueError("Absorption coefficient values must be non-negative.")
        if len(absorption_coefficient) != 8:
            raise ValueError("Absorption coefficient list must contain exactly 8 values for the frequency bands 63, 125, 250, 500, 1000, 2000, 4000, and 8000 Hz.")
        self.name = name
        self.absorption_coefficient = np.array(absorption_coefficient)
        # self.frequency_weight = self.get_frequency_weight()
        self.price = None

    def set_absorption_coefficient(self, absorption_coefficient):
        """
        Sets the absorption coefficient of the material.

        Parameters
        ----------
        absorption_coefficient : list of float
            A list of absorption coefficients at different frequencies.

        Raises
        -------
        TypeError
            If the absorption coefficient is not a list.
        ValueError
            If the absorption coefficient is not a list or if it contains non-numeric values.
        ValueError
            If the absorption coefficient list is empty.
        ValueError
            If the absorption coefficient list contains negative values.
        ValueError
            If the absorption coefficient list does not contain exactly 8 values for the frequency bands 63, 125, 250, 500, 1000, 2000, 4000, and 8000 Hz.
        """
        if not isinstance(absorption_coefficient, list):
            raise TypeError("Absorption coefficient must be a list.")
        if not all(isinstance(ac, (int, float)) for ac in absorption_coefficient):
            raise ValueError("Absorption coefficient must be a list of numeric values.")
        if len(absorption_coefficient) == 0:
            raise ValueError("Absorption coefficient list cannot be empty.")
        if any(ac < 0 for ac in absorption_coefficient):
            raise ValueError("Absorption coefficient values must be non-negative.")
        if len(absorption_coefficient) != 8:
            raise ValueError("Absorption coefficient list must contain exactly 8 values for the frequency bands 63, 125, 250, 500, 1000, 2000, 4000, and 8000 Hz.")
        self.absorption_coefficient = absorption_coefficient

    def get_absorption_coefficient(self):
        """
        Returns the absorption coefficient of the material.

        Returns
        -------
        list
            The absorption coefficient of the material at different frequencies.
        """
        return self.absorption_coefficient
    
    def set_name(self, name):
        """
        Sets the name of the material.

        Parameters
        ----------
        name : str
            The name of the material.

        Raises
        -------
        TypeError
            If the name is not a string.
        """
        if not isinstance(name, str):
            raise TypeError("Name must be a string.")
        self.name = name

    def get_name(self):
        """
        Returns the name of the material.

        Returns
        -------
        str
            The name of the material if it has been set, otherwise returns None.
        """
        if not hasattr(self, 'name'):
            return None
        return self.name
    
    def set_price(self, price):
        """
        Sets the price of the material.

        Parameters
        ----------
        price : int or float
            The price of the material in €/m$^2$.

        Raises
        -------
        TypeError
            If the price is not a numeric value.
        ValueError
            If the price is not a positive numeric value.
        """
        if not isinstance(price, (int, float)):
            raise TypeError("Price must be an integer or float.")
        if price < 0:
            raise ValueError("Price must be a non-negative value.")
        self.price = price

    def get_price(self):
        """
        Returns the price of the material in €/m$^2$ if it has been set.
        
        Returns
        -------
        float or None
            The price of the material in €/m$^2$ if it has been set, otherwise returns None.
        """
        return self.price if hasattr(self, 'price') else None
    
    # def get_frequency_weight(self):
    #     # Berechnung der Gewichtung einzelner Frequenzbänder
    #     # Platzhalter für die Frequenzgewichtung
    #     return self.frequency_weight
    


class surface:
    """
    Defines a "surface" object with properties such as name, area, and material.

    Attributes
    ----------
    name : str
        The name of the surface.
    area : int or float
        The area of the surface in m$^2$.
    material : material
        The material of the surface, which is an instance of the material class.
    """
    
    def __init__(self, name, area, material):
        """
        Initializes a surface object with a specified name, area, and material.

        Parameters
        ----------
        name : str
            The name of the surface.
        area : int or float
            The area of the surface in m$^2$.
        material : material 
            The material of the surface, which is an instance of the material class.
        
        Raises
        -------
        TypeError
            If the name is not a string or if the area is not a numeric value.
        ValueError
            If the area is not a positive numeric value.
        """
        if not isinstance(name, str):
            raise TypeError("Name must be a string.")
        if not isinstance(area, (int, float)):
            raise TypeError("Area must be an integer or float.")
        self.name = name
        self.area = area
        self.material = material

    def set_area(self, area):
        """
        Sets the area of the surface.
        
        Parameters
        ----------
        area : int or float
            The area of the surface in m$^2$.
        
        Raises
        -------
        TypeError
            If the area is not a numeric value.
        ValueError
            If the area is not a positive numeric value.
        """
        if not isinstance(area, (int, float)):
            raise TypeError("Area must be a numeric value.")
        if area <= 0:
            raise ValueError("Area must be a positive value.")
        self.area = area

    def get_area(self):
        """
        Returns the area of the surface.
        
        Returns
        -------
        float
            The area of the surface in m$^2$.
        """

        return self.area
    
    def set_material(self, material):
        """
        Sets the material of the surface.

        Parameters
        ----------
        material : material
            The material of the surface, which is an instance of the material class.

        Raises
        -------
        TypeError
            If the material is not an instance of the material class.
        ValueError
            If the material does not have an absorption coefficient defined.
        """
        if not isinstance(material, material):
            raise TypeError("Material must be an instance of the material class.")
        if not hasattr(material, 'absorption_coefficient'):
            raise ValueError("Material must have an absorption coefficient defined.")
        self.material = material

    def get_material(self):
        """
        Returns the material of the surface.
        
        Returns
        -------
        material
            The material of the surface, which is an instance of the material class.
        """
        return self.material
    
    def set_surface_name(self, name):
        """
        Sets the name of the surface.

        Parameters
        ----------
        name : str
            The name of the surface.

        Raises
        -------
        TypeError
            If the name is not a string.
        """
        if not isinstance(name, str):
            raise TypeError("Name must be a string.")
        self.name = name

    def get_surface_name(self):
        """
        Returns the name of the surface if it has been set.
        
        Returns
        -------
        str or None
            The name of the surface if it has been set.
        """
        return self.name if hasattr(self, 'name') else None



class reverberation_time:
    """
    Defines a "reverberation_time" object that calculates the reverberation time of a room based on the extended Sabine formula from DIN EN ISO 354.

    Attributes
    ----------
    calc_room : room
        The room for which the reverberation time is calculated, which is an instance of the room class.
    surfaces : list
        A list of surfaces in the room, each of which is an instance of the surface class.
    frequency_bands : list
        A list of frequency bands in Hz for which the reverberation time is calculated.
    air_damp_calc : bool, optional
        A flag indicating whether air damping is considered in the calculation (default is True).
    Aeq : int or float
        The equivalent sound absorption area of the room in m$^2$, calculated based on the surfaces and their materials.
    c : int or float
        The speed of sound in air in m/s, calculated based on the room's temperature and pressure.
    volume : int or float
        The volume of the room in m$^3$.
    air_damp : air_damp
        An instance of the air_damp class that calculates the sound absorption coefficient of air based on frequency, temperature, humidity, and pressure.
    reverberation_time : list
        The calculated reverberation time of the room in s.
    """
    
    def __init__(self, calc_room, surfaces, air_damp_calc=True, meas_reverberation_time=None):
        """
        Initializes a reverberation_time object with a specified room, surfaces, and optional parameters for air damping calculation and measured reverberation time.
        
        Parameters
        ----------
        calc_room : room
            The room for which the reverberation time is calculated, which is an instance of the room class.
        surfaces : list of surface
            A list of surfaces in the room, each of which is an instance of the surface class.
        air_damp_calc : bool, optional
            A flag indicating whether air damping is considered in the calculation (default is True).
        meas_reverberation_time : list of int or float, optional
            A list of measured reverberation times of the room in s (default is None).
        
        Raises
        -------
        ValueError
            If the room is not an instance of the room class.
        TypeError
            If the surfaces are not a list or if any surface is not an instance of the surface class.
        ValueError
            If the surfaces list is empty.
        TypeError
            If the air_damp_calc is not a boolean.
        TypeError
            If the measured reverberation time is not a list or if it contains non-numeric values.
        ValueError
            If the measured reverberation time list does not contain exactly 8 entries for the frequency bands 63, 125, 250, 500, 1000, 2000, 4000, and 8000 Hz.
        ValueError
            If the measured reverberation time list is empty or if it contains negative values.
        """
        if not isinstance(calc_room, room):
            raise TypeError("Room must be an instance of the room class.")
        if not isinstance(surfaces, list):
            raise TypeError("Surfaces must be a list.")
        if not all(isinstance(calc_surface, surface) for calc_surface in surfaces):
            raise TypeError("All surfaces must be instances of the surface class.")
        if len(surfaces) == 0:
            raise ValueError("Surfaces list cannot be empty.")
        if not isinstance(air_damp_calc, bool):
            raise TypeError("Air damping calculation flag must be a boolean.")
        if meas_reverberation_time is not None:
            if not isinstance(meas_reverberation_time, list):
                raise TypeError("Measured reverberation time must be a list.")
            if not all(isinstance(mrt, (int, float)) for mrt in meas_reverberation_time):
                raise ValueError("Measured reverberation time must be a list of numeric values.")
            if len(meas_reverberation_time) != 8:
                raise ValueError("Measured reverberation time must be a list containing 8 entries for the frequency bands 63, 125, 250, 500, 1000, 2000, 4000, and 8000 Hz.")
            if len(meas_reverberation_time) == 0:
                raise ValueError("Measured reverberation time list cannot be empty.")
            if any(mrt < 0 for mrt in meas_reverberation_time):
                raise ValueError("Measured reverberation time values must be non-negative.")
        

        self.calc_room = calc_room
        self.frequency_bands = [63, 125, 250, 500, 1000, 2000, 4000, 8000]
        self.surfaces = surfaces
        self.calculate_Aeq()
        self.c = calc_room.get_c()
        #self.materials = surfaces.materials
        self.volume = calc_room.volume
        self.air_damp_calc = air_damp_calc
        self.air_damp = air_damp(self.frequency_bands)
        self.air_damp.set_temperature(calc_room.get_temperature())
        self.air_damp.set_pressure(calc_room.get_pressure())
        self.air_damp.set_rel_humidity(calc_room.get_rel_humidity())
        if meas_reverberation_time is not None:
            self.meas_reverberation_time = np.array(meas_reverberation_time)
        else:
            self.meas_reverberation_time = None
        self.calculate_reverberation_time()

    def calculate_Aeq(self):
        """
        Calculates the equivalent sound absorption area (Aeq) in m$^2$ of the room based on the surfaces and their materials.
        The equivalent sound absorption area is calculated as the sum of the product of the absorption coefficient and the area of each surface.
        
        Returns
        -------
        float
            The equivalent sound absorption area of the room in m$^2$.
        
        Raises
        -------
        ValueError
            If any surface does not have a material with an absorption coefficient defined.
        """
        if not all(hasattr(surface, 'get_material') and surface.get_material() is not None for surface in self.surfaces):
            raise ValueError("All surfaces must have a material with an absorption coefficient defined.")
        coeffs = np.array([surface.get_material().get_absorption_coefficient() for surface in self.surfaces])
        areas = np.array([surface.get_area() for surface in self.surfaces])
        Aeq_octave = coeffs * areas[:, np.newaxis]
        Aeq = np.nansum(Aeq_octave, axis=0)
        nan_mask = np.isnan(Aeq_octave).any(axis=0)
        Aeq[nan_mask] = np.nan
        self.Aeq = Aeq
        return self.Aeq

    def calculate_reverberation_time(self):
        r"""
        Calculates the reverberation time of the room based on the extended Sabine formula, considering air damping if specified.

        The reverberation time is calculated using the formula:

        $$T = \frac{55.3 \cdot V}{A_{eq} \cdot c}$$

        where:

        - $T$ is the reverberation time in s
        - $V$ is the volume of the room in m³
        - $A_{eq}$ is the equivalent sound absorption area in m²
        - $c$ is the speed of sound in air in m/s

        If air damping is considered, the formula is corrected by the speed of sound and air damping:

        $$T = \frac{55.3}{c} \cdot \frac{V}{A_{eq} + 4 \cdot V \cdot m}$$

        where $m$ is the sound absorption coefficient of air in 1/m, calculated based on frequency, temperature, humidity, and pressure according to EN ISO 354 and ISO 9613-1.

        If a measured reverberation time is provided, its equivalent sound absorption area

        $$A_{eq, measured} = \frac{55.3 \cdot V}{T_{measured} \cdot c}$$

        is used to specify initial values for the extension with additional sound absorption areas. The reverberation time is then calculated as:

        $$T = \frac{55.3 \cdot V}{(A_{eq} + A_{eq, measured}) \cdot c}$$
        """
        # Calculate the reverberation time based on the optimized Sabine formula according to DIN EN ISO 354
        if self.air_damp_calc is True:
            # If air damping is considered, use the Sabine formula corrected by the speed of sound and air damping
            if self.meas_reverberation_time is not None:
                # If measured reverberation time is provided, use the calculated equivalent sound absorption area to correct the measured reverberation time
                Aeq_meas = ((55.3 / self.c) * (self.volume / (self.meas_reverberation_time))) - 4 * self.volume * self.air_damp.calculate_coefficient()
                self.reverberation_time = (55.3 / self.c) * (self.volume / (self.Aeq + Aeq_meas + 4 * self.volume * self.air_damp.calculate_coefficient()))
            else:
                self.reverberation_time = (55.3 / self.c) * (self.volume / (self.Aeq + 4 * self.volume * self.air_damp.calculate_coefficient()))

        if self.air_damp_calc == False:
            # If air damping is not considered, use the standard Sabine formula corrected by the speed of sound
            if self.meas_reverberation_time is not None:
                # If measured reverberation time is provided, use the calculated equivalent sound absorption area to correct the measured reverberation time
                Aeq_meas = (55.3 * self.volume) / (self.meas_reverberation_time * self.c)
                self.reverberation_time = (55.3 * self.volume) / ((self.Aeq + Aeq_meas) * self.c)
            else:
                self.reverberation_time = (55.3 * self.volume) / (self.Aeq * self.c)



class DIN_18041_limits:
    """
    Defines a "DIN_18041_limits" object that calculates the limits for reverberation time according to DIN 18041 based on room type, volume, and height.

    Attributes
    ----------
    room : room
        The room for which the limits are calculated, which is an instance of the room class.
    volume : int or float
        The volume of the room in m$^3$.
    c : int or float
        The speed of sound in air in m/s, calculated based on the room's temperature and pressure.
    type : str
        The type of room according to DIN 18041, specified as a string (e.g., "A1", "B2", or 'no requirements'). 
    T_soll : int or float
        The target reverberation time in s according to DIN 18041, calculated based on the room type, volume and height.
    T_upper_limit : np.array
        The upper limit for reverberation time in s according to DIN 18041, calculated based on the target reverberation time.
    T_lower_limit : np.array
        The lower limit for reverberation time in s according to DIN 18041, calculated based on the target reverberation time.

    """
    
    def __init__(self, calc_room, type):
        """
        Initializes a DIN_18041_limits object with a specified room and room type.
        
        Parameters
        ----------
        calc_room : room
            The room for which the limits are calculated, which is an instance of the room class.
        type : str
            The type of room according to DIN 18041, specified as a string (e.g., "A1", "B2", or 'no requirements'). 

        Raises
        -------
        TypeError
            If the room is not an instance of the room class or if the type is not a string.
        ValueError
            If the type is not a valid room type according to DIN 18041.
        """
        if not isinstance(calc_room, room):
            raise TypeError("Room must be an instance of the room class.")
        if not isinstance(type, str):
            raise TypeError("Type must be a string.")
        if len(type) != 2 or type[0] not in ["A", "B"] or type[1] not in ["1", "2", "3", "4", "5"]:
            if type != "no requirements":
                raise ValueError("Type must be a valid room type according to DIN 18041 (e.g., 'A1', 'B2') or 'no requirements'.")
        self.calc_room = calc_room
        self.volume = self.calc_room.volume
        self.c = self.calc_room.c
        self.type = str(type)
        self.get_limits()
        

    def get_limits(self):
        """
        Calculates the limits for reverberation time in s according to DIN 18041 based on room type, volume, and height.
        
        Returns
        -------
        list of float
            A list containing the upper and lower limits for reverberation time in s according to DIN 18041.
        """

        # Get the limits Tsoll for reverberation time according to DIN 18041 based on room type, volume and height
        self.T_soll = None
        match self.type[0]:
            case "A":
                T_upper_limit_A = np.array((1.7,1.45,1.2,1.2,1.2,1.2,1.2,1.2))
                T_lower_limit_A = np.array((0.5,0.65,0.8,0.8,0.8,0.8,0.65,0.5))

                match self.type[1]:
                    case "1":
                        if self.volume < 30:
                            warnings.warn("According to DIN 18041, the room volume should be at least 30 m³ for type A1.")
                        if self.volume > 1000:
                            warnings.warn("According to DIN 18041, the room volume should be smaller than 1000 m³ for type A1.")
                        
                        self.T_soll = 0.45*np.log10(self.volume) + 0.07

                    case "2":
                        if self.volume < 50:
                            warnings.warn("According to DIN 18041, the room volume should be at least 50 m³ for type A2.")
                        if self.volume > 5000:
                            warnings.warn("According to DIN 18041, the room volume should be smaller than 5000 m³ for type A2.")
                        
                        self.T_soll = 0.37*np.log10(self.volume) + 0.14

                    case "3":
                        if self.volume < 30:
                            warnings.warn("According to DIN 18041, the room volume should be at least 30 m³ for type A3.")
                        if self.volume > 5000:
                            warnings.warn("According to DIN 18041, the room volume should be smaller than 5000 m³ for type A3.")
                        
                        self.T_soll = 0.32*np.log10(self.volume) + 0.17

                    case "4":
                        if self.volume < 30:
                            warnings.warn("According to DIN 18041, the room volume should be at least 30 m³ for type A4.")
                        if self.volume > 500:
                            warnings.warn("According to DIN 18041, the room volume should be smaller than 500 m³ for type A4.")
                        
                        self.T_soll = 0.26*np.log10(self.volume) + 0.14

                    case "5":
                        if self.volume < 200:
                            warnings.warn("According to DIN 18041, the room volume should be at least 200 m³ for type A5.")
                        if self.volume > 9999:
                            self.T_soll = 2
                        
                        self.T_soll = 0.75*np.log10(self.volume) + 1

                self.T_upper_limit = T_upper_limit_A*self.T_soll
                self.T_lower_limit = T_lower_limit_A*self.T_soll

            case "B":
                T_upper_limit_B = np.array((0,0,1,1,1,1,0,0))
                T_lower_limit_B = np.array((0,0,0,0,0,0,0,0))

                match self.type[1]:
                    case "1":
                        warnings.warn("According to DIN 18041, there are no requirements for type B1.")
                        self.T_soll = 0
                    case "2":
                        if self.calc_room.height <= 2.5:
                            A_V = 0.15
                        if self.calc_room.height > 2.5:
                            A_V = 1/(4.8 + 4.69 * np.log10(self.calc_room.height))

                    case "3":
                        if self.calc_room.height <= 2.5:
                            A_V = 0.20
                        if self.calc_room.height > 2.5:
                            A_V = 1/(3.13 + 4.69 * np.log10(self.calc_room.height))

                    case "4":
                        if self.calc_room.height <= 2.5:
                            A_V = 0.25
                        if self.calc_room.height > 2.5:
                            A_V = 1/(2.13 + 4.69 * np.log10(self.calc_room.height))

                    case "5":
                        if self.calc_room.height <= 2.5:
                            A_V = 0.30
                        if self.calc_room.height > 2.5:
                            A_V = 1/(1.47 + 4.69 * np.log10(self.calc_room.height))

                if self.T_soll == 0:
                    self.T_soll = 0
                else:
                    self.T_soll = (55.3/self.c) * (self.volume / (A_V * self.volume))

                self.T_upper_limit = T_upper_limit_B * self.T_soll
                self.T_lower_limit = T_lower_limit_B

            case _:
                raise ValueError("Invalid room type specified.")
            
                        
        match self.type:
            case "no requirements":
                self.T_soll = np.nan
                self.T_upper_limit = np.array([np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan])
                self.T_lower_limit = np.array([np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan])
            
        return (self.T_upper_limit, self.T_lower_limit)
