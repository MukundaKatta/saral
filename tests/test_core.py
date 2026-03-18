"""Tests for Saral."""
from src.core import Saral
def test_init(): assert Saral().get_stats()["ops"] == 0
def test_op(): c = Saral(); c.process(x=1); assert c.get_stats()["ops"] == 1
def test_multi(): c = Saral(); [c.process() for _ in range(5)]; assert c.get_stats()["ops"] == 5
def test_reset(): c = Saral(); c.process(); c.reset(); assert c.get_stats()["ops"] == 0
def test_service_name(): c = Saral(); r = c.process(); assert r["service"] == "saral"
