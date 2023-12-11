import argparse
import sys

from loguru import logger

from .utils.gitlab_connector import GitlabConnector, Deployment
from .utils.slack import send_to_slack

BUG_LABEL = "type::bug"
ICON_MR = ":gear:"
ICON_BUGFIX = ":negative_squared_cross_mark:"
ICON_FEATURE = ":star2:"


def _get_emoji_from_issue(changelog_entry) -> str:
    if not changelog_entry.issue_iid:
        # MR
        return ICON_MR
    if BUG_LABEL in changelog_entry.issue_labels:
        return ICON_BUGFIX
    return ICON_FEATURE


def slack_msg_from_deployment(dpl: Deployment, noop: bool) -> bool:
    msg = f":tada: New Deployment to *{dpl.environment}*, deployed at {dpl.deployed_at} by {dpl.deployed_by}.\n"

    for changelog_entry in dpl.changelog:
        emoji = _get_emoji_from_issue(changelog_entry)
        msg += f"{emoji}<{changelog_entry.url}|*{changelog_entry.get_title()}*> by {changelog_entry.author}\n"
    msg += f"\nLegend: {ICON_MR} Merge request w/o issues; {ICON_BUGFIX} bugfix; "
    msg += f"{ICON_FEATURE} new feature or improvement"

    logger.debug(msg)
    if not noop:
        send_to_slack(msg)
        return True
    else:
        logger.info("Nothing sent to Slack.")
        return False


def main():
    parser = argparse.ArgumentParser(prog="Gitlab Deployment Changelog")
    parser.add_argument("env", help="Name of the environment", default="production/the_exb")
    parser.add_argument("-c", "--count", help="How many last deployments to consider", default=1, type=int)
    parser.add_argument("-n", "--no_slack", help="Don't send to slack", action='store_true', default=False)
    parser.add_argument("-d", "--debug", help="Show debug output", action='store_true', default=False)
    args = parser.parse_args()

    if not args.debug:
        logger.remove()
        logger.add(sys.stdout, level="INFO")

    gc = GitlabConnector.factory()
    deployments = gc.get_changelog(environment=args.env, deployments_count=args.count)

    for d in deployments:
        slack_msg_from_deployment(d, noop=args.no_slack)


if __name__ == '__main__':
    main()
