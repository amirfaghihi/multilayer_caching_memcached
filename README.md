# Multilayer Caching for Searching Service
In this project I'm trying implement a 3-layer caching system for a searching service based on elasticsearch. Aside from **Dockerfiles** and **configs**, pretty much all of the project is developed using _Python Programming Language_. 
In the following document, I'll provide information on the _project design, _caching mechanism_, _dependency management_, _containarization_ and _preparing the project for deployment_. 

## Design & architecture
The basic initial architecture of this project is as follows:

![autodraw 8_15_2022](https://user-images.githubusercontent.com/16914719/184583731-0cf789e2-bfe5-40f5-8a13-8d5fa9e42741.png)



We use three layers of cache for our service. To implement caching services, [**Memcached**](https://memcached.org/) and [**Redis**](https://redis.io/) are the most popular choices. I've chosen to use **Memcached** because although it's less feature-rich than **Redis**, it handles large amounts of data better and it's also supports multithreading. So I've considered three services in my _docker-compose.yml_ file which is located [here](https://github.com/amirfaghihi/multilayer_caching_memcached/blob/main/cacheService/deploy/docker-compose.yml). Using below commands we can setup **Memcached** services that we need:

`docker-compose up -d memcached1`

`docker-compose up -d memcached2`

`docker-compose up -d memcached3`

Now that we've set up our cache services, we need to decide what to store in these cache memories. Here, we want to keep track of the term frequencies of the searched queries. The first idea that came to mind was to store the term frequencies alongside returned values inside cache layers like this:

`{"result": <returned value>, "freq": <term frequency>}`

For our cache layers (**L1**, **L2**, **L3**), we set _TTL_ values of 1 hour, 1 day and 1 week respectively. Every time a query comes from the client we start from the first cache layer (l1) and if it misses, we go to the next cache layer, and so on. If all cache layer miss, we retreive value from our DB, which in this case could be **Elasticsearch**, or any other searchable database. 

After getting the results from DB, we should set key-value pairs in our cache services following the pattern indicated before. As for _term frequencies_ we set 1 as initial number. In case of a cache hit, we need to update the term frequencies in each layer accordingly.
For example if cache hit happens in **L1** layer, we need to increase term frequency of this key in **L2** and **L3** as well. This way every time, we have stored the key-value pairs including the search result, and term frequency of key in the past 1 hour, 1 day and 1 week. 

In order to generate a report, based on the time period, we'll chose the cache layer in retrieve data from that cache, and then filter result based on the exact time period. For example, if we want to generate report on the past 3 hours, we will use **L2** layer, or if we want the report on the past 48 hours, we'll use **L3** layer. 

The problem that I faced after implementing all this mechanism, was that it's kind of not possible to retrieve all data from cache layers with **Memcached** python client. So I had to think of another way for _report generation_. I decided to change my approach in another branch. I used a **postgres** database to save every single query from the client side with a timestamp. After that for generating reports, I would just filter the database based on the time period, and group by each query string in the database. After getting the result from postgres, using **Pandas** library we can export the result into a **csv** file. With this new approach, the caching mechanism becomes much simpler, as we don't need to store the term frequencies inside cache layers. 

Overall I would say, maybe using **Memcached** for our caching service, wasn't the best choice and maybe using **Redis** here would be better.



