How to test this code:

1. Download contents of folder
2. Open command prompt / bash shell inside folder
3. run the following command `pip install rich`
3. Type "python test.py"
4. If you don't get any errors, that means it works.

The coordinate system:

- The coordinate of any cell in the grid is just an int
- See the map.svg file for the coordinates of the tile cells in a size-3 board
- In the size-3 board,
    - A step in the north-east direction adds 1 to the coordinate
    - A step to the north adds 23 to the coordinate
    - A step to the north-west adds 22 to the coordinate
    - A step to the south-west subtracts 1 from the coordinate
    - A step to the south subtracts 23 from the coordinate
    - A step to the south-east subtracts 22 from the coordinate
    - All coordinates are modulo 507