"""
Utility module for loading test data from JSON and CSV files
"""

import json
import csv
import os
from typing import Dict, List, Any, Optional, Union


class TestDataLoader:
    """Loads and provides access to test data from JSON and CSV files"""

    _instance = None
    _users_data = None
    _checkout_data = None

    def __new__(cls):
        """Singleton pattern to ensure data is loaded only once"""
        if cls._instance is None:
            cls._instance = super(TestDataLoader, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        """Initialize the test data loader"""
        if self._users_data is None:
            self._load_users_data()
        if self._checkout_data is None:
            self._load_checkout_data()

    def _load_users_data(self):
        """Load users data from users.json file"""
        # Get the project root directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(current_dir))
        users_json_path = os.path.join(project_root, 'data', 'users.json')

        try:
            with open(users_json_path, 'r') as file:
                self._users_data = json.load(file)
        except FileNotFoundError:
            print(f"Warning: users.json not found at {users_json_path}")
            self._users_data = {}

    def _load_checkout_data(self):
        """Load checkout data from checkout_data.csv file"""
        # Get the project root directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(current_dir))
        
        # Try multiple possible locations for the CSV file
        possible_paths = [
            os.path.join(project_root, 'data', 'checkout_data.csv'),
            os.path.join(project_root, 'src', 'utils', 'checkout_data.csv'),
            os.path.join(project_root, 'checkout_data.csv'),
        ]
        
        csv_path = None
        for path in possible_paths:
            if os.path.exists(path):
                csv_path = path
                break
        
        if csv_path is None:
            print(f"Warning: checkout_data.csv not found in any of these locations:")
            for path in possible_paths:
                print(f"  - {path}")
            self._checkout_data = []
            return
        
        try:
            with open(csv_path, 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                self._checkout_data = list(reader)
        except Exception as e:
            print(f"Warning: Error loading checkout_data.csv: {e}")
            self._checkout_data = []
    
    def get_valid_users(self) -> List[Dict[str, Any]]:
        """Get all valid users"""
        if self._users_data is None:
            return []
        return self._users_data.get('valid_users', [])

    def get_locked_users(self) -> List[Dict[str, Any]]:
        """Get all locked users"""
        if self._users_data is None:
            return []
        return self._users_data.get('locked_users', [])

    def get_invalid_credentials(self) -> List[Dict[str, Any]]:
        """Get all invalid credential combinations"""
        if self._users_data is None:
            return []
        return self._users_data.get('invalid_credentials', [])

    def get_empty_credentials(self) -> List[Dict[str, Any]]:
        """Get all empty credential combinations"""
        if self._users_data is None:
            return []
        return self._users_data.get('empty_credentials', [])

    def get_user_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        """Get user data by username from all categories"""
        all_users = (
            self.get_valid_users() +
            self.get_locked_users() +
            self.get_invalid_credentials() +
            self.get_empty_credentials()
        )

        for user in all_users:
            if user.get('username') == username:
                return user

        return None

    def get_credentials(self, username: str) -> tuple:
        """
        Get username and password tuple for a given username
        Returns: (username, password)
        """
        user = self.get_user_by_username(username)
        if user:
            return (user.get('username', ''), user.get('password', ''))
        return (username, '')

    def get_expected_error(self, username: str) -> str:
        """Get the expected error message for a given username"""
        user = self.get_user_by_username(username)
        if user:
            return user.get('expected_error', '')
        return ''

    def get_user_credentials(self, user_type: str = "standard") -> Dict[str, str]:
        """
        Get user credentials by type (compatible with config.py interface)

        Args:
            user_type: Type of user (standard, problem, performance_glitch, error, visual, locked_out)

        Returns:
            Dict with username and password keys

        Example:
            >>> test_data.get_user_credentials("standard")
            {'username': 'standard_user', 'password': 'secret_sauce'}
        """
        # Map user types to full usernames
        user_mapping = {
            "standard": "standard_user",
            "problem": "problem_user",
            "performance_glitch": "performance_glitch_user",
            "error": "error_user",
            "visual": "visual_user",
            "locked_out": "locked_out_user"
        }

        username = user_mapping.get(user_type.lower())

        if not username:
            raise ValueError(f"Unknown user type: {user_type}")

        # Get user data from users.json
        user_data = self.get_user_by_username(username)

        if not user_data:
            raise ValueError(f"User type '{user_type}' not found in users.json")

        return {
            "username": user_data["username"],
            "password": user_data["password"]
        }

    def get_checkout_data(self, index: Optional[int] = None) -> Union[Optional[Dict[str, Any]], List[Dict[str, Any]]]:
        """
        Get checkout customer data from CSV
        
        Args:
            index (int, optional): Index of customer data to retrieve. 
                                   If None, returns all customers.
        
        Returns:
            dict or list: Single customer dict if index provided, 
                         otherwise list of all customers
        
        Example:
            >>> test_data.get_checkout_data(0)
            {'first_name': 'John', 'last_name': 'Doe', 'postal_code': '12345', ...}
            
            >>> test_data.get_checkout_data()
            [{'first_name': 'John', ...}, {'first_name': 'Jane', ...}, ...]
        """
        if self._checkout_data is None or len(self._checkout_data) == 0:
            return [] if index is None else None
        
        if index is not None:
            if 0 <= index < len(self._checkout_data):
                return self._checkout_data[index]
            else:
                print(f"Warning: Index {index} out of range. Available: 0-{len(self._checkout_data)-1}")
                return None
        
        return self._checkout_data
    
    def get_checkout_data_by_description(self, description: str) -> Optional[Dict[str, Any]]:
        """
        Get checkout customer data by description
        
        Args:
            description (str): Description to search for (e.g., 'Standard US customer')
        
        Returns:
            dict: Customer data matching the description, or None if not found
        
        Example:
            >>> test_data.get_checkout_data_by_description('Standard US customer')
            {'first_name': 'John', 'last_name': 'Doe', 'postal_code': '12345', ...}
        """
        if self._checkout_data is None:
            return None
        
        for customer in self._checkout_data:
            if customer.get('description', '').lower() == description.lower():
                return customer
        
        print(f"Warning: No customer found with description: '{description}'")
        return None
    
    def get_all_checkout_customers(self) -> List[Dict[str, Any]]:
        """
        Get all checkout customer data
        
        Returns:
            list: List of all customer dictionaries
        """
        return self._checkout_data if self._checkout_data is not None else []
    
    def reload_checkout_data(self):
        """Reload checkout data from CSV (useful for testing or dynamic updates)"""
        self._checkout_data = None
        self._load_checkout_data()
    
    def reload_users_data(self):
        """Reload users data from JSON (useful for testing or dynamic updates)"""
        self._users_data = None
        self._load_users_data()


# Singleton instance
test_data = TestDataLoader()