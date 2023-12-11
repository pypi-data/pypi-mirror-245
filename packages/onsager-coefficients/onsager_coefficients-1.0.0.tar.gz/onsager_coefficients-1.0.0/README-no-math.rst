.. _example/: https://github.com/jwjeffr/onsager_coefficients/tree/master/example

Onsager coefficients from molecular dynamics run
################################################

This library is for calculating the Onsager coefficients in a molecular dynamics run, calculated with the generalized Einstein relation.

This code works by splicing a larger MD trajectory into N smaller subtrajetories, averaging the square displacements over those trajectories, and calculating the slope of that time series in the long time limit.

Parameters for the calculation are the LAMMPS-style dump file name, the number of subtrajectories to create, the timestep in the dump file, and the transient time.

The transient time parameter is for excluding the initial transient behavior in averaged trajectory.

With OVITO Pro, you can install this library into your OVITO interface with:

``ovitos -m pip install --user onsager_coefficients``

which adds a mean square displacement and a total displacement modifier to your interface. Or, for use in a standalone Python script:

``pip install onsager_coefficients``

An example of this repository used in a standalone script is in the `example/`_ directory.