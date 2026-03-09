from dataclasses import dataclass, field


@dataclass
class MetricsRegistry:
    counters: dict[str, int] = field(default_factory=dict)

    def inc(self, name: str, value: int = 1) -> None:
        self.counters[name] = self.counters.get(name, 0) + value

    def snapshot(self) -> dict[str, int]:
        return dict(self.counters)
