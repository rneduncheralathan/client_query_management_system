import mysql.connector

# Database Connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="cqms"
)

#User Register
def user_register(user_register):
    # print(user_register["user_name"],"rrrrrrrrrrrrrrrrr")
    cursor = conn.cursor()
    query = """INSERT INTO users(user_name,pass_word,user_role) VALUES(%s,%s,%s)"""
    values = (user_register["user_name"],user_register["pass_word"],user_register["user_role"])
    cursor.execute(query,(values),)
    conn.commit()
    cursor.close()


#Fetch Users Data
def fetch_users(as_dict):
    cursor = conn.cursor(dictionary=as_dict)
    cursor.execute("SELECT user_name, pass_word, user_role FROM users")
    results = cursor.fetchall()
    cursor.close()
    return results

#Query Insertion
def query_insertion(query_data):
    cursor = conn.cursor()
    # print(query_data["mail_id"],query_data["mobile_number"],query_data["query_heading"],query_data["query_description"],query_data["query_status"],query_data["query_closed_time"],) 
    cursor.execute("INSERT INTO query_management(mail_id,mobile_number,query_heading,query_description,query_status,query_closed_time) VALUES(%s, %s, %s, %s, %s,%s)", (query_data["mail_id"],query_data["mobile_number"],query_data["query_heading"],query_data["query_description"],query_data["query_status"],query_data["query_closed_time"]))
    conn.commit()
    cursor.close()

# Fetch All Query Data
def fetch_query(as_dict):
    cursor = conn.cursor(dictionary=as_dict)
    cursor.execute("SELECT * FROM query_management")
    results = cursor.fetchall()
    cursor.close()
    return results

# Update to Query Open Status to Close
def update_query(query_id):
    cursor = conn.cursor()
    query = """
        UPDATE query_management 
        SET query_status = "close", query_closed_time = NOW()
        WHERE query_id = %s
    """
    cursor.execute(query, (query_id,))
    conn.commit()
    cursor.close()
