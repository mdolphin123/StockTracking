from app.models.ProcessedData import ProcessedData

def generate_message(row: ProcessedData):
    return {
        'symbol': row.symbol,
        'price': row.open, #is price open?
        'timestamp': row.time_stamp.strftime('%Y-%m-%d %H:%M:%S'),
        'source':"Alpha Vantage",
        'raw_response_id':str(row.id)
    }



