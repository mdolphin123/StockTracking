from app.models.ProcessedData import ProcessedData
from app.models.RawData import RawData
from app.core.database import SessionDep
from app.services.generate_message import generate_message
from sqlmodel import select
from app.services.producer import producer


def raw_to_processed(raw_data: RawData, session: SessionDep, time_interval: int):

   #Big JSON file to process
   raw_json = raw_data.raw_data
   
   time_series = raw_json["Time Series (1min)"]
   sorted_keys = list(sorted(time_series.keys()))

   for i in range(0, len(sorted_keys)):
      existing = session.exec(select(ProcessedData).where(ProcessedData.symbol == raw_data.symbol, ProcessedData.time_stamp == sorted_keys[i])).first()
      if existing:
         continue

      row = ProcessedData(symbol = raw_data.symbol, created = raw_data.created, time_stamp = sorted_keys[i], interval = time_interval, 
                          open = time_series[sorted_keys[i]]["1. open"], close = time_series[sorted_keys[i]]["4. close"], high = time_series[sorted_keys[i]]["2. high"],
                          low = time_series[sorted_keys[i]]["3. low"])
      session.add(row)  
      session.commit()

      #producer stuff over here??
      
      my_message = generate_message(row)
      #should i put this after to be safe... then i can find my commit?
      producer.send('price-updates-new', my_message)
      
      producer.flush()

      #print("produced!")
      


   #filtered_data = list(filter(lambda d: datetime.strptime(d['year'], '%Y-%m-%dT%H:%M:%S.%f') > latest_time, data))
        #filtered_row = RawData(symbol = symbols[i], interval = time_interval, raw_data = filtered_data)