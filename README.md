### The Ripple-Spreading Algorithm for the $k$-Color Shortest Path Problem

##### Reference: Y.M. Ma, H. Zhou, X.B. Hu. The ripple-spreading algorithm for the k-color shortest path problem[C]//2022 IEEE Symposium Series on Computational Intelligence (SSCI). IEEE.

The $k$-color shortest path problem ($k$-CSPP) aims to find the shortest path that traverses at most $k$ colors on edge-colored graphs.

| Variables     | Meaning                                                      |
| ------------- | ------------------------------------------------------------ |
| network       | Dictionary, {node 1: {node 2: [weight 1, weight 2, ...], ...}, ...} |
| source        | The source node                                              |
| destination   | The destination node                                         |
| k             | The maximum number of colors traversed by the path           |
| nn            | The number of nodes                                          |
| neighbor      | Dictionary, {node 1: {node 2: [length, color], ...}, ...}    |
| v             | The ripple-spreading speed (i.e., the minimum length of arcs) |
| t             | The simulated time index                                     |
| nr            | The number of ripples - 1                                    |
| epicenter_set | List, the epicenter node of the i-th ripple is epicenter_set[i] |
| path_set      | List, the path of the i-th ripple from the source node to node i is path_set[i] |
| radius_set    | List, the radius of the i-th ripple is radius_set[i]         |
| active_set    | List, active_set contains all active ripples                 |
| objective_set | List, the objective value of the traveling path of the i-th ripple is objective_set[i] |
| color_set     | List, the colors traversed by the traveling path of the i-th ripple is color_set[i] |
| Omega         | Dictionary, Omega[n] = i denotes that ripple i is generated at node n |

#### Example

![k-CSPP example](C:\Users\dell\Desktop\研究生\个人算法主页\The ripple-spreading algorithm for the k-color shortest path problem\k-CSPP example.png)

```python
if __name__ == '__main__':
    # The color: 1 denotes black, 2 denotes red, 3 denotes blue, and 4 denotes green.
    temp_network = {
        0: {1: [1, 1], 3: [1, 4]},
        1: {2: [1, 2], 4: [1, 3]},
        2: {5: [1, 3]},
        3: {6: [1, 1]},
        4: {3: [1, 1], 7: [1, 4]},
        5: {4: [1, 1], 8: [1, 4]},
        6: {7: [1, 3]},
        7: {8: [1, 2]},
        8: {}
    }
    source_node = 0
    destination_node = 8
    color_num = 3
    print(main(temp_network, source_node, destination_node, color_num))
```

##### Output:

```python
{
    'path': [0, 1, 4, 3, 6, 7, 8], 
    'color': {1, 2, 3}, 
    'length': 6,
}
```

