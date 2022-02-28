# [type, time complexity, info]
DEFINITIONS = {
    "Quick Sort": [
        "Sorting, Divide And Conquer",
        ["Best: O(n log n)",
         "Average: O(n log n)",
         "Worst: O(n^2)"],
        """
        In simplest terms, Quick Sort functions by selecting a pivot point 
        and then organizing subsets of the dataset based on whether or not 
        they're larger than the pivot value.
        """
    ],

    "Merge Sort": [
        "Sorting, Divide And Conquer",
        ["All cases: O(n log n)"],
        """
        Merge Sort functions by dividing a dataset into smaller pieces, 
        sorting them in small segments, 
        then combining the pieces in chunks of increasing size
        Eventually, the sorted chunks are combined to form a final, sorted data set.
        """
    ],

    "Bubble Sort": [
        "Sorting, In-Place",
        ["Best: O(n)",
         "Worst and Average: O(n^2)"],
        """
        Bubble Sort is a simple-to-grasp sorting algorithm that functions based on
        the idea of "bubbling" larger values to the top of a dataset
        Though not very efficient, one of its main charms
        is its simplicity in concept and implementation.
        """
    ],

    "Optimized Bubble Sort": [
        "Sorting, In-Place",
        ["Best: O(n)",
         "Worst and Average: O(n^2)"],
        """
        Optimized Bubble Sort improves upon the speed of regular Bubble Sort by avoiding
        the last n-1 elements each loop, since those had already been placed 
        at their proper positions by the nature of Bubble Sort.
        """
    ],

    "Insertion Sort": [
        "Sorting, In-Place",
        ["Best: O(n)",
         "Worst and Average: O(n^2)"],
        """
        Insertion Sort functions by simply going through a dataset in order,
        checking for a smaller value that's ahead of a larger one, then inserting
        each element before the value ahead of the smaller one, 
        until it reaches an element smaller than the current value 
        """
    ],

    "Selection Sort": [
        "Sorting, In-Place",
        ["All cases: O(n^2)"],
        """
        Selection sort functions by going through a dataset in order,
        selecting a value, and searching for values smaller than it. When it finds
        one, it swaps the two values
        """
    ],

    "Cocktail Sort": [
        "Sorting, In-Place",
        ["Best: O(n)",
         "Worst and Average: O(n^2)"],
        """
        Cocktail sort is a variation of Bubble Sort that goes through the dataset in both directions.
        """
    ],

    # pathing
    "Breadth-First Search": [
        "Graph Search",
        ["Best and worst case: O(|V| + |E|)"],
        """
        Breadth-First Search operates by examining all nodes at each depth
        before moving on to the next level. For each node, its (unexamined) neighbors are added
        onto a queue to be examined later.
        """
    ],

    "Depth-First Search": [
        "Graph Search",
        ["Best and worst case: O(|V| + |E|)"],
        """
        Depth-First Search operates by examining all nodes along a branch before moving on
        to the next branch. It utilizes a stack to keep track of which nodes are to be scanned next.
        """
    ],

    "Dijkstra's Algorithm": [
        "Graph Search",
        ["Best and worst case: O((|V| + |E|) log |V|)"],
        """
        Dijkstra's functions using a graph with weighted edges, finding
        the lowest-cost path to the end by travelling along nodes with the lowest weights.
        NOTE: There is currently no way to manually set weights in ELPath, so nodes
        are weighted randomly.
        """
    ],

    "A* Algorithm": [
        "Graph Search",
        ["Depends on heuristic function."],
        """
        One of The most acclaimed graph search algorithms, A* utilizes the idea of
        low-cost pathfinding (Which node is closest to the beginning?)
        as well as a heuristic function (Which node is closest to the end?). 
        ELPath uses Manhattan distance for the heuristic,
        """
    ],
}
