import sys
from pathlib import Path

import pytest

# Add parent directory to path to allow imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.artemis_model import ArtemisModel
from src.core.simulation_config import SimulationConfig


class TestArtemisModel:
    def test_init(self):
        """Test that ArtemisModel can be instantiated."""
        config = SimulationConfig()
        model = ArtemisModel(config)
        assert model is not None

    def test_get_random_int_returns_int(self):
        """Test that get_random_int returns an integer."""
        config = SimulationConfig()
        model = ArtemisModel(config)
        result = model.get_random_int()
        assert isinstance(result, int)

    def test_get_random_int_in_range(self):
        """Test that get_random_int returns a value between 0 and 100."""
        config = SimulationConfig()
        model = ArtemisModel(config)
        for _ in range(100):
            result = model.get_random_int()
            assert 0 <= result <= 100

    def test_get_random_float_returns_float(self):
        """Test that get_random_float returns a float."""
        config = SimulationConfig()
        model = ArtemisModel(config)
        result = model.get_random_float()
        assert isinstance(result, float)

    def test_get_random_float_in_range(self):
        """Test that get_random_float returns a value between 0 and 1."""
        config = SimulationConfig()
        model = ArtemisModel(config)
        for _ in range(100):
            result = model.get_random_float()
            assert 0.0 <= result < 1.0

    def test_random_seed_deterministic(self):
        """Test that the random seed makes results deterministic."""
        config1 = SimulationConfig()
        model1 = ArtemisModel(config1)
        int1 = model1.get_random_int()
        float1 = model1.get_random_float()

        config2 = SimulationConfig()
        model2 = ArtemisModel(config2)
        int2 = model2.get_random_int()
        float2 = model2.get_random_float()

        assert int1 == int2
        assert float1 == float2

    def test_multiple_calls_different_values(self):
        """Test that multiple calls to get_random_int produce different values."""
        config = SimulationConfig()
        model = ArtemisModel(config)
        values = [model.get_random_int() for _ in range(10)]
        # Very unlikely that all 10 values are the same
        assert len(set(values)) > 1

    def test_multiple_float_calls_different_values(self):
        """Test that multiple calls to get_random_float produce different values."""
        config = SimulationConfig()
        model = ArtemisModel(config)
        values = [model.get_random_float() for _ in range(10)]
        # Very unlikely that all 10 values are the same
        assert len(set(values)) > 1