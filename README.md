# Project: Item Catalog
This is the third project of [Udacity](https://www.udacity.com): [Full Stack Web Developer Nanodegree](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd004)

**by Alan Po-Ching**

# About the project
Design and implement a database driven catalog website that allows user to create and manage their own items after logining via google+ or facebook. The theme for this website is *"cafe"*.

# Libraries and Dependencies
* Python 2
* SQLAlchemy, Flask

Install Vagrant, VirtualBox and clone [fullstack-nanodegree-vm](https://github.com/udacity/fullstack-nanodegree-vm), run `vagrant up` to get your environment set up.

# OAuth2.0 Providers      
* [Google+](https://developers.google.com/identity/protocols/OAuth2)
* [Facebook](https://developers.facebook.com/docs/facebook-login/)

# Getting Started
1. Download this repo and extract the files into fullstack-nanodegree-vm/vagrant/catalog/ directory.
2. Run `vagrant up` to start your virtual machine.
3. Run `vagrant ssh` to log on to the virtual machine.
4. Move to the /vagrant/catalog/ directory.
5. Run `python database_setup.py` to setup the project database.
6. Populate the database by running `python populate_db_items.py`
7. Run `python project.py` start the application.
8. Access the website via  [http://localhost:8000](http://localhost:8000).
