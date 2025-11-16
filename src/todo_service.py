import boto3
from botocore.exceptions import ClientError
from typing import List, Optional, Dict, Any
from .models import Todo

class TodoService:
    def __init__(self, table_name: str = 'todos'):
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table(table_name)
    
    def get_all(self, /, completed: Optional[bool] = None) -> List[Dict[str, Any]]:
        try:
            response = self.table.scan()
            todos = [Todo.from_dict(item).to_dict() for item in response['Items']]
            
            if completed is not None:
                todos = [t for t in todos if t['completed'] == completed]
            
            return sorted(todos, key=lambda x: x['created_at'])
        except ClientError as e:
            raise RuntimeError(f"Failed to retrieve todos: {e}")
    
    def get_by_id(self, todo_id: str, /) -> Optional[Dict[str, Any]]:
        try:
            response = self.table.get_item(Key={'id': todo_id})
            if 'Item' in response:
                return Todo.from_dict(response['Item']).to_dict()
            return None
        except ClientError as e:
            raise RuntimeError(f"Failed to retrieve todo: {e}")
    
    def create(self, title: str, /) -> Dict[str, Any]:
        if not (title := title.strip()):
            raise ValueError("Title cannot be empty")
        
        todo = Todo(title=title)
        try:
            self.table.put_item(Item=todo.to_dict())
            return todo.to_dict()
        except ClientError as e:
            raise RuntimeError(f"Failed to create todo: {e}")
    
    def update(self, todo_id: str, /, **updates) -> Optional[Dict[str, Any]]:
        try:
            # First check if item exists
            response = self.table.get_item(Key={'id': todo_id})
            if 'Item' not in response:
                return None
            
            todo = Todo.from_dict(response['Item'])
            todo.update(**updates)
            
            self.table.put_item(Item=todo.to_dict())
            return todo.to_dict()
        except ClientError as e:
            raise RuntimeError(f"Failed to update todo: {e}")
    
    def delete(self, todo_id: str, /) -> bool:
        try:
            response = self.table.delete_item(
                Key={'id': todo_id},
                ReturnValues='ALL_OLD'
            )
            return 'Attributes' in response
        except ClientError as e:
            raise RuntimeError(f"Failed to delete todo: {e}")
    
    def clear_all(self) -> None:
        """For testing purposes only."""
        try:
            response = self.table.scan()
            with self.table.batch_writer() as batch:
                for item in response['Items']:
                    batch.delete_item(Key={'id': item['id']})
        except ClientError as e:
            raise RuntimeError(f"Failed to clear todos: {e}")
