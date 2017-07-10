__author__ = 'Tien'
import sys

def update_product():
    try:
        datas = readXlsx("/tmp/Approved.xlsx", sheet=1, header=True)
        cover_price = "cover_price"
        pub_year = "pub_year"
        for data in datas:
            if len(data.keys()) > 0:
                product = db(db.clsb_product.product_code == data['product_code']).select()
                if len(product) > 0:
                    product_id = product.first()['id']
                    db(db.clsb_product.id == product_id).update(product_title=data['product_title'],
                                                                product_price=int(data['product_price']),
                                                                product_status="Pending")
                    # update cover_price
                    metadata_cover_price = db(db.clsb_dic_metadata.metadata_name == cover_price).select.first()['id']
                    check_cover_price = db(db.clsb_product_metadata.product_id == product_id)\
                            (db.clsb_product_metadata.metadata_id == metadata_cover_price).select()
                    if len(check_cover_price) > 0:
                        db(db.clsb_product_metadata.product_id == product_id)\
                            (db.clsb_product_metadata.metadata_id == metadata_cover_price).update(metadata_value=data['cover_price'])
                    else:
                        db.clsb_product_metadata.insert(product=product_id,
                                                        metadata_id=metadata_cover_price,
                                                        metadata_value=data['cover_price'])
                    #update pub_year
                    metadata_pub_year = db(db.clsb_dic_metadata.metadata_name == pub_year).select.first()['id']
                    check_pub_year = db(db.clsb_product_metadata.product_id == product_id)\
                            (db.clsb_product_metadata.metadata_id == metadata_pub_year).select()
                    if len(check_pub_year):
                        db(db.clsb_product_metadata.product_id == product_id)\
                            (db.clsb_product_metadata.metadata_id == metadata_pub_year).update(metadata_value=data['publish_year'])
                    else:
                        db.clsb_product_metadata.insert(product=product_id,
                                                        metadata_id=metadata_pub_year,
                                                        metadata_value=data['publish_year'])
        return dict(product=datas)
    except Exception as err:
        return dict(error=str(err) + " on line " + str(sys.exc_traceback.tb_lineno))

def readXlsx(fileName, **args):

    import zipfile
    from xml.etree.ElementTree import iterparse

    if "sheet" in args:
       sheet = args["sheet"]
    else:
       sheet = 1
    if "header" in args:
       isHeader = args["header"]
    else:
       isHeader=False

    rows = []
    row = {}
    header = {}
    z = zipfile.ZipFile(fileName)

    # Get shared strings
    strings = [ el.text for e, el
                        in  iterparse( z.open( 'xl/sharedStrings.xml' ) )
                        if el.tag.endswith( '}t' )
                        ]
    #print(strings)
    value = ''
    for e, el in iterparse( z.open( 'xl/worksheets/sheet%d.xml'%( sheet ) ) ):
       # get value or index to shared strings
       if el.tag.endswith( '}v' ):                                   # <v>84</v>
           value = el.text
       if el.tag.endswith( '}c' ):                                   # <c r="A3" t="s"><v>84</v></c>

           # If value is a shared string, use value as an index
           if el.attrib.get( 't' ) == 's':
               value = strings[int( value )]

           # split the row/col information so that the row leter(s) can be separate
           letter = el.attrib['r']                                   # AZ22
           while letter[-1].isdigit():
               letter = letter[:-1]

           # if it is the first row, then create a header hash for the names
           # that COULD be used
           if rows ==[]:
               header[letter]=value
           else:
               if value != '':

                   # if there is a header row, use the first row's names as the row hash index
                   if isHeader == True and letter in header:
                       row[header[letter]] = value
                   else:
                       row[letter] = value

           value = ''
       if el.tag.endswith('}row'):
           rows.append(row)
           row = {}
    z.close()
    return rows

def update_title():
    import csv
    try:
        data = list()
        with open('/tmp/title update.csv', mode='r') as infile:
            reader = csv.reader(infile)
            for row in reader:
                try:
                    data.append(str(row).split("\t")[0])
                except Exception as err:
                    data.append(err)
        return dict(data=data)
    except Exception as err:
        return dict(error=str(err) + " on line " + str(sys.exc_traceback.tb_lineno))

def update_title_txt():
    try:
        data = list()
        f = open("/tmp/title update.txt",'r')
        out = f.readlines()
        title = ""
        for line in out:
            str_line = line.split("|")
            temp = dict()
            temp['id'] = str_line[0]
            temp['title'] = str_line[1]
            title = str_line[1]
            data.append(temp)
            db(db.clsb_product.id == str_line[0], 'utf-8').update(product_title=unicode(str_line[1], 'utf-8'))
        return dict(data=data)
    except Exception as err:
        return dict(error=str(err) + " on line " + str(sys.exc_traceback.tb_lineno), title=title)
		

def classbook_windows():
    try:
        #msgs = list()
        msg1 = dict()
        msg1['version'] = '1.0.0'
        msg1['build'] = '20150715.01'
        msg1['link'] = 'http://app.classbook.vn/static/Classbook.exe'
        msg1['message'] = ''
        #msgs.append(msg1)
        return dict(updateinfo=msg1)
    except Exception as ex:
        raise HTTP(500, "Bad request " + ex.message)
