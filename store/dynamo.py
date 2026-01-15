# store/dynamo.py
import boto3
import time

table = boto3.resource("dynamodb").Table("race-ai-approvals")

def create_approval(item: dict):
    now = int(time.time())
    item["created_at"] = now
    item["updated_at"] = now
    table.put_item(Item=item)

def update_approval(approval_id, updates: dict):
    updates["updated_at"] = int(time.time())
    table.update_item(
        Key={"approval_id": approval_id},
        UpdateExpression="SET " + ", ".join(f"{k}=:{k}" for k in updates),
        ExpressionAttributeValues={f":{k}": v for k, v in updates.items()}
    )

def get_approval(approval_id):
    return table.get_item(Key={"approval_id": approval_id}).get("Item")
