# Chat System for Lost & Found Application

## Overview

The chat system enables direct communication between users who lost items and users who found items. It's designed to facilitate the recovery process by allowing users to verify item details, coordinate meetups, and exchange information securely.

## Key Features

✅ **Direct Messaging** - Users can chat directly about specific lost/found items  
✅ **Report-Based Conversations** - Each conversation is linked to specific lost and found reports  
✅ **Read Receipts** - Track which messages have been read  
✅ **Unread Count** - See how many unread messages you have  
✅ **Access Control** - Only report owners can participate in conversations  
✅ **Auto-Deduplication** - Prevents duplicate conversations for the same report pair  

## Architecture

### Models

#### Conversation
Represents a chat conversation between two users about specific reports.

**Fields:**
- `lost_report` - Reference to the lost item report
- `found_report` - Reference to the found item report
- `lost_user` - User who reported the lost item
- `found_user` - User who reported the found item
- `is_active` - Whether the conversation is still active
- `created_at` - When the conversation started
- `updated_at` - Last activity timestamp

**Constraints:**
- Unique combination of (lost_report, found_report)
- Ensures one conversation per report pair

#### Message
Represents individual messages within a conversation.

**Fields:**
- `conversation` - Parent conversation
- `sender` - User who sent the message
- `content` - Message text
- `is_read` - Read status
- `created_at` - Message timestamp

## API Endpoints

All endpoints require authentication with JWT token.

### Base URL: `/api/chat/`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/conversations/` | List user's conversations |
| POST | `/conversations/` | Create new conversation |
| GET | `/conversations/{id}/messages/` | Get conversation messages |
| POST | `/conversations/{id}/send_message/` | Send a message |
| GET | `/conversations/unread_count/` | Get unread count |
| GET | `/messages/` | List all user's messages |
| POST | `/messages/{id}/mark_read/` | Mark message as read |

See [API_DOCUMENTATION.md](./API_DOCUMENTATION.md) for detailed endpoint documentation.

## Usage Examples

### Creating a Conversation

```python
import requests

# User who lost item creates conversation with user who found it
response = requests.post(
    'http://localhost:8000/api/chat/conversations/',
    headers={'Authorization': f'Bearer {token}'},
    json={
        'lost_report_id': 1,  # Your lost report
        'found_report_id': 5  # Matched found report
    }
)

conversation = response.json()
print(f"Conversation created with ID: {conversation['id']}")
```

### Sending a Message

```python
# Send a message in the conversation
response = requests.post(
    f'http://localhost:8000/api/chat/conversations/{conversation_id}/send_message/',
    headers={'Authorization': f'Bearer {token}'},
    json={
        'content': 'Hi! I think you found my laptop. It has a sticker on it.'
    }
)

message = response.json()
```

### Getting Messages

```python
# Retrieve all messages in a conversation
response = requests.get(
    f'http://localhost:8000/api/chat/conversations/{conversation_id}/messages/',
    headers={'Authorization': f'Bearer {token}'}
)

messages = response.json()
for msg in messages:
    print(f"{msg['sender']['username']}: {msg['content']}")
```

## Integration with Frontend

### Workflow

1. **User finds a match** - From the matches list, user clicks "Contact"
2. **Create conversation** - Frontend calls `POST /api/chat/conversations/`
3. **Open chat interface** - Navigate to chat screen with conversation ID
4. **Load messages** - Call `GET /api/chat/conversations/{id}/messages/`
5. **Send messages** - Use `POST /api/chat/conversations/{id}/send_message/`
6. **Poll for updates** - Periodically fetch new messages (or use WebSockets)

### UI Components Needed

- **Conversation List** - Shows all active conversations with last message preview
- **Chat Window** - Displays messages in a conversation
- **Message Input** - Text field to compose and send messages
- **Unread Badge** - Shows number of unread messages
- **User Info** - Display other participant's profile

### Example React Component Structure

```jsx
// ConversationList.jsx - List all conversations
// ChatWindow.jsx - Display messages and send new ones
// MessageItem.jsx - Individual message bubble
// ChatInput.jsx - Message composition area
```

## Security & Permissions

### Authorization Rules

1. **View Conversations** - Users can only see conversations they're part of
2. **Create Conversations** - Users can only create conversations for their own reports
3. **Send Messages** - Users can only send messages in their own conversations
4. **Read Messages** - Users can only read messages in their conversations

### Validation

- Lost report must have `report_type='lost'`
- Found report must have `report_type='found'`
- User must own one of the reports to create conversation
- Message content cannot be empty

## Testing

Run the test suite:

```bash
python manage.py test chat
```

### Test Coverage

- ✅ Creating conversations
- ✅ Sending messages
- ✅ Retrieving messages
- ✅ Unauthorized access prevention
- ✅ Unread message counting
- ✅ Auto-marking messages as read

## Database Migrations

The chat system migrations are in `chat/migrations/0001_initial.py`.

To apply migrations:

```bash
python manage.py migrate chat
```

## Admin Interface

Access the Django admin at `/admin/` to:

- View all conversations
- Read messages
- Filter by date, read status, users
- Search conversations and messages

## Performance Considerations

### Optimizations Implemented

1. **Select Related** - Preload related users and reports to reduce queries
2. **Prefetch Related** - Load messages efficiently
3. **Indexing** - Created indexes on foreign keys and timestamps
4. **Read Status Bulk Update** - Mark multiple messages as read in one query

### Recommended Enhancements

For production at scale:

- Implement pagination for message lists
- Add database indexes on commonly queried fields
- Consider caching conversation lists
- Implement WebSocket for real-time updates
- Add message retention policies

## Future Enhancements

Potential features to add:

- 📎 **File Attachments** - Share images of items
- 🔍 **Search Messages** - Find specific messages in conversations
- 🗑️ **Delete Messages** - Allow users to delete their messages
- ✏️ **Edit Messages** - Edit recently sent messages
- 📍 **Location Sharing** - Share meetup locations
- 🔔 **Push Notifications** - Real-time message notifications
- ⌨️ **Typing Indicators** - Show when other user is typing
- 👁️ **Online Status** - Show if user is online
- ⭐ **Message Reactions** - React to messages with emojis
- 🔒 **Archive Conversations** - Archive completed conversations

## Troubleshooting

### Common Issues

**Problem:** "You are not a participant in this conversation"  
**Solution:** Ensure you own either the lost or found report in the conversation

**Problem:** Messages not appearing  
**Solution:** Check authentication token is valid and user has access to conversation

**Problem:** Cannot create conversation  
**Solution:** Verify report IDs are correct and reports have correct types (lost/found)

## Support & Documentation

- Report issues: Contact development team
- For questions: Check API documentation first

## Version History

- **v1.0** (2025-11-10) - Initial release
  - Basic messaging functionality
  - Conversation management
  - Read receipts
  - Unread count

---

**Developed for LOAF - Lost & Found Application**
