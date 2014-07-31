* What's this ?
** python profram to start and stop mysql automatically
** Create some tables use 'test' database
** it's just for deploying my unitest mysql, you can modify it to for your own

* Required ?
** Make sure python installed
** Make sure MySQLdb module installed

* Attention
** the program download mysql-xx-xx.tar.gz from an url, encoded in code, u can change it

* example
1. Start mysql under ./tmp () on port 4338
   python start_mysql.py -d ./tmp -p 4338 
or
   python start_mysql.py --dir=./tmp --port=4338

2. Stop mysql we stared above
   python stop_mysql.py --dir=./tmp/ --port=4338
or
   python stop_mysql.py --D   ./tmp/ -p 4338
     
   
