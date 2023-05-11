create table country (
    country_id smallint,
    country_name varchar(50),
    iso_code varchar(3),
    PRIMARY KEY(country_id)
);

create table payment_type (
    payment_type_id smallint,
    payment_type varchar(40),
    payment_tax numeric(15,5),
    PRIMARY KEY(payment_type_id)
);

create table class (
    class_id smallint,
    class_name varchar(15),
    PRIMARY KEY(class_id)
);

create TABLE wallet (
    wallet_id serial,
    wallet_name varchar(256),
    PRIMARY KEY (wallet_id)
)

create table dividends_dates (
    ticker varchar(40),
    date_payment date,
    amount numeric(10,4),
    position numeric(15,5),
    currency varchar(5),
    country_id smallint REFERENCES country,
    class_id smallint REFERENCES class,
    payment_type_id smallint REFERENCES payment_type,
    PRIMARY KEY (date_payment, ticker, amount, position)
);

create table assets (
    company varchar(150),
    ticker varchar(40),
    api_request_ticker varchar(30),
    position int,
    average_price numeric(15,2),
    country_id smallint REFERENCES country,
    class_id smallint REFERENCES class
);


create table stock_daily_price (
    read_date TIMESTAMP,
    ticker varchar(20),
    open_price numeric(15,2),
    high_price numeric(15,2),
    low_price numeric(15,2),
    close_price numeric(15,2),
    volume int,
    PRIMARY KEY (read_date, ticker)
);

CREATE TABLE orders(
    date_order date,
    ticker varchar(20),
    order_direction char(1),
    order_size numeric(10,5),
    price numeric(15,3)
);

INSERT INTO country 
VALUES (1, 'Brasil', 'BR'), (2, 'EUA', 'US');

INSERT INTO payment_type
VALUES (1, 'DIVIDENDOS', 0),
(2, 'JCP', 0.15),
(3, 'RENDIMENTOS', 0),
(4, 'FOREIGN GAINS', 0.3);

INSERT INTO class 
VALUES (1, 'Ação'), (2, 'Fii'), (3, 'REITS'), (4, 'ETF');
