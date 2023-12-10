"""@package MassFlow
  Massflow for compressible flow
"""

import numpy as np

# from . import IterativeSolve
from scipy.optimize import fsolve, newton
from ..common import defaultgas as defg

# internal initialization (estimated) Mach for Sigma->Mach computations
def __MachSub_sigma(sigma, gamma):
    return 1.0 - np.sqrt(
        (1.0 - 1.0 / sigma) * (4.0 * (gamma - 1.0) / (3.0 - gamma))
    )  # (2./(gamma+1.))**(.5*(gamma+1.)/(gamma-1.))/sigma


def __MachSup_sigma(sigma, gamma):
    return 1.0 + np.sqrt((sigma - 1.0) * (4.0 * (gamma - 1.0) / (3.0 - gamma)))


# -- Compressible flow functions  --


def WeightMassFlow(Mach, r=287.1, gamma=defg._gamma):
    return (
        np.sqrt(gamma)
        * Mach
        * (1.0 + 0.5 * (gamma - 1) * Mach ** 2) ** (-0.5 * (gamma + 1.0) / (gamma - 1.0))
    )


def Sigma_Mach(Mach, gamma=defg._gamma):
    return (2.0 / (gamma + 1.0) * (1.0 + 0.5 * (gamma - 1) * Mach ** 2)) ** (
        0.5 * (gamma + 1.0) / (gamma - 1.0)
    ) / Mach


def Mach_Sigma(sigma, Mach=2.0, gamma=defg._gamma):
    if np.size(Mach) != 1:
        Minit = np.where(Mach <= 1.0, __MachSub_sigma(sigma, gamma), __MachSup_sigma(sigma, gamma))
    else:
        Minit = Mach

    def sigma_of_mach(m):
        return Sigma_Mach(m, gamma) - sigma

    result = newton(sigma_of_mach, Minit)
    return result  # if np.size(result)!=1 else np.asscalar(result)


def MachSub_Sigma(sigma, gamma=defg._gamma):
    # initial guess
    Mach = __MachSub_sigma(sigma, gamma)
    return Mach_Sigma(sigma, Mach, gamma)


def MachSup_Sigma(sigma, gamma=defg._gamma):
    # initial guess
    # cg = (gamma+1.)/(gamma-1.)
    # Mach = np.sqrt((sigma*cg**(.5*cg))**(2./(cg-1.))-cg)
    Mach = __MachSup_sigma(sigma, gamma)
    return Mach_Sigma(sigma, Mach, gamma)
