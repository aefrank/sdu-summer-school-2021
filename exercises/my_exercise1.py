# Exercise 1
# Author: Andrea Frank <aefrank17@gmail.com>
# Date: 02 August, 2021 
# SDU Summer School 2021, Odense Denmark

import math
import numpy as np

#################################################################
#   Helper functions
#################################################################

def random_unit_vector_spheric(dims=6):
    """
    Generates a random unit vector in (hyper)spherical coordinates.

    First coordinate is radial coordinate, followed by the
    angular coordinates with the "phi" coords (those that range from
    0 to pi) first followed by the "theta" coord (ranging 0-2pi)
    """
    spheric = np.ones(dims)
    spheric[1:-1] =   math.pi*np.random.random(dims-2)  
    spheric[-1]   = 2*math.pi*np.random.random()
    return spheric

def spheric_to_cart(spheric):
    """
    Converts (hyper)spherical coordinates to Cartesian coordinates.

    Assumes first coordinate is radial coordinate, followed by the
    angular coordinates with the "phi" coords (those that range from
    0 to pi) first followed by the "theta" coord (ranging 0-2pi) .
    
    Conversion follows the pattern:

        x0 = r * cos(phi0)
        x1 = r * sin(phi0) * cos(phi1)
        x2 = r * sin(phi0) * sin(phi1) * cos(phi2)
        ...
        xi = r * sin(phi0) * ... * sin(phi_i-1) * cos(phi_i)
        ...
        xn = r * sin(phi0) * ... * sin(phi_n-1) * sin(theta)
    """
    dims = len(spheric)
    r = spheric[0]    # radial coord
    cart = np.ones(dims)
    for c in range(dims-1):
        cart[c] *= r*np.prod(np.sin(spheric[1:c+1]))*math.cos(spheric[c+1])
    cart[-1] *= r*np.prod(np.sin(spheric[1:]))
    return cart

def random_unit_vector_cart(dims=6):
    """
    Generates a random unit vector in Cartesian space.
    """
    return spheric_to_cart(random_unit_vector_spheric(dims=dims))


def eucl_dist_from_configs(config1, config2=None):
    """
    Euclidean world distance between two poses described in configuration space.
    """
    if config2 is None:
        config2 = np.zeros(len(config1))
    return np.linalg.norm(config_to_cart(config1)-config_to_cart(config2))

################################################################
#           Exercise 1
################################################################

W = [1,1,0.5,0.3,0.2,0.1]

def config_to_cart(config):
    """
    Convert configuration space (joint angle) to Cartesian world space such
    that each joint angle is weighted according to the length of the arm segment 
    it controls the position of the end effector in Euclidean world space.
    """
    return config*W

def cart_to_config(cart):
    """
    Convert Cartesian world coordinates into configuration space (joint angles).
    """
    return cart/W

def random_config_dist_away(config, dist):
    """
    Generates a random configuration <dist> Cartesian world units away 
    from the input <config>, which is defined in configuration space.
    """
    return config + cart_to_config(dist*random_unit_vector_cart(len(config)))


if __name__ == '__main__':
    D = 5
    eps = 1E-6

    initial_config = np.random.random(6)
    new_config = random_config_dist_away(config=initial_config, dist=D)
    dist = eucl_dist_from_configs(initial_config,new_config)
    err  = dist-D 

    print("Distance to new configuration: {}\nError: {}".format(dist,err))
    assert(np.abs(err) < eps)
    print("Success!")