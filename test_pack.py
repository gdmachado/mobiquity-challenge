"""Class file implementing tests for the Packer class."""

import pytest
from pack import Packer, APIException


@pytest.fixture
def empty_packer():
    """Return a Packer instance initiated with default (empty) values."""
    return Packer()


@pytest.fixture
def valid_packer():
    """
    Return a Packer instance initiated with a valid test package.

    The package used for testing is as follows:
        50 : (1,10,€60) (2,20,€100) (3,30,€100)
    """
    return Packer('50 : (1,10,€60) (2,20,€100) (3,30,€100)')


@pytest.fixture(scope='session')
def input_file(tmpdir_factory):
    """Generate a temporary file used for testing the parse_file method."""
    rows = [('81 : (1,53.38,€45) (2,88.62,€98) (3,78.48,€3) (4,72.30,€76) '
             '(5,30.18,€9) (6,46.34,€48)'), '8 : (1,15.3,€34)',
            ('75 : (1,85.31,€29) (2,14.55,€74) (3,3.98,€16) (4,26.24,€55) '
             '(5,63.69,€52) (6,76.25,€75) (7,60.02,€74) (8,93.18,€35) '
             '(9,89.95,€78)'),
            ('56 : (1,90.72,€13) (2,33.80,€40) (3,43.15,€10) (4,37.97,€16) '
             '(5,46.81,€36) (6,48.77,€79) (7,81.80,€45) (8,19.36,€79) '
             '(9,6.76,€64)')]

    expected = [(8100,
                 ((1, 5338, 45), (2, 8862, 98), (3, 7848, 3), (4, 7230, 76),
                  (5, 3018, 9), (6, 4634, 48))), (800, ((1, 1530, 34), )),
                (7500, ((1, 8531, 29), (2, 1455, 74), (3, 398, 16),
                        (4, 2624, 55), (5, 6369, 52), (6, 7625, 75),
                        (7, 6002, 74), (8, 9318, 35), (9, 8995, 78))),
                (5600, ((1, 9072, 13), (2, 3379, 40), (3, 4315, 10),
                        (4, 3797, 16), (5, 4681, 36), (6, 4877, 79),
                        (7, 8180, 45), (8, 1936, 79), (9, 676, 64)))]

    p = tmpdir_factory.mktemp('input_data').join('input_file')

    with open(p, 'w+') as file:
        for row in rows:
            print(row, file=file)

    return (p, expected)


def test_default_available_items(empty_packer):
    """Test emptyness of available_items when instancing an empty Packer."""
    assert empty_packer.available_items == []
    assert empty_packer.num_available_items == 0


def test_default_inserted_items(empty_packer):
    """Test emptyness of inserted_items when instancing an empty Packer."""
    assert empty_packer.inserted_items == []
    assert empty_packer.num_inserted_items == 0


def test_default_maximum_weight(empty_packer):
    """Test default max_weight when instancing an empty Packer."""
    assert empty_packer.max_weight == 10000


def test_default_package_weight(empty_packer):
    """Test default total_weight when instancing an empty Packer."""
    assert empty_packer.total_weight == 0


def test_default_package_value(empty_packer):
    """Test default total_value when instancing an empty Packer."""
    assert empty_packer.total_value == 0


def test_valid_available_items(valid_packer):
    """Test available_items when instancing a non-empty, valid Packer."""
    assert valid_packer.available_items == [(1, 1000, 60), (2, 2000, 100),
                                            (3, 3000, 100)]
    assert valid_packer.num_available_items == 3


def test_valid_inserted_items(valid_packer):
    """Test inserted_items when instancing a non-empty, valid Packer."""
    assert valid_packer.inserted_items == []
    assert valid_packer.num_inserted_items == 0


def test_valid_maximum_weight(valid_packer):
    """Test max_weight when instancing a non-empty, valid Packer."""
    assert valid_packer.max_weight == 5000


def test_valid_package_weight(valid_packer):
    """Test total_weight when instancing a non-empty, valid Packer."""
    assert valid_packer.total_weight == 0


def test_valid_package_value(valid_packer):
    """Test total_weight when instancing a non-empty, valid Packer."""
    assert valid_packer.total_value == 0


def test_parse_file(input_file, empty_packer):
    """Test behavior of parse_file class method."""
    result = [x for x in empty_packer.parse_file(input_file[0])]
    expected = input_file[1]
    assert result == expected


def test_parse_input_row(empty_packer):
    """Test behavior of parse_input_row static method."""
    input_data = '50 : (1,10,€60) (2,20,€100) (3,30,€100)'
    expected = (5000, ((1, 1000, 60), (2, 2000, 100), (3, 3000, 100)))
    assert empty_packer.parse_input_row(input_data) == expected


def test_available_append(empty_packer):
    """Test behavior of available_append method."""
    empty_packer.available_append((1, 1000, 60))
    assert (1, 1000, 60) in empty_packer.available_items
    assert empty_packer.num_available_items == 1


def test_inserted_append(empty_packer):
    """Test behavior of inserted_append method."""
    empty_packer.inserted_append((1, 1000, 60))
    assert (1, 1000, 60) in empty_packer.inserted_items
    assert empty_packer.num_inserted_items == 1


@pytest.mark.parametrize(
    'input_data, error_message',
    [('120 : (1,10,€60) (2,20,€100) (3,30,€100)',
      'Package weight must not be over 100'),
     ('50 : (1,10,€60) (2,20,€100) (3,30,€100) (3,30,€100) (3,30,€100) '
      '(3,30,€100) (3,30,€100) (3,30,€100) (3,30,€100) (3,30,€100) (3,30,€100)'
      ' (3,30,€100) (3,30,€100) (3,30,€100) (3,30,€100) (3,30,€100)',
      'Package\'s number of avalable items must not be over 15'),
     ('50 : (1,10,€60) (2,20,€100) (3,30,€120)',
      'Max weight and cost of an item must not be over 100'),
     ('50 : (1,10,€60) (2,20,€100) (3,300,€100)',
      'Max weight and cost of an item must not be over 100')])
def test_max_weight_constraint(input_data, error_message):
    """Test all of the challenge's constraints, expect APIException."""
    with pytest.raises(
            APIException, match=error_message,
            message='Expecting APIException'):
        Packer(input_data)


@pytest.mark.parametrize('input_data, expected_solution',
                         [('50 : (1,10,€60) (2,20,€100) (3,30,€100)', '2,3'),
                          ('8 : (1,15.3,€34)', '-')])
def test_solve_method(input_data, expected_solution):
    """Test functionality of the solve method, comparing to known solution."""
    packer = Packer(input_data)
    packer.solve()
    assert packer.__str__() == expected_solution
