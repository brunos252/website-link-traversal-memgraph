import urllib.request
from exceptions import WebsiteNotFoundError
from utils import trim_slash, get_links


def network(args, connector):
    """BFS search through websites from START_URL, adds them to database"""
    start = trim_slash(args.START_URL)
    connector.execute(
        "MERGE (:Website {address: '" + start + "'})"
    )

    queue = [(start, 0)]
    visited = set()

    while len(queue) > 0:
        node = queue.pop(0)
        if node[1] >= args.depth:
            break
        if node[0] in visited:
            continue

        # scrape the current website (node)
        try:
            adjacent = get_links(node[0])
        except urllib.error.HTTPError as exception:
            # print(exception)
            continue
        except urllib.error.URLError:
            if node[0] == start:
                raise WebsiteNotFoundError(node[0])
            else:
                continue

        for element in adjacent:
            link = element['href']
            # check if link is valid
            if link[0:4] != "http":
                if len(link) > 0 and link[0] == '/':
                    link = node[0] + link
                else:
                    continue

            link = trim_slash(link)

            # add link to queue to be visited, along with depth
            queue.append((link, node[1] + 1))

            # create node corresponding to linked website, IF it doesn't already exist
            connector.execute(
                "MERGE (:Website {address: '" + link + "'})"
            )

            # create relationship between current and linked website
            connector.execute(
                """
                MATCH (l1:Website), (l2:Website)
                WHERE l1.address = '{add1}' AND l2.address = '{add2}'
                CREATE (l1)-[r:Link]->(l2)
                SET r.weight = 1
                RETURN r
                """.format(add1=node[0], add2=link)
            )

        visited.add(node[0])
