#
# Utility function to flatten lists of lists into a single list containing all the elements
# Example: [[1,2,3], 4, 5] becomes [1,2,3,4,5]
#
def flatten(list):
    flattened_list = []
    for item in list:
        try:
            flattened_list.extend(item)
        except TypeError:
            flattened_list.append(item)

    return flattened_list