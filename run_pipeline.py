"""Pipeline runner - orchestrates execution of pipeline steps.

Usage:
    python run_pipeline.py --all
    python run_pipeline.py --steps ingestion sentiment
    python run_pipeline.py --steps forecasting --dry-run
"""

import argparse
import logging
import logging.config
from pathlib import Path

import yaml

from services.backtesting import runner as backtesting_runner
from services.forecasting import runner as forecasting_runner
from services.ingestion import runner as ingestion_runner
from services.sentiment import runner as sentiment_runner

PIPELINE_STEPS = {
    "ingestion": ingestion_runner,
    "sentiment": sentiment_runner,
    "forecasting": forecasting_runner,
    "backtesting": backtesting_runner,
}

DEFAULT_STEP_ORDER = ["ingestion", "sentiment", "forecasting", "backtesting"]


def setup_logging() -> None:
    """Configure logging from configs/logging.yaml."""
    config_path = Path("configs/logging.yaml")
    with open(config_path) as f:
        config = yaml.safe_load(f)
    logging.config.dictConfig(config)


def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments.

    Returns:
        Parsed arguments namespace.
    """
    parser = argparse.ArgumentParser(
        description="Run financial research platform pipeline steps",
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--all",
        action="store_true",
        help="Run all pipeline steps in default order",
    )

    group.add_argument(
        "--steps",
        nargs="+",
        choices=list(PIPELINE_STEPS.keys()),
        help="Run specific pipeline steps",
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be executed without running",
    )

    return parser.parse_args()


def run_step(step_name: str, dry_run: bool = False) -> None:
    """Run a single pipeline step.

    Args:
        step_name: Name of the step to run.
        dry_run: If True, only log what would be executed.
    """
    logger = logging.getLogger(__name__)

    if dry_run:
        logger.info(f"[DRY RUN] Would execute step: {step_name}")
        return

    logger.info(f"Executing step: {step_name}")
    runner_module = PIPELINE_STEPS[step_name]
    runner_module.run()
    logger.info(f"Completed step: {step_name}")


def main():
    """Pipeline runner entry point.

    Returns:
        Exit code: 0 for success, 1 for failure.
    """
    setup_logging()
    logger = logging.getLogger(__name__)

    args = parse_arguments()
    steps_to_run = DEFAULT_STEP_ORDER if args.all else args.steps
    logger.info(f"Pipeline starting with steps: {steps_to_run}")
    if args.dry_run:
        logger.info("Running in DRY RUN mode")

    for step in steps_to_run:
        try:
            run_step(step, dry_run=args.dry_run)
        except NotImplementedError as e:
            logger.warning(f"Step '{step}' is not implemented: {e}")
            continue
        except Exception as e:
            logger.error(f"Step '{step}' failed: {e}", exc_info=True)
            return 1

    logger.info("Pipeline completed successfully")
    return 0


if __name__ == "__main__":
    exit(main())
