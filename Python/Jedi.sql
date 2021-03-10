CREATE DATABASE JEDI;

DROP TABLE IF EXISTS tlog;
CREATE TABLE tlog(
order_time DATETIME,
order_id INT,
product_id INT
);

DROP TABLE IF EXISTS orders;
CREATE TABLE orders (
id INT,
time DATETIME,
system_time DATETIME
);

DROP TABLE IF EXISTS product;
CREATE TABLE product (
id INT,
name VARCHAR(500),
storage INT,
per_tote INT
);

DROP TABLE IF EXISTS forecast;
CREATE TABLE forecast (
product_id INT,
forecast_qty INT
);

DROP TABLE IF EXISTS inventory_tote;
CREATE TABLE inventory_tote (
id INT,
product_id INT,
quantity INT
);

DROP TABLE IF EXISTS location;
CREATE TABLE location (
id INT,
bay VARCHAR(50),
tote INT,
status VARCHAR(50)
);

DROP TABLE IF EXISTS order_pick;
CREATE TABLE order_pick (
order_id INT,
product_id INT,
required_qty INT,
picked_qty INT
);

DROP TABLE IF EXISTS robot_move_queue;
CREATE TABLE robot_move_queue (
tote_id INT,
from_loc INT,
to_loc INT,
status VARCHAR(50)
);

CREATE TABLE robot (
id INT,
status VARCHAR(50)
);

DROP TABLE IF EXISTS run;
CREATE TABLE run (
id BIGINT,
order_id INT,
status VARCHAR(50),
bay INT,
order_start_time DATETIME,
order_end_time DATETIME
);

CREATE TABLE run_log (
run_id BIGINT,
order_id INT,
action VARCHAR(500),
time DATETIME,
log VARCHAR(2000)
);