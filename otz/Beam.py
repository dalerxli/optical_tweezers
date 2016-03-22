import pdb
import numpy as np
import scipy as sp

h = 6.626E-34
c = 3.0E8

def uniform(max_angle, intensity):
    def profile(phi):
        if (abs(phi) < max_angle):
            return intensity
        else:
            return 0
    return profile

def default_profile(angle):
    flux = 1.48e18
    solid_angle = 2*np.pi*(1-np.cos(np.pi/8))
    dFlux = flux/solid_angle
    return uniform(np.pi/8.0, 1)(angle)

class Bead:
    def __init__(self, diameter, index=2, mass=1, r=0, z=None):
        self.disable = diameter
        self.radius = diameter/2.0
        self.mass = mass
        self.r = r
        if z is None:
            z = diameter
        self.z = z
        self.index = index
    def set_position(self, r, z):
        self.r = r
        self.z = z

class Beam:
    def __init__(self, wavelength, profile=default_profile):
        self.profile = profile
        self.wavelength = wavelength
    def force(self, bead):
        """
        WARNING: This function only returns the force in a 2d plane.
        To return the true force in 3d, it needs to be modified to
        integrate over azimuthal angle as well.
        """
        r = bead.r
        z = bead.z
        n = bead.index
        R = bead.radius
        d = np.sqrt(z**2+r**2)
        phi_prime = np.arctan2(r,z)

        def theta(phi):
            return np.arctan2(R*np.sin(phi),d-R*np.cos(phi))
        def theta_prime(phi):
            return theta(phi) + phi_prime
        def theta2(phi):
            return np.arcsin(np.sin(phi+theta(phi))/n)
        def delta_theta(phi):
            return 2*theta2(phi)
        def p(phi):
            return self.profile(phi)*h*c/self.wavelength
        def dF_r(phi):
            angle = theta_prime(phi)
            return -p(angle)*(np.sin(angle)-np.sin(angle+delta_theta(phi)))
        def dF_z(phi):
            angle = theta_prime(phi)
            return -p(angle)*(np.cos(angle)-np.cos(angle+delta_theta(phi)))
        F_r = sp.integrate.quad(dF_r, -np.pi/2.0, np.pi/2.0)
        F_z = sp.integrate.quad(dF_z, -np.pi/2.0, np.pi/2.0)
        return (F_r, F_z)

    def r_potential(self, bead, r_lim=None, z=None, dx = None):
        if r_lim is None:
            r_lim = 2*bead.radius
        if z is not None:
            bead.z = z
        if dx is None:
            dx = r_lim/1e4
        r = np.arange(-r_lim, r_lim, dx)
        def restoring_force(dist):
            bead.r = dist
            return self.force(bead)[0][0]
        force_r = [restoring_force(dist) for dist in r]
        V = -sp.integrate.cumtrapz(force_r, r)
        return (r[:-1],V)
