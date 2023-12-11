CPU_TIME_RE = r'^(?:(?P<days>\d+)-)?(?P<hours>\d+):(?P<minutes>\d+):(?P<seconds>\d+)$'


class MemoryUsed:
    def __init__(self, value: str) -> None:
        self.value: int | None = None
        if value.endswith('K'):
            self.value = int(value[:-1]) // 1024
            return

        if value.endswith('M'):
            self.value = int(value[:-1])
            return

        if value.endswith('G'):
            self.value = int(value[:-1]) * 1024
            return

        try:
            self.value = int(value) // (1024 * 1204)
        except ValueError:
            self.value = None

    def __str__(self) -> str:
        return f'{self.GB}GB'

    def __repr__(self) -> str:
        return f'{self.GB}GB'

    @property
    def MB(self) -> int:  # pylint: disable=invalid-name
        if self.value is None:
            raise RuntimeError('Value not set.')
        return self.value

    @property
    def GB(self) -> int:  # pylint: disable=invalid-name
        if self.value is None:
            raise RuntimeError('Value not set.')
        return self.value // 1024
