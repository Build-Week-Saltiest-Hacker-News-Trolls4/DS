def push_heroku(df):
        # Push to backend

        # Needs df
        df.to_csv('output/top_20.csv', index=False)

        # Put above later
        import sqlite3
        import psycopg2

        # Store elsewhere
        dbname = ''
        user = ''
        password = ''
        host = ''

        pg_conn = psycopg2.connect(dbname=dbname,user=user,password=password,host=host)
        pg_curs = pg_conn.cursor()

        # Set table features
        create_top_20_users = '''
            CREATE TABLE top_20_users (
            comment_ID SERIAL PRIMARY KEY,
            author VARCHAR(100),
            comment_Text VARCHAR(1000), # need to figure out how to better set upper limit
            time DATE,
            neg FLOAT,
            pos FLOAT,
            neu FLOAT
        )
        '''
        #pg_curs.execute('DROP TABLE top_20_users')
        #pg_curs.execute("ROLLBACK")

        pg_curs.execute(create_top_20_users)

        # Put above
        import csv

        # Check save time
        start = time.time()

        # Store from saved csv file
        with open('output/???.csv', newline='') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Skip first row of column names
            for row in reader:
                pg_curs.execute('INSERT INTO top_20_users \
                        (%s, %s, %s, %s, %s, %s, %s)', row)
        
        end = time.time()
        print(end - start)



        return 0