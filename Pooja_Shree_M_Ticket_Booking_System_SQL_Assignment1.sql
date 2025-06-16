-- TASK 1
create database TicketBookingSystem ;
use TicketBookingSystem ;
-- drop database TicketBookingSystem ;

-- create venue table
Create table Venue( 
	venue_id int primary key auto_increment,
	venue_name varchar(255) not null,
	address varchar(255) not null
);
-- create event table
Create table Event(
	event_id int primary key auto_increment,
    event_name varchar(200) not null,
    event_date DATE not null,
    event_time TIME not null,
    total_seats int not null,
    available_seats int not null,
    venue_id int not null,
    ticket_price decimal(10,2) not null,
    event_type enum('Movie', 'Sports', 'Concert'),
	foreign Key (venue_id) references Venue(venue_id)
    );
-- create customer table
Create table Customer (
	customer_id int primary key auto_increment,
    customer_name varchar(200) not null,
    email varchar(200) unique not null,
    phone_number varchar(20) not null
    );
-- create booking table
Create table Booking (
 booking_id int primary key auto_increment,
    customer_id int not null,
    event_id int not null,
    num_tickets int not null,
    total_cost decimal(10,2) not null,
    booking_date datetime default current_timestamp,
    foreign key (customer_id) references Customer(customer_id),
    foreign key (event_id) references Event(event_id)
);
-- Insert records into Venue table
insert into Venue (venue_name, address) values
('Grand Cinema', '123 Movie St, CityA'),
('City Stadium', '456 Sports Rd, CityB'),
('Concert Hall', '789 Music Ave, CityC'),
('Exhibition Center', '101 Expo Blvd, CityD'),
('Community Theater', '202 Play Ln, CityE'),
('Museum of Art', '303 Gallery Pkwy, CityF'),
('Science Center', '404 Discovery Dr, CityG'),
('Botanical Gardens', '505 Green St, CityH'),
('Waterfront Park', '606 Oceanfront Rd, CityI'),
('The Jazz Club', '888 Melody Lane, CityK'),
('Children''s Museum Auditorium', '999 Imagination Blvd, CityL'),
('Innovation Hub', '707 Tech Ave, CityJ');

-- Insert records into Event table
insert into Event (event_name, event_date, event_time, venue_id, total_seats, available_seats, ticket_price, event_type) values
('The Dark Knight Rises', '2025-07-15', '19:00:00', 1, 300, 250, 200.00, 'Movie'),
('Unbooked Test Movie', '2025-07-30', '17:00:00', 1, 100, 100, 250.00, 'Movie'),
('Cricket World Cup Final', '2025-08-20', '14:30:00', 2, 50000, 48000, 1500.00, 'Sports'),
('Rock Legends Concert', '2025-09-10', '20:00:00', 3, 5000, 4500, 2500.00, 'Concert'),
('Comedy Night Live', '2025-07-25', '21:00:00', 4, 150, 100, 150.00, 'Movie'),
('Annual Sports Meet', '2025-08-01', '09:00:00', 5, 10000, 9000, 500.00, 'Sports'),
('Classical Music Gala', '2025-09-22', '18:00:00', 3, 800, 750, 1800.00, 'Concert'),
('Summer Movie Marathon', '2025-07-20', '10:00:00', 1, 400, 350, 100.00, 'Movie'),
('Football Championship', '2025-10-05', '16:00:00', 2, 30000, 28000, 1200.00, 'Sports'),
('Jazz Fusion Night', '2025-10-15', '20:30:00', 6, 600, 550, 2000.00, 'Concert'),
('AI fusion ', '2025-06-20', '10:00:00', 1, 100, 40, 500, 'concert'),
('Kids Movie Festival', '2025-07-18', '11:00:00', 7, 200, 180, 80.00, 'Movie');

-- Insert records into Customer table
insert into Customer (customer_name, email, phone_number) values
('Alice Smith', 'alice.s@example.com', '9876543210'),
( 'John NoBook', 'john.nobook@example.com', '9999988888'),
('Bob Johnson', 'bob.j@example.com', '9988776655'),
('Charlie Brown', 'charlie.b@example.com', '9000000000'),
('Diana Prince', 'diana.p@example.com', '9111111111'),
('Eve Adams', 'eve.a@example.com', '9222222222'),
('Frank Green', 'frank.g@example.com', '9333333333'),
('Grace Hopper', 'grace.h@example.com', '9444444444'),
('Harry Potter', 'harry.p@example.com', '9555555555'),
('Ivy Rose', 'ivy.r@example.com', '9666666666'),
('Jack Sparrow', 'jack.s@example.com', '9777777777');
-- Insert records into Booking table
insert into Booking (customer_id, event_id, num_tickets, total_cost) values
(1, 1, 2, 400.00),
(2, 2, 5, 7500.00),
(3, 3, 1, 2500.00),
(4, 1, 3, 600.00),
(5, 4, 1, 150.00),
(6, 5, 6, 3000.00),
(7, 6, 2, 3600.00),
(8, 7, 4, 400.00),
(9, 8, 5, 6000.00),
(10, 9, 3, 6000.00),
(1, 10, 2, 160.00),
(2, 1, 1, 200.00);

-- TASK 2
--  listing all Events
select * from event;

-- events with available tickets
select * from event where available_seats > 0 ;

--  events name partial match with ‘cup’
select * from event where event_name like '%cup%';

-- events with ticket price range is between 1000 to 2500
select * from event where ticket_price between 1000 and 2500;

-- events with dates falling within a specific range
select * from event where event_date between '2025-07-10' and '2025-07-15';

-- events with available tickets that also have "Concert" in their name
select * from event where available_seats >0 and event_name like '%concert%';

-- users in batches of 5, starting from the 6th user
select * from customer limit 5 offset 5;

-- bookings details contains booked no of ticket more than 4
select * from Booking where num_tickets > 4 ;

-- customer information whose phone number end with ‘000’.
select * from Customer where phone_number like '%000';

-- events in order whose seat capacity more than 15000
select * from event where total_seats > 15000 order by total_seats ;

-- events name not start with ‘x’, ‘y’, ‘z’
select * from event where event_name not like 'x%' and  event_name not like '%y' and event_name not like  '%z';

-- TASK 3
-- query to List Events and Their Average Ticket Prices
select event_name , avg(ticket_price) as Average_Ticket_Price
from event group by event_name ;

-- Calculate the Total Revenue Generated by Events
select E.event_name , sum(B.total_cost) as Total_Revenue
from event E
join Booking B on E.event_id = B.event_id
group by event_name;

-- find the event with the highest ticket sales
select E.event_name, sum(B.num_tickets) as TotalTicketsSold
from Event E
join Booking B on E.event_id = B.event_id
group by E.event_name
order by TotalTicketsSold desc
limit 1;

-- Calculate the Total Number of Tickets Sold for Each Event
select E.event_name,
       coalesce((
         select count(*) 
         from Booking B 
         where B.event_id = E.event_id
       ), 0) as TicketsSold
from Event E;

-- Events with No Ticket Sales
select E.event_name-- , sum(B.num_tickets) as TotalTicketsSold 
from Event E
left join Booking B on E.event_id = B.event_id
where booking_id is null; 

-- User Who Has Booked the Most Tickets
select C.customer_name , sum(B.num_tickets) as TicketsBooked
from Customer C  
left join Booking B on C.customer_id = B.booking_id
group by C.customer_name
order by TicketsBooked desc
limit 1;

-- Events and the total number of tickets sold for each month
select E.event_name,date_format(B.booking_date, '%Y-%m') as BookingMonth , sum(B.num_tickets) as TicketSold
from Event E
join Booking B on E.event_id = B.booking_id
group by E.event_name , BookingMonth
order by E.event_name , BookingMonth;

-- calculate the average Ticket Price for Events in Each Venue
select V.venue_name, E.event_name ,avg(E.ticket_price) as AverageTicketPrice
from Event E
join Venue V on E.event_id= V.venue_id
group by V.venue_name,E.event_name;

-- calculate the total Number of Tickets Sold for Each Event Type
select E.event_type , sum(B.num_tickets) as TotalTicketsSold
from Event E
left join Booking B on E.event_id = B.event_id
group by E.event_type;

-- calculate the total Revenue Generated by Events in Each Year
select  year(booking_date) as BookingYear,sum(total_cost) as TotalRevenue
from Booking
group by BookingYear
order by BookingYear;

-- users who have booked tickets for multiple events
select C.customer_name from Customer C 
join Booking B on C.customer_id = B.customer_id
group by C.customer_id, C.customer_name
having count(distinct B.event_id) > 1;

-- calculate the Total Revenue Generated by Events for Each User
select C.customer_name , sum(B.total_cost) as TotalRevenue 
from Customer C 
join Booking B on C.customer_id = B.customer_id
group by customer_name;

-- calculate the Average Ticket Price for Events in Each Category and Venue
select V.venue_name, E.event_type, avg(E.ticket_price) as AverageTicketPrice
from Venue V
join Event E on V.venue_id = E.venue_id
group by V.venue_name, E.event_type
order by V.venue_name, E.event_type;

-- list Users and the Total Number of Tickets They've Purchased in the Last 30 Days
select C.customer_name , sum(B.num_tickets) as TotalTicketsPurchased
from Customer C
join Booking B on C.customer_id = B.customer_id
where B.booking_date >= date_sub(curdate(), interval 30 day)
group by C.customer_name
order by TotalTicketsPurchased desc;

-- TASK 4
-- Average Ticket Price for Events in Each Venue Using a Subquery
select V.venue_name,
       coalesce((
		select avg(E.ticket_price)
         from Event E
         where E.venue_id = V.venue_id
       ), 0) as AverageTicketPrice
from Venue V;

-- Events with More Than 50% of Tickets Sold using a subquery
select event_name, total_seats, available_seats
from Event
where (total_seats - available_seats) > (total_seats * 0.5);

-- Total Number of Tickets Sold for Each Event
select E.event_name,
       coalesce((
           select sum(B.num_tickets)
           from booking B
           where B.event_id = E.event_id
       ), 0) as Total_Tickets_Sold
from Event E ;

-- Users Who Have Not Booked Any Tickets Using a NOT EXISTS Subquery
select Customer_name from Customer C 
where not exists
 (select  1 
 from Booking B
 where B.customer_id = C.customer_id
);

-- Events with No Ticket Sales Using a NOT IN Subquery
select event_name
from Event
where event_id not in (select distinct event_id from Booking);

-- Total Number of Tickets Sold for Each Event Type Using a Subquery in the FROM Clause
select event_type, sum(num_tickets_sold) AS TotalTicketsSold
from (
    select E.event_type, B.num_tickets as num_tickets_sold
    from Event E
    join Booking B on E.event_id = B.event_id
) as EventSales
group by event_type;

-- Events with Ticket Prices Higher Than the Average Ticket Price Using a Subquery in the WHERE Clause
select event_name, ticket_price
from Event
where ticket_price > (select avg(ticket_price) from Event);

-- Total Revenue Generated by Events for Each User Using a Correlated Subquery
select
    C.customer_name,
    (select sum(B.total_cost) from Booking B where B.customer_id = C.customer_id) AS TotalRevenue
from Customer C;

-- Users Who Have Booked Tickets for Events (for example 'Grand Cinema') in a Given Venue Using a Subquery in the WHERE Clause
select distinct C.customer_name
from Customer C
where C.customer_id in (
    select B.customer_id
    from Booking B
    join Event E on B.event_id = E.event_id
    join Venue V on E.venue_id = V.venue_id
    where V.venue_name = 'Grand Cinema'
);

-- Total Number of Tickets Sold for Each Event Category Using a Subquery with GROUP BY
select event_type, sum(tickets_sold) as TotalTicketsSold
from (
    select E.event_type, B.num_tickets as tickets_sold
    from Event E
    join Booking B on E.event_id = B.event_id
) as EventCategorySales
group by event_type;

-- Users Who Have Booked Tickets for Events in each Month Using a Subquery with DATE_FORMAT
select distinct C.customer_name, date_format(B.booking_date, '%Y-%m') as BookingMonth
from Customer C
join Booking B on C.customer_id = B.customer_id
order by C.customer_name, BookingMonth;

-- Average Ticket Price for Events in Each Venue Using a Subquery
select V.venue_name, (
   select avg(E.ticket_price)
    from Event E
    where E.venue_id = V.venue_id
) as AverageTicketPrice
from Venue V
where V.venue_id in (select distinct venue_id from Event);