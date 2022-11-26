import pandas


def customCross(data):
    # initializing the matrix 
    x= data.ID
    y= data.Product
    t = pandas.DataFrame(index=x.drop_duplicates(), columns= y.drop_duplicates(), dtype= int).fillna(0)
    for index in range(1,t.shape[0]+2) :
        x = data[data['ID'] == index] 
        x = x.filter(items=['Product'])
        for key,item in x.iterrows() :
            t[item['Product']][index] = 1
    return t

def compare(customCross,pandasCross):
    for column in customCross:
        columnCustumCross = customCross[column]
        columnPandasCross = pandasCross[column]
        if( not columnCustumCross.convert_dtypes(convert_integer=True).equals(columnPandasCross.convert_dtypes(convert_integer=True)) ):
            f = open("customV.txt", "w")
            f2 = open("PandasV.txt", "w")
            print(column)
            f.write(columnCustumCross.to_string())
            f2.write(columnPandasCross.to_string())
            f.close()
            f2.close()
            return False
    return True
