# Project Plan

## Summary

This projects aims to analyze daily bike traffic in relation to weather data for every given day. The bike traffic data will be provided by the city of Münster, weather data comes from Deutscher Wetterdiesnt. The goal is to analyze and interpret the impact different weather factors have on the decision making of whether to use the bike or resort other other forms of transportation.

## Rationale

The analysis will show how many people will take their bike every day vs. how many people exclusively ride when there's good weather. As a result more accurate predicions about bike traffic can be made and possibly also applied in other cities outside of Münster.

## Datasources

### Datasource1: Klimadaten und –produkte (DWD)
* Metadata URL: https://mobilithek.info/offers/-4979349128225020802
* Data URL: https://opendata.dwd.de/climate_environment/CDC/observations_germany/ {multiple files}
* Data Type: CSV

Weather data for germany. Multiple stations meassuring different kinds of weather attributes. Historical data included.

### Datasource2: Verkehrszählung Fahrradverkehr (Stadt Münster)
* Metadata URL: https://mobilithek.info/offers/-3391607290159170073
* Data URL: https://github.com/od-ms/radverkehr-zaehlstellen/tree/main/100053305/ {multiple files}
* Data Type: CSV

Bike traffic in the city of Münster. Historical data included.

## Work Packages

1. Data Aggregation Pipeline [#1][i1]
2. Automated tests [#2][i2]
3. Continuous Integration [#3][i3]
4. Data visualization [#5][i5]
5. Deployment via GitHub Pages [#4][i4]

[i1]: https://github.com/maanex/2023-amse/issues/1
[i2]: https://github.com/maanex/2023-amse/issues/2
[i3]: https://github.com/maanex/2023-amse/issues/3
[i4]: https://github.com/maanex/2023-amse/issues/5
[i5]: https://github.com/maanex/2023-amse/issues/4
