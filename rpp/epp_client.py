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

config = SerializerConfig(pretty_print=True)
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

    def login(self, cfg: Config, username: str, password: str) -> bool:

        if not self.connected:
            self.connect()

        epp_request = login(cl_id=username, pw=password, version="1.0", lang="en",
                             obj_uri=cfg.rpp_epp_objects,
                             ext_uri=cfg.rpp_epp_extensions
                            )

        epp_response = self.send_command(epp_request)
        ok, epp_status, message = is_ok_response(epp_response)
        if ok:
            #logger.info(f"Login successful for client: {username}")
            self.logged_in = True
            return True #, to_base_response(epp_response)
            #raise RuntimeError(f"Login failed: {epp_response.response.result[0].msg.value}")
        else:
            #logger.info(f"Login failed for client: {username}, error: {message}, code: {epp_status}")
            #return False, to_base_response(epp_response)
            raise EppException(status_code=403, epp_response=epp_response)
        
        #self.logged_in = True
        #return epp_response

    def logout(self, client_trid: str = None) -> Epp:
        self.logged_in = False
        self.connected = False
    
        try:
            epp_request = logout(trId=client_trid if client_trid else random_tr_id())
            epp_response = self.send_command(epp_request)
            ok, epp_status, message = is_ok_response(epp_response)
            if ok:
                logger.info("Logout successful")
            else:
                logger.error(f"Logout failed: {message}, code: {epp_status}")
        finally:
            self.tls_sock.close()
            self.tls_sock = None

        return epp_response

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
        logger.info(f"Received greeting from EPP server: {serializer.render(epp_response)}")

        self.greeting = epp_response.greeting
        return self.greeting


    def send_command(self, epp_request: Epp) -> Epp:
        xml_payload = serializer.render(epp_request)
        print(f"send xml: {xml_payload}")

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
        print(f"Response from EPP server: {response_data.decode('utf-8')}")
                
        response_str = response_data.decode("utf-8")
        epp_response = parser.from_string(response_str, Epp)
        logger.debug(f"Response XML object: {serializer.render(epp_response)}")
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
