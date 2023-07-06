#!/usr/bin/python3

from fabric.api import local
from datetime import datetime

def do_pack():
    """Generates a .tgz archive from the contents of the web_static folder"""

    # Create the versions folder if it doesn't exist
    local("mkdir -p versions")

    # Create the archive file name
    now = datetime.now().strftime("%Y%m%d%H%M%S")
    archive_name = "web_static_" + now + ".tgz"

    # Compress the web_static folder into the archive
    result = local("tar -czvf versions/{} web_static".format(archive_name))

    if result.failed:
        return None
    else:
        return "versions/{}".format(archive_name)
