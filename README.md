## Ambiance_TSP
A traveling salesman problem based on the song [_Ambiance, Ambiance_](https://www.youtube.com/watch?v=EqdQyoAUQZ0) by [Sam Gooris](https://nl.wikipedia.org/wiki/Sam_Gooris).

## Problem description
In 2013, Belgian songsmith [Sam Gooris](https://nl.wikipedia.org/wiki/Sam_Gooris) rocked the charts with his dance hit [_Ambiance, Ambiance_](https://www.youtube.com/watch?v=EqdQyoAUQZ0).

During the [Nerdland Podcast](www.nerdland.be), we looked at the [lyrics](https://muzikum.eu/en/123-173-5017/sam-gooris/ambiance-lyrics.html) of this song. In his anthem, Mr. Gooris eloquently describes how he visits several Belgian villages and cities in order to engage in rhyming party-related activities. However, the order in which he visits these locations is far from optimal. [Bart Van Peer](https://twitter.com/zebbedeusje) posed the question: **_What if Mr. Gooris could rearrange his travel itinerary (and, subsequently, his lyrics) to allow for an optimal usage of his time and mileage?_**

This is a classic example of a [Traveling Salesman](https://en.wikipedia.org/wiki/Travelling_salesman_problem) problem, a well-known problem in Computer Sciences which is NP-hard, which means that the worst-case running time of any problem-solving technique will increase superpolynomially with the number of cities. In this example, Mr. Gooris visits 26 locations in this order:

```
Mal -> Ghent -> Leest -> Peer -> As -> Tielt -> Lot -> Puurs -> Lint -> Heist -> Reet -> Bree -> Schriek -> Geel -> Leut -> Doel -> Duffel -> Sinaai -> Vorst -> Niel -> Bere* -> Gits -> Boom -> Haacht -> Mal
```

Note that we have interpeted the village of _Bere_ as slang for the city of [Meulebeke](https://en.wikipedia.org/wiki/Meulebeke) (because the village of [Béré](https://en.wikipedia.org/wiki/B%C3%A9r%C3%A9,_Burkina_Faso) in Burkina Faso would be uncharacteristic), and suppose that Mr. Gooris will start and end his party tour in the same location.

## Solution strategy

With _n_ being the number of locations, there are _(n-1)!/2_ possible solutions, which in this case results in 7.755605e+24. We solve this problem by using the constraint optimization solver from Google's [ORtools](https://developers.google.com/optimization/). The method we use is based on [this article](https://developers.google.com/optimization/routing/tsp).

We use the latitude and longitute of the center (as per Google Maps) of every location in the list, stored together with the location name and the planned activity of Mr. Gooris (not needed to solve the problem, but funny) in the CSV file ``ambiance.csv``. We use the Euclidean (straight line) distance between these (lat, long) coordinates in the distance matrix.

## Solution

Within an execution limit of 30 seconds, the solver returns the following optimized path for Mr. Gooris, resulting in more than 1000kms off the original path. No additional refinements were found when gradually increasing execution limits (On a 3.6 Ghz Intel Xeon processor).

```
Mal -> As -> Leut -> Bree -> Peer -> Geel -> Schriek -> Haacht -> Duffel -> Lint -> Reet -> Leest -> Boom -> Niel -> Puurs -> Doel -> Sinaai -> Heist -> Gits -> Bere -> Tielt -> Ghent -> Lot -> Vorst ->  Mal
```

The village of [Mal](https://nl.wikipedia.org/wiki/Mal_(Tongeren)) is chosen as a startpoint here, but the solution is a closed loop, so it doesn't matter where Mr. Gooris chooses to start.

![TSP_difference](https://github.com/Forceflow/Ambiance_TSP/blob/master/readme_img/TSP_diff.gif "Difference between original and optimized itinerary")

## Installation
The script requires **Python 3.6** or newer and depends on the , ``csv``, ``numpy`` and ``ortools`` packages, which you can install using your favorite package manager, for example: ``pip install csv numpy ortools``.

## Possible improvements:
 * Convert from Latitude/Longitude to actual kilometers using earth curvature, for more detailed stats
 * Use the Google Maps (or similar) API to fetch actual paths and their lengths between each location. (Like [here](http://www.theprojectspot.com/tutorial-post/solving-traveling-salesman-problem-using-google-maps-and-genetic-algorithms/9)).
 * Figure out the _exact_ location where Mr. Gooris would like to engage in party-related activities for added accuracy
 * Attack the problem using a different technique, like genetic algorithms programming (Like [here](https://towardsdatascience.com/evolution-of-a-salesman-a-complete-genetic-algorithm-tutorial-for-python-6fe5d2b3ca35)).
