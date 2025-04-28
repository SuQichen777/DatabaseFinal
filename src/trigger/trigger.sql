DROP TRIGGER IF EXISTS trg_update_total_expense_after_transport_insert;
CREATE TRIGGER trg_update_total_expense_after_transport_insert
AFTER INSERT ON TransportationExpense
FOR EACH ROW
BEGIN
    UPDATE TotalExpense
    SET Amount = (
        (SELECT IFNULL(SUM(Amount), 0) FROM TransportationExpense WHERE TotalExpenseID = NEW.TotalExpenseID)
      + (SELECT IFNULL(SUM(Amount), 0) FROM AccommodationExpense WHERE TotalExpenseID = NEW.TotalExpenseID)
      + (SELECT IFNULL(SUM(Amount), 0) FROM ActivityExpense WHERE TotalExpenseID = NEW.TotalExpenseID)
    )
    WHERE TotalExpenseID = NEW.TotalExpenseID;
END;

DROP TRIGGER IF EXISTS trg_update_total_expense_after_transport_update;
CREATE TRIGGER trg_update_total_expense_after_transport_update
AFTER UPDATE ON TransportationExpense
FOR EACH ROW
BEGIN
    UPDATE TotalExpense
    SET Amount = (
        (SELECT IFNULL(SUM(Amount), 0) FROM TransportationExpense WHERE TotalExpenseID = NEW.TotalExpenseID)
      + (SELECT IFNULL(SUM(Amount), 0) FROM AccommodationExpense WHERE TotalExpenseID = NEW.TotalExpenseID)
      + (SELECT IFNULL(SUM(Amount), 0) FROM ActivityExpense WHERE TotalExpenseID = NEW.TotalExpenseID)
    )
    WHERE TotalExpenseID = NEW.TotalExpenseID;
END;

DROP TRIGGER IF EXISTS trg_update_total_expense_after_accommodation_insert;
CREATE TRIGGER trg_update_total_expense_after_accommodation_insert
AFTER INSERT ON AccommodationExpense
FOR EACH ROW
BEGIN
    UPDATE TotalExpense
    SET Amount = (
        (SELECT IFNULL(SUM(Amount), 0) FROM TransportationExpense WHERE TotalExpenseID = NEW.TotalExpenseID)
      + (SELECT IFNULL(SUM(Amount), 0) FROM AccommodationExpense WHERE TotalExpenseID = NEW.TotalExpenseID)
      + (SELECT IFNULL(SUM(Amount), 0) FROM ActivityExpense WHERE TotalExpenseID = NEW.TotalExpenseID)
    )
    WHERE TotalExpenseID = NEW.TotalExpenseID;
END;

DROP TRIGGER IF EXISTS trg_update_total_expense_after_accommodation_update;
CREATE TRIGGER trg_update_total_expense_after_accommodation_update
AFTER UPDATE ON AccommodationExpense
FOR EACH ROW
BEGIN
    UPDATE TotalExpense
    SET Amount = (
        (SELECT IFNULL(SUM(Amount), 0) FROM TransportationExpense WHERE TotalExpenseID = NEW.TotalExpenseID)
      + (SELECT IFNULL(SUM(Amount), 0) FROM AccommodationExpense WHERE TotalExpenseID = NEW.TotalExpenseID)
      + (SELECT IFNULL(SUM(Amount), 0) FROM ActivityExpense WHERE TotalExpenseID = NEW.TotalExpenseID)
    )
    WHERE TotalExpenseID = NEW.TotalExpenseID;
END;

DROP TRIGGER IF EXISTS trg_update_total_expense_after_activity_insert;
CREATE TRIGGER trg_update_total_expense_after_activity_insert
AFTER INSERT ON ActivityExpense
FOR EACH ROW
BEGIN
    UPDATE TotalExpense
    SET Amount = (
        (SELECT IFNULL(SUM(Amount), 0) FROM TransportationExpense WHERE TotalExpenseID = NEW.TotalExpenseID)
      + (SELECT IFNULL(SUM(Amount), 0) FROM AccommodationExpense WHERE TotalExpenseID = NEW.TotalExpenseID)
      + (SELECT IFNULL(SUM(Amount), 0) FROM ActivityExpense WHERE TotalExpenseID = NEW.TotalExpenseID)
    )
    WHERE TotalExpenseID = NEW.TotalExpenseID;
END;

DROP TRIGGER IF EXISTS trg_update_total_expense_after_activity_update;
CREATE TRIGGER trg_update_total_expense_after_activity_update
AFTER UPDATE ON ActivityExpense
FOR EACH ROW
BEGIN
    UPDATE TotalExpense
    SET Amount = (
        (SELECT IFNULL(SUM(Amount), 0) FROM TransportationExpense WHERE TotalExpenseID = NEW.TotalExpenseID)
      + (SELECT IFNULL(SUM(Amount), 0) FROM AccommodationExpense WHERE TotalExpenseID = NEW.TotalExpenseID)
      + (SELECT IFNULL(SUM(Amount), 0) FROM ActivityExpense WHERE TotalExpenseID = NEW.TotalExpenseID)
    )
    WHERE TotalExpenseID = NEW.TotalExpenseID;
END;
