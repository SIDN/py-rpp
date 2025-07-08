import re
import socket
import ssl
import struct
import logging
from rpp.common import EppException
from rpp.model.config import Config
from rpp.model.epp.epp_1_0 import EppType, Epp, GreetingType
from rpp.model.epp.common_commands import login, logout
from xsdata.formats.dataclass.parsers import XmlParser
from xsdata.formats.dataclass.context import XmlContext
from xsdata.formats.dataclass.serializers import XmlSerializer
from xsdata.formats.dataclass.serializers.config import SerializerConfig
from xsdata.formats.dataclass.parsers.config import ParserConfig

from rpp.model.epp.helpers import random_tr_id
from rpp.model.rpp.common_converter import is_ok_response, to_base_response

logger = logging.getLogger('uvicorn.error')

config = SerializerConfig(
    pretty_print=True,
)

ns_map = {
    "epp": "urn:ietf:params:xml:ns:epp-1.0",
    "domain": "urn:ietf:params:xml:ns:domain-1.0",
    "contact": "urn:ietf:params:xml:ns:contact-1.0",
    "host": "urn:ietf:params:xml:ns:host-1.0",
    "secDNS": "urn:ietf:params:xml:ns:secDNS-1.1",
    "sidn-ext-epp": "urn:sidn:xml:epp:sidn-ext-epp-1.0",
    "rgp": "urn:ietf:params:xml:ns:rgp-1.0",
}

serializer = XmlSerializer(config=config)

parser_config = ParserConfig()
parser_context = XmlContext()
parser = XmlParser(context=parser_context, config=parser_config)

class EppClient:
    def __init__(self, cfg: Config):
        self.host = cfg.rpp_epp_host
        self.port = cfg.rpp_epp_port
        self.timeout = cfg.rpp_epp_timeout
        self.context = ssl.create_default_context()

        self.connected = False
        self.logged_in = False
        self.greeting: GreetingType = None

    def login(self, cfg: Config, username: str, password: str) -> tuple[bool, Epp, str]:

        if not self.connected:
            self.connect()

        epp_request = login(cl_id=username, pw=password, version="1.0", lang="en",
                             obj_uri=cfg.rpp_epp_objects,
                             ext_uri=cfg.rpp_epp_extensions
                            )

        epp_response = self.send_command(epp_request, login=True)
        ok, epp_status, message = is_ok_response(epp_response)
        if ok:
            self.logged_in = True
            return True, epp_response, message 
        return False, epp_response, message

    def logout(self, client_trid: str = None) -> tuple[bool, Epp, str]:
        self.logged_in = False
        self.connected = False

        ok, message, epp_response = None, None, None
        try:
            epp_request = logout(trId=client_trid if client_trid else random_tr_id())
            epp_response = self.send_command(epp_request)
            ok, epp_status, message = is_ok_response(epp_response)
        finally:
            self.tls_sock.close()
            self.tls_sock = None

        return ok, epp_response, message

    def connect(self) -> GreetingType:
        sock = socket.create_connection((self.host, self.port), timeout=self.timeout)
        # Receive 4-byte length prefix
        self.tls_sock = self.context.wrap_socket(sock, server_hostname=self.host)
        header = self._recv_exact(self.tls_sock, 4)
        if len(header) < 4:
            raise RuntimeError("Failed to read response length header")
                
        response_length = struct.unpack(">I", header)[0] - 4
        response_data = self._recv_exact(self.tls_sock, response_length)
        self.connected = True

        response_str = response_data.decode('utf-8')
        epp_response = parser.from_string(response_str, Epp)
        logger.info(f"Received greeting from EPP server: {serializer.render(epp_response, ns_map=ns_map)}")

        self.greeting = epp_response.greeting
        return self.greeting


    def send_command(self, epp_request: Epp, login: bool =False) -> Epp:
        xml_payload = serializer.render(epp_request, ns_map=ns_map)
        if login:
            masked_xml_payload = re.sub(r"(<.*:pw>)(.*?)(</.*:pw>)", r"\1********\3", xml_payload, flags=re.DOTALL)
            logger.info(f"send EPP request: {masked_xml_payload}")
        else:
            logger.info(f"send EPP request: {xml_payload}")

        payload_bytes = xml_payload.encode("utf-8")
        total_length = len(payload_bytes) + 4
        msg = struct.pack(">I", total_length) + payload_bytes

        self.tls_sock.sendall(msg)

        # Receive 4-byte length prefix
        header = self._recv_exact(self.tls_sock, 4)
        if len(header) < 4:
            raise RuntimeError("Failed to read response length header")
        
        response_length = struct.unpack(">I", header)[0] - 4
        response_data = self._recv_exact(self.tls_sock, response_length)
        #logger.info(f"Response from EPP server: {response_data.decode('utf-8')}")
                
        #response_str = response_data.decode("utf-8")
        epp_response = parser.from_string(response_data.decode("utf-8"), Epp)
        logger.debug(f"Response XML object: {serializer.render(epp_response, ns_map=ns_map)}")
        return epp_response
      
        

    def _recv_exact(self, conn, num_bytes: int) -> bytes:
        """Receive exactly num_bytes or raise."""
        buf = b""
        while len(buf) < num_bytes:
            chunk = conn.recv(num_bytes - len(buf))
            if not chunk:
                raise ConnectionError("Connection closed before expected bytes were received")
            buf += chunk
        return buf
