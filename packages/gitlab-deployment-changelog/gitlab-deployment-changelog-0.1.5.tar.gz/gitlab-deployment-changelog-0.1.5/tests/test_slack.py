from datetime import datetime

from gitlab_deployment_changelog.gdc import slack_msg_from_deployment
from gitlab_deployment_changelog.utils.gitlab_connector import Deployment

dpl = Deployment(deployed_by="cb", deployed_at=datetime.now(), changelog=[], environment="env")


def test_slack_msg_from_dpl(mocker):
    mocker.patch("gitlab_deployment_changelog.utils.slack.send_to_slack")
    assert slack_msg_from_deployment(dpl, False)


def test_slack_noop():
    assert not slack_msg_from_deployment(dpl, True)
