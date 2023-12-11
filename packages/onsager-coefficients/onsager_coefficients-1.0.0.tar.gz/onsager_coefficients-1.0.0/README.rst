.. role:: math(raw)
    :format: latex html

.. _example/: https://github.com/jwjeffr/onsager_coefficients/tree/master/example

Onsager coefficients from molecular dynamics run
################################################

This library is for calculating the Onsager coefficients in a molecular dynamics run, calculated with the generalized Einstein relation:

:math:`$$L_{\alpha\beta} = \lim_{t\to\infty}\frac{\left\langle \mathbf{R}_\alpha(t)\cdot\mathbf{R}_\beta(t)\right\rangle}{6t}$$`

where :math:`$\mathbf{R}_\alpha(t)$` is the total displacement of :math:`$\alpha$`-atoms (i.e. the sum of all displacements of :math:`$\alpha$` atoms) at time :math:`$t$`.

This code works by splicing a larger MD trajectory into :math:`$N$` smaller subtrajetories, averaging :math:`$\left\langle \mathbf{R}_\alpha(t)\cdot\mathbf{R}_\beta(t)\right\rangle$` over those trajectories, and calculating the slope of that time series in the long :math:`$t$` limit.

Parameters for the calculation are the LAMMPS-style dump file name, the number of subtrajectories to create, the timestep in the dump file, and the transient time.

The transient time parameter is for excluding the initial transient behavior in averaged trajectory.

With OVITO Pro, you can install this library into your OVITO interface with:

``ovitos -m pip install --user onsager_coefficients``

which adds a mean square displacement and a total displacement modifier to your interface. Or, for use in a standalone Python script:

``pip install onsager_coefficients``

An example of this repository used in a standalone script is in the `example/`_ directory.