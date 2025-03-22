CREATE TABLE customers (
    customer_id VARCHAR(255) PRIMARY KEY, 
    customer_name VARCHAR(255) NOT NULL,
    age INT CHECK (age >= 0),            
    gender VARCHAR(10) CHECK (gender IN ('Male', 'Female', 'Other')),
    email VARCHAR(255) UNIQUE,           
    city VARCHAR(255),
    country VARCHAR(255)
);


CREATE TABLE products (
    product_id VARCHAR(50) PRIMARY KEY,   
    product_name VARCHAR(255) NOT NULL,
    category VARCHAR(100),
    price NUMERIC(10, 2) CHECK (price >= 0),  
    cost NUMERIC(10, 2) CHECK (cost >= 0)    
);


CREATE TABLE sales (
    sale_id VARCHAR(50) PRIMARY KEY,               
    product_id VARCHAR(50) NOT NULL,     
    customer_id VARCHAR(255) NOT NULL,    
    quantity INT CHECK (quantity > 0),    
    sale_date DATE NOT NULL,              
    price NUMERIC(10, 2) CHECK (price >= 0),

    CONSTRAINT fk_product
        FOREIGN KEY (product_id)
        REFERENCES products(product_id)
        ON DELETE CASCADE,

    CONSTRAINT fk_customer
        FOREIGN KEY (customer_id)
        REFERENCES customers(customer_id)
        ON DELETE CASCADE
);
