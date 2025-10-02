# attendance-project

# PYTHON INSTALL
py -m pip install -r requirement.txt
py -m pip install opencv-contrib-python --default-timeout=1000
py -m pip install mysql-connector-python
py -m pip install pillow



https://github.com/opencv/opencv/blob/master/data/haarcascades/haarcascade_frontalface_default.xml


# SQL FiX

mysql -u root -p

-- Create a user named 'attendance' that can connect from anywhere
CREATE USER 'attendance'@'%' IDENTIFIED BY 'yourpassword';

-- Give this user access to your database
GRANT ALL PRIVILEGES ON attendance_db.* TO 'attendance'@'%';

-- Apply changes
FLUSH PRIVILEGES;