INSERT INTO Users (UserID, Name, Password, PhoneNumber, Email, Age, Preference) VALUES
(1, 'Lena Yamamoto', '123456', '+819012345678', 'lena.y@example.com', 29, 'Culture and nature'),
(2, 'Thierry Dubois', '123456', '+33712345678', 'thierry.d@example.com', 41, 'Museums and food'),
(3, 'Zanele Khumalo', '123456', '+27825551122', 'zanele.k@example.com', 35, 'Wildlife and hiking'),
(4, 'Carlos Rivas', '123456', '+51999876543', 'carlos.r@example.com', 26, 'Adventure and history'),
(5, 'Emma Chen', '123456', '+16048881234', 'emma.chen@example.com', 32, 'Parks and markets'),
(6, 'Logan Mitchell', '123456', '+6421432567', 'logan.m@example.com', 38, 'Snow and photography'),
(7, 'Chiara Bianchi', '123456', '+393481234567', 'chiara.b@example.com', 44, 'Historic walking tours'),
(8, 'Youssef Amrani', '123456', '+212699123456', 'youssef.a@example.com', 30, 'Street food and culture'),
(9, 'Napat Srisuk', '123456', '+66929991234', 'napat.s@example.com', 27, 'Temples and nightlife'),
(10, 'Anna Sigurdardottir', '123456', '+3546919876', 'anna.s@example.com', 36, 'Hot springs and stars');

INSERT INTO Guide (GuideID, GuideName, Languages, ExperienceYrs, GuidePhone, GuideEmail, Availabilities) VALUES
(1, 'Aiko Tanaka', 'Japanese, English', 7, '+81-70-1234-5678', 'aiko.t@example.jp', 'Available Mon–Fri, 9am–6pm'),
(2, 'Jean Dupont', 'French, English, Spanish', 12, '+33-6-23-45-67-89', 'jean.d@example.fr', 'Weekends only,
 advance booking required'),
(3, 'Sipho Mokoena', 'Zulu, English, Afrikaans', 5, '+27-73-456-7890', 'sipho.m@example.co.za', 'Available daily, 8am–8pm'),
(4, 'Maria Gutierrez', 'Spanish, English', 9, '+51-989-123-456', 'maria.g@example.pe', 'Flexible availability, prefers mornings'),
(5, 'Jason Lee', 'English, Mandarin, Cantonese', 4, '+1-604-321-6543', 'jason.l@example.ca', 'Available weekdays after 2pm'),
(6, 'Emma Clarke', 'English', 10, '+64-21-876-543', 'emma.c@example.nz', 'Full-time, can travel'),
(7, 'Luca Romano', 'Italian, English, French', 15, '+39-347-123-4567', 'luca.r@example.it', 'Available for private and group tours'),
(8, 'Fatima El Hadi', 'Arabic, French, English', 6, '+212-670-123456', 'fatima.eh@example.ma', 'Available on demand, 10am–6pm'),
(9, 'Niran Kanchana', 'Thai, English', 8, '+66-89-999-1234', 'niran.k@example.th', 'Weekdays only, not available holidays'),
(10, 'Bjorn Jonsson', 'Icelandic, English', 11, '+354-691-2345', 'bjorn.j@example.is', 'Available for Northern Lights season (Sep–Mar)');

INSERT INTO Trip (TripID, UserID, GuideID, TripName, StartDate, EndDate, TripDes) VALUES
(1, 1, 1, 'Kyoto Cultural Escape', '2025-05-01', '2025-05-05', 'A traditional journey through Kyoto’s historic sites'),
(2, 2, 2, 'Parisian Adventure', '2025-06-10', '2025-06-15', 'Romantic city experience with museums and cafes'),
(3, 3, 3, 'Cape Coast Safari', '2025-07-20', '2025-07-25', 'Beachside and wildlife tour around Cape Town'),
(4, 4, 4, 'Sacred Peru Trail', '2025-08-01', '2025-08-03', 'Visit Cusco and trek to the ancient Incan ruins'),
(5, 5, 5, 'Vancouver Chill', '2025-04-15', '2025-04-20', 'Relaxed itinerary of city parks and mountain air'),
(6, 6, 6, 'Snow & Serenity NZ', '2025-09-12', '2025-09-18', 'Explore Queenstown’s peaks and lakeside serenity'),
(7, 7, 7, 'Roman Relics Tour', '2025-10-05', '2025-10-10', 'Uncover ancient Roman history and architecture'),
(8, 8, 8, 'Moroccan Markets & Palaces', '2025-11-01', '2025-11-07', 'Spices, stories, and souks of Marrakech'),
(9, 9, 9, 'Bangkok Highlights', '2025-12-20', '2025-12-25', 'Temples, nightlife, and local Thai cuisine'),
(10, 10, 10, 'Northern Lights Quest', '2026-01-10', '2026-01-15', 'Chasing auroras and exploring Iceland’s wonders');

INSERT INTO Hotel (HotelID, HotelName, HotelAddress, RoomDescription) VALUES
(1, 'Kyoto Garden Inn', '45 Hanami Lane, Gion District, Kyoto, Japan', 'Traditional tatami-style rooms with garden views and onsen access'),
(2, 'Hôtel Lumière', '12 Rue de l’Étoile, Paris, France', 'Modern boutique rooms with Eiffel Tower view and complimentary breakfast'),
(3, 'Table Bay Retreat', '1 Ocean View Drive, Cape Town, South Africa', 'Luxury suites with harbor view, spa, and infinity pool'),
(4, 'Andean Vista Lodge', 'Cusco Valley Road 201, Cusco, Peru', 'Rustic mountain rooms with private terraces and local cuisine'),
(5, 'Harbor View Suites', '122 Bay Street, Vancouver, Canada', 'Spacious rooms with kitchenette, ideal for long stays'),
(6, 'Alpine Ridge Resort', 'Lakefront Road, Queenstown, New Zealand', 'Wooden cabins with lake views and fireplace, ideal for ski season'),
(7, 'Roma Imperial Hotel', 'Via Roma 8, Rome, Italy', 'Classic Roman interior, walking distance to Colosseum'),
(8, 'Riad El Medina', '27 Medina Street, Marrakech, Morocco', 'Authentic Moroccan rooms around a courtyard, with rooftop dining'),
(9, 'Sawasdee Bangkok Hotel', '55 Sukhumvit Soi 8, Bangkok, Thailand', 'Comfortable city rooms near nightlife and BTS station'),
(10, 'Aurora Lodge', 'Laugavegur 101, Reykjavik, Iceland', 'Glass-roof rooms for Northern Lights viewing, geothermal hot tub access');

INSERT INTO TotalExpense (TotalExpenseID, TripID, Amount, ExpenseDescription) VALUES
(1, 1, 1050.75, 'Accommodation and city tour package'),
(2, 2, 1820.40, 'Scuba diving, resort stay, and meals'),
(3, 3, 900.00, 'Cultural workshop and hotel combo'),
(4, 4, 670.20, 'Budget hike trip with guide fee'),
(5, 5, 1245.60, 'Wine tour with luxury accommodation'),
(6, 6, 880.30, 'Museum access and daily transport'),
(7, 7, 1499.99, 'Safari adventure with dinner and lodging'),
(8, 8, 1375.45, 'Rafting and mountain inn expenses'),
(9, 9, 925.00, 'Snorkeling, equipment rental, and hotel'),
(10, 10, 1100.85, 'Temple trip with private guide and meals');

INSERT INTO Accommodation (AccommodationID, TripID, HotelID, CheckInDate, CheckOutDate) VALUES
(1, 1, 1, '2025-05-01', '2025-05-05'),
(2, 2, 3, '2025-06-10', '2025-06-15'),
(3, 3, 2, '2025-07-20', '2025-07-25'),
(4, 4, 4, '2025-08-01', '2025-08-03'),
(5, 5, 1, '2025-04-15', '2025-04-20'),
(6, 6, 5, '2025-09-12', '2025-09-18'),
(7, 7, 6, '2025-10-05', '2025-10-10'),
(8, 8, 3, '2025-11-01', '2025-11-07'),
(9, 9, 7, '2025-12-20', '2025-12-25'),
(10, 10, 2, '2026-01-10', '2026-01-15');

INSERT INTO AccommodationExpense (AccommodationID, TotalExpenseID, Amount, ExpenseDescription) VALUES
(1, 1, 450.00, '5 nights at budget hotel'),
(2, 2, 1200.00, 'Luxury resort stay'),
(3, 3, 800.50, 'Mid-range hotel with breakfast'),
(4, 4, 300.00, 'Short stay in city inn'),
(5, 5, 550.75, '4-night family suite'),
(6, 6, 980.00, 'Business hotel including meals'),
(7, 7, 400.00, 'Hotel near airport'),
(8, 8, 650.25, 'Hotel with ocean view'),
(9, 9, 700.00, 'Holiday season peak price'),
(10, 10, 520.60, 'City center accommodation');

INSERT INTO Destination (DestinationID, City, Country, DetailAddress, DestinationDescription) VALUES
(1, 'Kyoto', 'Japan', '123 Gion District, Kyoto-shi', 'Ancient temples and cherry blossoms'),
(2, 'Paris', 'France', '5 Rue de Rivoli', 'Romantic city with art and architecture'),
(3, 'Cape Town', 'South Africa', 'Table Mountain National Park', 'Coastal city with mountains and beaches'),
(4, 'Cusco', 'Peru', 'Plaza de Armas, Historic Center', 'Gateway to Machu Picchu'),
(5, 'Vancouver', 'Canada', 'Stanley Park Drive, BC', 'Modern city with scenic nature'),
(6, 'Queenstown', 'New Zealand', 'Lake Wakatipu, Otago', 'Adventure capital with mountain views'),
(7, 'Rome', 'Italy', 'Piazza Venezia', 'Rich in ancient Roman history'),
(8, 'Marrakech', 'Morocco', 'Jemaa el-Fnaa, Medina', 'Cultural hub with markets and palaces'),
(9, 'Bangkok', 'Thailand', '123 Charoen Krung Rd', 'Bustling city with temples and nightlife'),
(10, 'Reykjavik', 'Iceland', 'Laugavegur 55', 'Gateway to geysers and northern lights');


INSERT INTO Activity (ActivityID, TripID, DestinationID, ActivityName, ActivityDescription, StartDate, Duration) VALUES
(1, 1, 1, 'City Tour', 'Guided tour through historical landmarks', '2025-05-02', 5),
(2, 2, 2, 'Scuba Diving', 'Explore coral reefs and marine life', '2025-06-12', 3),
(3, 3, 3, 'Cooking Class', 'Learn to make traditional dishes', '2025-07-21', 2),
(4, 4, 4, 'Mountain Hiking', 'Full-day hike with scenic views', '2025-08-02', 8),
(5, 5, 5, 'Wine Tasting', 'Visit vineyards and taste local wines', '2025-04-17', 4),
(6, 6, 6, 'Museum Visit', 'Explore the national art museum', '2025-09-13', 2),
(7, 7, 7, 'Desert Safari', 'Evening jeep safari and BBQ dinner', '2025-10-06', 6),
(8, 8, 8, 'River Rafting', 'Adventure rafting in Class III rapids', '2025-11-03', 4),
(9, 9, 9, 'Snorkeling', 'Shallow reef snorkeling with guide', '2025-12-21', 3),
(10, 10, 10, 'Temple Visit', 'Morning spiritual tour of ancient temples', '2026-01-11', 3);

INSERT INTO ActivityExpense (ActivityID, TotalExpenseID, Amount, ExpenseDescription) VALUES
(1, 1, 50.00, 'Entrance fees and local guide'),
(2, 2, 120.00, 'Scuba gear rental and instructor fee'),
(3, 3, 45.00, 'Cooking ingredients and kitchen rental'),
(4, 4, 75.00, 'Transport and mountain pass fee'),
(5, 5, 60.00, 'Wine samples and vineyard tour'),
(6, 6, 30.00, 'Museum entry and audio guide'),
(7, 7, 90.00, 'Desert transport and dinner buffet'),
(8, 8, 100.00, 'Rafting gear and insurance'),
(9, 9, 40.00, 'Snorkel equipment rental'),
(10, 10, 25.00, 'Temple donation and shuttle transport');

INSERT INTO Transportation (TransportationID, TripID, StartDate, Duration, StartingPoint, EndingPoint, TransportationType) VALUES
(1, 1, '2025-05-01', 2, 'Kyoto Station', 'Arashiyama Bamboo Grove', 'Train'),
(2, 2, '2025-06-11', 1, 'Paris CDG Airport', 'Hotel Lumière', 'Shuttle'),
(3, 3, '2025-07-20', 3, 'Cape Town Airport', 'Table Mountain Base', 'Private Car'),
(4, 4, '2025-08-01', 4, 'Cusco Center', 'Machu Picchu Gate', 'Bus'),
(5, 5, '2025-04-16', 1, 'Vancouver Airport', 'Stanley Park Hotel', 'Taxi'),
(6, 6, '2025-09-12', 2, 'Queenstown Downtown', 'Ski Lift Station', 'Shuttle Bus'),
(7, 7, '2025-10-05', 1, 'Rome Fiumicino Airport', 'Hotel Roma Imperial', 'Airport Transfer'),
(8, 8, '2025-11-01', 2, 'Marrakech Airport', 'Riad El Medina', 'Private Taxi'),
(9, 9, '2025-12-20', 1, 'Bangkok BTS Siam', 'Sawasdee Hotel', 'Tuk-Tuk'),
(10, 10, '2026-01-10', 2, 'Reykjavik Airport', 'Aurora Lodge', 'Minibus');

INSERT INTO TransportationExpense (TransportationID, TotalExpenseID, Amount, ExpenseDescription) VALUES
(1, 1, 25.00, 'Train fare from Kyoto to Arashiyama'),
(2, 2, 18.50, 'Shared airport shuttle to hotel'),
(3, 3, 40.00, 'Private car from airport to Table Mountain'),
(4, 4, 15.00, 'Bus transfer from Cusco to Machu Picchu'),
(5, 5, 22.75, 'Taxi ride from Vancouver airport'),
(6, 6, 30.00, 'Shuttle to ski resort area'),
(7, 7, 28.00, 'Hotel pickup from Rome airport'),
(8, 8, 35.50, 'Private taxi to riad in Marrakech'),
(9, 9, 5.00, 'Short tuk-tuk ride to hotel'),
(10, 10, 60.00, 'Minibus from airport to Aurora Lodge');


INSERT INTO CurrentStatus (StatusID, IsConfirmed, IsPending, IsCanceled) VALUES
(1, 1, 0, 0),  -- Confirmed
(2, 0, 1, 0),  -- Pending
(3, 0, 0, 1),  -- Canceled
(4, 1, 0, 0),  -- Confirmed
(5, 0, 1, 0),  -- Pending
(6, 1, 0, 0),  -- Confirmed
(7, 0, 1, 0),  -- Pending
(8, 0, 0, 1),  -- Canceled
(9, 1, 0, 0),  -- Confirmed
(10, 0, 1, 0); -- Pending

INSERT INTO Booking (BookingID, StatusID, UserID, TripID, BookingDate) VALUES
(1, 3, 7, 2, '2025-03-18'),
(2, 1, 4, 5, '2025-05-02'),
(3, 5, 2, 8, '2025-07-11'),
(4, 2, 9, 1, '2025-02-28'),
(5, 6, 1, 10, '2025-06-03'),
(6, 4, 10, 3, '2025-08-20'),
(7, 9, 5, 6, '2025-04-27'),
(8, 7, 8, 4, '2025-09-15'),
(9, 8, 3, 9, '2025-01-22'),
(10, 10, 6, 7, '2025-10-06');

INSERT INTO Review (ReviewID, UserID, TripID, Rating, Comments) VALUES
(1, 2, 1, 5, 'Absolutely loved the guide and the activities. Everything was perfectly arranged.'),
(2, 4, 3, 3, 'The trip was okay, but the weather impacted a few plans.'),
(3, 1, 2, 4, 'Very informative and well-paced. Would recommend to friends.'),
(4, 6, 4, 2, 'The accommodation wasn’t clean, and the trip felt rushed.'),
(5, 3, 6, 5, 'An unforgettable experience! The guide was exceptional.'),
(6, 7, 5, 4, 'Well organized, but could use more free time in the itinerary.'),
(7, 8, 7, 1, 'Trip was cancelled last minute, very disappointed.'),
(8, 5, 8, 5, 'Perfect in every way – from hotel to hiking trails!'),
(9, 9, 9, 3, 'Mixed feelings. Great food, but the activities were a bit short.'),
(10, 10, 10, 4, 'Smooth booking and good coordination. Would go again.');