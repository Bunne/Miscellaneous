DataTools
=========
Small tools I make to handle data I work with.

Most of these tools were created for research purposes, or for fun. I put up what I can.


Projects
========
### Relation Extraction
Take a table of relational objects related by ID from an SQL table and output the actual relationships side-by-side.

Example:
  
    Input:
    ID | Name   | Parent
    --------------------
    1  | Fruit  | 0
    2  | Apple  | 1
    3  | Orange | 1
    
    Output:
    Apple, Fruit
    Orange, Fruit
  
#### Use
Translate relational data of this format into a format easily convertable into tree structures for visualization.
