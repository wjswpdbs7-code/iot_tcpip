pip install flask
pip install flask-mysqldb 
pip install werkzeug 
pip install python-dotenv 


auto_increment는 MySQL에서 사용하는 키워드로, 해당 컬럼의 값이 자동으로 증가하도록 설정하는 기능입니다. 이를 통해 새로운 레코드가 추가될 때마다 고유한 값을 자동으로 생성할 수 있습니다. 
예를 들어, bookid 컬럼에 auto_increment를 설정하면 새로운 책이 추가될 때마다 bookid 값이 자동으로 1씩 증가하여 고유한 식별자가 됩니다.
on DELETE CASCADE: 책이나 고객이 사라지면 관련된 주문도 자동으로 삭제되도록 설정하는 옵션입니다

create database bookstore_flask; 
use bookstore_flask;

CREATE TABLE book(
    bookid int primary key auto_increment, 
    bookname varchar(40) not null,
    publisher varchar(40) not null,
    price int
);

CREATE TABLE customer(
    custid int primary key auto_increment,
    name varchar(40) not null,
    address varchar(40),
    phone varchar(40),
    password varchar(255) not null
);

CREATE TABLE orders(
    orderid int primary key auto_increment,
    custid int,
    bookid int,
    saleprice int,
    orderdate date,
    FOREIGN KEY (custid) REFERENCES customer(custid) ON DELETE CASCADE,
    FOREIGN KEY (bookid) REFERENCES book(bookid) ON DELETE CASCADE
);


