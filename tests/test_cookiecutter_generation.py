import os
import re
import sh

import pytest
from binaryornot.check import is_binary

PATTERN = '{{(\s?cookiecutter)[.](.*?)}}'
RE_OBJ = re.compile(PATTERN)


@pytest.fixture
def context():

    return {
        'project_name': 'iibold',
        'project_slug': 'my_test_project',
        'author_name': 'Test Author',
        'email': 'test@example.com',
        'description': 'A short description of the project.',
        'domain_name': 'iibold.com',
        "application_name": "iibold",
        "application_slug": "iibold",
        "application_user": "hack",
        "application_root": "/hack/iibold",
        "staging_server_domain": "staging.iibold.com",
        "production_server_domain": "iibold.com",
        "add_your_public_key": "y",
        "add_letsencrypt_certificate": "n",
        "letsencrypt_email": "support@production_server_domain",
        "project_git_remote": "git@github.com:iibold/cookiecutter-django-ansible.git",
        "author_name": "cason wang",
        "domain_name": "iibold.com",
        "version": "0.1.0",
        "timezone": "Asia/Shanghai",
        "use_whitenoise": "n",
        "use_celery": "n",
        "use_mailhog": "y",
        "use_sentry_for_error_reporting": "y",
        "use_opbeat": "n",
        "use_pycharm": "n",
        "private_network": "192.168.13.38",
        "windows": "n",
        "use_docker": "n",
        "use_heroku": "n",
        "use_elasticbeanstalk_experimental": "n",
        "use_compressor": "n",
        "postgresql_version": "9.6",
        "js_task_runner": "Gulp",
        "custom_bootstrap_compilation": "n",
        "open_source_license": "Not open source"
    }



def build_files_list(root_dir):
    """Build a list containing absolute paths to the generated files."""
    return [
        os.path.join(dirpath, file_path)
        for dirpath, subdirs, files in os.walk(root_dir)
        for file_path in files
    ]


def check_paths(paths):
    """Method to check all paths have correct substitutions,
    used by other tests cases
    """
    # Assert that no match is found in any of the files
    for path in paths:
        if is_binary(path):
            continue
        for line in open(path, 'r'):
            match = RE_OBJ.search(line)
            msg = 'cookiecutter variable not replaced in {}'
            assert match is None, msg.format(path)


def test_default_configuration(cookies, context):
    result = cookies.bake(extra_context=context)
    assert result.exit_code == 0
    assert result.exception is None
    assert result.project.basename == context['project_slug']
    assert result.project.isdir()

    paths = build_files_list(str(result.project))
    assert paths
    check_paths(paths)


@pytest.fixture(params=['use_mailhog', 'use_celery', 'windows'])
def feature_context(request, context):
    context.update({request.param: 'y'})
    return context


def test_enabled_features(cookies, feature_context):
    result = cookies.bake(extra_context=feature_context)
    assert result.exit_code == 0
    assert result.exception is None
    assert result.project.basename == feature_context['project_slug']
    assert result.project.isdir()

    paths = build_files_list(str(result.project))
    assert paths
    check_paths(paths)


def test_flake8_compliance(cookies):
    """generated project should pass flake8"""
    result = cookies.bake()

    try:
        sh.flake8(str(result.project))
    except sh.ErrorReturnCode as e:
        pytest.fail(e)
