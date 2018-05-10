# ri-vetorial

# System dependence
    tesseract

# Install python dependences
pip3 install -r requirements.txt

# Configure mysql user
create user 'ri_vetorial'@'localhost' identified by '14411441';
grant all privileges on ri_vetorial.* to 'ri_vetorial'@'localhost';
