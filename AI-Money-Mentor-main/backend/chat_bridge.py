"""
AI Money Mentor - Chat Bridge
Connects Frontend to OpenClaw Agent Swarm with Database Storage
Uses OpenClaw CLI for agent communication
"""

import sqlite3
import subprocess
import json
import os
import uuid
from datetime import datetime
from typing import Optional, List, Dict, Any

from fastapi import HTTPException
from pydantic import BaseModel

# Database setup - use project's data directory
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'chat_history.db')
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

def init_db():
    """Initialize SQLite database for chat history"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chat_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            session_id TEXT NOT NULL,
            agent_id TEXT NOT NULL,
            role TEXT NOT NULL,
            message TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_user_session ON chat_messages(user_id, session_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_timestamp ON chat_messages(timestamp)')
    conn.commit()
    conn.close()

def store_message(user_id: str, session_id: str, agent_id: str, role: str, message: str):
    """Store a message in the database"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO chat_messages (user_id, session_id, agent_id, role, message)
        VALUES (?, ?, ?, ?, ?)
    ''', (user_id, session_id, agent_id, role, message))
    conn.commit()
    conn.close()

def get_chat_history(user_id: str, session_id: str, limit: int = 20) -> List[Dict[str, Any]]:
    """Retrieve chat history for context"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('''
        SELECT role, message, agent_id, timestamp
        FROM chat_messages
        WHERE user_id = ? AND session_id = ?
        ORDER BY timestamp DESC
        LIMIT ?
    ''', (user_id, session_id, limit))
    rows = cursor.fetchall()
    conn.close()
    
    # Reverse to get chronological order
    history = []
    for row in reversed(rows):
        history.append({
            'role': row['role'],
            'content': row['message'],
            'agent_id': row['agent_id'],
            'timestamp': row['timestamp']
        })
    return history

def send_to_agent(agent_id: str, message: str, session_id: str = None) -> str:
    """
    Send message to OpenClaw agent via CLI
    
    Uses: openclaw agent --agent <agent_id> --message <message> --session-id <session_id>
    """
    session_key = f"frontend:{session_id}" if session_id else None
    
    # Inject FY 2025-26 context for tax-related agents
    if agent_id in ('karvid', 'dhan-sarthi'):
        if any(kw in message.lower() for kw in ['tax', 'income', 'regime', '80c', '80d', 'deduction', 'slab', 'capital gain']):
            message = f"[Context: Current Financial Year is FY 2025-26 (AY 2026-27). Always use FY 2025-26 tax slabs and rules.] {message}"

    try:
        cmd = ['openclaw', 'agent', '--agent', agent_id, '--message', message]
        if session_key:
            cmd.extend(['--session-id', session_key])
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=120  # 2 minute timeout
        )
        
        if result.returncode != 0:
            # Fallback: return error message
            return f"[Agent {agent_id} error: {result.stderr.strip() or 'Unknown error'}]"
        
        # Parse the response
        response = result.stdout.strip()
        return response if response else "[No response from agent]"
        
    except subprocess.TimeoutExpired:
        return f"[Agent {agent_id} timed out after 2 minutes]"
    except Exception as e:
        return f"[Error reaching {agent_id}: {str(e)}]"

# FastAPI Models
class ChatRequest(BaseModel):
    message: str
    user_id: str
    session_id: Optional[str] = None
    agent_id: str = 'dhan-sarthi'

class ChatResponse(BaseModel):
    agent: str
    response: str
    session_id: str
    history_count: int

# Initialize database on import
init_db()

# Export for FastAPI router
__all__ = ['ChatRequest', 'ChatResponse', 'init_db', 'store_message', 'get_chat_history', 'send_to_agent']