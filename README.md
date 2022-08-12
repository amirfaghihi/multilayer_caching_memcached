# multilayer_caching_memcached
In this project I'm trying implement a 3-layer caching system for a searching service based on elasticsearch. Aside from **Dockerfiles** and **configs**, pretty much all of the project is developed using _Python Programming Language_. 
In the following document, I'll provide information on the _project architecture_, _caching mechanism_, _dependency management_, _containarization_ and _preparing the project for deployment_. 

Basically, we use three layers of cache for our service. To implement caching services, [**Memcached**](https://memcached.org/) and [**Redis**](https://redis.io/) are the most popular choices. I've chosen to use **Memcached** because although it's less feature-rich than **Redis**, it handles large amounts of data better. So I've considered three services in my _docker-compose.yml_ file which is located [here](https://github.com/amirfaghihi/multilayer_caching_memcached/blob/main/cacheService/deploy/docker-compose.yml). Using below commands we can setup **Memcached** services that we need:

`docker-compose up -d memcached1`

`docker-compose up -d memcached2`

`docker-compose up -d memcached3`

Now that we've set up our cache services, we need to decide what to store in these cache memories. Here, we want to keep track of the term frequencies of the searched queries. 



