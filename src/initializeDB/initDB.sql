DROP TABLE IF EXISTS AccommodationExpense;
DROP TABLE IF EXISTS Accommodation;
DROP TABLE IF EXISTS Hotel;
DROP TABLE IF EXISTS TransportationExpense;
DROP TABLE IF EXISTS Transportation;
DROP TABLE IF EXISTS ActivityExpense;
DROP TABLE IF EXISTS Activity;
DROP TABLE IF EXISTS Destination;
DROP TABLE IF EXISTS TotalExpense;
DROP TABLE IF EXISTS Booking;
DROP TABLE IF EXISTS CurrentStatus;
DROP TABLE IF EXISTS Review;
DROP TABLE IF EXISTS Trip;
DROP TABLE IF EXISTS Guide;
DROP TABLE IF EXISTS Users;


CREATE TABLE Users(
    UserID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(50),
    Password VARCHAR(255),
    PhoneNumber VARCHAR(15),
    Email VARCHAR(50),
    Age INT,
    Preference VARCHAR(150)
);

CREATE TABLE Guide(
    GuideID INT PRIMARY KEY AUTO_INCREMENT,
    GuideName VARCHAR(50),
    Languages VARCHAR(150),
    ExperienceYrs INT,
    GuidePhone VARCHAR (25),
    GuideEmail VARCHAR(25),
    Availabilities VARCHAR(400)
);

CREATE TABLE Trip(
    TripID INT PRIMARY KEY AUTO_INCREMENT,
    UserID INT,
    GuideID INT,
    TripName VARCHAR(50),
    StartDate DATE,
    EndDate DATE,
    TripDes VARCHAR(150),
    FOREIGN KEY(UserID) REFERENCES Users(UserID),
    FOREIGN KEY(GuideID) REFERENCES Guide(GuideID)
);

CREATE TABLE Review(
    ReviewID INT PRIMARY KEY AUTO_INCREMENT,
    UserID INT,
    TripID INT,
    Rating INT,
    Comments VARCHAR(500),
    FOREIGN KEY(UserID) REFERENCES Users(UserID),
    FOREIGN KEY(TripID) REFERENCES Trip(TripID)
);

CREATE TABLE CurrentStatus(
    StatusID INT PRIMARY KEY,
    IsConfirmed BOOLEAN,
    IsPending BOOLEAN,
    IsCanceled BOOLEAN
);

CREATE TABLE Booking(
    BookingID INT PRIMARY KEY AUTO_INCREMENT,
    StatusID INT,
    UserID INT,
    TripID INT,
    BookingDate DATE,
    FOREIGN KEY(StatusID) REFERENCES CurrentStatus(StatusID),
    FOREIGN KEY(UserID) REFERENCES Users(UserID),
    FOREIGN KEY(TripID) REFERENCES Trip(TripID)   
);

CREATE Table TotalExpense(
    TotalExpenseID INT PRIMARY KEY AUTO_INCREMENT,
    TripID INT,
    Amount DECIMAL(10, 2),
    ExpenseDescription VARCHAR(150),
    FOREIGN KEY(TripID) REFERENCES Trip(TripID)
);

CREATE TABLE Destination(
    DestinationID INT PRIMARY KEY AUTO_INCREMENT,
    City VARCHAR(50),
    Country VARCHAR(50),
    DetailAddress VARCHAR(150),
    DestinationDescription VARCHAR(150)
);

CREATE TABLE Activity(
    ActivityID INT PRIMARY KEY AUTO_INCREMENT,
    TripID INT,
    DestinationID INT,
    ActivityName VARCHAR(50),
    ActivityDescription VARCHAR(150),
    StartDate DATE,
    Duration INT,
    FOREIGN KEY(TripID) REFERENCES Trip(TripID),
    FOREIGN KEY(DestinationID) REFERENCES Destination(DestinationID)
);

CREATE TABLE ActivityExpense(
    ActivityID INT PRIMARY KEY,
    TotalExpenseID INT,
    Amount DECIMAL(10, 2),
    ExpenseDescription VARCHAR(150),
    FOREIGN KEY(TotalExpenseID) REFERENCES TotalExpense(TotalExpenseID),
    FOREIGN KEY(ActivityID) REFERENCES Activity(ActivityID)
);

CREATE TABLE Transportation(
    TransportationID INT PRIMARY KEY AUTO_INCREMENT,
    TripID INT,
    StartDate DATE,
    Duration INT,
    StartingPoint VARCHAR(150),
    EndingPoint VARCHAR(150),
    TransportationType VARCHAR(50),
    FOREIGN KEY(TripID) REFERENCES Trip(TripID)
);

CREATE TABLE TransportationExpense(
    TransportationID INT PRIMARY KEY,
    TotalExpenseID INT,
    Amount DECIMAL(10, 2),
    ExpenseDescription VARCHAR(150),
    FOREIGN KEY(TotalExpenseID) REFERENCES TotalExpense(TotalExpenseID),
    FOREIGN KEY(TransportationID) REFERENCES Transportation(TransportationID)
);

CREATE TABLE Hotel(
    HotelID INT PRIMARY KEY AUTO_INCREMENT,
    HotelName VARCHAR(150),
    HotelAddress VARCHAR(150),
    RoomDescription VARCHAR(500)
);

CREATE TABLE Accommodation(
    AccommodationID INT PRIMARY KEY AUTO_INCREMENT,
    TripID INT,
    HotelID INT,
    CheckInDate DATE,
    CheckOutDate DATE,
    FOREIGN KEY(TripID) REFERENCES Trip(TripID),
    FOREIGN KEY(HotelID) REFERENCES Hotel(HotelID)
);

CREATE TABLE AccommodationExpense(
    AccommodationID INT PRIMARY KEY,
    TotalExpenseID INT,
    Amount DECIMAL(10, 2),
    ExpenseDescription VARCHAR(150),
    FOREIGN KEY(TotalExpenseID) REFERENCES TotalExpense(TotalExpenseID),
    FOREIGN KEY(AccommodationID) REFERENCES Accommodation(AccommodationID)
);