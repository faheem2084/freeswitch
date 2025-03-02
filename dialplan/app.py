from fastapi import FastAPI
from fastapi.responses import Response

app = FastAPI()

@app.get("/")
@app.post("/")  # Allow both GET and POST
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