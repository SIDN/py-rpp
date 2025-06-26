import socket
import ssl
import struct
from rpp.model.config import Config
from rpp.model.epp.epp_1_0 import EppType, Epp
from rpp.model.epp.common_commands import login, logout
from xsdata.formats.dataclass.parsers import XmlParser
from xsdata.formats.dataclass.context import XmlContext
from xsdata.formats.dataclass.serializers import XmlSerializer
from xsdata.formats.dataclass.serializers.config import SerializerConfig
from xsdata.formats.dataclass.parsers.config import ParserConfig

config = SerializerConfig(pretty_print=True)
serializer = XmlSerializer(config=config)

parser_config = ParserConfig()
parser_context = XmlContext()
parser = XmlParser(context=parser_context, config=parser_config)

class EppClient:
    def __init__(self, host: str, port: int = 700, timeout: float = 10.0):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.context = ssl.create_default_context()

        self.connected = False
        self.logged_in = False

    def login(self, cfg: Config):

        if not self.connected:
            self.connect()
            self.connected = True

        epp_request = login(cl_id=cfg.epp_client_id, pw=cfg.epp_password, version="1.0", lang="en",
                             obj_uri=['urn:ietf:params:xml:ns:domain-1.0',
                                      'urn:ietf:params:xml:ns:contact-1.0'],
                             ext_uri=['http://rxsd.domain-registry.nl/sidn-ext-epp-1.0',
                                      'urn:ietf:params:xml:ns:secDNS-1.1']
                            )
        # xml_output = serializer.render(epp_request)
        # print(f"login xml: {xml_output}")

        epp_response = self.send_command(epp_request)
        #print(f"Response 1 from EPP server: {epp_response}")
        #login_response = parser.from_string(epp_response, EppType)
        
        #print(f"Response 2 from EPP server: {login_response}")

        self.logged_in = True
        return epp_response
    
    def logout(self):
    
        epp_request = logout(trId="tr12345")
        # xml_output = serializer.render(epp_request)
        # print(f"logout xml: {xml_output}")

        epp_response = self.send_command(epp_request)
        #print(f"Response from EPP server: {response}")
        #response = parser.from_string(response, EppType)

        self.logged_in = False
        self.connected = False

        self.tls_sock.close()

        return epp_response

    def connect(self):
        sock = socket.create_connection((self.host, self.port), timeout=self.timeout)
        # Receive 4-byte length prefix
        self.tls_sock = self.context.wrap_socket(sock, server_hostname=self.host)
        header = self._recv_exact(self.tls_sock, 4)
        if len(header) < 4:
            raise RuntimeError("Failed to read response length header")
                
        response_length = struct.unpack(">I", header)[0] - 4
        response_data = self._recv_exact(self.tls_sock, response_length)
        self.connected = True
        return response_data.decode("utf-8", errors="replace")


    def send_command(self, epp_request: Epp) -> str:
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
                
        return parser.from_string(response_data.decode("utf-8", errors="replace"), Epp)

    def _recv_exact(self, conn, num_bytes: int) -> bytes:
        """Receive exactly num_bytes or raise."""
        buf = b""
        while len(buf) < num_bytes:
            chunk = conn.recv(num_bytes - len(buf))
            if not chunk:
                raise ConnectionError("Connection closed before expected bytes were received")
            buf += chunk
        return buf
