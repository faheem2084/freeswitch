# freeswitch build
docker build --build-arg USER=************* --build-arg TOKEN=******************** -t freeswitch .


This docker uses mod_xml_curl to fetch xml dialplan from remote http server. Currently Python/FastAPI is use to return xml.
