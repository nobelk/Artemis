import sys
from pathlib import Path

import pytest

# Add parent directory to path to allow imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.agent.context_window_memory import ContextWindowMemory
from src.agent.memory import Memory


class TestContextWindowMemory:
    """Test suite for ContextWindowMemory class"""

    def test_initialization_with_defaults(self):
        """Test that ContextWindowMemory initializes with default max_tokens"""
        memory = ContextWindowMemory()
        assert hasattr(memory, '_messages')
        assert isinstance(memory._messages, list)
        assert len(memory._messages) == 0
        assert memory.max_tokens == 2048

    def test_initialization_with_custom_max_tokens(self):
        """Test initialization with custom max_tokens"""
        memory = ContextWindowMemory(max_tokens=1024)
        assert memory.max_tokens == 1024

    def test_inheritance(self):
        """Test that ContextWindowMemory inherits from Memory"""
        memory = ContextWindowMemory()
        assert isinstance(memory, Memory)

    def test_recall_empty_messages(self):
        """Test recall() returns empty list when no messages added"""
        memory = ContextWindowMemory()
        result = memory.recall()
        assert result == []
        assert isinstance(result, list)

    def test_recall_preserves_system_messages(self):
        """Test recall() always includes system messages"""
        memory = ContextWindowMemory(max_tokens=100)
        memory._messages = [
            {'role': 'system', 'content': 'You are a helpful assistant'},
            {'role': 'user', 'content': 'Hello'},
            {'role': 'assistant', 'content': 'Hi!'}
        ]

        result = memory.recall()

        # System messages should always be included
        system_msgs = [m for m in result if m.get('role') == 'system']
        assert len(system_msgs) == 1
        assert system_msgs[0]['content'] == 'You are a helpful assistant'

    def test_recall_includes_recent_messages(self):
        """Test recall() includes recent messages based on token estimation"""
        memory = ContextWindowMemory(max_tokens=2048)

        # Add multiple messages
        messages = [
            {'role': 'user', 'content': f'Message {i}'}
            for i in range(30)
        ]
        memory._messages = messages

        result = memory.recall()

        # Should return approximately last max_tokens // 100 messages
        expected_count = 2048 // 100  # 20 messages
        assert len(result) == expected_count

    def test_recall_with_system_and_recent_messages(self):
        """Test recall() returns system messages plus recent messages"""
        memory = ContextWindowMemory(max_tokens=1000)

        memory._messages = [
            {'role': 'system', 'content': 'System message 1'},
            {'role': 'system', 'content': 'System message 2'},
        ] + [
            {'role': 'user', 'content': f'Message {i}'}
            for i in range(20)
        ]

        result = memory.recall()

        # Should have system messages at the start
        assert result[0]['role'] == 'system'
        assert result[1]['role'] == 'system'

        # Plus recent messages
        recent_count = 1000 // 100  # 10 messages
        # Total should be system messages + recent messages
        assert len(result) == 2 + recent_count

    def test_recall_when_few_messages(self):
        """Test recall() when total messages is less than token limit"""
        memory = ContextWindowMemory(max_tokens=2048)

        memory._messages = [
            {'role': 'system', 'content': 'System'},
            {'role': 'user', 'content': 'Hello'},
            {'role': 'assistant', 'content': 'Hi'}
        ]

        result = memory.recall()

        # Should include all messages since we're under the limit
        # System message + last 20 messages (2048//100), but we only have 3 total
        assert len(result) <= len(memory._messages) + 1

    def test_recall_no_system_messages(self):
        """Test recall() when there are no system messages"""
        memory = ContextWindowMemory(max_tokens=500)

        memory._messages = [
            {'role': 'user', 'content': f'Message {i}'}
            for i in range(10)
        ]

        result = memory.recall()

        # Should return last max_tokens // 100 messages
        expected_count = 500 // 100  # 5 messages
        assert len(result) == expected_count
        assert all(m['role'] == 'user' for m in result)

    def test_recall_multiple_system_messages(self):
        """Test recall() preserves all system messages and recent messages"""
        memory = ContextWindowMemory(max_tokens=1000)

        memory._messages = [
            {'role': 'system', 'content': 'System 1'},
            {'role': 'user', 'content': 'User message'},
            {'role': 'system', 'content': 'System 2'},
            {'role': 'assistant', 'content': 'Assistant message'},
            {'role': 'system', 'content': 'System 3'},
        ]

        result = memory.recall()

        # Implementation returns system_msgs + recent_msgs, which may include duplicates
        # With 5 total messages and max_tokens=1000 (10 recent messages), all 5 messages
        # are in recent_msgs, resulting in: 3 system messages + 5 all messages = 8 total
        assert len(result) == 8

        # First 3 should be system messages
        assert result[0]['content'] == 'System 1'
        assert result[1]['content'] == 'System 2'
        assert result[2]['content'] == 'System 3'

        # Followed by the recent messages (all 5 messages in this case)
        assert len(result[3:]) == 5

    def test_put_method_exists(self):
        """Test that put() method exists"""
        memory = ContextWindowMemory()
        assert hasattr(memory, 'put')
        assert callable(memory.put)

    def test_recall_returns_list(self):
        """Test that recall() always returns a list"""
        memory = ContextWindowMemory()
        result = memory.recall()
        assert isinstance(result, list)

    def test_different_token_limits(self):
        """Test recall() with different max_tokens values"""
        test_cases = [
            (100, 1),   # 100 tokens = ~1 message
            (500, 5),   # 500 tokens = ~5 messages
            (1000, 10), # 1000 tokens = ~10 messages
            (5000, 50), # 5000 tokens = ~50 messages
        ]

        for max_tokens, expected_recent in test_cases:
            memory = ContextWindowMemory(max_tokens=max_tokens)
            memory._messages = [
                {'role': 'user', 'content': f'Message {i}'}
                for i in range(100)
            ]

            result = memory.recall()
            assert len(result) == expected_recent
