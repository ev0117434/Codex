import logging

from snapshot.config_loader import load_simple_yaml
from snapshot.healthcheck import get_status
from snapshot.logging_setup import setup_logging
from snapshot.metrics import MetricsRegistry


def main() -> None:
    config = load_simple_yaml("config/config.yaml")
    setup_logging(config.get("logging", {}).get("level", "INFO"))
    logger = logging.getLogger("snapshot.service")

    metrics = MetricsRegistry()
    metrics.inc("service_starts_total")

    logger.info("Service started")
    logger.info("Health: %s", get_status())
    logger.info("Metrics: %s", metrics.snapshot())


if __name__ == "__main__":
    main()
