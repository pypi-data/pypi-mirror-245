import time
from pydantic import validator
from typing import List, Any

from spotON_sdk.Logic.Price.markets import Market

from .customBaseModel import CustomBaseModel


class Timeframe(CustomBaseModel):
    start: int = -2
    end: int = 22

    @validator('*')
    def validate_hours(cls, value):
        if not -1 <= value <= 22:
            raise ValueError("hours should be in range -1, 22")
        return value
    
    @property
    def length(self) -> int:
        return self.end - self.start + 1
    
    @property
    def hours(self) -> List[int]:
        return list(range(self.start, self.end + 1))
    
class Local_Timeframe(Timeframe):

    def __init__(self, start: int, end: int, market: Market):
        utc_offset = market.area.calculate_utc_offset()
        start -= utc_offset
        end -= utc_offset
        super().__init__(start=start, end=end)



def hours_to_timeframes(hours_list: List[int]) -> List[Timeframe]:

    timeframes : List[Timeframe] = []
    hours_list = sorted(set(hours_list))  # Ensure hours are unique and sorted

    start = None
    prev_hour = None

    print(f"{hours_list=}")

    for index,hour in enumerate(hours_list):
        if start is None:
            start = hour  # Start of a new timeframe
            
        
        try:
            next_hour = hours_list[index+1]
        except IndexError:
            next_hour = None

        if hour +1 != next_hour: # It' the last hour in the list
            # If there's a gap, we end the current timeframe and start a new one
            timeframes.append(Timeframe(start=start, end=hour))
            start = None
        

    if start is not None and prev_hour is not None:
        # Close the last timeframe
        timeframes.append(Timeframe(start=start, end=prev_hour))


    
    return timeframes
def hours_to_timeframes_OLD(hours_list: List[int]) -> List[Timeframe]:

    timeframes : List[Timeframe] = []
    hours_list = sorted(set(hours_list))  # Ensure hours are unique and sorted

    start = None
    prev_hour = None

    for hour in hours_list:
        if start is None:
            start = hour  # Start of a new timeframe
        elif prev_hour is not None and hour != prev_hour + 1:
            # If there's a gap, we end the current timeframe and start a new one
            timeframes.append(Timeframe(start=hour, end=hour))
            start = hour
        prev_hour = hour

    if start is not None and prev_hour is not None:
        # Close the last timeframe
        timeframes.append(Timeframe(start=start, end=prev_hour))


    
    return timeframes


