from field import Field
from creature import Creature


def test_get_neighbours():
    field = Field()
    field.create(Creature(5, 5))
    field.create(Creature(5, 6))
    field.create(Creature(6, 5))
    field.create(Creature(6, 6))
    assert field.get_neighbours(Creature(5, 5)) == [Creature(5, 6), Creature(6, 5), Creature(6, 6)]


def test_generation_solid():
    field = Field()
    field.create(Creature(5, 5))
    field.create(Creature(5, 6))
    field.create(Creature(6, 5))
    field.create(Creature(6, 6))
    prev_gen = field.grid
    field.change_generation()
    assert field.grid == prev_gen


def test_generation_blink():
    field = Field()
    field.create(Creature(5, 5))
    field.create(Creature(5, 6))
    field.create(Creature(5, 7))
    field.change_generation()
    assert field.grid == {4: {6: True}, 5: {6: True}, 6: {6: True}}