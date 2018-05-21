import pymysql
import os

def get_db_connection():
	"""Returns connection object to the mysql application database."""
	connection = pymysql.connect(host=os.environ['DBHOST'],
								port=3306,
			                    user=os.environ['DBUSERNAME'],
			                    password=os.environ['DBPW'],
			                    db='testfcchatbot',
			                    charset='utf8mb4',
			                    cursorclass=pymysql.cursors.DictCursor)	
	return connection

def execute_query(conn, sql, **kwargs):
	"""
	Executes and returns the result of the query specified by the sql parameter.

	Parameters:
		conn - The database connection object.
		sql - The SQL query to be executed.
		kwargs - The keyword arguments specifiying values to be used in the SQL query.

	Returns the result of the query which is either the number of affected rows or 
	the rows selected by the query represented as either a dictionary or a list of
	dictionaries.
	"""
	with conn.cursor() as cursor:
		result = cursor.execute(sql, kwargs)
	return result

#---- Functions for querying the CustomerInformation table ----#

def get_user_information(conn, psid):
	"""
	Returns a dictionary representing a row in the CustomerInformation table.

	Parameters:
		conn - The database connection object.
		psid - The Page-scoped ID number for the user

	"""
	sql = """
			SELECT * FROM CustomerInformation WHERE Psid = %(psid)
		"""
	return execute_query(conn, sql, psid=psid)

def insert_user_information(conn, psid, **kwargs):
	"""
	Inserts a row into the CustomerInformation table.

	Parameters:
		conn - The database connection objects.
		psid - The Page-scoped ID number for the user.
	
	Keyword arguments:
		FirstName 
		LastName
		Email
		Address 
		Phone
	"""
	column_string = "("
	values_string = "("
	for column_name in kwargs:
		column_string += column_name + ", "
		values_string += "%(" + column_name + ", "

	column_string = column_string[:-2] + ");"
	values_string = values_string[:-2] + ");"
	sql = "INSERT INTO CustomerInformation " + column_string + "VALUES " + values_string

	execute_query(conn, sql, **kwargs)


#---- Functions for querying the Messages table ----#

def insert_message(conn, psid, user_message, response, entity=None, value=None):
	"""
	Inserts a row into the Messages table of the database.

	Parameters:
		conn - The database connection object.
		psid - The Page-scoped ID number for the user.
		user_message - The message sent to the chatbot by the user.
		response - The message sent from the chatbot to the user.
		entity - The entity for user_message determiend by witai
		value - The value for user_message determined by witai

	Returns: The number of rows affected by the query.
	"""
	columns_string = "(Psid, ReceivedMessage, SentMessage" + (", Entity" if entity) + (", Value" if value) + ") "
	values_string = "VALUES (%(psid), %(user_message), %(response) " + ('%(entity)' if entity) + ('%(value)' if value) + ";"
	sql = "INSERT INTO Messages " + columns_string + values_string

	kwargs = {'psid': psid, 'user_message': user_message, 'response': response, }
	kwargs['entity'] = entity if entity
	kwargs['value'] = value if value

	return execute_query(conn, sql, **kwargs)


def get_last_message(conn, psid, user_message, response, entity=None, value=None):
	"""
	Returns a dictionary containing the last message and response
	sent to the user with the Page-scoped ID psid. The dictionary also
	contains the entity and value determined by witai for the user message.

	Parameters:
		conn - The database connection object.
		psid - The Page-scoped ID number for the user.

	Returns: Dictionary containing keys 'ReceivedMessage', 'SentMessage',
	'Entity', and 'Value'
	"""
	sql = """
			SELECT ReceivedMessage, SentMessage, Entity, Value 
			FROM Messages
			WHERE Psid = %(psid)
			ORDER BY Created DESC
			LIMIT 1;
		"""
	return execute_query(conn, psid=psid)

def get_all_messages(conn, psid):
	"""
	Returns a list of dictionaries representing all messages and responses 
	for a given user and the entities and values determined by witai for each message.

	Parameters:
		conn - The database connection object.
		psid - The Page-scoepd ID number for the user.

	Returns: List of dictionaries with keys 'ReceivedMessage', 'SentMessage',
	'Entity', and 'value'.
	"""
	sql = """
			SELECT ReceivedMessage, SentMessage, Entity, Value 
			FROM Messages
			WHERE Psid = %(psid)
		"""
	return execute_query(conn, sql, psid=psid)