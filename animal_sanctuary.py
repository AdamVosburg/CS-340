# animal_sanctuary.py
from pymongo import MongoClient
from bson.objectid import ObjectId

class AnimalSanctuary:
    """CRUD operations for Animal collection in MongoDB."""

    def __init__(self):
        """Initialize connection to MongoDB."""
        USER = 'aacuser' 
        PASS = 'RighteousFire83!'
        HOST = 'nv-desktop-services.apporto.com'
        PORT = 31024
        DB = 'aac'
        AUTH_DB = 'admin'  # The user is authenticated against the 'admin' database
        COL = 'animals'
        
        try:
            self.client = MongoClient(f'mongodb://{USER}:{PASS}@{HOST}:{PORT}/{DB}?authSource={AUTH_DB}')
            self.database = self.client[DB]
            self.collection = self.database[COL]
            # Test the connection
            self.client.admin.command('ismaster')
            print("MongoDB connection established successfully")
        except Exception as e:
            print(f"Failed to establish connection to MongoDB: {e}")
            raise  # Re-raise the exception to stop execution if connection fails

    def create(self, data):
        """
        Create a new document in the collection.
        Args:
            data (dict): Dictionary of key/value pairs to insert.
        Returns:
            bool: True if insert was successful, False otherwise.
        Raises:
            ValueError: If data is None or empty.
        """
        if not data:
            raise ValueError("Nothing to save, because data parameter is empty")
        print("Attempting to insert document:", data)
        try:
            insert_result = self.collection.insert_one(data)
            print("Insert result:", insert_result.inserted_id)
            return True
        except Exception as e:
            print(f"An error occurred while inserting the document: {e}")
            return False

    def read(self, query):
        """
        Read documents from the collection based on the query.
        Args:
            query (dict): Dictionary of key/value pairs to search for.
        Returns:
            list: List of documents if the query was successful, else an empty list.
        """
        if not query:
            query = {}
        print("Attempting to find documents with query:", query)
        try:
            cursor = self.collection.find(query)
            results = list(cursor)
            print(f"Found {len(results)} documents")
            return results
        except Exception as e:
            print(f"An error occurred while querying the documents: {e}")
            return []

    def update(self, query, update_data):
        """
        Update document(s) in the collection based on the query.
        
        Args:
            query (dict): Dictionary of key/value pairs to search for.
            update_data (dict): Dictionary of key/value pairs to update.
        
        Returns:
            int: The number of documents modified.
        """
        if not query or not update_data:
            return 0
        
        print(f"Attempting to update documents matching query: {query}")
        print(f"Update data: {update_data}")
        
        try:
            result = self.collection.update_many(query, {"$set": update_data})
            print(f"Modified {result.modified_count} document(s)")
            return result.modified_count
        except Exception as e:
            print(f"An error occurred while updating the documents: {e}")
            return 0

    def delete(self, query):
        """
        Delete document(s) from the collection based on the query.
        
        Args:
            query (dict): Dictionary of key/value pairs to search for.
        
        Returns:
            int: The number of documents removed.
        """
        if not query:
            return 0
        
        print(f"Attempting to delete documents matching query: {query}")
        
        try:
            result = self.collection.delete_many(query)
            print(f"Deleted {result.deleted_count} document(s)")
            return result.deleted_count
        except Exception as e:
            print(f"An error occurred while deleting the documents: {e}")
            return 0
