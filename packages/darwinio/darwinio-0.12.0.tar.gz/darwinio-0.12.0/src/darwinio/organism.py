# The GPLv3 License (GPLv3)

# Copyright © 2023 Tushar Maharana, and Mihir Nallagonda

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Organism class and related stuff.

Classes:
--------
Organism: A class representing an organism.

Functions:
--------
reproduce: Generate offspring of the two Organisms.
"""

from __future__ import annotations

import random

import numpy as np

import darwinio.brain as brn
import darwinio.genome as gn


class Organism:
    """A class representing an organism.

    Class Attributes:
    ---------
    temp_range: Range of temperature values for the organism's adaptation.

    energy_range: Range of energy values for the organism's energy capacity.

    reproductive_types: Range of reproductive type values for the organism's
    reproductive strategy.

    Attributes:
    ---------
    genome_array: A Numpy array representing the organism's genome.

    neural_network: A neural network generated from the genome of the organism
    """

    temp_range: tuple[int, int] = (30, 150)
    energy_range: tuple[int, int] = (100, 1000)
    reproductive_types: tuple[int, int] = (0, 1 + 1)

    def __init__(
        self,
        genome_array: np.ndarray,
    ) -> None:
        """Initializes an instance of the Organism class.

        Args:
        -----
        genome_array: A Numpy array representing the organism's genome.
        """

        self.genome_array: np.ndarray = genome_array

        # assign a neural_network generated from the genome
        neural_structure = np.array([2, 2])
        weights: np.ndarray = brn.create_weights(self.genome_array, neural_structure)
        self.neural_network = brn.NeuralNetwork(weights, neural_structure)

        # range
        self.temp_range: tuple[int, int] = (30, 150)
        self.energy_range: tuple[int, int] = (100, 1000)
        self.reproductive_types: tuple[int, int] = (0, 1 + 1)

    def get_tier(self) -> float:
        """Return the classification tier."""
        return np.sum(self.genome_array[:3]) / (
            self.temp_range[1] + self.energy_range[1] + self.reproductive_types[1]
        )

    @classmethod
    def random(cls) -> Organism:
        """Generate a random organism.

        Returns:
        ---------
        Organism: A random instance of the Organism class.
        """
        characters: np.ndarray = np.array(
            (
                random.randint(*sorted(cls.temp_range)),
                random.randint(*sorted(cls.energy_range)),
                random.randint(*sorted(cls.reproductive_types)),
            )
        )
        return cls(characters)


def reproduce(
    parent_1: Organism, parent_2: Organism, mutation_factor: float
) -> Organism:
    """Generate offspring of the two Organisms.

    Args:
    -----
    parent_1(np.ndarray): One of the parent Organisms

    parent_2(np.ndarray): One of the parent Organisms

    mutation_factor(float): A value between 0 and 1 (inclusive) representing
    the probability of a mutation occurring in the offspring's genome.

    Returns:
    ---------
    offspring: Child of the parents.
    """
    offspring_genome: np.ndarray = gn.generate_offspring_genome(
        parent_1.genome_array, parent_2.genome_array, mutation_factor
    )
    return Organism(offspring_genome)
