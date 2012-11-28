from django.conf import settings
from dajaxice.decorators import dajaxice_register
from django.utils import simplejson
import datetime
import os
import yaml
from prerelease_website.rosinstall_gen.distro import generate_rosinstall
from prerelease_website.rosinstall_gen.old_distro import generate_dry_rosinstall

import logging
logger = logging.getLogger('submit_jobs')

@dajaxice_register
def get_rosinstall_ajax(request, distro, packages, dry):
    logger.info("Got distro %s, packages %s, dry %s" % (distro, packages, dry))
    timestr = datetime.datetime.now().strftime("%Y%m%d-%H%M%S%f")
    filename = '%s.rosinstall' % '_'.join(packages)
    relative_dir = os.path.join('rosinstalls', timestr)
    path = os.path.join(settings.MEDIA_ROOT, relative_dir, filename)
    logger.info("Writing rosinstall file to %s" % path)
    try:
        os.makedirs(os.path.realpath(os.path.dirname(path)))
    except:
        pass

    if dry:
        logger.info("Calling dry")
        rosinstall = generate_dry_rosinstall(distro, packages[0])
    else:
        logger.info("Calling wet")
        rosinstall = generate_rosinstall(distro, packages)

    with open(path, 'w+') as f:
        f.write(rosinstall)
        #yaml.dump(rosinstall, f, default_flow_style=False)

    return simplejson.dumps({'rosinstall_url': os.path.join(relative_dir,
                                                            filename)})