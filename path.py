from exceptions import ShortestPathNotFoundError, WebsiteNotFoundError
from utils import trim_slash


def path(args, connector):
    """path query, calculates and displays the shortest path between websites in Memgraph database"""

    start = trim_slash(args.START_URL)
    end = trim_slash(args.END_URL)

    """check if START_URL and END_URL exist in database"""
    start_db = connector.execute_and_fetch("MATCH (n: Website) WHERE n.address = '" + start + "' RETURN n")
    end_db = connector.execute_and_fetch("MATCH (n: Website) WHERE n.address = '" + end + "' RETURN n")
    if not any(start_db):
        raise WebsiteNotFoundError(start)
    if not any(end_db):
        raise WebsiteNotFoundError(end)

    """use Memgraph to calculate shortest path"""
    results = connector.execute_and_fetch(
        "MATCH p = (:Website {address: '" + start +
        "'})-[:Link * wShortest (e, v | e.weight) total_weight]->(:Website {address: '" + end +
        "'}) RETURN nodes(p) AS websites, total_weight;")

    for result in results:
        print("Shortest Path: " + str(len(result['websites']) - 1) + " clicks")
        for count, node in enumerate(result['websites']):
            print(count, "-", node.properties['address'])
        break
    else:
        raise ShortestPathNotFoundError
