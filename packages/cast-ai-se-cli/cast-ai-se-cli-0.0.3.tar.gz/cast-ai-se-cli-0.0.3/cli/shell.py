"""
se-cli: The swiss army command-line for Cast.AI SE`s.

Usage:
    se-cli demo <on|off|refresh> [--cluster_id <cluster_id>] [-h|--help] [-d|--debug]
    se-cli snapshot <analyze> [--cluster_id <cluster_id>] [-h|--help] [-d|--debug]

Options:
    -h, --help  Show this help message and exit.
    -d, --debug  Enable debug logging.
    -c, --cluster_id <cluster_id>  (Optional) Specify the cluster ID for the demo environment.

Commands:
    demo      Manage the demo environment.
    snapshot  Manage snapshots.

Subcommands for "demo":
    on   Prep demo environment for demo.
    off  Hibernate demo environment.
"""
import sys

from orchestrators.demo_orch import DemoOrchestrator
from orchestrators.snapshot_orch import SnapshotOrchestrator
from services.misc_svc import init

from docopt import docopt


commands_table = {
    "demo": DemoOrchestrator,
    "snapshot": SnapshotOrchestrator
}

if __name__ == '__main__':
    try:
        # TODO: check version once pypi is up
        parsed_options = docopt(__doc__, sys.argv[1:])
        cfg = init(parsed_options)
        orchestrator_class = commands_table[cfg.app_inputs["command"]]
        main_orch = orchestrator_class(cfg)
        main_orch.execute()
    except Exception as e:
        print(f"An error occurred: {e}")
