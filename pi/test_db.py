import mysql.connector

db_config = {
    'host': 'localhost',    # your XAMPP/MySQL server IP
    'user': 'pi_user',        # the user you created
    'password': 'your_password',  # ⚠️ must match exactly the password you set
    'database': 'attendance_db'
}

try:
    conn = mysql.connector.connect(**db_config)
    if conn.is_connected():
        print("✅ Successfully connected to the database!")
        cursor = conn.cursor()
        cursor.execute("SHOW TABLES;")
        print("Available tables:", cursor.fetchall())
        cursor.close()
        conn.close()
except Exception as e:
    print("❌ Error connecting to database:", e)
