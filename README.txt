To run the client side, cd into the main popcrn folder outside of the internal popcrn folder. Then run python -m SimpleHTTPServer <portnumber>.
Visiting 0.0.0.0:<portnumber> will serve the client side page.

The server requires a lot more processing. For example you would first need to activate the virtual environment. This happens by being in the
popcrn directory and then running source venv/bin/activate. After being in the environment, if mysql is not installed run brew install mysql.

Then run mysql -u root -p. Then you would "create database popcrn". After exiting, 
