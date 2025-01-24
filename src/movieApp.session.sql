-- @block
CREATE TABLE users(
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(255),
    password CHAR(102)
);

-- @block
ALTER TABLE users
ADD COLUMN fullname VARCHAR(255)


-- @block
INSERT INTO users(username,password,fullname)
VALUES(
    'JGOMEZ',
    'scrypt:32768:8:1$bIziB0bPpZLd4mAF$fc3a39293c3f02b7b6c6139b76005021d873378ea3fd865ca7400879c67bd45bc3833977d6e22fa5e5279e125fe1217bb6cb3ac6587c166eff1403ba538d31e0',
    'Jeronimo Gomez'
)

-- @block
INSERT INTO users(username,password,fullname)
VALUES(
    'jeronimo',
    'scrypt:32768:8:1$MDat5EE0IMwhsCXP$fde259387e349e440a9fd6a81569d594c90be6c513e4ad4c8bfc6358b4a25574d76bdeb1020366c33fd53460e346d6d7f612233eb0eba77320717a4a246e99c6',
    'Jeronimo'
)



-- @block
ALTER TABLE users
MODIFY COLUMN password VARCHAR(255);

-- @block
SELECT * FROM users;

