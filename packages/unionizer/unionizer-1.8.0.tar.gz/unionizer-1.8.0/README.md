<h1 align="center">
  <a href="https://i.ibb.co/MnW0Y8M/360-F-133480376-PWls-Z1-Bdr2-SVn-TRpb8j-Ct-Y59-Cy-EBdo-Ut-modified.png"><img src="https://i.ibb.co/MnW0Y8M/360-F-133480376-PWls-Z1-Bdr2-SVn-TRpb8j-Ct-Y59-Cy-EBdo-Ut-modified.png" alt="unionizer" border="0" width="145"></a>
</h1>


[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/aws/mit-0/blob/master/MIT-0)
[![Python Versions](https://img.shields.io/badge/python-3.7%20|%203.8%20|%203.9%20|%203.10%20|%203.11%20|%203.12%20-blue)](https://www.python.org/downloads/)

```
unionizer: V1.8.0

Unionizer helps developers pair objects together.
```

## Installing
```shell
# Linux/macOS
python3 pip install -U unionizer

# Windows
py -3 -m pip install -U unionizer
```

# Logic
```python
unionizer.assign(1, 2) # 2 isinstance of 1 and 5
unionizer.assign(1, 5) # 5 is instance of 1 and 2
unionizer.assign(5, 7) # 7 is only instance of 5, not 1 or 2

# Set:
    1, (2, 5)

# Subset:
    5, 7

# Architecture:
    1 (
        2, 
        5 (
            7
        )
    )
```

## Local Tied Memory / Pairs
```python
bond: unionizer.Bond = unionizer.Bond(size=10) # Limit bond memory to 10.

bond.assign(object_1, object_2) # Tie object_1 and object_2 together.
# bond.delete(object_1, object_2) # Untie object_1 and object_2 from
    
bond.filter(object_2) # Filter all pairs that are tied to object_2.

bond.groups() # Return all pairs.

bond.isinstance(object_1, object_2) # Check if object_1 and object_2 are paired.
```

## Global Tied Memory / Pairs
```python
unionizer.core # (VARIABLE of backend core class object) Stored memory with no size limit unless changed

# Changing core params
#     unionizer.core(unique=True, size=10) # Limit core memory to 10 and make all keys be instance variables.

#     unionizer.set(unique=True, size=10) # Limit core memory to 10 and make all keys be instance variables.

unionizer.assign(object_1, object_2) # Tie object_1 and object_2 together.

unionizer.get(object_1) # Get object_1's tied object.

unionizer.delete(object_1) # Untie object_1 from its tied object.

unionizer.filter(object_2) # Filter all pairs that are tied to object_2.

# Properties
#     unionizer.vars # Return all instance variables.
#     unionizer.groups # Return all pairs.
#     unionizer.rules # Return all rules.
#     unionizer.memory # Return all memory.
```