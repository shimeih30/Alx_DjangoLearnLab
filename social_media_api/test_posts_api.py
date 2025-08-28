"""
Test script for Posts and Comments API endpoints
Run this script to test the API functionality
"""

import requests
import json

# Base URL for your API
BASE_URL = "http://localhost:8000/api"

# Test user credentials (create these users first)
TEST_USER_1 = {
    "username": "testuser1",
    "password": "testpass123"
}

TEST_USER_2 = {
    "username": "testuser2", 
    "password": "testpass123"
}

def register_test_user(user_data):
    """Register a test user"""
    data = {
        **user_data,
        "email": f"{user_data['username']}@example.com",
        "password_confirm": user_data['password'],
        "first_name": "Test",
        "last_name": "User"
    }
    
    response = requests.post(f"{BASE_URL}/register/", json=data)
    print(f"Register {user_data['username']}: {response.status_code}")
    if response.status_code == 201:
        return response.json()['token']
    return None

def login_user(user_data):
    """Login and get token"""
    response = requests.post(f"{BASE_URL}/login/", json=user_data)
    print(f"Login {user_data['username']}: {response.status_code}")
    if response.status_code == 200:
        return response.json()['token']
    return None

def test_posts_crud(token):
    """Test Posts CRUD operations"""
    headers = {"Authorization": f"Token {token}"}
    
    # Create a post
    post_data = {
        "title": "My First Post",
        "content": "This is the content of my first post. It's quite exciting!"
    }
    response = requests.post(f"{BASE_URL}/posts/", json=post_data, headers=headers)
    print(f"Create Post: {response.status_code}")
    if response.status_code == 201:
        post_id = response.json()['id']
        print(f"Created post with ID: {post_id}")
    else:
        print(f"Error creating post: {response.text}")
        return None
    
    # Get all posts
    response = requests.get(f"{BASE_URL}/posts/", headers=headers)
    print(f"Get All Posts: {response.status_code}")
    if response.status_code == 200:
        posts = response.json()
        print(f"Found {posts['count']} posts")
    
    # Get specific post
    response = requests.get(f"{BASE_URL}/posts/{post_id}/", headers=headers)
    print(f"Get Single Post: {response.status_code}")
    if response.status_code == 200:
        post = response.json()
        print(f"Post title: {post['title']}")
    
    # Update post
    update_data = {
        "title": "My Updated Post",
        "content": "This content has been updated!"
    }
    response = requests.put(f"{BASE_URL}/posts/{post_id}/", json=update_data, headers=headers)
    print(f"Update Post: {response.status_code}")
    
    return post_id

def test_comments_crud(token, post_id):
    """Test Comments CRUD operations"""
    headers = {"Authorization": f"Token {token}"}
    
    # Add comment to post
    comment_data = {"content": "This is a great post!"}
    response = requests.post(f"{BASE_URL}/posts/{post_id}/add_comment/", json=comment_data, headers=headers)
    print(f"Add Comment: {response.status_code}")
    if response.status_code == 201:
        comment_id = response.json()['id']
        print(f"Created comment with ID: {comment_id}")
    else:
        print(f"Error adding comment: {response.text}")
        return None
    
    # Get comments for post
    response = requests.get(f"{BASE_URL}/posts/{post_id}/comments/", headers=headers)
    print(f"Get Post Comments: {response.status_code}")
    if response.status_code == 200:
        comments = response.json()
        print(f"Found {len(comments)} comments")
    
    # Get all comments
    response = requests.get(f"{BASE_URL}/comments/", headers=headers)
    print(f"Get All Comments: {response.status_code}")
    
    # Update comment
    update_data = {"content": "This is an updated comment!"}
    response = requests.put(f"{BASE_URL}/comments/{comment_id}/", json=update_data, headers=headers)
    print(f"Update Comment: {response.status_code}")
    
    return comment_id

def test_search_and_filter(token):
    """Test search and filtering"""
    headers = {"Authorization": f"Token {token}"}
    
    # Search posts by title
    response = requests.get(f"{BASE_URL}/posts/?search=Updated", headers=headers)
    print(f"Search Posts: {response.status_code}")
    
    # Filter posts by author
    response = requests.get(f"{BASE_URL}/posts/?author=1", headers=headers)
    print(f"Filter Posts by Author: {response.status_code}")
    
    # Get my posts
    response = requests.get(f"{BASE_URL}/posts/my_posts/", headers=headers)
    print(f"Get My Posts: {response.status_code}")

def test_permissions(token1, token2, post_id, comment_id):
    """Test permissions - user2 shouldn't be able to edit user1's content"""
    headers = {"Authorization": f"Token {token2}"}
    
    # Try to update another user's post
    update_data = {"title": "Hacked Post", "content": "This should not work!"}
    response = requests.put(f"{BASE_URL}/posts/{post_id}/", json=update_data, headers=headers)
    print(f"Try to Update Other User's Post: {response.status_code} (Should be 403)")
    
    # Try to delete another user's comment
    response = requests.delete(f"{BASE_URL}/comments/{comment_id}/", headers=headers)
    print(f"Try to Delete Other User's Comment: {response.status_code} (Should be 403)")

def main():
    """Run all tests"""
    print("=== Social Media API - Posts & Comments Testing ===\n")
    
    # Register or login test users
    token1 = register_test_user(TEST_USER_1) or login_user(TEST_USER_1)
    token2 = register_test_user(TEST_USER_2) or login_user(TEST_USER_2)
    
    if not token1 or not token2:
        print("Failed to get authentication tokens")
        return
    
    print(f"\nUser 1 Token: {token1[:20]}...")
    print(f"User 2 Token: {token2[:20]}...\n")
    
    # Test Posts