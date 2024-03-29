"""
retina example that just feeds data from a retina to live output via an
intermediate population
"""
import spynnaker.pyNN as p
import spynnaker_external_devices_plugin.pyNN as external_devices

# Setup
p.setup(timestep=1.0)

# FPGA Retina - Down Polarity
retina_pop = p.Population(
    2000, external_devices.ArbitaryFPGADevice, {
        'fpga_link_id': 12,
        'fpga_id': 1,
        'label': "bacon"},
    label='External sata thing')

p.run(1000)
p.end()
