-- Indexes for table `Users`
ALTER TABLE `Users`
  ADD UNIQUE KEY `idx_users_email` (`Email`),
  ADD KEY `idx_users_phone` (`PhoneNumber`);

-- Indexes for table `Guide`
ALTER TABLE `Guide`
  ADD KEY `idx_guide_email` (`GuideEmail`),
  ADD KEY `idx_guide_phone` (`GuidePhone`);

-- Indexes for table `Trip`
ALTER TABLE `Trip`
  ADD KEY `idx_trip_userid` (`UserID`),
  ADD KEY `idx_trip_guideid` (`GuideID`);

-- Indexes for table `Review`
ALTER TABLE `Review`
  ADD KEY `idx_review_userid` (`UserID`),
  ADD KEY `idx_review_tripid` (`TripID`);

-- Indexes for table `CurrentStatus`
-- no additional indexes needed

-- Indexes for table `Booking`
ALTER TABLE `Booking`
  ADD KEY `idx_booking_statusid` (`StatusID`),
  ADD KEY `idx_booking_userid` (`UserID`),
  ADD KEY `idx_booking_tripid` (`TripID`);

-- Indexes for table `TotalExpense`
ALTER TABLE `TotalExpense`
  ADD KEY `idx_totalexpense_tripid` (`TripID`);

-- Indexes for table `Destination`
-- no additional indexes needed

-- Indexes for table `Activity`
ALTER TABLE `Activity`
  ADD KEY `idx_activity_tripid` (`TripID`),
  ADD KEY `idx_activity_destinationid` (`DestinationID`);

-- Indexes for table `ActivityExpense`
ALTER TABLE `ActivityExpense`
  ADD KEY `idx_activityexpense_totalexpenseid` (`TotalExpenseID`);

-- Indexes for table `Transportation`
ALTER TABLE `Transportation`
  ADD KEY `idx_transportation_tripid` (`TripID`);

-- Indexes for table `TransportationExpense`
ALTER TABLE `TransportationExpense`
  ADD KEY `idx_transportationexpense_totalexpenseid` (`TotalExpenseID`);

-- Indexes for table `Hotel`
-- no additional indexes needed

-- Indexes for table `Accommodation`
ALTER TABLE `Accommodation`
  ADD KEY `idx_accommodation_tripid` (`TripID`),
  ADD KEY `idx_accommodation_hotelid` (`HotelID`);

-- Indexes for table `AccommodationExpense`
ALTER TABLE `AccommodationExpense`
  ADD KEY `idx_accommodationexpense_totalexpenseid` (`TotalExpenseID`);