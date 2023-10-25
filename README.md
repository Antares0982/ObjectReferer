# Object Referrer
Keep track of your Python objects from anywhere as long as you still has the class of them.

### Explains by Copilot

The `ObjectReferrer` is used to keep track of objects that are registered with it and to retrieve them later. The class has two main methods: `register` and `get`. The `register` method takes an object as an argument and adds it to a dictionary of weak reference sets. The `get` method takes a class as an argument and returns a generator that yields all the objects that have been registered with that class.

The `ObjectReferrer` class also has a method called `get_by_base` that takes a class as an argument and returns a generator that yields all the objects that have been registered with that class or any of its base classes. This method works by first finding the inheritance tree for the given class and then collecting all the classes in that tree. It then iterates over all the classes and yields all the objects that have been registered with them.

The `ObjectReferrer` class uses two helper classes: `WeakRefSet` and `InheritanceTreeNode`. The `WeakRefSet` class is a generic class that implements a set of weak references. It is used to store weak references to objects that have been registered with the `ObjectReferrer` class. The `InheritanceTreeNode` class is also a generic class that represents a node in an inheritance tree. It is used to build the inheritance tree for a given class.

The `ObjectReferrer` class uses a dictionary to store the weak reference sets for each class. It also uses another dictionary to store the inheritance trees for each class. The inheritance trees are built lazily, as needed, when objects are registered with the `ObjectReferrer` class.

Overall, the `ObjectReferrer` class provides a simple way to keep track of objects and retrieve them later. It uses weak references to avoid keeping objects alive longer than necessary and provides a way to retrieve objects based on their class or any of their base classes. The use of inheritance trees allows for efficient retrieval of objects based on their base classes.
