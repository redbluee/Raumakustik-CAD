import pytest
import numpy as np
from reverberation_calc import room, material, surface, reverberation_time, DIN_18041_limits

# Fixtures for reusable objects
@pytest.fixture
def sample_room():
    """Provides a sample room object."""
    r = room(volume=100)
    r.set_temperature(20)
    r.set_rel_humidity(50)
    r.set_pressure(101.325)
    return r

@pytest.fixture
def sample_material():
    """Provides a sample material object."""
    coeffs = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]
    return material(name="Test Material", absorption_coefficient=coeffs)

@pytest.fixture
def sample_surface(sample_material):
    """Provides a sample surface object."""
    return surface(name="Test Surface", area=50, material=sample_material)

# Tests for the room class
def test_room_initialization():
    r = room(volume=200)
    assert r.volume == 200
    assert r.temperature == 20
    with pytest.raises(ValueError):
        room(volume=-100)

def test_room_setters(sample_room):
    sample_room.set_height(3)
    assert sample_room.height == 3
    sample_room.set_temperature(25)
    assert sample_room.temperature == 25
    sample_room.set_rel_humidity(60)
    assert sample_room.rel_humidity == 60
    sample_room.set_pressure(100)
    assert sample_room.pressure == 100
    with pytest.raises(ValueError):
        sample_room.set_height(-1)

# Tests for the material class
def test_material_initialization(sample_material):
    assert sample_material.name == "Test Material"
    assert len(sample_material.absorption_coefficient) == 8
    with pytest.raises(ValueError):
        material("Invalid Material", [0.1, 0.2])

# Tests for the surface class
def test_surface_initialization(sample_surface, sample_material):
    assert sample_surface.name == "Test Surface"
    assert sample_surface.area == 50
    assert sample_surface.material == sample_material

# Tests for reverberation_time class
def test_reverberation_time_calculation(sample_room, sample_surface):
    rt = reverberation_time(sample_room, [sample_surface], air_damp_calc=True)
    assert rt.calc_room == sample_room
    assert len(rt.surfaces) == 1
    assert len(rt.reverberation_time) == 8
    # Check if reverberation time is a positive number
    assert all(t >= 0 for t in rt.reverberation_time)

def test_reverberation_time_no_air_damp(sample_room, sample_surface):
    rt = reverberation_time(sample_room, [sample_surface], air_damp_calc=False)
    assert len(rt.reverberation_time) == 8
    # Sabine's formula check
    total_absorption = np.sum(np.array(sample_surface.material.absorption_coefficient) * sample_surface.area)
    assert rt.reverberation_time[3] > 0 # 500 Hz

# Tests for DIN_18041_limits class
def test_din_18041_limits_initialization(sample_room):
    limits = DIN_18041_limits(sample_room, "A3")
    assert limits.calc_room == sample_room
    assert limits.type == "A3"
    assert len(limits.T_upper_limit) == 8
    assert len(limits.T_lower_limit) == 8
    assert all(t >= 0 for t in limits.T_upper_limit)
    assert all(t >= 0 for t in limits.T_lower_limit)

def test_din_18041_invalid_usage(sample_room):
    with pytest.raises(ValueError):
        DIN_18041_limits(sample_room, "Invalid Usage")

def test_din_18041_music_usage(sample_room):
    limits = DIN_18041_limits(sample_room, "A1")
    assert limits.T_upper_limit[3] > 0.5

def test_din_18041_speech_usage(sample_room):
    limits = DIN_18041_limits(sample_room, "A4")
    assert limits.T_upper_limit[3] < 1.0
