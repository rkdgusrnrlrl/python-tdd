from fabric.contrib.files import append, exists, sed
from fabric.api import env,local,run
import random

REPO_URL = 'https://github.com/rkdgusrnrlrl/python-tdd.git'


def _create_directory_structure_if_necessary(site_folder):
    for subfolder in ('database', 'static', 'virtualenv', 'source'):
        run('mkdir -p %s%s' % (site_folder, subfolder))


def _get_lastest_source(site_folder):
    if exists(site_folder+'/.git'):
        run('cd %s && git fetch ' % (site_folder,))
    else:
        run('git clone %s %s' % (REPO_URL, site_folder))

    # local 로컬 장비에서 실행 subprocess.Popen 을 렙핑됨
    current_commit = local("git log -n 1 --format=%H", capture=True)
    run('cd %s && git reset --hard %s ' % (site_folder, current_commit))

def _update_settings(source_folder):
     setting_path = source_folder + '/superlists/setting.py'
     sed(setting_path, 'DEBUG = True', 'DEBUG = True')
     sed(setting_path, 'ALLOWED_HOSTS =.+$', 'ALLOWED_HOSTS = ["%s"]' % ('http://rkdgusrnrlrl.vps.phps.kr'))
     secret_key_file = source_folder + '/superlists/secret_key.py'
     if not exists(secret_key_file):
         chars = 'rkaskdjgoashidgioasdjkfnqwkjenfkajsbdhjlfqwejnflkasdjbfkjqwhe'
         key = ''.join(random.SystemRandom.choice(chars) for _ in range(50))
         append(secret_key_file, "SECRET_KEY = '%s'" % (key,))
     append(setting_path, '\nform .secret_key import SECRET_KEY')



def _update_virtualenv(source_folder):
    virtual_folder = source_folder + '/../virtualenv'
    if not exists(virtual_folder + '/bin/pip'):
        run('virtualenv --python==python3.4 %s' % (virtual_folder,))
    run('%s/bin/pip install -r %s requirement.txt' % (virtual_folder, source_folder))


def _update_static_file(source_folder):
    run('cd %s && ../virtualenv/bin/python manage.py collectstatic --noinput' % (source_folder))

def _update_database(source_folder):
    run('cd %s && ../virtualenv/bin/python manage.py migrate --noinput' % (source_folder))

def deploy():
    site_folder = '/home/%s/docker/py_tdd' % env.user
    source_folder = site_folder + '/source'
    _create_directory_structure_if_necessary(site_folder)
    _get_lastest_source(site_folder)
    _update_virtualenv(source_folder)
    _update_static_file(source_folder)
    _update_database(source_folder)
