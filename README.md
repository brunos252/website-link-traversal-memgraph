## Website link traversal

Script for scraping static websites for links, using BFS search algorithm for graph traversal and Memgraph database for link storage and representation. Memgraph is also used to find the shortest path between website nodes present in the database after web traversal.

## Installation
Docker and a running instance of Memgraph is needed to run the script. 
To download and run Memgraph:
```
docker pull memgraph/memgraph-platform
docker run -it -p 7687:7687 -p 3000:3000 memgraph/memgraph-platform
```
To easily install required packages:
```
pip3 install -r requirements.txt
```

## Usage
Get all website page links from starting website START_URL with a max depth of DEPTH:
```
python main.py network START_URL [--depth | -d DEPTH]
```
Find the shortest path from START_URL to END_URL from a scraped network of websites in the Memgraph database:
```
python main.py path START_URL END_URL
```
