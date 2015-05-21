import sys
import os
import traceback
from simtk.openmm import app
import simtk.openmm as mm
from simtk import unit as u

niterations = 100
temperature = 300 * u.kelvin

kB = u.MOLAR_GAS_CONSTANT_R
kT = kB * temperature

if '--platform' in sys.argv:
    platform_name = sys.argv[sys.argv.index('--platform') + 1]
else:
    platform_name = 'CUDA'


def get_highest_sim_index():
    filenames = os.listdir('output')
    sim_indices = []
    for filename in filenames:
        try:
            sim_indices.append(int(filename))
        except:
            continue

    if len(sim_indices) == 0:
        return None

    highest_index = sorted(sim_indices)[-1]
    return highest_index


def sim_inner(output_filepath):

    with open('explicit-integrator-start.xml') as integrator_file:
        integrator = mm.XmlSerializer.deserialize(integrator_file.read())
    with open('explicit-state-start.xml') as state_file:
        state = mm.XmlSerializer.deserialize(state_file.read())
    with open('explicit-system-start.xml') as system_file:
        system = mm.XmlSerializer.deserialize(system_file.read())

    platform = mm.Platform.getPlatformByName(platform_name)
    context = mm.Context(system, integrator, platform)
    context.setPositions(state.getPositions())
    context.setVelocitiesToTemperature(temperature)

    energy_outfile = open(output_filepath, 'w')
    energy_outfile.write('# iteration | simulation time (ps) | potential_energy (kT) | kinetic_energy (kT) | volume (nm^3)\n')
    energy_outfile.flush()

    for iteration in range(niterations):
        try:
            integrator.step(500)
        except Exception as e:
            trbk = traceback.format_exc()
            energy_outfile.write(trbk)
            energy_outfile.write(str(e))
            print(trbk)
            print(e)
            break

        state = context.getState(getEnergy=True)
        simulation_time = state.getTime()
        potential_energy = state.getPotentialEnergy()
        kinetic_energy = state.getKineticEnergy()
        box_vectors = state.getPeriodicBoxVectors()
        volume_in_nm3 = (box_vectors[0][0] * box_vectors[1][1] * box_vectors[2][2]) / (u.nanometers**3) # TODO: Use full determinant

        energy_outfile.write("  %8d %8.1f %8.3f %8.3f %.3f\n" % (iteration, simulation_time / u.picoseconds, potential_energy / kT, kinetic_energy / kT, volume_in_nm3))
        energy_outfile.flush()

    energy_outfile.close()


if __name__ == '__main__':
    while True:
        if not os.path.exists('output'):
            os.mkdir('output')

        highest_sim_index = get_highest_sim_index()
        if highest_sim_index is not None:
            i = highest_sim_index + 1
        else:
            i = 0
        print('Simulation {0}'.format(i))
        sim_inner(os.path.join('output', str(i)))
