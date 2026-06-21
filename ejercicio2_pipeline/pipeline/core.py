from functools import reduce
from typing import Generator, List, Callable, Any

class DeclarativePipeline:


    def __init__(self, stages: List[Callable[[Generator], Generator]]):

        self.stages = stages

    def execute(self, source_stream: Generator[Any, None, None]) -> Generator[Any, None, None]:

        if not self.stages:
            return source_stream
        composed_pipeline = reduce(
            lambda stream_acumulado, stage: stage(stream_acumulado),
            self.stages,
            source_stream
        )
        
        return composed_pipeline