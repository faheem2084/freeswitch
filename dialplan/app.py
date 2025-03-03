from fastapi import FastAPI, Response, Form, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, Boolean, TIMESTAMP, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Database connection URL (replace with your actual database URL)
DATABASE_URL = "postgresql://postgres:postgres@postgres:5432/freeswitch"

# Create the SQLAlchemy engine and session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Define the SQLAlchemy model
Base = declarative_base()

class FSDirectory(Base):
    __tablename__ = "fs_directory"

    id = Column(Integer, primary_key=True, index=True)
    domain = Column(String(255), nullable=False)
    user_id = Column(String(255), nullable=False)
    ha1 = Column(String(32), nullable=False)
    effective_caller_id_name = Column(String(255))
    effective_caller_id_number = Column(String(255))
    outbound_caller_id_name = Column(String(255))
    outbound_caller_id_number = Column(String(255))
    voicemail_enabled = Column(Boolean, default=True)
    user_context = Column(String(255), default="default")
    created_at = Column(TIMESTAMP, default=func.now())
    updated_at = Column(TIMESTAMP, default=func.now(), onupdate=func.now())

# Create the FastAPI app
app = FastAPI()

# Endpoint to return directory XML
@app.post("/directory")
def get_directory(
    domain: str = Form(...),  # Required form field
    user: str = Form(...)     # Required form field
):
    logger.debug(f"Received request: domain={domain}, user={user}")

    # Create a database session
    db = SessionLocal()

    try:
        # Query the database for the user
        user_data = db.query(FSDirectory).filter(
            FSDirectory.domain == domain,
            FSDirectory.user_id == user
        ).first()

        # If the user is not found, return a 404 error
        if not user_data:
            logger.error(f"User not found: domain={domain}, user={user}")
            raise HTTPException(status_code=404, detail="User not found")

        # Generate the XML content dynamically
        xml_content = f"""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
          <document type="freeswitch/xml">
            <section name="directory" description="Remote Directory">
              <domain name="{domain}">
                <user id="{user_data.user_id}">
                  <params>
                    <param name="a1-hash" value="{user_data.ha1}"/>
                    <param name="vm-password" value="{user_data.user_id}"/>
                  </params>
                  <variables>
                    <variable name="user_context" value="{user_data.user_context}"/>
                    <variable name="effective_caller_id_name" value="{user_data.effective_caller_id_name or 'Extension ' + user_data.user_id}"/>
                    <variable name="effective_caller_id_number" value="{user_data.effective_caller_id_number or user_data.user_id}"/>
                  </variables>

                </user>
              </domain>
            </section>
          </document>
          """
        # Return the XML response
        return Response(content=xml_content, media_type="application/xml", headers={"Cache-Control": "no-cache"})

    except Exception as e:
        logger.error(f"Error processing request: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

    finally:
        # Close the database session
        db.close()




@app.get("/dialplan")
@app.post("/dialplan")  # Allow both GET and POST
def get_dialplan():
    xml_content = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<document type="freeswitch/xml">
  <section name="dialplan" description="Remote Dialplan">
    <context name="default">
      <extension name="Demo">
        <condition field="destination_number" expression="^9196$">
          <action application="answer"/>
          <action application="playback" data="/usr/share/freeswitch/sounds/music/8000/danza-espanola-op-37-h-142-xii-arabesca.wav"/>
          <action application="echo"/>
          <action application="hangup"/>
        </condition>
      </extension>
    </context>
  </section>
</document>
"""
    return Response(content=xml_content, 
                    media_type="application/xml", 
                    headers={"Cache-Control": "no-cache"})

