## Ambiance_TSP
A Traveling Salesman problem based on the song [_Ambiance, Ambiance_](https://www.youtube.com/watch?v=EqdQyoAUQZ0) by [Sam Gooris](https://nl.wikipedia.org/wiki/Sam_Gooris). (And some other songs.)

[![nerdland_logo](https://github.com/Forceflow/Ambiance_TSP/blob/master/readme_img/nerdland_logo.JPG)](http://www.nerdland.be)

## Problem description
In 1999, Belgian songsmith [Sam Gooris](https://nl.wikipedia.org/wiki/Sam_Gooris) rocked the charts with his dance hit [_Ambiance, Ambiance_](https://www.youtube.com/watch?v=EqdQyoAUQZ0).

During the [March 2019 edition](https://soundcloud.com/lieven-scheire/nerdland-maandoverzicht-maart-2019) of the [Nerdland Science Podcast](www.nerdland.be) ([listen at 39:08](https://soundcloud.com/lieven-scheire/nerdland-maandoverzicht-maart-2019#t=39:11)), whilst discussing the news that [amoeba had been succesfully used in problem-solving](https://phys.org/news/2018-12-amoeba-approximate-solutions-np-hard-problem.html), we looked at the [lyrics](https://muzikum.eu/en/123-173-5017/sam-gooris/ambiance-lyrics.html) of this song. In his anthem, Mr. Gooris eloquently describes how he visits several Belgian villages and cities in order to engage in rhyming party-related activities. However, the order in which he visits these locations is far from optimal. [Bart Van Peer](https://twitter.com/zebbedeusje) posed the question: **_What if Mr. Gooris could rearrange his travel itinerary (and, subsequently, his lyrics) to allow for an optimal usage of his time and mileage?_**

This is a classic example of a [Traveling Salesman](https://en.wikipedia.org/wiki/Travelling_salesman_problem) problem, a well-known problem in Computer Sciences which is [NP-hard](https://en.wikipedia.org/wiki/NP-hardness), which means that the worst-case running time of any problem-solving technique will increase [superpolynomially](https://en.wikipedia.org/wiki/Time_complexity#Polynomial_time) with the number of cities. In this instance, Mr. Gooris visits 24 locations in the following order, derived from the lyrics:

```
Mal -> Ghent -> Leest -> Peer -> As -> Tielt -> Lot -> Puurs -> Lint -> Heist -> Reet -> Bree -> Schriek -> Geel -> Leut -> Doel -> Duffel -> Sinaai -> Vorst -> Niel -> Bere* -> Gits -> Boom -> Haacht -> Mal
```

We name this problem TSP, a _Travelling Sam Problem_.

## Solution strategy

With _n_ being the number of locations, there are _(n-1)!/2_ possible solutions, which in this case results in 1.2926008e+22
. We solve this problem by using the constraint optimization solver from Google's [ORtools](https://developers.google.com/optimization/). The method we use is based on [this article](https://developers.google.com/optimization/routing/tsp).

We use the latitude and longitute of the center (as per Google Maps) of every location in the list, stored together with the location name and the planned activity of Mr. Gooris (not needed to solve the problem, but funny) in the CSV file ``ambiance.csv``. We use the Euclidean (straight line) distance between these (lat, long) coordinates in the distance matrix.

## Solution

Within an execution limit of 30 seconds, the solver returns the following optimized path for Mr. Gooris, resulting in more than 1000kms off the original path. No additional refinements were found when gradually increasing execution limits (On a 3.6 Ghz Intel Xeon processor).

```
Mal -> As -> Leut -> Bree -> Peer -> Geel -> Schriek -> Haacht -> Duffel -> Lint -> Reet -> Leest -> Boom -> Niel -> Puurs -> Doel -> Sinaai -> Heist -> Gits -> Bere -> Tielt -> Ghent -> Lot -> Vorst ->  Mal
```

The village of [Mal](https://nl.wikipedia.org/wiki/Mal_(Tongeren)) is chosen as a startpoint here, but the solution is a closed loop, so it doesn't matter where Mr. Gooris chooses to start.

![TSP_difference](https://github.com/Forceflow/Ambiance_TSP/blob/master/readme_img/TSP_diff.gif "Difference between original and optimized itinerary")

## *Bere or Mere? Leut or Jeuk?

* We originally interpeted the village of _Bere_ as slang for the city of [Meulebeke](https://en.wikipedia.org/wiki/Meulebeke), because the village of [Bere](https://en.wikipedia.org/wiki/Bere,_Botswana) in Botswana would be uncharacteristic. Now, several listeners have informed us that they - after careful listening of the song - don't hear _Bere_, but _Mere_, which could be slang for the city of [_Erpe-Mere_](https://en.wikipedia.org/wiki/Erpe-Mere). 
* The same goes for the part about _leuk in_, where we heard _Leut_, but several listeners informed us that _Jeuk_ is also a [village](https://nl.wikipedia.org/wiki/Jeuk_(Gingelom)), and would fit better into the rhyming scheme.

The jury's still out on which interpretation is correct, but we have included an alternative list of locations in ``ambiance_alt.csv``, and ran the solver again, resulting in the following (slightly altered) optimized path:

```
Mal -> As -> Bree -> Peer -> Geel -> Schriek -> Haacht -> Duffel -> Lint -> Reet -> Leest -> Boom -> Niel -> Puurs -> Doel -> Sinaai -> Heist -> Gits -> Tielt -> Ghent -> Mere -> Lot -> Vorst -> Jeuk ->  Mal
```

As you can see, introducing the locations of _Mere_ and _Jeuk_ to the solution changes the path slightly between Ghent and Mal.

## Extra: Let's try another song!
To put the algorithm through a more thorough test, we also tested with the song [_Vlaand'renland_](https://www.youtube.com/watch?v=Qb9bvgouEnA) by Nerdland jingle producer and well-known rockabilly [Johnny Trash](https://www.johnnytrash.be/). In this song, ca. 100 locations are mentioned. The data for this song is in ``johnny_trash.csv``. Mr. Trash does not specify any activities he undertakes at these locations, but it's safe to assume the default is ``heavy drinking``.

The script came up with the following solution:

![trash_route](https://github.com/Forceflow/Ambiance_TSP/blob/master/readme_img/trash_route.jpg "Calculated route for Johnny Trash")

## Installation
The script requires **Python 3.6** or newer and depends on the , ``csv``, ``numpy`` and ``ortools`` packages, which you can install using your favorite package manager, for example: ``pip install csv numpy ortools``.

## Visualisation
A quick and dirty Google Maps example to plot the results is included in ``src\util\plotmap.html``. You can use the command ``solve_tsp.py --gmapjs ambiance.csv``to output the result as copy-pastable JavaScript coordinates. Please note that in order to use this rudimentary visualizer, you'll have to generate and specify your Google Maps API key (see [Google Dev Console](https://console.developers.google.com)) in the source code.

## See also:
A lot of people took up the challenge to solve this TSP
 * Github user [soniCaH](https://github.com/soniCaH/Traveling-Sam-Gooris-Problem) has developed a method which uses the Google Maps API to get the actual paths, and solves the problem in Excel: [Traveling-Sam-Gooris-Problem](https://github.com/soniCaH/Traveling-Sam-Gooris-Problem).
 * Martin Fiers made nice write-up on tackling the problem using Python and genetic algorithms: [notebook](https://nbviewer.jupyter.org/gist/martinfiers/e8f3efce89e099653d87fb47a8e10b0e)
 * Koos Fransen attacked the problem using ArcGIS - [tweet link](https://twitter.com/Koos_Fransen/status/1122044998541877248)
 * Q-Music DJ Maarten Vancoillie suggested we added Sam's hometown of Brasschaat to the tour - [tweet link](https://twitter.com/Maartn/status/1119710413233561601?s=20)

