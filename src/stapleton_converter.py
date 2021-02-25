
def change_neighborhood(hood):
    """ In the summer of 2020 Stapleton changed its name to Central park 
        this function can be used mapped over the neighborhood_id column
        of the Denver crime dataset to convert stapleton to central-park
    """
    if hood == 'stapleton':
        return 'central-park'
    return hood


#crime['NEIGHBORHOOD_ID'] = crime['NEIGHBORHOOD_ID'].map(change_neighborhood)
