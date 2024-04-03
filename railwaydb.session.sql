-- @block
CREATE TABLE Locations (
    location_id INT NOT NULL AUTO_INCREMENT,
    location_name VARCHAR(255) NOT NULL,
    address VARCHAR(255),
    city VARCHAR(100),
    state VARCHAR(100),
    zipcode VARCHAR(20),
    PRIMARY KEY (location_id)
);

-- @block NEW ITEMS
CREATE TABLE Items (
    item_id INT NOT NULL AUTO_INCREMENT,
    location_id INT,
    name VARCHAR(255),
    description TEXT,
    GTIN VARCHAR(50),
    SKU VARCHAR(255),
    unit VARCHAR(50),
    weight DECIMAL(10, 2),
    price DECIMAL(10, 2),
    stock INT,
    low_stock_level INT,
    PRIMARY KEY (item_id),
    FOREIGN KEY (location_id) REFERENCES Locations(location_id)
);

-- @block
INSERT INTO Locations (location_name, address, city, state, zipcode)
VALUES
    ('DU', '2100 S University Blvd', 'Denver', 'CO', 80210);

-- @block
-- Inserting data into Items table
INSERT INTO Items (location_id, name, description, GTIN, SKU, unit, weight, price, stock, low_stock_level)
VALUES 
    (1, 'Pork Ribs', 'Description of Pork Ribs', '1234567890123', 'SKU123', 'lbs', 0.00, 0.00, 20, 5),
    (1, 'Chicken Wings', 'Description of Chicken Wings', '1234567890124', 'SKU124', 'lbs', 0.00, 0.00, 15, 5),
    (1, 'Beef Brisket', 'Description of Beef Brisket', '1234567890125', 'SKU125', 'lbs', 0.00, 0.00, 25, 5),
    (1, 'Pulled Pork', 'Description of Pulled Pork', '1234567890126', 'SKU126', 'lbs', 0.00, 0.00, 18, 5),
    (1, 'BBQ Sauce', 'Description of BBQ Sauce', '1234567890127', 'SKU127', 'bottles', 0.00, 0.00, 10, 5),
    (1, 'Potato Salad', 'Description of Potato Salad', '1234567890128', 'SKU128', 'servings', 0.00, 0.00, 30, 10),
    (1, 'Cornbread', 'Description of Cornbread', '1234567890129', 'SKU129', 'pieces', 0.00, 0.00, 40, 15),
    (1, 'Cole Slaw', 'Description of Cole Slaw', '1234567890130', 'SKU130', 'servings', 0.00, 0.00, 25, 10);
