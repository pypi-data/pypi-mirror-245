message = {"Options_1": '''\
OPTIONS sip:{dest_ip}:{dest_port};transport={transport} SIP/2.0
Call-ID: {callId}
CSeq: 1 OPTIONS
To: <sip:{dest_ip}:{dest_port}>
From: <sip:{user}@{source_ip}:{source_port}>;tag=snl_{fromTag}
User-Agent: OpenScape Voice V9R0
Content-Length: 0
Max-Forwards: 70
Via: SIP/2.0/{transport} {source_ip}:{source_port};branch={viaBranch}
''',
		"200_OK_Notify":'''
SIP/2.0 200 OK
Contact: Will be overwritten by incoming NOTIFY
Call-ID: Will be overwritten by incoming NOTIFY
CSeq: Will be overwritten by incoming NOTIFY
From: Will be overwritten by incoming NOTIFY
To: Will be overwritten by incoming NOTIFY
Via: Will be overwritten by incoming NOTIFY
Content-Type: application/sdp
Content-Length: 0
''',
        "Subscribe_secondary":'''\
SUBSCRIBE sip:{user}@{dest_ip}:{dest_port};transport={transport} SIP/2.0
Call-ID: {callId}
CSeq: 1 SUBSCRIBE
To: <sip:{user}@{dest_ip}:{dest_port}>
From: "{primary}" <sip:{user}@{dest_ip}:{dest_port}>;tag=snl_{fromTag}
User-Agent: optiPoint 420 Advance/V7 V7 R0.16.1/10.2.31.5
Content-Length: 0
Max-Forwards: 70
Via: SIP/2.0/{transport} {source_ip}:{primary_port};branch={viaBranch}
Accept: application/keyset-info+xml
Allow: NOTIFY
Expires: {expires}
Event: keyset-info
Contact: "{primary}" <sip:{user}@{source_ip}:{primary_port};transport={transport}>
''',
         "Register_secondary":'''\
REGISTER sip:{dest_ip}:{dest_port};transport={transport} SIP/2.0
Call-ID: {callId}
CSeq: 1 REGISTER
To: <sip:{user}@{dest_ip}:{dest_port}>
From: "{user}" <sip:{user}@{dest_ip}:{dest_port}>;tag=snl_{fromTag}
User-Agent: optiPoint 420 Advance/V7 V7 R0.16.1/10.2.31.5
Content-Length: 0
Max-Forwards: 70
Via: SIP/2.0/{transport} {source_ip}:{source_port};branch={viaBranch}
Accept: application/dls-contact-me
Supported: X-Siemens-Proxy-State
Contact: "{user}" <sip:{user}@{source_ip}:{primary_port};transport={transport}>;expires={expires}
''',
         "Register_primary":'''\
REGISTER sip:{dest_ip}:{dest_port};transport={transport} SIP/2.0
Call-ID: {callId}
CSeq: 1 REGISTER
To: <sip:{user}@{dest_ip}:{dest_port}>
From: "{user}" <sip:{user}@{dest_ip}:{dest_port}>;tag=snl_{fromTag};epid={epid}
User-Agent: optiPoint 420 Advance/V7 V7 R0.16.1/10.2.31.5
Content-Length: 0
Max-Forwards: 70
Via: SIP/2.0/{transport} {source_ip}:{source_port};branch={viaBranch}
Accept: application/dls-contact-me
Supported: X-Siemens-Proxy-State
Contact: "{user}" <sip:{user}@{source_ip}:{source_port};transport={transport}>;expires={expires}
''',

           "Register_1": '''\
REGISTER sip:{dest_ip}:{dest_port};transport={transport} SIP/2.0
Call-ID: {callId}
CSeq: 1 REGISTER
To: <sip:{user}@{dest_ip}:{dest_port}>
From: "{user}" <sip:{user}@{dest_ip}:{dest_port}>;tag=snl_{fromTag}
User-Agent: Python tools
Content-Length: 0
Max-Forwards: 70
Via: SIP/2.0/{transport} {source_ip}:{source_port};branch={viaBranch}
Accept: application/dls-contact-me
Supported: X-Siemens-Proxy-State
Contact: "{user}" <sip:{user}@{source_ip}:{source_port};transport={transport}>;expires={expires}
''',
           "Register_2": '''\
REGISTER sip:{dest_ip}:{dest_port};transport={transport} SIP/2.0
Call-ID: {callId}
CSeq: 1 REGISTER
To: <sip:{user}@{dest_ip}:{dest_port}>
From: "{user}" <sip:{user}@{dest_ip}:{dest_port}>;tag=snl_{fromTag};epid={epid}
User-Agent: Python tools
Content-Length: 0
Max-Forwards: 70
Via: SIP/2.0/{transport} {source_ip}:{source_port};branch={viaBranch}
Accept: application/dls-contact-me
Supported: X-Siemens-Proxy-State
Contact: "{user}" <sip:{user}@{source_ip}:{source_port};transport={transport}>;expires={expires}
''',
           "Invite_SDP_1": '''\
INVITE sip:{userB}@{dest_ip}:{dest_port};transport={transport} SIP/2.0
Via: SIP/2.0/{transport} {source_ip}:{source_port};branch={viaBranch}
From: {userA} <sip:{userA}@{dest_ip}:{dest_port}>;tag={fromTag}
To: <sip:{userB}@{dest_ip}:{dest_port};transport={transport}>
Contact: <sip:{userA}@{source_ip}:{source_port};transport={transport}>
Content-Type: application/sdp
Call-ID: {callId}
CSeq: 1 INVITE
Max-Forwards: 70
Content-Length: Will be overridden during creation

v=0
o=Anomymous {userA} 1234567890 IN IP4 {source_ip}
s=SIGMA is the best
c=IN IP4 {source_ip}
t=0 0
m=audio 6006 RTP/AVP 8 0 3
a=rtpmap:8 PCMA/8000
a=rtpmap:0 PCMU/8000
a=rtpmap:3 GSM/8000
m=video 6008 RTP/AVP 40
a=rtpmap:40 H263-1998/90000
''',
           "Trying_1": '''\
SIP/2.0 100 Trying
Call-ID: Will be overwritten by incoming INVITE
CSeq: Will be overwritten by incoming INVITE
From: Will be overwritten by incoming INVITE
To: Will be overwritten by incoming INVITE
Via: Will be overwritten by incoming INVITE
Content-Length: 0
''',
           "Ringing_1": '''\
SIP/2.0 180 Ringing
Call-ID: Will be overwritten by incoming INVITE
CSeq: Will be overwritten by incoming INVITE
From: Will be overwritten by incoming INVITE
To: Will be overwritten by incoming INVITE and a tag will be added
Via: Will be overwritten by incoming INVITE
Contact: <sip:{user}@{source_ip}:{source_port};transport={transport}>
Content-Length: 0
''',
           "200_OK_SDP_1": '''\
SIP/2.0 200 OK
Contact: <sip:{user}@{source_ip}:{source_port};transport={transport}>
Call-ID: Will be overwritten by incoming INVITE
CSeq: Will be overwritten by incoming INVITE
From: Will be overwritten by incoming INVITE
To: Will be overwritten by incoming INVITE and a tag will be added
Via: Will be overwritten by incoming INVITE
Content-Type: application/sdp
Content-Length: Will be overridden during creation

v=0
o=Anomymous {user} 1234567890 IN IP4 {source_ip}
s=SIGMA is the best
c=IN IP4 {source_ip}
t=0 0
m=audio 6006 RTP/AVP 8 0 3
a=rtpmap:8 PCMA/8000
a=rtpmap:0 PCMU/8000
a=rtpmap:3 GSM/8000
m=video 6008 RTP/AVP 40
a=rtpmap:40 H263-1998/90000
''',
           "Ack_1": '''\
ACK sip:{userB}@{dest_ip}:{dest_port};transport={transport};maddr={dest_ip} SIP/2.0
CSeq: 1 ACK
Via: SIP/2.0/{transport} {source_ip}:{source_port};branch={viaBranch}
To: Same as initial INVITE
From: Same as initial INVITE
Call-ID: Same as initial INVITE
Max-Forwards: 70
Content-Length: 0
''',
           "Bye_1": '''\
BYE sip:{userB}@{dest_ip}:{dest_port};transport={transport};maddr={dest_ip} SIP/2.0
Call-ID: Same as initial INVITE
CSeq: 2 BYE
Via: SIP/2.0/{transport} {source_ip}:{source_port};branch={viaBranch}
To: Same as initial INVITE
From: Same as initial INVITE
Max-Forwards: 70
Content-Length: 0
''',
           "200_OK_1": '''\
SIP/2.0 200 OK
Content-Length: 0
Call-ID: Will be overwritten by incoming BYE
CSeq: Will be overwritten by incoming BYE
From: Will be overwritten by incoming BYE
To: Will be overwritten by incoming BYE
Via: Will be overwritten by incoming BYE
''',
           "Notify_terminated_1": '''\
NOTIFY sip:{user}@{dest_ip}:{dest_port};transport={transport} SIP/2.0
Via: SIP/2.0/{transport} {source_ip};branch={viaBranch}
Max-Forwards: 70
From: {user} <sip:{user}@{source_ip}:{source_port};transport={transport}>
To: <sip:{user}@{dest_ip}:{dest_port};transport={transport}>
Call-ID: {callId}
CSeq: 465101717 NOTIFY
Contact: <sip:{user}@{source_ip}:{source_port};transport={transport}>
Event: keyset-info
Subscription-State: active;expires={expires}
User-Agent: OpenStage_60_V3 R1.41.0      SIP  130205
Content-Type: application/keyset-info+xml
Content-Length: 316

<?xml version="1.0"?>
<keyset-info xmlns="urn:ietf:params:xml:ns:keyset-info"
	version="0"
	entity="sip:{user}@{dest_ip}:{dest_port}">
	<ki-data> <ki-state>"unconfirmed"</ki-state> <ki-event>"unknown"</ki-event>  </ki-data>
	<di:dialog id="no-dialog"> 
		<di:state>terminated</di:state>
	</di:dialog>
</keyset-info>
''',
           "487_Request_Terminated": '''\
SIP/2.0 487 Request Terminated
Via: SIP/2.0/{transport} {dest_ip}:5060;branch={viaBranch}
From: <sip:{user}@{dest_ip}>;tag={fromTag}
To: {user} <sip:{user}@{source_ip}:{source_port}>
Call-ID: {callId}
CSeq: 1235 INVITE
Server: optiPoint 420 Standard/V7 V7 R2.1.0
Content-Length: 0
'''
           }
