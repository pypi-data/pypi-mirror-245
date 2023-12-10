string = """
V1.8.5

Unionizer helps developers pair objects together.

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

For local pairs:
    ```
    bond: unionizer.Bond = unionizer.Bond(size=10) # Limit bond memory to 10.

    bond.assign(object_1, object_2) # Tie object_1 and object_2 together.

    # bond.delete(object_1, object_2) # Untie object_1 and object_2 from

    bond.filter(object_2) # Filter all pairs that are tied to object_2.

    bond.groups() # Return all pairs.

    bond.isinstance(object_1, object_2) # Check if object_1 and object_2 are paired.
    ```

For global pairs:
    ```
    unionizer.core # Stored memory with no size limit unless changed

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
"""

print(string)