import base64
import subprocess
import tempfile


def ditaa(fm, path, alt=""):
    """Example directive for including an exteranlly-generated image.
    """
    if alt:
        alt = 'alt="{0}"'.format(alt)

    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp:
        subprocess.call(["ditaa", path, temp.name], stdout=subprocess.PIPE)
        data = base64.b64encode(temp.read()).decode()

    return '<img src="data:image/png;base64,{0}" {1}>'.format(data, alt)
