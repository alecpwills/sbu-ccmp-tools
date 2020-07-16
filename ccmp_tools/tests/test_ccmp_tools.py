"""
Unit and regression test for the ccmp_tools package.
"""

# Import package, test suite, and other packages as needed
import ccmp_tools
import pytest
import sys, os
from ccmp_tools import md

def test_ccmp_tools_imported():
    """Sample test, will always pass so long as import statement worked"""
    assert "ccmp_tools" in sys.modules
    assert "ccmp_tools.md" in sys.modules
    
def test_md():
    print("Testing the MD module on sample files.")
    sim = md.SiestaSimulation('mdtestfiles', fdfb=True, fdfext='.fdf')
    assert sim.path == 'mdtestfiles', "sim.path not properly set."
    assert sim.fdf, "sim.fdf not properly found."
    assert sim.simlabel == 'nacl', "sim.simlabel not properly assigned."
    assert sim.latticeconstant == 14.373, "sim.latticeconstant not properly assigned."
    assert sim.dt == 0.5, "sim.dt not properly assigned."
    assert sim.istep == 1, "sim.istep not properly assigned."
    assert sim.fstep == 7000, "sim.fstep not properly assigned."
    assert sim.nsteps == 7000, "sim.nsteps not properly calculated."
    assert sim.simtype == 'md', "sim.simtype not properly assigned."
    assert sim.mdtype == "Verlet", "sim.mdtype not properly assigned."
    assert sim.natoms == 290, "sim.natoms not properly assigned."
    assert sim.nspecies == 4, "sim.nspecies not properly assigned."

def test_go():
    print("Testing the MD module on sample files for GO detection")
    sim = md.SiestaSimulation('gotestfiles', fdfb=True, fdfext='.fdf')
    assert sim.simtype == 'go', "sim.simtype not properly assigned."

def test_fc():
    print("Testing the MD module on sample files for FC detection")
    sim = md.SiestaSimulation('fctestfiles', fdfb=True, fdfext='.fdf')
    assert sim.simtype == 'phonon', "sim.simtype not properly assigned."

def test_md_imde():
    print("Testing MD module on sample files for MDE reading.")
    sim = md.SiestaSimulation('mdtestfiles', fdfb=True, fdfext='.fdf')
    print(sim.path)
    sim.iMDE(mde=True, fext=".MDE")
    assert sim.mdep == os.path.join(sim.path, 'nacl.MDE'), "sim.mdep not properly assigned."
    print(sim.mde.shape)
    assert sim.mde.shape == (sim.nsteps, 6), "sim.mde has improper shape"

def test_md_imd():
    print("Testing MD module on sample files for trajectory reading.")
    sim = md.SiestaSimulation('mdtestfiles', fdfb=True, fdfext='.fdf')
    sim.iMD(ani=True, fext='.ANI', defaultcell=True)
    print(sim.anip)
    assert sim.anip == os.path.join(sim.path, 'nacl.ANI'), "sim.anip not properly assigned."
    assert sim.universe.trajectory.dt == 0.5, "sim.universe has incorrect timestep."
    assert sim.universe.trajectory.units['time'] == 'fs', "sim.universe has incorrect time units."
    assert sim.universe.trajectory.n_atoms == sim.natoms, "sim.universe has inccorect number of atoms."
    print(sim.speclst)
    assert len(sim.speclst) == sim.natoms, "sim.speclst has incorrect length."