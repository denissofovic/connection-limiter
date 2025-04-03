import os
from supabase import create_client,Client
import json
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')
supabase : Client = create_client(SUPABASE_URL, SUPABASE_KEY)

async def fetch_connects(member_id):
    try:
        response = (supabase.table("connections")
            .select("num_of_connects")
            .eq("member_id", member_id)
            .execute()
        )
        
        data = response.data
        
        if not data:
            return None
            
        num_of_connects = data[0]['num_of_connects']
        return num_of_connects
        
    except Exception as e:
        print(f"Error fetching connects: {e}")
        return None

async def increment_connects(member_id,num_of_connects):
    try:
        response = (
            supabase.table("connections")
            .update({"num_of_connects": num_of_connects + 1})
            .eq("member_id", member_id)
            .execute()
        )

        return True

    except Exception as e:
        print(e)


async def create_row(member_id):
    try:
        response = (
            supabase.table("connections")
            .insert({"member_id": member_id, "num_of_connects": 0})
            .execute()
        )
    
    except Exception as e:
        print(e)