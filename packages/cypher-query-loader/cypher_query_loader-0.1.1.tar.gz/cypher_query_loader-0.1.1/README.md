# Cypher Query Loader

A small package that handles loading strings from `*.cypher` files into python strings.  I use this code in packages that query a database and need saved queries.  It lets me keep the code in `.cypher` format and use syntax highlighing in my IDE.

<strong>Important safetly note:</strong>This code does not check cypher files for safety or security. End users should only point their QueryLoader objects at file systems they trust and control.