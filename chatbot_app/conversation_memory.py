"""
Conversation Memory System for Human-like Interactions
"""
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any
import sqlite3
import os

class ConversationMemory:
    def __init__(self, db_path="conversation_memory.db"):
        self.db_path = db_path
        self.init_database()
        
    def init_database(self):
        """Initialize conversation memory database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Conversation history table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                user_message TEXT,
                bot_response TEXT,
                message_type TEXT,
                timestamp DATETIME,
                user_sentiment TEXT,
                context_tags TEXT,
                importance_score INTEGER DEFAULT 1
            )
        ''')
        
        # User preferences table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_preferences (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                preference_type TEXT,
                preference_value TEXT,
                created_at DATETIME,
                updated_at DATETIME
            )
        ''')
        
        # User profile table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_profiles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT UNIQUE,
                name TEXT,
                interests TEXT,
                communication_style TEXT,
                expertise_level TEXT,
                last_interaction DATETIME,
                interaction_count INTEGER DEFAULT 0
            )
        ''')
        
        conn.commit()
        conn.close()
        print("✅ Conversation memory database initialized")

    def save_conversation(self, session_id: str, user_message: str, bot_response: str, 
                         message_type: str = "general", sentiment: str = "neutral", 
                         context_tags: List[str] = None, importance: int = 1):
        """Save conversation to memory"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO conversations 
            (session_id, user_message, bot_response, message_type, timestamp, user_sentiment, context_tags, importance_score)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            session_id, user_message, bot_response, message_type, 
            datetime.now(), sentiment, json.dumps(context_tags or []), importance
        ))
        
        # Update user interaction count
        cursor.execute('''
            INSERT OR REPLACE INTO user_profiles 
            (session_id, last_interaction, interaction_count)
            VALUES (?, ?, COALESCE((SELECT interaction_count FROM user_profiles WHERE session_id = ?) + 1, 1))
        ''', (session_id, datetime.now(), session_id))
        
        conn.commit()
        conn.close()

    def get_conversation_history(self, session_id: str, limit: int = 10) -> List[Dict]:
        """Get recent conversation history"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT user_message, bot_response, message_type, timestamp, user_sentiment, context_tags
            FROM conversations 
            WHERE session_id = ? 
            ORDER BY timestamp DESC 
            LIMIT ?
        ''', (session_id, limit))
        
        results = cursor.fetchall()
        conn.close()
        
        return [{
            'user_message': r[0],
            'bot_response': r[1],
            'message_type': r[2],
            'timestamp': r[3],
            'sentiment': r[4],
            'context_tags': json.loads(r[5]) if r[5] else []
        } for r in reversed(results)]

    def get_user_context(self, session_id: str) -> Dict[str, Any]:
        """Get user context for personalization"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get user profile
        cursor.execute('SELECT * FROM user_profiles WHERE session_id = ?', (session_id,))
        profile = cursor.fetchone()
        
        # Get recent topics
        cursor.execute('''
            SELECT message_type, COUNT(*) as count
            FROM conversations 
            WHERE session_id = ? AND timestamp > datetime('now', '-7 days')
            GROUP BY message_type
            ORDER BY count DESC
        ''', (session_id,))
        recent_topics = cursor.fetchall()
        
        # Get user preferences
        cursor.execute('SELECT preference_type, preference_value FROM user_preferences WHERE session_id = ?', (session_id,))
        preferences = cursor.fetchall()
        
        conn.close()
        
        return {
            'profile': {
                'name': profile[2] if profile else None,
                'interests': profile[3] if profile else None,
                'communication_style': profile[4] if profile else None,
                'expertise_level': profile[5] if profile else None,
                'interaction_count': profile[7] if profile else 0
            },
            'recent_topics': [{'type': r[0], 'count': r[1]} for r in recent_topics],
            'preferences': {r[0]: r[1] for r in preferences}
        }

    def analyze_conversation_patterns(self, session_id: str) -> Dict[str, Any]:
        """Analyze user conversation patterns for personalization"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Most common message types
        cursor.execute('''
            SELECT message_type, COUNT(*) as count
            FROM conversations 
            WHERE session_id = ?
            GROUP BY message_type
            ORDER BY count DESC
        ''', (session_id,))
        message_types = cursor.fetchall()
        
        # Communication patterns
        cursor.execute('''
            SELECT 
                AVG(LENGTH(user_message)) as avg_message_length,
                COUNT(*) as total_messages,
                COUNT(DISTINCT DATE(timestamp)) as active_days
            FROM conversations 
            WHERE session_id = ?
        ''', (session_id,))
        patterns = cursor.fetchone()
        
        conn.close()
        
        return {
            'preferred_topics': [{'type': r[0], 'frequency': r[1]} for r in message_types],
            'communication_style': {
                'avg_message_length': patterns[0] if patterns[0] else 0,
                'total_messages': patterns[1] if patterns[1] else 0,
                'engagement_level': 'high' if patterns[1] and patterns[1] > 20 else 'medium' if patterns[1] and patterns[1] > 5 else 'low'
            }
        }

    def update_user_preference(self, session_id: str, preference_type: str, preference_value: str):
        """Update user preferences"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO user_preferences 
            (session_id, preference_type, preference_value, created_at, updated_at)
            VALUES (?, ?, ?, datetime('now'), datetime('now'))
        ''', (session_id, preference_type, preference_value))
        
        conn.commit()
        conn.close()

# Global memory instance
conversation_memory = ConversationMemory()
