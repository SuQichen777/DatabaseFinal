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
    SELECT * 
    FROM Hotel 
    WHERE HotelName = p_HotelName;
END;

DROP PROCEDURE IF EXISTS sp_get_activity_by_name;
CREATE PROCEDURE sp_get_activity_by_name (IN p_ActivityName VARCHAR(50))
BEGIN
    SELECT * 
    FROM Activity 
    WHERE ActivityName = p_ActivityName;
END;

DROP PROCEDURE IF EXISTS sp_get_guide_by_name;
CREATE PROCEDURE sp_get_guide_by_name (IN p_GuideName VARCHAR(50))
BEGIN
    SELECT * 
    FROM Guide 
    WHERE GuideName = p_GuideName;
END;

DROP PROCEDURE IF EXISTS sp_get_destination_by_name;
CREATE PROCEDURE sp_get_destination_by_name (IN p_City VARCHAR(50))
BEGIN
    SELECT * 
    FROM Destination 
    WHERE City = p_City;
END;

DROP PROCEDURE IF EXISTS sp_get_user_by_name;
CREATE PROCEDURE sp_get_user_by_name (IN p_UserName VARCHAR(50))
BEGIN
    SELECT * 
    FROM Users 
    WHERE Name = p_UserName;
END;

DROP PROCEDURE IF EXISTS sp_get_current_status;
CREATE PROCEDURE sp_get_current_status ()
BEGIN
    SELECT * 
    FROM CurrentStatus;
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