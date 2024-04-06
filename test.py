from itertools import combinations

def get_combinations(items, n):
  """
  This function returns all possible combinations of n items from a list.

  Args:
      items: A list of items to generate combinations from.
      n: The number of items to include in each combination.

  Returns:
      A list of tuples representing all possible combinations.
  """

  if n > len(items):
    return []  # Handle case where n is greater than the list length
  return list(combinations(items, n))

# Example usage
items = [i for i in range(15)]
n = 7

combinations = get_combinations(items, n)

for combo in combinations:
  print(combo)