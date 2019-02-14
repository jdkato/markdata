from delegator import chain


def output(fm, **kwargs) -> str:
    """Example directive for fetching external output.
    """
    c = chain(kwargs["cmd"])
    return c.out.strip()
