"""
retina example that just feeds data from a retina to live output via an
intermediate population
"""
import spynnaker.pyNN as p
import spynnaker_external_devices_plugin.pyNN as external_devices

# Setup
p.setup(timestep=1.0)

# FPGA Retina
retina_pop = p.Population(
    2000, external_devices.ExternalFPGARetinaDevice, {
        'spinnaker_link_id': 0,
        'retina_key': 0x5,
        'mode': external_devices.ExternalFPGARetinaDevice.MODE_128,
        'polarity': external_devices.ExternalFPGARetinaDevice.DOWN_POLARITY},
    label='External sata thing')

retina_pop2 = p.Population(
    2000, external_devices.ExternalFPGARetinaDevice, {
        'spinnaker_link_id': 0,
        'retina_key': 0x5,
        'mode': external_devices.ExternalFPGARetinaDevice.MODE_128,
        'polarity': external_devices.ExternalFPGARetinaDevice.DOWN_POLARITY},
    label='External sata thing')

p.run(1000)
p.end()
