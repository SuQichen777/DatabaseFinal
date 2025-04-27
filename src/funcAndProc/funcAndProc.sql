DROP PROCEDURE IF EXISTS sp_get_total_expense_by_trip;
CREATE PROCEDURE sp_get_total_expense_by_trip (IN p_TripID INT)
BEGIN
    SELECT * 
    FROM TotalExpense 
    WHERE TripID = p_TripID;
END;

DROP PROCEDURE IF EXISTS sp_get_hotel_by_name;
CREATE PROCEDURE sp_get_hotel_by_name (IN p_HotelName VARCHAR(150))
BEGIN
    IF p_HotelName = '' OR p_HotelName IS NULL THEN
        SELECT * FROM Hotel;
    ELSE
        SELECT * 
        FROM Hotel 
        WHERE HotelName LIKE CONCAT('%', p_HotelName, '%');
    END IF;
END;


DROP PROCEDURE IF EXISTS sp_get_activity_by_name;
CREATE PROCEDURE sp_get_activity_by_name (IN p_ActivityName VARCHAR(50))
BEGIN
    IF p_ActivityName = '' OR p_ActivityName IS NULL THEN
        SELECT * FROM Activity;
    ELSE
        SELECT * 
        FROM Activity 
        WHERE ActivityName LIKE CONCAT('%', p_ActivityName, '%');
    END IF;
END;



DROP PROCEDURE IF EXISTS sp_get_guide_by_name;
CREATE PROCEDURE sp_get_guide_by_name (IN p_GuideName VARCHAR(50))
BEGIN
    IF p_GuideName = '' OR p_GuideName IS NULL THEN
        SELECT * FROM Guide;
    ELSE
        SELECT * 
        FROM Guide 
        WHERE GuideName LIKE CONCAT('%', p_GuideName, '%');
    END IF;
END;


DROP PROCEDURE IF EXISTS sp_get_destination_by_name;
CREATE PROCEDURE sp_get_destination_by_name (IN p_City VARCHAR(50))
BEGIN
    IF p_City = '' OR p_City IS NULL THEN
        SELECT * FROM Destination;
    ELSE
        SELECT * 
        FROM Destination 
        WHERE City LIKE CONCAT('%', p_City, '%');
    END IF;
END;



DROP PROCEDURE IF EXISTS sp_get_user_by_name;
CREATE PROCEDURE sp_get_user_by_name (IN p_UserName VARCHAR(50))
BEGIN
    IF p_UserName = '' OR p_UserName IS NULL THEN
        SELECT * FROM Users;
    ELSE
        SELECT * 
        FROM Users 
        WHERE Name LIKE CONCAT('%', p_UserName, '%');
    END IF;
END;



DROP PROCEDURE IF EXISTS sp_get_trip_by_name;
CREATE PROCEDURE sp_get_trip_by_name (IN p_TripName VARCHAR(50))
BEGIN
    IF p_TripName = '' OR p_TripName IS NULL THEN
        SELECT * FROM Trip;
    ELSE
        SELECT *
        FROM Trip
        WHERE TripName LIKE CONCAT('%', p_TripName, '%');
    END IF;
END;


DROP PROCEDURE IF EXISTS sp_get_visible_trips;
CREATE PROCEDURE sp_get_visible_trips (IN p_UserID INT, IN p_SearchTerm VARCHAR(50))
BEGIN
    IF p_SearchTerm = '' OR p_SearchTerm IS NULL THEN
        SELECT Trip.*
        FROM Trip
        LEFT JOIN Booking ON Trip.TripID = Booking.TripID
        LEFT JOIN CurrentStatus ON Booking.StatusID = CurrentStatus.StatusID
        WHERE Trip.UserID = p_UserID
           OR (Trip.UserID != p_UserID AND CurrentStatus.IsConfirmed = TRUE);
    ELSE
        SELECT Trip.*
        FROM Trip
        LEFT JOIN Booking ON Trip.TripID = Booking.TripID
        LEFT JOIN CurrentStatus ON Booking.StatusID = CurrentStatus.StatusID
        WHERE (Trip.UserID = p_UserID
               OR (Trip.UserID != p_UserID AND CurrentStatus.IsConfirmed = TRUE))
          AND Trip.TripName LIKE CONCAT('%', p_SearchTerm, '%');
    END IF;
END;



DROP PROCEDURE IF EXISTS sp_get_reviews_by_trip;
CREATE PROCEDURE sp_get_reviews_by_trip (IN p_TripID INT)
BEGIN
    SELECT * 
    FROM Review 
    WHERE TripID = p_TripID;
END;

DROP PROCEDURE IF EXISTS DeleteTripAndRelatedData;
CREATE PROCEDURE DeleteTripAndRelatedData (
    IN in_TripID INT
)
BEGIN
    DELETE AE FROM AccommodationExpense AE
    JOIN Accommodation A ON AE.AccommodationID = A.AccommodationID
    WHERE A.TripID = in_TripID;

    DELETE TE FROM TransportationExpense TE
    JOIN Transportation T ON TE.TransportationID = T.TransportationID
    WHERE T.TripID = in_TripID;

    DELETE AE FROM ActivityExpense AE
    JOIN Activity A ON AE.ActivityID = A.ActivityID
    WHERE A.TripID = in_TripID;

    DELETE FROM TotalExpense WHERE TripID = in_TripID;
    DELETE FROM Review WHERE TripID = in_TripID;
    DELETE FROM Booking WHERE TripID = in_TripID;
    DELETE FROM Accommodation WHERE TripID = in_TripID;
    DELETE FROM Transportation WHERE TripID = in_TripID;
    DELETE FROM Activity WHERE TripID = in_TripID;
    DELETE FROM Trip WHERE TripID = in_TripID;
END;

DROP PROCEDURE IF EXISTS UpdateUserInfo;
CREATE PROCEDURE UpdateUserInfo (
    IN in_UserID INT,
    IN in_Name VARCHAR(50),
    IN in_PhoneNumber VARCHAR(15),
    IN in_Email VARCHAR(50),
    IN in_Age INT,
    IN in_Preference VARCHAR(150)
)
BEGIN
    UPDATE Users
    SET 
        Name = in_Name,
        PhoneNumber = in_PhoneNumber,
        Email = in_Email,
        Age = in_Age,
        Preference = in_Preference
    WHERE UserID = in_UserID;
END;

DROP PROCEDURE IF EXISTS sp_add_trip_and_init_total;
CREATE PROCEDURE sp_add_trip_and_init_total(
    IN p_UserID INT,
    IN p_GuideID INT,
    IN p_TripName VARCHAR(50),
    IN p_StartDate DATE,
    IN p_EndDate DATE,
    IN p_TripDes VARCHAR(150)
)
BEGIN
    INSERT INTO Trip(UserID, GuideID, TripName, StartDate, EndDate, TripDes)
    VALUES (p_UserID, p_GuideID, p_TripName, p_StartDate, p_EndDate, p_TripDes);

    SET @newTripID = LAST_INSERT_ID();

    INSERT INTO TotalExpense(TripID, Amount, ExpenseDescription)
    VALUES (@newTripID, 0.00, 'Initial total expense');
END;



DROP PROCEDURE IF EXISTS sp_get_trips_by_user;
CREATE PROCEDURE sp_get_trips_by_user (IN p_UserID INT)
BEGIN
    SELECT * 
    FROM Trip 
    WHERE UserID = p_UserID;
END;



DROP PROCEDURE IF EXISTS sp_get_collected_trips_by_user;
CREATE PROCEDURE sp_get_collected_trips_by_user (IN p_UserID INT)
BEGIN
    SELECT Trip.*
    FROM Review
    JOIN Trip ON Review.TripID = Trip.TripID
    WHERE Review.UserID = p_UserID;
END;


DROP PROCEDURE IF EXISTS sp_get_activities_by_trip;
CREATE PROCEDURE sp_get_activities_by_trip(IN p_TripID INT)
BEGIN
    SELECT * 
    FROM Activity
    WHERE TripID = p_TripID
    ORDER BY StartDate ASC, ActivityID ASC;
END;


DROP PROCEDURE IF EXISTS sp_get_accommodations_by_trip;
CREATE PROCEDURE sp_get_accommodations_by_trip(IN p_TripID INT)
BEGIN
    SELECT A.*, H.HotelName
    FROM Accommodation A
    JOIN Hotel H ON A.HotelID = H.HotelID
    WHERE A.TripID = p_TripID
    ORDER BY CheckInDate ASC, AccommodationID ASC;
END;


DROP PROCEDURE IF EXISTS sp_get_transportations_by_trip;
CREATE PROCEDURE sp_get_transportations_by_trip(IN p_TripID INT)
BEGIN
    SELECT * 
    FROM Transportation
    WHERE TripID = p_TripID
    ORDER BY StartDate ASC, TransportationID ASC;
END;


DROP PROCEDURE IF EXISTS sp_get_unscheduled_activities;
CREATE PROCEDURE sp_get_unscheduled_activities(IN p_TripID INT)
BEGIN
    SELECT *
    FROM Activity
    WHERE TripID = p_TripID AND StartDate IS NULL;
END;


DROP PROCEDURE IF EXISTS sp_get_unscheduled_accommodations;
CREATE PROCEDURE sp_get_unscheduled_accommodations(IN p_TripID INT)
BEGIN
    SELECT A.*, H.HotelName
    FROM Accommodation A
    JOIN Hotel H ON A.HotelID = H.HotelID
    WHERE A.TripID = p_TripID AND (CheckInDate IS NULL OR CheckOutDate IS NULL);
END;


DROP PROCEDURE IF EXISTS sp_get_unscheduled_transportations;
CREATE PROCEDURE sp_get_unscheduled_transportations(IN p_TripID INT)
BEGIN
    SELECT *
    FROM Transportation
    WHERE TripID = p_TripID AND StartDate IS NULL;
END;
