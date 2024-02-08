if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data, *args, **kwargs):
    """
    Template code for a transformer block.

    Add more parameters to this function if this block has multiple parent blocks.
    There should be one parameter for each output variable from each parent block.

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    # Remove rows where passenger count is 0 or trip distance is 0
    print(f"Preprocessing: total rows: {data.shape}")

    data = data[ (data['passenger_count'] > 0) & (data['trip_distance'] > 0) ]

    print(f"Shape of data with passengers > 0: {data.shape}")

    # Create a new column by converting lpep_pickup_datetime to a date
    data['lpep_pickup_date'] = data['lpep_pickup_datetime'].dt.date

    print(f"pickup_datetime: {data['lpep_pickup_datetime'].dtype}")
    print(f"pickup_date: {data['lpep_pickup_date'].dtype}")
    #print( data['lpep_pickup_datetime'][0])
    #print( data['lpep_pickup_date'][0])
    print(f"Shape of data after adding date col: {data.shape}")

    # Obtain the existing values of VendorID in the dataset
    print(f"Values of VendorID: { data['VendorID'].unique().tolist() }")

    # Rename columns in Camel Case to Snake Case
    print(f"Column names: {data.columns.values}")

    data.rename( columns={ "VendorID": "vendor_id",
                           "RatecodeID": "ratecode_id",
                           "PULocationID": "pu_location_id",
                           "DOLocationID": "do_location_id",
                             }, inplace=True)

    print(f"Column names: {data.columns.values}")

    return data


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    # assert: vendor_id is one of the existing values in the column
    assert 'vendor_id' in output.columns.values.tolist(), "vendor_id is not a column name."

    # assert: passenger_count is greater than 0
    assert output[ 'passenger_count'].isin([0]).sum()==0, "There are rides with 0 passengers."

    # assert trip_distance is greater than 0
    assert output['trip_distance'].isin([0]).sum()==0, "There are rides with 0 trip distance."

    assert output is not None, 'The output is undefined'
