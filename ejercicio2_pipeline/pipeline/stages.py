from datetime import timedelta
from typing import Generator, Dict, Any, List

def filter_stage(
    stream: Generator[Dict[str, Any], None, None], 
    target_type: str = "heartbeat"
) -> Generator[Dict[str, Any], None, None]:
    for event in stream:
        if event["event_type"] != target_type:
            yield event


def transform_stage(
    stream: Generator[Dict[str, Any], None, None]
) -> Generator[Dict[str, Any], None, None]:

    for event in stream:

        event["value"] = round(event["value"] * 1.19, 2)
        event["metadata"]["processed"] = True
        event["metadata"]["processed_by"] = "senior_pipeline_v1"
        yield event


def window_aggregation_stage(
    stream: Generator[Dict[str, Any], None, None], 
    window_minutes: int = 5
) -> Generator[List[Dict[str, Any]], None, None]:

    current_window_events = []
    window_start_time = None
    window_duration = timedelta(minutes=window_minutes)

    for event in stream:
        event_time = event["timestamp"]

        if window_start_time is None:
            window_start_time = event_time

        if event_time < window_start_time + window_duration:
            current_window_events.append(event)
        else:
            if current_window_events:
                yield current_window_events

            while event_time >= window_start_time + window_duration:
                window_start_time += window_duration

            current_window_events = [event]

    if current_window_events:
        yield current_window_events