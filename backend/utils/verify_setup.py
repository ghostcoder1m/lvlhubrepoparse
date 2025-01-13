import os
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials
from google.oauth2 import service_account
from google.cloud import storage

def verify_setup():
    """Verify the setup of API keys and service accounts."""
    print("Verifying setup...")
    
    # Load environment variables
    load_dotenv()
    print("\n1. Environment Variables:")
    env_vars = [
        'SECRET_KEY',
        'GOOGLE_CLOUD_PROJECT_ID',
        'GOOGLE_APPLICATION_CREDENTIALS',
        'FIREBASE_API_KEY',
        'FIREBASE_PROJECT_ID',
    ]
    
    for var in env_vars:
        value = os.getenv(var)
        print(f"  ✓ {var}: {'Present' if value else 'Missing'}")
    
    # Verify Google Cloud credentials
    print("\n2. Google Cloud Service Account:")
    try:
        credentials = service_account.Credentials.from_service_account_file(
            os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
        )
        print("  ✓ Service account credentials loaded successfully")
        
        # Test with Storage client
        storage_client = storage.Client(credentials=credentials)
        storage_client.list_buckets(max_results=1)
        print("  ✓ Successfully authenticated with Google Cloud")
    except Exception as e:
        print(f"  ✗ Error with Google Cloud credentials: {str(e)}")
    
    # Verify Firebase Admin SDK
    print("\n3. Firebase Admin SDK:")
    try:
        if not firebase_admin._apps:
            cred = credentials.Certificate(os.getenv('FIREBASE_ADMIN_SDK_PATH'))
            firebase_admin.initialize_app(cred)
        print("  ✓ Firebase Admin SDK initialized successfully")
    except Exception as e:
        print(f"  ✗ Error with Firebase Admin SDK: {str(e)}")
    
    print("\nSetup verification complete!")

if __name__ == "__main__":
    verify_setup() 