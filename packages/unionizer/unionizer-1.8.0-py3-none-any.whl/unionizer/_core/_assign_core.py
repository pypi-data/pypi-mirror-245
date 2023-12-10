class Core:
    def __init__(self, size: int=None, *args, **kwargs):
        self.__assign_core_rules = {'unique': True, 'size': size}
        self.__assign_core_memory = {}
    
    def set(self, **kwargs):
        assign_core_rules = self.__assign_core_rules
        for key, value in kwargs.items():
            if key in assign_core_rules:
                assign_core_rules[key] = value

        self.__rules_size_update()

    def __rules_size_update(self):
        assign_core_rules = self.__assign_core_rules
        assign_core_memory = self.__assign_core_memory
        size = assign_core_rules['size']
        if size is not None and len(assign_core_memory) >= size:
            self.__assign_core_memory = dict(list(assign_core_memory.items())[:size])

    def filter(self, value, *args, **kwargs):
        assign_core_memory = self.__assign_core_memory
        filtered_keys = [key for key, val in assign_core_memory.items() if val == value]
        return {value: filtered_keys}

    def assign(self, key, value, *args, **kwargs):
        assign_core_rules = self.__assign_core_rules
        assign_core_memory = self.__assign_core_memory
        size = assign_core_rules['size']
        if size:
            if len(assign_core_memory) < size:
                self.__assign_value_helper(key, value)
        else:
            self.__assign_value_helper(key, value)

        if assign_core_rules['unique']:
            setattr(self, self.__clean(key), value)
        self.__assign_core_memory = assign_core_memory
        return assign_core_memory

    def isinstance(self, object_1, object_2, *args, **kwargs):
        assign_core_memory = self.__assign_core_memory
        for value in assign_core_memory.values():
            if isinstance(value, (list, tuple, set, dict)):
                if object_1 in value and object_2 in value:
                    return True
            elif value == object_1 == object_2:
                return True
        return False
    
    def __assign_value_helper(self, key, value, *args, **kwargs):
        assign_core_memory = self.__assign_core_memory
    
        if key in assign_core_memory:
            existing_value = assign_core_memory[key]
    
            if isinstance(existing_value, list):
                assign_core_memory[key].append(value)
            elif isinstance(existing_value, set):
                assign_core_memory[key].add(value)
            elif isinstance(existing_value, tuple):
                assign_core_memory[key] = existing_value + (value,)
            else:
                assign_core_memory[key] = [existing_value, value]
        else:
            assign_core_memory[key] = value
    
        self.__assign_core_memory = assign_core_memory
                

    def get(self, key, *args, **kwargs):
        return self.__assign_core_memory.get(key)

    def delete(self, key, *args, **kwargs):
        return self.__assign_core_memory.pop(key, None)

    @property
    def vars(self, *args, **kwargs):
        return [var for var in self.__assign_core_memory.keys()]

    @property
    def shape(self, *args, **kwargs):
        return f'({len(self.__assign_core_memory)},{self.size})'

    @property
    def size(self, *args, **kwargs):
        size = self.__assign_core_rules['size']
        return 'inf' if size is None else size

    @property
    def groups(self, *args, **kwargs):
        assign_core_memory = self.__assign_core_memory
        return {value: self.filter(value)[value] for value in assign_core_memory.values()}

    @property
    def rules(self, *args, **kwargs):
        return self.__assign_core_rules

    @property
    def memory(self, *args, **kwargs):
        return self.__assign_core_memory

    def __call__(self, unique: bool=True, size: int=None, *args, **kwargs):
        return self.set(unique=unique, size=size, **kwargs)

    def __getitem__(self, key, *args, **kwargs):
        return self.get(key)

    def __setitem__(self, key, value, *args, **kwargs):
        self.assign(key, value)

    def __delitem__(self, key, *args, **kwargs):
        self.delete(key)

    def __contains__(self, key, *args, **kwargs):
        return key in self.__assign_core_memory

    def __len__(self, *args, **kwargs):
        return len(self.__assign_core_memory)

    def __iter__(self, *args, **kwargs):
        return iter(self.__assign_core_memory)

    def __reversed__(self, *args, **kwargs):
        return reversed(self.__assign_core_memory)

    def __repr__(self, *args, **kwargs):
        return self.__assign_core_memory

    def __str__(self, *args, **kwargs):
        return str(self.__assign_core_memory)

    def __class_getitem__(self, item, *args, **kwargs):
        return item

    def __clean(self, attr):
        final_attr = ''.join(c if c.isalnum() else '_' for c in str(attr))
        final_attr = f'_{final_attr}' if not final_attr.isidentifier() else final_attr
        return final_attr