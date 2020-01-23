"""Testing Python with Markdata

An example of using Markdata to extract a code snippet from within a
larger testing context (in this case, pytest).
"""


def test_yaml():
    """An example of testing a Python code example.
    """
    from ruamel.yaml import YAML

    inp = """\
    - &CENTER {x: 1, y: 2}
    - &LEFT {x: 0, y: 2}
    - &BIG {r: 10}
    - &SMALL {r: 1}
    # All the following maps are equal:
    # Explicit keys
    - x: 1
      y: 2
      r: 10
      label: center/big
    # Merge one map
    - <<: *CENTER
      r: 10
      label: center/big
    # Merge multiple maps
    - <<: [*CENTER, *BIG]
      label: center/big
    # Override
    - <<: [*BIG, *LEFT, *SMALL]
      x: 1
      label: center/big
    """

    yaml = YAML()
    data = yaml.load(inp)
    assert data[7]['y'] == 2
