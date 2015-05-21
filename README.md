The directories `hanging` and `error-downloading-array-posq` contain serialized system, state and integrator xml files for models which failed simulation either by hanging with no further output, or with an Exception message (`Error downloading array posq: Invalid error code (700)`), respectively.

The directories also contain model IDs and logfiles (`explicit-log.yaml` and `explicit-energies.txt`) from the original failed MD simulations, performed using Ensembler. Protein models had been refined with 100 ps implicit solvent MD simulation, then solvated and subjected to energy minimzation. The system, state and integrator files were output at this stage (before the start of the failed explicit solvent MD simulations).

`scripts/test_openmm_sim_from_serialized.py` will repeatedly deserialize the above files and run a 100 ps simulation. Each simulation reports energies in files stored in the `output` directories. Exceptions are caught and written to these files.

On the MSKCC cBio cluster, approximately 1 in 10 simulations fails either by hanging or by emitting the above Exception.
