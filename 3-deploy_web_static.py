#!/usr/bin/python3

from fabric.api import env, put, run
from datetime import datetime
import os

# Update the Fabric environment with your web server IPs
env.hosts = ['<IP web-01>', '<IP web-02>']
env.user = '<your-username>'
env.key_filename = '<path-to-ssh-key>'

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


def do_deploy(archive_path):
    """Distributes an archive to the web servers"""

    # Check if the archive file exists
    if not os.path.exists(archive_path):
        return False

    try:
        # Upload the archive to /tmp/ directory on the web server
        put(archive_path, "/tmp/")

        # Extract the archive to the web server's releases directory
        archive_filename = os.path.basename(archive_path)
        archive_folder = "/data/web_static/releases/{}".format(
            archive_filename.split(".")[0]
        )
        run("mkdir -p {}".format(archive_folder))
        run("tar -xzf /tmp/{} -C {}".format(archive_filename, archive_folder))

        # Delete the archive file from the web server
        run("rm /tmp/{}".format(archive_filename))

        # Move the contents of the extracted folder to the web server's web_static directory
        extracted_folder = "{}/web_static".format(archive_folder)
        run("mv {}/web_static/* {}".format(extracted_folder, archive_folder))

        # Delete the extracted folder
        run("rm -rf {}".format(extracted_folder))

        # Delete the existing symbolic link
        run("rm -rf /data/web_static/current")

        # Create a new symbolic link
        run("ln -s {} /data/web_static/current".format(archive_folder))

        return True

    except Exception as e:
        print(str(e))
        return False


def deploy():
    """Create and distribute an archive to the web servers"""

    # Create the archive
    archive_path = do_pack()

    # Return False if no archive has been created
    if not archive_path:
        return False

    # Deploy the archive to the web servers
    return do_deploy(archive_path)
