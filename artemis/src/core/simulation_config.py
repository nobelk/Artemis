import dataclasses
from enum import Enum
from typing import Tuple


class SpaceType(Enum):
    """Types of simulation space"""
    GRID_2D = "grid_2d"
    CONTINUOUS_2D = "continuous_2d"
    NETWORK = "network"


class TopologyType(Enum):
    """Boundary conditions for grid spaces"""
    BOUNDED = "bounded"  # Hard boundaries
    TORUS = "torus"      # Wrapped edges (periodic boundaries)


class NeighborhoodType(Enum):
    """Types of agent neighborhoods"""
    MOORE = "moore"              # 8 neighbors (includes diagonals)
    VON_NEUMANN = "von_neumann"  # 4 neighbors (no diagonals)
    CUSTOM = "custom"            # Custom interaction network


class SchedulerType(Enum):
    """Agent activation scheduling types"""
    RANDOM = "random"              # Random order each step
    SEQUENTIAL = "sequential"      # Fixed order
    STAGED = "staged"

class DataCollectionConfig:
    """Data collection configuration"""
    collection_frequency: int = 10


@dataclasses.dataclass
class SimulationConfig:
    """Simulation configuration"""
    space_type: SpaceType = SpaceType.GRID_2D
    topology: TopologyType = TopologyType.BOUNDED
    neighborhood_type: NeighborhoodType = NeighborhoodType.VON_NEUMANN
    scheduler: SchedulerType = SchedulerType.RANDOM
    dimensions: Tuple[int, ...] = (2, 2)

    # Neighborhood configuration
    interaction_radius: float = 1.0
    # Randomness configuration for mersenne_twister generator
    seed: int = 7919
    name: str = "default"
    description: str = ""
    version: str = "1.0"
    num_agents: int = 2
    max_steps: int = 10
    data_collection_config: DataCollectionConfig = DataCollectionConfig()


