import pytest
import json

from server import Server, Inventory
from database import Database


# --------------------------------------------------
# Helper function
# --------------------------------------------------

def create_server():
    return Server(
        "web01",
        "192.168.1.10",
        "Linux",
        64,
        8,
        500,
        "Coimbatore",
        "Online"
    )


# --------------------------------------------------
# Fixture
# --------------------------------------------------

@pytest.fixture
def inventory(tmp_path, monkeypatch):
    # Run each test inside a temporary directory
    # so the real inventory.db is not modified.
    monkeypatch.chdir(tmp_path)

    inv = Inventory()

    yield inv

    inv.db.close()


# ==================================================
# SERVER CLASS TESTS
# ==================================================

def test_server_creation():
    s = create_server()

    assert s.host == "web01"
    assert s.ip == "192.168.1.10"
    assert s.os == "Linux"
    assert s.cpu == 64
    assert s.ram == 8
    assert s.disk == 500
    assert s.loc == "Coimbatore"
    assert s.stat == "Online"


def test_server_string():
    s = create_server()

    result = str(s)

    assert "web01" in result
    assert "192.168.1.10" in result
    assert "Linux" in result
    assert "Online" in result


# ==================================================
# INVENTORY TESTS
# ==================================================

def test_add(inventory):

    s = create_server()

    inventory.add(s)

    assert len(inventory.ser) == 1
    assert inventory.ser[0].host == "web01"


def test_checkhost(inventory):

    s = create_server()

    inventory.add(s)

    assert inventory.checkhost("web01") is True
    assert inventory.checkhost("web02") is False


def test_search(inventory, capsys):

    s = create_server()

    inventory.add(s)

    inventory.search("web01")

    output = capsys.readouterr().out

    assert "server found" in output
    assert "web01" in output


def test_search_not_found(inventory, capsys):
    s = create_server()

    inventory.add(s)

    inventory.search("web99")

    output = capsys.readouterr().out

    assert "Server Not Found" in output


def test_update(inventory):

    s = create_server()

    inventory.add(s)

    inventory.update("web01", "web02")

    assert inventory.ser[0].host == "web02"


def test_switch_status(inventory):

    s = create_server()

    inventory.add(s)

    inventory.switchstats("web01")

    assert inventory.ser[0].stat == "Offline"

    inventory.switchstats("web01")

    assert inventory.ser[0].stat == "Online"


def test_delete(inventory):

    s = create_server()

    inventory.add(s)

    assert len(inventory.ser) == 1

    inventory.delete("web01")

    assert len(inventory.ser) == 0


def test_report(inventory):

    s1 = create_server()

    s2 = Server(
        "win01",
        "192.168.1.20",
        "Windows",
        32,
        16,
        1000,
        "Coimbatore",
        "Offline"
    )

    inventory.add(s1)
    inventory.add(s2)

    report = inventory.report()

    assert "Total Servers:2" in report
    assert "Linux Servers: 1" in report
    assert "Windows Servers: 1" in report
    assert "Online Servers:1" in report
    assert "Offline Servers:1" in report


# ==================================================
# DATABASE TESTS
# ==================================================

@pytest.fixture
def database(tmp_path, monkeypatch):

    monkeypatch.chdir(tmp_path)

    db = Database()

    yield db

    db.close()


def test_database_add(database):

    s = create_server()

    database.addserver(s)

    rows = database.getallserver()

    assert len(rows) == 1
    assert rows[0][0] == "web01"


def test_database_search(database):

    s = create_server()

    database.addserver(s)

    result = database.searchserver("web01")

    assert result is not None
    assert result[0] == "web01"


def test_database_search_not_found(database):

    result = database.searchserver("web99")

    assert result is None


def test_database_update(database):

    s = create_server()

    database.addserver(s)

    database.updateserver("web01", "web02")

    result = database.searchserver("web02")

    assert result is not None
    assert result[0] == "web02"


def test_database_switch_status(database):

    s = create_server()

    database.addserver(s)

    database.switchstat("web01")

    result = database.searchserver("web01")

    assert result[7] == "Offline"

    database.switchstat("web01")

    result = database.searchserver("web01")

    assert result[7] == "Online"


def test_database_delete(database):

    s = create_server()

    database.addserver(s)

    database.deleteserver("web01")

    result = database.searchserver("web01")

    assert result is None


# ==================================================
# JSON TESTS
# ==================================================

def test_export_json(inventory):

    s = create_server()

    inventory.add(s)

    inventory.exportjson()

    with open("server.json", "r") as f:
        data = json.load(f)

    assert len(data) == 1
    assert data[0]["hostname: "] == "web01"
    assert data[0]["IP: "] == "192.168.1.10"
    assert data[0]["OS: "] == "Linux"


def test_import_json(inventory):

    data = [
        {
            "hostname: ": "web02",
            "IP: ": "192.168.1.20",
            "OS: ": "Linux",
            "CPU: ": 64,
            "RAM: ": 16,
            "Disk: ": 500,
            "Location: ": "Coimbatore",
            "Status: ": "Online"
        }
    ]

    with open("server.json", "w") as f:
        json.dump(data, f)

    inventory.importjson()

    assert len(inventory.ser) == 1
    assert inventory.ser[0].host == "web02"
    assert inventory.ser[0].ram == 16


def test_import_duplicate(inventory, capsys):

    s = create_server()

    inventory.add(s)

    data = [
        {
            "hostname: ": "web01",
            "IP: ": "192.168.1.10",
            "OS: ": "Linux",
            "CPU: ": 64,
            "RAM: ": 8,
            "Disk: ": 500,
            "Location: ": "Coimbatore",
            "Status: ": "Online"
        }
    ]

    with open("server.json", "w") as f:
        json.dump(data, f)

    inventory.importjson()

    output = capsys.readouterr().out

    assert "web01 already exists" in output
    assert len(inventory.ser) == 1
