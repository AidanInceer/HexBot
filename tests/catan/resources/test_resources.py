import unittest

from src.catan.resources.resources import Brick, Ore, Resources, Sheep, Wheat, Wood


class TestResources(unittest.TestCase):
    def test_brick(self):
        resources = Resources()
        assert resources["brick"].count == 4

    def test_ore(self):
        resources = Resources()
        assert resources["ore"].count == 0

    def test_sheep(self):
        resources = Resources()
        assert resources["sheep"].count == 2

    def test_wheat(self):
        resources = Resources()
        assert resources["wheat"].count == 2

    def test_wood(self):
        resources = Resources()
        assert resources["wood"].count == 4

    def test_brick_str(self):
        resources = Resources()
        assert str(resources["brick"]) == "4"

    def test_ore_str(self):
        resources = Resources()
        assert str(resources["ore"]) == "0"

    def test_sheep_str(self):
        resources = Resources()
        assert str(resources["sheep"]) == "2"

    def test_wheat_str(self):
        resources = Resources()
        assert str(resources["wheat"]) == "2"

    def test_wood_str(self):
        resources = Resources()
        assert str(resources["wood"]) == "4"

    def test_brick_add(self):
        resources = Resources()
        resources["brick"].count += 1
        assert resources["brick"].count == 5

    def test_ore_add(self):
        resources = Resources()
        resources["ore"].count += 1
        assert resources["ore"].count == 1

    def test_sheep_add(self):
        resources = Resources()
        resources["sheep"].count += 1
        assert resources["sheep"].count == 3

    def test_wheat_add(self):
        resources = Resources()
        resources["wheat"].count += 1
        assert resources["wheat"].count == 3

    def test_wood_add(self):
        resources = Resources()
        resources["wood"].count += 1
        assert resources["wood"].count == 5

    def test_brick_sub(self):
        resources = Resources()
        resources["brick"].count -= 1
        assert resources["brick"].count == 3

    def test_ore_sub(self):
        resources = Resources()
        resources["ore"].count -= 1
        assert resources["ore"].count == -1

    def test_sheep_sub(self):
        resources = Resources()
        resources["sheep"].count -= 1
        assert resources["sheep"].count == 1

    def test_wheat_sub(self):
        resources = Resources()
        resources["wheat"].count -= 1
        assert resources["wheat"].count == 1

    def test_wood_sub(self):
        resources = Resources()
        resources["wood"].count -= 1
        assert resources["wood"].count == 3

    def test_resource_repr(self):
        resources = Resources()
        assert repr(resources) == "Resources: brick: 4, sheep: 2, wheat: 2, wood: 4"

    def test_resource_attr(self):
        resources = Resources()
        assert resources["brick"].count + 1 == 5

    def test_getitem(self):
        resources = Resources()
        brick = resources["brick"]
        self.assertIsInstance(brick, Brick)
        self.assertEqual(brick.count, 4)

    def test_all_resources(self):
        resources = Resources()
        all_resources = resources.all_resources()
        expected_resources = [
            "brick",
            "ore",
            "sheep",
            "wheat",
            "wood",
        ]
        self.assertEqual(all_resources, expected_resources)
