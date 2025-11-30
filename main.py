from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

# ---------------- MODELS ----------------
class UpdateMembersRequest(BaseModel):
    groupName: str
    members: int

class SendMessageRequest(BaseModel):
    groupName: str
    userId: str
    username: Optional[str]
    fullName: Optional[str]
    profilePic: Optional[str]
    message: str

class MessageResponse(BaseModel):
    userId: str
    username: Optional[str]
    fullName: Optional[str]
    profilePic: Optional[str]
    message: str
    timestamp: datetime

# ---------------- STORAGE ----------------
members_count = {
    "Cyber Security Chat": 502,
    "Tech Talk Community": 510,
    "Business Networking": 520,
    "Startup Founders Group": 505,
    "Digital Marketing Hub": 508,
    "Crypto & Investment 💎": 1050,
    "Tech Entrepreneurs ⚡": 1200,
    "Cybersecurity Experts 🔒": 1105,
    "Startup Founders 🚀": 1300,
    "NFT & Art Collectors 🎨": 1250
}

messages = { group_name: [] for group_name in members_count.keys() }

# ---------------- APP INIT ----------------
app = FastAPI(title="Intelligent Space Group Chat Backend")

# Allow CORS for your frontend (use your domain instead of "*" in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# ---------------- ENDPOINTS ----------------

@app.post("/update-members")
def update_members(request: UpdateMembersRequest):
    if request.groupName not in members_count:
        raise HTTPException(status_code=404, detail="Group not found")
    members_count[request.groupName] = request.members
    return {"message": f'Members for "{request.groupName}" updated', "members": request.members}

@app.post("/send-message")
def send_message(request: SendMessageRequest):
    if request.groupName not in messages:
        raise HTTPException(status_code=404, detail="Group not found")
    msg_data = {
        "userId": request.userId,
        "username": request.username,
        "fullName": request.fullName,
        "profilePic": request.profilePic,
        "message": request.message,
        "timestamp": datetime.utcnow()
    }
    messages[request.groupName].append(msg_data)
    return {"message": "Message sent successfully"}

@app.get("/messages/{group_name}", response_model=List[MessageResponse])
def get_messages(group_name: str):
    if group_name not in messages:
        raise HTTPException(status_code=404, detail="Group not found")
    return messages[group_name]

@app.get("/members/{group_name}")
def get_members(group_name: str):
    if group_name not in members_count:
        raise HTTPException(status_code=404, detail="Group not found")
    return {"groupName": group_name, "members": members_count[group_name]}
