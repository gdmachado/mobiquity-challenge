"""
Main class file for the Packer class.

The Packer class contains all code for parsing
input files and calculating the solution for the knapsack problem.
"""

import re
import sys


class APIException(Exception):
    """Exception risen during handling of challenge constraints."""

    pass


class Packer(object):
    """Main Packer class."""

    def __init__(self, row=None):
        """Items expects tuples in the form of (index, weight, cost)."""
        self.inserted_items = []
        self.num_inserted_items = 0
        self.total_weight = 0
        self.total_value = 0

        if row is None:
            self.max_weight = 10000
            self.available_items = []
            self.num_available_items = 0
        else:
            input_info = self.parse_input_row(row)

            # Check for max weight constraint
            if input_info[0] > 100 * 100:
                raise APIException('Package weight must not be over 100')

            # Check for package's number of items constraint
            if len(input_info[1]) > 15:
                raise APIException(
                    'Package\'s number of avalable items must not be over 15')

            # Check for package items' weight and cost constraint
            for item in input_info[1]:
                if item[1] > 100 * 100 or item[2] > 100:
                    raise APIException(
                        'Max weight and cost of an item must not be over 100')

            self.max_weight = input_info[0]
            self.available_items = list(input_info[1])
            self.num_available_items = len(input_info[1])

    @classmethod
    def parse_file(cls, file_path):
        """
        Parse input files.

        Iterate through input file, yielding the final input information in
        the form of (package_weight, (thing, thing, ...)).
        """
        with open(file_path, 'r+') as file:
            for row in file:
                yield cls.parse_input_row(row)

    @staticmethod
    def parse_input_row(row):
        """
        Parse a row from input file.

        Uses regex to extract each piece of information from each row.
        This converts given weight into integer form by multiplying by 100, to
        make it possible for us to use the dynamic programming solution.

        Expect rows in the form of:
            package_weight : (item_id,item_weight,item_value)
        Example:
            50 : (1,10,€60) (2,20,€100) (3,30,€100)
        """
        package_weight_re = re.compile(r'^[0-9.]+')
        things_re = re.compile(r'\(([0-9]+),([0-9.]+),€([0-9]+)\)')

        package_weight = int(float(package_weight_re.findall(row)[0]) * 100)
        things = tuple((int(x[0]), int(float(x[1]) * 100), int(x[2]))
                       for x in things_re.findall(row))

        return (package_weight, things)

    def available_append(self, item):
        """Simply add a new item to the list of available items."""
        self.available_items.append(item)
        self.available_items.sort()
        self.num_available_items += 1

    def inserted_append(self, item):
        """Add a new item onto the inserted items list, update totals."""
        self.inserted_items.append(item)
        self.inserted_items.sort()
        self.num_inserted_items += 1
        self.total_weight += item[1]
        self.total_value += item[2]

    def pack(self, package_info):
        """
        Perform solution for the knapsack problem.

        Implementation of the dynamic programming algorithm is performed here.
        """
        self.max_weight = package_info[0]
        for item in package_info[1]:
            self.available_append(item)

        # Solve the problem using Dynamic Programming
        self.solve()

    def solve(self):
        """
        Solve the knapsack problem using Dynamic Programming.

        The solve method performs the Dynamic Programming algorithm on itself,
        uses the resulting array for determining what items were picked, and
        appends those items into inserted_items.
        """
        # Initiate our temporary array
        A = [[0 for x in range(self.max_weight + 1)]
             for x in range(self.num_available_items + 1)]

        # Build array for determining maximum total weight
        for i in range(self.num_available_items + 1):
            for j in range(self.max_weight + 1):
                if self.available_items[i - 1][1] > j:
                    A[i][j] = A[i - 1][j]
                else:
                    A[i][j] = max(A[i - 1][j],
                                  A[i - 1][j - self.available_items[i - 1][1]]
                                  + self.available_items[i - 1][2])

        # At this point the solution is complete, but what we have so far is
        # the total value of the final solution. We need to iterate the
        # array in order to find what items were picked for the solution.
        self.compute_items(A)

    def compute_items(self, A):
        """
        Compute items selected by the Dynamic Programming algorithm.

        Iterates through the array passed, determining which items among
        available_items were picked for the solution.
        """
        items = self.available_items
        w = self.max_weight

        # Iterate resulting array for determining which things were picked
        i = self.num_available_items
        j = self.max_weight

        while i > 0:
            if (items[i - 1][1] <= w and A[i][j] -
                    A[i - 1][j - items[i - 1][1]] == items[i - 1][2]):
                # when it's determined that item is in package, append it
                # to inserted items list
                self.inserted_append(items[i - 1])
                i -= 1
                j -= items[i][1]
            else:
                i -= 1

    def __str__(self):
        """
        Redefine __str__ method for Packer class.

        String representation of the package, used for challenge output.
        """
        if self.inserted_items:
            return ','.join([str(x[0]) for x in self.inserted_items])
        return '-'


if __name__ == '__main__':
    filename = sys.argv[1]

    for info in Packer.parse_file(filename):
        packer = Packer()
        packer.pack(info)
        print(packer)
