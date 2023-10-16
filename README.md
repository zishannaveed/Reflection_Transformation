## LS-DYNA Node Reflection Tool
This Python script facilitates node reflection in LS-DYNA input files, providing a convenient method for setting up symmetric geometries. The script allows users to define a **reflection point** and **axis**, and it automatically renumbers nodes within specified groups. It is particularly useful for simulating symmetric structures.

**Usage:**

**Input File:** Provide the path to the original LS-DYNA input file (original_file_path).

**Reflection Parameters:** Set the reflection point (reflection_point), reflection direction (reflection_direction), and the number of nodes in each group (group_size).

**Output File:** Specify the desired path for the new LS-DYNA input file (new_file_path).

**Run the Script:** Execute the script to generate a new LS-DYNA input file with reflected node coordinates.

**Example**

```python
original_file_path = "plate_1.k"
new_file_path = "plate_2.k"
reflection_point = (0, 30, 0)
reflection_direction = 'x'
group_size = 5
transformed_nodes = transform_nodes(nodes_data, reflection_point, reflection_direction, group_size)
create_new_file_with_transformed_nodes(original_file_path, new_file_path, transformed_nodes)
