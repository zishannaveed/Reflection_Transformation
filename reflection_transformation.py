# -*- coding: utf-8 -*-
"""
Created on Fri Jul 24  10:05:41 2023

@author: Zishan Naveed
"""

import re
import math

def extract_node_coordinates(content):
    # Find the *NODE section and extract the node lines
    node_section = re.search(r"\*NODE\s*([\s\S]*?)(\*\w+|$)", content)
    if not node_section:
        return []

    node_lines = node_section.group(1).strip().split('\n')

    # Extract node number, x, y, and z coordinates from each line
    nodes_data = []
    for line in node_lines:
        parts = line.split()
        node_number = int(parts[0])
        x, y, z = map(float, parts[1:4])
        nodes_data.append((node_number, x, y, z))

    return nodes_data


def transform_nodes(nodes_data, reflection_point, reflection_direction, group_size):
    # Reflect nodes in the chosen direction and renumber them in reverse order within each group
    reflected_nodes = []

    for node_id, x, y, z in nodes_data:
        group_number = (node_id - 1) // group_size + 1
        group_position = (node_id - 1) % group_size
        new_group_position = group_size - group_position - 1
        new_node_id = (group_number - 1) * group_size + new_group_position + 1
        
        if reflection_direction == 'x':
            new_x,new_y,new_z = 2 * reflection_point[0] - x, y, z
        elif reflection_direction == 'y':
            new_x,new_y,new_z = x, 2 * reflection_point[1] - y, z
        elif reflection_direction == 'z':
            new_x,new_y,new_z = x, y, 2 * reflection_point[2] - z
        else:
            raise ValueError("Invalid reflection direction")

        #reflected_nodes[new_node_id] = reflected_coords
        reflected_nodes.append((new_node_id,new_x,new_y,new_z))
       
        reflected_nodes = sorted(reflected_nodes, key=lambda x: x[0])
       
    

    return reflected_nodes
	
def create_new_file_with_transformed_nodes(original_file_path, new_file_path, transformed_nodes):
    with open(original_file_path, 'r') as file:
        content = file.read()

    # Find the *NODE section and replace the node coordinates
    node_section = re.search(r"\*NODE\s*([\s\S]*?)(\*\w+|$)", content)
    if node_section:
        node_lines = node_section.group(1).strip().split('\n')
        new_node_lines = []
        for i, line in enumerate(node_lines):
            node_number, x, y, z = transformed_nodes[i]
            # Format the node data as specified
            formatted_line = f"{str(node_number)}".rjust(8)
            formatted_line += f"{round(x, 6):.6f}".rjust(15)
            formatted_line += f"{round(y, 6):.6f}".rjust(15)
            formatted_line += f"{round(z, 6):.6f}".rjust(15)
            new_node_lines.append(formatted_line)
        new_node_section = "*NODE\n" + "\n".join(new_node_lines) + "\n"
        content = content.replace(node_section.group(0), new_node_section)

    # Write the transformed node coordinates to a new file
    with open(new_file_path, 'w') as new_file:
        new_file.write(content)

if __name__ == "__main__":
    original_file_path = "FILE_NAME"  # Replace with the actual file path
    new_file_path = "FILE_NAME"  # Replace with the desired new file path
    with open(original_file_path, 'r') as file:
        content = file.read()

    nodes_data = extract_node_coordinates(content)

    # Reflection point
    reflection_point = (0, 30, 0)  # Change this according to the desired reflection point

    # Choose the reflection direction: 'x', 'y', or 'z'
    reflection_direction = 'x'

    # Number of nodes in each group
    group_size = 5     #represent number of control point in 'r' direction


    # Transform the nodes
    transformed_nodes = transform_nodes(nodes_data, reflection_point, reflection_direction, group_size)
    
    # Create a new file with the transformed node coordinates
    create_new_file_with_transformed_nodes(original_file_path, new_file_path, transformed_nodes)