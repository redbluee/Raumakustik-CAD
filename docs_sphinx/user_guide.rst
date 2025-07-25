User Guide
=============

This tool provides a user-friendly interface for calculating and optimizing reverberation times in rooms according to the DIN 18041 [DIN18041]_ standard. It allows users to input room dimensions, surface materials, and other acoustic properties to obtain accurate reverberation time calculations. 

The tool can be found under this link: `RoomAcousticWizard <https://raumakustik-cad.onrender.com/>`_


Here is a brief overview of how to use the tool:

1. **Input Room Parameters**: 

Enter the room parameters such as volume, temperature, humidity, and atmospheric pressure. 
These parameters are necessary for the reverberation time calculation. 
To compare the results to the requirements from DIN 18041 [DIN18041]_, the room type according to the standard must be selected. It can be selected from the dropdown menu.
Linked to the requirements is the optional room height parameter, which is needen when comparing the reverberation times with "B"-requirements from DIN 18041 [DIN18041]_. 
Another optional parameter is a switch, selecting if the air damping should be considered in the calculation.

2. **Select Surface Materials**: 

In the Table below the diagram you can select the surfaces contributing to the room. They can be defined by their name, the area, the material name, and the absorption coefficients in the octaves between 63 Hz and 8000 Hz. 
If one absorption coefficient value is not known and the field is left empty, the reverberation time in this octave band won't be calculated.
For the ease of use, materials and their absorption coefficients can be selected from an exemplary database based on DIN 18041 [DIN18041]_ by clicking the database symbol next to the material selection field. This allows quick access to standardized material data without manual entry.

3. **Calculate Reverberation Time**: 

After entering all necessary parameters, the results will be displayed in the diagram. 
Visualized are the reverberation times in the octave bands between 63 Hz and 8000 Hz (if every parameter in each octave band is completely defined) and the requirements from DIN 18041 [DIN18041]_ for the selected room type.

For further information about the used methods, please refer to the official norm DIN 18041:2016-03 [DIN18041]_.

.. [DIN18041] DIN 18041:2016-03. Hörsamkeit in Räumen – Anforderungen, Empfehlungen und Hinweise für die Planung. Beuth Verlag, Berlin.