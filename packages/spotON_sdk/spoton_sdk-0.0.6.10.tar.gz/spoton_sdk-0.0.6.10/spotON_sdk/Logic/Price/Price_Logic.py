from typing import Any, List, Union
from pydantic import  Field, PositiveInt

from .timeframes import Timeframe, hours_to_timeframes
from .markets import Market, Markets
from pprint import pprint
import pandas as pd

from typing import List, Union, Optional
from pydantic import BaseModel, Field
from .timeframes import Timeframe
from .markets import Market, Markets

class PricefindingError(ValueError):
    pass

class Interrupted_On_Time(BaseModel):
    name: str = "Interrupted_On_Time"

class Continuous_On_Time(BaseModel):
    name: str = "Continuous_On_Time"
    week: Optional[int] = Field(None, ge=0)
    best_hour: Optional[int] = Field(None, ge=0)

class Price_Logic(BaseModel):
    nr_of_hours_on: PositiveInt = Field(ge=1)
    market: Market
    minimum_hours_on: PositiveInt = Field(default=1, ge=1, le=24)
    timeframes: List[Timeframe] = Field(default_factory=lambda: [Timeframe(start=-1,end=22)])
    pricefinding: Union[Continuous_On_Time, Interrupted_On_Time] = Field(default_factory=Interrupted_On_Time)
    resolution: float = Field(default=1.0)

    @property
    def possible_hours(self) -> List[int]:
        hours = set()
        for timeframe in self.timeframes:
            start, end = timeframe.start, timeframe.end
            end += 1
            hours.update(range(start, end))

        return sorted(list(hours))
    

    
    def possible_hours_with_utc_offset(self) -> List[int]:
        offset = self.market.area.calculate_utc_offset()
        hours = set()   
        for hour in self.possible_hours:
            hours.add(hour + offset)



        return sorted(list(hours))


    def add_utc_timeframe(self, start: int, end: int):
        self.timeframes.append(Timeframe(start=start, end=end))

    def add_utc_timeframe_array(self, timeframe_array: List[Timeframe]):
        for timeframe in timeframe_array:
            self.add_utc_timeframe(timeframe.start, timeframe.end)

    def remove_timeframe(self, start: int, end: int):
        self.timeframes = [timeframe for timeframe in self.timeframes if not (timeframe.start == start and timeframe.end == end)]
    
    def remove_initial_timeframe(self):
        self.timeframes = self.timeframes[1:]


    def timeframes_as_String(self):
        timeframe_list = []
        for timeframe in self.timeframes:
            timeframe_list.append(str(timeframe.start) + " - " + str(timeframe.end) + " ")
        timeframe_str = ', '.join(map(str, timeframe_list))
        return timeframe_str    

    def update_pricefinding(self, pricefinding: Union[Continuous_On_Time, Interrupted_On_Time]):
        if not isinstance(pricefinding, (Continuous_On_Time, Interrupted_On_Time)):
            raise ValueError("Invalid type for pricefinding")
        self.pricefinding = pricefinding



    def update_timeframes(self, timeframes: List[Timeframe]):
        self.timeframes = timeframes

    def add_timeframe(self, start: int, end: int):
        '''Adds a localised timeframe to the list of timeframes'''
        utc_offset = self.market.area.calculate_utc_offset()

        start = (start - utc_offset)

        end = (end - utc_offset)

        self.timeframes.append(Timeframe(start=start, end=end))

    def add_timeframe_array(self, timeframe_array: List[Timeframe]):
        for timeframe in timeframe_array:
            self.add_timeframe(timeframe.start, timeframe.end)

        


    '''def to_json(self) -> str:
        switch_pattern_dict = self.to_dict()
        json_str = json.dumps(switch_pattern_dict)

        return json_str'''
    
    def pack(self) -> dict[str, Any]:
        '''Pack the object into a dictionary'''
        details = {
            "area": self.market.area.name,  
            "nr_of_hours_on": self.nr_of_hours_on,
            "timeframes": self.possible_hours,
            "pricefinding": self.pricefinding.name,
            "minimum_hours_on": self.minimum_hours_on
        }
        return details

    def get_start_end_hours_in_UTC(self) -> tuple[pd.Timestamp,pd.Timestamp]:
        return self.market.get_start_end_hours_in_UTC()

    @staticmethod
    def unpack(details: dict[str, Any]) -> "Price_Logic":
        pprint (f"{details=}")
        '''Unpack the dictionary into a Price_Logic object'''
        market = Markets.get_market_by_code(details["area"])
        nr_of_hours_on = details["nr_of_hours_on"]
        timeframes_decimal = details['timeframes']
        minimum_hours_on = details['minimum_hours_on']
        # Convert 'timeframes' list of Decimal to list of int
        timeframes_int = [int(tf) for tf in timeframes_decimal]
        print(f"timeframes_int before unpacking: {timeframes_int}")
        # If there's a function called 'hours_to_timeframes' you want to use, apply it here
        timeframes = hours_to_timeframes(timeframes_int)
        print(f"timeframes after unpacking: {timeframes}")
        pricefinding_class_string = details["pricefinding"]

        if market is None:
            raise ValueError("Market is not valid")
        price_logic = Price_Logic(nr_of_hours_on=nr_of_hours_on, market=market)
        price_logic.update_timeframes(timeframes)




        if pricefinding_class_string == Interrupted_On_Time().name:
            price_logic.update_pricefinding(Interrupted_On_Time())
            price_logic.minimum_hours_on = int(minimum_hours_on)
        else:
            raise PricefindingError
        

        

        print (f"{price_logic=}")

        return price_logic


