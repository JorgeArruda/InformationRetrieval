# ri-vetorial

# OS dependencies

    tesseract

# OS dependencies for pdftotext (https://github.com/jalan/pdftotext)

Debian, Ubuntu, and friends:

```
sudo apt-get update
sudo apt-get install build-essential libpoppler-cpp-dev pkg-config python-dev
```

Fedora, Red Hat, and friends:

```
sudo yum install gcc-c++ pkgconfig poppler-cpp-devel python-devel redhat-rpm-config
```

macOS:

```
brew install pkg-config poppler
```

# Install python dependences
```
pip3 install -r requirements.txt
```


# Configure mysql user

```
create database ri_vetorial;
create user 'ri_vetorial'@'localhost' identified by '14411441';
grant all privileges on ri_vetorial.* to 'ri_vetorial'@'localhost';
```

```
python manager.py makemigrations
python manager.py migrate
```