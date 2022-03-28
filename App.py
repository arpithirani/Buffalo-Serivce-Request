import csv
import datetime


#readCSV
def readCSV(filename):
  ret_val=[]
  with open(filename, newline='', encoding="utf-8") as f:
    reader=csv.reader(f)
    header=next(reader)
    for line in reader:
      count=0
      dic={}
      for element in line:
        dic[header[count]]=line[count]
        count+=1
      ret_val.append(dic)
  return ret_val     


ALL_DATA=readCSV('311_Service_Requests_small.csv')


#writeCSV
def writeCSV(filename, list_of_dictionaries):
  with open(filename,'w') as f:
    writer=csv.writer(f)
    writer.writerow(list_of_dictionaries[0].keys())
    for dic in list_of_dictionaries:
      writer.writerow(dic.values())
  return None


#keepOnly
def keepOnly(list_of_dictionaries, key, value):
  final=[]
  for pair in list_of_dictionaries:
    for k in pair.keys():
      if k == key:
        for v in pair.values():
          if v == value:
            pair[k]=v
            final.append(pair)
  return final


#discardOnly
def discardOnly(list_of_dictionaries, key, value):
  val=[]
  for dic in list_of_dictionaries:
    if dic[key] != value:
      val.append(dic) 
  return val      
  

#filterRange
def filterRange(list_of_dictionaries, key, low, high):
  end=[]
  for d in list_of_dictionaries:
    if low <= d[key] < high:
      end.append(d)
  return end


#duration
def duration(date1,date2):
  diff=date2-date1
  return diff.days


#App.departments function 
def departments(list_of_dictionaries):
  sub=[]
  for dic in list_of_dictionaries:
    for key in dic.keys():
      if key == "SUBJECT":
        if dic[key] not in sub:
          sub.append(dic[key])
  sub.sort()
  return sub


#App.open_year function  
def open_year(dictionary):
  for key in dictionary.keys():
    if "OPEN DATE" == key:
      year=dictionary[key][6:10]
  return year


#App.filterYear function
def filterYear(list_of_dictionaries, low, high):
  tot=[]
  for d in list_of_dictionaries:
    if int(low) <= int(open_year(d)) < int(high):
      tot.append(d)
  return tot


#App.date function 
def date(string):
  y=int(string[6:10])
  m=int(string[0:2])
  d=int(string[3:5])
  dt=datetime.date(y,m,d)
  return dt


#App.data_by_subject function
def data_by_subject(dic):
  ret_val=[]
  start= dic["year_start"]
  end= dic["year_end"]
  tot_dept= departments(ALL_DATA)
  req_data=filterYear(ALL_DATA,start,end+1)
  dom=0
  for each_year in range(start,end+1):
    yearly_data=[]
    for dic in req_data:
      if open_year(dic) == str(each_year):
        yearly_data.append(dic)
    values=[]
    if len(yearly_data)>0:
      for d in tot_dept:
        dept=keepOnly(yearly_data,"SUBJECT",d)
        avg = int( 100*round(len(dept)/len(yearly_data), 2))
        values.append(avg)
    if len(values)>0:
      chart={"values" : values, "labels" : tot_dept, "domain" : {"column" : dom}, "name" : str(each_year), "hole" : .4, "type" : 'pie'}
      ret_val.append(chart)
    dom+=1
  return ret_val


#App.data_by_subject_duration function
def data_by_subject_duration(dictionary):
  ret_val = []
  year = dictionary['year']
  req_data = filterYear(ALL_DATA, year, year+1)
  need_data = discardOnly(req_data, 'STATUS', 'Open')
  dept = departments(ALL_DATA)
  val = []
  for dct in need_data:
    start = date(dct['OPEN DATE'])
    end = date(dct['CLOSED DATE'])
    dur = duration(start, end)
    val.append(dur)
  val_x=[]
  if len(val)<=0:
    val_x.append(0)
  else:
    mx=max(val)
    for r in range(mx+1):
      val_x.append(r)
  for d in dept:
    dept_list = keepOnly(need_data, 'SUBJECT', d)
    mx_y=[]
    for dt in dept_list:
      du = duration(date(dt['OPEN DATE']), date(dt['CLOSED DATE']))
      mx_y.append(du)
    val_y=[]
    for num in val_x:
      count = mx_y.count(num)
      val_y.append(count)
    final_dic = {"x": val_x, "y": val_y, "name": d, "mode": 'markers', "type": 'scatter'}
    ret_val.append(final_dic)
  return ret_val