import os
from supabase import create_client, Client

class DevelopmentConfig:
    SUPABASE_URL = "https://ajdfitvuaqhxfpxbrvet.supabase.co"
    SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFqZGZpdHZ1YXFoeGZweGJydmV0Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTczNzg0NjM0NSwiZXhwIjoyMDUzNDIyMzQ1fQ.AMu0M0jYJBvcDDFKWU4TPHUsFeqHXJLuxGppGI1LKk0"
    SECRET_KEY = 'B!1weNAt1T*%kvhUI*S'

config = {
    'development': DevelopmentConfig
}

def get_supabase_client() -> Client:
    config_obj = config.get('development')  # Cambiar según el entorno si es necesario
    if not config_obj.SUPABASE_URL or not config_obj.SUPABASE_KEY:
        raise ValueError("SUPABASE_URL y SUPABASE_KEY deben estar configurados correctamente.")
    
    return create_client(config_obj.SUPABASE_URL, config_obj.SUPABASE_KEY)