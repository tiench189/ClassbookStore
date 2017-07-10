__author__ = 'Tien'
fh = open("/var/log/apache2/access.log", "r")
count = 0
str_find = "/static/ClassbookAppSS.apk"
arr_lines = fh.readlines()
for line in arr_lines:
    if str_find in line:
        count += 1
fh.close()
print("find in file: " + str(count))