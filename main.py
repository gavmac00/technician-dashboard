import time # measures program's speed and performance
import statistics # calculates the mean of repair dates interval

import pandas as pd  # read csv, df manipulation
import streamlit as st  # web development

from PIL import Image # displays images
from datetime import datetime, timedelta # using datetime objects

# streamlit page config
st.set_page_config(page_title='Real-Time Data Science Dashboard',
                   page_icon='i',
                   layout='wide')

# functions
def convert_to_string(delta):
  days = delta.days
  hours, remainder = divmod(delta.seconds, 3600)
  minutes, seconds = divmod(remainder, 60)
  return '{} days {:02}:{:02}:{:02}'.format(days, hours, minutes, seconds)

def convert_to_days(time_string):
  parts = time_string.split(' ')
  days = int(parts[0].strip().strip('days'))
  delta = timedelta(days=days)
  return delta.days

def getLocation():
  count = 0
  with open('individ_testdata.csv') as file:
    for line in file:
      try:
        latitude = int(line.split(',')[7])
        print(f"lat: {latitude}")
        longitude = int(line.split(',')[8])
      except:
        continue
      if count == 1:
        return latitude, longitude
      count += 1

def formDatesList():
  count = 0
  DatesList = []
  with open('individ_testdata.csv') as file:
    for line in file:
      date = line.split(',')[4]
      count += 1
      if count == 2:
        date = datetime.strptime(date, '%d/%m/%Y')
        DatesList.append(date)
      elif count > 2:
        date = datetime.strptime(date, '%d/%m/%Y')
        DatesList.append(date)
        DatesList.append(date)

  DatesList.append(datetime.now())

  return DatesList, count

def formDaysList(DatesList):
  DaysList = []
  for i in range(len(DatesList)):
    if i == 0:
      DaysList.append(0)
      continue
    if i > 0:
      current_date = DatesList[i]
      previous_date = DatesList[i - 1]
      difference = current_date - previous_date
      difference = str(difference)
      days = difference.split(' ')[0]
      try:
        days = int(days)
      except:
        days = 0

    DaysList.append(days)

  return DaysList

def formExpectedList(DaysList):
  ExpectedList = []
  NonNegDaysList = []
  for i in range(len(DaysList)):
    numdays = DaysList[i]
    if numdays != 0:
      NonNegDaysList.append(numdays)

  avgdays = statistics.mean(NonNegDaysList)

  for i in range(len(DaysList)):
    ExpectedList.append(avgdays)

  return ExpectedList

# Lists formation
DatesList, numRepairs = formDatesList()
DaysList = formDaysList(DatesList)
ExpectedList = formExpectedList(DaysList)

start = time.time()

# read in csv
df = pd.read_csv("individ_testdata.csv")

# Get Today's date as a DateTime object
today = datetime.now()
formatted_date = today.strftime("%Y-%m-%d")
datetime_object = datetime.strptime(formatted_date, "%Y-%m-%d")

# Find average time between repair dates
avg_reliability = int(round(ExpectedList[0], 0))
estimated_repair_date = DatesList[-2] + timedelta(days=avg_reliability)
estimated_repair_date = datetime.strftime(estimated_repair_date, '%d/%m/%Y')

# last repair date (col2)
last_repair = DatesList[-2]
last_repair = datetime.strftime(last_repair, '%d/%m/%Y')

# no repairs (col5)
no_repairs_str = numRepairs

# dashboard titles and headings
st.header('SEW Service Dashboard')
st.subheader(f":red[{'Driving the world.'}]")
now = datetime.now()
now = now.strftime("%H:%M")
time_now = f"Last Updated at {now}"
st.caption(time_now)

# divider
st.markdown("<hr style='background-color:black;'>", unsafe_allow_html=True)
# ---------------------------------------------------------------------------

col1, col2, col3 = st.columns(3)

with col1:
  st.subheader('Serial ID:')
  st.subheader(f":blue[{df['productID'][0]}]")

with col2:
  st.subheader("Last Repair Date:")
  st.subheader(f":blue[{last_repair}]")

with col3:
  st.subheader("Mean Time Between Maintenance:")
  st.subheader(f":blue[{avg_reliability} Days ({int(round(avg_reliability/7,0))} Weeks)]")

col4, col5, col6 = st.columns(3)

with col4:
  st.subheader('Customer Name and Location: ')
  st.subheader(f":blue[{df['customer'][0] + ', ' + df['address'][0]}]")

with col5:
  st.subheader("No. Repairs To Date:")
  st.subheader(f":blue[{no_repairs_str}]")

with col6:
  st.subheader('Estimated Next Repair Date:')
  st.subheader(f":blue[{estimated_repair_date}]")

# divider
st.markdown("<hr style='background-color:black;'>", unsafe_allow_html=True)
# ---------------------------------------------------------------------------

#SECTION 2: Graph

# DataFrame formation
dfg = pd.DataFrame({
  'Dates': DatesList,
  'Current Lifetime': DaysList,
  'Expected Lifetime': ExpectedList
})
dfg.columns = ['Dates', 'Current Lifetime', 'Expected Lifetime']

# Setting the first column as index, important
dfg.set_index('Dates', inplace=True)

# Plotting a line chart
st.line_chart(dfg)

# divider
st.markdown("<hr style='background-color:black;'>", unsafe_allow_html=True)
# ---------------------------------------------------------------------------

#SECTION 3: Diagnosis Information

col9, col12 = st.columns(2)

with col9:

  # left column
  tab1, tab2 = st.tabs(["Metrics", "Customer Data"])
  avg_reliability_change = 1.2

  tab1.header(':red[Metrics]')
  tab1.metric(label="Average Reliability",
              value=avg_reliability,
              delta=avg_reliability_change)

  z_url = "https://kth-se.zoom.us/j/4103788683"
  m_url = "https://www.microsoft.com/en-ie/microsoft-teams/"
  o_url = "https://oculavis.de/en/home/"

  if tab1.button('Schedule Maintenance Call'):
    tab1.markdown(
      f'''<a href={z_url}><button style="border-radius: 10px; padding: 5px 10px;color:white;background-color:#295bfc;">Zoom Call</button></a>''',
      unsafe_allow_html=True)
    tab1.markdown(
      f'''<a href={m_url}><button style="border-radius: 10px; padding: 5px 10px;color:white;background-color:#4f52ba;">Teams Call</button></a>''',
      unsafe_allow_html=True)
    tab1.markdown(
      f'''<a href={o_url}><button style="border-radius: 10px; padding: 5px 10px;color:white;background-color:#43b2a1;">Oculavis Call</button></a>''',
      unsafe_allow_html=True)
  tab2.header('Customer')
  customer_logo = Image.open('images/dublin-airport-logo.png')
  tab2.image(customer_logo)
  customer_info = 'Dublin Airport is one of the largest and busiest airports in Ireland, serving as the main hub for Aer Lingus and Ryanair. It is located approximately 10 kilometers north of Dublin city center and handles over 31 million passengers annually. The airport offers a wide range of facilities, including shopping and dining options, duty-free shopping, and free Wi-Fi. There are two terminals, Terminal 1 and Terminal 2, which handle both domestic and international flights. The airport has good transport links, including bus, train, and taxi services, making it easily accessible from the city center and surrounding areas.'
  tab2.write(customer_info)

  # customer map
  try:
    latitude, longitude = getLocation()
    print("getLocation worked.")
  except:
    latitude, longitude = (53.42306, -6.24472)
  data = {'latitude': [latitude], 'longitude': [longitude]}
  coords = pd.DataFrame(data)
  tab2.map(coords, 12)

  # data entry here for updates by active technician (perhaps during teams call)
  name_label = 'Name:'
  date_label = 'Add Maintenance Date (dd/mm/yyyy):'
  current_technician = tab1.text_input(name_label)
  if current_technician:
    tab1.write(f"Hello {current_technician}")
  new_repair = tab1.text_input(date_label)
  if new_repair:
    new_repair = datetime.strptime(new_repair, '%d/%m/%Y')
    print(f"new_repair: {new_repair}")
    DatesList.append(new_repair)

    DaysList = formDaysList(DatesList)
    # print(f"DaysList: {DaysList}\n\n")
    ExpectedList = formExpectedList(DaysList)

    old_avg_reliability = avg_reliability
    avg_reliability = ExpectedList[0]

  audio_upload = tab1.file_uploader('Upload Machine Data', '.xml')
  if audio_upload is not None:
    # Save the file to disk
    with open("audio_upload.xml", "wb") as f:
      f.write(audio_upload.read())
    st.write("SEW Technician has received your file!")

with col12:

  # Product Specific Information
  image = Image.open('images/gearmotor.png')
  st.subheader('Product Image:')
  st.image(image)
  with st.expander("Product Details:"):
    model = df['type'][0]
    product = df['productID'][0]
    st.write(f"{'Model ID: ' + model}")
    st.write(f":white[{'Serial ID: ' + product}]")
    text = 'The electrogearbox is a compact and efficient gear motor solution for the industry. The ' + model + ' is designed for use in a variety of applications, offering reliable and \nsmooth operation for demanding environments. The ' + model + ' version is equipped with advanced features to meet the specific needs of industrial applications. As an SEW technician, you should be familiar with the features \nand capabilities of the Electrogearbox, as it is a common product used in a wide range of industrial applications.'
    st.write(text)
    customer_image = Image.open('images/customer_image.png')
    st.subheader('Customer Configuration:')
    last_visit = DatesList[-1].strftime('%d/%m/%Y')
    last_technician = 'Thorsten Schmidt'
    st.caption(f'Image taken by {last_technician} on {last_visit}:')
    st.image(customer_image)
    image_location = 'Heavy Duty Goods, Gate 301, Runway 2, Dublin Airport'
    st.caption(f"Location: {image_location}")

# divider
st.markdown("<hr style='background-color:black;'>", unsafe_allow_html=True)
# ---------------------------------------------------------------------------
end = time.time()
total_time = round(end - start, 3)
print(f"Total Time: {total_time} seconds")
