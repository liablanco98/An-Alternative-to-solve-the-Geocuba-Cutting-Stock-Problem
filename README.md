# An-Alternative-to-solve-the-Geocuba-Cutting-Stock-Problem

The Cuban company GeoCuba is dedicated, among other things, to the manufacture of rectangular labels. Currently, it does not have any automatic tool that performs the label placement process for subsequent cutting. This problem is known as the Two-dimensional Cutting and Packing Problem. The number of different cut patterns that can be made increases exponentially with respect to the number of labels to be manufactured; so it is a combinatorial optimization problem, non-deterministic polynomial-time, hard.

In this work, a study is carried out on the alternative solutions proposed over the years regarding The Cutting and Packing Problem. From these, a new strategy is elaborated that, taking into account the conditions of Geocuba, allows to solve its label placement process, in a reasonable time. It consists of a genetic algorithm whose population is made up of cut patterns, resulting from using some placement heuristic on a set of labels. The evaluation function consists of applying the Simplex Method on the set of patterns, obtaining those that satisfy the demand for parts with the least waste.

Four different implementations are provided to compare the results:
- The proposed solution that combines a Genetic Algorithm, Simplex Method and Collocation Heusistics.
- A random solution that generates a series of cutting patterns using Colocation Heusistics and its optimization using the Simplex Method.
- Geocuba Strategy.
- A placement heusistic called FFD-CUT 2D.

To run and see the results:
 python3 tester.py
 
In that file you can modify the values.
 
