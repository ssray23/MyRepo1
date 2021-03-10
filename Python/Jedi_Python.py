# Jedi Store Model

# Configuration
import time
import threading
import datetime
import csv
# commented pymysql below, replaced with mysql.connector
# import pymysql
import mysql.connector

tlogfilename = "Jedi.csv"

# Initialise Database Connection and Cursor
print("Initialising Database Connector")
print("Database Connector loaded")
print("Connecting to Database")
mydb = mysql.connector.connect(
	host="localhost",
	user="root",
	passwd="root",
	database="jedi",
	autocommit=True
)
print(mydb)
print("Connected to Database")
print("Getting a cursor")
# Had to specify buffered clause else  cur variable was not able to execute the INSERT statement later on...
cur = mydb.cursor(buffered=True)
print("Got a cursor")
print("Connected to Database")
print("Getting a cursor")

# Clear and Load TLOG into DB
print("Clearing previous TLOG in DB")
cur.execute("SELECT COUNT(*) FROM tlog")
result = cur.fetchone()
print("Previous records:")
print(result[0])
cur.execute("DELETE FROM tlog")
cur.execute("SELECT COUNT(*) FROM tlog")
print("Loading TLOG into DB")
print("Loading " + tlogfilename)
with open(tlogfilename) as tlogfile:
	csv_reader = csv.reader(tlogfile, delimiter=',')
	line_count = 0
	for row in csv_reader:
		if line_count > 0:
			statement = "INSERT INTO tlog (order_time,order_id,product_id) VALUES (" + \
				row[0]+","+row[1]+","+row[2]+")"
			print(statement)
			cur.execute(statement)
			mydb.commit()
		line_count += 1
tlogfile.close()
cur.execute("SELECT COUNT(*) FROM tlog")
result = cur.fetchone()
print("Records Loaded:")
print(result[0])

# record the remaining tables

# Clear and Load product into DB
productfilename = "product.csv"
print("Clearing previous product in DB")
cur.execute("SELECT COUNT(*) FROM product")
result = cur.fetchone()
print("Previous records:")
print(result[0])
cur.execute("DELETE FROM product")
cur.execute("SELECT COUNT(*) FROM product")
print("Loading product into DB")
print("Loading " + productfilename)
with open(productfilename) as productfile:
	csv_reader = csv.reader(productfile, delimiter=',')
	line_count = 0
	for row in csv_reader:
		if line_count > 0:
			statement = "INSERT INTO product (id,name,storage,per_tote) VALUES (" + \
				row[0]+","+row[1]+","+row[2]+","+row[3]+")"
			print(statement)
			cur.execute(statement)
			mydb.commit()
		line_count += 1
productfile.close()
cur.execute("SELECT COUNT(*) FROM product")
result = cur.fetchone()
print("Records Loaded:")
print(result[0])

# Forecast Default Products based on TLOG in Forecast Table (can replace manually)
print("Clearing previous Forecasts in DB")
cur.execute("SELECT COUNT(*) FROM forecast")
result = cur.fetchone()
print("Previous records:")
print(result[0])
cur.execute("DELETE FROM forecast")
mydb.commit()
statement = "INSERT INTO forecast (product_id,forecast_qty) (SELECT product_id,count(product_id) FROM tlog GROUP BY product_id ORDER BY 2 DESC)"
cur.execute(statement)
mydb.commit()
cur.execute("SELECT count(*) from forecast")
result = cur.fetchone()
print("Forecasts Loaded:")
print(result[0])
cur.execute("SELECT * from forecast")
result = cur.fetchall()
print("Forecast Details:")
print(result)

# Update Products with Products-per-tote value (can replace manually)
statement = "UPDATE product SET per_tote = 10"
cur.execute(statement)
mydb.commit()

# Load Inventory in Rack Totes based on TLOG
# Loop through TLOG and insert a new Tote with either max of Product or product per tote
# If any product inventory left after product_per_tote, then insert a new Tote and repeat until TLOG quantity is zero
# Inventory is not a problem in this model as you should never get an order for stock you don't have
print("Clearing previous Inventory Totes in DB")
cur.execute("SELECT COUNT(*) FROM inventory_tote")
result = cur.fetchone()
print("Previous records:")
print(result[0])
cur.execute("DELETE FROM inventory_tote")
mydb.commit()

insert_counter = 0
cur.execute("SELECT product_id,count(product_id) FROM tlog GROUP BY product_id")
result = cur.fetchall()
for row in result:
	total_inventory = row[1]
	statement = ("SELECT per_tote FROM product WHERE id="+str(row[0]))
	cur.execute(statement)
	miniresult = cur.fetchone()
	per_tote = miniresult[0]
	if total_inventory <= per_tote:
		insert_counter += 1
		statement = ("INSERT INTO inventory_tote (id,product_id,quantity) VALUES (" +
					 str(insert_counter)+","+str(row[0])+","+str(total_inventory)+")")
		print(statement)
		cur.execute(statement)
	else:
		while total_inventory > 0:
			insert_counter += 1
			if total_inventory >= per_tote:
				statement = ("INSERT INTO inventory_tote (id,product_id,quantity) VALUES (" +
							 str(insert_counter)+","+str(row[0])+","+str(per_tote)+")")
			else:
				statement = ("INSERT INTO inventory_tote (id,product_id,quantity) VALUES (" +
							 str(insert_counter)+","+str(row[0])+","+str(total_inventory)+")")
			print(statement)
			cur.execute(statement)
			total_inventory -= per_tote
mydb.commit()

# Clear Locations
print("Clearing previous Racks in DB")
cur.execute("SELECT COUNT(*) FROM location WHERE bay=0")
result = cur.fetchone()
print("Previous Total Rack locations:")
print(result[0])
cur.execute("SELECT COUNT(*) FROM location WHERE bay>0")
result = cur.fetchone()
print("Previous Total Bay locations:")
print(result[0])
cur.execute("DELETE FROM location")
mydb.commit()

# Create Bays
print("Creating Bays - empty for now")
insert_counter = 0
bay_count = 5
totes_per_bay = 4
for bayloop in range(bay_count):
	bayloop += 1
	for toteloop in range(totes_per_bay):
		insert_counter += 1
		statement = ("INSERT INTO location (id,bay,tote) VALUES (" +
					 str(insert_counter)+","+str(bayloop)+",0)")
		print(statement)
		cur.execute(statement)
mydb.commit()

# Create Racks and Fill
print("Creating Racks and filling them")
cur.execute("SELECT id, product_id, quantity FROM inventory_tote")
result = cur.fetchall()
for row in result:
	record_id = row[0]
	record_product = row[1]
	record_quantity = row[2]
	insert_counter += 1
	statement = ("INSERT INTO location (id,bay,tote) VALUES (" +
				 str(insert_counter)+",0,"+str(row[0])+")")
	print(statement)
	cur.execute(statement)
mydb.commit()

# Load Default Products by Tote into Bays, in order of Bays 1-5
# Assuming to bring one tote of each rather than multiple for higher forecast,
# as assume these have the opportunity to replenish in other tote locations if other products sell out
# Finding totes with the highest quantity contents (best for picking speed, not for rack space availability)
# Not explicitly supporting lot tracking yet
print("Moving highest forecast products from Racks to Bays (start-of-day, so immediate)")
cur.execute("SELECT min(id) FROM location WHERE bay=1")
result = cur.fetchone()
location_counter = result[0]
cur.execute("SELECT product_id FROM forecast ORDER BY forecast_qty DESC")
result = cur.fetchall()
for row in result:
	record_product = row[0]
	# Update Tote's location in Bay 1
	statement = ("UPDATE location SET tote = (SELECT id from inventory_tote WHERE product_id=" +
				 str(record_product)+" ORDER BY quantity DESC LIMIT 1) WHERE id = "+str(location_counter))
	print(statement)
	cur.execute(statement)

	# Added by Suddha
	# Clean up Rack location (as tote has moved from Rack location to Bay location)
	# Fetch tote which just got moved to Bay
	cur.execute("SELECT tote FROM location WHERE id = " + str(location_counter))
	current_tote = cur.fetchone()[0]
	# Fetch id of the rack location where tote was present before it moved to Bay
	cur.execute("SELECT id FROM location WHERE tote = " + str(current_tote) + " AND bay=0")
	rack_location = cur.fetchone()[0]
	# Empty this rack location (i.e. as tote not present in rack as it was moved to bay)
	cur.execute("UPDATE location SET tote = 0 WHERE id = " + str(rack_location))
	# End Added by Suddha

	location_counter += 1

mydb.commit()

# Creating Customer Orders from TLOG in Orders table
# Match timings in TLOG table to current time in second column (becomes priamry for order time)
# Timeshift first order to one min from now, and timeshift the rest according to their original delta from first
print("Clearing previous Customer Orders in DB")
cur.execute("SELECT COUNT(*) FROM orders")
result = cur.fetchone()
print("Previous records:")
print(result[0])
cur.execute("DELETE FROM orders")
cur.execute("DELETE FROM order_pick")
mydb.commit()
print("Creating Customer Orders from TLOG and giving them a time to start, 1 min from now")
rightnow = datetime.datetime.now()
rightnowformatted = rightnow.strftime('%Y-%m-%d %H:%M:%S')
print("Time right now is " + rightnowformatted)
timedelta = rightnow + datetime.timedelta(seconds=60)
timedeltaformatted = timedelta.strftime('%Y-%m-%d %H:%M:%S')
print("Orders will start at "+str(timedeltaformatted))
cur.execute("SELECT MIN(order_time) FROM tlog")
firstorder = cur.fetchone()
firstorderdate = firstorder[0]
firstorderformatted = firstorderdate.strftime('%Y-%m-%d %H:%M:%S')
print("The first order was actually at "+str(firstorderformatted))
cur.execute(
	"SELECT MIN(order_time), order_id FROM tlog GROUP BY order_id ORDER BY order_time ASC")
result = cur.fetchall()
for row in result:
	record_order_time = row[0]
	record_order_id = row[1]
	print("Processing the order that was at time " + str(record_order_time))
	orderdelta = record_order_time - firstorderdate
	print(orderdelta)
	print("The offset from the first order was " + str(orderdelta))
	newordertime = timedelta + orderdelta
	newordertimeformatted = newordertime.strftime('%Y-%m-%d %H:%M:%S')
	print("The new time for that order will be " + newordertimeformatted)
	statement = ("INSERT INTO orders (id,time,system_time) VALUES ("+str(record_order_id) +
				 ",'"+str(record_order_time)+"','"+str(newordertimeformatted)+"')")
	print(statement)
	cur.execute(statement)
	statement = ("INSERT INTO order_pick(order_id,product_id,required_qty) SELECT t.order_id,t.product_id,COUNT(t.order_id) FROM tlog t WHERE t.order_id = " +
				 str(record_order_id)+" GROUP BY t.product_id;")
	print(statement)
	cur.execute(statement)

# Temp Code added by Suddha to test scenario where tote may have addtional units of a product on top of those coming from the tlog.
# Inflate Tote 3 by 5 more units of Product 1235. After order processing, these 5 units should remain in Tote 3.
# cur.execute("UPDATE inventory_tote SET quantity = quantity + 5 WHERE id = 3 AND product_id = 1235")
# End Temp Code
# Temp Code added by Suddha to test scenario where tote may have less units than the units required coming from the tlog.
# Reduce Tote 3 by 2 units for Product 1235. After order processing, picked_qty < required_qty in order_pick and status shud remain In Progress
# cur.execute("UPDATE inventory_tote SET quantity = quantity -2 WHERE id = 3 AND product_id = 1235")
# End Temp Code
mydb.commit()

# Log Run ID value as current timestamp
print("Logging this run")
rightnow = datetime.datetime.now()
rightnowformatted = rightnow.strftime('%Y%m%d%H%M%S')
runid = rightnowformatted
print("Time right now is " + str(rightnow) + " so making Run ID " + runid)

###############
# Initialise Robots - insert 5 if none are in the table
print("Checking for robots")
cur.execute("SELECT count(*) FROM robot")
robotcount = cur.fetchone()
print(robotcount[0])
defaultrobots = 5
if robotcount[0] == 0:
	print("No robots found in database so adding default of " + str(defaultrobots))
	for robotloop in range(defaultrobots):
		robot = robotloop+1
		statement = (
			"INSERT INTO robot (id,status) VALUES ("+str(robot)+",'ready')")
		print(statement)
		cur.execute(statement)
else:
	print("Found "+str(robotcount[0])+" robots")
print("Setting all robot status to 'ready'")
cur.execute("UPDATE robot SET status='ready'")
mydb.commit()

# Added by Suddha
# Summarises the Bay, Tote and Qty before order run starts
def bay_tote_summary():
	print("")
	print("---------------------------- ")
	print("Printing Bay Summary ")
	print("---------------------------- ")
	baycursor = mydb.cursor(buffered=True)
	bay_count = 5
	for bayloop in range(bay_count):
		bayloop += 1
		print("BAY " + str(bayloop))
		print("------")
		baycursor.execute("SELECT t.id, t.product_id, t.quantity, l.bay FROM inventory_tote t \
								INNER JOIN location l ON t.id = l.tote WHERE l.bay = " + str(bayloop) + " ORDER by t.id")
		totes = baycursor.fetchall()
		if baycursor.rowcount > 0:
			for tote_rec in totes:
				print(" Tote " + str(tote_rec[0]) + " (Product " + str(tote_rec[1]) + " .. " + str(tote_rec[2]) + " units.)")
		else:
				print(" No Totes.")

	print("")


###############
# Start of threaded processes
#

###############
# Robot Controller - check for available robots and moves to process every second
# If so, process the move taking 1 min per move
#


def robot_controller(passedrobotarg):
	robotcur = mydb.cursor()
	while True:
		print("Checking for work for the Robots")
		robotcur.execute(
			"SELECT count(*) FROM robot_move_queue WHERE status='waiting'")
		robotwork = robotcur.fetchone()
		if robotwork[0] == 0:
			print("Robots have no work")
		else:
			print("ROBOTS HAVE WORK!!")
		time.sleep(2)
# TODO: Make robots actually do work


###############
# Bay Processor (Picker)
###############
pick_time = 2


def bay_processor(passedbayidarg):
	print("Bay Processor started for Bay: " + str(passedbayidarg))
	baycur = mydb.cursor()
	while True:
		print("Checking for work for the Bay Picker")
#		print("SELECT count(*) FROM run WHERE bay="+str(passedbayidarg))
		baycur.execute("SELECT count(*) FROM run WHERE bay=" +
					   str(passedbayidarg))
		baywork = baycur.fetchone()
		if baywork[0] == 0:
			print("Picker has no work in Bay "+str(passedbayidarg))
		else:
			print("PICKER HAS WORK IN BAY "+str(passedbayidarg))
		time.sleep(0.5)
# TODO: Make pickers actually do work

#################
# Order Processor
#################


def order_processor(passedorderidarg):
	# Update Order Run to Processing status and log start time
	# Find out which Products are in this order
	print("")
	print("-------------------------------------------------------------------------")
	print("Order processor is processing order number: " + str(passedorderidarg))
	print("-------------------------------------------------------------------------")
	orderproccur = mydb.cursor(buffered=True)
	orderproccur.execute(
		"SELECT product_id FROM order_pick WHERE order_id = " + str(passedorderidarg))
	print("Products in this Order: "+str(orderproccur.rowcount))
	orderproducts = orderproccur.fetchall()
	print(orderproducts)
	for orderproduct in orderproducts:
		# Find quantity customer needs
		orderproccur.execute("SELECT required_qty FROM order_pick WHERE order_id = " +
							 str(passedorderidarg)+" AND product_id = " + str(orderproduct[0]))
		orderproductrequiredqty = orderproccur.fetchone()
		if orderproductrequiredqty[0] > 0:
			print(" Customer needs: "+str(orderproductrequiredqty[0]) + " units of product_id = " + str(
				orderproduct[0]) + " for order_id " + str(passedorderidarg))
			
			# Identify all the totes this product is in, and choose one(s) to pull from
			# Added by Suddha
			#orderproccur.execute("SELECT t.id, t.product_id, t.quantity, l.bay FROM inventory_tote t INNER JOIN location l ON t.id = l.tote \
			#							WHERE t.product_id = " + str(orderproduct[0]) + "  ORDER by t.id")
			#totes = orderproccur.fetchall()
			#selected_totes = []
			# totes[0] is Tote ID
			# totes[1] is Product ID
			# totes[2] is Qty loaded in the tote for Product ID (based on forecast)
			# totes[3] is the Bay where the tote is placed

			#print("Totes, Qty and Bay for Product "+ str(orderproduct[0]))
			#for row in totes:
			#	selected_totes.append((row[0],row[2],row[3]))	
			#print(selected_totes)



	# Check if can move Order to next Bay
	# orderproccur.execute(
	#	"SELECT bay FROM run WHERE order_id = " + str(passedorderidarg))
	#currentordercurrentbay = orderproccur.fetchone()
	#print(currentordercurrentbay[0])
	#print("Current Bay for Order "+str(passedorderidarg) +
	#	  " is "+str(currentordercurrentbay[0]))

	# Move Customer Order to Bay 1 and pick available products (pick_time per product)
	# If Product not there yet (ie status is en route), wait (check every second) and then pick (pick_time per product)
	# Move Customer Order to Bay 2 and pick available products (pick_time per product)
	# If Product not there yet (ie status is en route), wait (check every second) and then pick (pick_time per product)
	# Move Customer Order to Bay 3 and pick available products (pick_time per product)
	# If Product not there yet (ie status is en route), wait (check every second) and then pick (pick_time per product)
	# Move Customer Order to Bay 4 and pick available products (pick_time per product)
	# If Product not there yet (ie status is en route), wait (check every second) and then pick (pick_time per product)
	# Move Customer Order to Bay 5 and pick available products (pick_time per product)
	# If Product not there yet (ie status is en route), wait (check every second) and then pick (pick_time per product)
	# Update Order Run to Complete status and log complete time
	print("")
	bay_count = 5
	for bayloop in range(bay_count):
		bayloop += 1
		print("BAY " + str(bayloop))
		print("-----------------------")
		# Fetch products in the current order
		orderproccur.execute("SELECT product_id, required_qty FROM order_pick \
										WHERE order_id = " + str(passedorderidarg))
		products = orderproccur.fetchall()
		for product_rec in products:
			# Check for a tote for the product in current Bay
			orderproccur.execute("SELECT t.id, t.quantity, l.bay, l.id FROM inventory_tote t INNER JOIN location l ON t.id = l.tote \
										WHERE t.product_id = " + str(product_rec[0]) + " AND t.quantity > 0 \
										    AND l.bay = " + str(bayloop) + " LIMIT 1")
			tote = orderproccur.fetchone()
			tote_found = orderproccur.rowcount
			# Found a tote for this product in current Bay
			if tote_found == 1:
				# Pick Required Qty
				print(" Product " + str(product_rec[0]) + " found in Tote " + str(tote[0]) + ". Starting to pick .. ",end= ' ' ) 
				time.sleep(3)
				# Decrement Tote inventory by Picked Qty
				orderproccur.execute("UPDATE inventory_tote SET quantity = quantity - " + str(product_rec[1])  + 
							" WHERE id = " + str(tote[0]) + " AND product_id = " + str(product_rec[0]))
				# If Tote is empty after picking, move back to Racks
				orderproccur.execute("SELECT quantity FROM inventory_tote where id = " + str(tote[0]) + " AND product_id = " + str(product_rec[0]))
				tote_qty = orderproccur.fetchone()
				#print("Tote Qty after picking = " + str(tote_qty[0]))
				if tote_qty[0] < 1:
					orderproccur.execute("UPDATE location SET tote = 0 WHERE id = " + str(tote[3]))
					orderproccur.execute("SELECT min(id) FROM location WHERE tote = 0 AND bay = 0")
					min_loc_rack = orderproccur.fetchone()
					orderproccur.execute("UPDATE location SET tote = " + str(tote[0]) + " WHERE id = " + str(min_loc_rack[0]))
					# Time for tote to move back to Bay 0 (rack)
					#time.sleep(3)
				# Update order_pick for this product
				orderproccur.execute("UPDATE order_pick SET picked_qty = IFNULL(picked_qty,0) + " + str(product_rec[1])  + 
					" WHERE product_id = " + str(product_rec[0]) + " AND order_id = " + str(passedorderidarg))
				print("Pick completed." ) 
			else:
				print(" Product " + str(product_rec[0]) + " not found." ) 

	# Update Run Table for this order
	# Fetch sum of required_qty vs picked_qty from order_pick for this order
	orderproccur.execute("SELECT SUM(required_qty), SUM(picked_qty) FROM order_pick GROUP BY order_id HAVING order_id = " +  str(passedorderidarg))
	orderqtys = orderproccur.fetchone()
	# print("Required Qty = " + str(orderqtys[0]))
	# print("Picked Qty = " + str(orderqtys[1]))
	orderendtime = datetime.datetime.now()
	orderendtimeformatted = orderendtime.strftime('%Y-%m-%d %H:%M:%S')
	if str(orderqtys[0]) == str(orderqtys[1]):
		orderproccur.execute("UPDATE run SET status = " + "'" + "Complete"  + "'" + " , order_end_time =  '" + str(orderendtimeformatted) + "' WHERE order_id = " +  str(passedorderidarg))

	mydb.commit()

# TODO: Make orders actually progress

##################
# Order Controller
##################
# Check for Orders to process every second until Orders all submitted and completed
# If found, Check if required Products exist in any Bay
# For products which don't, check which ones are not currently required for orders
# Prefer to move Bays 5-1, to those locations, replacing the lowest on the forecast
# Move Totes from Racks to Bays in robot_move_queue
# Move usurped Totes from Bays to Racks (move_time) in robot_move_queue
# Move Order to Run table and to Bay 1 so Order Processor picks it up
#

def order_controller(passedorderarg):
	ordercur = mydb.cursor()
	ordercur.execute("DELETE FROM run")
	print("TLOG Orders starting processing")
	ordercur.execute("SELECT id FROM orders")
	orderstoprocess = ordercur.rowcount
	print("Orders to process: " + str(orderstoprocess))
	orderidstoprocess = ordercur.fetchall()
	for currentorderid in orderidstoprocess:
		# print("Processing Order " + str(currentorderid[0]))
		orderstarttime = datetime.datetime.now()
		orderstarttimeformatted = orderstarttime.strftime('%Y-%m-%d %H:%M:%S')
		statement = "INSERT INTO run (id,order_id,status,bay,order_start_time) VALUES ("+str(
			runid)+","+str(currentorderid[0])+",'In Progress',1,'"+str(orderstarttimeformatted)+"')"
#		print(statement)
		ordercur.execute(statement)
		order_processor(currentorderid[0])
#	mydb.commit()
	print("TLOG Orders completed processing")


###############
# Main Thread Controller
#
print()
print("Main start")
# currentbay=0
# for baycounter in range(bay_count):
#	currentbay+=1
#	print("Starting Bay Processor for Bay: " + str(currentbay))
#	z = threading.Thread(target=bay_processor, args=(currentbay,), daemon=True)
#	z.start()

# Print Bay 1-5 Summary 
bay_tote_summary() 

#y = threading.Thread(target=robot_controller, args=(2,), daemon=True)
# y.start()
x = threading.Thread(target=order_controller, args=(2,))
x.start()
x.join()
# mydb.commit()

# Print Bay 1-5 Summary 
# bay_tote_summary() 

print("Main end")





