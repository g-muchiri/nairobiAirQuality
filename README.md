### Nairobi Air Quality Data Platform
The project is one that fetches data from OpenAQ API, transforms it through a series of steps and finally loads it into postgresql for processing

#### Understanding the data source and jargon used in the API

1. What is a location

    A location is a physical or virtual tracking station.

2. What is a Sensor
    A sensor is an instrument that measures a specific element of pollution

3. What is a measurement

    A measurement is an actual recorded value that is immutable

4. What pollutants are there

    O3, CO, NO2, SO2, PM25, PM10

5. How is Measurement time represented

    The measurement end point in results has a datetime dictionary which gives time in local time/UTC

6. What units are used

    milligram/meter3
    ppb

7. How does pagination work

    A page could have many incoming records when traversing large endpoints such as OpenAQ. Two parameters should be passed  `limit = 100` and `page = 1`
8. What happens if an invalid API key is keyed in and what is the status code raised

    In the event one keys ina a wrong API KEY, an `AuthenicationError` is raised. If  there is no API KEY then `MissingAPIKeyError` is thrown and the status code thrown take the form 401. Unauthorised. 

### The next order of business will be extraction of data from the API, loading and designing a dynamic Task Mapping in Airflow

#### Extraction
We will be extracting the following
1. Sensors from the location
2. Measurements from the sensors and storing them away in a database