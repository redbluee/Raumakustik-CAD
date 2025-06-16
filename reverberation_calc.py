import numpy as np
import warnings

class room:
    """
    Defines a "room" object with properties such as volume, temperature, pressure, relative humidity, and speed of sound.

    Attributes
    ----------
    volume : int
        The volume of the room in cubic meters
    temperature : int
        The temperature of the room in degrees Celsius (default is 20)
    pressure : int
        The pressure of the room in kilopascals (default is 101.325)
    rel_humidity : int
        The relative humidity of the room in percentage (default is 50)
    height : int, optional
        The height of the room in meters (default is None)
    c : float
        The speed of sound in air in meters per second, calculated based on temperature and relative humidity

    Methods
    -------
    set_volume(volume)
        Sets the volume of the room.
    get_volume()
        Returns the volume of the room.
    set_temperature(temperature)
        Sets the temperature of the room.
    get_temperature()
        Returns the temperature of the room.
    set_pressure(pressure)
        Sets the pressure of the room.
    get_pressure()
        Returns the pressure of the room.
    set_rel_humidity(rel_humidity)
        Sets the relative humidity of the room.
    get_rel_humidity()
        Returns the relative humidity of the room.
    set_height(height)
        Sets the height of the room.
    get_height()
        Returns the height of the room.
    get_c()
        Calculates and returns the speed of sound in air based on the current temperature and relative humidity.
    """

    def __init__(self, volume):
        self.volume = volume
        self.temperature = 20           # Celsius
        self.pressure = 101.325         # kPa
        self.rel_humidity = 50          # percentage
        self.height = None              # meters
        self.c = self.get_c()           # Speed of sound in air in m/s

    def set_height(self, height):
        self.height = height
    def get_height(self):
        return self.height

    def set_volume(self, volume):
        self.volume = volume
    def get_volume(self):
        return self.volume
    
    def set_temperature(self, temperature):
        self.temperature = temperature
    def get_temperature(self):
        return self.temperature
    
    def set_pressure(self, pressure):
        self.pressure = pressure
    def get_pressure(self):
        return self.pressure
    
    def set_rel_humidity(self, rel_humidity):
        self.rel_humidity = rel_humidity
    def get_rel_humidity(self):
        return self.rel_humidity
    
    def get_c(self):
        # Speed of sound in air according to DIN EN ISO 354
        self.c = (331.6 + 0.6 * self.get_temperature())# * (1 + (self.get_rel_humidity() / 100)) ** 0.5 # automatisch ausgefüllt, kp wieso
        return self.c



class air_damp:
    """
    Defines an "air_damp" object that calculates the sound absorption coefficient m in 1/m of air based on frequency, temperature, humidity, and pressure according to DIN EN ISO 354, based on alpha from ISO 9613-1.

    Parameters
    ----------
    frequency : list
        A list of frequencies in Hz for which the sound absorption coefficient is calculated
    pressure : float, optional
        The pressure in kPa (default is 101.325)
    ref_pressure : float, optional
        The reference pressure in kPa (default is 101.325)
    rel_humidity : float, optional
        The relative humidity in percentage (default is 50)
    abs_humidity : float, optional
        The absolute humidity as molar conentration of water vapour in air as percentage according to ISO 9613-1 Annex B
    temperature : float, optional
        The temperature in Celsius (default is 20)
    ref_temperature : float, optional
        The reference temperature in Kelvin (default is 293.15, which is 20 degrees Celsius)
    alpha : list
        A list of sound absorption coefficients in dB/m, calculated based on the frequency, temperature, humidity and pressure
    m : list
        A list of sound absorption coefficients in 1/m, calculated from alpha
    
    Methods
    -------
    set_frequency(frequency)
        Sets the frequency in Hz for which the sound absorption coefficient is calculated.
    set_pressure(pressure)
        Sets the pressure in kPa for the sound absorption coefficient calculation.
    set_temperature(temperature)
        Sets the temperature in Celsius for the sound absorption coefficient calculation.
    get_temperature()
        Returns the temperature in Celsius.
    set_rel_humidity(rel_humidity)
        Sets the relative humidity in percentage for the sound absorption coefficient calculation.
    calculate_abs_humidity()
        Calculates the absolute humidity based on the relative humidity, pressure, and temperature.
    set_ref_pressure(ref_pressure)
        Sets the reference pressure in kPa for the sound absorption coefficient calculation.
    calculate_coefficient()
        calculates the sound absorption coefficient m in 1/m and alpha in dB/m of air based on frequency, temperature, humidity and pressure according to DIN EN ISO 354, based on alpha from ISO 9613-1.
    """
    def __init__(self, frequency):
        self.frequency = frequency
        self.pressure = 101.325
        self.ref_pressure = 101.325
        self.rel_humidity = 50          # percentage
        self.temperature = 20           # Celsius
        self.ref_temperature = 293.15   # Kelvin
        self.calculate_abs_humidity()
        self.coefficient = self.calculate_coefficient()
    
    def set_frequency(self, frequency):
        # Set frequency in Hz
        self.frequency = frequency    

    def set_pressure(self, pressure):
        # Set pressure in kPa
        self.pressure = pressure
    
    def set_temperature(self, temperature):
        # Set temperature in Celsius and convert to Kelvin
        self.temperature = temperature + 273.15
    def get_temperature(self):
        # Return temperature in Celsius
        return self.temperature - 273.15
    
    def set_rel_humidity(self, rel_humidity):
        # Set relative humidity in percentage and calculate ... humidity
        self.rel_humidity = rel_humidity
        self.calculate_abs_humidity()
    
    def calculate_abs_humidity(self):
        self.abs_humidity = (self.rel_humidity * 10**(-6.8346 * ((273.16 / (self.temperature))**1.261) + 4.6151)) / (self.pressure / 101.325)

    def set_ref_pressure(self, ref_pressure):
        # Set reference pressure in kPa
        self.ref_pressure = ref_pressure

    def calculate_coefficient(self):
        # calculates the sound absorption coefficient of air based on frequency, temperature, humidity and pressure according to ISO 9613-1
        # if not hasattr(self, 'temperature'):
        #     raise ValueError("Temperature must be set before calculating coefficient.") 
        # if not hasattr(self, 'rel_humidity'):
        #     raise ValueError("Relative humidity must be set before calculating coefficient.")
        # if not hasattr(self, 'pressure'):
        #     raise ValueError("Pressure must be set before calculating coefficient.")
        # else:
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
    Defines a "material" object with properties such as name, absorption coefficient, and price.

    Attributes
    ----------
    name : str
        The name of the material
    absorption_coefficient : list
        The absorption coefficient of the material at different frequencies
    price : float, optional
        The price of the material as €/m² (default is None)

    Methods
    ------- 
    set_absorption_coefficient(absorption_coefficient)
        Sets the absorption coefficient of the material.
    get_absorption_coefficient()
        Returns the absorption coefficient of the material.
    set_name(name)
        Sets the name of the material.
    get_name()
        Returns the name of the material.
    set_price(price)
        Sets the price of the material.
    get_price()
        Returns the price of the material if it has been set, otherwise returns None.
    """
    "material properties"
    
    def __init__(self, name, absorption_coefficient):
        self.name = name
        self.absorption_coefficient = np.array(absorption_coefficient)
        # self.frequency_weight = self.get_frequency_weight()
        self.price = None

    def set_absorption_coefficient(self, absorption_coefficient):
        self.absorption_coefficient = absorption_coefficient
    def get_absorption_coefficient(self):
        return self.absorption_coefficient
    
    def set_name(self, name):
        self.name = name
    def get_name(self):
        return self.name
    
    def set_price(self, price):
        self.price = price
    def get_price(self):
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
        The name of the surface
    area : float
        The area of the surface in square meters
    material : material
        The material of the surface, which is an instance of the material class

    Methods
    -------
    set_area(area)
        Sets the area of the surface.
    get_area()
        Returns the area of the surface.
    set_material(material)
        Sets the material of the surface.
    get_material()
        Returns the material of the surface.
    set_surface_name(name)
        Sets the name of the surface.
    get_surface_name()
        Returns the name of the surface if it has been set, otherwise returns None.
    """
    
    def __init__(self, name, area, material):
        self.name = name
        self.area = area
        self.material = material

    def set_area(self, area):
        self.area = area
    def get_area(self):
        return self.area
    
    def set_material(self, material):
        self.material = material
    def get_material(self):
        return self.material
    
    def set_surface_name(self, name):
        self.name = name
    def get_surface_name(self):
        return self.name if hasattr(self, 'name') else None



class reverberation_time:
    """
    Defines a "reverberation_time" object that calculates the reverberation time of a room based on the extended Sabine formula from DIN EN ISO 354.

    Attributes
    ----------
    room : room
        The room for which the reverberation time is calculated, which is an instance of the room class
    surfaces : list
        A list of surfaces in the room, each of which is an instance of the surface class
    frequency_bands : list
        A list of frequency bands in Hz for which the reverberation time is calculated
    air_damp_calc : bool, optional
        A flag indicating whether air damping is considered in the calculation (default is True)
    Aeq : float
        The equivalent sound absorption area of the room, calculated based on the surfaces and their materials
    c : float
        The speed of sound in air in meters per second, calculated based on the room's temperature and pressure
    volume : float
        The volume of the room in cubic meters
    air_damp : air_damp
        An instance of the air_damp class that calculates the sound absorption coefficient of air based on frequency, temperature, humidity, and pressure
    reverberation_time : list
        The calculated reverberation time of the room in seconds

    Methods
    -------
    calculate_Aeq()
        Calculates the equivalent sound absorption area (Aeq) of the room based on the surfaces and their materials.
    calculate_reverberation_time()
        Calculates the reverberation time of the room based on the extended Sabine formula, considering air damping if specified.
    """
    
    def __init__(self, room, surfaces, air_damp_calc=True, meas_reverberation_time=None):
        self.room = room
        self.frequency_bands = (63, 125, 250, 500, 1000, 2000, 4000, 8000)
        self.surfaces = surfaces
        self.calculate_Aeq()
        self.c = room.get_c()
        #self.materials = surfaces.materials
        self.volume = room.volume
        self.air_damp_calc = air_damp_calc
        self.air_damp = air_damp(self.frequency_bands)
        self.air_damp.set_temperature(room.get_temperature())
        self.air_damp.set_pressure(room.get_pressure())
        self.air_damp.set_rel_humidity(room.get_rel_humidity())
        self.meas_reverberation_time = meas_reverberation_time
        self.calculate_reverberation_time()

    def calculate_Aeq(self):
        coeffs = np.array([surface.get_material().get_absorption_coefficient() for surface in self.surfaces])
        areas = np.array([surface.get_area() for surface in self.surfaces])
        Aeq_octave = coeffs * areas[:, np.newaxis]
        Aeq = np.nansum(Aeq_octave, axis=0)
        nan_mask = np.isnan(Aeq_octave).any(axis=0)
        Aeq[nan_mask] = np.nan
        self.Aeq = Aeq
        return self.Aeq

    def calculate_reverberation_time(self):
        # Calculate the reverberation time based on the optimized Sabine formula according to DIN EN ISO 354
        if self.air_damp_calc == True:
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
        The room for which the limits are calculated, which is an instance of the room class
    volume : float
        The volume of the room in cubic meters
    c : float
        The speed of sound in air in meters per second, calculated based on the room's temperature and pressure
    type : str
        The type of room according to DIN 18041, specified as a string (e.g., "A1", "B2")
    T_soll : float
        The target reverberation time according to DIN 18041, calculated based on the room type, volume and height
    T_upper_limit : np.array
        The upper limit for reverberation time according to DIN 18041, calculated based on the target reverberation time
    T_lower_limit : np.array
        The lower limit for reverberation time according to DIN 18041, calculated based on the target reverberation time

    Methods
    -------
    get_limits()
        Calculates the limits for reverberation time according to DIN 18041 based on room type, volume and height.
    """
    
    def __init__(self, room, type):
        self.room = room
        self.volume = self.room.volume
        self.c = self.room.c
        self.type = str(type)
        self.get_limits()
        

    def get_limits(self):
        # Get the limits Tsoll for reverberation time according to DIN 18041 based on room type, volume and height
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
                        if self.room.height <= 2.5:
                            A_V = 0.15
                        if self.room.height > 2.5:
                            A_V = 1/(4.8 + 4.69 * np.log10(self.room.height))

                    case "3":
                        if self.room.height <= 2.5:
                            A_V = 0.20
                        if self.room.height > 2.5:
                            A_V = 1/(3.13 + 4.69 * np.log10(self.room.height))

                    case "4":
                        if self.room.height <= 2.5:
                            A_V = 0.25
                        if self.room.height > 2.5:
                            A_V = 1/(2.13 + 4.69 * np.log10(self.room.height))

                    case "5":
                        if self.room.height <= 2.5:
                            A_V = 0.30
                        if self.room.height > 2.5:
                            A_V = 1/(1.47 + 4.69 * np.log10(self.room.height))

                if self.T_soll == 0:
                    self.T_soll = 0
                else:
                    self.T_soll = (55.3/self.c) * (self.volume / (A_V * self.volume))

                self.T_upper_limit = T_upper_limit_B * self.T_soll
                self.T_lower_limit = T_lower_limit_B

            case _:
                raise ValueError("Invalid room type specified.")
            
        return (self.T_upper_limit, self.T_lower_limit)
