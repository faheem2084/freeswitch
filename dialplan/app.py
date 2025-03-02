from fastapi import FastAPI
from fastapi.responses import Response

app = FastAPI()

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
    return Response(content=xml_content, media_type="application/xml")


@app.get("/directory")
@app.post("/directory")  # Endpoint for directory
def get_directory():
    xml_content = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<document type="freeswitch/xml">
  <section name="directory" description="Remote Directory">
    <domain name="$${domain}">
      <user id="1000">
        <params>
          <param name="password" value="1234"/>
          <param name="vm-password" value="1000"/>
        </params>
        <variables>
          <variable name="user_context" value="default"/>
          <variable name="effective_caller_id_name" value="Extension 1000"/>
          <variable name="effective_caller_id_number" value="1000"/>
        </variables>
      </user>
    </domain>
  </section>
</document>
"""
    return Response(content=xml_content, media_type="application/xml")

