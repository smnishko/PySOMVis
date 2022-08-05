import numpy as np
from PIL import Image

def read_dataset(data_path, name):
    X = []

    with open(data_path + name + "/" + name + ".vec", "r") as vector_file:
        for line in vector_file:
            if line.startswith("$"):
                continue
            X.append(np.array(line.strip().split(" ")[:-1]).astype(np.float))
    return X

def convert_to_binary(image):
    return np.amax(image, axis=2)//255

def is_active_unit(image, x, y, width, height):
    x0 = min(x, image.shape[1])
    y0 = min(y, image.shape[0])
    x1 = min(x + width, image.shape[1])
    y1 = min(y + height, image.shape[0])

    return (np.sum(image[y0:y1, x0:x1])/image[y0:y1, x0:x1].size) > 0.5

def convert_to_active_unit_matrix(image, som_width, som_height):
    unit_width = image.shape[1]/som_width
    unit_height = image.shape[0]/som_height

    active_unit_matrix = np.zeros([som_width, som_height], dtype = int)

    for l in range(som_height):
        for c in range(som_width):
            x = int(c * unit_width)
            y = int(l * unit_height)

            active_unit_matrix[c, l] = (1 if is_active_unit(image, x, y, int(unit_width), int(unit_height)) else 0)

    return active_unit_matrix.T

def is_out_of_bounds(array, x, y):
    return x < 0 or y < 0 or array.shape[0] <= x or array.shape[1] <= y

def calculate_distances_for_unit(active_unit_matrix, distance_matrix, unit):
    visited_units = active_unit_matrix != 1
    active_units = []
    next_active_units = [unit]
    visited_units[unit[0], unit[1]] = True

    distance = 0 

    while len(next_active_units) > 0:
        active_units = next_active_units
        next_active_units = []

        while len(active_units) > 0:
            current_unit = active_units.pop(0)
            x = current_unit[0]
            y = current_unit[1]

            distance_matrix.set_distance_by_coords(unit[0], unit[1], x, y, distance)

            # neighbourhood
            if not is_out_of_bounds(visited_units, x-1, y) and not visited_units[x-1, y]:
                next_active_units.append([x-1, y])
                visited_units[x-1, y] = True
            if not is_out_of_bounds(visited_units, x+1, y) and not visited_units[x+1, y]:
                next_active_units.append([x+1, y])
                visited_units[x+1, y] = True
            if not is_out_of_bounds(visited_units, x, y-1) and not visited_units[x, y-1]:
                next_active_units.append([x, y-1])
                visited_units[x, y-1] = True
            if not is_out_of_bounds(visited_units, x, y+1) and not visited_units[x, y+1]:
                next_active_units.append([x, y+1])
                visited_units[x, y+1] = True

        #print(next_active_units)

        distance += 1

def calculate_distance_matrix(active_unit_matrix):
    distance_matrix = DistanceMatrix(active_unit_matrix)

    for i, unit in enumerate(distance_matrix.get_active_units()):
        calculate_distances_for_unit(active_unit_matrix, distance_matrix, unit)

    return distance_matrix

def load_mnemonic_image(image_path, som_width, som_height):
    img = Image.open(image_path)
    img = convert_to_binary(np.asarray(img))

    active_unit_matrix = convert_to_active_unit_matrix(img, som_width, som_height)
    distance_matrix = calculate_distance_matrix(active_unit_matrix)

    return active_unit_matrix, distance_matrix

class DistanceMatrix:

    def __init__(self, active_unit_matrix):
        self.unit_index = []

        for x in range(active_unit_matrix.shape[0]):
            for y in range(active_unit_matrix.shape[1]):
                if active_unit_matrix[x, y] == 1:
                    self.unit_index.append([x, y])

        self.distance_array = np.full((len(self.unit_index), len(self.unit_index)), np.inf)

    def _get_index(self, x, y):
        for i, elem in enumerate(self.unit_index):
            if x == elem[0] and y == elem[1]:
                return i
        return -1

    def set_distance_by_index(self, i0, i1, value):
        self.distance_array[i0, i1] = value
        self.distance_array[i1, i0] = value

    def get_distance_by_index(self, i0, i1):
        return self.distance_array[i0, i1]

    def set_distance_by_coords(self, x0, y0, x1, y1, value):
        i0 = self._get_index(x0, y0)
        i1 = self._get_index(x1, y1)

        if i0 == -1 or i1 == -1:
            return

        return self.set_distance_by_index(i0, i1, value)

    def get_distance_by_coords(self, x0, y0, x1, y1):
        i0 = self._get_index(x0, y0)
        i1 = self._get_index(x1, y1)

        if i0 == -1 or i1 == -1:
            return np.inf

        return self.get_distance_by_index(i0, i1)

    def get_active_unit_count(self):
        return len(self.unit_index)

    def get_active_units(self):
        return self.unit_index

    def show_distance_map(self, image_width, image_height, x, y, normalize = False):
        distance_map = np.full((image_height, image_width), 0)

        for xp in range(distance_map.shape[1]):
            for yp in range(distance_map.shape[0]):
                dist = self.get_distance_by_coords(x, y, xp, yp)

                distance_map[yp, xp] = (dist if dist != np.inf else 0)

        if normalize:
            distance_map = distance_map/np.max(distance_map)

        plt.imshow(distance_map)
        plt.show()
