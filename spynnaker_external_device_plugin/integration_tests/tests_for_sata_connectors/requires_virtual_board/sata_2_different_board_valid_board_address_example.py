"""
retina example that just feeds data from a retina to live output via an
intermediate population
"""
import spynnaker.pyNN as p
import spynnaker_external_devices_plugin.pyNN as external_devices

# Setup
p.setup(timestep=1.0)

retina_pop = p.Population(
    2000, external_devices.ArbitaryFPGADevice, {
        'fpga_link_id': 12,
        'fpga_id': 1,
        'board_address': "127.0.0.1", # 4, 8
        'label': "bacon"},
    label='External sata thing')

retina_pop = p.Population(
    2000, external_devices.ArbitaryFPGADevice, {
        'fpga_link_id': 11,
        'fpga_id': 1,
        'board_address': "127.0.0.2", # 0 0
        'label': "bacon"},
    label='External sata thing')

p.run(1000)
p.end()
