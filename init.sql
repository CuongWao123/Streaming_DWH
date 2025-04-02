-- CREATE TABLE customers (
--     customer_id VARCHAR(255) PRIMARY KEY, 
--     customer_name VARCHAR(255) NOT NULL,
--     age INT CHECK (age >= 0),            
--     gender VARCHAR(10) CHECK (gender IN ('Male', 'Female', 'Other')),
--     email VARCHAR(255) UNIQUE,           
--     city VARCHAR(255),
--     country VARCHAR(255)
-- );


-- CREATE TABLE products (
--     product_id VARCHAR(50) PRIMARY KEY,   
--     product_name VARCHAR(255) NOT NULL,
--     category VARCHAR(100),
--     price NUMERIC(10, 2) CHECK (price >= 0),  
--     cost NUMERIC(10, 2) CHECK (cost >= 0)    
-- );


-- CREATE TABLE sales (
--     sale_id VARCHAR(50) PRIMARY KEY,               
--     product_id VARCHAR(50) NOT NULL,     
--     customer_id VARCHAR(255) NOT NULL,    
--     quantity INT CHECK (quantity > 0),    
--     sale_date DATE NOT NULL,              
--     price NUMERIC(10, 2) CHECK (price >= 0),

--     CONSTRAINT fk_product
--         FOREIGN KEY (product_id)
--         REFERENCES products(product_id)
--         ON DELETE CASCADE,

--     CONSTRAINT fk_customer
--         FOREIGN KEY (customer_id)
--         REFERENCES customers(customer_id)
--         ON DELETE CASCADE
-- );





-- DROP TABLES FIRST (Optional - để rollback và tạo lại dễ dàng)
DROP TABLE IF EXISTS data;
DROP TABLE IF EXISTS current;
DROP TABLE IF EXISTS current_air_quality;
DROP TABLE IF EXISTS current_astro;
DROP TABLE IF EXISTS location;
DROP TABLE IF EXISTS request;

-- ====================
-- TABLE: request
-- ====================
CREATE TABLE request (
    request_id VARCHAR(50) PRIMARY KEY,
    type VARCHAR(50),
    language VARCHAR(10),
    unit VARCHAR(10)
);

-- ====================
-- TABLE: location
-- ====================
CREATE TABLE location (
    location_id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(255),
    country VARCHAR(255),
    lat DECIMAL(10,6),
    lon DECIMAL(10,6),
    localtime TIMESTAMP
);

-- ====================
-- TABLE: current_air_quality
-- ====================
CREATE TABLE current_air_quality (
    quality_id VARCHAR(50) PRIMARY KEY,
    co DECIMAL(10,2),
    no2 DECIMAL(10,2),
    o3 DECIMAL(10,2),
    so2 DECIMAL(10,2),
    pm2_5 DECIMAL(10,2),
    pm10 DECIMAL(10,2)
);

-- ====================
-- TABLE: current_astro
-- ====================
CREATE TABLE current_astro (
    astro_id VARCHAR(50) PRIMARY KEY,
    sunrise TIME,
    sunset TIME,
    moonrise TIME,
    moonset TIME,
    moon_phase VARCHAR(50),
    moon_illumination DECIMAL(5,2)
);

-- ====================
-- TABLE: current
-- ====================
CREATE TABLE current (
    current_id VARCHAR(50) PRIMARY KEY,
    observation_time TIME,
    temperature INTEGER,
    wind_speed INTEGER,
    wind_degree INTEGER,
    wind_dir VARCHAR(10),
    pressure INTEGER,
    precip INTEGER,
    humidity INTEGER,
    cloudcover INTEGER,
    feelslike INTEGER,
    uv_index INTEGER,
    visibility INTEGER,
    astro_id UUID,
    quality_id UUID,

    -- FOREIGN KEYS
    CONSTRAINT fk_astro FOREIGN KEY (astro_id)
        REFERENCES current_astro (astro_id)
        ON DELETE CASCADE,
    
    CONSTRAINT fk_quality FOREIGN KEY (quality_id)
        REFERENCES current_air_quality (quality_id)
        ON DELETE CASCADE
);

-- ====================
-- TABLE: data (Trung gian)
-- ====================
CREATE TABLE datas (
    data_id VARCHAR(50) PRIMARY KEY,

    request_id VARCHAR(50),
    location_id VARCHAR(50),
    current_id VARCHAR(50),

    -- FOREIGN KEYS
    CONSTRAINT fk_request FOREIGN KEY (request_id)
        REFERENCES request (request_id)
        ON DELETE CASCADE,

    CONSTRAINT fk_location FOREIGN KEY (location_id)
        REFERENCES location (location_id)
        ON DELETE CASCADE,

    CONSTRAINT fk_current FOREIGN KEY (current_id)
        REFERENCES current (current_id)
        ON DELETE CASCADE
);


