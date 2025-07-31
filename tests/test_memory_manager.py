# src/tests/test_memory_manager.py
import os
import pytest
from src.memory_manager import MemoryManager

# Define a test file path that we can clean up later
TEST_MEMORY_FILE = "test_memory.json"

@pytest.fixture
def memory_manager():
    """
    This is a pytest "fixture". It sets up an object for our tests to use.
    It runs before each test function and handles cleanup afterwards.
    """
    # --- Setup ---
    # Ensure there's no old test file before we start
    if os.path.exists(TEST_MEMORY_FILE):
        os.remove(TEST_MEMORY_FILE)
    
    manager = MemoryManager(file_path=TEST_MEMORY_FILE)
    
    # This 'yield' passes the manager object to the test function
    yield manager
    
    # --- Teardown ---
    # This code runs after the test is complete to clean up
    if os.path.exists(TEST_MEMORY_FILE):
        os.remove(TEST_MEMORY_FILE)

def test_add_and_get_memory(memory_manager):
    """Tests if adding a memory correctly stores it."""
    assert memory_manager.get_all_memories() == []  # Should be empty initially
    
    memory_content = "The user's favorite color is blue."
    memory_manager.add_memory(memory_content)
    
    memories = memory_manager.get_all_memories()
    assert len(memories) == 1
    assert memories[0]["content"] == memory_content

def test_delete_memory(memory_manager):
    """Tests if deleting a memory correctly removes it."""
    memory_manager.add_memory("Fact A: The user owns a cat.")
    memory_manager.add_memory("Fact B: The user lives in London.")
    
    assert len(memory_manager.get_all_memories()) == 2
    
    # Delete based on a keyword
    memory_manager.delete_memory("cat")
    
    memories = memory_manager.get_all_memories()
    assert len(memories) == 1
    assert memories[0]["content"] == "Fact B: The user lives in London."

def test_delete_nonexistent_memory(memory_manager):
    """Tests that attempting to delete something not there doesn't cause an error."""
    memory_manager.add_memory("The user is learning Python.")
    initial_memories = memory_manager.get_all_memories()
    
    memory_manager.delete_memory("Java") # Try to delete something that doesn't exist
    
    final_memories = memory_manager.get_all_memories()
    assert initial_memories == final_memories # The memory list should be unchanged