import pytest

from connector import Connector
from exceptions import WebsiteNotFoundError, ShortestPathNotFoundError
from utils import trim_slash, get_links
from argparse import Namespace
from path import path
from network import network


def test_trim_slash():
    assert trim_slash("www.google.com/") == "www.google.com"


def test_trim_slash_none():
    assert trim_slash("www.google.com") == "www.google.com"


def test_get_links():
    """test if it reads link from page"""
    links = get_links("http://www.stealthboats.com/")
    assert len(links) == 1 and links[0]['href'] == "http://www.pointlesssites.com/"


def test_connector_execute():
    """test execute queries with database"""
    conn = Connector()
    conn.execute("CREATE (n: Person {name: 'Andy'})")
    res = conn.execute_and_fetch("MATCH (n: Person) WHERE n.name = 'Andy' RETURN n.name")
    assert res.__next__()['n.name'] == 'Andy'
    conn.execute("MATCH(n) DETACH DELETE n")


def test_connector_execute_and_fetch():
    """test execute_and_fetch with database"""
    conn = Connector()
    res = conn.execute_and_fetch("CREATE (n: Person {name: 'Bruno'}) RETURN n.name")
    assert res.__next__()['n.name'] == 'Bruno'
    conn.execute("MATCH(n) DETACH DELETE n")


def test_path(capfd):
    """create connected nodes first->second->third with bypass second->offroute->third, check shortest path"""
    conn = Connector()
    conn.execute(
        """
        CREATE (f: Website {address: 'www.first.com'})
        CREATE(f)-[r1: Link]->(s: Website {address: 'www.second.com'})
        SET r1.weight = 1
        CREATE(s)-[r2: Link]->(t: Website {address: 'www.third.com'})
        SET r2.weight = 1
        CREATE(s)-[r3: Link]->(o: Website {address: 'www.offroute.com'})
        SET r3.weight = 1
        CREATE(o)-[r4: Link]->(t)
        SET r4.weight = 1
        """
    )

    args = Namespace(START_URL="www.first.com", END_URL="www.third.com")
    path(args, conn)
    out, err = capfd.readouterr()
    assert out == "Shortest Path: 2 clicks\n" \
                  "0 - www.first.com\n" \
                  "1 - www.second.com\n" \
                  "2 - www.third.com\n"

    conn.execute("MATCH(n) DETACH DELETE n")


def test_path_not_in_database():
    """test raising WebsiteNotFoundError when URL is not in database"""
    conn = Connector()
    args = Namespace(START_URL="https://www.Andy.com", END_URL="https://www.Bruno.com")
    with pytest.raises(WebsiteNotFoundError) as execinfo:
        path(args, conn)
    assert execinfo.value.args[0] == "Website not found: https://www.Andy.com"

    conn.execute("MATCH(n) DETACH DELETE n")


def test_path_no_path():
    """test raising ShortestPathNotFoundError when no path is found"""
    conn = Connector()
    conn.execute(
        """
        CREATE (f: Website {address: 'www.first.com'})
        CREATE(f)-[r1: Link]->(s: Website {address: 'www.second.com'})
        SET r1.weight = 1
        CREATE(s)-[r2: Link]->(t: Website {address: 'www.third.com'})
        SET r2.weight = 1
        CREATE(s)-[r3: Link]->(o: Website {address: 'www.offroute.com'})
        SET r3.weight = 1
        CREATE(o)-[r4: Link]->(t)
        SET r4.weight = 1
        """
    )

    args = Namespace(START_URL="www.third.com", END_URL="www.first.com")
    with pytest.raises(ShortestPathNotFoundError) as execinfo:
        path(args, conn)
    assert execinfo.value.args[0] == "Shortest path not found!"

    conn.execute("MATCH(n) DETACH DELETE n")


def test_network():
    """test if network finds all nodes"""
    conn = Connector()
    args = Namespace(START_URL="https://zvonimir.info", depth=1)
    network(args, conn)

    res = conn.execute_and_fetch(
        """
        MATCH (n)
        RETURN count(n) as count
        """
    )
    assert res.__next__()['count'] == 14

    conn.execute("MATCH(n) DETACH DELETE n")


def test_network_url_doesnt_exist():
    """test raising WebsiteNotFoundError if URL does not exist"""
    conn = Connector()
    args = Namespace(START_URL="https://nemazvonimira.info", depth=1)
    with pytest.raises(WebsiteNotFoundError) as execinfo:
        network(args, conn)
    assert execinfo.value.args[0] == "Website not found: https://nemazvonimira.info"


def test_network_and_path(capfd):
    """integration test of network and path"""
    conn = Connector()
    args = Namespace(START_URL="http://www.stealthboats.com/", depth=2)
    network(args, conn)

    args = Namespace(START_URL="http://www.stealthboats.com/", END_URL="https://www.dramabutton.com")
    path(args, conn)

    out, err = capfd.readouterr()
    assert out == "Shortest Path: 2 clicks\n" \
                  "0 - http://www.stealthboats.com\n" \
                  "1 - http://www.pointlesssites.com\n" \
                  "2 - https://www.dramabutton.com\n"

    conn.execute("MATCH(n) DETACH DELETE n")


if __name__ == "__main__":
    test_path_not_in_database()