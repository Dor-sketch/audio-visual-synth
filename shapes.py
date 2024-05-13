import numpy as np


def Cube():
    vertices = (
        (1, -1, -1),
        (1, 1, -1),
        (-1, 1, -1),
        (-1, -1, -1),
        (1, -1, 1),
        (1, 1, 1),
        (-1, -1, 1),
        (-1, 1, 1),
    )
    edges = (
        (0, 1),
        (0, 3),
        (0, 4),
        (2, 1),
        (2, 3),
        (2, 7),
        (6, 3),
        (6, 4),
        (6, 7),
        (5, 1),
        (5, 4),
        (5, 7),
    )

    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()


# Define the vertices of the two interlocking tetrahedrons
STAR_OF_DAVID_VERTICES = np.array(
    [
        [1, 1, 1],  # Vertex 1 of the first tetrahedron
        [1, -1, -1],  # Vertex 2 of the first tetrahedron
        [-1, 1, -1],  # Vertex 3 of the first tetrahedron
        [-1, -1, 1],  # Vertex 4 of the first tetrahedron
        [1, -1, 1],  # Vertex 1 of the second tetrahedron
        [1, 1, -1],  # Vertex 2 of the second tetrahedron
        [-1, -1, -1],  # Vertex 3 of the second tetrahedron
        [-1, 1, 1],  # Vertex 4 of the second tetrahedron
    ]
)
