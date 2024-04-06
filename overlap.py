from shapely.geometry import Polygon, MultiPolygon

def get_overlap_info(shapes):
  """
  This function takes a list of shapely geometries and returns a dictionary
  containing information about overlapping regions.

  Args:
      shapes: A list of shapely geometry objects (Polygon or MultiPolygon)

  Returns:
      A dictionary with the following keys:
          overlaps: A MultiPolygon representing the combined overlap region
          counts: A dictionary where keys are tuples representing coordinates
                  of overlapping points and values represent the number of times
                  that point overlaps.
  """
  overlaps = shapes[0]  # Initialize with the first shape
  counts = {}

  for shape in shapes[1:]:
    # Perform intersection between current overlaps and the new shape
    intersection = overlaps.intersection(shape)

    # Update overlaps with the intersected area
    overlaps = overlaps.union(intersection)

    # Update overlap counts
    for point in intersection.exterior.coords:
      if point in counts:
        counts[point] += 1
      else:
        counts[point] = 1

  return {"overlaps": overlaps, "counts": counts}

# Example usage
shapes = [Polygon([(0, 0), (2, 0), (2, 1), (0, 1)]),
          Polygon([(1, 0), (3, 0), (3, 2), (1, 2)]),
          Polygon([(1, 0), (1, 2), (2, 1.5)])]

overlap_info = get_overlap_info(shapes)

# Access the overlap region as a MultiPolygon
overlap_region = overlap_info["overlaps"]

# Access the overlap counts dictionary
overlap_counts = overlap_info["counts"]

# Print information about overlaps
print("Overlap region:", overlap_region)
for point, count in overlap_counts.items():
  print(f"Point {point} overlaps {count} times")
