import sqlite3
import csv
import json

# proj3_choc.py
# You can change anything in this file you want as long as you pass the tests
# and meet the project requirements! You will need to implement several new
# functions.

# Part 1: Read data from CSV and JSON into a new database called choc.db
DBNAME = 'choc.db'
BARSCSV = 'flavors_of_cacao_cleaned.csv'
COUNTRIESJSON = 'countries.json'
data_choc = []
conn = sqlite3.connect('choc.db')
cur = conn.cursor()

def create_bars_db():
    # Drop tables
    statement = '''
    DROP TABLE IF EXISTS 'Bars';
    '''
    cur.execute(statement)


    with open("flavors_of_cacao_cleaned.csv") as BARSCSV:
        csvReader = csv.reader(BARSCSV)
        for row in csvReader:
            if "Company" != row[0]:
                row[4] = row[4].rstrip("%")
                row[4] = float(row[4])*0.01
                row[4] = round(row[4],2)
                row[6] = round(float(row[6]),2)

                #print(type(row[4]))
                print(row[6])
            data_choc.append(row)


        #data_choc = data_choc[1:]
        #print(data_choc[0])


    statement = '''
            CREATE TABLE 'Bars' (
                'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
                'Company' TEXT NOT NULL,
                'SpecificBeanBarName' TEXT NOT NULL,
                'REF' TEXT NOT NULL,
                'ReviewDate' TEXT NOT NULL,
                'CocoaPercent' REAL NOT NULL,
                'CompanyLocationId' INTEGER NOT NULL,
                'Rating' REAL NOT NULL,
                'BeanType' TEXT NOT NULL,
                'BroadBeanOriginId' INTEGER NOT NULL

            );
        '''

    cur.execute(statement)

    for inst in data_choc[1:]:
        insertion = (None, inst[0], inst[1], inst[2],inst[3], inst[4], inst[5],inst[6], inst[7], inst[8])
        #print(insertion)
        statement = 'INSERT INTO "Bars"'
        statement += 'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
        cur.execute(statement,insertion)

    conn.commit()

    pass



def create_countries_db():
    statement = '''
    DROP TABLE IF EXISTS 'Countries';
    '''
    cur.execute(statement)

    data_country = []
    o = open("countries.json")
    load_country = json.load(o)
    #print(load_country)

    for row in load_country:
        data_country_row = []
        #print(load_country.index(row))
        data_country_row.append(load_country.index(row)+1)
        data_country_row.append(row["alpha2Code"])
        data_country_row.append(row["alpha3Code"])
        data_country_row.append(row["name"])
        data_country_row.append(row["region"])
        data_country_row.append(row["subregion"])
        data_country_row.append(row["population"])
        data_country_row.append(row["area"])
        data_country.append(data_country_row)



    #print("this is data_counrty[4]")
    #print(data_country[4])
    statement = '''
            CREATE TABLE 'Countries' (
                'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
                'Alpha2' TEXT NOT NULL,
                'Alpha3' TEXT NOT NULL,
                'EnglishName' TEXT NOT NULL,
                'Region' TEXT NOT NULL,
                'Subregion' TEXT NOT NULL,
                'Population' INTEGER NOT NULL,
                'Area' REAL
            );
        '''

    cur.execute(statement)

    for inst in data_country:
        insertion = (inst[0], inst[1], inst[2], inst[3], inst[4], inst[5], inst[6],inst[7])
        print(insertion)
        statement = 'INSERT INTO "Countries"'
        statement += 'VALUES (?, ?, ?, ?, ?, ?, ?, ?)'
        cur.execute(statement,insertion)

    conn.commit()
    pass





#print(create_bars_db())

#print(create_countries_db())



#command = "bars ratings top=1"
# Part 2: Implement logic to process user commands

def bars_return(command):
    conn = sqlite3.connect('choc.db')
    cur = conn.cursor()
    get_bars_data = []
    statement = "SELECT Bars.'SpecificBeanBarName',Bars.'Company', Bars.'CompanyLocationId', Bars.'Rating',Bars.'CocoaPercent', Bars.'BroadBeanOriginId' "
    #print("ription: Specifies a country or region within which to limit the results, and also specifies whether to limit by the seller (or manufacturer) or by the bean origin source.: ")
    s = command.split()
    bar_infor = []


    print(s)
    for i in s:
        o = i.split("=")
        if len(o) == 2:
            if "sellcountry" in o:
                sellcountry = o[1]
            elif "sourcecountry" in o:
                sourcecountry = o[1]
            elif "sourceregion" in o:
                sourceregion = o[1]
            elif "sellregion" in o:
                sellregion = o[1]
            elif "bottom" in o:
                bottom = o[1]
            elif "top" in o:
                top = o[1]

    if "sellcountry" in s:
        pass
    elif "sourceregion" in s:
        pass
    elif "ratings" in s:
        pass
    elif "cocoa"  in s:
        pass
    elif "top" in s:
        pass
    elif "bottom"  in s:
        pass
    elif "country"  in s:
        pass
    elif "region"  in s:
        pass
    elif "sellers"   in s:
        pass
    elif "sources"  in s:
        pass
    else:
        return("command is wrong")



    i = command
    if "sellcountry" in i:
        statement += " FROM Bars join Countries on Bars.CompanyLocationId= Countries.EnglishName"
        statement += ' WHERE Alpha2="' + str(sellcountry) + '" '
        if "cocoa" in i:
            statement += ' ORDER BY CocoaPercent'
            if "bottom" in i:
                statement += '  Limit "' + str(bottom) + '" '
                print(statement)
                cur.execute(statement)
                for row in cur:
                    bar_infor.append(row)
                return(bar_infor)
            elif "top" in i:
                statement += ' DESC Limit "' + str(top) + '" '
                print(statement)
                cur.execute(statement)
                for row in cur:
                    bar_infor.append(row)
                return(bar_infor)
            else:
                statement += ' DESC Limit 10'
                print(statement)
                cur.execute(statement)
                for row in cur:
                    bar_infor.append(row)
                return(bar_infor)
        else:
            statement += ' ORDER BY Rating'
            if "bottom" in i:
                statement += '  Limit "' + str(bottom) + '" '
                print(statement)
                cur.execute(statement)
                for row in cur:
                    bar_infor.append(row)
                return(bar_infor)
            elif "top" in i:
                statement += ' DESC Limit "' + str(top) + '" '
                print(statement)
                cur.execute(statement)
                for row in cur:
                    bar_infor.append(row)
                return(bar_infor)
            else:
                statement += '  DESC Limit 10'
                print(statement)
                cur.execute(statement)
                for row in cur:
                    bar_infor.append(row)
                return(bar_infor)
    elif "sourcecountry" in i:
        statement += " FROM Bars join Countries on Bars.CompanyLocationId= Countries.EnglishName"
        statement += ' WHERE Alpha2="' + str(sourcecountry) + '" '
        if "cocoa" in i:
            statement += ' ORDER BY CocoaPercent'
            if "bottom" in i:
                statement += '  Limit "' + str(bottom) + '" '
                print(statement)
                cur.execute(statement)
                for row in cur:
                    bar_infor.append(row)
                return(bar_infor)
            elif "top" in i:
                statement += ' DESC Limit "' + str(top) + '" '
                print(statement)
                cur.execute(statement)
                for row in cur:
                    bar_infor.append(row)
                return(bar_infor)
            else:
                statement += ' DESC Limit 10'
                print(statement)
                cur.execute(statement)
                for row in cur:
                    bar_infor.append(row)
                return(bar_infor)
        else:
            statement += ' ORDER BY Rating'
            if "bottom" in i:
                statement += '  Limit "' + str(bottom) + '" '
                print(statement)
                cur.execute(statement)
                for row in cur:
                    bar_infor.append(row)
                return(bar_infor)
            elif "top" in i:
                statement += ' DESC Limit "' + str(top) + '" '
                print(statement)
                cur.execute(statement)
                for row in cur:
                    bar_infor.append(row)
                return(bar_infor)
            else:
                statement += ' DESC Limit 10'
                print(statement)
                cur.execute(statement)
                for row in cur:
                    bar_infor.append(row)
                return(bar_infor)
    elif "sellregion" in i:
        statement += " FROM Bars join Countries on Bars.BroadBeanOriginId= Countries.EnglishName"
        statement += ' WHERE Region="' + str(sellregion) + '" '
        if "cocoa" in i:
            statement += ' ORDER BY CocoaPercent'
            if "bottom" in i:
                statement += '  Limit "' + str(bottom) + '" '
                print(statement)
                cur.execute(statement)
                for row in cur:
                    bar_infor.append(row)
                return(bar_infor)
            elif "top" in i:
                statement += ' DESC Limit "' + str(top) + '" '
                print(statement)
                cur.execute(statement)
                for row in cur:
                    bar_infor.append(row)
                return(bar_infor)
            else:
                statement += ' DESC Limit 10'
                print(statement)
                cur.execute(statement)
                for row in cur:
                    bar_infor.append(row)
                return(bar_infor)
        else:
            statement += ' ORDER BY Rating'
            if "bottom" in i:
                statement += '  Limit "' + str(bottom) + '" '
                print(statement)
                cur.execute(statement)
                for row in cur:
                    bar_infor.append(row)
                return(bar_infor)
            elif "top" in i:
                statement += ' DESC Limit "' + str(top) + '" '
                print(statement)
                cur.execute(statement)
                for row in cur:
                    bar_infor.append(row)
                return(bar_infor)
            else:
                statement += ' DESC Limit 10'
                print(statement)
                cur.execute(statement)
                for row in cur:
                    bar_infor.append(row)
                return(bar_infor)
    elif "sourceregion"in i:
        statement += " FROM Bars join Countries on Bars.BroadBeanOriginId= Countries.EnglishName"
        statement += ' WHERE Region="' + str(sourceregion) + '" '
        if "cocoa" in i:
            statement += ' ORDER BY CocoaPercent'
            if "bottom" in i:
                statement += '  Limit "' + str(bottom) + '" '
                print(statement)
                cur.execute(statement)
                for row in cur:
                    bar_infor.append(row)
                return(bar_infor)
            elif "top" in i:
                statement += ' DESC Limit "' + str(top) + '" '
                print(statement)
                cur.execute(statement)
                for row in cur:
                    bar_infor.append(row)
                return(bar_infor)
            else:
                statement += ' DESC Limit 10'
                print(statement)
                cur.execute(statement)
                for row in cur:
                    bar_infor.append(row)
                return(bar_infor)
        else:
            statement += ' ORDER BY Rating'
            if "bottom" in i:
                statement += '  Limit "' + str(bottom) + '" '
                print(statement)
                cur.execute(statement)
                for row in cur:
                    bar_infor.append(row)
                return(bar_infor)
            elif "top" in i:
                statement += ' DESC Limit "' + str(top) + '" '
                print(statement)
                cur.execute(statement)
                for row in cur:
                    bar_infor.append(row)
                return(bar_infor)
            else:
                statement += ' DESC  Limit 10'
                print(statement)
                cur.execute(statement)
                for row in cur:
                    bar_infor.append(row)
                return(bar_infor)
    else:
        statement += ' From Bars'
        #statement += " FROM Bars join Countries on Bars.CompanyLocationId= Countries.EnglishName"
        if "cocoa" in i:
            statement += ' ORDER BY CocoaPercent'
            if "bottom" in i:
                statement += '  Limit "' + str(bottom) + '" '
                print(statement)
                cur.execute(statement)
                for row in cur:
                    bar_infor.append(row)
                return(bar_infor)

            elif "top" in i:
                statement += '  DESC Limit "' + str(top) + '" '
                print(statement)
                cur.execute(statement)
                for row in cur:
                    bar_infor.append(row)
                return(bar_infor)
            else:
                statement += ' DESC  Limit 10'
                print(statement)
                cur.execute(statement)
                for row in cur:
                    bar_infor.append(row)
                return(bar_infor)
        else:
            statement += ' ORDER BY Rating '
            if "bottom" in i:
                statement += ' Limit "' + str(bottom) + '" '
                print(statement)
                cur.execute(statement)
                for row in cur:
                    bar_infor.append(row)
                return(bar_infor)
            elif "top" in i:
                statement += ' DESC  Limit "' + str(top) + '" '
                print(statement)
                cur.execute(statement)
                print("this is cur")
                print(cur)
                for row in cur:
                    bar_infor.append(row)
                #print(bar_infor)
                return(bar_infor)
            else:
                statement += ' DESC  Limit 10'
                print(statement)
                cur.execute(statement)
                for row in cur:
                    bar_infor.append(row)
                return(bar_infor)



#print(bars_return())


def companies_return(command):
    conn = sqlite3.connect('choc.db')
    cur = conn.cursor()
    get_bars_data = []
    #statement = "SELECT Bars.Company "
    #print("ription: Specifies a country or region within which to limit the results, and also specifies whether to limit by the seller (or manufacturer) or by the bean origin source.: ")
    if "cocoa" in command:
        statement = "SELECT Bars.Company, Bars.CompanyLocationId, round(AVG(Bars.CocoaPercent),2)"
    elif "bars_sold" in command:
        statement = "SELECT Bars.Company, Bars.CompanyLocationId, COUNT(Bars.SpecificBeanBarName)"
    else:
        statement = "SELECT Bars.Company, Bars.CompanyLocationId, round(AVG(Bars.Rating),2) "
    s = command.split()
    bar_infor = []

    if "sellcountry" in s:
        pass
    elif "sourceregion" in s:
        pass
    elif "ratings" in s:
        pass
    elif "cocoa"  in s:
        pass
    elif "bars_sold" in s:
        pass
    elif "top" in s:
        pass
    elif "bottom"  in s:
        pass
    elif "country"  in s:
        pass
    elif "region"  in s:
        pass
    elif "sellers"   in s:
        pass
    elif "sources"  in s:
        pass
    else:
        return("command is wrong")
    print(s)
    for i in s:
        o = i.split("=")
        if len(o) == 2:
            if "country" in o:
                country = o[1]
                print(country)
            elif "region" in o:
                region = o[1]
                print(region)
            elif "bottom" in o:
                bottom = o[1]
                print(bottom)
            elif "top" in o:
                top = o[1]
                print(top)
    i = command
    if "country" in i:
        statement += " FROM Bars join Countries on Bars.CompanyLocationId= Countries.EnglishName"
        statement += " GROUP BY Bars.Company"
        if "cocoa" in i:
            statement += ' HAVING Alpha2="' + str(country) + '" '
            statement += ' AND COUNT(Bars.SpecificBeanBarName) > 4'
            statement += ' ORDER BY round(AVG(Bars.CocoaPercent),2)'
            if "bottom" in i:
                statement += '  Limit "' + str(bottom) + '" '
                print(statement)
                cur.execute(statement)
                for row in cur:
                    bar_infor.append(row)
                return(bar_infor)
            elif "top" in i:
                statement += ' DESC Limit "' + str(top) + '" '
                print(statement)
                cur.execute(statement)
                for row in cur:
                    bar_infor.append(row)
                return(bar_infor)
            else:
                statement += ' DESC Limit 10'
                print(statement)
                cur.execute(statement)
                for row in cur:
                    bar_infor.append(row)
                return(bar_infor)
        elif "bars_sold" in i:
            statement += ' HAVING Alpha2="' + str(country) + '" '
            statement += ' AND COUNT(Bars.SpecificBeanBarName) > 4'
            statement += ' ORDER BY COUNT(Bars.SpecificBeanBarName)'
            if "bottom" in i:
                statement += ' Limit "' + str(bottom) + '" '
                print(statement)
                cur.execute(statement)
                for row in cur:
                    bar_infor.append(row)
                return(bar_infor)
            elif "top" in i:
                statement += ' DESC Limit "' + str(top) + '" '
                print(statement)
                cur.execute(statement)
                for row in cur:
                    bar_infor.append(row)
                return(bar_infor)
            else:
                statement += ' DESC Limit 10'
                print(statement)
                cur.execute(statement)
                for row in cur:
                    bar_infor.append(row)
                return(bar_infor)
        else:
            statement += ' HAVING Alpha2="' + str(country) + '" '
            statement += ' AND COUNT(Bars.SpecificBeanBarName) > 4'
            statement += ' ORDER BY round(AVG(Bars.Rating),2)'
            if "bottom" in i:
                statement += '  Limit "' + str(bottom) + '" '
                print(statement)
                cur.execute(statement)
                for row in cur:
                    bar_infor.append(row)
                return(bar_infor)
            elif "top" in i:
                statement += ' DESC Limit "' + str(top) + '" '
                print(statement)
                cur.execute(statement)
                for row in cur:
                    bar_infor.append(row)
                return(bar_infor)
            else:
                statement += ' DESC Limit 10'
                print(statement)
                cur.execute(statement)
                for row in cur:
                    bar_infor.append(row)
                return(bar_infor)
    elif "region" in i:
        statement += " FROM Bars join Countries on Bars.CompanyLocationId= Countries.EnglishName"
        statement += " GROUP BY Bars.Company"
        if "cocoa" in i:
            statement += ' HAVING COUNT(Bars.SpecificBeanBarName) > 4'
            statement += ' AND Region="' + str(region) + '" '
            statement += ' ORDER BY round(AVG(Bars.CocoaPercent),2)'
            if "bottom" in i:
                statement += '  Limit "' + str(bottom) + '" '
                print(statement)
                cur.execute(statement)
                for row in cur:
                    bar_infor.append(row)
                return(bar_infor)
            elif "top" in i:
                statement += ' DESC Limit "' + str(top) + '" '
                print(statement)
                cur.execute(statement)
                for row in cur:
                    bar_infor.append(row)
                return(bar_infor)
            else:
                statement += ' DESC Limit 10'
                print(statement)
                cur.execute(statement)
                for row in cur:
                    bar_infor.append(row)
                return(bar_infor)
        elif "bars_sold" in i:
            statement += ' HAVING COUNT(Bars.SpecificBeanBarName) > 4'
            statement += ' AND Region="' + str(region) + '" '
            statement += ' ORDER BY COUNT(Bars.SpecificBeanBarName)'
            if "bottom" in i:
                statement += ' Limit "' + str(bottom) + '" '
                print(statement)
                cur.execute(statement)
                for row in cur:
                    bar_infor.append(row)
                return(bar_infor)
            elif "top" in i:
                statement += ' DESC Limit "' + str(top) + '" '
                print(statement)
                cur.execute(statement)
                for row in cur:
                    bar_infor.append(row)
                return(bar_infor)
            else:
                statement += ' DESC Limit 10'
                print(statement)
                cur.execute(statement)
                for row in cur:
                    bar_infor.append(row)
                return(bar_infor)
        else:
            statement += ' HAVING COUNT(Bars.SpecificBeanBarName) > 4'
            statement += ' AND Region="' + str(region) + '" '
            statement += ' ORDER BY Bars.Rating'
            if "bottom" in i:
                statement += '  Limit "' + str(bottom) + '" '
                print(statement)
                cur.execute(statement)
                for row in cur:
                    bar_infor.append(row)
                return(bar_infor)
            elif "top" in i:
                statement += ' DESC Limit "' + str(top) + '" '
                print(statement)
                cur.execute(statement)
                for row in cur:
                    bar_infor.append(row)
                return(bar_infor)
            else:
                statement += ' DESC Limit 10'
                print(statement)
                cur.execute(statement)
                for row in cur:
                    bar_infor.append(row)
                return(bar_infor)
    else:
        statement += " FROM Bars join Countries on Bars.CompanyLocationId= Countries.EnglishName"
        if "cocoa" in i:
            statement += " GROUP BY Bars.Company"
            statement += ' HAVING COUNT(Bars.SpecificBeanBarName) > 4'

            statement += ' ORDER BY round(AVG(Bars.CocoaPercent),2) '
            if "bottom" in i:
                statement += '  Limit "' + str(bottom) + '" '
                print(statement)
                cur.execute(statement)
                for row in cur:
                    bar_infor.append(row)
                return(bar_infor)
            elif "top" in i:
                statement += ' DESC Limit "' + str(top) + '" '
                print(statement)
                cur.execute(statement)
                for row in cur:
                    bar_infor.append(row)
                return(bar_infor)
            else:
                statement += ' DESC Limit 10'
                print(statement)
                cur.execute(statement)
                for row in cur:
                    bar_infor.append(row)
                return(bar_infor)
        elif "bars_sold" in i:
            statement += " GROUP BY Bars.Company"
            statement += ' HAVING COUNT(Bars.SpecificBeanBarName) > 4'
            statement += ' ORDER BY COUNT(Bars.SpecificBeanBarName)'
            if "bottom" in i:
                statement += ' Limit "' + str(bottom) + '" '
                print(statement)
                cur.execute(statement)
                for row in cur:
                    bar_infor.append(row)
                return(bar_infor)
            elif "top" in i:
                statement += ' DESC Limit "' + str(top) + '" '
                print(statement)
                cur.execute(statement)
                for row in cur:
                    bar_infor.append(row)
                return(bar_infor)
            else:
                statement += ' DESC Limit 10'
                print(statement)
                cur.execute(statement)
                for row in cur:
                    bar_infor.append(row)
                return(bar_infor)
        else:
            statement += " GROUP BY Bars.Company"
            statement += ' HAVING COUNT(Bars.SpecificBeanBarName) > 4'
            statement += ' ORDER BY round(AVG(Bars.Rating),2) '
            if "bottom" in i:
                statement += '  Limit "' + str(bottom) + '" '
                print(statement)
                cur.execute(statement)
                for row in cur:
                    bar_infor.append(row)
                return(bar_infor)
            elif "top" in i:
                statement += ' DESC Limit "' + str(top) + '" '
                print(statement)
                cur.execute(statement)
                for row in cur:
                    bar_infor.append(row)
                return(bar_infor)
            else:
                statement += ' DESC Limit 10'
                print(statement)
                cur.execute(statement)
                for row in cur:
                    bar_infor.append(row)
                return(bar_infor)




def countries_return(command):
    conn = sqlite3.connect('choc.db')
    cur = conn.cursor()
    get_bars_data = []
    #statement = "SELECT Bars.Company "
    #print("ription: Specifies a country or region within which to limit the results, and also specifies whether to limit by the seller (or manufacturer) or by the bean origin source.: ")
    if "cocoa" in command:
        statement = "SELECT Countries.EnglishName , Countries.Region, round(AVG(Bars.CocoaPercent),2)"
    elif "bars_sold" in command:
        statement = "SELECT Countries.EnglishName , Countries.Region, COUNT(Bars.SpecificBeanBarName)"
    else:
        statement = "SELECT Countries.EnglishName , Countries.Region, round(AVG(Bars.Rating),2) "
    s = command.split()
    bar_infor = []
    if "sellcountry" in s:
        pass
    elif "sourceregion" in s:
        pass
    elif "ratings" in s:
        pass
    elif "cocoa"  in s:
        pass
    elif "bars_sold" in s:
        pass
    elif "top" in s:
        pass
    elif "bottom"  in s:
        pass
    elif "country"  in s:
        pass
    elif "region"  in s:
        pass
    elif "sellers"   in s:
        pass
    elif "sources"  in s:
        pass
    else:
        return("command is wrong")

    print(s)
    for i in s:
        o = i.split("=")
        if len(o) == 2:
            if "region" in o:
                region = o[1]
                print(region)
            elif "bottom" in o:
                bottom = o[1]
                print(bottom)
            elif "top" in o:
                top = o[1]
                print(top)
    i = command
    print(i)
    if "region" in i:
        print("connecting region")
        if "sources" in i:
            print("connecting source")
            statement += " FROM Bars join Countries on Bars.BroadBeanOriginId= Countries.EnglishName"
            if "cocoa" in i:
                statement += " GROUP BY Countries.EnglishName"
                statement += ' HAVING COUNT(Bars.SpecificBeanBarName) > 4'
                statement += ' AND Region="' + str(region) + '" '
                statement += " ORDER BY round(AVG(Bars.CocoaPercent),2) "
                if "bottom" in i:
                    statement += '  Limit "' + str(bottom) + '" '
                    print(statement)
                    cur.execute(statement)
                    for row in cur:
                        bar_infor.append(row)
                    return(bar_infor)
                elif "top" in i:
                    statement += ' DESC Limit "' + str(top) + '" '
                    print(statement)
                    cur.execute(statement)
                    for row in cur:
                        bar_infor.append(row)
                    return(bar_infor)
                else:
                    statement += ' DESC Limit 10'
                    print(statement)
                    cur.execute(statement)
                    for row in cur:
                        bar_infor.append(row)
                    return(bar_infor)
            elif "bars_sold" in i:
                statement += " GROUP BY Countries.EnglishName"
                statement += ' HAVING COUNT(Bars.SpecificBeanBarName) > 4'
                statement += ' AND Region="' + str(region) + '" '
                statement += ' ORDER BY COUNT(Bars.SpecificBeanBarName)'
                if "bottom" in i:
                    statement += ' Limit "' + str(bottom) + '" '
                    print(statement)
                    cur.execute(statement)
                    for row in cur:
                        bar_infor.append(row)
                    return(bar_infor)
                elif "top" in i:
                    statement += ' DESC Limit "' + str(top) + '" '
                    print(statement)
                    cur.execute(statement)
                    for row in cur:
                        bar_infor.append(row)
                    return(bar_infor)
                else:
                    statement += ' DESC Limit 10'
                    print(statement)
                    cur.execute(statement)
                    for row in cur:
                        bar_infor.append(row)
                    return(bar_infor)
            else:
                statement += " GROUP BY Countries.EnglishName"
                statement += ' HAVING COUNT(Bars.SpecificBeanBarName) > 4'
                statement += ' AND Region="' + str(region) + '" '
                statement += ' ORDER BY round(AVG(Bars.Rating),2)'
                if "bottom" in i:
                    statement += '  Limit "' + str(bottom) + '" '
                    print(statement)
                    cur.execute(statement)
                    for row in cur:
                        bar_infor.append(row)
                    return(bar_infor)
                elif "top" in i:
                    statement += ' DESC Limit "' + str(top) + '" '
                    print(statement)
                    cur.execute(statement)
                    for row in cur:
                        bar_infor.append(row)
                    return(bar_infor)
                else:
                    statement += ' DESC Limit 10'
                    print(statement)
                    cur.execute(statement)
                    for row in cur:
                        bar_infor.append(row)
                    return(bar_infor)
        else:
            print("connecting seller")
            statement += " FROM Bars join Countries on Bars.CompanyLocationId= Countries.EnglishName"
            if "cocoa" in i:
                statement += " GROUP BY Countries.EnglishName"
                statement += ' HAVING COUNT(Bars.SpecificBeanBarName) > 4'
                statement += ' AND Region="' + str(region) + '" '
                statement += " ORDER BY round(AVG(Bars.CocoaPercent),2) "
                if "bottom" in i:
                    statement += '  Limit "' + str(bottom) + '" '
                    print(statement)
                    cur.execute(statement)
                    for row in cur:
                        bar_infor.append(row)
                    return(bar_infor)
                elif "top" in i:
                    statement += ' DESC Limit "' + str(top) + '" '
                    print(statement)
                    cur.execute(statement)
                    for row in cur:
                        bar_infor.append(row)
                    return(bar_infor)
                else:
                    statement += ' DESC Limit 10'
                    print(statement)
                    cur.execute(statement)
                    for row in cur:
                        bar_infor.append(row)
                    return(bar_infor)
            elif "bars_sold" in i:
                statement += " GROUP BY Countries.EnglishName"
                statement += ' HAVING COUNT(Bars.SpecificBeanBarName) > 4'
                statement += ' AND Region="' + str(region) + '" '
                statement += ' ORDER BY COUNT(Bars.SpecificBeanBarName)'
                if "bottom" in i:
                    statement += ' Limit "' + str(bottom) + '" '
                    print(statement)
                    cur.execute(statement)
                    for row in cur:
                        bar_infor.append(row)
                    return(bar_infor)
                elif "top" in i:
                    statement += ' DESC Limit "' + str(top) + '" '
                    print(statement)
                    cur.execute(statement)
                    for row in cur:
                        bar_infor.append(row)
                    return(bar_infor)
                else:
                    statement += ' DESC Limit 10'
                    print(statement)
                    cur.execute(statement)
                    for row in cur:
                        bar_infor.append(row)
                    return(bar_infor)
            else:
                statement += " GROUP BY Countries.EnglishName"
                statement += ' HAVING COUNT(Bars.SpecificBeanBarName) > 4'
                statement += ' AND Region="' + str(region) + '" '
                statement += ' ORDER BY round(AVG(Bars.Rating),2)'
                if "bottom" in i:
                    statement += '  Limit "' + str(bottom) + '" '
                    print(statement)
                    cur.execute(statement)
                    for row in cur:
                        bar_infor.append(row)
                    return(bar_infor)
                elif "top" in i:
                    statement += ' DESC Limit "' + str(top) + '" '
                    print(statement)
                    cur.execute(statement)
                    for row in cur:
                        bar_infor.append(row)
                    return(bar_infor)
                else:
                    statement += ' DESC Limit 10'
                    print(statement)
                    cur.execute(statement)
                    for row in cur:
                        bar_infor.append(row)
                    return(bar_infor)

    else:
        print("connecting else")
        if "sources" in i:
            statement += " FROM Bars join Countries on Bars.BroadBeanOriginId= Countries.EnglishName"
            if "cocoa" in i:
                statement += " GROUP BY Countries.EnglishName"
                statement += ' HAVING COUNT(Bars.SpecificBeanBarName) > 4'
                statement += " ORDER BY round(AVG(Bars.CocoaPercent),2) "
                if "bottom" in i:
                    statement += '  Limit "' + str(bottom) + '" '
                    print(statement)
                    cur.execute(statement)
                    for row in cur:
                        bar_infor.append(row)
                    return(bar_infor)
                elif "top" in i:
                    statement += ' DESC Limit "' + str(top) + '" '
                    print(statement)
                    cur.execute(statement)
                    for row in cur:
                        bar_infor.append(row)
                    return(bar_infor)
                else:
                    statement += ' DESC Limit 10'
                    print(statement)
                    cur.execute(statement)
                    for row in cur:
                        bar_infor.append(row)
                    return(bar_infor)
            elif "bars_sold" in i:
                statement += " GROUP BY Countries.EnglishName"
                statement += ' HAVING COUNT(Bars.SpecificBeanBarName) > 4'
                statement += ' ORDER BY COUNT(Bars.SpecificBeanBarName)'
                if "bottom" in i:
                    statement += ' Limit "' + str(bottom) + '" '
                    print(statement)
                    cur.execute(statement)
                    for row in cur:
                        bar_infor.append(row)
                    return(bar_infor)
                elif "top" in i:
                    statement += ' DESC Limit "' + str(top) + '" '
                    print(statement)
                    cur.execute(statement)
                    for row in cur:
                        bar_infor.append(row)
                    return(bar_infor)
                else:
                    statement += ' DESC Limit 10'
                    print(statement)
                    cur.execute(statement)
                    for row in cur:
                        bar_infor.append(row)
                    return(bar_infor)
            else:
                statement += " GROUP BY Countries.EnglishName"
                statement += ' HAVING COUNT(Bars.SpecificBeanBarName) > 4'
                statement += ' ORDER BY round(AVG(Bars.Rating),2)'
                if "bottom" in i:
                    statement += '  Limit "' + str(bottom) + '" '
                    print(statement)
                    cur.execute(statement)
                    for row in cur:
                        bar_infor.append(row)
                    return(bar_infor)
                elif "top" in i:
                    statement += ' DESC Limit "' + str(top) + '" '
                    print(statement)
                    cur.execute(statement)
                    for row in cur:
                        bar_infor.append(row)
                    return(bar_infor)
                else:
                    statement += ' DESC Limit 10'
                    print(statement)
                    cur.execute(statement)
                    for row in cur:
                        bar_infor.append(row)
                    return(bar_infor)
        else:
            statement += " FROM Bars join Countries on Bars.CompanyLocationId= Countries.EnglishName"
            if "cocoa" in i:
                statement += " GROUP BY Countries.EnglishName"
                statement += ' HAVING COUNT(Bars.SpecificBeanBarName) > 4'
                statement += " ORDER BY round(AVG(Bars.CocoaPercent),2) "
                if "bottom" in i:
                    statement += '  Limit "' + str(bottom) + '" '
                    print(statement)
                    cur.execute(statement)
                    for row in cur:
                        bar_infor.append(row)
                    return(bar_infor)
                elif "top" in i:
                    statement += ' DESC Limit "' + str(top) + '" '
                    print(statement)
                    cur.execute(statement)
                    for row in cur:
                        bar_infor.append(row)
                    return(bar_infor)
                else:
                    statement += ' DESC Limit 10'
                    print(statement)
                    cur.execute(statement)
                    for row in cur:
                        bar_infor.append(row)
                    return(bar_infor)
            elif "bars_sold" in i:
                statement += " GROUP BY Countries.EnglishName"
                statement += ' HAVING COUNT(Bars.SpecificBeanBarName) > 4'
                statement += ' ORDER BY COUNT(Bars.SpecificBeanBarName)'
                if "bottom" in i:
                    statement += ' Limit "' + str(bottom) + '" '
                    print(statement)
                    cur.execute(statement)
                    for row in cur:
                        bar_infor.append(row)
                    return(bar_infor)
                elif "top" in i:
                    statement += ' DESC Limit "' + str(top) + '" '
                    print(statement)
                    cur.execute(statement)
                    for row in cur:
                        bar_infor.append(row)
                    return(bar_infor)
                else:
                    statement += ' DESC Limit 10'
                    print(statement)
                    cur.execute(statement)
                    for row in cur:
                        bar_infor.append(row)
                    return(bar_infor)
            else:
                statement += " GROUP BY Countries.EnglishName"
                statement += ' HAVING COUNT(Bars.SpecificBeanBarName) > 4'
                statement += ' ORDER BY round(AVG(Bars.Rating),2)'
                if "bottom" in i:
                    statement += '  Limit "' + str(bottom) + '" '
                    print(statement)
                    cur.execute(statement)
                    for row in cur:
                        bar_infor.append(row)
                    return(bar_infor)
                elif "top" in i:
                    statement += ' DESC Limit "' + str(top) + '" '
                    print(statement)
                    cur.execute(statement)
                    for row in cur:
                        bar_infor.append(row)
                    return(bar_infor)
                else:
                    statement += ' DESC Limit 10'
                    print(statement)
                    cur.execute(statement)
                    for row in cur:
                        bar_infor.append(row)
                    return(bar_infor)


#print(countries_return(command= "companies country=US bars_sold top=5"))




def region_return(command):
    conn = sqlite3.connect('choc.db')
    cur = conn.cursor()
    get_bars_data = []
    #statement = "SELECT Bars.Company "
    #print("ription: Specifies a country or region within which to limit the results, and also specifies whether to limit by the seller (or manufacturer) or by the bean origin source.: ")
    if "cocoa" in command:
        statement = "SELECT Countries.Region, round(AVG(Bars.CocoaPercent),2)"
    elif "bars_sold" in command:
        statement = "SELECT Countries.Region, COUNT(Bars.SpecificBeanBarName)"
    else:
        statement = "SELECT Countries.Region, round(AVG(Bars.Rating),2) "
    s = command.split()
    if "sellcountry" in s:
        pass
    elif "sourceregion" in s:
        pass
    elif "ratings" in s:
        pass
    elif "cocoa"  in s:
        pass
    elif "bars_sold" in s:
        pass
    elif "top" in s:
        pass
    elif "bottom"  in s:
        pass
    elif "country"  in s:
        pass
    elif "region"  in s:
        pass
    elif "sellers"   in s:
        pass
    elif "sources"  in s:
        pass
    else:
        return("command is wrong")

    bar_infor = []
    print(s)
    for i in s:
        o = i.split("=")
        if len(o) == 2:
            if "bottom" in o:
                bottom = o[1]
                print(bottom)
            elif "top" in o:
                top = o[1]
                print(top)
    i = command
    if "sources" in i:
        statement += " FROM Bars join Countries on Bars.BroadBeanOriginId= Countries.EnglishName"
        if "cocoa" in i:
            statement += " GROUP BY Bars.BroadBeanOriginId"
            statement += ' HAVING COUNT(Bars.SpecificBeanBarName) > 4'
            statement += " ORDER BY round(AVG(Bars.CocoaPercent),2) "
            if "bottom" in i:
                statement += '  Limit "' + str(bottom) + '" '
                print(statement)
                cur.execute(statement)
                for row in cur:
                    bar_infor.append(row)
                return(bar_infor)
            elif "top" in i:
                statement += ' DESC Limit "' + str(top) + '" '
                print(statement)
                cur.execute(statement)
                for row in cur:
                    bar_infor.append(row)
                return(bar_infor)
            else:
                statement += ' DESC Limit 10'
                print(statement)
                cur.execute(statement)
                for row in cur:
                    bar_infor.append(row)
                return(bar_infor)
        elif "bars_sold" in i:
            statement += " GROUP BY Countries.Region"
            statement += ' HAVING COUNT(Bars.SpecificBeanBarName) > 4'
            statement += ' ORDER BY COUNT(Bars.SpecificBeanBarName)'
            if "bottom" in i:
                statement += ' Limit "' + str(bottom) + '" '
                print(statement)
                cur.execute(statement)
                for row in cur:
                    bar_infor.append(row)
                return(bar_infor)
            elif "top" in i:
                statement += ' DESC Limit "' + str(top) + '" '
                print(statement)
                cur.execute(statement)
                for row in cur:
                    bar_infor.append(row)
                return(bar_infor)
            else:
                statement += ' DESC Limit 10'
                print(statement)
                cur.execute(statement)
                for row in cur:
                    bar_infor.append(row)
                return(bar_infor)
        else:
            statement += " GROUP BY Countries.Region"
            statement += ' HAVING COUNT(Bars.SpecificBeanBarName) > 4'
            statement += ' ORDER BY round(AVG(Bars.Rating),2)'
            if "bottom" in i:
                statement += '  Limit "' + str(bottom) + '" '
                print(statement)
                cur.execute(statement)
                for row in cur:
                    bar_infor.append(row)
                return(bar_infor)
            elif "top" in i:
                statement += ' DESC Limit "' + str(top) + '" '
                print(statement)
                cur.execute(statement)
                for row in cur:
                    bar_infor.append(row)
                return(bar_infor)
            else:
                statement += ' DESC Limit 10'
                print(statement)
                cur.execute(statement)
                for row in cur:
                    bar_infor.append(row)
                return(bar_infor)
    else:
        statement += " FROM Bars join Countries on Bars.CompanyLocationId= Countries.EnglishName"
        if "cocoa" in i:
            statement += " GROUP BY Countries.Region"
            statement += ' HAVING COUNT(Bars.SpecificBeanBarName) > 4'
            statement += " ORDER BY round(AVG(Bars.CocoaPercent),2) "
            if "bottom" in i:
                statement += '  Limit "' + str(bottom) + '" '
                print(statement)
                cur.execute(statement)
                for row in cur:
                    bar_infor.append(row)
                return(bar_infor)
            elif "top" in i:
                statement += ' DESC Limit "' + str(top) + '" '
                print(statement)
                cur.execute(statement)
                for row in cur:
                    bar_infor.append(row)
                return(bar_infor)
            else:
                statement += ' DESC Limit 10'
                print(statement)
                cur.execute(statement)
                for row in cur:
                    bar_infor.append(row)
                return(bar_infor)
        elif "bars_sold" in i:
            statement += " GROUP BY Countries.Region"
            statement += ' HAVING COUNT(Bars.SpecificBeanBarName) > 4'
            statement += ' ORDER BY COUNT(Bars.SpecificBeanBarName)'
            if "bottom" in i:
                statement += ' Limit "' + str(bottom) + '" '
                print(statement)
                cur.execute(statement)
                for row in cur:
                    bar_infor.append(row)
                return(bar_infor)
            elif "top" in i:
                statement += ' DESC Limit "' + str(top) + '" '
                print(statement)
                cur.execute(statement)
                for row in cur:
                    bar_infor.append(row)
                return(bar_infor)
            else:
                statement += ' DESC Limit 10'
                print(statement)
                cur.execute(statement)
                for row in cur:
                    bar_infor.append(row)
                return(bar_infor)
        else:
            statement += " GROUP BY Countries.Region "
            statement += ' HAVING COUNT(Bars.SpecificBeanBarName) > 4'
            statement += ' ORDER BY round(AVG(Bars.Rating),2)'
            if "bottom" in i:
                statement += '  Limit "' + str(bottom) + '" '
                print(statement)
                cur.execute(statement)
                for row in cur:
                    bar_infor.append(row)
                return(bar_infor)
            elif "top" in i:
                statement += ' DESC Limit "' + str(top) + '" '
                print(statement)
                cur.execute(statement)
                for row in cur:
                    bar_infor.append(row)
                return(bar_infor)
            else:
                statement += ' DESC Limit 10'
                print(statement)
                cur.execute(statement)
                for row in cur:
                    bar_infor.append(row)
                return(bar_infor)



#print(region_return())

#command = input("type commands like companies region=Asia bars_sold ")

def process_command(command):
    s = command.split()
    for i in s:
        if "bars" in i:
            print("using bars")
            return(bars_return(command))
        elif "countries" in i:
            print("using countries")
            return(countries_return(command))
        elif "companies" in i:
            print("using companies")
            return(companies_return(command))
        elif "regions" in i:
            print("using region")
            return(region_return(command))



#print("this is the output of process_commad")

#print(process_command(command="bars sourceregion=Africa ratings top=5"))


def load_help_text():
    with open('help.txt') as f:
        return f.read()

#Part 3: Implement interactive prompt. We've started for you!
def interactive_prompt():
    help_text = load_help_text()
    command = ''

    while(True):
        command = str(input('Enter a command: '))
        s = command.split()
        print(s)
        try:
            if command == "help":
                print(load_help_text())
            elif command =="exit":
                print("bye")
                break

            elif "bars" == s[0]:
                print("using bars")
                for i in bars_return(command):
                    i = list(i)
                    for s in i:
                        if type(s) != str:
                            #print("type is not string ")
                            pass
                        elif len(s)>20:
                            #print(i)
                            inde = i.index(str(s))
                            i[inde] = s[:13] + "..."
                            #print(i)
                            #print("type is long string ")
                        else:
                            s = s[:20]
                            #print("type is string ")
                    print("{:<20}          {:<20}          {:<20}          {:<20}          {:<20}          {:<20}".format(i[0],i[1],i[2],i[3],i[4],i[5]))
            elif "countries" == s[0]:
                print("using countries")
                #print(countries_return(command))
                for i in countries_return(command):
                    i = list(i)
                    for s in i:
                        if type(s) != str:
                            pass
                        elif len(s)>20:
                            inde = i.index(str(s))
                            i[inde] = s[:13] + "..."
                        else:
                            s = s[:20]
                    print("{:<20}          {:<20}          {:<20}".format(i[0],i[1],i[2]))

            elif "companies" == s[0]:
                print("using companies")
                #print(companies_return(command))
                for i in companies_return(command):
                    i = list(i)
                    for s in i:
                        if type(s) != str:
                            #print("type is not string ")
                            pass
                        elif len(s)>20:
                            #print(i)
                            inde = i.index(str(s))
                            i[inde] = s[:13] + "..."
                            #print(i)
                            #print("type is long string ")
                        else:
                            s = s[:20]
                            #print("type is string ")
                    print("{:<20}          {:<20}          {:<20}".format(i[0],i[1],i[2]))

            elif "regions" == s[0]:
                print("using region")
                #print(region_return(command))
                for i in region_return(command):
                    i = list(i)
                    for s in i:
                        if type(s) != str:
                            #print("type is not string ")
                            pass
                        elif len(s)>20:
                            #print(i)
                            inde = i.index(str(s))
                            i[inde] = s[:13] + "..."
                            #print(i)
                            #print("type is long string ")
                        else:
                            s = s[:20]
                            #print("type is string ")

                    print("{:<20}          {:<20}".format(i[0],i[1]))
            else:
                print("commands is wrong")


        except:
            print("command is wrong")




            #command = input('Enter a command: ')







# Make sure nothing runs or prints out when this file is run as a module
if __name__=="__main__":
    interactive_prompt()
