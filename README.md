## Ambiance_TSP
A traveling salesman problem based on the song [_Ambiance, Ambiance_](https://www.youtube.com/watch?v=EqdQyoAUQZ0) by [Sam Gooris](https://nl.wikipedia.org/wiki/Sam_Gooris).

## Problem description
In 2013, Belgian songsmith [Sam Gooris](https://nl.wikipedia.org/wiki/Sam_Gooris) rocked the charts with his dance hit [_Ambiance, Ambiance_](https://www.youtube.com/watch?v=EqdQyoAUQZ0).

During the [Nerdland Podcast](www.nerdland.be), we looked at the lyrics of this song. In his anthem, Mr. Gooris eloquently describes how he visits several Belgian villages and cities in order to engage in party-related activities. However, the order in which he visits these locations is far from optimal. [Bart Van Peer](https://twitter.com/zebbedeusje) posed the question: **_What if Mr. Gooris could rearrange his travel itinerary (and, subsequently, his lyrics) to allow for an optimal usage of his time and mileage?_**

This is a classic example of a [Traveling Salesman](https://en.wikipedia.org/wiki/Travelling_salesman_problem) problem, a well-known problem in Computer Sciences which is NP-hard, which means that the worst-case running time of any problem-solving technique will increase superpolynomially with the number of cities. In this example, Mr. Gooris visits 26 locations in this order:

```
Mal -> Ghent -> Leest -> Peer -> As -> Tielt -> Lot -> Puurs -> Lint -> Heist -> Reet -> Bree -> Schriek -> Geel -> Leut -> Doel -> Duffel -> Sinaai -> Vorst -> Niel -> Bere* -> Gits -> Boom -> Haacht -> Mal
```

Note that we have interpeted the village of _Bere_ as slang for the city of [Meulebeke](https://en.wikipedia.org/wiki/Meulebeke) (because the village of [Béré](https://en.wikipedia.org/wiki/B%C3%A9r%C3%A9,_Burkina_Faso) in Burkina Faso would be uncharacteristic), and suppose that Mr. Gooris will start and end his party tour in the village of [Mal](https://nl.wikipedia.org/wiki/Mal_(Tongeren)).

## Solution

(max number of combinations)
(requirements)
