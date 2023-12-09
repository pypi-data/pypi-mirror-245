A library which provides implementations of the kernel of the Alchemical Integral Transform (AIT) for general potentials in 1D. An introduction to the concept, further explanations and details can be found under https://arxiv.org/abs/2312.04458.

Instead of calculating electronic energies of systems one at a time, this kernel provides a shortcut. By using an initial system's electron density, one can calculate the energy difference to any other system within the radius of convergence of AIT. Check out my [GitHub page](https://github.com/SimonLeonKrug/pyalchemy) and the corresponding [paper](https://arxiv.org/abs/2312.04458).

PyAlchemy uses [Hartree atomic units](https://en.wikipedia.org/wiki/Hartree_atomic_units).
