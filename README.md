For investigating explicit solvent MD simulation failures for protein kinase models generated using [Ensembler](https://github.com/choderalab/ensembler).

Model directories, containing serialized system, state and integrator xml files:
* `hanging` - model failed simulation by hanging with no further output
* `error-downloading-array-posq` - model failed simulation Exception message `Error downloading array posq: Invalid error code (700)`

Protein models were generated using Modeller, then refined with 100 ps implicit solvent MD simulation, solvated, and subjected to energy minimzation. The serialized system, state and integrator files stored here were output at the start of the subsequent explicit solvent MD simulation (after EM, before MD). The original explicit solvent MD simulations were performed using the CUDA platform on GTX 680s.

The model directories also contain model IDs and logfiles (`explicit-log.yaml` and `explicit-energies.txt`) from the original failed MD simulations, performed using Ensembler. 

`scripts/test_openmm_sim_from_serialized.py` will repeatedly deserialize the above files and run a 100 ps simulation. Run it from one of the model directories. Each successive simulation reports energies in files stored in a directory named `output`. Exceptions are also caught and written to these files.

On the MSKCC cBio cluster, approximately 1 in 10 simulations fails either by hanging or by emitting the above Exception. The remainder complete successfully.
`hanging` model usually seems to fail around 8 or 9 ps.
